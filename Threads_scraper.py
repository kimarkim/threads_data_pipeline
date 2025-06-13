import time
import datetime
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
import numpy as np

class ThreadsScraper:
    def __init__(self):
        options = webdriver.ChromeOptions()
        
        # Original options
        options.add_argument("--start-maximized")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--incognito")
        
        # Anti-detection measures
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        # Random user agent rotation
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        ]
        options.add_argument(f"--user-agent={random.choice(user_agents)}")
        
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        
        # Execute script to hide webdriver property
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        # Random viewport size
        viewport_sizes = [(1920, 1080), (1440, 900), (1536, 864)]
        width, height = random.choice(viewport_sizes)
        self.driver.set_window_size(width, height)
        
        self.wait = WebDriverWait(self.driver, 15)
        self.scraped_posts_text = set()
        
        # Add action chains for human-like interactions
        self.actions = ActionChains(self.driver)
    
    def login_threads(self, username, password):
        print("Navigating to Threads to login...")
        Threads_URL = "https://www.threads.com/login?hl=jp"
        
        # Add random delay before navigation
        time.sleep(random.uniform(1, 3))
        self.driver.get(Threads_URL)
        
        # Simulate page load waiting
        time.sleep(random.uniform(3, 6))

        try:
            username_field = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[autocomplete="username"]')))
            
            # Human-like interaction - move to element and click
            self.actions.move_to_element(username_field).click().perform()
            time.sleep(random.uniform(0.5, 1.5))
            
            # Human-like typing with random delays
            username_field.clear()
            for char in username:
                username_field.send_keys(char)
                time.sleep(random.uniform(0.05, 0.25))
            
            time.sleep(random.uniform(1, 2))
            
            password_field = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[autocomplete='current-password']")))
            self.actions.move_to_element(password_field).click().perform()
            time.sleep(random.uniform(0.5, 1.5))
            
            # Human-like typing for password
            password_field.clear()
            for char in password:
                password_field.send_keys(char)
                time.sleep(random.uniform(0.05, 0.25))

            time.sleep(random.uniform(1, 3))

            login_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@role='button' and .//div[text()='Log in']]")))
            self.actions.move_to_element(login_button).pause(random.uniform(0.5, 1.5)).click().perform()

            # Random wait time for login
            login_wait = random.uniform(5, 10)
            time.sleep(login_wait)
            print("Login successful!")
            return True

        except Exception as e:
            print(f"Login failed: {e}")
            self.driver.quit()
            return False
    
    def redirect_url(self, keyword):
        print("Accessing the url bar...")
        
        # Random delay before redirection
        time.sleep(random.uniform(2, 5))
        
        # Redirection to recent thread posts about Korea
        try:
            self.driver.get(f"https://www.threads.com/search?q={keyword}")
            return True
            
        except Exception as e:
            print(f"Redirection failed: {e}")
            self.driver.quit()
            return False


    def scrape(self, num_posts, start_id=1, max_scrolls=20):
        self.scraped_posts_text.clear()
        # More robust selectors
        selector = "div[class*='x1a6qonq'] span[class*='x1lliihq'][dir='auto'] span"

        try:
            # Wait for content to load
            self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
            print("Post containers found. Starting to scrape.")
            time.sleep(random.uniform(2, 4))
        except Exception as e:
            print(f"No post containers found with selector: {selector}. Error: {e}")
            return []

        scroll_count = 0
        consecutive_small_scrolls = 0

        while len(self.scraped_posts_text) < num_posts and scroll_count < max_scrolls:
            try:
                self.html_doc = self.driver.page_source
                soup = BeautifulSoup(self.html_doc, 'html.parser')

                # Find all 'div' tags with the specified class
                text_elements = soup.find_all('div', class_='x1a6qonq')
                
                # Extract text from elements
                for element in text_elements:
                    post_text = element.get_text(strip=True)
                    post_text = post_text.removesuffix("Translate").strip() 

            # Find all 'div' tags with the specified class
                    if post_text and len(post_text) > 10:  # Filter out very short or empty posts
                        self.scraped_posts_text.add(post_text)
            
                # Human-like scrolling behavior
                if random.random() < 0.7:  # 70% normal scroll
                    scroll_amount = random.randint(300, 800)
                    # Sometimes scroll in chunks
                    if random.random() < 0.3:
                        chunks = random.randint(2, 4)
                        chunk_size = scroll_amount // chunks
                        for _ in range(chunks):
                            self.driver.execute_script(f"window.scrollBy(0, {chunk_size});")
                            time.sleep(random.uniform(0.1, 0.5))
                    else:
                        self.driver.execute_script(f"window.scrollBy(0, {scroll_amount});")
                    consecutive_small_scrolls = 0
                else:  # 30% small scroll (like reading carefully)
                    scroll_amount = random.randint(100, 300)
                    self.driver.execute_script(f"window.scrollBy(0, {scroll_amount});")
                    consecutive_small_scrolls += 1
                
                # Simulate reading behavior (30% chance)
                if random.random() < 0.3:
                    reading_time = random.uniform(2, 8)
                    print(f"Simulating reading behavior ({reading_time:.1f}s)...")
                    time.sleep(reading_time)
                
                # Occasional longer pauses like getting distracted (10% chance)
                if random.random() < 0.1:
                    distraction_time = random.uniform(8, 10)
                    print(f"Simulating distraction ({distraction_time:.1f}s)...")
                    time.sleep(distraction_time)
                
                # After several small scrolls, do a larger one
                if consecutive_small_scrolls >= 3:
                    print("Doing a larger scroll after careful reading...")
                    large_scroll = random.randint(600, 1200)
                    self.driver.execute_script(f"window.scrollBy(0, {large_scroll});")
                    consecutive_small_scrolls = 0
                
                scroll_count += 1
                
                # Use exponential distribution for more natural timing
                cycle_delay = np.random.exponential(3) + 1
                cycle_delay = min(cycle_delay, 10)  # Cap at 10 seconds
                time.sleep(cycle_delay)
                
            except Exception as e:
                print(f"Error during scraping iteration: {e}")
                scroll_count += 1
                time.sleep(random.uniform(2, 5))
                continue
        
        upload_date = datetime.datetime.now()
        final_data = list(self.scraped_posts_text)[:num_posts]
        return [{'id': i, 'upload date': upload_date.strftime('%Y.%b.%a.%H.%M'), 'post': post_content} for i, post_content in enumerate(final_data, start=start_id)]

        
    def close_session(self):
        print("\nAll tasks finished. Closing the browser.")
        
        # Human-like closing behavior
        time.sleep(random.uniform(1, 3))
        
        if self.driver:
            self.driver.quit()