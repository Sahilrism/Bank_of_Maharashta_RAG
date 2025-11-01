import json
import re
from pathlib import Path

input_file = Path("data/raw_data/combined_bom_data.json")
output_file = Path("data/raw_data/cleaned_combined.json")

# Load combined data
with open(input_file, "r", encoding="utf-8") as f:
    all_pages = json.load(f)

def extract_section(title, text, next_titles):
    """Extract section content between titles."""
    pattern = re.escape(title) + r"(.*?)(?=" + "|".join(map(re.escape, next_titles)) + r"|$)"
    match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
    return match.group(1).strip() if match else ""

# Section headers to look for
sections = [
    "Features & Benefits",
    "Documents Required",
    "Interest Rates",
    "Check Eligibility",
    "Eligibility",
    "FAQs",
    "How to Apply",
    "Charges",
    "Processing Fees"
]

cleaned_data = []

for page in all_pages:
    text = page["content"]
    structured = {
        "page_name": page.get("page_name", ""),
        "url": page.get("url", "")
    }

    # Extract each section
    for i, title in enumerate(sections):
        next_titles = sections[i + 1 :]
        structured[title] = extract_section(title, text, next_titles)

    # Try to find Interest Rate with regex
    rate_match = re.search(r"(\d+\.\d+)\s*%P\.?A", text, re.IGNORECASE)
    structured["Interest Rate"] = rate_match.group(1) + "%" if rate_match else "Not Found"

    cleaned_data.append(structured)

# Save all cleaned data
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(cleaned_data, f, indent=4, ensure_ascii=False)

print(f"Cleaned data for all loans saved to {output_file}")
