import os
import time
import json
import boto3
import datetime
from Threads_scraper import ThreadsScraper
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# --- Configuration ---
USERNAME = os.environ.get('THREADS_USERNAME')
PASSWORD = os.environ.get('THREADS_PASSWORD')
TARGET_KEYWORD = ["韓国", "韓国トレンド", "韓国旅行"]
TARGET_POSTS_NUM = 50
BUCKETNAME = os.environ.get('BUCKET_NAME')

def main():
  """
  Main function to orchestrate the scraping and S3 upload process.
  """
  scraper = ThreadsScraper()

  try:
    if scraper.login_threads(USERNAME, PASSWORD):
      
      # It's more efficient to create the S3 client once, outside the loop
      session = boto3.Session(profile_name='default')
      s3 = session.client('s3')

      for keyword in TARGET_KEYWORD:
        if not scraper.redirect_url(keyword):
          print(f"Failed to redirect for keyword: {keyword}. Skipping.")
          continue
        
        time.sleep(2)  # Wait for page to load after redirect

        target_file_name = f'threads_data_{keyword}.json'
        existing_data = []
        start_id = 1

        # Step 1: Get Existing Data from S3 (if it exists)
        try:
          response = s3.get_object(Bucket=BUCKETNAME, Key=target_file_name)
          body = response['Body'].read().decode('utf-8')
          existing_data = json.loads(body)
          print(f"Successfully loaded {len(existing_data)} existing posts for keyword '{keyword}'.")

          # Step 2: Determine the Next ID to start from
          if existing_data:
            last_id = existing_data[-1]['id']
            start_id = last_id + 1

        except s3.exceptions.NoSuchKey:
          print(f"No existing file for '{keyword}'. Starting new file with ID 1.")
        
        # Step 3: Scrape New Data, passing the correct starting ID
        newly_scraped_data = scraper.scrape(TARGET_POSTS_NUM, start_id=start_id)

        # Step 4: Filter to only add posts that are actually new
        existing_posts_set = {post['post'] for post in existing_data}
        new_unique_posts = [
            scraped_post for scraped_post in newly_scraped_data 
            if scraped_post['post'] not in existing_posts_set
        ]

        if not new_unique_posts:
          print(f"Scraped data contains no new unique posts for '{keyword}'. Nothing to upload.")
          continue

        print(f"Found {len(new_unique_posts)} new unique posts to add.")

        # Step 5: Combine old and new data, then upload the complete file
        final_upload_list = existing_data + new_unique_posts
        final_upload_body = json.dumps(final_upload_list, indent=2, ensure_ascii=False).encode('utf-8')

        s3.put_object(
          Bucket=BUCKETNAME,
          Key=target_file_name,
          Body=final_upload_body,
          ContentType='application/json'
        )
        
        print(f"✅ Successfully uploaded {len(final_upload_list)} total posts for '{keyword}'.")

      scraper.close_session()

  except Exception as e:
    print(f"An unexpected error occurred in the main process: {e}")

  finally:
    print("✅ Task Done ✅")


if __name__ == "__main__":
  main()