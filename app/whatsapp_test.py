import requests

print("Script started")

ACCESS_TOKEN = "EAALHZAkuHdf8BQwLx34Vkmebvl5Ht0PouKktlG7rw8vZBRwYKZAMHi5iW35sNM2cRaHzygBDEzhtFgSiNUaTzCdI1NaiHDUgMO0dOnIAzAO5wcmfgKtcYrotaVr0OLHAecESj2AEM66dG7zrNZC9wgwGlH5WfpWZBeXyDgDkTzELB4Xc2XCxrzmK7tqwmJUqeVdZCxNEwHlcKQbWKLLOj41Nzml2mQJtRQweiFcgX6K8lfRhEpCZA5g3HlYUPPrK08x7XI0J0ETv4oxGI5Q7g1EzqFi5QZDZD"
PHONE_NUMBER_ID = "1133619556482851"

url = f"https://graph.facebook.com/v18.0/{PHONE_NUMBER_ID}/messages"

headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type": "application/json"
}

data = {
    "messaging_product": "whatsapp",
    "to": "918168100074",
    "type": "text",
    "text": {
        "body": "Hello Tamanna 👋 Your Interview Scheduler WhatsApp API is working!"
    }
}

response = requests.post(url, headers=headers, json=data)

print(response.json())
