#OneDrive\Desktop\Projects\science\pages\scrapers>python scientificlabs-scraper-7.py
from playwright.sync_api import sync_playwright
import json

def fetch_all_products():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # Set to True for headless mode
        page = browser.new_page()

        base_url = "https://www.scientificlabs.co.uk/search/all?page={}&sortby=DEFAULT"
        page_number = 1
        all_data = []
        max_retries = 3  # Number of times to retry a page

        try:
            while True:
                # Construct the URL for the current page
                search_url = base_url.format(page_number)
                
                try:
                    retry_count = 0
                    while retry_count < max_retries:
                        try:
                            # Attempt to load the page and wait until the network is idle
                            page.goto(search_url, timeout=180000, wait_until='networkidle')  # Increased timeout, wait for network idle
                            break  # Exit retry loop if successful
                        except Exception as e:
                            retry_count += 1
                            print(f"Retry {retry_count} failed for page {page_number}: {e}")

                    # If max retries exceeded, skip the page
                    if retry_count == max_retries:
                        print(f"Skipping page {page_number} after {max_retries} retries.")
                        page_number += 1
                        continue

                except Exception as load_error:
                    print(f"Failed to load page {page_number}: {load_error}")
                    # Skip to the next page if the page fails to load
                    page_number += 1
                    continue

                # Wait for the product listings to appear
                page.wait_for_selector('div.code', timeout=30000)  # Increased to 30 seconds

                # Extract product data (same as before)
                product_codes = page.query_selector_all('div.code span')
                product_descriptions = page.query_selector_all('div.description a')
                unit_sizes = page.query_selector_all('span[id$="searchResultUnit"]')
                prices = page.query_selector_all('div.price span.gridDisplayBlock')

                if not product_codes:  # If no products are found, break the loop (i.e., no more pages)
                    break

                page_data = []
                for i in range(len(product_codes)):
                    product_code = product_codes[i].inner_text()
                    product_description = product_descriptions[i].inner_text()
                    product_link = product_descriptions[i].get_attribute('href')
                    unit_size = unit_sizes[i].inner_text() if len(unit_sizes) > i else 'N/A'

                    # Extract the price and replace \u00a3 with the actual £ symbol
                    price = prices[i].inner_text() if len(prices) > i else 'N/A'
                    price = price.replace("\u00a3", "£")  # Directly replace the Unicode pound symbol

                    # Store the product data
                    page_data.append({
                        'code': product_code,
                        'description': product_description,
                        'link': product_link,
                        'unit_size': unit_size,
                        'price': price
                    })

                all_data.extend(page_data)

                # Optionally save page-by-page to a JSON file
                with open(f'scientificlabs_page_{page_number}.json', 'w', encoding='utf-8') as f:
                    json.dump(page_data, f, indent=4, ensure_ascii=False)  # Use ensure_ascii=False

                print(f"Page {page_number} scraped. {len(page_data)} products found.")

                # Increment the page number
                page_number += 1

        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            browser.close()

        # Save the full dataset if needed
        with open('scientificlabs_all_products.json', 'w', encoding='utf-8') as f:
            json.dump(all_data, f, indent=4, ensure_ascii=False)  # Use ensure_ascii=False to prevent escaping

if __name__ == "__main__":
    fetch_all_products()





