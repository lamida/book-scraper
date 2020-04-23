#!/usr/bin/env python
# -*- coding: utf-8 -*-

from urllib.request import urlopen
from bs4 import BeautifulSoup
import json
from datetime import datetime


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

    def last_update(self, last_update):
        self.last_update = last_update

    def price_decreased(self, price_decreased):
        self.price_decreased = price_decreased


def get_bd_meta(url, html):
    product = Product()
    product.url(url)
    product.last_update(datetime.now().isoformat())

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
    product.last_update(datetime.now().isoformat())

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

            for p in json_products:
                product = Product()
                product.url(url)
                product.name(p.get('name'))
                product.price(p.get('price'))
                product.last_price(p.get('last_price'))
                product.min_price(p.get('min_price'))
                product.rrp(p.get('rrp'))
                product.last_update(p.get('last_update'))
                product.price_decreased(p.get('price_decreased'))

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
            if product.price < stored_product.min_price:
                product.min_price(product.price)
                product.price_decreased(True)
            else:
                product.min_price(stored_product.min_price)
                product.price_decreased(False)
            db[url] = product

    print(f"going to dump json: {db}")
    # Make it json seriazable
    json_db = []
    for url in sorted(db.keys()):
        db[url] = db[url].__dict__
        json_db.append(db[url])

    updated_db_json = json.dumps(
        json_db,
        sort_keys=True,
        indent=4,
        separators=(
            ',',
            ': '))
    with open(STORAGE, 'w') as storage:
        storage.write(updated_db_json)

    print("DB is updated...")

    for key in sorted(db.keys()):
        product = db[key]
        if product["price_decreased"]:
            print(f"Price decreased for {product['name']} to {product['price']}")


run()
