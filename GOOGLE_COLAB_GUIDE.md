# Google Colab Setup Guide - Step by Step

Follow these instructions to use the Letterboxd Review Scraper in Google Colab.

## What You'll Need
- A Google account (free)
- A web browser
- 5 minutes

---

## Step-by-Step Instructions

### Step 1: Get the Notebook File

**Option A: Download from GitHub**
1. Go to this repository
2. Click on `letterboxd_colab.ipynb`
3. Click the **Download** button (or right-click "Raw" → Save as)
4. Save it to your computer

**Option B: Copy the raw content**
- You can also just copy all the content from `letterboxd_colab.ipynb` to paste later

---

### Step 2: Open Google Colab

1. Go to **[colab.research.google.com](https://colab.research.google.com/)**
2. Sign in with your Google account if needed

---

### Step 3: Upload the Notebook

1. In Google Colab, click **File** in the top menu
2. Click **Upload notebook**
3. Click the **Choose File** button
4. Select the `letterboxd_colab.ipynb` file you downloaded
5. Wait for it to upload

**Alternative**: If you copied the content, click **File** → **New notebook**, then paste the code.

---

### Step 4: Run the Notebook

You'll see several "cells" (boxes with code). Here's what to do:

#### Cell 1: Install Dependencies
1. Click the **Play button** (▶) on the left of the first cell
2. Wait for it to finish (you'll see "✅ Dependencies installed!")

#### Cell 2: Load Scraper Code
1. Click the **Play button** on the second cell
2. Wait for "✅ Scraper code loaded!"

#### Cell 3: Search for Reviews
1. **CUSTOMIZE YOUR SEARCH HERE**:
   ```python
   FILM_URL = "https://letterboxd.com/film/taxi-1998/"  # Change this!
   PAGE = 1
   SORT = "popular"
   ```

2. Change `FILM_URL` to any Letterboxd film you want:
   - Use full URL: `https://letterboxd.com/film/parasite-2019/`
   - Or just the slug: `parasite-2019`

3. Change `PAGE` if you want page 2, 3, etc.

4. Change `SORT` to:
   - `"popular"` - Most liked reviews
   - `"recent"` - Most recent reviews
   - `"highest-rated"` - Highest rated reviews
   - `"lowest-rated"` - Lowest rated reviews

5. Click the **Play button** to run the search

#### Cell 4: Export to CSV (Optional)
1. After getting results, run this cell to download a CSV file
2. The file will automatically download to your computer

---

### Step 5: Get Results!

You should see output like this:

```
🎬 Fetching film information...

================================================================================
🎥 Film: Taxi
📅 Year: 1998
🎬 Director: Gérard Pirès
⭐ Average Rating: ★★★½
================================================================================

📝 Fetching reviews (page 1, sorted by popular)...

✅ Found 12 reviews:

================================================================================
Review #1
================================================================================
👤 User: JohnDoe
⭐ Rating: ⭐⭐⭐⭐⭐ (5.0/5)
📅 Date: 2 weeks ago
❤️  Likes: 143

This movie is absolutely incredible! The car chases are some of the best...
```

---

## Quick Reference

### Want to search a different film?
- Edit `FILM_URL` in Cell 3
- Run Cell 3 again (no need to rerun Cells 1-2)

### Want more reviews?
- Change `PAGE = 2` (or 3, 4, etc.)
- Run Cell 3 again

### Want different sorting?
- Change `SORT = "recent"` (or other options)
- Run Cell 3 again

### Want to save the data?
- Run Cell 4 (Export to CSV)
- File downloads automatically

---

## Troubleshooting

### "403 Forbidden" Error
- This means Letterboxd is temporarily blocking the request
- **Solution**: Wait 1-2 minutes and try again
- Usually works after a retry or two

### No reviews showing
- Check that the film slug is correct
- Try visiting the URL in your browser first
- Some films might have no reviews

### Cells won't run
- Click **Runtime** → **Restart runtime**
- Then run cells again from the top

### Want to start over?
- Click **Runtime** → **Restart runtime**
- Run all cells again

---

## Example Films to Try

```python
FILM_URL = "https://letterboxd.com/film/parasite-2019/"
FILM_URL = "https://letterboxd.com/film/the-shawshank-redemption/"
FILM_URL = "https://letterboxd.com/film/pulp-fiction/"
FILM_URL = "https://letterboxd.com/film/spirited-away/"
FILM_URL = "https://letterboxd.com/film/dune-part-two/"
FILM_URL = "https://letterboxd.com/film/oppenheimer-2023/"
```

Just copy one of these into the `FILM_URL` field!

---

## Tips

- ⚡ **Run all at once**: Click **Runtime** → **Run all** to run everything
- 💾 **Save your notebook**: Click **File** → **Save** to keep your customizations
- 📁 **Rename it**: Click **File** → **Rename** to give it a custom name
- 🔗 **Share it**: Click **Share** button to share with others

---

## Need Help?

If you run into issues:
1. Try restarting the runtime (**Runtime** → **Restart runtime**)
2. Check that you're copying the film URL correctly from Letterboxd
3. Wait a minute or two if you get blocked (403 errors)
4. Make sure you ran Cells 1 and 2 before Cell 3

Enjoy exploring Letterboxd reviews! 🎬✨
