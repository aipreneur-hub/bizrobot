from typing import Dict, Any
import os

def policy_filter(ctx: Dict[str, Any]) -> tuple[bool, str]:
    # Example: require currency and non-negative amount
    ok = "currency" in ctx and ctx.get("amount", 0) >= 0
    return ok, "policy OK" if ok else "policy violation: currency/amount"

def bias_filter(ctx: Dict[str, Any]) -> tuple[bool, str]:
    # Example heuristic: never auto-approve new vendors if amount > 3000
    if ctx.get("vendor", {}).get("is_new") and ctx.get("amount", 0) > 3000:
        return False, "bias: new vendor high amount"
    return True, "bias OK"

def risk_filter(ctx: Dict[str, Any]) -> tuple[bool, str]:
    # Example: mark high VAT as risk
    return (ctx.get("vat", 0) <= 20), "risk OK" if ctx.get("vat",0) <= 20 else "risk: vat high"

def check_file_exists(inputs):
    file_path = inputs.get("file_path")
    if not file_path:
        return False, "file_path missing"
    exists = os.path.exists(file_path)
    return exists, "File exists" if exists else "File not found"

def always_pass(inputs):
    return True, "OK"

FILTERS = {
    "file_path": check_file_exists,
    "default": always_pass,
}