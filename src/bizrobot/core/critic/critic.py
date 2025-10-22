# bizrobot/core/critic/critic.py
from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
import re
import json

@dataclass
class Finding:
    criterion: str
    passed: bool
    severity: str  # "info" | "warn" | "block"
    message: str
    details: Dict[str, Any] = field(default_factory=dict)

@dataclass
class CritiqueResult:
    ok: bool
    score: float          # 0..100
    findings: List[Finding]
    summary: str

class Critic:
    """
    Lightweight heuristic critic for validating/ scoring model/tool outputs.
    No external deps. Deterministic. Safe to run in any environment.
    """

    def __init__(
        self,
        min_chars: int = 20,
        max_chars: int = 20000,
        required_keywords: Optional[List[str]] = None,
        banned_patterns: Optional[List[str]] = None,
        block_on_fail_keywords: bool = False,
        target_keywords_weight: float = 0.35,
        quality_weight: float = 0.45,
        style_weight: float = 0.20,
    ):
        self.min_chars = min_chars
        self.max_chars = max_chars
        self.required_keywords = [k.lower() for k in (required_keywords or [])]
        self.banned_patterns = [re.compile(p, re.I) for p in (banned_patterns or [])]
        self.block_on_fail_keywords = block_on_fail_keywords

        # weights sum to 1.0
        total = target_keywords_weight + quality_weight + style_weight
        self.w_kw = target_keywords_weight / total
        self.w_q = quality_weight / total
        self.w_st = style_weight / total

    # ---------- Public API ----------

    def evaluate(
        self,
        text: str,
        criteria: Optional[List[str]] = None,
        extras: Optional[Dict[str, Any]] = None,
    ) -> CritiqueResult:
        """Evaluate text against heuristics + optional criteria."""
        criteria = criteria or []
        findings: List[Finding] = []

        # 1) Basic sanity
        findings += self._check_length(text)
        findings += self._check_empty(text)
        findings += self._check_banned(text)

        # 2) Content fit
        if self.required_keywords:
            findings += self._check_required_keywords(text, self.required_keywords)

        # 3) Style/quality
        findings += self._check_placeholders(text)
        findings += self._check_shouting(text)
        findings += self._check_unbalanced_code_blocks(text)
        findings += self._check_json_blocks(text)

        # 4) Optional ad-hoc criteria (keyword presence)
        if criteria:
            findings += self._check_required_keywords(text, [c.lower() for c in criteria], tag="criterion")

        # Score
        score = self._score(text, findings)
        ok = self._decide_ok(findings)

        summary = self._summarize(findings, score)

        return CritiqueResult(ok=ok, score=score, findings=findings, summary=summary)

    def compare(self, a: str, b: str) -> Dict[str, Any]:
        """Return which text is better according to this critic."""
        ra = self.evaluate(a)
        rb = self.evaluate(b)
        better = "a" if ra.score >= rb.score else "b"
        return {"better": better, "score_a": ra.score, "score_b": rb.score, "result_a": ra, "result_b": rb}

    # ---------- Internals ----------

    def _check_length(self, text: str) -> List[Finding]:
        n = len(text)
        out = []
        if n < self.min_chars:
            out.append(Finding("length", False, "warn", f"Too short ({n} < {self.min_chars}).", {"length": n}))
        if n > self.max_chars:
            out.append(Finding("length", False, "block", f"Too long ({n} > {self.max_chars}).", {"length": n}))
        return out

    def _check_empty(self, text: str) -> List[Finding]:
        if not text or not text.strip():
            return [Finding("empty", False, "block", "Text is empty.")]
        return []

    def _check_banned(self, text: str) -> List[Finding]:
        out = []
        for pat in self.banned_patterns:
            if pat.search(text):
                out.append(Finding("banned_pattern", False, "block", f"Banned pattern matched: {pat.pattern}"))
        return out

    def _check_required_keywords(self, text: str, kws: List[str], tag: str = "required_keywords") -> List[Finding]:
        lower = text.lower()
        out = []
        missing = [k for k in kws if k not in lower]
        if missing:
            severity = "block" if self.block_on_fail_keywords else "warn"
            out.append(Finding(tag, False, severity, f"Missing keywords: {missing}", {"missing": missing}))
        else:
            out.append(Finding(tag, True, "info", "All required keywords present.", {}))
        return out

    def _check_placeholders(self, text: str) -> List[Finding]:
        placeholders = ["TBD", "TODO", "<fill>", "{your_", "lorem ipsum"]
        hits = [p for p in placeholders if re.search(re.escape(p), text, re.I)]
        if hits:
            return [Finding("placeholders", False, "warn", f"Contains placeholders: {hits}", {"hits": hits})]
        return [Finding("placeholders", True, "info", "No placeholders found.")]

    def _check_shouting(self, text: str) -> List[Finding]:
        words = re.findall(r"[A-Z]{4,}", text)
        if len(words) >= 8:  # lots of ALLCAPS tokens
            return [Finding("shouting", False, "warn", "Excessive ALL-CAPS detected.", {"samples": words[:10]})]
        return [Finding("shouting", True, "info", "No excessive ALL-CAPS.")]

    def _check_unbalanced_code_blocks(self, text: str) -> List[Finding]:
        ticks = text.count("```")
        if ticks % 2 != 0:
            return [Finding("code_blocks", False, "warn", "Unbalanced triple backticks detected.", {"count": ticks})]
        return [Finding("code_blocks", True, "info", "Code fences balanced.")]

    def _check_json_blocks(self, text: str) -> List[Finding]:
        out = []
        fences = re.findall(r"```(?:json)?\s*([\s\S]*?)```", text, re.I)
        for i, block in enumerate(fences):
            try:
                json.loads(block)
                out.append(Finding("json_block", True, "info", f"JSON block #{i+1} valid."))
            except Exception as e:
                out.append(Finding("json_block", False, "warn", f"JSON block #{i+1} invalid: {e}"))
        return out or [Finding("json_block", True, "info", "No JSON blocks to validate.")]

    def _score(self, text: str, findings: List[Finding]) -> float:
        # Keyword fit score
        kw_find = next((f for f in findings if f.criterion in ("required_keywords", "criterion")), None)
        kw_score = 1.0 if (kw_find and kw_find.passed) or not self.required_keywords else (0.6 if kw_find else 0.5)

        # Quality score (length within bounds, no banned patterns, no placeholders/blockers)
        penalties = 0.0
        for f in findings:
            if f.severity == "block" and not f.passed:
                penalties += 0.6
            elif f.severity == "warn" and not f.passed:
                penalties += 0.25
        quality = max(0.0, 1.0 - penalties)

        # Style score (shouting, code blocks, json)
        style_ok = all((f.passed or f.severity == "info") for f in findings if f.criterion in ("shouting", "code_blocks", "json_block"))
        style = 1.0 if style_ok else 0.7

        final = (self.w_kw * kw_score + self.w_q * quality + self.w_st * style) * 100.0
        return round(max(0.0, min(100.0, final)), 1)

    def _decide_ok(self, findings: List[Finding]) -> bool:
        # Any blocking failure → not ok
        for f in findings:
            if f.severity == "block" and not f.passed:
                return False
        return True

    def _summarize(self, findings: List[Finding], score: float) -> str:
        blocks = [f for f in findings if f.severity == "block" and not f.passed]
        warns = [f for f in findings if f.severity == "warn" and not f.passed]
        if blocks:
            return f"Blocked ({score}). " + "; ".join(f"{b.criterion}: {b.message}" for b in blocks[:3])
        if warns:
            return f"OK with warnings ({score}). " + "; ".join(f"{w.criterion}: {w.message}" for w in warns[:3])
        return f"OK ({score})."
