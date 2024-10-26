from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

def fetch_paginated_data(url, headers):
    result = []
    page = 1
    while True:
        response = requests.get(url, headers=headers, params={"page": page, "per_page": 100})
        if response.status_code != 200:
            print(f"Error fetching data: {response.status_code}")
            break
        page_data = response.json()
        if not page_data:
            break
        result.extend([user["login"] for user in page_data])
        page += 1
    return result

def unfollow(user, headers):
    url = f"https://api.github.com/user/following/{user}"
    response = requests.delete(url, headers=headers)
    return response.status_code == 204

def follow(user, headers):
    url = f"https://api.github.com/user/following/{user}"
    response = requests.put(url, headers=headers)
    return response.status_code == 204

def balance_following(username, token, exceptions):
    followers_url = f"https://api.github.com/users/{username}/followers"
    following_url = f"https://api.github.com/users/{username}/following"

    headers = {"Authorization": f"token {token}"}
    followers = fetch_paginated_data(followers_url, headers)
    following = fetch_paginated_data(following_url, headers)

    to_unfollow = list(set(following) - set(followers))
    to_follow = list(set(followers) - set(following))

    followed = [user for user in to_follow if follow(user, headers)]
    unfollowed = [user for user in to_unfollow if user not in exceptions and unfollow(user, headers)]

    return {"unfollowed": unfollowed, "followed": followed}

@app.route('/align', methods=['POST'])
def api_balance_following():
    data = request.json
    username = data.get("username")
    token = data.get("token")
    exceptions = data.get("exceptions", [])

    if not username or not token:
        return jsonify({"error": "username and token are required"}), 400

    result = balance_following(username, token, exceptions)
    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)