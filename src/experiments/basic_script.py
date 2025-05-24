#!/usr/bin/env python3

import argparse
import logging

logger: logging.Logger = logging.getLogger(__name__)

def other_function():
    logger.info("execute other_function()")

def main(args: argparse.Namespace):
    logger.info(f"string: {args.param_string}")
    logger.info(f"integer: {args.param_integer}")
    logger.info(f"option: {args.option}")
    other_function()

if __name__ == "__main__":
    logging.basicConfig(format="%(asctime)s %(levelname)-8s %(message)s", level=logging.INFO)

    parser: argparse.ArgumentParser = argparse.ArgumentParser(description="Basic Script")
    parser.add_argument("param_string")
    parser.add_argument("param_integer", type=int)
    parser.add_argument("--option", default="default_value")
    args: argparse.Namespace = parser.parse_args()

    main(args)
