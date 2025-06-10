import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup


class ThreadsScraper:
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--incognito") 
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        self.wait = WebDriverWait(self.driver, 15) # Using a 15-second wait for login
        self.scraped_posts_text = set()
  
    def login_threads(self, username, password):
        print("Navigating to Threads to login...")
        Threads_URL = "https://www.threads.com/login?hl=jp" 
        self.driver.get(Threads_URL)

        try:
            # login_link = self.wait.until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "Login")))
            # login_link.click()
            username_field = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[autocomplete="username"]')))
            username_field.send_keys(username)
            password_field = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[autocomplete='current-password']")))
            password_field.send_keys(password)

            # Better button selector - simpler XPath
            login_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@role='button' and .//div[text()='Log in']]")))
            login_button.click()

            time.sleep(5)
            print("Login successful!")
            return True

        except Exception as e:
            print(f"Login failed: {e}")
            self.driver.quit()
            return False
    
    def search(self, keyword):
        print("Accessing the search bar...")

        try: 
            # Clicking the searchbar input field
            searchbar_button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href='/search']")))
            searchbar_button.click()

            # Inputting keyword into searchbar
            search_input = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='search']")))
            search_input.send_keys(keyword)
            search_input.send_keys(Keys.RETURN)
            time.sleep(5)
            print(f"Search for '{keyword}' successful!")
            return True
      
        except Exception as e:
            print(f"Search failed: {e}")
            self.driver.quit()
            return False

    def scrape(self, num_posts):
        print(f"Starting to scrape for {num_posts} posts...")
        body_element = self.driver.find_element(By.TAG_NAME, 'body')

        # FIXED: Use num_posts instead of hardcoded 50
        while len(self.scraped_posts_text) < num_posts:
            self.html_doc = self.driver.page_source
            soup = BeautifulSoup(self.html_doc, 'html.parser')

            # Find all 'div' tags with the specified class
            text_elements = soup.find_all('div', class_='x1a6qonq')

            # Loop through the found elements and collect their text
            for element in text_elements:
                post_text = element.get_text(strip=True)
                post_text = post_text.removesuffix("Translate").strip() # Erase translate button text

                if post_text and len(post_text) > 10:  # Filter out very short or empty posts
                    self.scraped_posts_text.add(post_text)

            if len(self.scraped_posts_text) >= num_posts:
                print(f"Goal of {num_posts} unique posts reached.")
                break
        
            print(f"Found {len(self.scraped_posts_text)} posts, scrolling down...")
            body_element.send_keys(Keys.PAGE_DOWN)
            time.sleep(3)
      
        # Finish scraping process and close driver
        print("Scraping finished.")
        self.driver.quit()
        final_data= list(self.scraped_posts_text)[:num_posts]
        return [{'id': i, 'post': post_content} for i, post_content in enumerate(final_data, start=1)]