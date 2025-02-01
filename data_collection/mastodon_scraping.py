from mastodon import Mastodon
import requests
import json
import csv
from datetime import datetime, timezone
import re
m = Mastodon(access_token="6BPeXcM63JRbiLJAEIPKtLi7F9rYUIKwLsdPKLYE08g", api_base_url="https://mastodon.social")

def remove_links(content):
    return re.sub(r'<a[^>]*>.*?</a>', '', content)


def remove_paragraph_tags(content):
    return re.sub(r'<p>|</p>', '', content)
def get_hashtag_posts(hashtags, start_date, end_date):
    all_posts = set()  # Use a set to avoid duplicates

    for tag in hashtags:
        print(f"Fetching posts for hashtag: {tag}")
        api_url = f'https://mastodon.social/api/v1/timelines/tag/{tag}'
        count = 0

        fetch_complete = False
        max_id = None
        while not fetch_complete:
            params = {'limit': 40}
            if max_id:
                params['max_id'] = max_id

            response = requests.get(api_url, params=params)
            data = json.loads(response.text)

            if not data:
                break

            for post in data:
                created_utc = datetime.fromisoformat(post['created_at'].replace('Z', '+00:00'))
                formatted_date = created_utc.strftime('%m-%d-%Y')
                content = post['content']
                formatted_content = remove_links(content)
                formatted_content = remove_paragraph_tags(formatted_content)
                if len(formatted_content) < 40:
                    continue
                if start_date <= created_utc <= end_date:
                    post_tuple = (formatted_date, formatted_content)
                    if post_tuple not in all_posts:
                        all_posts.add(post_tuple)
                        count += 1

                elif created_utc < start_date:
                    fetch_complete = True
                    break

            if not fetch_complete and data:
                max_id = data[-1]['id']

    return [{'created_utc': p[0], 'content_matsodon': p[1]} for p in all_posts]


def save_to_csv(posts, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['created_utc', 'content_matsodon']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for post in posts:
            writer.writerow(post)


# Set up the date range
start_date = datetime(2022, 1, 1, tzinfo=timezone.utc)
end_date = datetime(2022, 1, 2, tzinfo=timezone.utc)

hashtags_to_search = ['tesla']

posts = get_hashtag_posts(hashtags_to_search, start_date, end_date)
save_to_csv(posts, "mastodon_tesla_posts_1st_half_year2022.csv")

print(
    f"Tesla-related posts from {start_date.date()} to {end_date.date()} saved to mastodon_tesla_posts_oct23_nov22.csv!")
print(f"Total unique posts: {len(posts)}")