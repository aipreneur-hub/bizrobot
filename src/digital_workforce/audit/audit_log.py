from ..utils.logger import logger
from datetime import datetime
from typing import Dict, Any

def write_audit(event: str, payload: Dict[str, Any]) -> None:
    logger.info(f"[AUDIT] {datetime.utcnow().isoformat()} {event} {payload}\n")
