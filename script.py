#!/usr/bin/env python
# -*- coding: utf-8 -*-

from urllib.request import urlopen
from bs4 import BeautifulSoup
import json

urls = [
    "https://bookdepository.com/Java-Performance-Charlie-Hunt/9780137142521",
    "https://bookdepository.com/Random-Walk-Down-Wall-Street-Burton-G-Malkiel/9781324002185",
    "https://bookdepository.com/Release-It-Design-Deploy-Production-Ready-Software-Michael-T-Nygard/9781680502398",
    "https://bookdepository.com/Inspired-Marty-Cagan/9781119387503",
    "https://bookdepository.com/Happiness-Hypothesis-Jonathan-Haidt/9780465028023",
    "https://bookdepository.com/Bullet-Journal-Method-Ryder-Carroll/9780008261375",
    "https://bookdepository.com/Brave-Learner-Julie-Bogart/9780143133223",
    "https://bookdepository.com/Upheaval-Jared-Diamond/9780241003435",
    "https://bookdepository.com/Hyperion-Dan-Simmons/9780553283686",
    "https://bookdepository.com/Brothers-Karamazov-Fyodor-Dostoevsky/9780099922803",
    "https://bookdepository.com/Mind-for-Numbers-Barbara-Oakley/9780399165245",
    "https://bookdepository.com/Writing-Down-Bones-Natalie-Goldberg/9781611803082",
    "https://bookdepository.com/Simple-Path-Wealth-J-L-COLLINS/9781533667922",
    "https://bookdepository.com/Little-Book-Common-Sense-Investing-John-C-Bogle/9781119404507",
    "https://bookdepository.com/Bogleheads-Guide-Investing-Taylor-Larimore/9781118921289",
    "https://bookdepository.com/HBRs-10-Must-Reads-on-Managing-Yourself-with-bonus-article-How-Will-You-Measure-Your-Life-by-Clayton-M-Christensen-Peter-F-Drucker/9781422157992",
    "https://bookdepository.com/Cloud-Native-Designing-change-tolerant-software-Cornelia-Davis/9781617294297",
    "https://bookdepository.com/Building-Secure-Reliable-Systems-Ana-Oprea/9781492083122",
    "https://bookdepository.com/Capital-Twenty-First-Century-Thomas-Piketty/9780674430006",
    "https://bookdepository.com/Managing-Humans-Michael-Lopp/9781484221570",
    "https://bookdepository.com/Database-Internals-Alex-Petrov/9781492040347",
    "https://bookdepository.com/Python-for-DevOps-Noah-Gift/9781492057697",
    "https://bookdepository.com/Metasploit-Jr-David-Kennedy/9781593272883",
    "https://bookdepository.com/Cloud-Native-DevOps-with-Kubernetes-John-Arundel/9781492040767",
    "https://bookdepository.com/Cloud-Native-Boris-Scholl/9781492053828",
    "https://bookdepository.com/Architecture-Patterns-with-Python-Harry-J-W-Percival/9781492052203",
    "https://bookdepository.com/BPF-Performance-Tools-Brendan-Gregg/9780136554820",
    "https://bookdepository.com/Learning-Kali-Linux-Ric-Messier/9781492028697",
    "https://bookdepository.com/Terraform-Up-Running-Yevgeniy-Brikman/9781492046905",
    "https://bookdepository.com/Fundamentals-Software-Architecture-Mark-Richards/9781492043454",
]

results = []

for url in urls:
    html = urlopen(url)
    bs = BeautifulSoup(html.read(), 'html.parser')
    prices = bs.findAll('span', {'class':'sale-price'})
    rrps = bs.findAll('span', {'class':'rrp'})
    names = bs.findAll('h1', {'itemprop':'name'})
    product = {}
    if len(names) > 0:
        product["name"] = names[0].text
    if len(prices) > 0:
        product["price"] = prices[0].text
    if len(rrps) > 0:
        product["rrp"] = rrps[0].text
    results.append(product)

print(json.dumps(results, sort_keys=True, indent=4, separators=(',', ': ')))