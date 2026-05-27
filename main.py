"""
Main scraper runner for PEI Local News

Runs all three scrapers (Twitter, Reddit, Facebook) and aggregates results.
"""

import logging
from scrapers.twitter_scraper import TwitterScraper
from scrapers.reddit_scraper import RedditScraper
from scrapers.facebook_scraper import FacebookScraper
from database import NewsDatabase

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def run_all_scrapers():
    """Run all scrapers and display results."""
    print("\n" + "=" * 80)
    print("PEI LOCAL NEWS SCRAPER - FULL RUN")
    print("=" * 80 + "\n")

    db = NewsDatabase()

    # Twitter
    print("\n[1/3] Running Twitter Scraper...")
    twitter_scraper = TwitterScraper()
    twitter_posts = twitter_scraper.scrape_all_queries()
    twitter_scraper.display_results(twitter_posts, limit=3)

    # Reddit
    print("\n[2/3] Running Reddit Scraper...")
    reddit_scraper = RedditScraper()
    reddit_posts = reddit_scraper.search_all_keywords()
    reddit_scraper.display_results(reddit_posts, limit=3)

    # Facebook
    print("\n[3/3] Running Facebook Scraper...")
    facebook_scraper = FacebookScraper()
    facebook_posts = facebook_scraper.scrape_all_pages()
    facebook_scraper.display_results(facebook_posts, limit=3)

    # Summary
    print("\n" + "=" * 80)
    print("SCRAPING SUMMARY")
    print("=" * 80)
    print(f"Twitter posts scraped:   {len(twitter_posts)}")
    print(f"Reddit posts scraped:    {len(reddit_posts)}")
    print(f"Facebook posts scraped:  {len(facebook_posts)}")
    print(f"Total posts collected:   {len(twitter_posts) + len(reddit_posts) + len(facebook_posts)}")
    print("=" * 80)

    # Database summary
    print("\nDatabase Summary:")
    print(f"Twitter posts in DB:  {db.get_post_count('twitter_posts')}")
    print(f"Reddit posts in DB:   {db.get_post_count('reddit_posts')}")
    print(f"Facebook posts in DB: {db.get_post_count('facebook_posts')}")

    # Export to CSV
    print("\n" + "=" * 80)
    print("EXPORTING TO CSV")
    print("=" * 80)
    db.export_to_csv("twitter_posts")
    db.export_to_csv("reddit_posts")
    db.export_to_csv("facebook_posts")

    print("\nScraping complete! Check output/exports/ for CSV files.")


def run_twitter_only():
    """Run only Twitter scraper."""
    logger.info("Running Twitter scraper only...")
    scraper = TwitterScraper()
    posts = scraper.scrape_all_queries()
    scraper.display_results(posts)
    return posts


def run_reddit_only():
    """Run only Reddit scraper."""
    logger.info("Running Reddit scraper only...")
    scraper = RedditScraper()
    posts = scraper.search_all_keywords()
    scraper.display_results(posts)
    return posts


def run_facebook_only():
    """Run only Facebook scraper."""
    logger.info("Running Facebook scraper only...")
    scraper = FacebookScraper()
    posts = scraper.scrape_all_pages()
    scraper.display_results(posts)
    return posts


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        if sys.argv[1] == "twitter":
            run_twitter_only()
        elif sys.argv[1] == "reddit":
            run_reddit_only()
        elif sys.argv[1] == "facebook":
            run_facebook_only()
        else:
            print("Usage: python main.py [twitter|reddit|facebook]")
            print("Or run without arguments to run all scrapers")
    else:
        run_all_scrapers()
