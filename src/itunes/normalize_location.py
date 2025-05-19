#!/usr/bin/env python3

import argparse
import sys
import unicodedata
import urllib.parse
import xml.etree.ElementTree as ElementTree

def encode_url(url: str) -> str:
    return urllib.parse.quote(url)

def decode_url(url: str) -> str:
    return urllib.parse.unquote(url)

def normalize_kana(kana: str) -> str:
    return unicodedata.normalize('NFC', kana)

def decompose_kana(kana: str) -> str:
    return unicodedata.normalize('NFD', kana)

def process_xml(input_file: str, output_file: str) -> None:
    tree: ElementTree.ElementTree[ElementTree.Element[str]] = ElementTree.parse(input_file)
    root: ElementTree.Element[str] = tree.getroot()

    for item in root.findall("./dict/dict/dict"):
        flag: bool = False
        for element in item.iter():
            if flag:
                decoded_url: str = decode_url(element.text)
                normalized_url: str = normalize_kana(decoded_url)
                encoded_url: str = encode_url(normalized_url)
                element.text = encoded_url
                break

            if element.tag == "key" and element.text == "Location":
                flag = True

    tree.write(output_file, encoding="utf-8", xml_declaration=True)

def main(args: argparse.Namespace) -> None:
    if not args.input_file.strip():
        raise ValueError("input_file not specified")

    process_xml(args.input_file, args.output_file)

if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")

    parser: argparse.ArgumentParser = argparse.ArgumentParser(description="normalize location for Mac Music App xml")
    parser.add_argument("input_file")
    parser.add_argument("-o", "--output_file", default="output.xml")
    args: argparse.Namespace = parser.parse_args()

    main(args)
