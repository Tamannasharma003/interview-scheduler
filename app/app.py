from flask import Flask

app = Flask(__name__)

# ✅ IMPORTANT: load routes
from webhook import *


print("✅ app.py loaded")

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
