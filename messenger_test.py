import requests
from dotenv import dotenv_values

config = dotenv_values(".env")

def callSendAPI(senderPsid, response):
    PAGE_ACCESS_TOKEN = config.PAGE_ACCESS_TOKEN

    payload = {
    'recipient': {'id': senderPsid},
    'message': response,
    'messaging_type': 'RESPONSE'
    }
    headers = {'content-type': 'application/json'}

    url = 'https://graph.facebook.com/v10.0/me/messages?access_token={}'.format(PAGE_ACCESS_TOKEN)
    r = requests.post(url, json=payload, headers=headers)
    print(r.text)


# client = Client(config["FB_EMAIL"], config["FB_PASSWORD"])

print("hi")

# print("Own id: {}".format(client.uid))

# client.send(Message(text="Hi me!"), thread_id=client.uid, thread_type=ThreadType.USER)

# client.logout()