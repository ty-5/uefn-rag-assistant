import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

BASE_URL = "https://dev.epicgames.com"

# Only the one seed URL that reliably works
SEED_URLS = [
    "https://dev.epicgames.com/documentation/en-us/fortnite/verse-language-reference",
]

# Known high-value API pages to add manually since auto-discovery misses them
MANUAL_API_URLS = [
    "https://dev.epicgames.com/documentation/en-us/fortnite/verse-api",
    "https://dev.epicgames.com/documentation/en-us/fortnite/verse-api/fortnitedotcom/characters/fort_character",
    "https://dev.epicgames.com/documentation/en-us/fortnite/verse-api/versedotorg/simulation/player",
    "https://dev.epicgames.com/documentation/en-us/fortnite/verse-api/versedotorg/simulation/playspace",
    "https://dev.epicgames.com/documentation/en-us/fortnite/verse-api/fortnitedotcom/devices/creative_device",
    "https://dev.epicgames.com/documentation/en-us/fortnite/verse-api/fortnitedotcom/devices/creative_prop",
]

# Known patch notes URLs to add manually
MANUAL_PATCH_URLS = [
    "https://dev.epicgames.com/documentation/en-us/fortnite/whats-new-in-unreal-editor-for-fortnite",
    "https://dev.epicgames.com/documentation/en-us/fortnite/39-00-fortnite-ecosystem-updates-and-release-notes",
    "https://dev.epicgames.com/documentation/en-us/fortnite/38-00-fortnite-ecosystem-updates-and-release-notes",
    "https://dev.epicgames.com/documentation/en-us/fortnite/37-00-fortnite-ecosystem-updates-and-release-notes",
]

# Pages to explicitly exclude (low value for developers)
EXCLUDE_KEYWORDS = [
    'campaigns', 'community-building', 'promoting', 'education',
    'video-tutorials', 'lego', 'walking-dead', 'kpop', 'patchwork',
    'weapons-primer', 'game-collections', 'template-islands',
    'discover-the-resources', 'creator-portal', 'island-moderation',
    'in-island-transactions', 'mobile-development'
]

def create_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    )
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def is_excluded(url):
    return any(keyword in url for keyword in EXCLUDE_KEYWORDS)

def extract_doc_links(driver, url):
    try:
        driver.get(url)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "a"))
        )
        time.sleep(6)

        links = set()
        anchor_tags = driver.find_elements(By.TAG_NAME, "a")

        for tag in anchor_tags:
            href = tag.get_attribute("href")
            if href and '/documentation/en-us/' in href:
                if any(section in href for section in ['/fortnite/', '/uefn/']):
                    clean_url = href.split('?')[0].split('#')[0].rstrip('/')
                    if not is_excluded(clean_url):
                        links.add(clean_url)

        return links

    except Exception as e:
        print(f"  Error fetching {url}: {e}")
        return set()

def categorize_url(url):
    if 'verse-api' in url:
        return 'api-reference'
    elif any(term in url for term in [
        'release-notes', 'ecosystem-updates', 'patch', 'whats-new'
    ]):
        return 'patch-notes'
    elif any(term in url for term in [
        'troubleshoot', 'debug', 'optimize', 'performance', 'memory'
    ]):
        return 'troubleshooting'
    elif any(term in url for term in [
        'expressions', 'functions', 'variables', 'constants', 'types',
        'control-flow', 'operators', 'modules', 'specifiers', 'failure',
        'concurrency', 'composite', 'container', 'grouping', 'code-blocks',
        'comments', 'working-with-types', 'verse-language', 'verse-glossary',
        'verse-version'
    ]):
        return 'verse-language'
    else:
        return 'tutorial'

def discover_urls():
    print("Starting Chrome driver...")
    driver = create_driver()
    all_links = set()

    try:
        # First pass — scan seed URLs
        for seed_url in SEED_URLS:
            print(f"Scanning seed: {seed_url}")
            links = extract_doc_links(driver, seed_url)
            all_links.update(links)
            print(f"  Found {len(links)} links")
            time.sleep(2)

        # Second pass — crawl each discovered URL for more links
        print(f"\nDeep crawling {len(all_links)} discovered pages...")
        second_pass_links = set()
        for i, url in enumerate(sorted(all_links)):
            print(f"  [{i+1}/{len(all_links)}] {url.split('/')[-1]}")
            links = extract_doc_links(driver, url)
            second_pass_links.update(links)
            time.sleep(2)

        all_links.update(second_pass_links)
        print(f"\nAfter deep crawl: {len(all_links)} total URLs")

    finally:
        driver.quit()
        print("Browser closed.")

    # Add manual URLs
    for url in MANUAL_API_URLS + MANUAL_PATCH_URLS:
        all_links.add(url)
    print(f"After adding manual URLs: {len(all_links)} total URLs")

    # Categorize
    categorized = {}
    for url in sorted(all_links):
        category = categorize_url(url)
        if category not in categorized:
            categorized[category] = []
        categorized[category].append(url)

    # Print summary
    print(f"\n=== DISCOVERY SUMMARY ===")
    print(f"Total URLs found: {len(all_links)}")
    for category, urls in categorized.items():
        print(f"  {category}: {len(urls)} pages")

    # Save
    with open('docs/discovered_urls.json', 'w') as f:
        json.dump(categorized, f, indent=2)

    print(f"\nSaved to docs/discovered_urls.json")
    return categorized

if __name__ == "__main__":
    discover_urls()