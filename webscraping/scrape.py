import requests
import pandas as pd
import time
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('API_KEY')
url = os.getenv('BASE_URL')
query = os.getenv('QUERY')

print(API_KEY, url, query)

all_reviews = []

# Get first page to determine total pages
response = requests.get(
    url,
    params={"query": query, "page": 1},
    headers={"API-Key": API_KEY}
)

data = response.json()

total_pages = 15
print(f"Total pages: {total_pages}")

# Loop through all pages
for page in range(1, total_pages + 1):

    print(f"Scraping page {page}/{total_pages}")

    response = requests.get(
        url,
        params={
            "query": query,
            "page": page
        },
        headers={
            "API-Key": API_KEY
        }
    )

    data = response.json()

    reviews = data["results"]

    for review in reviews:

        # Convert subratings list into a dictionary
        subratings = {
            item["name"]: item["rating"]
            for item in review.get("subratings", [])
        }

        all_reviews.append({
        "review_id": review.get("review_id"),
        "title": review.get("title"),
        "text": review.get("text"),
        "review_tip": review.get("review_tip"),
        "rating": review.get("rating"),

        # Subratings
        "value_rating": subratings.get("value"),
        "rooms_rating": subratings.get("rooms"),
        "location_rating": subratings.get("location"),
        "cleanliness_rating": subratings.get("cleanliness"),
        "service_rating": subratings.get("service"),
        "sleep_quality_rating": subratings.get("sleep_quality"),

        "language": review.get("language"),
        "trip_type": review.get("trip", {}).get("trip_type"),
        "stay_date": review.get("trip", {}).get("stay_date"),

        "reviewer_name": review.get("reviewer", {}).get("name"),
        "reviewer_username": review.get("reviewer", {}).get("username"),
        "contribution_count": review.get("reviewer", {}).get("contribution_count"),

        "published_at_date": review.get("published_at_date"),
        "review_link": review.get("review_link")
    })

    time.sleep(0.5)

# Create dataframe
df = pd.DataFrame(all_reviews)

print(f"\nCollected {len(df)} reviews")

# Save CSV
filename = "Hotel.csv"
df.to_csv(filename, index=False)

print(f"Saved to {filename}")

# Preview
df.head()