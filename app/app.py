from flask import Flask

app = Flask(__name__)

# Import webhook routes AFTER creating app
import webhook


import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

