# Instagram Web Gallery Integration with AWS Amplify

## Overview
This project integrates an Instagram account with a website hosted on AWS Amplify. The website will display posts with the hashtag `#webgallery` from the Instagram account. The solution involves fetching Instagram data using the Instagram Graph API and automating updates through AWS Lambda or Webhooks.

---

## Features
- Displays Instagram posts tagged with `#webgallery` on the website.
- Automated updates of the gallery based on Instagram posts.
- Built on AWS services, including Amplify, Lambda, and DynamoDB.

---

## Requirements

### For Instagram Setup:
1. **Instagram Professional Account**
   - Either Business or Creator account.
   - Linked to a Facebook Page.
2. **Facebook Developer App**
   - Permissions: `instagram_basic`, `user_media`, `pages_read_engagement`.
   - Long-lived Access Token for API authentication.

### For AWS Setup:
1. **AWS Amplify**
   - To host the website.
2. **AWS Lambda**
   - To automate the process of fetching Instagram posts.
3. **DynamoDB**
   - To store Instagram post metadata (e.g., captions, media URLs).
4. **AWS API Gateway (Optional)**
   - If implementing Webhooks.

---

## Architecture
1. **Frontend**: React app hosted on AWS Amplify.
2. **Backend**: AWS Lambda functions for:
   - Fetching Instagram posts periodically.
   - Filtering posts with the hashtag `#webgallery`.
   - Storing data in DynamoDB.
3. **Database**: DynamoDB table to store post metadata.
4. **Instagram API**: Fetch Instagram posts using the Graph API.
5. **Optional Webhooks**: For real-time updates from Instagram.

---

## Process Workflow

### 1. Instagram Setup
- **Step 1**: Create a Facebook Page and link it to the Instagram account.
- **Step 2**: Register a Facebook Developer App.
  - Add the "Instagram Graph API" product.
  - Generate App ID and App Secret.
- **Step 3**: Get API Permissions.
  - Request `instagram_basic`, `user_media`, and `pages_read_engagement`.
  - Generate a long-lived access token using the following API call:
    ```bash
    GET https://graph.facebook.com/v16.0/oauth/access_token?
    grant_type=fb_exchange_token&
    client_id={app-id}&
    client_secret={app-secret}&
    fb_exchange_token={short-lived-token}
    ```

### 2. AWS Amplify Setup
- **Step 1**: Create an Amplify app and connect it to your GitHub repository (React app).
- **Step 2**: Deploy the app and ensure it can display a gallery.
- **Step 3**: Fetch DynamoDB data to dynamically populate the gallery.

### 3. Backend Development
- **Option 1: Lambda Polling**
  1. Write a Lambda function to fetch posts using the Instagram Graph API.
  2. Filter posts for `#webgallery` in captions.
  3. Store filtered post metadata (e.g., media URL, caption) in DynamoDB.
  4. Use EventBridge to schedule periodic execution (e.g., every hour).

### 4. Frontend Integration
- Fetch the gallery data from DynamoDB and display it on the website.
- Implement a simple refresh mechanism or periodic updates.

---

## Example Lambda Function
Here’s an example of a Lambda function to fetch Instagram posts:

```python
import requests
import boto3

def handler(event, context):
    ACCESS_TOKEN = "YOUR_LONG_LIVED_ACCESS_TOKEN"
    API_URL = f"https://graph.instagram.com/me/media?fields=id,caption,media_url,timestamp&access_token={ACCESS_TOKEN}"
    
    response = requests.get(API_URL).json()
    posts = response.get('data', [])
    
    gallery_posts = [post for post in posts if '#webgallery' in post.get('caption', '')]

    # Save to DynamoDB
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('InstagramPosts')
    for post in gallery_posts:
        table.put_item(Item=post)
    
    return {"statusCode": 200, "body": "Fetched and stored posts"}

```

## AWS Amplify Next.js (App Router) Starter Template

This repository provides a starter template for creating applications using Next.js (App Router) and AWS Amplify, emphasizing easy setup for authentication, API, and database capabilities.

## Overview

This template equips you with a foundational Next.js application integrated with AWS Amplify, streamlined for scalability and performance. It is ideal for developers looking to jumpstart their project with pre-configured AWS services like Cognito, AppSync, and DynamoDB.

## Features

- **Authentication**: Setup with Amazon Cognito for secure user authentication.
- **API**: Ready-to-use GraphQL endpoint with AWS AppSync.
- **Database**: Real-time database powered by Amazon DynamoDB.

## Deploying to AWS

For detailed instructions on deploying your application, refer to the [deployment section](https://docs.amplify.aws/nextjs/start/quickstart/nextjs-app-router-client-components/#deploy-a-fullstack-app-to-aws) of our documentation.

## Security

See [CONTRIBUTING](CONTRIBUTING.md#security-issue-notifications) for more information.

## License

This library is licensed under the MIT-0 License. See the LICENSE file.

## AWS Configuration

This project uses AWS Amplify. To configure your AWS credentials:

## Architecture
### **S3 Folder Structure**
To prepare for future scalability and security, the S3 bucket is structured as follows:
- **Public** (used for now):
  - `public/data/`: JSON files with public metadata.
  - `public/images/`: Public images for the gallery.
- **Protected** (future use): Requires authentication for access.
  - `protected/data/`
  - `protected/images/`
- **Private** (future use): Specific to individual users.
  - `private/<user-id>/data/`
  - `private/<user-id>/images/`

---

## Data Storage Conventions
### **File Naming**
- Each JSON file maps to its associated image using the `image` key in the JSON metadata.
- Example `JSON`:
  ```json
  {
    "id": "post123",
    "title": "Stylish Lamp",
    "price": "49.99",
    "image": "post123.jpg"
  }
Example Files in S3:
public/data/post123.json
public/images/post123.jpg
Reasoning
Using the image key in the JSON ensures flexibility for file naming and future reorganizations.

Amplify Setup
This project assumes Amplify CLI v10.x or higher. Check Amplify documentation for newer versions as APIs might change.

1. Install Amplify
Ensure Amplify is installed and configured:

bash
Copy code
npm install -g @aws-amplify/cli
amplify configure
2. Add Hosting
bash
Copy code
amplify add hosting
amplify push
3. Add Storage
bash
Copy code
amplify add storage
Select "Content (Images, audio, video, etc.)".
Set access level for "guest" (public access).
Frontend Integration
The Amplify Storage module is used to fetch JSON and images from S3.

Example: Fetch JSON and Render Gallery
javascript
Copy code
import { Storage } from 'aws-amplify';
import { useEffect, useState } from 'react';

function Gallery() {
  const [gallery, setGallery] = useState([]);

  useEffect(() => {
    async function fetchGallery() {
      // Fetch the gallery JSON file
      const jsonUrl = await Storage.get('public/data/gallery.json', { level: 'public' });
      const response = await fetch(jsonUrl);
      const posts = await response.json();
      setGallery(posts);
    }
    fetchGallery();
  }, []);

  return (
    <div className="gallery">
      {gallery.map(post => (
        <div key={post.id} className="post">
          <img
            src={`https://your-bucket.s3.amazonaws.com/public/images/${post.image}`}
            alt={post.title}
          />
          <h3>{post.title}</h3>
          <p>Price: ${post.price}</p>
        </div>
      ))}
    </div>
  );
}

export default Gallery;
Notes
Replace your-bucket.s3.amazonaws.com with your actual S3 bucket endpoint.
For newer Amplify versions, confirm compatibility of Storage.get.
Future Considerations
Protected and Private Data:

Use Amplify’s protected and private access levels to secure user-specific content in the future.
Frontend will need authentication via Amplify Auth module.
Lambda for Dynamic Needs:

If dynamic querying or private data handling is required later, consider adding AWS Lambda with a REST API.
Caching:

Use Amazon CloudFront for faster global delivery if traffic scales.
Summary
For now, the project uses a public-only S3 structure with data/ and images/ folders. Amplify’s Storage module handles fetching files directly. This lightweight setup ensures cost-efficiency and simplicity while allowing for future scalability.


## BACKEND
### Installation
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

### How to run Lambdas:
serverless invoke local --function updateGallery --aws-profile amplify-user-1