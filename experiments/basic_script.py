#!/usr/bin/env python3

import argparse

def other_function():
    print("execute other_function()")

def main(args):
    print(f"string: {args.param_string}")
    print(f"integer: {args.param_integer}")
    print(f"option: {args.option}")
    other_function()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Basic Script")
    parser.add_argument("param_string")
    parser.add_argument("param_integer", type=int)
    parser.add_argument("--option", default="default_value")
    args = parser.parse_args()

    main(args)
