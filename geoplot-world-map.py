import requests

if __name__ == '__main__':

    url = "https://randomuser.me/api/"

    headers = {
        'accept': "application/json",
        'content-type': "application/json"
    }

    response = requests.request("GET", url, headers=headers)

    print(response.text)