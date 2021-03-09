import requests
from bs4 import BeautifulSoup
import pandas as pd

def get_gen_number(gen_cell_text):
    # Gets roman numeral of generation number
    gen_number = gen_cell_text.split(" ")[2]
    # Slices new line escape character off the end
    gen_number = gen_number[0:(len(gen_number) - 1)]
    # Converting roman numeral generation to integer so can be used in comparisons
    if (gen_number == "I"):
        return("Gen1")
    if (gen_number == "II"):
        return("Gen2")
    if (gen_number == "III"):
        return("Gen3")
    if (gen_number == "IV"):
        return("Gen4")
    if (gen_number == "V"):
        return("Gen5")
    if (gen_number == "VI"):
        return("Gen6")
    if (gen_number == "VII"):
        return("Gen7")
    if (gen_number == "VIII"):
        return("Gen8")
    

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

games_by_generation = [["Red/Blue", "Yellow", "Red/Green"],
                       ["Gold", "Silver", "Crystal"],
                       ["Ruby/Sapphire", "Emerald", "FireRed/LeafGreen"],
                       ["Diamond/Pearl", "Platinum", "HeartGold/SoulSilver"],
                       ["Black/White", "Black_2/White_2"],
                       ["X/Y", "Omega_Ruby/Alpha_Sapphire"],
                       ["Sun/Moon", "Ultra_Sun/Ultra_Moon"],
                       ["Sword/Shield"]
                      ]
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
# TODO: Figure out url pattern and determine:
    # Mega evolutions
    # Gigantamax
    # Sex differences
    # Forms
    # Shinies
    # Front/Back

generation = "Gen0"
for cell in sprites_table:
    # if not cell.img == None:
    #     sprite_img_links.append(cell.img.get('src'))
    # These will all be finding what parameters to add to file name
    # TODO: get pokemon number & name
    # Getting generation

    if "Generation" in cell.text:
        generation = get_gen_number(cell.text)
    print(generation)
    # Getting game (a since all game headers have links to their pages)
    if cell.a:
        if not cell.text == " \n":
            game.append(cell.text)
    # if title in text
        # get game title and name with pair or individually
print(game)


# pd.set_option('display.max_colwidth', None)
# pd.set_option('display.max_columns', 500)
# pd.set_option('display.width', 150)
# sprites_table_pandas = pd.read_html(str(indv_poke_url))
# print(sprites_table_pandas.shape)

#print(str(sprites_table))