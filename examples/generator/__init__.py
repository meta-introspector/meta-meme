#Got it! It looks like you're using a GraphQL query to retrieve the discussion information fro#m a specific repository. Here's how you can integrate the GraphQL query with the Python script using the `requests` library to make the API request:

#```python
import requests

# Define the GraphQL query
query = """
query {
  repository(owner: "meta-introspector", name: "meta-meme") {
    discussion(number: 21) {
      title
      body
      comments(first: 10) {
        nodes {
          author {
            login
          }
          body
        }
      }
    }
  }
}
"""

# API endpoint
url = "https://api.github.com/graphql"

# Your GitHub personal access token
headers = {
    "Authorization": "Bearer YOUR_PERSONAL_ACCESS_TOKEN"
}

# Make the API request
response = requests.post(url, json={"query": query}, headers=headers)
data = response.json()

# Extract and display the information
discussion_data = data["data"]["repository"]["discussion"]
discussion_title = discussion_data["title"]
print("Discussion Title:", discussion_title)

comments = discussion_data["comments"]["nodes"]
for comment in comments:
    author = comment["author"]["login"]
    body = comment["body"]
    print("Author:", author)
    print("Comment:", body)
    print("-" * 20)

# Replace `YOUR_PERSONAL_ACCESS_TOKEN` with your actual GitHub personal access token. Make sure you have the `requests` library installed (`pip install requests`) before running the script. This script will send the GraphQL query to the GitHub API, retrieve the discussion data, and display the discussion title along with the author and comment body for each comment.
