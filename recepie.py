import bs4.element
import requests
from bs4 import BeautifulSoup

import json

def get_item(soup):
    item_data = {
        "outputs": {},
        "inputs": {},
        "crafting time": -1
    }

    children = []

    recipe = soup.find_all('td', attrs={'class': 'infobox-vrow-value'})[0]
    children_elements = [child for child in recipe.children if child]

    are_inputs = True

    for c in children_elements:
        if isinstance(c, bs4.element.NavigableString):
            if "→" in c:
                are_inputs = False

        elif isinstance(c, bs4.element.Tag):

            name = c.find('a').get('title').lower()

            if are_inputs:
                if name.lower() == "time":
                    quant = c.find('div', attrs={'class': 'factorio-icon-text'}).text
                    item_data['crafting time'] = quant

                else:
                    quant = c.find('div', attrs={'class': 'factorio-icon-text'}).text
                    children.append((name, c.find('a').get('href')))

                    item_data['inputs'][name] = quant

            else:
                quant = c.find('div', attrs={'class': 'factorio-icon-text'}).text

                item_data['outputs'][name] = quant

    title = soup.find('h1', attrs={'class': 'mw-first-heading'}).text.lower()

    return title, item_data, children


def get_item_recursive(title, href, recipes):
    base_url = 'https://wiki.factorio.com'

    url = f'{base_url}{href}'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    if title in recipes:
        return

    title, item_data, children = get_item(soup)

    print(f'found {title}')
    recipes[title] = item_data

    for name, next in children:
        print('looking in child', name)
        get_item_recursive(name, next, recipes)


recipes = {
    "copper ore": None,
    "iron ore": None,
    "stone": None,
    "coal": None,
    "crude oil": None,
    "petroleum gas": None,
    "light oil": None,
    "heavy oil": None,
    "water": None,
    "uranium ore": None,
    "solid fuel": None
}


recipes.update(json.load(open('recipies.json', 'r')))

bases = [
    ("satellite", "/Satellite"),
    ("utility science pack","/Utility_science_pack"),
    ("production science pack", "/Production_science_pack"),
    ("chemical science pack", "/Chemical_science_pack"),
    ("military science pack", "/Military_science_pack"),
    ("logistic science pack", "/Logistic_science_pack"),
    ("automation science pack", "/Automation_science_pack")

]

for name, href in bases:
    get_item_recursive(name, href, recipes)
    3
json.dump(recipes, open('recipies.json', 'w'), indent=2)
