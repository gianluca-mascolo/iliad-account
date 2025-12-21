"""Iliad account scraper - fetches data usage progress from iliad.it"""

import getpass
import os
import sys

import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

LOGIN_URL = "https://www.iliad.it/account/"
ACCOUNT_URL = "https://www.iliad.it/account/"
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)


def get_credentials() -> tuple[str, str]:
    """Get login credentials from .env file or prompt user."""
    user_id = os.getenv("ILIAD_USER_ID")
    password = os.getenv("ILIAD_PASSWORD")

    if user_id and password:
        return user_id, password

    print("=== Iliad Account Login ===")
    if not user_id:
        user_id = input("ID utente (8 cifre): ").strip()
    if not password:
        password = getpass.getpass("Password: ")
    return user_id, password


def login(
    session: requests.Session, user_id: str, password: str, debug: bool = False
) -> bool:
    """Attempt to login to iliad account."""
    # First, get the login page to capture any cookies/tokens
    response = session.get(LOGIN_URL)
    response.raise_for_status()

    # Parse for any hidden form fields (CSRF tokens, etc.)
    soup = BeautifulSoup(response.text, "html.parser")
    login_form = soup.find("form")

    if debug:
        print(f"\n[DEBUG] Form found: {login_form is not None}")
        if login_form:
            print(f"[DEBUG] Form action: {login_form.get('action')}")
            print(f"[DEBUG] Form method: {login_form.get('method')}")
            for inp in login_form.find_all("input"):
                print(f"[DEBUG] Input: name={inp.get('name')}, type={inp.get('type')}")

    # Build login payload
    payload = {
        "login-ident": user_id,
        "login-pwd": password,
    }

    # Add any hidden fields from the form
    if login_form:
        for hidden_input in login_form.find_all("input", type="hidden"):
            name = hidden_input.get("name")
            value = hidden_input.get("value", "")
            if name:
                payload[name] = value

    if debug:
        print(f"[DEBUG] Payload keys: {list(payload.keys())}")

    # Submit login
    response = session.post(LOGIN_URL, data=payload)
    response.raise_for_status()

    if debug:
        print(f"[DEBUG] Response URL: {response.url}")
        print(
            f"[DEBUG] 'conso-progress' in response: {'conso-progress' in response.text}"
        )
        print(f"[DEBUG] 'Consumi' in response: {'Consumi' in response.text}")
        print(f"[DEBUG] Response snippet: {response.text[:500]}")

    # Check if login was successful (we should be on the account page)
    return "conso-progress" in response.text or "Consumi" in response.text


def get_progress_value(session: requests.Session) -> str | None:
    """Fetch the data-progress-value from the account page."""
    response = session.get(ACCOUNT_URL)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    # Find the div with id="conso-progress" and class="progressbar"
    progress_div = soup.find("div", id="conso-progress", class_="progressbar")

    if progress_div:
        return progress_div.get("data-progress-value")

    # Try alternative: find any div with class progressbar that has the attribute
    progress_div = soup.find(
        "div", class_="progressbar", attrs={"data-progress-value": True}
    )

    if progress_div:
        return progress_div.get("data-progress-value")

    return None


def main() -> int:
    """Main entry point for the CLI."""
    load_dotenv()
    user_id, password = get_credentials()

    session = requests.Session()
    session.headers.update({"User-Agent": USER_AGENT})

    debug = os.getenv("DEBUG", "").lower() in ("1", "true", "yes")

    print("\nLogging in...")
    try:
        if not login(session, user_id, password, debug=debug):
            print("Login failed. Please check your credentials.")
            return 1
    except requests.RequestException as e:
        print(f"Connection error: {e}")
        return 1

    print("Login successful!")
    print("\nFetching progress value...")

    try:
        progress_value = get_progress_value(session)
    except requests.RequestException as e:
        print(f"Error fetching account page: {e}")
        return 1

    if progress_value is None:
        print("\nCould not find progress value on the page.")
        return 1

    # Convert progress value (Italian decimal format with comma)
    percentage = float(progress_value.replace(",", "."))

    # Get available data from env
    data_gb_str = os.getenv("ILIAD_DATA_GB")
    if not data_gb_str:
        print(f"\nData usage: {percentage:.2f}%")
        print("(Set ILIAD_DATA_GB in .env to see usage in GB)")
        return 0

    total_gb = int(data_gb_str)
    used_gb = round(percentage * total_gb / 100, 2)

    print(f"\nData usage: {used_gb} GB / {total_gb} GB ({percentage:.2f}%)")

    return 0


if __name__ == "__main__":
    sys.exit(main())
