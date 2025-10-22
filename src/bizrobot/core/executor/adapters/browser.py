"""
Browser adapter (mock). Replace with Playwright.
"""
from typing import Dict, Any

class BrowserAdapter:
    def run(self, step: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "ok": True,
            "capability": f"WEB::{step.get('target')}",
            "performed": "fill_form",
        }
