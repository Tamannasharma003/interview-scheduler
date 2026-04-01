from flask import Flask

app = Flask(__name__)

# ✅ HOME ROUTE HERE (guaranteed to work)
@app.route("/")
def home():
    return "Server running ✅"

# import AFTER route
import webhook  

print("✅ app.py loaded")

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
