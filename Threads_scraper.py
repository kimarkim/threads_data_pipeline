import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys




class ThreadsScraper:
  def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        self.wait = WebDriverWait(self.driver, 15) # Using a 15-second wait for login
        self.scraped_posts_text = set()
  
  def login_threads(self, username, password):
    print("Navigating to Threads to login. . .")
    Threads_URL = "https://www.threads.com/?hl=jp"
    self.driver.get(Threads_URL)

    try:
      login_link = self.wait.until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "Log in with username instead")))
      login_link.click()

      username_field = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[autocomplete="username"]')))
      username_field.send_keys(username)

      password_field = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[autocomplete='current-password']")))
      password_field.send_keys(password)

      # Better button selector - simpler XPath
      login_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div/div/div[3]/div/div/div/div[2]/div[1]/div[3]/form/div/div[1]/div[2]/div[2]/div/div/div')))
      login_button.click()

      time.sleep(5)
      

    except Exception as e:
        print(f"Login failed: {e}")
        self.driver.quit()
        return False
    
    def search(self, keyword):
      print("Accessing the search bar. . .")

      try: 
        # Clicking the searchbar input field
        searchbar_button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "svg[aria-label='검색']")))
        searchbar_button.click()

        # Inputting keyword into searchbar
        search_input = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='search']")))
        search_input.send_keys(keyword)

        # Pressing the search recommendation
        key_recomm = self.wait.until(EC.presence_of_element_located((By.XPATH, "//span[text()='韓国']/parent::div")))
        key_recomm.click()
        time.sleep(5)
      
      except Exception as e:
        print(f"Searchbar failed: {e}")
        self.driver.quit()
        return False


    def scrape(self, num_posts):
      print(f"Starting to scrape for {num_posts} posts...")
      element = self.driver.find_element(By.TAG_NAME, 'body')

      while len(self.scraped_posts_text) < 50:
        self.html_doc = self.driver.page_source
        soup = BeautifulSoup(self.html_doc, 'html.parser')

        # Find all 'span' tags where the 'dir' attribute is 'auto'
        text_elements = soup.find_all('div', class_='x1a6qonq')

        # Loop through the found elements and print their text
        for element in text_elements:
            # .get_text(strip=True) cleans up whitespace
            print(element.get_text(strip=True))

        if len(self.scraped_posts_text) >= num_posts:
                print(f"Goal of {num_posts} unique posts reached.")
                break
        
        print(f"Found {len(self.scraped_posts_text)} posts, scrolling down...")
        element.send_keys(Keys.PAGE_DOWN)
        time.sleep(3)
      
      # Finish scraping process and driver
      print("Scraping finished.")
      self.driver.quit()
      return list(self.scraped_posts_text)[:num_posts]