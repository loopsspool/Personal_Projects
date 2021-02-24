import requests
from bs4 import BeautifulSoup

page = requests.get("https://bulbapedia.bulbagarden.net/wiki/List_of_Pok%C3%A9mon_by_National_Pok%C3%A9dex_number")
soup = BeautifulSoup(page.content, 'html.parser')
pokemon_list = []

# Semi-crude way of removing sytling for tables
    # Since they're split up by pokemon generation
# Searches table rows
for poke in soup.find_all('th'):
    # And only appends if there are no attributes (meaning it's a pokemon cell)
    if poke.attrs == {}:
        pokemon_list.append(poke)

print(pokemon_list)