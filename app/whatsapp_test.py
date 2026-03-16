import requests

print("Script started")

ACCESS_TOKEN = "EAALHZAkuHdf8BQ0qQe1Pj0yEdwjgIchpZAgDkdkUyAfKGa0s3cSf6PcEGAGEXgUaPHyJhoSOzUlaJXB0L7HxgMFuCQQmsa3irXTyuYq3rrV5U6iZA9gmZA1cSJqi9rJqYFVwTFuElBAFdpfVZBbl90fpZBr0WVnOEHHsiLWMM1ZAZCo5DJBZCDprJYPD4rKgljW6szsmPob9vQ6QYiL2Benp8SKZBgehaewAuZB6ZCjoxWqsiM9dmkICQXFSH1mHNBB9PAs6qXUzB8lYqRpsWTC9b5rgiuyWZBAZDZD"
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
