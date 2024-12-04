from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import time
# chang this to your own chrome driver path
# chrome driver:https://googlechromelabs.github.io/chrome-for-testing/
chrome_driver_path = r"D:\download\chromedriver-win64\chromedriver-win64\chromedriver.exe"
service = Service(chrome_driver_path)

options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
driver = webdriver.Chrome(service=service, options=options)

base_url = "https://www.purdue.edu/newsroom/articles/"

with open("purdue_articles.csv", mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Year", "URL"])

    for year in range(2011, 2025):
        for page in range(1, 100):
            url = f"{base_url}?order=DESC&orderby=date&paged={page}&filter_year={year}"
            print(f"Processing: {url}")
            driver.get(url)
            time.sleep(3)
            try:
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "purdue-home-cta-card--story"))
                )
            except Exception as e:
                print(f"Timeout or no articles found: {url}")
                break

            articles = driver.find_elements(By.CLASS_NAME, "purdue-home-cta-card--story")
            if not articles:
                print(f"No articles found on page {page} for year {year}")
                break

            for article in articles:
                try:
                    href = article.get_attribute("href")
                except Exception as e:
                    print(f"Error getting href: {e}")
                    continue
                if href:
                    writer.writerow([year, href])
                    print(f"Added: {year}, {href}")

driver.quit()
