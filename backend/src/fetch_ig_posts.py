import json
import boto3
import requests
import urllib.request
from datetime import datetime, timedelta
import pytz
from openai import OpenAI
import os

s3 = boto3.client('s3')
print("os.environ['OPENAI_API_KEY']: ", os.environ['OPENAI_API_KEY'])
client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])
BUCKET_NAME = os.environ['BUCKET_NAME']

SYSTEM_PROMPT = """
#TASK
your job is to take the caption content of an instagram post that contains an image of jewelry, and to create a suiting title and extract the price based ont that content. If there is no specific price mentioned, then make it None for the price prop. the title and optionally the price will be later displayed under the image of the instagram post and be shown in a gallery view

The content might be in either english or Korean.

User input format in json:
{
  "ig_post_caption": "contains post content"
}

Your output format in json:
{
  "title": "the title based on the content",
  "description": "describes the jewelry object of the image based on the description of the post."
  "price": null/or float
}
"""



def get_gpt_response(user_input, model="gpt-3.5-turbo"):
	# print('system_prompt:\n', system_prompt)
	completion = client.chat.completions.create(
		model=model,
		messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": json.dumps(user_input, indent=4, ensure_ascii=False)}
		],
		response_format={ "type": "json_object" }
	)
	# print("chat completion:\n", completion)
	content_str = completion.choices[0].message.content
	response_json = json.loads(content_str)
	return response_json

def get_unique_image_file_name(image_title, gallery_entries):
  
  similar_image_title_counter = 0
  for gallery_entry in gallery_entries:
    entry_image_title = gallery_entry.get('image', '').split('.')[0]
    if image_title in entry_image_title:
      similar_image_title_counter += 1

  if similar_image_title_counter > 0:
    image_title = f"image_title_{similar_image_title_counter+1}"

  return f"{image_title}.jpg"

def get_current_gallery_entry_from_s3():
    """Fetch current gallery.json from S3"""
    try:
        response = s3.get_object(
            Bucket=BUCKET_NAME,
            Key="public/data/gallery.json"
        )
        return json.loads(response['Body'].read().decode('utf-8'))
    except s3.exceptions.NoSuchKey:
        print("No existing gallery.json found, starting fresh")
        return []
    except Exception as e:
        print(f"Error reading from S3: {e}")
        return []

def save_image_to_s3(image_url, image_key):
    """Download image from Instagram and upload to S3"""
    try:
        # Download image from Instagram
        with urllib.request.urlopen(image_url) as response:
            image_data = response.read()
        
        # Upload to S3
        s3.put_object(
            Bucket=BUCKET_NAME,
            Key=f"public/images/{image_key}",
            Body=image_data,
            ContentType='image/jpeg'
        )
        return True
    except Exception as e:
        print(f"Error saving image to S3: {e}")
        return False

def save_gallery_to_s3(gallery_entries):
    """Save updated gallery.json to S3"""
    try:
        s3.put_object(
            Bucket=BUCKET_NAME,
            Key="public/data/gallery.json",
            Body=json.dumps(gallery_entries, indent=2),
            ContentType='application/json'
        )
        print("Successfully saved gallery.json to S3")
    except Exception as e:
        print(f"Error saving gallery to S3: {e}")

def create_gallery_entry_from_post(
    post_id,
    caption,
    media_url,
    timestamp,
    gallery_entries
):
    user_input = {
        "ig_post_caption": caption
    }
    gpt_response = get_gpt_response(user_input)
    print("gpt_response:", gpt_response)
    
    image_file_name = get_unique_image_file_name(gpt_response['title'], gallery_entries)
    new_gallery_entry = {
        "id": post_id,
        "title": gpt_response['title'],
        "price": gpt_response['price'],
        "ig_media_url": media_url,
        "image": image_file_name
    }
    
    # Save image to S3
    if save_image_to_s3(media_url, image_file_name):
        gallery_entries.append(new_gallery_entry)
    else:
        print(f"Skipping gallery entry due to image save failure: {post_id}")

def fetch_instagram_posts():
    """
    Fetch Instagram posts using the Graph API and filter for last 24 hours.
    """
    url = f"https://graph.instagram.com/me/media?fields=id,caption,media_url,timestamp,media_type&access_token={os.environ['INSTAGRAM_ACCESS_TOKEN']}"
    response = requests.get(url)
    
    if response.status_code == 200:
        posts = response.json().get('data', [])
        
        # Get posts from last 24 hours
        one_day_ago = datetime.now(pytz.UTC) - timedelta(days=1)
        
        print('first post: \n', posts[0])
        # Filter posts by timestamp
        recent_posts = [
            post for post in posts
            if datetime.strptime(post['timestamp'], '%Y-%m-%dT%H:%M:%S%z') > one_day_ago
        ]
        
        print(f"Found {len(recent_posts)} posts from last 24 hours")
        return recent_posts
    else:
        print(f"Error fetching Instagram posts: {response.text}")
        return []

def process_post(post, gallery_entries):
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
      create_gallery_entry_from_post(
        post_id,
        caption,
        media_url,
        timestamp, 
        gallery_entries
      )

def main():
  """
  Main function to fetch and process Instagram posts with #einlabgallery.
  """
  gallery_entries = get_current_gallery_entry_from_s3()

  posts = fetch_instagram_posts()
  for post in posts:
      process_post(post, gallery_entries)

  # Save updated gallery entries to S3
  save_gallery_to_s3(gallery_entries)

def handler(event, context):
    try:
        main()
        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "Successfully processed Instagram posts"
            })
        }
    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            "statusCode": 500,
            "body": json.dumps({
                "error": str(e)
            })
        }