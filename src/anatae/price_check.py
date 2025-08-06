#!/usr/bin/env python3

import argparse
import json
import logging
import os
import re
import requests
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright
from playwright.sync_api import expect

logger: logging.Logger = logging.getLogger(__name__)

def check_price(browser, item_page_url: str) -> tuple[str, int]:
    # サイトにアクセス
    page = browser.new_page()
    page.goto(item_page_url)

    # 合計が表示されるまで待つ
    total_label = page.locator("span", has_text=re.compile(r"^合計$")).first
    total_label.wait_for()

    # タイトルを取得
    title: str = page.locator("h1").text_content().strip()
    logger.debug(f"title: {title}")

    # 価格を取得する
    # 「合計」要素の兄弟要素を取得する
    spans = total_label.locator("xpath=..").locator("span").all()
    logger.debug(f"span size: {len(spans)}")
    if len(spans) < 4:
        raise ValueError("The website structure is unexpected")

    # 価格が表示されるまで待つ
    expect(spans[2]).not_to_have_text("", timeout=5000)

    # カンマ区切り文字列を解析する
    text = spans[2].text_content().strip()
    logger.debug(f"span text: {text}")
    match = re.search(r"\d[\d,]*\.?\d*", text)
    if not match:
        raise ValueError("The price display is unexpected")

    # 価格を数値してタイトルとともに返却する
    price = int(match.group().replace(",", ""))
    logger.debug(f"price: {price}")
    return (title, price)

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
    item_page_urls = json.loads(os.getenv("ITEM_PAGE_URLS"))
    notify_webhook_url = os.getenv("NOTIFY_WEBHOOK_URL")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        try:
            for item_page_url in item_page_urls:
                # 価格情報を取得
                price_info: tuple[str, int] = check_price(browser, item_page_url)
                # Discordで通知
                notify_discord(notify_webhook_url, price_info)
        finally:
            browser.close()

if __name__ == "__main__":
    load_dotenv()

    log_level = getattr(logging, os.environ.get("LOG_LEVEL", "INFO").upper(), logging.INFO)
    logging.basicConfig(format="%(asctime)s %(levelname)-8s %(message)s", level=log_level)
    logging.getLogger("urllib3").setLevel(max(log_level, logging.INFO))

    parser: argparse.ArgumentParser = argparse.ArgumentParser(description="check price")
    args: argparse.Namespace = parser.parse_args()

    main(args)
