import requests
import json

# Configuration
ACCESS_TOKEN = "IGQWRQUGRIejV5T1dzWTNHQ1pQajRnYkdtY1VfSUh6WUhqN0phLTRnaThfbEozRkNYczZAsS2FLVlU4UDU1V25RSHVxWjRUUWlfbkxocDdHY211X0ExX2Y1M1NZAV0QzZAlZAvRFFjSmRKTmdnZAHpBU284VUE1MklBRjQZD"

def fetch_instagram_posts():
    """
    Fetch Instagram posts using the Graph API.
    """
    url = f"https://graph.instagram.com/me/media?fields=id,caption,media_url,timestamp,media_type&access_token={ACCESS_TOKEN}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get('data', [])
    else:
        print(f"Error fetching Instagram posts: {response.text}")
        return []

def process_post(post):
    """
    Process a single Instagram post and print its details.
    """
    post_id = post['id']
    caption = post.get('caption', "")
    media_url = post['media_url']
    timestamp = post['timestamp']

    # Filter posts with #webgallery
    if "#einlabgallery" in caption:
        print("------ Post Details ------")
        print(f"ID: {post_id}")
        print(f"Caption: {caption}")
        print(f"Media URL: {media_url}")
        print(f"Timestamp: {timestamp}")
        print("--------------------------")

def main():
    """
    Main function to fetch and print Instagram posts with #webgallery.
    """
    posts = fetch_instagram_posts()
    for post in posts:
        process_post(post)

if __name__ == "__main__":
    main()
