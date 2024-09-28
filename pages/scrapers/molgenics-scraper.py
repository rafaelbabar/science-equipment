#OneDrive\Desktop\Projects\science\pages\scrapers>python molgenics-scraper.py
from playwright.sync_api import sync_playwright
import json

def fetch_all_products():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # Set to True for headless mode
        page = browser.new_page()

        base_url = "https://www.scientificlabs.co.uk/search/all?page={}&sortby=DEFAULT"
        page_number = 1
        all_data = []

        try:
            while True:
                # Construct the URL for the current page
                search_url = base_url.format(page_number)
                page.goto(search_url, timeout=60000)

                # Wait for the product listings to appear
                page.wait_for_selector('div.code', timeout=15000)  # Use a reliable element to wait for

                # Extract product data based on the snippets provided
                product_codes = page.query_selector_all('div.code span')  # Adjusted for product code
                product_descriptions = page.query_selector_all('div.description a')  # Adjusted for description and link
                # Use a more general selector for unit size that targets any span with an ID ending in 'searchResultUnit'
                unit_sizes = page.query_selector_all('span[id$="searchResultUnit"]')  # Adjusted for unit size
                prices = page.query_selector_all('div.price span.gridDisplayBlock')  # Adjusted for price

                if not product_codes:  # If no products are found, break the loop (i.e., no more pages)
                    break

                page_data = []
                for i in range(len(product_codes)):
                    # Extract the necessary details
                    product_code = product_codes[i].inner_text()
                    product_description = product_descriptions[i].inner_text()
                    product_link = product_descriptions[i].get_attribute('href')
                    unit_size = unit_sizes[i].inner_text() if len(unit_sizes) > i else 'N/A'
                    price = prices[i].inner_text() if len(prices) > i else 'N/A'

                    # Replace Unicode pound symbol with the actual £ symbol
                    price = price.replace("\u00a3", "£")

                    # Store the product data
                    page_data.append({
                        'code': product_code,
                        'description': product_description,
                        'link': product_link,
                        'unit_size': unit_size,
                        'price': price
                    })

                # Append the page data to all_data
                all_data.extend(page_data)

                # Optionally save page-by-page to a JSON file (to prevent data loss on large scrapes)
                with open(f'scientificlabs_page_{page_number}.json', 'w') as f:
                    json.dump(page_data, f, indent=4)

                print(f"Page {page_number} scraped. {len(page_data)} products found.")
                
                # Increment the page number to fetch the next page
                page_number += 1

        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            browser.close()

        # Save the full dataset if needed
        with open('scientificlabs_all_products.json', 'w') as f:
            json.dump(all_data, f, indent=4)

if __name__ == "__main__":
    fetch_all_products()



