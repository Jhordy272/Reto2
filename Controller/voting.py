from collections import Counter
from typing import List, Tuple

def majority_vote(values: List[float], precision: int = 2) -> Tuple[float, Counter]:
    r = [round(x, precision) for x in values]
    tally = Counter(r)
    top = max(tally.values())
    winners = sorted([v for v, c in tally.items() if c == top])
    if len(winners) == 1:
        return float(winners[0]), tally
    n = len(winners)
    mid = n // 2
    if n % 2 == 1:
        return float(winners[mid]), tally
    return float((winners[mid - 1] + winners[mid]) / 2), tally
