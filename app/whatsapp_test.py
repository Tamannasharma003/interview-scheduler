import requests

print("Script started")

ACCESS_TOKEN = "EAALHZAkuHdf8BQ2ew8XaCYAJuye510MtX2gMS9Rw2sZBPfsJUEwWMkQOhIxxYH2ZBclZBGWuG4suZAKgNSAkOKp265s4b38QCDzsW9fQOP7Bt0oIIeZAplNwYdBkL7AcQKf7j8s7BUdJyHqwsZAjYvywX2HVn352KmP8CIwkxvXJnzyphX1s1B3VZCdl6lhi6hk0zerZBCZAqnok88f6j3zCD8vtab9ZBO4eJvhzZBIrjg6mGF7GQnAwPt7kyt0CuS5gniEHgdCHnSnNwCA94YnZAtAAm9kAN"
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
