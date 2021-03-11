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

# Crude translations due to the page being in spanish lol
def game_translate(s):
    if s == "Rojo y Azul":
        return("Red-Blue")
    if s == "Verde":
        return("Red-Green")
    if s == "Amarillo":
        return("Yellow")
    if s == "Oro":
        return("Gold")
    if s == "Plata":
        return("Silver")
    # Because crystal sprites are default animated from this site
        # Will save first frame later for statics
    if s == "Cristal":
        return("Crystal Animated")
    if s == "Rubí y Zafiro":
        return("Ruby-Sapphire")
    # Because Emerald, DPP, HGSS sprites are default static on this site
        # Will retrieve animated sprites from bulbagarden archives
    if s == "Esmeralda":
        return("Emerald Static")
    if s == "Rojo Fuego y Verde Hoja":
        return("FireRed-LeafGreen")
    if s == "Diamante y Perla":
        return("Diamond-Pearl Static")
    if s == "Platino":
        return("Platinum Static")
    if s == "Oro HeartGold y Plata SoulSilver":
        return("HGSS Static")
    if s == "Negro y Blanco":
        return("Black-White")
    if s == "Negro y Blanco 2":
        return("Black2-White2")
    if s == "X y Pokémon Y":
        return("XY")
    if s == "Rubí Omega y Pokémon Zafiro Alfa":
        return("ORAS")
    if s == "Sol y Pokémon Luna":
        return("Sun-Moon")
    if s == "Ultrasol y Pokémon Ultraluna":
        return("USUM")
    if s == "Let's Go, Pikachu! y Pokémon Let's Go, Eevee!":
        return("Let's Go")
    if s == "Espada y Pokémon Escudo":
        return("Sword-Shield")

def get_game(a):
    # From titles, not text, so shiny pokemon (who's text is V) can still get the game
    title = a["title"].split("Pokémon ", 1)[1]
    title = game_translate(title)
    return(title)

sprites_link_dict = {}
# Template for file naming, also easy access to each game sprites link
def sprite_link_dict_entry(gen, link, animated = False):
    back = False
    shiny = False

    # Get game if link isn't to back sprites (since those are generationally recycled)
    if not link.text == "E" and not link.text == "EV":
        game = get_game(link)
    # Getting shiny, back parameters
    if link.text == "V":
        shiny = True
    if link.text == "E":
        back = True
    if link.text == "EV":
        back = True
        shiny = True

    keyname = ""
    # No animated sprites below gen 5 on this website
        # Except for Crystal, which the tag was added in game_translate
    if gen < 5:
        if back == False and shiny == False:
            keyname = "Gen" + str(gen) + " " + game
        if back == False and shiny == True:
            keyname = "Gen" + str(gen) + " " + game + " Shiny"
        if back == True and shiny == False:
            keyname = "Gen" + str(gen) + "-Back"
        if back == True and shiny == True:
            keyname = "Gen" + str(gen) + "-Back Shiny"
    else:
        if animated == True:
            if back == False and shiny == False:
                keyname = "Gen" + str(gen) + " " + game + " Animated"
            if back == False and shiny == True:
                keyname = "Gen" + str(gen) + " " + game + " Animated" + " Shiny"
            if back == True and shiny == False:
                keyname = "Gen" + str(gen) + "-Back" + " Animated"
            if back == True and shiny == True:
                keyname = "Gen" + str(gen) + "-Back Animated Shiny"
        if animated == False:
            if back == False and shiny == False:
                keyname = "Gen" + str(gen) + " " + game + " Static"
            if back == False and shiny == True:
                keyname = "Gen" + str(gen) + " " + game + " Static" + " Shiny"
            if back == True and shiny == False:
                keyname = "Gen" + str(gen) + "-Back" + " Static"
            if back == True and shiny == True:
                keyname = "Gen" + str(gen) + "-Back Static Shiny"

    sprites_link_dict[keyname] = link

# Gets rows (games) of sprite link table
for games in game_sprites_link_table.findAll("td"):
    games_by_gen.append(games)

# TODO: Exclude Let's Go
for i in range(len(games_by_gen)):
    current_gen = i + 1
    current_game = ""
    # No animated sprites below gen5, so just get statics
    if (current_gen < 5):
        # Grabbing links and adding them to the dict
        for link in games_by_gen[i].findAll("a"):
            sprite_link_dict_entry(current_gen, link)

    # Seperates static and animated sprite pages gen 5 and above
    else:
        for image_type in games_by_gen[i].findAll('b'):
            # Excludes game seperators
            if not image_type.text == '|':
                # Gets animated or static
                if image_type.text == "Estáticos:":
                    is_animated = False
                if image_type.text == "Animados:":
                    is_animated = True
                # Grabbing links and adding them to the dict
                for link in image_type.find_next_siblings("a"):
                    sprite_link_dict_entry(current_gen, link, is_animated)

for k,v in sprites_link_dict.items():
    print(k, ":", v, "\n")

# No do-while loop in python, so running a while True loop with a break condition
#while True:
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