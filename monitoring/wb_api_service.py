import requests


def get_product_info(article):
    product_info = requests.get(
        f'https://card.wb.ru/cards/detail?appType=1&curr=rub&dest=123585853&spp=29&nm={article}').json()["data"]["products"]
    if product_info:
        title = product_info[0]['name']
        availability = False
        for size in product_info[0]['sizes']:
            if len(size['stocks']):
                availability = True
                break
        if availability:
            price = product_info[0]['salePriceU'] / 100
        else:
            price = -1
        dict_product_info = {'title': title, 'availability': availability, 'price': price}
        return dict_product_info
    else:
        return None

def get_image(article) -> str:
    _short_id = article // 100000
    if 0 <= _short_id <= 143:
        basket = '01'
    elif 144 <= _short_id <= 287:
        basket = '02'
    elif 288 <= _short_id <= 431:
        basket = '03'
    elif 432 <= _short_id <= 719:
        basket = '04'
    elif 720 <= _short_id <= 1007:
        basket = '05'
    elif 1008 <= _short_id <= 1061:
        basket = '06'
    elif 1062 <= _short_id <= 1115:
        basket = '07'
    elif 1116 <= _short_id <= 1169:
        basket = '08'
    elif 1170 <= _short_id <= 1313:
        basket = '09'
    elif 1314 <= _short_id <= 1601:
        basket = '10'
    elif 1602 <= _short_id <= 1655:
        basket = '11'
    elif 1656 <= _short_id <= 1919:
        basket = '12'
    else:
        basket = '13'
    return f"https://basket-{basket}.wb.ru/vol{article // 100000}/part{article // 1000}/{article}/images/big/{1}.webp"
