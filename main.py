import os
import time
import json
import boto3
import uuid
import datetime
from Threads_scraper import ThreadsScraper
from dotenv import load_dotenv

load_dotenv()

USERNAME = os.environ.get('THREADS_USERNAME')
PASSWORD = os.environ.get('THREADS_PASSWORD')
TARGET_KEYWORD = ["韓国","韓国トレンド","韓国旅行"]
TARGET_POSTS_NUM = 50
BUCKETNAME = os.environ.get('BUCKET_NAME')


def main():
  scraper = ThreadsScraper()

  try:
    if scraper.login_threads(USERNAME, PASSWORD):

      for keyword in TARGET_KEYWORD:
        if scraper.redirect_url(keyword):

          # Search target keyword
          time.sleep(2)

          # Scrape data
          scraped_data = scraper.scrape(TARGET_POSTS_NUM)

          if scraped_data:
            # Get scrape & upload date
            time_now = datetime.datetime.now().strftime("%m%d")

            # Provide file uuid
            unique_id = uuid.uuid4()

            # Target file name configure
            target_file_name = f'threads_data_{keyword}_{time_now}_{unique_id}.json'

            # Convert Python list to json formatted string
            # ensure_ascii=False used for smoothe Japanese txt recognition
            upload_data = json.dumps(scraped_data, indent=2, ensure_ascii=False).encode('utf-8')
            session = boto3.Session(profile_name='default')
            s3 = session.client('s3')

            s3.put_object(
              Bucket=BUCKETNAME,
              Key=target_file_name,
              Body=upload_data,
              ContentType='application/json' # Good practice to set the content type
            )
            print("✅ Upload successful!")
      scraper.close_session() 

  except Exception as e:
    print(f"An unexpected error occurred in the main process: {e}")

  finally:
    # --- 4. Always ensure the browser is closed ---
    print("✅ Task Done ✅")

if __name__ == "__main__":

  main()
