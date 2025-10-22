# Very small, safe expression evaluator for simple boolean rules like:
# "amount < 5000 and vendor.trust_score > 0.8"
# We restrict names and builtins.
import operator, re

ALLOWED_NAMES = set()  # we only expose the context dict
ALLOWED_BUILTINS = {}

def _resolve_attr(obj, path):
    cur = obj
    for part in path.split("."):
        if isinstance(cur, dict):
            cur = cur.get(part)
        else:
            cur = getattr(cur, part, None)
    return cur

def eval_condition(expr: str, ctx: dict) -> bool:
    # Replace dotted identifiers with lookups from ctx
    tokens = re.findall(r"[A-Za-z_]\w*(?:\.[A-Za-z_]\w*)*", expr)
    local_vars = {}
    for t in tokens:
        if t in ("and","or","not","True","False"): 
            continue
        local_vars[t.replace(".","__")] = _resolve_attr(ctx, t)
        expr = re.sub(rf"\b{re.escape(t)}\b", t.replace(".","__"), expr)
    return bool(eval(expr, {"__builtins__": ALLOWED_BUILTINS}, local_vars))
