import json
import requests
from os import environ
from bs4 import BeautifulSoup
import time

api_key = environ.get("TELEGRAM_API_KEY")


def lambda_handler(event, context):
    headers = {"User-agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36"}
    webpage_url = "https://www.lenovo.com/ar/es/laptops/thinkpad/serie-t/c/thinkpadt"
    page = requests.get(webpage_url, headers=headers)
    soup = BeautifulSoup(page.text, "html.parser")
    # search all html lines containing table data
    top_info = soup.find_all('div', {'class': 'top-info'})
    titles = []
    laptop_found = False
    laptop_url = ""
    multiple_laptops_found = False
    for info in top_info:
        header = info.find('h3', {'class': 'seriesListings-title'})
        price = info.find('dd', {'itemprop': 'price'})
        if header is not None and price is not None:
            anchor = header.find('a')
            title = anchor.contents[0]
            href = "https://www.lenovo.com"+anchor.attrs['href']
            if ("T14 " in title or "T15 " in title) and "AMD" in title:
                if laptop_found:
                    multiple_laptops_found = True
                    laptop_url = webpage_url
                else:
                    laptop_found = True
                    laptop_url = href
            titles.append(f"<a href='{href}'>{title}</a><pre> {price.contents[0]} </pre>")

         

    requests.post(
        f"https://api.telegram.org/bot{api_key}/sendMessage",
        json={
            'chat_id': "@ThinkHunt",
            'text': ' '.join(titles),
            'parse_mode': 'HTML'
        })

    if laptop_found:
        time.sleep(2)
        requests.post(
            f"https://api.telegram.org/bot{api_key}/sendMessage",
            json={
                'chat_id': "@ThinkHunt",
                'text': f"<a href='{laptop_url}'>Encontre más de una compu!!</a>" if multiple_laptops_found else f"<a href='{laptop_url}'>Encontre una compu!!</a>",
                'parse_mode': 'HTML'
            }) 

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": 
            "\n".join(titles),
        }),
    }
