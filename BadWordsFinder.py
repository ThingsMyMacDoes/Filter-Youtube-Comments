import streamlit as st
import json
import re
from collections import Counter

# Function to load JSON data from a file
def load_json(file):
    data = json.load(file)
    return data

# Function to load keywords from a text file
def load_keywords(file):
    keywords = file.read().decode('utf-8').splitlines()
    return [keyword.strip() for keyword in keywords if keyword.strip()]

# Function to highlight keywords in text and count occurrences
def highlight_keywords(text, keywords, keyword_counts):
    for keyword in keywords:
        pattern = re.compile(r'\b' + re.escape(keyword) + r'\b', re.IGNORECASE)
        matches = pattern.findall(text)
        keyword_counts[keyword] += len(matches)
        text = pattern.sub(f'<mark><span style="color:red; background-color:yellow;">{keyword}</mark>', text)
    return text

# Function to display a single comment or reply with highlighted text
def display_comment(item, keywords, keyword_counts):
    text_display = highlight_keywords(item['snippet']['textDisplay'], keywords, keyword_counts)
    comment_html = f"""
    <div>
        <p><strong>Text Display:</strong> {text_display}</p>
        <p><strong>Total Reply Count:</strong> {item.get('totalReplyCount', 'N/A')}</p>
        <p><strong>Parent ID:</strong> {item.get('parentId', 'N/A')}</p>
        <p><strong>Author Channel URL:</strong> <a href="{item['snippet']['authorChannelUrl']}" target="_blank">{item['snippet']['authorChannelUrl']}</a></p>
        <p><strong>Date:</strong> {item['snippet']['publishedAt']}</p>
        <p><strong>Updated At:</strong> {item['snippet']['updatedAt']}</p>
        <p><strong>Likes:</strong> {item['snippet']['likeCount']}</p>
        <hr>
    </div>
    """
    return comment_html

# Main function to visualize comments and replies
def main():
    st.title("Comments Analysis")

    # Sidebar for inputs
    st.sidebar.header("Options")
    json_file = st.sidebar.file_uploader("Upload the Comments File", type=["json"])
    text_file = st.sidebar.file_uploader("Upload the Bad Words File", type=["txt"])

    if st.sidebar.button("Load and Display Comments"):
        if json_file is not None and text_file is not None:
            try:
                # Load JSON data
                data = load_json(json_file)
                video_details = data['videoDetails']
                comments_data = data['comments']

                # Extract video title
                video_title = re.sub(r'\W+', '_', video_details['title'])

                # Display video details
                st.markdown("## Video Details")
                st.write(f"**Title:** {video_details['title']}")
                st.write(f"**URL:** {video_details['url']}")
                st.write(f"**Published At:** {video_details['publishedAt']}")

                # Load keywords from text file
                keywords = load_keywords(text_file)

                # Initialize keyword counts
                keyword_counts = Counter()

                # Group and Sort Data
                comments = {}
                for item in comments_data:
                    if item['commentType'] == 'Top-Level Comment':
                        comments[item['id']] = {
                            'comment': item,
                            'replies': []
                        }
                    elif item['commentType'] == 'Reply':
                        parent_id = item['parentId']
                        if parent_id in comments:
                            comments[parent_id]['replies'].append(item)

                # Prepare HTML content
                html_content = f"""
                <html>
                <head>
                    <title>Comments Analysis</title>
                    <style>
                        body {{ font-family: Arial, sans-serif; }}
                        .comment {{ margin-bottom: 20px; }}
                        .reply {{ margin-left: 20px; margin-bottom: 20px; }}
                        mark {{ color: red; background-color: yellow; }}
                    </style>
                </head>
                <body>
                    <h1>Comments Analysis</h1>
                    <h2>Video Details</h2>
                    <p><strong>Title:</strong> {video_details['title']}</p>
                    <p><strong>URL:</strong> <a href="{video_details['url']}" target="_blank">{video_details['url']}</a></p>
                    <p><strong>Published At:</strong> {video_details['publishedAt']}</p>
                    <hr>
                """

                # Display comments and replies based on keyword filter
                author_urls = []
                for comment_id, comment_data in comments.items():
                    comment = comment_data['comment']
                    text_display = comment['snippet']['textDisplay'].lower().split()

                    # Check if any keyword is in the text display of the comment as an exact match
                    if any(keyword.lower() in text_display for keyword in keywords):
                        st.markdown(f"### Top-Level Comment by {comment['snippet']['authorDisplayName']}")
                        comment_html = display_comment(comment, keywords, keyword_counts)
                        st.markdown(comment_html, unsafe_allow_html=True)
                        html_content += f'<div class="comment"><h3>Top-Level Comment by {comment["snippet"]["authorDisplayName"]}</h3>{comment_html}</div>'
                        author_urls.append(comment['snippet']['authorChannelUrl'])
                    else:
                        for reply in comment_data['replies']:
                            reply_text_display = reply['snippet']['textDisplay'].lower().split()
                            if any(keyword.lower() in reply_text_display for keyword in keywords):
                                st.markdown(f"#### Reply by {reply['snippet']['authorDisplayName']}")
                                reply_html = display_comment(reply, keywords, keyword_counts)
                                st.markdown(reply_html, unsafe_allow_html=True)
                                html_content += f'<div class="reply"><h4>Reply by {reply["snippet"]["authorDisplayName"]}</h4>{reply_html}</div>'
                                author_urls.append(reply['snippet']['authorChannelUrl'])

                # Display keyword counts
                st.sidebar.markdown("## Keyword Counts")
                keyword_counts_html = "<h2>Keyword Counts</h2><ul>"
                for keyword, count in keyword_counts.items():
                    st.sidebar.write(f"**{keyword}:** {count}")
                    keyword_counts_html += f"<li><strong>{keyword}:</strong> {count}</li>"
                keyword_counts_html += "</ul>"
                html_content += keyword_counts_html

                html_content += """
                </body>
                </html>
                """

                # Provide download button for HTML content
                st.sidebar.download_button(
                    label="Download Analysis",
                    data=html_content,
                    file_name=f"{video_title}_analysis.html",
                    mime="text/html"
                )

                # Prepare HTML content for author channel URLs
                urls_content = f"""
                <html>
                <head>
                    <title>Author Channel URLs</title>
                    <script>
                        function copyToClipboard(url) {{
                            navigator.clipboard.writeText(url);
                        }}
                    </script>
                </head>
                <body>
                    <h1>Author Channel URLs</h1>
                    <ul>
                """
                for url in author_urls:
                    urls_content += f'<li><a href="#" onclick="copyToClipboard(\'{url}\'); return false;">{url}</a></li>'
                urls_content += """
                    </ul>
                </body>
                </html>
                """

                # Provide download button for author channel URLs
                st.sidebar.download_button(
                    label="Download The Bandits",
                    data=urls_content,
                    file_name=f"{video_title}_Bandits.html",
                    mime="text/html"
                )

            except Exception as e:
                st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
