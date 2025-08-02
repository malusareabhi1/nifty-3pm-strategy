from kiteconnect import KiteConnect
import webbrowser

api_key = "your_api_key"
api_secret = "your_api_secret"

kite = KiteConnect(api_key=api_key)
login_url = kite.login_url()
webbrowser.open(login_url)
print("🔑 Visit this URL and paste request_token from redirect URL:")

request_token = input("🔁 Request Token: ")
data = kite.generate_session(request_token, api_secret=api_secret)

print("✅ Access Token:", data["access_token"])
