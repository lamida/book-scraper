#!/usr/bin/env python
# -*- coding: utf-8 -*-

from urllib.request import urlopen
from bs4 import BeautifulSoup
import json


class Product:
    def __init__(self):
        pass

    def url(self, url):
        self.url = url

    def name(self, name):
        self.name = name

    def price(self, price):
        self.price = price

    def last_price(self, last_price):
        self.last_price = last_price

    def min_price(self, min_price):
        self.min_price = min_price

    def rrp(self, rrp):
        self.rrp = rrp


def get_bd_meta(url, html):
    product = Product()
    product.url(url)

    bs = BeautifulSoup(html.read(), 'html.parser')
    prices = bs.findAll('span', {'class': 'sale-price'})
    rrps = bs.findAll('span', {'class': 'rrp'})
    names = bs.findAll('h1', {'itemprop': 'name'})

    if len(names) > 0:
        product.name(names[0].text)
    if len(prices) > 0:
        product.price(prices[0].text)
    if len(rrps) > 0:
        product.rrp(rrps[0].text)
    return product


def get_amazon_meta(url, html):
    product = Product()
    product.url(url)

    bs = BeautifulSoup(html.read(), 'html.parser')
    prices = bs.findAll('span', {'class': 'offer-price'})
    names = bs.findAll(id='productTitle')

    if len(names) > 0:
        product.name(names[0].text)
    if len(prices) > 0:
        product.price(prices[0].text)
    return product


def get_product(url):
    html = urlopen(url)
    if "bookdepository" in url:
        return get_bd_meta(url, html)
    elif "amazon" in url:
        return get_amazon_meta(url, html)
    else:
        print(f"Unknown provider {url}")
        return None


STORAGE = "books.json"


def load_db():
    db = dict()
    try:
        with open(STORAGE) as storage:
            json_string = storage.read()
            json_products = json.loads(json_string)

            for url in sorted(json_products.keys()):
                p = json_products[url]

                product = Product()
                product.url(url)
                product.name(p.get('name'))
                product.price(p.get('price'))
                product.last_price(p.get('last_price'))
                product.min_price(p.get('min_price'))
                product.rrp(p.get('rrp'))

                db[p['url']] = product
    except Exception as e:
        print(f"Error {e}")
        with open(STORAGE, "w") as storage:
            print("The DB file is not available, create a new empty one")
            storage.write("{}")
    return db


def load_urls():
    url_files = ["urls/amazonsg", "urls/bd"]
    urls = []
    for url_file in url_files:
        with open(url_file) as f:
            urls += f.read().splitlines()
    urls = list(filter(lambda x: x != "" and not x.startswith("#"), urls))
    return urls


def run():
    print("starting...")
    print("loading db...")
    db = load_db()
    print("loading url...")
    urls = load_urls()
    print(f"getting urls: {urls}")

    print("going to process urls...")
    for url in urls:
        print(f"Processing {url}")
        stored_product = db.get(url)
        product = get_product(url)
        if stored_product is None:
            print(f"No stored product for {url}")
            product.min_price(product.price)
            db[url] = product
        else:
            print(f"Found stored product for {url}")
            product.last_price(stored_product.price)
            product.min_price(product.price if product.price <
                              stored_product.min_price else stored_product.min_price)
            db[url] = product

    print(f"going to dump json: {db}")
    # Make it json seriazable
    for url in sorted(db.keys()):
        db[url] = db[url].__dict__

    updated_db_json = json.dumps(
        db,
        sort_keys=True,
        indent=4,
        separators=(
            ',',
            ': '))
    with open(STORAGE, 'w') as storage:
        storage.write(updated_db_json)

    print("DB is updated...")


run()
