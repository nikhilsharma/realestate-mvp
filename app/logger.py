import logging

def setup_logger(log_level=logging.DEBUG):
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
        datefmt="%H:%M:%S"
    )

logger = logging.getLogger("urban_bricks")