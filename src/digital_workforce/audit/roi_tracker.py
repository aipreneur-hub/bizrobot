from ..utils.logger import logger

def track_roi(project_id: str, roi_score: float) -> None:
    logger.info(f"[ROI] project={project_id} roi_score={roi_score}\n")
