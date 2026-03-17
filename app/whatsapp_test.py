import requests

print("Script started")

ACCESS_TOKEN = "EAALHZAkuHdf8BQ0KZB8tR5Kxy70bqAR0pTaYnKVFiKvWQe8AsDGphStHoRKhZAGNzwFZAfHhFZChE4kaAc3K0t4TahWZA9YI8aXTXV4PnCFTENjNZAoKzsU4BCunEI82c8CAsZBWAUAS1zyLH9BLwtogC7IoYKvnt12K1fIjPK4esMSDBLg1XUUQbYBiHraZBLS56wBSpezGxoQUPfZCmAi3v1OgwQAZBk1D9VrlgkRf2WM4fcXPOUDWMTomczvqE4ZAXYjBgOVPeR3e5o5oYSLAtmN4HOZBE"
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
