import requests

url = "https://orange-chainsaw-q7qgpx95p9gxc6wr9-8000.app.github.dev/get_data"
response = requests.get(url)
json_data = response.json()

print(json_data)