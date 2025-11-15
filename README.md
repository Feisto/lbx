# Letterboxd Review Scraper

A Python tool to search and fetch reviews from Letterboxd film pages.

## Features

- Fetch reviews for any film on Letterboxd
- Sort reviews by: popular, recent, highest-rated, or lowest-rated
- Pagination support to browse through multiple pages of reviews
- Display film information (title, year, director, average rating)
- Show review details including username, rating, text, likes, and date

## 🚀 Quick Start with Google Colab (Recommended)

The easiest way to use this tool is with Google Colab - no installation needed!

### Option 1: Use the Colab Notebook (Easiest)

1. **Open the notebook**: Click this link → [Open in Google Colab](https://colab.research.google.com/)
2. **Upload the notebook**:
   - Download `letterboxd_colab.ipynb` from this repository
   - In Colab, click **File** → **Upload notebook** → Select the file
3. **Run it**:
   - Click **Runtime** → **Run all**
   - Or run cells one by one with the play button
4. **Customize your search**:
   - In Step 3, change `FILM_URL` to any film you want
   - Change `PAGE` or `SORT` as needed
   - Run the cell again

### Option 2: Quick Colab Setup (Copy & Paste)

1. Go to [Google Colab](https://colab.research.google.com/)
2. Create a new notebook
3. Copy and paste the code from `letterboxd_colab.ipynb`
4. Run all cells

### Why Google Colab?
- ✅ No installation required
- ✅ Runs in your browser
- ✅ Less likely to be blocked by Letterboxd
- ✅ Free to use
- ✅ Can export results to CSV

---

## 💻 Local Installation

1. Clone this repository
2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

```bash
python letterboxd_reviews.py <film_url_or_slug>
```

### Examples

Using a full Letterboxd URL:
```bash
python letterboxd_reviews.py https://letterboxd.com/film/taxi-1998/
```

Using just the film slug:
```bash
python letterboxd_reviews.py taxi-1998
```

### Advanced Options

**Pagination** - View different pages of reviews:
```bash
python letterboxd_reviews.py taxi-1998 --page 2
```

**Sorting** - Sort reviews by different criteria:
```bash
python letterboxd_reviews.py taxi-1998 --sort recent
python letterboxd_reviews.py taxi-1998 --sort highest-rated
python letterboxd_reviews.py taxi-1998 --sort lowest-rated
```

**Combine options:**
```bash
python letterboxd_reviews.py taxi-1998 --page 3 --sort recent
```

### Sort Options

- `popular` (default) - Most liked/popular reviews
- `recent` - Most recent reviews
- `highest-rated` - Reviews with highest ratings
- `lowest-rated` - Reviews with lowest ratings

## Output Format

The tool displays:
- Film information (title, year, director, average rating)
- Review count for the current page
- For each review:
  - Username
  - Star rating (★★★★★)
  - Date posted
  - Number of likes
  - Full review text

## Requirements

- Python 3.7+
- requests
- beautifulsoup4
- lxml

## Use as a Library

You can also import and use the scraper in your own Python code:

```python
from letterboxd_reviews import LetterboxdReviewScraper

scraper = LetterboxdReviewScraper()

# Get film info
film_info = scraper.get_film_info('taxi-1998')
print(film_info)

# Get reviews
reviews = scraper.get_reviews('taxi-1998', page=1, sort='popular')
for review in reviews:
    print(review['username'], review['rating'], review['text'])
```

## Notes

- This tool scrapes public Letterboxd pages and respects their structure
- Review availability depends on what's publicly visible on Letterboxd
- Large review counts may require pagination through multiple pages

## Known Limitations

Letterboxd implements anti-scraping measures that may block automated requests with a 403 Forbidden error. This is a protective measure by the website.

### Workarounds

If you encounter 403 errors, try:

1. **Run from a different network** - Residential IPs are less likely to be blocked than server/datacenter IPs
2. **Add delays between requests** - The script already includes small delays
3. **Use a browser automation tool** - Tools like Selenium or Playwright that control a real browser are harder to detect
4. **Use rotating proxies** - Can help avoid IP-based blocking
5. **Access through a browser first** - Sometimes visiting the site in a browser helps establish cookies

### Alternative: Browser-Based Approach

For environments where the script is blocked, consider using a browser automation approach:

```python
# Example using Playwright (install with: pip install playwright)
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto('https://letterboxd.com/film/taxi-1998/reviews/')
    content = page.content()
    # Parse with BeautifulSoup...
```

### Ethical Scraping

This tool is designed for:
- Personal use and research
- Respecting Letterboxd's server resources with rate limiting
- Reading only public data

Please use responsibly and consider:
- Supporting Letterboxd through their official channels
- Checking if Letterboxd offers an official API for your use case
- Respecting their terms of service

## Troubleshooting

**403 Forbidden Error**: Website is blocking automated requests. Try the workarounds above.

**Empty Results**: The film slug might be incorrect, or the page structure may have changed.

**Timeout Errors**: Increase timeout values or check your internet connection.

## License

MIT
