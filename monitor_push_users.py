import requests
import sqlite3
import json
import time

# Define the SQLite DB name
DB_NAME = '/app/db/github_users.db'

# Read configuration file
with open('config.json', 'r') as f:
    config = json.load(f)
    ORGANIZATIONS = config['organizations']
    API_KEY = config['api_key']

# Create the SQLite DB and the table if they don't exist
conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS GithubUsers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    organization TEXT NOT NULL
)
""")
conn.commit()

def monitor_github():
    headers = {
        'Accept': 'application/vnd.github+json',
        'Authorization': f'token {API_KEY}'
    }
    for org in ORGANIZATIONS:
        url = f'https://api.github.com/orgs/{org}/events'
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            events = response.json()
            for event in events:
                if event['type'] == 'PushEvent':
                    username = event['actor']['login']
                    try:
                        cursor.execute("""
                        INSERT INTO GithubUsers (username, organization) 
                        VALUES (?, ?)
                        """, (username, org))
                        conn.commit()
                        print(f'Successfully inserted {username} from {org}')
                    except sqlite3.IntegrityError:
                        print(f'User {username} from {org} already exists in the database')
                    monitor_user_commits(username, headers)
        else:
            print(f'Failed to retrieve events for {org}. Status code: {response.status_code}')

        # GitHub API has a rate limit, adjust accordingly
        time.sleep(1)

def monitor_user_commits(username, headers):
    url = f'https://api.github.com/users/{username}/events'
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        events = response.json()
        for event in events:
            if event['type'] == 'PushEvent':
                for commit in event['payload']['commits']:
                    repo_name = event['repo']['name']
                    sha = commit['sha']
                    commit_url = f'https://api.github.com/repos/{repo_name}/commits/{sha}'
                    commit_response = requests.get(commit_url, headers=headers)
                    if commit_response.status_code == 200:
                        commit_content = commit_response.json()
                        print(f'Commit by {username}: {commit_content}')  # print the entire commit content
                    else:
                        print(f'Failed to retrieve commit content for {username}. Status code: {commit_response.status_code}')
    else:
        print(f'Failed to retrieve events for {username}. Status code: {response.status_code}')



if __name__ == "__main__":
    while True:
        monitor_github()
        # Delay between checks, adjust as needed
        time.sleep(60)

