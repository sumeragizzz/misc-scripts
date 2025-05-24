#!/usr/bin/env python3

import logging

def main():
    logging.debug("debug log message")
    logging.info("info log message")
    logging.warning("warning log message")
    logging.error("error log message")
    logging.critical("critical log message")

if __name__ == "__main__":
    logging.basicConfig(format="%(asctime)s %(levelname)-8s %(message)s", level=logging.DEBUG)

    main()
