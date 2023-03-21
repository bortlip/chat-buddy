import logging
from datetime import datetime

def create_logger(name, level=logging.INFO, filename_prefix=None):
    logger = logging.getLogger(name)
    logger.setLevel(level)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    if filename_prefix:
        filename_suffix = datetime.now().strftime("%Y%m%d-%H%M%S")
        filename= f"{filename_prefix}-{filename_suffix}.txt"
        fh = logging.FileHandler(filename, encoding='utf-8')
        fh.setLevel(level)
        fh.setFormatter(formatter)
        logger.addHandler(fh)
    else:
        ch = logging.StreamHandler()
        ch.setLevel(level)
        ch.setFormatter(formatter)
        logger.addHandler(ch)
    return logger