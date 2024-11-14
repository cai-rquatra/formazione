import requests

def login(username, password, expires_in_mins=30):
    url = "https://dummyjson.com/auth/login"
    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "username": username,
        "password": password,
        "expiresInMins": expires_in_mins
    }

    # Send the POST request to log in
    response = requests.post(url, json=payload, headers=headers)

    # Check for successful response
    if response.status_code == 200:
        access_token = response.json().get("accessToken")
        if access_token:
            print("Login successful!")
            return access_token
        else:
            print("Access token not found in response.")
            return None
    else:
        print(f"Login failed with status code {response.status_code}")
        print("Error message:", response.text)
        return None

def get_user_info(access_token):
    url = "https://dummyjson.com/auth/me"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    # Send the POST request to get user info
    response = requests.get(url, headers=headers)

    # Check for successful response
    if response.status_code == 200:
        user_info = response.json()
        print("User info retrieved successfully!")
        return user_info
    else:
        print(f"Failed to retrieve user info with status code {response.status_code}")
        print("Error message:", response.text)
        return None

def main():
    # Login and retrieve the access token
    access_token = login(username="emilys", password="emilyspass")

    # If login was successful, get user info
    if access_token:
        user_info = get_user_info(access_token)
        if user_info:
            print("User Info:", user_info)

if __name__ == "__main__":
    main()
