from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import time

# Set up the Chrome WebDriver (specify path to chromedriver if needed)
driver = webdriver.Chrome()

# URL of the website to scrape
base_url = "http://quotes.toscrape.com"


# Function to scrape quotes from a single page
def scrape_page():
    # Find all the quote elements
    quotes_elements = driver.find_elements(By.CLASS_NAME, "quote")

    # List to hold the scraped data
    quotes_list = []

    for quote in quotes_elements:
        # Extract quote text
        text = quote.find_element(By.CLASS_NAME, "text").text
        # Extract author name
        author = quote.find_element(By.CLASS_NAME, "author").text
        # Extract tags
        tags_elements = quote.find_elements(By.CLASS_NAME, "tag")
        tags = [tag.text for tag in tags_elements]

        # Append the data to the list
        quotes_list.append({
            'Quote': text,
            'Author': author,
            'Tags': ', '.join(tags)
        })

    return quotes_list


# Function to scrape all pages
def scrape_quotes():
    url = base_url
    all_quotes = []

    driver.get(url)  # Open the website

    while True:
        print(f"Scraping {driver.current_url} ...")
        quotes = scrape_page()
        all_quotes.extend(quotes)

        # Check if there's a "Next" button and click it if available
        try:
            next_button = driver.find_element(By.LINK_TEXT, "Next")
            next_button.click()  # Click the "Next" button to go to the next page
            time.sleep(2)  # Add a short delay to wait for the page to load
        except:
            print("No more pages found.")
            break

    return all_quotes


# Function to save quotes to a CSV file
def save_to_csv(quotes):
    with open('quotes_selenium.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Quote', 'Author', 'Tags']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for quote in quotes:
            writer.writerow(quote)


# Main execution
if __name__ == '__main__':
    all_quotes = scrape_quotes()
    save_to_csv(all_quotes)
    print("Quotes have been successfully scraped and saved to 'quotes_selenium.csv'.")
    driver.quit()
