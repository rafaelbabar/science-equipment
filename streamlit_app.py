#D:\OneDrive\Desktop\Projects\science>streamlit run science-main.py
import streamlit as st
import json

# Load the JSON data
with open('D:/OneDrive/Desktop/Projects/science/pages/scrapers/molgenics.json') as f:
    molgenics_data = json.load(f)

with open('D:/OneDrive/Desktop/Projects/science/pages/scrapers/scientificlabs_all_products.json') as f:
    scientificlabs_data = json.load(f)

# Function to search both JSON files
def search_products(query):
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

# Streamlit interface
st.title("Product Search")

# Input for search query
search_query = st.text_input("Enter search term")

# Display search results
if search_query:
    results = search_products(search_query)
    if results:
        for result in results:
            st.subheader(result["source"])
            st.write(f"**Product/Description:** {result['product']}")
            st.write(f"**Price:** {result['price']}")
            st.write(f"**Link:** [Product Link]({result['link']})")
    else:
        st.write("No results found.")

