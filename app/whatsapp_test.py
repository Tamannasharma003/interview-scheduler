import requests

print("Script started")

ACCESS_TOKEN = "EAALHZAkuHdf8BQzlOppsIycxGewnpJMXxqRYkobA2PLBNruHGPAn8jHm5oeWCxZAx8TWJ7NSpJa2APxw8ugqPfAdUmKTPhTk9i6mgKc3D0YJ6ayuKUVLpPxdGcZBgZAZCnLYX71aLGMg1UsqDYtvMdrlwE8SXyZChov5PJgb6Vw6q3zmN5urNBhOe0q9iT43JAqq2iZCgTo9zG1sw19aDqOKEZA4iBObr3VeaSVio8Bm068HeCLXDbH6GQEJ3eDTbLEcTZACLTkz9zLA4om6CGTYVnGRd"

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
