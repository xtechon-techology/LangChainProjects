import requests
import json

username = '{YOUR_USERNAME}'
apiKey = '{YOUR_API_KEY}'

apiEndPoint = "http://api.scraping-bot.io/scrape/data-scraper"

payload = json.dumps({
  "scraper": "linkedinCompanyProfile",
  "url": "",
  "keywords": "Apple",
  "account": "google",
  "hashtag": "",
  "keyword": "iPhone",
  "search": "Apple",
  "language": "en",
  "page": "/company",
  "posts_number": "12",
  "max_video_count": 30,
  "load_more_items_count": 10,
  "items_limit": 50,
  "city": "paris",
  "country": "FR",
  "number_of_tweets": 30,
  "posts_max_count": 100,
  "posts_number": 10
})
headers = {
  'Content-Type': "application/json"
}

response = requests.request("POST", apiEndPoint, data=payload, auth=(username,apiKey), headers=headers)

print(response.text)