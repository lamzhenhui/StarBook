
import requests

url = "https://api.weixin.qq.com/customservice/kfaccount/add?access_token=88_jHFluDPCeF6NSoXsmcAwiHBLBU7-pkatF2byU84BDQrH5EJegyh1LGI4ASSNPWSIxPlbmGlr9gsVfQTgzqsp6ymaJrwL90ZdmbYHWU6WxCSH5IEUmE53rMjdmwEASVcAGAHZC"
params = {
     "kf_account" : "test1@test",
     "nickname" : "客服1",
     "password" : "pswmd5"
}

response = requests.post(url, params=params)
print(response.json())

"""
cd /opt/code/post_app/. && python wg_app.py
"""