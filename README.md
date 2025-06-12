Threads Data Scraper & S3 Uploader
This project is a Python-based web scraper designed to automatically collect posts from Threads.net based on specific keywords. It uses Selenium with advanced techniques to mimic human behavior and avoid detection. Scraped data is then formatted as a JSON file and uploaded directly to a specified AWS S3 bucket.

Features
Secure Login: Securely logs into Threads.net using credentials stored in environment variables.
Keyword-Based Scraping: Iterates through a list of target keywords to search and collect relevant posts.
Human-like Behavior: Implements various techniques to mimic human interaction, such as random delays, variable scrolling speeds, and realistic mouse movements, reducing the risk of being blocked.
AWS S3 Integration: Automatically uploads scraped data as a uniquely named JSON file to an AWS S3 bucket for storage and further analysis.
Secure Credential Management: Employs a .env file for managing sensitive information like login credentials and AWS bucket names, keeping them separate from the source code.
Robust & Resilient: Includes error handling and waits for elements to load, making the scraper more reliable.
How It Works
Initialization: The main script loads environment variables (USERNAME, PASSWORD, BUCKET_NAME) from a .env file.
Login: The ThreadsScraper class initializes a Selenium WebDriver with anti-detection settings and logs into Threads.
Search & Scrape: For each keyword defined in TARGET_KEYWORD, the scraper navigates to the search results page.
Data Collection: It scrolls down the page, simulating human reading, and scrapes the text content of the posts until the desired number of posts (TARGET_POSTS_NUM) is collected.
Data Formatting: The collected data is cleaned and formatted into a JSON structure.
S3 Upload: A boto3 session is established, and the JSON data is uploaded to the specified S3 bucket. Each file is given a unique name including the keyword, date, and a UUID.
Cleanup: The browser session is properly closed upon completion or in case of an error.
Prerequisites
Before you begin, ensure you have the following installed and configured:

Python 3.9+
A Threads.net account
An AWS Account with an S3 bucket created
AWS CLI installed and configured on your machine.
Setup & Installation
Follow these steps to get your local environment set up.

1. Clone the repository
Bash

git clone https://github.com/your-username/your-repository-name.git
cd your-repository-name
2. Create a Virtual Environment (Recommended)
Bash

# For Mac/Linux
python3 -m venv venv
source venv/bin/activate

# For Windows
python -m venv venv
.\venv\Scripts\activate
3. Install Dependencies
Create a requirements.txt file with the following content:

requirements.txt

selenium
webdriver-manager
beautifulsoup4
numpy
python-dotenv
boto3
Then, install the packages:

Bash

pip install -r requirements.txt
4. Create the Environment File (.env)
Create a file named .env in the root of your project. This file should NOT be committed to GitHub. Add your sensitive credentials here.

.env

THREADS_USERNAME="your_threads_username"
THREADS_PASSWORD="your_threads_password"
BUCKET_NAME="your-aws-s3-bucket-name"
5. Configure AWS Credentials
This script uses the default AWS profile. Configure it by running the following command in your terminal and following the prompts. You will need your AWS Access Key ID and Secret Access Key.

Bash

aws configure
This will store your credentials securely in the ~/.aws/ directory, which boto3 can access automatically.

6. Add .env to .gitignore
Ensure your .gitignore file contains the following lines to prevent your secret credentials from being uploaded to GitHub.

# Environment variables
.env

# Virtual environment
venv/
__pycache__/
Usage
Customize Script: Open the main Python file and adjust the following variables if needed:

TARGET_KEYWORD: A list of Japanese keywords to search for.
TARGET_POSTS_NUM: The number of posts you want to scrape for each keyword.
Run the Script: Execute the following command from your terminal:

Bash

python main.py
The script will now launch a browser, perform the login and scraping tasks, and print progress updates to the console.

Output
Upon successful execution for a keyword, a new JSON file will be uploaded to your S3 bucket.

File Naming Convention: threads_data_{keyword}_{date}_{uuid}.json

Example: threads_data_韓国トレンド_0613_a1b2c3d4-e5f6-7890-1234-567890abcdef.json
JSON File Structure:

JSON

[
  {
    "id": 1,
    "post": "This is the text content of the first scraped post about the keyword..."
  },
  {
    "id": 2,
    "post": "This is another post that was scraped. All Japanese characters are preserved."
  }
]
⚠️ Important Security & Ethical Considerations
Credential Security: NEVER hardcode your credentials (username, password, AWS keys) directly in the Python scripts. Always use the .env file and ensure it is listed in your .gitignore.
Responsible Scraping: Web scraping can put a heavy load on servers. This script includes "human-like" delays to be considerate. Do not decrease these delays excessively. Always respect the website's terms of service and robots.txt file. Use this tool responsibly.
License: Consider adding a LICENSE file (e.g., MIT License) to your repository to define how others can use your code.
