#!/usr/bin/env python3
"""Capture Swagger UI screenshots for README documentation."""

from pathlib import Path

from playwright.sync_api import sync_playwright

DOCS_URL = "http://localhost:8000/docs"
OUTPUT_DIR = Path(__file__).resolve().parent.parent / "docs" / "images"


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        page = browser.new_page(viewport={"width": 1440, "height": 900})
        page.goto(DOCS_URL, wait_until="networkidle")
        page.screenshot(path=str(OUTPUT_DIR / "swagger-overview.png"), full_page=True)

        post_asset = page.locator(".opblock-summary-post").first
        if post_asset.count():
            post_asset.click()
            page.wait_for_timeout(500)
            page.screenshot(path=str(OUTPUT_DIR / "swagger-post-asset.png"), full_page=True)

        browser.close()

    print(f"Screenshots saved to {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
