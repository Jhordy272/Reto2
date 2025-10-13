from collections import defaultdict, deque
from time import time
import re, math

NOW = lambda: time()
ALPHA = 0.2            # EWMA para tasa
THRESHOLD = 4.0        # umbral de alerta (sigue siendo configurable)

# Palabras “peligrosas” con pesos (ampliadas)
KW = {
    "fatal":3.0, "exception":3.0, "error":3.0, "timeout":2.5,
    "refused":2.0, "denied":2.0, "unauthorized":2.5, "panic":3.0,
    "privilege":2.5, "escalation":2.5, "unauthorised":2.5, "unauth":2.0,
    "config":1.0, "changed":0.8, "manipulate":2.0, "tamper":2.5
}

NUM = re.compile(r'\b\d+\b')
UUID = re.compile(r'\b[0-9a-fA-F-]{8,}\b')

# patterns para detectar frases concretas (devuelven peso adicional y etiqueta)
PATTERNS = [
    (re.compile(r'unauthorized.*config|config.*unauthorized', re.I), (1.5, "unauthorized_config_pattern")),
    (re.compile(r'privileg(e|y).*escalat|escalation|privilege escalation', re.I), (2.0, "privilege_escalation_pattern")),
    (re.compile(r'unauthorized admin|admin access attempt', re.I), (2.0, "unauthorized_admin_pattern")),
    (re.compile(r'login denied|login failed', re.I), (1.5, "login_denied_pattern")),
]

def template(msg:str)->str:
    m = msg or ""
    m = NUM.sub("<num>", m)
    m = UUID.sub("<id>", m)
    return m.strip().lower()

# Baselines en memoria por servicio y plantilla
svc_rate = defaultdict(float)                         # service -> ewma rate
svc_events = defaultdict(lambda: deque(maxlen=3000))  # ts de últimos eventos por servicio
tpl_freq = defaultdict(int)                           # (service, tpl) -> count en ventana corta
tpl_window = defaultdict(lambda: deque(maxlen=2000))  # (service) -> deque de plantillas recientes
svc_kw_hist = defaultdict(int)                        # service -> contador de KW

# Nuevo: contabilizar actores por servicio para saber si son novedosos
svc_actor_counts = defaultdict(lambda: defaultdict(int))  # svc -> actor -> count

def score_keywords(msg:str)->float:
    s = (msg or "").lower()
    return sum(w for k,w in KW.items() if k in s)

def pattern_score(msg:str):
    s = msg or ""
    total = 0.0
    reasons = []
    for pat, (w, tag) in PATTERNS:
        if pat.search(s):
            total += w
            reasons.append(tag)
    return total, reasons

def update_baselines(service:str, msg:str, context:dict | None = None):
    ts = NOW()
    # tasa por servicio
    evq = svc_events[service]; evq.append(ts)
    if len(evq) >= 2:
        span = max(evq[-1]-evq[0], 1e-3)
        curr_rate = 60.0 * len(evq) / span
    else:
        curr_rate = 0.0
    svc_rate[service] = ALPHA*curr_rate + (1-ALPHA)*svc_rate[service]
    # plantilla
    tpl = template(msg)
    tpl_window[service].append(tpl)
    tpl_freq[(service, tpl)] += 1
    # keywords
    if score_keywords(msg) > 0:
        svc_kw_hist[service] += 1
    # actor counts (actualiza si viene actor/user en context)
    ctx = context or {}
    actor = ctx.get("user") or ctx.get("actor") or ctx.get("service") or ctx.get("ip")
    if actor:
        svc_actor_counts[service][actor] += 1

def compute_score(service:str, level:str, msg:str, context:dict)->tuple[float, list]:
    reasons = []
    score = 0.0

    # 0) pattern matches (fuerte)
    pat_score, pat_reasons = pattern_score(msg)
    if pat_score > 0:
        score += pat_score
        reasons.extend(pat_reasons)

    # 1) keywords
    sk = score_keywords(msg)
    if sk >= 3.0:
        score += min(3.0, sk)
        reasons.append(f"keyword:{sk:.1f}")
    elif sk > 0:
        score += min(1.5, sk/2.0)
        reasons.append(f"keyword:{sk:.1f}")

    # 2) burst por servicio (inst vs ewma)
    evq = svc_events[service]
    inst = len([t for t in evq if (NOW()-t)<=10.0])*6.0
    base = svc_rate[service] or 0.1
    ratio = inst/base
    if ratio > 4.0 and len(evq) > 10:
        add = min(2.0, ratio/4.0)
        score += add; reasons.append(f"burst:{ratio:.1f}")

    # 3) rare template dentro de ventana
    tpl = template(msg)
    recent = tpl_window[service]
    if len(recent) >= 50:
        freq = sum(1 for x in recent if x == tpl)
        if freq/len(recent) <= 0.05 and level.upper() in {"WARN","ERROR"}:
            score += 1.0; reasons.append("rare_template")

    # 4) context “sospechoso” (actor novelty)
    actor = (context or {}).get("user") or (context or {}).get("actor") or (context or {}).get("service") or (context or {}).get("ip")
    if actor:
        count = svc_actor_counts[service].get(actor, 0)
        # actor visto pocas veces -> más sospechoso
        if count <= 1:
            score += 1.0; reasons.append("actor_novel")
        elif count <= 3:
            score += 0.5; reasons.append("actor_few")

    # 5) nivel de severidad
    if level.upper() == "ERROR":
        score += 0.5; reasons.append("level_error")
    elif level.upper() == "CRITICAL":
        score += 1.0; reasons.append("level_critical")

    # return final
    return score, reasons
