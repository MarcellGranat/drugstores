import pandas as pd
import requests
import bs4
from datetime import date

df = pd.read_csv('c:/pyprojects/dm/data/rm_links_to_brands2021-08-17.csv')

links = list(df.links)

links = [str(x) + '?isLayerAjax=1&limit=36' for x in links]

print(links)

df_total = pd.DataFrame()

for category_link in links:
    print('######################################## ' + category_link + ' ################################################')

    product_names_all = list()
    product_urls_all = list()
    product_prices_all = list()

    n_page = 1
    while True:
        print(n_page)
        if n_page == 1:
            url = category_link + '?isLayerAjax=1&limit=36'
        else:
            url = category_link + '?isLayerAjax=1&limit=36&p=' + str(n_page)
        try:
            page = bs4.BeautifulSoup(requests.get(url).text, 'lxml')
            product_names = page.select('h2 > a')
            product_urls = [product_name.attrs['href'] for product_name in product_names]
            product_prices = page.select('.special .price , .regular-price .price')
            product_names = [product_name.text for product_name in product_names]
            product_prices = [product_price.text for product_price in product_prices]

        except:
            break

        if product_names[0] in product_names_all:
            break
        else:
            for product_name in product_names:
                product_names_all.append(product_name)
            for product_url in product_urls:
                product_urls_all.append(product_url)
            for product_price in product_prices:
                product_prices_all.append(product_price)

        n_page += 1

        df = pd.DataFrame({'product': product_names_all, 'price': product_prices_all, 'url': product_urls_all})
        df['category'] = category_link
        df_total = df_total.append(df)

df_total.to_csv('c:/pyprojects/dm/data/rm_product_data' + str(date.today()) + '.csv')

print('DONE...')
