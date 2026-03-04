import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

VERSE_API_URL = "https://dev.epicgames.com/documentation/en-us/fortnite/verse-api"
BASE_URL = "https://dev.epicgames.com"

# All modules across all three top-level sections
MODULES = [
    # Fortnite.com modules
    "fortnitedotcom/ai",
    "fortnitedotcom/animation",
    "fortnitedotcom/characters",
    "fortnitedotcom/devices",
    "fortnitedotcom/fortplayerutilities",
    "fortnitedotcom/game",
    "fortnitedotcom/input",
    "fortnitedotcom/itemization",
    "fortnitedotcom/marketplace",
    "fortnitedotcom/playspaces",
    "fortnitedotcom/teams",
    "fortnitedotcom/ui",
    "fortnitedotcom/vehicles",
    # UnrealEngine.com modules
    "unrealenginedotcom/assets",
    "unrealenginedotcom/basicshapes",
    "unrealenginedotcom/controlinput",
    "unrealenginedotcom/itemization",
    "unrealenginedotcom/json",
    "unrealenginedotcom/scenegraph",
    "unrealenginedotcom/temporary",
    "unrealenginedotcom/webapi",
    # Verse.org modules
    "versedotorg/assets",
    "versedotorg/colors",
    "versedotorg/concurrency",
    "versedotorg/native",
    "versedotorg/presentation",
    "versedotorg/random",
    "versedotorg/scenegraph",
    "versedotorg/simulation",
    "versedotorg/spatialmath",
    "versedotorg/verse",
]

def create_driver():
    options = Options()
    #options.add_argument("--headless")
    # removing headless to evade anti-bot measures taken by UEFN
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    )
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def extract_links_from_page(driver):
    """Extract all verse-api links from the current page."""
    urls = set()
    anchor_tags = driver.find_elements(By.TAG_NAME, "a")
    for tag in anchor_tags:
        href = tag.get_attribute("href")
        if href and '/verse-api/' in href:
            clean_url = href.split('?')[0].split('#')[0].rstrip('/')
            path_after_api = clean_url.split('/verse-api/')[-1]
            segments = [s for s in path_after_api.split('/') if s]
            # Keep pages with 3+ segments = actual class/interface pages
            if len(segments) >= 3:
                urls.add(clean_url)
    return urls

def scrape_module(driver, module_path):
    """
    Visit a module page and extract all class/interface/enumeration links.
    """
    module_url = f"{BASE_URL}/documentation/en-us/fortnite/verse-api/{module_path}"

    try:
        driver.get(module_url)

        # Wait for basic page load
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.TAG_NAME, "a"))
        )

        # Wait longer for headless rendering
        # Keep checking until we find module-specific links or timeout
        max_wait = 45  # maximum seconds to wait
        interval = 3   # check every 3 seconds
        elapsed = 0
        found_urls = set()

        while elapsed < max_wait:
            time.sleep(interval)
            elapsed += interval

            # Check if module-specific links have appeared
            candidate_urls = extract_links_from_page(driver)
            module_specific = {
                u for u in candidate_urls
                if f'/verse-api/{module_path}/' in u
            }

            if len(module_specific) > 0:
                print(f"  Content loaded after {elapsed}s — "
                      f"found {len(module_specific)} pages")
                found_urls = module_specific
                break
            else:
                print(f"  Waiting... ({elapsed}s elapsed, "
                      f"no module links yet)")

        if not found_urls:
            print(f"  Timeout after {max_wait}s — no links found")

        return found_urls

    except Exception as e:
        print(f"  Error: {e}")
        return set()

def main():
    print("=== Verse API URL Crawler ===\n")
    driver = create_driver()
    all_urls = set()

    try:
        print(f"Scanning {len(MODULES)} modules...\n")

        for i, module in enumerate(MODULES):
            print(f"[{i+1}/{len(MODULES)}] {module}")
            module_urls = scrape_module(driver, module)
            all_urls.update(module_urls)
            time.sleep(2)

    finally:
        driver.quit()
        print("\nBrowser closed.")

    # Organize by module
    organized = {}
    for url in sorted(all_urls):
        path = url.split('/verse-api/')[-1]
        parts = path.split('/')
        if len(parts) >= 3:
            module_key = f"{parts[0]}/{parts[1]}"
            if module_key not in organized:
                organized[module_key] = []
            organized[module_key].append(url)

    # Print summary
    print(f"\n=== CRAWL SUMMARY ===")
    print(f"Total API pages found: {len(all_urls)}")
    for module, urls in sorted(organized.items()):
        print(f"  {module}: {len(urls)} pages")

    # Save
    output = {
        "total": len(all_urls),
        "by_module": organized,
        "all_urls": sorted(list(all_urls))
    }

    with open('docs/api_urls.json', 'w') as f:
        json.dump(output, f, indent=2)

    print(f"\nSaved to docs/api_urls.json")

if __name__ == "__main__":
    main()
### What Changed

#The key insight is that instead of trying to expand the sidebar on the landing page, we **visit each module page directly**. Each module page (like `/verse-api/fortnitedotcom/devices`) should render its own content table listing all classes inside it — this is static content that doesn't require sidebar interaction.

#We also tightened the URL filter to require **3+ path segments** after `/verse-api/` which ensures we only get actual class pages:

#fortnitedotcom/devices/creative_device  ← 3 segments ✅
#fortnitedotcom/devices                  ← 2 segments ❌ skipped

###