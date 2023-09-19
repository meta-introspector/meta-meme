import requests
import os
import json

def gen_discussion_query(
        discussion_id,
        owner = "meta-introspector",
        first_n_threads=10,
        repo_name  = "meta-meme",
):
    return f"""
    query {{
        repository(owner: "{owner}", name: "{repo_name}") {{
            discussion(number: {discussion_id}) {{                title                body
                comments(first: {first_n_threads}) {{
                    nodes {{                        author {{                            login                        }}                        body                    }}                }}            }}        }}    }}
    """

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
    if data['data']['repository']['discussion'] is None:
        pass
    else:
        #print(data)
        print(json.dumps({"data":data}))

for x in range(1,100): #fix me
    q = gen_discussion_query(x)
    run_req(q)
    #print(o)
        
