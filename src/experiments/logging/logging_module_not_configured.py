#!/usr/bin/env python3

import logging
import module.logging_module as lm

logger: logging.Logger = logging.getLogger(__name__)

def main():
    lm.execute()

if __name__ == "__main__":
    main()
