import cloudscraper
import re
import os
import asyncio
import time
import random
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

# --- STYLING ---
R, G, Y, B, C = "\033[91m", "\033[92m", "\033[93m", "\033[94m", "\033[0m"
BOLD = "\033[1m"

# --- SMART CONFIG ---
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
]

SENSITIVE_FILES = [".env", "robots.txt", "wp-json/wp/v2/users", ".git/config", "sitemap.xml"]

# --- DYNAMIC ANALYSIS ENGINE ---
async def scan_resource(scraper, url, is_js=False):
    label = f"{B}[JS]{C}" if is_js else f"{G}[HTML]{C}"
    print(f"{label} Analyzing: {url}")
    
    try:
        # Har request ke liye random user agent
        scraper.headers.update({'User-Agent': random.choice(USER_AGENTS)})
        res = scraper.get(url, timeout=15)
        
        # 1. Secret Patterns
        secrets = {
            "Internal IP": r"\b10\.\d{1,3}\.\d{1,3}\.\d{1,3}\b",
            "WP-Config Leak": r"DB_PASSWORD|DB_USER|AUTH_KEY",
            "Possible MD5": r"\b[a-f0-9]{32}\b"
        }
        
        for name, pat in secrets.items():
            match = re.search(pat, res.text)
            if match:
                print(f"  {R}{BOLD}[!] {name} Found:{C} {Y}{match.group()}{C}")

        # 2. Endpoint Extraction
        if is_js or not is_js: # Dono mein check karo
            eps = re.findall(r'["\']((?:https?://|/)[^"\'\s>]+)["\']', res.text)
            clean_eps = list(set([e for e in eps if len(e) > 5 and "/" in e]))
            if clean_eps:
                print(f"  {G}[+] Found {len(clean_eps)} Hidden Paths (e.g., {clean_eps[0]}){C}")
                
    except:
        print(f"  {R}[X] Blocked/Timeout{C}")

async def main():
    os.system('clear')
    print(f"{BOLD}{Y}="*60)
    print(f"🛡️  SECURESTACK v7.0: THE GHOST ANALYZER (ANTI-BLOCK)")
    print("="*60 + f"{C}")

    target = input(f"{BOLD}Target URL: {C}").strip()
    if not target.startswith("http"): target = "http://" + target

    scraper = cloudscraper.create_scraper(browser='chrome')

    try:
        print(f"\n{BOLD}{B}[*] Phase 1: Deep Crawling{C}")
        response = scraper.get(target, timeout=15)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Baseline Scan
        await scan_resource(scraper, target)

        # Better JS Extraction (WordPress specific)
        scripts = soup.find_all('script')
        js_links = []
        for s in scripts:
            src = s.get('src')
            if src:
                full_url = urljoin(target, src)
                if urlparse(target).netloc in full_url:
                    js_links.append(full_url)

        if js_links:
            print(f"\n{B}[*] Analyzing {len(js_links)} Scripts with Delays...{C}")
            for js in js_links[:5]: # Top 5 scripts
                await scan_resource(scraper, js, is_js=True)
                time.sleep(1) # 1 second delay to avoid 503

        print(f"\n{BOLD}{Y}[!] Phase 2: Sensitive File Check (Bypassing WAF){C}")
        for file in SENSITIVE_FILES:
            f_url = urljoin(target, file)
            # Dummy parameter to bypass cache
            f_url += f"?v={random.randint(1,1000)}"
            
            f_res = scraper.get(f_url, timeout=10, allow_redirects=False)
            if f_res.status_code == 200:
                print(f"  {R}{BOLD}[!!!] EXPOSED: {f_url}{C}")
            else:
                print(f"  {C}[-] {file} status: {f_res.status_code}{C}")
            time.sleep(1.5)

    except Exception as e:
        print(f"{R}[X] Critical Error: {e}{C}")

    print("\n" + "="*60 + f"\n{BOLD}{G}✅ SCAN COMPLETED!{C}")

if __name__ == "__main__":
    asyncio.run(main())
