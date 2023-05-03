import os
import requests
import praw
import urllib.request

# Set the minimum number of upvotes and the subreddit you want to fetch images from
min_upvotes = 100
subreddit_name = "aww"

# Initialize the Reddit API client
reddit = praw.Reddit(
    client_id="",
    client_secret="",
    password="",
    user_agent="",
    username="",
)

print(reddit.user.me())

# Enable read-only mode
reddit.read_only = True

# Get the top posts from the subreddit
subreddit = reddit.subreddit(subreddit_name)
top_posts = subreddit.top(limit=None)

# Iterate through top submissions
count = 0
imageFound = False
for submission in top_posts:

    # Get the link of the submission
    url = str(submission.url)

    # Check if the link is an image and has at least the minimum number of upvotes
    if submission.ups >= min_upvotes and (url.endswith("jpg") or url.endswith("jpeg") or url.endswith("png")):

        # Retrieve the image and save it in the /tmp folder
        image_path = f"/tmp/image{count}.jpg"
        urllib.request.urlretrieve(url, image_path)
        imageFound = True
        break

    else:
        count += 1

    # Stop after going through 100 posts and print an error message
    if count >= 100:
        print("No image found in the top 100 posts.")
        break

# Set the downloaded image as wallpaper using feh
if imageFound:
    os.system(f"feh --bg-scale {image_path}")
