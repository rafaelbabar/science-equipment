#D:\OneDrive\Desktop\Projects\science>streamlit run science-main.py
import streamlit as st
import json
import os

# Load JSON data from two different files
def load_data(file_name):
    # Get the directory where the current script is located
    current_dir = os.path.dirname(__file__)
    
    # Construct the full path to the JSON file
    json_path = os.path.join(current_dir, 'pages\scrapers', file_name)
    
    # Load the JSON data
    with open(json_path, 'r', encoding='utf-8') as f:
        return json.load(f)

# Function to search products across both datasets
def search_products(query, molgenics_data, scientificlabs_data):
    results = []
    
    # Search in molgenics.json file
    for item in molgenics_data:
        if query.lower() in item["product"].lower():
            results.append({
                "source": "Molgenics",
                "product": item["product"],
                "description": item.get("description", ""),
                "price": item.get("price", ""),
                "link": item.get("link", "")
            })
    
    # Search in scientificlabs.json file
    for item in scientificlabs_data:
        if query.lower() in item["description"].lower():
            results.append({
                "source": "Scientific Labs",
                "product": item.get("description", ""),
                "price": item.get("price", ""),
                "link": item.get("link", "")
            })
    
    return results

# Load the data from both JSON files
molgenics_data = load_data('molgenics.json')
scientificlabs_data = load_data('scientificlabs_all_products.json')

# Streamlit interface
st.title("Product Search")

# Input for search query
search_query = st.text_input("Enter search term")

# Display search results
if search_query:
    results = search_products(search_query, molgenics_data, scientificlabs_data)
    if results:
        for result in results:
            st.subheader(result["source"])
            st.write(f"**Product/Description:** {result['product']}")
            st.write(f"**Price:** {result['price']}")
            st.write(f"**Link:** [Product Link]({result['link']})")
    else:
        st.write("No results found.")


