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
    # settings formatter
    formatter = logging.Formatter("%(asctime)s %(levelname)-8s %(message)s")
    # output console
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.INFO)
    # output file
    file_handler = logging.FileHandler("output.log", "w")
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.WARNING)
    # settings logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    logger.setLevel(logging.DEBUG)

    main()
