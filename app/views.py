import os
import json
import requests
import pandas as pd
from bs4 import BeautifulSoup
from config import headers
from app import app
from flask import render_template, redirect, url_for, request


def list_to_html(l):
    return "<ul>"+"".join([f"<li>{e}</li>" for e in l])+"</ul>" if l else ""

def extract (ancestor, selector, attribute=None, multiple=False):
    if selector:
        if multiple:
            if attribute:
                return [tag.text.strip() for tag in ancestor(selector)]
            return [tag.text.strip() for tag in ancestor(selector)]
        if attribute:
            try:
                return ancestor.select_one(selector)[attribute].strip() 
            except TypeError:
                  return None
        try:
            return ancestor.select_one(selector).strip()
        except AttributeError:
            return None
    if attribute:
        return ancestor[attribute].text.strip()
    return None

selectors = {
                "opinion_id": (None, "data-entry-id"),
                "author": ("span.user-post__author-name",),
                "recommendation": ("span.user-post__author-recomendation > em",),
                "stars": ("span.user-post__score-count",),
                "content": ("div.user-post__text",),
                "pros": ("div.review-feeature__item--positive" None, True),
                "cons": ("div.review-feeature__item--negative" None, True),
                "useful": ("button.vote-yes", "data-total-vote"),
                "useless": ("button.vote-no", "data-total-vote"),
                "post_date": ("span.user-post__published > time:nth-child(1)", "datetime"),
                "purchase_date": ("span.user-post__published > time:nth-child(2)", "datetime"),
            }             

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/extract', methods=['post'])
def extract_data():
    product_id = request.form.get('product_id')
    url = f"https://www.ceneo.pl/{product_id}#tab=reviews"
    all_opinions = []
    while url:
        response = requests.get(url, headers=headers)
        print(response.status_code)
        if response.status_code==200:
            page_dom = BeautifulSoup(response.text, "html.parser")
            opinions = page_dom.select("div.js_product-review:not(.user-post--highlight)")
            if opinions:
                print(len(opinions))    
                for opinion in opinions:
                    single_opinion = {
                        key: extract(opinion, *value) for key, value in selectors.items()
                    }             
                all_opinions.append(single_opinion)
            try:
                url = "https://www.ceneo.pl"+extract(page_dom, "a.pagination__next", "href")
            except TypeError:
                url = None
        if not os.path.exists("./app/data"):
            os.mkdir("./app/data")
        if not os.path.exists("./app/data/opinions"):
            os.mkdir("./app/data/opinions")
        with open(f"./app/data/opinions/{product_id}.json", "w", encoding="UTF-8") as jf:
            json.dump(all_opinions, jf, indent=4, ensure_ascii=False)
        product_info = {
    "product_id": product_id,
    "product_name": "Urządzenie wielofunkcyjne HP Envy 6020e AiO HP+ Instant Ink (223N4B)",
    "opinions_count": 55,
    "pros_count": 37,
    "cons_count": 1,
    "average_stars": 4.618181818181818,
    "stars_distr": {
        "0.0": 0,
        "0.5": 1,
        "1.0": 2,
        "1.5": 0,
        "2.0": 0,
        "2.5": 0,
        "3.0": 1,
        "3.5": 2,
        "4.0": 1,
        "4.5": 5,
        "5.0": 43
    },
    "recommendation_distr": {
        "Polecam": 49,
        "Nie polecam": 3,
        "null": 0
    }
}

        return redirect(url_for('products', product_id=product_id))
    error = "Coś poszło nie tak"
    return render_template("extract.html", error=error)

@app.route('/extract', methods=['get'])
def display_form():
    return render_template("extract.html")

@app.route('/products')
def products():
    products = []
    for file in os.listdir("./app/data/products"):
        if file.endswith(".json"):
            with open(os.path.join("./app/data/products", file), "r", encoding="utf-8") as f:
                data = json.load(f)
                products.append(data)
    return render_template("product.html", products=products)

@app.route('/author')
def author():
    return render_template("author.html")

@app.route('/product/<int:product_id>')
def product(product_id:int):
    try:
        with open(f"./app/data/opinions/{product_id}.json", "r", encoding="UTF-8") as jf:
            try:
                opinions = json.load(jf)
            except json.JSONDecodeError:
                error = "błędny format pliku"
                return render_template("product.html", error=error)
    except FileNotFoundError:
                error = "Dla produktu o podanym id nie pobrano jeszcze opinii"
                return render_template("product.html", error=error)
    
    opinions = pd.DataFrame.from_dict(opinions)
    opinions.pros = opinions.pros.apply(list_to_html)
    opinions.cons = opinions.pros.apply(list_to_html)

    return render_template("product.html", opinions= opinions.to_html(classes="table table-hover tabel-bordered table-striped", index=False))