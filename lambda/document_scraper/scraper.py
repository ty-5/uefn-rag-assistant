"""
UEFN Documentation Scraper
===========================
Uses Selenium to fetch fully rendered pages from Epic's documentation site.
Extracts clean text content and saves as JSON to local output folder.
"""

import json
import time
import os
import re
import random
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

# Import our master URL list
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from master_urls import get_all_urls

OUTPUT_DIR = "docs/scraped"

def wait_for_content(driver, timeout=30):
    start = time.time()
    while time.time() - start < timeout:
        # Random delay between 2-5 seconds to mimic human behavior
        time.sleep(random.uniform(2, 5))
        source = driver.page_source
        if any(tag in source for tag in ['<h1', '<h2', '<article', '<p class']):
            return True
    return False

def create_driver():
    options = Options()
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    )
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    return driver


def wait_for_content(driver, timeout=30):
    """
    Wait until the page has actually rendered meaningful content.
    We know the page is ready when we see real content tags like
    h1, h2, p, article appearing inside app-root.
    """
    start = time.time()
    while time.time() - start < timeout:
        time.sleep(3)
        source = driver.page_source
        # Real content indicators
        if any(tag in source for tag in ['<h1', '<h2', '<article', '<p class']):
            return True
    return False


def extract_content(driver, url, category):
    """
    Extract clean text content from a fully rendered page.
    Removes navigation, headers, footers, and other noise.
    """
    soup = BeautifulSoup(driver.page_source, "html.parser")

    # Get page title - clean up the " | Fortnite Documentation | Epic..." suffix
    title = ""
    if soup.title:
        title = soup.title.string or ""
        title = title.split("|")[0].strip()


    # Remove noise elements we don't want in our content
    noise_selectors = [
        "nav", "header", "footer",
        "[class*='navigation']",
        "[class*='sidebar']",
        "[class*='breadcrumb']",
        "[class*='toc']",
        "[class*='table-of-contents']",
        "[class*='cookie']",
        "[class*='banner']",
        "[class*='feedback']",
    ]
    for selector in noise_selectors:
        for element in soup.select(selector):
            element.decompose()

    # Remove all script and style tags
    for tag in soup(["script", "style"]):
        tag.decompose()

    # Extract text
    text = soup.get_text(separator="\n")

    # Clean up whitespace
    lines = [line.strip() for line in text.splitlines()]
    lines = [line for line in lines if line]  # Remove empty lines
    clean_text = "\n".join(lines)

    # Remove repeated whitespace
    clean_text = re.sub(r'\n{3,}', '\n\n', clean_text)

    # Remove the page title line that appears at the top of every page
    # Format is always "Page Title | Fortnite Documentation | Epic Developer Community"
    if "Epic Developer Community" in clean_text[:200]:
        lines = clean_text.split("\n")
        # Remove lines containing the site title suffix
        lines = [l for l in lines if "Epic Developer Community" not in l]
        clean_text = "\n".join(lines)

    return {
        "url": url,
        "title": title,
        "category": category,
        "content": clean_text,
        "content_length": len(clean_text),
        "scraped_at": datetime.utcnow().isoformat() + "Z"
    }


def reset_session(driver):
        
        """Clear cookies and cache to avoid bot detection between requests."""

        driver.delete_all_cookies()
        # Navigate to a neutral page first to reset state
        driver.get("about:blank")
        time.sleep(2)

def scrape_url(driver, url, category):
    """
    Scrape a single URL and return the document dict.
    Returns None if scraping fails.
    """

    try:
        reset_session(driver) # reset session to avoid bot flags
        print(f"  Loading page...")
        driver.get(url)

        print(f"  Waiting for content...")
        loaded = wait_for_content(driver)

        if not loaded:
            print(f"  WARNING: Content may not have fully loaded")

        print(f"  Extracting content...")
        doc = extract_content(driver, url, category)

        print(f"  Content length: {doc['content_length']} chars")

        if doc['content_length'] < 500:
            print(f"  WARNING: Very short content — page may not have rendered")

        return doc

    except Exception as e:
        print(f"  ERROR: {e}")
        return None


def save_document(doc, output_dir):
    """Save a document as a JSON file."""
    # Create filename from URL
    url_path = doc['url'].split('/documentation/en-us/fortnite/')[-1]
    filename = url_path.replace('/', '_') + '.json'
    filepath = os.path.join(output_dir, filename)

    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(doc, f, indent=2, ensure_ascii=False)

    return filepath


def main():
    print("=== UEFN Documentation Scraper ===\n")

    # Create output directory
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Load URLs
    all_urls = get_all_urls()
    total = sum(len(urls) for urls in all_urls.values())
    print(f"Total URLs to scrape: {total}")
    print(f"Output directory: {OUTPUT_DIR}\n")

    driver = create_driver()
    results = {"success": 0, "failed": 0, "short": 0}
    failed_urls = []

    try:
        url_count = 0
        for category, urls in all_urls.items():
            print(f"\n{'='*50}")
            print(f"Category: {category} ({len(urls)} pages)")
            print(f"{'='*50}")

            for url in urls:
                url_count += 1
                print(f"\n[{url_count}/{total}] {url.split('/')[-1]}")
                print(f"  Category: {category}")

                doc = scrape_url(driver, url, category)

                if doc is None:
                    results["failed"] += 1
                    failed_urls.append(url)
                    continue

                if doc['content_length'] < 500:
                    results["short"] += 1

                filepath = save_document(doc, OUTPUT_DIR)
                results["success"] += 1
                print(f"  Saved: {os.path.basename(filepath)}")

                # Polite delay between requests
                time.sleep(2)

    finally:
        driver.quit()
        print("\nBrowser closed.")

    # Summary
    print(f"\n{'='*50}")
    print(f"SCRAPING COMPLETE")
    print(f"{'='*50}")
    print(f"Successful: {results['success']}")
    print(f"Failed:     {results['failed']}")
    print(f"Short (<500 chars): {results['short']}")

    if failed_urls:
        print(f"\nFailed URLs:")
        for url in failed_urls:
            print(f"  {url}")

    # Save summary
    summary = {
        "total_urls": total,
        "results": results,
        "failed_urls": failed_urls,
        "completed_at": datetime.utcnow().isoformat() + "Z"
    }
    with open(os.path.join(OUTPUT_DIR, "_scrape_summary.json"), 'w') as f:
        json.dump(summary, f, indent=2)
    print(f"\nSummary saved to {OUTPUT_DIR}/_scrape_summary.json")


if __name__ == "__main__":
    main()