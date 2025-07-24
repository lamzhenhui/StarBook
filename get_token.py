import requests

url = "http://39.108.219.192/post-endpoint"
data = {"message": "Hello, Server!"}

response = requests.post(url, json=data)
print(response.json())


# import requests

# url = "https://api.weixin.qq.com/cgi-bin/token?"
# params = {
#     "appid": "wx685f417e73c9985f",
#     "grant_type": "client_credential",
#     "secret": "50bd22561b8b69f0a45bb80db5693dbb"
#     }

# response = requests.get(url, params=params)
# print(response.json())

# """
# cd /opt/code/post_app/. && python wg_app.py
# """