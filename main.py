from Threads_scraper import ThreadsScraper
import time

def main():
    """
    Main function to run the Threads scraper
    """
    print("=== Threads Scraper ===")
    
    # Get user credentials
    print("Insert your Threads username: ")
    username = input()
    print("Insert your Threads password: ")
    password = input()
    
    # Get search keyword
    print("Insert the keyword you want to search: ")
    keyword = input().strip()
    if not keyword:
        keyword = "韓国"
    
    # Get number of posts to scrape
    try:
        print("How many posts do you want to scrape?: ")
        num_posts = int(input())
    except ValueError:
        num_posts = 10
        print("Invalid input, using default: 10 posts")
    
    # Initialize scraper
    scraper = ThreadsScraper()
    
    try:
        # Login to Threads
        if not scraper.login_threads(username, password):
            print("Failed to login. Exiting...")
            return
        
        # Search for keyword
        if not scraper.search(keyword):
            print("Failed to search. Exiting...")
            return
        
        # Scrape posts
        scraped_posts = scraper.scrape(num_posts)
        
        # Display results
        print(f"\n=== Scraped {len(scraped_posts)} Posts ===")
        for i, post in enumerate(scraped_posts, 1):
            print(f"\n--- Post {i} ---")
            print(post)
            print("-" * 50)
        
        # Optionally save to file
        save_to_file = input("\nSave results to file? (y/n): ").lower().strip()
        if save_to_file == 'y':
            filename = f"threads_posts_{keyword}_{int(time.time())}.txt"
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f"Threads Posts for keyword: {keyword}\n")
                f.write(f"Scraped on: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("=" * 50 + "\n\n")
                
                for i, post in enumerate(scraped_posts, 1):
                    f.write(f"Post {i}:\n{post}\n\n")
            
            print(f"Results saved to: {filename}")
    
    except KeyboardInterrupt:
        print("Scraping interrupted by user.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Ensure driver is closed
        try:
            scraper.driver.quit()
        except:
            pass


if __name__ == "__main__":
    main()