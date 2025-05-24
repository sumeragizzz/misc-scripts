#!/usr/bin/env python3

import logging

logger: logging.Logger = logging.getLogger(__name__)

def main():
    logger.debug("debug log message")
    logger.info("info log message")
    logger.warning("warning log message")
    logger.error("error log message")
    logger.critical("critical log message")

if __name__ == "__main__":
    # filemode "a": append(default), "w": overwrite
    logging.basicConfig(filename="output.log", filemode="w", format="%(asctime)s %(levelname)-8s %(message)s", level=logging.DEBUG)

    main()
