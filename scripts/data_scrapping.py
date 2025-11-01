import os
import json
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

data_save_path = "data/raw_data"
os.makedirs(data_save_path, exist_ok=True)

URLS = {
    "home_loan": "https://bankofmaharashtra.bank.in/personal-banking/loans/home-loan",
    "maha_super_housing_construction": "https://bankofmaharashtra.bank.in/maha-super-housing-loan-scheme-for-construction-acquiring",
    "maha_super_housing_plot": "https://bankofmaharashtra.bank.in/maha-super-housing-loan-scheme-for-purchase-plot-construction-thereon",
    "maha_super_housing_repair": "https://bankofmaharashtra.bank.in/maha-super-housing-loan-scheme-for-repairs",
    "car_loan": "https://bankofmaharashtra.bank.in/personal-banking/loans/car-loan",
    "advances": "https://bankofmaharashtra.bank.in/advances",
    "credit_card_simplysave": "https://bankofmaharashtra.bank.in/bom-sbi-credit-cards-simplysave",
    "credit_card_prime": "https://bankofmaharashtra.bank.in/bom-sbi-credit-cards-prime",
    "credit_card_elite": "https://bankofmaharashtra.bank.in/bom-sbi-credit-cards-elite",
    "gold_loan": "https://bankofmaharashtra.bank.in/gold-loan",
    "topup_home_loan": "https://bankofmaharashtra.bank.in/topup-home-loan",
    "rewards_vouchers": "https://reward.bankofmaharashtra.in/vouchers/all-vouchers",
    "vehicle_loan": "https://bomdigitalloans.bankofmaharashtra.in/vehicle-loan/#/vehicle-home",
    "personal_loan": "https://bankofmaharashtra.bank.in/personal-banking/loans/personal-loan",
}

def scrape_page(url):
    """Scrape text content from a given URL."""
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        elements = soup.find_all(["p", "h1", "h2", "h3", "h4", "li", "td"])
        text_content = " ".join(el.get_text(separator=" ", strip=True) for el in elements)

        text_content = " ".join(text_content.split())

        return text_content

    except Exception as e:
        print(f"Failed to scrape {url}: {e}")
        return None

all_data = []

for name, url in tqdm(URLS.items(), desc="Scraping Bank of Maharashtra pages"):
    print(f"\n🔹 Scraping {name} ...")
    content = scrape_page(url)
    if content:
        # Save individual JSON file
        file_path = os.path.join(data_save_path, f"{name}.json")
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump({"name": name, "url": url, "content": content}, f, indent=2, ensure_ascii=False)
        print(f"Saved: {file_path}")

        all_data.append({"name": name, "url": url, "content": content})
    else:
        print(f"Skipped {name} due to empty content.")

combined_path = os.path.join(data_save_path, "combined_bom_data.json")
with open(combined_path, "w", encoding="utf-8") as f:
    json.dump(all_data, f, indent=2, ensure_ascii=False)

print(f"\n All pages scraped and combined into: {combined_path}")