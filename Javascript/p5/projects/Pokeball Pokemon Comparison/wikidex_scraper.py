import requests     # For fetching HTML
from bs4 import BeautifulSoup   # For parsing HTML
import xlrd     # For reading excel data (female, forms, etc)
import urllib.request      # For saving images
import re   # To check each name is formatted properly

# SPREADSHEET DATA
pokemon_info = xlrd.open_workbook('C:\\Users\\ejone\\OneDrive\\Desktop\\Code\\Javascript\\p5\\projects\\Pokeball Pokemon Comparison\\Pokemon Info.xls')
sheet = pokemon_info.sheet_by_index(0)

def cell_value(row, col):
    return (sheet.cell_value(row, col))


# WEB DATA
sprite_page = requests.get("https://www.wikidex.net/wiki/Categor%C3%ADa:Sprites_de_Pok%C3%A9mon")
sprite_page_soup = BeautifulSoup(sprite_page.content, 'html.parser')

game_sprites_link_table = sprite_page_soup.find("table")
games_by_gen = []

for games in game_sprites_link_table.findAll("td"):
    games_by_gen.append(games)

for i in range(len(games_by_gen)):
    # Since arrays start at 0, 5th generation == i at 4
    # So, less than 5th gen (4th iter) are where there are no static sprites
    if (i < 4):
        print(games_by_gen[i].findAll("a"), "\n\n")
    # Seperates static and animated sprite pages
    else:
        for each in games_by_gen[i].findAll('b'):
            if not each.text == '|':
                print(each.text, "\n", each.find_next_siblings("a"), "\n\n")
    #print(gen.findAll('b'))

# TODO: Put below in a conditional to loop if true
#print(game_page_soup.find("a", string="página siguiente"))
# Gets pokemon name and number
pokemon_name_number_dict = {}
for i in range(2, 900):
    pokemon_name_number_dict[cell_value(i, 3)] = cell_value(i, 2)

# Pokemon name : Sprite link
pokemon_sprites_dict = {}
# Gets pokemon names for each image
pokemon_names = []
for name in game_page_soup.find_all(class_="gallerytext"):
    # Doing by file extension because whitespace splits male/female, Mr.Mime, etc
    # TODO: Somehow find file extensions used? Or allow all to pass for split
        # Changes with game
    for poke in pokemon_name_number_dict:
        # TODO: Due to pokes like porygon, porgyon2, porygon-z
            # A porygon iteration will match all 3 first
            # So, either I create a list from the dictionary and knock off names as I go through
            # OR, as I prefer, grab the suffix manually, hardcode it per game, split the string, then match it with the pokemon from excel
        if poke in name.text and not "\(CV\)" in name.text:
            #print(poke)
            pokemon_names.append(poke)
    #pokemon_names.append(name.text.split(' espalda G1.png')[0])
#print(pokemon_names)
# Removing preceding new line character from names
for i in range(len(pokemon_names)):
    name = pokemon_names[i].split('\n')[1]
    # Crude hardcode translation services, at your service
    if "hembra" in name:
        name = name.replace("hembra", "f")
    if "macho" in name:
        name = name.replace("macho", "m")
    pokemon_names[i] = name
# Adding pokedex number before name
for i in range(len(pokemon_names)):
    for poke, num in pokemon_name_number_dict.items():
        if pokemon_names[i] == poke:
            pokemon_names[i] = num + " " + pokemon_names[i]
            break
# Regex checker to make sure each name is formatted properly
for name in pokemon_names:
    if re.search("^\d\d\d\s[a-zA-Z]+", name):
        continue
    else:
        print(name, "is not formatted correctly")

# Gets link to pokemon sprite image
pokemon_img_link = []
for sprite in game_page_soup.find_all(class_="gallerybox"):
    pokemon_img_link.append(sprite.a.img["src"])

for i in range(len(pokemon_names)):
    # Excludes japanese versions 
    # TODO: Allow any file extension after the period
    if "\(CV\)" in pokemon_names[i]:
        print(pokemon_names[i], "omitted bc japanese variant")
    else:
        pokemon_sprites_dict[pokemon_names[i]] = pokemon_img_link[i]
    # TODO: Change filename to accomodate for game
    file_name = "Images/Pokemon/" + pokemon_names[i] + " Gen1-Back.png"
    # Saves file
    #urllib.request.urlretrieve(pokemon_img_link[i], file_name)

#print(pokemon_sprites_dict)