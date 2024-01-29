import requests


def get_product_info(article):
    product_info = requests.get(
        f'https://card.wb.ru/cards/detail?appType=1&curr=rub&dest=123585853&spp=29&nm={article}').json()
    return product_info["data"]["products"]
