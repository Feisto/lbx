#!/usr/bin/env python3
"""
Letterboxd Review Scraper
Fetches and displays reviews for films on Letterboxd
"""

import requests
from bs4 import BeautifulSoup
import sys
import re
import time
from typing import List, Dict, Optional


class LetterboxdReviewScraper:
    """Scraper for Letterboxd film reviews"""

    BASE_URL = "https://letterboxd.com"

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Cache-Control': 'max-age=0'
        })

    def extract_film_slug(self, url: str) -> Optional[str]:
        """Extract film slug from Letterboxd URL"""
        # Handle both full URLs and slugs
        if url.startswith('http'):
            match = re.search(r'letterboxd\.com/film/([^/]+)', url)
            if match:
                return match.group(1)
        else:
            # Assume it's already a slug
            return url.strip('/')
        return None

    def get_reviews(self, film_slug: str, page: int = 1, sort: str = 'popular') -> List[Dict]:
        """
        Fetch reviews for a film

        Args:
            film_slug: The film's slug (e.g., 'taxi-1998')
            page: Page number for pagination
            sort: Sort order ('popular', 'recent', 'highest-rated', 'lowest-rated')

        Returns:
            List of review dictionaries containing username, rating, review text, etc.
        """
        # Try AJAX endpoint first (less likely to be blocked)
        ajax_url = f"{self.BASE_URL}/film/{film_slug}/reviews/by/{sort}/page/{page}/"

        # Add small delay to avoid rate limiting
        time.sleep(0.5)

        try:
            # Try with AJAX headers first
            ajax_headers = {
                'X-Requested-With': 'XMLHttpRequest',
                'Referer': f'{self.BASE_URL}/film/{film_slug}/',
            }
            response = self.session.get(ajax_url, headers=ajax_headers, timeout=15)
            response.raise_for_status()
        except requests.RequestException:
            # If AJAX fails, try regular request
            try:
                response = self.session.get(ajax_url, timeout=15)
                response.raise_for_status()
            except requests.RequestException as e:
                print(f"Error fetching reviews: {e}", file=sys.stderr)
                print(f"URL attempted: {ajax_url}", file=sys.stderr)
                return []

        soup = BeautifulSoup(response.content, 'lxml')
        reviews = []

        # Find all review items
        review_items = soup.find_all('li', class_='film-detail')

        for item in review_items:
            review = self._parse_review_item(item)
            if review:
                reviews.append(review)

        return reviews

    def _parse_review_item(self, item) -> Optional[Dict]:
        """Parse a single review item"""
        review = {}

        # Get username
        user_link = item.find('strong', class_='name')
        if user_link:
            review['username'] = user_link.get_text(strip=True)

        # Get rating (stars)
        rating_span = item.find('span', class_='rating')
        if rating_span:
            # Count filled stars
            stars = len(rating_span.find_all('span', class_='rated-'))
            review['rating'] = stars / 2  # Letterboxd uses half-star increments
        else:
            review['rating'] = None

        # Get review text
        review_body = item.find('div', class_='body-text')
        if review_body:
            # Remove "read more" links and get clean text
            for span in review_body.find_all('span', class_='collapsed-text'):
                span.decompose()
            review_text = review_body.get_text(separator=' ', strip=True)
            review['text'] = review_text
        else:
            review['text'] = ""

        # Get likes count
        like_link = item.find('a', class_='has-icon icon-liked icon-16 has-count')
        if like_link:
            like_count = like_link.get_text(strip=True)
            try:
                review['likes'] = int(like_count) if like_count else 0
            except ValueError:
                review['likes'] = 0
        else:
            review['likes'] = 0

        # Get date
        date_span = item.find('span', class_='_nobr')
        if date_span:
            review['date'] = date_span.get_text(strip=True)

        return review if review else None

    def get_film_info(self, film_slug: str) -> Optional[Dict]:
        """Get basic film information"""
        url = f"{self.BASE_URL}/film/{film_slug}/"

        # Add small delay to avoid rate limiting
        time.sleep(0.5)

        try:
            response = self.session.get(url, timeout=15)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"Error fetching film info: {e}", file=sys.stderr)
            print(f"URL attempted: {url}", file=sys.stderr)
            print(f"\nNote: Letterboxd may be blocking automated requests.", file=sys.stderr)
            print(f"You can try:", file=sys.stderr)
            print(f"  1. Running the script again (sometimes it works after retry)", file=sys.stderr)
            print(f"  2. Using a VPN or different network", file=sys.stderr)
            print(f"  3. Waiting a few minutes before trying again", file=sys.stderr)
            return None

        soup = BeautifulSoup(response.content, 'lxml')

        info = {}

        # Get title
        title_tag = soup.find('h1', class_='headline-1')
        if title_tag:
            info['title'] = title_tag.get_text(strip=True)

        # Get year
        year_tag = soup.find('small', class_='number')
        if year_tag:
            info['year'] = year_tag.get_text(strip=True)

        # Get director
        director_tag = soup.find('span', class_='prettify')
        if director_tag:
            info['director'] = director_tag.get_text(strip=True)

        # Get average rating
        rating_meta = soup.find('meta', {'name': 'twitter:data2'})
        if rating_meta:
            info['average_rating'] = rating_meta.get('content', '')

        return info


def print_review(review: Dict, index: int):
    """Pretty print a review"""
    print(f"\n{'='*80}")
    print(f"Review #{index}")
    print(f"{'='*80}")
    print(f"User: {review.get('username', 'Anonymous')}")

    if review.get('rating'):
        stars = '★' * int(review['rating']) + '☆' * (5 - int(review['rating']))
        print(f"Rating: {stars} ({review['rating']}/5)")
    else:
        print("Rating: No rating")

    if review.get('date'):
        print(f"Date: {review['date']}")

    if review.get('likes'):
        print(f"Likes: {review['likes']}")

    if review.get('text'):
        print(f"\n{review['text']}")
    else:
        print("\n(No review text)")


def main():
    """Main CLI interface"""
    if len(sys.argv) < 2:
        print("Usage: python letterboxd_reviews.py <film_url_or_slug> [--page N] [--sort ORDER]")
        print("\nExamples:")
        print("  python letterboxd_reviews.py https://letterboxd.com/film/taxi-1998/")
        print("  python letterboxd_reviews.py taxi-1998")
        print("  python letterboxd_reviews.py taxi-1998 --page 2 --sort recent")
        print("\nSort options: popular, recent, highest-rated, lowest-rated")
        sys.exit(1)

    film_input = sys.argv[1]

    # Parse optional arguments
    page = 1
    sort = 'popular'

    for i, arg in enumerate(sys.argv[2:], 2):
        if arg == '--page' and i + 1 < len(sys.argv):
            try:
                page = int(sys.argv[i + 1])
            except ValueError:
                print(f"Invalid page number: {sys.argv[i + 1]}", file=sys.stderr)
        elif arg == '--sort' and i + 1 < len(sys.argv):
            sort = sys.argv[i + 1]

    scraper = LetterboxdReviewScraper()

    # Extract film slug
    film_slug = scraper.extract_film_slug(film_input)
    if not film_slug:
        print(f"Invalid film URL or slug: {film_input}", file=sys.stderr)
        sys.exit(1)

    # Get film info
    print(f"Fetching film information...")
    film_info = scraper.get_film_info(film_slug)

    if film_info:
        print(f"\n{'='*80}")
        print(f"Film: {film_info.get('title', 'Unknown')}")
        if film_info.get('year'):
            print(f"Year: {film_info['year']}")
        if film_info.get('director'):
            print(f"Director: {film_info['director']}")
        if film_info.get('average_rating'):
            print(f"Average Rating: {film_info['average_rating']}")
        print(f"{'='*80}")

    # Get reviews
    print(f"\nFetching reviews (page {page}, sorted by {sort})...\n")
    reviews = scraper.get_reviews(film_slug, page=page, sort=sort)

    if not reviews:
        print("No reviews found.")
        sys.exit(0)

    print(f"Found {len(reviews)} reviews:")

    for i, review in enumerate(reviews, 1):
        print_review(review, i)

    print(f"\n{'='*80}")
    print(f"Total reviews displayed: {len(reviews)}")
    print(f"{'='*80}\n")


if __name__ == "__main__":
    main()
