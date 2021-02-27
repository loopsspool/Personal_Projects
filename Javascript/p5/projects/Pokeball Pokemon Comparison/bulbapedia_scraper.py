import requests
from bs4 import BeautifulSoup

# Origin page (list of pokes by national pokedex)
starter_url = "https://bulbapedia.bulbagarden.net"
nat_pokedex_page = requests.get("https://bulbapedia.bulbagarden.net/wiki/List_of_Pok%C3%A9mon_by_National_Pok%C3%A9dex_number")
nat_pokedex_soup = BeautifulSoup(nat_pokedex_page.content, 'html.parser')
pokemon_links = []

# Semi-crude way of excluding styling for tables
    # Since they're split up by pokemon generation
# Searches table rows
for poke in nat_pokedex_soup.find_all('th'):
    # And only appends if there are no attributes (meaning it's a pokemon cell)
    if poke.attrs == {}:
        pokemon_links.append(poke.a.get('href'))

# This line removes duplicates (while maintaining order) from:
    # Mega evolutions
    # Different forms
    # Regional forms
    # etc.
pokemon_links = list(dict.fromkeys(pokemon_links))

# TODO: Apply to all pokemon pages
# Dealing with individual pokemon pages
indv_poke_url = starter_url + pokemon_links[0]
indv_poke_page = requests.get(indv_poke_url)
indv_poke_soup = BeautifulSoup(indv_poke_page.content, 'html.parser')

sprite_img_links = []
# Finds where the sprite point is in the page and grabs it's parent
sprites_start = indv_poke_soup.find(id="Sprites").parent
# Then grab the next sibling (sprites image table)
sprites_table = sprites_start.find_next_sibling()
sprites_table = sprites_table.find_all('th')
# TODO: Seperate by game or generation?
# TODO: Figure out url pattern and determine:
    # Mega evolutions
    # Gigantamax
    # Sex differences
    # Shinies
    # Front/Back
# And filter for images (so no generation headers)
for cell in sprites_table:
    if not cell.img == None:
        sprite_img_links.append(cell.img.get('src'))

print(sprite_img_links)
