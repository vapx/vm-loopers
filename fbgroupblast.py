from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import pyperclip
import time
import os
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# Parameters
email_txt = 'matteomina1275@gmail.com'
pwd_txt = 'napkow-Zijto4-reztys'
post_text = "This is the caption for the post."
file_name = "groups.txt"
image_path = "/Users/kimdeleon/Downloads/sample.png"

# Path to chromedriver
PATH = r'/Users/kimdeleon/Downloads/chromedriver-mac-arm64/chromedriver'
service = Service(PATH)

chrome_options = webdriver.ChromeOptions()
prefs = {"profile.default_content_setting_values.notifications": 2}
chrome_options.add_experimental_option("prefs", prefs)

driver = webdriver.Chrome(service=service, options=chrome_options)
driver.get("https://www.facebook.com")
time.sleep(3)

# Login to Facebook
email_field = driver.find_element(By.NAME, "email")
email_field.send_keys(email_txt)

password_field = driver.find_element(By.NAME, "pass")
password_field.send_keys(pwd_txt)

login_button = driver.find_element(By.NAME, "login")
login_button.click()

# Wait for the page to load
time.sleep(5)

# Check if user is logged in
try:
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//a[@aria-label='Home']"))
    )
    print("Login successful!")
except TimeoutException:
    print("Login failed. Please check your credentials or login process.")
    driver.quit()
    exit()

# Open file with group URLs
with open(file_name, "r") as f:
    group_urls = f.readlines()

# Function to copy the image to clipboard (Mac-specific)
def copy_image_to_clipboard(image_path):
    os.system(f'osascript -e \'set the clipboard to (read (POSIX file "{image_path}") as JPEG picture)\'')

# Main cycle to post in each group
for group_url in group_urls:
    group_url = group_url.strip()  # Remove any extra whitespace/newline

    print(f"Navigating to group: {group_url}")
    driver.get(group_url)
    
    # Wait for the group page to load
    time.sleep(5)

    print("Scrolling the page to load elements...")
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)  # Wait for scrolling

    print("Waiting for the 'Write something...' section...")
    try:
        write_something_button = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, "//span[text()='Write something...']"))
        )
        
        driver.execute_script("arguments[0].scrollIntoView(true);", write_something_button)  # Scroll to the button
        time.sleep(1)  # Wait a moment after scrolling

        # Click using JavaScript to avoid interception issues
        driver.execute_script("arguments[0].click();", write_something_button)

        # Wait for the text area to become visible
        caption_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[@aria-label='Create a public post…' and @role='textbox']"))
        )

        # Type the caption
        caption_box.click()
        pyperclip.copy(post_text)
        caption_box.send_keys(pyperclip.paste())
        print("Caption typed successfully.")
 
        # Paste the image from clipboard
        print("Copying image to clipboard...")
        copy_image_to_clipboard(image_path)
        time.sleep(5)  # Give time for the image to be copied

        print("Pasting the image...")
        caption_box.click()  # Focus again on the post box
        time.sleep(1)  # Small delay before pasting

        caption_box.send_keys(Keys.COMMAND, 'v')  # Simulate paste (CMD+V on Mac)
        print("Image pasted successfully.")

        # Ensure the post button is clickable
        print("Waiting for the post button to be clickable...")
        post_button = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@aria-label='Post']"))
        )
        
        # Scroll to the button to ensure it's visible
        driver.execute_script("arguments[0].scrollIntoView(true);", post_button)
        time.sleep(1)

        # Click the post button via JavaScript
        print("Clicking the post button...")
        driver.execute_script("arguments[0].click();", post_button)
        time.sleep(5)  # Wait for the post to be processed

        # Wait for confirmation that the post has been added
        print("Waiting for the post to appear in the group feed...")
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'This is the caption for the post.')]"))
        )
        print("Post submitted successfully and is now visible in the group feed.")

    except TimeoutException:
        print(f"Timeout: Element not found in group {group_url}.")
    except NoSuchElementException as e:
        print(f"Element not found: {e}")
    except Exception as e:
        print(f"Failed to post in group {group_url}: {e}")

# Close the browser
driver.quit()