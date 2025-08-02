#!/usr/bin/env python3

import argparse
import logging
import os
import re
import requests
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

logger: logging.Logger = logging.getLogger(__name__)

def check_price(item_page_url: str) -> tuple[str, int]:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        try:
            # サイトにアクセス
            page = browser.new_page()
            page.goto(item_page_url)
            page.locator("span", has_text="合計").first.wait_for()

            # タイトルを取得
            title: str = page.locator("h1").text_content().strip()
            logger.debug(f"title: {title}")

            # 価格を取得する
            # 「合計」要素の兄弟要素を取得する
            total_label = page.locator("span", has_text="合計").first
            parent_div = total_label.locator("xpath=..")
            spans = parent_div.locator("span").all()
            logger.debug(f"span size: {len(spans)}")
            # 「¥」を含み、打消し線でないものを抽出
            for span in spans:
                text = span.text_content().strip()
                logger.debug(f"span text: {text}")
                classes = span.get_attribute("class") or ""
                if "¥" in text and "line-through" not in classes:
                    match = re.search(r"\d[\d,]*\.?\d*", text)
                    if match:
                        price = int(match.group().replace(",", ""))
                        logger.debug(f"price: {price}")
                        return (title, price)

            # 価格を抽出できない場合はエラーとする
            raise ValueError
        finally:
            browser.close()

def notify_discord(notify_webhook_url: str, price_info: tuple[str, int]) -> None:
    # メッセージ作成
    payload = {
        "content": f"\\{price_info[1]:,} {price_info[0]}"
    }

    # メッセージ送信
    response = requests.post(notify_webhook_url, json=payload)
    response.raise_for_status()

def main(args: argparse.Namespace) -> None:
    # 環境変数からURLを取得
    item_page_url = os.getenv("ITEM_PAGE_URL")
    notify_webhook_url = os.getenv("NOTIFY_WEBHOOK_URL")

    # 価格情報を取得
    price_info: tuple[str, int] = check_price(item_page_url)

    # Discordで通知
    notify_discord(notify_webhook_url, price_info)

if __name__ == "__main__":
    load_dotenv()

    log_level = getattr(logging, os.environ.get("LOG_LEVEL", "INFO").upper(), logging.INFO)
    logging.basicConfig(format="%(asctime)s %(levelname)-8s %(message)s", level=log_level)
    logging.getLogger("urllib3").setLevel(max(log_level, logging.INFO))

    parser: argparse.ArgumentParser = argparse.ArgumentParser(description="check price")
    args: argparse.Namespace = parser.parse_args()

    main(args)
