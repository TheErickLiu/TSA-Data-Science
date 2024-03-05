import requests
from requests.auth import HTTPBasicAuth
import datetime

# Authentication and setup
client_id = 'v-iUckckYiCHjoyz1UlMAQ'
client_secret = '5X3FHbm-nrXVmVv8OJE62PPVi-tGgw'
username = 'Necessary_Can_3405'
password = '9537(%#&'
user_agent = 'MyAPI/0.0.1'

auth = HTTPBasicAuth(client_id, client_secret)

data = {
    'grant_type': 'password',
    'username': username,
    'password': password,
}

headers = {'User-Agent': user_agent}

res = requests.post('https://www.reddit.com/api/v1/access_token', auth=auth, data=data, headers=headers)
TOKEN = res.json()['access_token']
headers['Authorization'] = f'bearer {TOKEN}'

# Parameters for the search
search_term = ['GOOGL', 'alphabet']
limit = 100  # Max number of posts per request

# wallstreetbets
# investing
# stocks
# options
# StockMarket

subreddit = ['wallstreetbets', 'investing', 'stocks', 'options', 'StockMarket']
desired_posts = 10000  # Total number of posts you want
for red in subreddit:
    for term in search_term:
        url_template = f'https://oauth.reddit.com/r/{red}/search?limit={limit}&q={term}&t=year&restrict_sr=1'

        posts_fetched = 0
        after = None

        # Open a file to append data
        currentfile = 'redditDataAlphabet.txt'
        with open(currentfile, 'a', encoding='utf-8') as file:
            while posts_fetched < desired_posts:
                if after:
                    url = f'{url_template}&after={after}'
                else:
                    url = url_template
                
                response = requests.get(url, headers=headers).json()
                posts = response.get('data', {}).get('children', [])
                
                if not posts:  # Break the loop if no more posts are returned
                    break
                
                for post in posts:
                    title = post['data']['title'].replace('\n', ' ').replace('\r', ' ')
                    body_text = post['data']['selftext'].replace('\n', ' ').replace('\r', ' ')
                    created_utc = post['data']['created_utc']
                    # Convert the UTC timestamp to a readable datetime format
                    created_time = datetime.datetime.utcfromtimestamp(created_utc).strftime('%Y-%m-%d %H:%M:%S')
                    
                    # Write the title, body text, and creation time to the file, formatted as requested
                    file.write(f"[{title},;,; {body_text},;,; {created_time}]\n")
                    
                    posts_fetched += 1
                    if posts_fetched >= desired_posts:
                        break
                
                after = response['data'].get('after')  # Update the 'after' for the next iteration
                
                if not after:  # If there's no more data to paginate through, break the loop
                    break

        print(f"Finished adding {posts_fetched} posts to {currentfile} for {term} in r/{red}.")