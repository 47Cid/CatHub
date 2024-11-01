import time
from selenium import webdriver

# URL to visit
url = "http://localhost:5000/?note=SomeText#:~:text=Administrator"

# Number of seconds to wait between visits
wait_time = 300  # 5 minutes

# Initialize the Chrome driver
driver = webdriver.Chrome()

try:
    while True:
        # Visit the URL
        driver.get(url)
        
        # Wait for the specified time before visiting again
        time.sleep(wait_time)
finally:
    driver.quit()