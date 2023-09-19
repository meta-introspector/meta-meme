#Got it! It looks like you're using a GraphQL query to retrieve the discussion information fro#m a specific repository. Here's how you can integrate the GraphQL query with the Python script using the `requests` library to make the API request:

#```python
import requests
import os
import json
import base64
import pprint



issues_query = """{
  viewer {
    login
    issues(last: 100) {
    nodes {
id 
url
}
        }
      }
    }
"""

def gen_issue_query(
        _id=1, first_n_items=100,  owner = "meta-introspector",
        first_n_threads=100, repo_name  = "meta-meme",
        node_type = "Issue", child_type = "comments",        title = "title"):
    return f"""{{ node(id: "{ _id}") {{ id __typename # Issue
    ... on {node_type} {{ 
       title
       state
       closed
       closedAt
       createdAt
       updatedAt
    body 
    author {{ login }}
    labels(first: 10) {{
         nodes {{
           name
           color
         }}
       }}
      milestone {{
        title
        state
        dueOn
      }}
      assignees(first: 10) {{
        nodes {{
          login
        }}
      }}
      reactions(content: THUMBS_UP, first: 10) {{
        totalCount
        nodes {{
          user {{
            login
          }}
        }}
    }}

    comments(first: 100) {{ totalCount nodes {{  
    author {{ login }}  body  createdAt }} }} }} }} }}
    """

# To retrieve maximum data for each issue using the GitHub GraphQL API, you would need to specify all the fields you're interested in within the query. Here's an example query that fetches various fields for a specific issue:

# ```graphql
# {
#   repository(owner: "owner_name", name: "repo_name") {
#     issue(number: 1) {
#       title
#       state
#       closed
#       closedAt
#       createdAt
#       updatedAt
#       author {
#         login
#       }
#       comments {
#         totalCount
#         nodes {
#           author {
#             login
#           }
#           body
#           createdAt
#         }
#       }
#       labels(first: 10) {
#         nodes {
#           name
#           color
#         }
#       }
#       milestone {
#         title
#         state
#         dueOn
#       }
#       assignees(first: 10) {
#         nodes {
#           login
#         }
#       }
#       reactions(content: THUMBS_UP, first: 10) {
#         totalCount
#         nodes {
#           user {
#             login
#           }
#         }
#       }
#     }
#   }
# }
# ```

# In this query:
# - `title`, `state`, `closed`, `closedAt`, `createdAt`, and `updatedAt` provide basic issue details.
# - `author { login }` fetches the login of the author of the issue.
# - `comments` retrieves comments associated with the issue, including their author, body, and creation time.
# - `labels` retrieves up to 10 labels applied to the issue, including their names and colors.
# - `milestone` fetches details about the milestone associated with the issue, including its title, state, and due date.
# - `assignees` retrieves up to 10 assignees of the issue.
# - `reactions` retrieves reactions of type "THUMBS_UP" on the issue, including their count and the login of the users who reacted.

# Feel free to adjust the query and fields according to your needs. Keep in mind that requesting a large amount of data may result in a larger response and increased response time.



# API endpoint
url = "https://api.github.com/graphql"

# Your GitHub personal access token

file_path = os.path.expanduser("~/.github")
with open(file_path, "r") as file:
    pat_contents = file.read()

headers = {
    "Authorization": f"Bearer {pat_contents}"
}


def run_req(query):
    response = requests.post(url, json={"query": query}, headers=headers)
    data = response.json()

    yield data


#for x in range(1,67): #fix me
    #q = gen_discussion_query(x)
q = issues_query #= """{ gen_discussion_query(node_type="issues")
for data in run_req(q):
    print(json.dumps({"index":data}))
    for x in data['data']['viewer']['issues']['nodes']:                  
        if "id" in x:

            #decoded_id = base64.b64decode(x["id"]).decode("utf-8")
            decoded_id = x["id"]
            
            q2 = gen_issue_query(decoded_id)
            #print(q2)
            for data in run_req(q2):
                #print(x, data)
                print(json.dumps({"node":x,"payload":data}))
        else:
            print(json.dumps({"err":x}))
    #print(o)
        
    #print(data)
