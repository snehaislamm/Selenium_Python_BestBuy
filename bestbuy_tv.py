# Importing necessary libraries for web scraping and automation.
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Function to perform the search and extract data
def search_and_extract(driver, query):
    # Locate the search input field by its ID and prepare to enter a query.
    search_bar = driver.find_element(By.ID, "gh-search-input")
    search_bar.clear()  # Clears any pre-existing text in the search bar.
    search_bar.send_keys(query)  # Types the search query into the search bar.
    search_bar.send_keys(Keys.RETURN)  # Simulates pressing the Enter key to submit the search.

    # Wait until the search results are visible on the new page.
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, ".sku-header"))
    )

    # Gather all elements that represent individual TV listings on the search results page.
    tvs = driver.find_elements(By.CSS_SELECTOR, ".sku-item")

    # List to store results
    results = []

    # Loop through each TV listing to extract and print the required details.
    for tv in tvs:
        try:
            # Extract and print the TV title from each listing.
            title = tv.find_element(By.CSS_SELECTOR, ".sku-header a").text

            # Continue only if the title matches the search query criteria.
            if any(keyword in title for keyword in ['75"', '76"', '77"', '78"', '79"', '80"', '81"', '82"', '83"', '84"', '85"']):
                try:
                    # Attempt to extract the price; if not present, set a default message.
                    price = tv.find_element(By.CSS_SELECTOR, ".priceView-customer-price span").text
                except:
                    price = "No price listed"

                try:
                    # Attempt to extract sales end date information; format it if present.
                    sales_end = tv.find_element(By.CSS_SELECTOR, ".priceView-price-messaging span").text
                    if "Ends" in sales_end:
                        sales_end_date = sales_end.split("Ends ")[1]
                    else:
                        sales_end_date = "No specific end date"
                except:
                    sales_end_date = "No sales information"

                # Store the result
                result = f"TV: {title}, Price: {price}, Sales End Date: {sales_end_date}"
                results.append(result)

        except Exception as e:
            # Store the exception message
            results.append(f"Error processing TV: {str(e)}")

    return results

# Specify the path to chromedriver.exe
service = Service(executable_path='./chromedriver.exe')

# Initialize the Chrome browser session using the specified service.
driver = webdriver.Chrome(service=service)

# Directs the browser to open the URL for Best Buy's homepage.
driver.get("https://www.bestbuy.ca")

# Maximizes the browser window to ensure visibility of all web elements.
driver.maximize_window()

# Pause the script for 5 seconds to allow the web page to load completely.
time.sleep(5)

# Attempt to find and close any popup that might block further interactions.
try:
    close_popup = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, ".c-modal-close-icon"))
    )
    close_popup.click()
except:
    print("No popup found")

# Read search queries from the text file
with open('search_queries.txt', 'r') as file:
    queries = file.readlines()

all_results = []

# Perform search and extract data for each query
for query in queries:
    query = query.strip()  # Remove any leading/trailing whitespace
    if query:
        print(f"\nSearching for: {query}")
        results = search_and_extract(driver, query)
        all_results.extend(results)

# Write the results to a file
with open('search_results.txt', 'w') as file:
    for result in all_results:
        file.write(result + "\n")

# Close the browser after completing all operations.
driver.quit()

