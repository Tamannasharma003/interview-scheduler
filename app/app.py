from webhook import app
import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))  # Railway PORT
    print("🚀 Starting main app...")
    app.run(host="0.0.0.0", port=port)


