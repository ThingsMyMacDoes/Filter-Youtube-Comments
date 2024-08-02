
import re
import json
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Your API key
api_key = 'AIzaSyAoY3vMsz5jiN4Hh7_Azs3uArRIocJrUqw'

# Build the YouTube service
youtube = build('youtube', 'v3', developerKey=api_key)

# Function to extract video ID from URL
def extract_video_id(url):
    video_id_match = re.search(r'(?<=v=)[^&#]+', url)
    if video_id_match:
        return video_id_match.group(0)
    video_id_match = re.search(r'(?<=be/)[^&#]+', url)
    if video_id_match:
        return video_id_match.group(0)
    video_id_match = re.search(r'(?<=embed/)[^&#]+', url)
    if video_id_match:
        return video_id_match.group(0)
    return None

# Function to get video details
def get_video_details(video_id):
    try:
        response = youtube.videos().list(
            part='snippet',
            id=video_id
        ).execute()
        if 'items' in response and response['items']:
            video = response['items'][0]['snippet']
            return {
                'title': video['title'],
                'url': f"https://www.youtube.com/watch?v={video_id}",
                'publishedAt': video['publishedAt']
            }
        else:
            return None
    except HttpError as e:
        print(f"An HTTP error occurred: {e}")
        return None

# Function to get all comments and replies on a given video using comments.list
def get_total_comments_and_replies(video_id):
    total_comments = 0
    comments = []
    try:
        # First, get all top-level comments
        response = youtube.commentThreads().list(
            videoId=video_id,
            part='snippet',
            maxResults=100,
            order='time'
        ).execute()

        while 'items' in response:
            for item in response['items']:
                top_comment_id = item['id']
                top_comment = item['snippet']['topLevelComment']['snippet']
                top_comment_data = {
                    'id': item['id'],
                    'videoId': video_id,
                    'snippet': item['snippet']['topLevelComment']['snippet'],
                    'totalReplyCount': item['snippet']['totalReplyCount'],
                    'commentType': 'Top-Level Comment'
                }
                comments.append(top_comment_data)
                total_comments += 1  # Counting the top-level comment

                # Get replies for each top-level comment
                replies_response = youtube.comments().list(
                    parentId=top_comment_id,
                    part='snippet',
                    maxResults=100
                ).execute()

                while 'items' in replies_response:
                    for reply in replies_response['items']:
                        reply_data = {
                            'id': reply['id'],
                            'parentId': top_comment_id,
                            'snippet': reply['snippet'],
                            'commentType': 'Reply'
                        }
                        comments.append(reply_data)
                    total_comments += len(replies_response['items'])  # Counting the replies

                    if 'nextPageToken' in replies_response:
                        replies_response = youtube.comments().list(
                            parentId=top_comment_id,
                            part='snippet',
                            maxResults=100,
                            pageToken=replies_response['nextPageToken']
                        ).execute()
                    else:
                        break

            print(f"Fetched {total_comments} comments so far...")

            if 'nextPageToken' in response:
                response = youtube.commentThreads().list(
                    videoId=video_id,
                    part='snippet',
                    maxResults=100,
                    order='time',
                    pageToken=response['nextPageToken']
                ).execute()
            else:
                break
    except HttpError as e:
        print(f"An HTTP error occurred: {e}")
    return total_comments, comments

# Main function
def main():
    video_url = input("Enter the YouTube video URL: ")
    video_id = extract_video_id(video_url)
    if not video_id:
        print("Invalid YouTube video URL.")
        return

    video_details = get_video_details(video_id)
    if not video_details:
        print("Could not retrieve video details.")
        return

    total_comments, comments = get_total_comments_and_replies(video_id)
    print(f"The total number of comments, including replies, is: {total_comments}")

    output = {
        'videoDetails': video_details,
        'comments': comments
    }

    comments_file = f"all_comments_on_{video_id}.json"
    with open(comments_file, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=4, ensure_ascii=False)
    print(f"All comments and replies have been saved to {comments_file}")

if __name__ == "__main__":
    main()
