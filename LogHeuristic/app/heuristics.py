from collections import defaultdict, deque
from time import time
import re, math

NOW = lambda: time()
ALPHA = 0.2          
THRESHOLD = 4.0      

KW = {"fatal":3.0, "exception":3.0, "error":3.0, "timeout":2.5, "refused":2.0, "denied":2.0, "unauthorized":2.5, "panic":3.0}
NUM = re.compile(r'\b\d+\b'); UUID = re.compile(r'\b[0-9a-fA-F-]{8,}\b')

def template(msg:str)->str:
    m = msg or ""
    m = NUM.sub("<num>", m)
    m = UUID.sub("<id>", m)
    return m.strip().lower()

svc_rate = defaultdict(float)  
svc_events = defaultdict(lambda: deque(maxlen=3000)) 
tpl_freq = defaultdict(int)  
tpl_window = defaultdict(lambda: deque(maxlen=2000))  
svc_kw_hist = defaultdict(int) 

def score_keywords(msg:str)->float:
    s = msg.lower()
    return sum(w for k,w in KW.items() if k in s)

def update_baselines(service:str, msg:str):
    ts = NOW()
    evq = svc_events[service]; evq.append(ts)
    if len(evq) >= 2:
        span = max(evq[-1]-evq[0], 1e-3)
        curr_rate = 60.0 * len(evq) / span
    else:
        curr_rate = 0.0
    svc_rate[service] = ALPHA*curr_rate + (1-ALPHA)*svc_rate[service]

    tpl = template(msg)
    tpl_window[service].append(tpl)
    tpl_freq[(service, tpl)] += 1

    if score_keywords(msg) > 0: svc_kw_hist[service] += 1

def compute_score(service:str, level:str, msg:str, context:dict)->tuple[float, list]:
    reasons = []
    score = 0.0
    sk = score_keywords(msg)
    if sk >= 3.0:
        score += min(3.0, sk)
        reasons.append(f"keyword:{sk:.1f}")
    evq = svc_events[service]
    inst = len([t for t in evq if (NOW()-t)<=10.0])*6.0
    base = svc_rate[service] or 0.1
    ratio = inst/base
    if ratio > 4.0 and len(evq) > 10:
        add = min(2.0, ratio/4.0)
        score += add; reasons.append(f"burst:{ratio:.1f}")

    tpl = template(msg)
    recent = tpl_window[service]
    if len(recent) >= 50:
        freq = sum(1 for x in recent if x == tpl)
        if freq/len(recent) <= 0.05 and level.upper() in {"WARN","ERROR"}:
            score += 1.0; reasons.append("rare_template")

    actor = (context or {}).get("user") or (context or {}).get("actor") or (context or {}).get("service")
    if actor:
        actor_seen = (context or {}).get("actor_seen_count", 0)
        if actor_seen < 3:
            score += 0.5; reasons.append("actor_novel")
    if level.upper() == "ERROR":
        score += 0.5; reasons.append("level_error")

    return score, reasons
