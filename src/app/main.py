from __future__ import annotations

import logging

from app.logging_config import configure_logging

logger = logging.getLogger(__name__)


def main() -> None:
    run_id = configure_logging()
    logger.info("Application started (run_id=%s)", run_id)


if __name__ == "__main__":
    main()
