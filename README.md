# 🛡️ SECURESTACK v7.0: The Ghost Analyzer

**SecureStack** is a powerful, Python-based security reconnaissance tool designed to automate the discovery of hidden assets and vulnerabilities. Built for bug bounty hunters and penetration testers, it focuses on stealth, anti-blocking, and deep-dive analysis of web resources.

---

## 🚀 Key Features

* **👻 Stealth Scanning:** Utilizes `cloudscraper` and randomized `User-Agents` to bypass WAFs and basic bot protection.
* **📂 Sensitive File Discovery:** Automated checks for critical files like `.env`, `.git/config`, `robots.txt`, and exposed `wp-json` endpoints.
* **🔍 Deep JS Intelligence:** Extracts hidden API endpoints, internal IP addresses, and hardcoded secrets from JavaScript files.
* **⚡ Adaptive Delays:** Implements human-like timing between requests to prevent IP rate-limiting and 503 errors.
* **🎯 OWASP Aligned:** Specifically targets Sensitive Data Exposure (A04:2021) and Security Misconfigurations (A05:2021).

---

## 🛠️ Installation & Setup

### 1. Prerequisites
Ensure you have **Python 3.8+** installed on your system (Termux, Pydroid3, Linux, or Windows).

### 2. Install Dependencies
Run the following command to install the required libraries:
```bash
pip install cloudscraper beautifulsoup4 asyncio
