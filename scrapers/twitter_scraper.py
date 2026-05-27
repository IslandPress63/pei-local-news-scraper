"""
Twitter/X Scraper for PEI Local News

Scrapes tweets about PEI, West Prince, and eastern PEI using snscrape.
"""

import snscrape.modules.twitter as sntwitter
import time
import logging
from datetime import datetime, timedelta
from config import TWITTER_SEARCH_QUERIES, TWITTER_RATE_LIMIT, POSTS_LIMIT, DAYS_BACK
from database import NewsDatabase

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TwitterScraper:
    """Scrapes tweets using snscrape library."""

    def __init__(self):
        """Initialize Twitter scraper."""
        self.db = NewsDatabase()
        self.rate_limit = TWITTER_RATE_LIMIT

    def scrape_tweets(self, query, max_posts=POSTS_LIMIT):
        """
        Scrape tweets for a given query.

        Args:
            query (str): Search query
            max_posts (int): Maximum posts to retrieve

        Returns:
            list: List of tweet data
        """
        tweets = []

        try:
            logger.info(f"Scraping tweets for query: {query}")

            # Build search query with date filter
            if DAYS_BACK:
                since_date = (datetime.now() - timedelta(days=DAYS_BACK)).strftime("%Y-%m-%d")
                search_query = f"{query} since:{since_date}"
            else:
                search_query = query

            # Scrape using snscrape
            scraper = sntwitter.TwitterSearchScraper(search_query)
            for i, tweet in enumerate(scraper.get_items()):
                if i >= max_posts:
                    break

                tweet_data = {
                    "id": tweet.id,
                    "username": tweet.author.username,
                    "content": tweet.content,
                    "url": f"https://twitter.com/{tweet.author.username}/status/{tweet.id}",
                    "created_at": tweet.date,
                    "engagement": tweet.likeCount + tweet.retweetCount + tweet.replyCount,
                }

                tweets.append(tweet_data)

                # Store in database
                self.db.insert_twitter_post(
                    tweet_data["id"],
                    tweet_data["username"],
                    tweet_data["content"],
                    tweet_data["url"],
                    tweet_data["created_at"],
                    tweet_data["engagement"],
                )

                # Rate limiting
                time.sleep(self.rate_limit)

            logger.info(f"Successfully scraped {len(tweets)} tweets for '{query}'")

        except Exception as e:
            logger.error(f"Error scraping tweets for '{query}': {str(e)}")

        return tweets

    def scrape_all_queries(self):
        """Scrape tweets for all configured queries."""
        all_tweets = []

        for query in TWITTER_SEARCH_QUERIES:
            tweets = self.scrape_tweets(query)
            all_tweets.extend(tweets)
            time.sleep(self.rate_limit * 2)  # Extra delay between queries

        logger.info(f"Total tweets scraped: {len(all_tweets)}")
        return all_tweets

    def display_results(self, tweets, limit=5):
        """Display sample of scraped tweets."""
        print(f"\n{'='*80}")
        print(f"TWITTER SCRAPER RESULTS - Sample (showing {min(limit, len(tweets))} of {len(tweets)})")
        print(f"{'='*80}\n")

        for i, tweet in enumerate(tweets[:limit], 1):
            print(f"Tweet {i}:")
            print(f"  Author: @{tweet['username']}")
            print(f"  Date: {tweet['created_at']}")
            print(f"  Content: {tweet['content'][:200]}...")
            print(f"  Engagement: {tweet['engagement']}")
            print(f"  URL: {tweet['url']}\n")


if __name__ == "__main__":
    scraper = TwitterScraper()
    tweets = scraper.scrape_all_queries()
    scraper.display_results(tweets)
