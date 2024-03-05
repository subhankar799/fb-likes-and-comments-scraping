import requests
import pandas as pd
import json

def get_comments(page_id, post_id, access_token):

    #URL for comments retrieval

    # your access token, from https://developers.facebook.com/tools/explorer/
    url = f'https://graph.facebook.com/{page_id}_{post_id}/comments?access_token={access_token}'

    # Send GET request to Facebook Graph API
    response = requests.get(url)

    # Check for successful response
    if response.status_code == 200:
        # Parse response JSON
        data = response.json()

        # Extract comments data
        comments_data = data.get('data', [])

        # Handle pagination if necessary
        while 'paging' in data and 'next' in data['paging']:
            next_page_url = data['paging']['next']
            response = requests.get(next_page_url)
            if response.status_code == 200:
                data = response.json()
                comments_data.extend(data.get('data', []))
            else:
                print("Error retrieving next page of comments.")
                break

        return comments_data
    else:
        print("Error retrieving comments:", response.status_code)
        return []

def get_likes(page_id, post_id, access_token):
    #URL for likes retrieval
    url = f'https://graph.facebook.com/{page_id}_{post_id}/likes?access_token={access_token}'

    # Send GET request to Facebook Graph API
    response = requests.get(url)

    # Check for successful response
    if response.status_code == 200:
        # Parse response JSON
        data = response.json()

        # Extract likes data
        likes_data = data.get('data', [])

        # Handle pagination if necessary
        while 'paging' in data and 'next' in data['paging']:
            next_page_url = data['paging']['next']
            response = requests.get(next_page_url)
            if response.status_code == 200:
                data = response.json()
                likes_data.extend(data.get('data', []))
            else:
                print("Error retrieving next page of likes.")
                break

        return likes_data
    else:
        print("Error retrieving likes:", response.status_code)
        return []

def save_to_excel(data, output_file):
    # Create DataFrame from data
    df = pd.DataFrame(data)

    # Save DataFrame to Excel file
    df.to_excel(output_file, index=False)

if __name__ == "__main__":
    page_id = input("Enter your page ID: ")
    post_id = input("Enter your post ID: ")
    access_token = input("Enter your access token: ")

    # Retrieve comments and likes from Facebook API
    comments = get_comments(page_id, post_id, access_token)
    likes = get_likes(page_id, post_id, access_token)

    if comments:
        save_to_excel(comments, 'comments.xlsx')
        print("Comments saved to 'comments.xlsx'")
    else:
        print("No comments found.")

    if likes:
        save_to_excel(likes, 'likes.xlsx')
        print("Likes saved to 'likes.xlsx'")
    else:
        print("No likes found.")
