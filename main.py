from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os

USERNAME = input("Masukkan username Instagram: ")
PASSWORD = input("Masukkan password Instagram: ")


num_highlights = int(input("Masukkan jumlah highlight yang ingin di-screenshot: "))
highlight_ids = []
for i in range(num_highlights):
    hid = input(f"Masukkan ID highlight ke-{i+1}: ")
    highlight_ids.append(hid)


HIGHLIGHT_URLS = [f"https://www.instagram.com/stories/highlights/{hid}/" for hid in highlight_ids]

SAVE_PATH = input("Masukkan path penyimpanan media: ")


chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920x1080")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=chrome_options)
wait = WebDriverWait(driver, 10)

def is_homepage():
    
    try:
        return driver.find_element(
            By.XPATH,
            '//div[@role="button" and .//span[contains(., "Create")] '
            'and .//svg[@aria-label="New post"]]'
        ) is not None
    except:
        return False

def login():
    driver.get("https://www.instagram.com/accounts/login/")
    
    username_input = wait.until(EC.presence_of_element_located((By.NAME, "username")))
    password_input = wait.until(EC.presence_of_element_located((By.NAME, "password")))

    username_input.send_keys(USERNAME)
    password_input.send_keys(PASSWORD)
    password_input.send_keys(Keys.RETURN)
    
    time.sleep(5)

def screenshot_story(highlight_url, folder_name, delay=5):
    driver.get(highlight_url)
    time.sleep(3)

    try:
        view_stories_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'x1i10hfl') and contains(text(), 'View story')]")))
        view_stories_button.click()
        time.sleep(3)
    except:
        print("[WARNING] Tidak menemukan tombol View Stories.")

    last_story_element = None  
    story_count = 0 

    while True:
        try:
            current_story_element = wait.until(EC.presence_of_element_located((By.XPATH, "//time")))
            story_text = current_story_element.get_attribute("datetime")  
        except:
            print("[INFO] Story habis atau tidak bisa diambil.")
            break

        if last_story_element != story_text:
            story_count += 1
            last_story_element = story_text

            screenshot_path = os.path.join(folder_name, f"story_{story_count}.png")
            driver.save_screenshot(screenshot_path)
            print(f"[INFO] Screenshot {story_count} disimpan di {screenshot_path}")

        time.sleep(delay)

    print("[INFO] Semua screenshot selesai.")

login()

for index, highlight_url in enumerate(HIGHLIGHT_URLS):
    folder_name = os.path.join(SAVE_PATH, f"highlight_{index+1}")
    os.makedirs(folder_name, exist_ok=True)
    screenshot_story(highlight_url, folder_name)

driver.quit()
print("[INFO] Semua screenshot selesai.")
