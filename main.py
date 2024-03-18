from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Optional - Keep the browser open (helps diagnose issues if the script crashes)
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

# Path to ChromeDriver executable
chrome_driver_path = "C:\chromedriver.exe"  # Assuming the ChromeDriver executable is named chromedriver.exe

# Create and configure the Chrome webdriver with the specified path to ChromeDriver
driver = webdriver.Chrome(executable_path=chrome_driver_path, options=chrome_options)

# Open the Cookie Clicker game
driver.get("http://orteil.dashnet.org/experiments/cookie/")

# Get the clickable cookie element
cookie = driver.find_element(by=By.ID, value="cookie")

# Get IDs of all upgrade items
items = driver.find_elements(by=By.CSS_SELECTOR, value="#store div")
item_ids = [item.get_attribute("id") for item in items]

# Set a timeout for the initial loop iteration
timeout = time.time() + 5

# Set a timeout for stopping the bot after 5 minutes
five_min = time.time() + 60*5  # 5 minutes

while True:
    # Click the cookie to earn cookies
    cookie.click()

    # Every 5 seconds:
    if time.time() > timeout:

        # Get all upgrade prices
        all_prices = driver.find_elements(by=By.CSS_SELECTOR, value="#store b")
        item_prices = []

        # Convert the price text into integer prices
        for price in all_prices:
            element_text = price.text
            if element_text != "":
                cost = int(element_text.split("-")[1].strip().replace(",", ""))
                item_prices.append(cost)

        # Create a dictionary of store items and prices
        cookie_upgrades = {}
        for n in range(len(item_prices)):
            cookie_upgrades[item_prices[n]] = item_ids[n]

        # Get current cookie count
        money_element = driver.find_element(by=By.ID, value="money").text
        if "," in money_element:
            money_element = money_element.replace(",", "")
        cookie_count = int(money_element)

        # Find upgrades that can currently be afforded
        affordable_upgrades = {}
        for cost, id in cookie_upgrades.items():
            if cookie_count > cost:
                affordable_upgrades[cost] = id

        # Purchase the most expensive affordable upgrade
        highest_price_affordable_upgrade = max(affordable_upgrades)
        to_purchase_id = affordable_upgrades[highest_price_affordable_upgrade]
        driver.find_element(by=By.ID, value=to_purchase_id).click()

        # Add another 5 seconds until the next check
        timeout = time.time() + 5

    # After 5 minutes stop the bot and check the cookies per second count
    if time.time() > five_min:
        cookie_per_s = driver.find_element(by=By.ID, value="cps").text
        print(cookie_per_s)
        break
