import requests     # For fetching HTML
from bs4 import BeautifulSoup   # For parsing HTML
import xlrd     # For reading excel data (female, forms, etc)
import urllib.request      # For saving images
import re   # To check each name is formatted properly
import time     # To simulate a pause between each page opening

# SPREADSHEET DATA
pokemon_info = xlrd.open_workbook('C:\\Users\\ejone\\OneDrive\\Desktop\\Code\\Javascript\\p5\\projects\\Pokeball Pokemon Comparison\\Pokemon Info.xls')
sheet = pokemon_info.sheet_by_index(0)

def cell_value(row, col):
    return (sheet.cell_value(row, col))

def isnt_empty(row, col):
    return (str(cell_value(row, col)) != "")

def is_empty(row, col):
    return (cell_value(row, col) == empty_cell.value)

# Returns column number from column name
def get_col_number(col_name):
    for col in range(sheet.ncols):
        if (cell_value(1, col) == col_name):
            return col


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
    # Because emerald sprites are default animated from this site
        # Will save first frame later for statics    
    if s == "Esmeralda":
        return("Emerald Animated")
    if s == "Rojo Fuego y Verde Hoja":
        return("FireRed-LeafGreen")
    # Because DPP & HGSS sprites are default static on this site
        # Will retrieve animated sprites from bulbagarden archives
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

    # Excludes Let's Go because there's not enough sprites to justify it's inclusion
    # And Gen8 Shiny Back sprites because the page isn't uploaded yet
    if not "Let's Go" in keyname and not keyname == "Gen8-Back Static Shiny":
        sprites_link_dict[keyname] = "https://www.wikidex.net" + link.get("href")

# Gets rows (games) of sprite link table
for games in game_sprites_link_table.findAll("td"):
    games_by_gen.append(games)

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

# for k,v in sprites_link_dict.items():
#     print(k, ":", v, "\n\n")

split_seperators_by_game = {
    "Gen1 Red-Green": " V",
    "Gen1 Red-Blue": " RA",
    "Gen1 Yellow": " A",
    "Gen1-Back": " espalda",
    "Gen2 Gold": " oro",
    "Gen2 Gold Shiny": " oro",
    "Gen2 Silver": " plata",
    "Gen2 Silver Shiny": " plata",
    "Gen2 Crystal Animated": " cristal",
    "Gen2 Crystal Animated Shiny": " cristal",
    "Gen2-Back": " espalda",
    "Gen2-Back Shiny": " espalda",
    "Gen3 Ruby-Sapphire": " RZ",
    "Gen3 Ruby-Sapphire Shiny": " RZ",
    "Gen3 Emerald Animated": " E",
    "Gen3 Emerald Animated Shiny": " E",
    "Gen3 FireRed-LeafGreen": "RFVH",
    "Gen3 FireRed-LeafGreen Shiny": "RFVH",
    "Gen3-Back": " espalda",
    "Gen3-Back Shiny": " espalda",
    "Gen4 Diamond-Pearl Static": " DP",
    "Gen4 Diamond-Pearl Static Shiny": " DP",
    "Gen4 Platinum Static": " Pt",
    "Gen4 Platinum Static Shiny": " Pt",
    "Gen4 HGSS Static": " HGSS",
    "Gen4 HGSS Static Shiny": " HGSS",
    "Gen4-Back": " espalda",
    "Gen4-Back Shiny": " espalda",
    "Gen5 Black-White Static": " NB",
    "Gen5 Black-White Static Shiny": " NB",
    "Gen5 Black2-White2 Static": " N2B2",
    "Gen5 Black2-White2 Static Shiny": " N2B2",
    "Gen5-Back Static": " espalda",
    "Gen5-Back Static Shiny": " espalda",
    "Gen5 Black-White Animated": " NB",
    "Gen5 Black-White Animated Shiny": " NB",
    "Gen5 Black2-White2 Animated": " N2B2",
    "Gen5 Black2-White2 Animated Shiny": " N2B2",
    "Gen5-Back Animated": " espalda",
    "Gen5-Back Animated Shiny": " espalda",
    "Gen6 XY Static": " XY",
    "Gen6 XY Static Shiny": " XY",
    "Gen6 ORAS Static": " ROZA",
    "Gen6 ORAS Static Shiny": " XY",
    "Gen6-Back Static": " espalda",
    "Gen6-Back Static Shiny": " espalda",
    "Gen6 XY Animated": " XY",
    "Gen6 XY Animated Shiny": " XY",
    "Gen6 ORAS Animated": " ROZA",
    "Gen6 ORAS Animated Shiny": " ROZA",
    "Gen6-Back Animated": " espalda",
    "Gen6-Back Animated Shiny": " espalda",
    "Gen7 Sun-Moon Static": " SL",
    "Gen7 Sun-Moon Static Shiny": " SL",
    "Gen7 USUM Static": " USUL",
    "Gen7 USUM Static Shiny": " USUL",
    "Gen7-Back Static": " espalda",
    "Gen7-Back Static Shiny": " espalda",
    "Gen7 Sun-Moon Animated": " SL",
    "Gen7 Sun-Moon Animated Shiny": " SL",
    "Gen7 USUM Animated": " USUL",
    "Gen7 USUM Animated Shiny": " USUL",
    "Gen7-Back Animated": " espalda",
    "Gen7-Back Animated Shiny": " espalda",
    "Gen8 Sword-Shield Static": " EpEc",
    "Gen8 Sword-Shield Static Shiny": " EpEc",
    "Gen8-Back Static": " espalda",
    "Gen8 Sword-Shield Animated": " EpEc",
    "Gen8 Sword-Shield Animated Shiny": " EpEc",
    "Gen8-Back Animated": " espalda",
    "Gen8-Back Animated Shiny": " espalda"
}
# Gets pokemon info from excel sheet
class Pokemon:
    def __init__(self, name, number, gen, has_f_var, has_mega, has_giganta, reg_forms, has_type_forms, has_misc_forms):
        self.name = name
        self.number = number
        self.gen = gen
        self.has_f_var = has_f_var
        self.has_mega = has_mega
        self.has_giganta = has_giganta
        self.reg_forms = reg_forms
        self.has_type_forms = has_type_forms
        self.has_misc_forms = has_misc_forms

# Gets column numbers from spreadsheet
name_col = get_col_number("Name")
num_col = get_col_number("#")
gen_col = get_col_number("Gen")
f_col = get_col_number("Female Variation")
mega_col = get_col_number("Mega")
giganta_col = get_col_number("Gigantamax")
reg_forms_col = get_col_number("Regional Forms")
type_forms_col = get_col_number("Type Forms")
misc_forms_col = get_col_number("Misc Forms")

# Adds pokemon info from spreadsheet to object array
pokedex = []
for i in range(2, 900):
    name = cell_value(i, name_col)
    num = cell_value(i, num_col)
    gen = int(cell_value(i, gen_col))
    has_f_var = isnt_empty(i, f_col)
    has_mega = isnt_empty(i, mega_col)
    has_giganta = isnt_empty(i, giganta_col)
    reg_forms = cell_value(i, reg_forms_col)
    has_type_forms = isnt_empty(i, type_forms_col)
    has_misc_forms = isnt_empty(i, misc_forms_col)

    pokedex.append(Pokemon(name, num, gen, has_f_var, has_mega, has_giganta, reg_forms, has_type_forms, has_misc_forms))

# Prints out each pokemon's relevant info from spreadsheet
# for i in range(len(pokedex)):
#     print(vars(pokedex[i]))

outlier_sprites = []
for game, link in sprites_link_dict.items():
    # Getting soup of the corresponding sprite page
    game_page = requests.get(link)
    game_page_soup = BeautifulSoup(game_page.content, 'html.parser')

    # Inside for loop to clear for each game
    pokemon_img_dict = {}

    current_gen = re.findall("Gen\d", game)[0][-1]
    # Loops through pages of sprites collecting image links to download
    # No do-while loop in python, so running a while True loop with a break condition
        # This break condition being if there is not a next page
    while True:
        # Gets images and captions on page
        names = game_page_soup.find_all(class_="gallerytext")
        imgs = game_page_soup.find_all(class_="gallerybox")
        for i in range(len(names)):
            # If japanese sprites, 3d ones, or game blocks skip em
            if "\(CV\)" in names[i].text or "Japón" in names[i].text or "3D" in names[i].text or "Bloque" in names[i].text:
                continue
            file_ext = names[i].text.split("\n")[1]
            file_ext = file_ext[len(file_ext)-4 : len(file_ext)]

            # Crude hardcode translation services, at your service
            # Done before split because in their naming convention they put genders after the game (which is the split seperator)
            gender = ""
            if "hembra" in names[i].text or "macho" in names[i].text:
                if "hembra" in names[i].text:
                    gender = " f"
                if "macho" in names[i].text:
                    gender = " m"

            # Removing game, file size, extension, etc
            # This conditional is due to the websites oversight-- Most on the page are XY Static shinies
                # Except mostly the Megas, hence the exception. The rest I will do by hand
            if game == "Gen6 ORAS Static Shiny" and names[i].startswith("Mega-"):
                split_name = names[i].text.split(" ROZA")[0]
            else:
                split_name = names[i].text.split(split_seperators_by_game[game])[0]
            # Removing leading newline character
            split_name = split_name.split("\n")[1]
            # Handling Nidoran, the only pokemon where this is the case
            if "Nidoran" in split_name and gender != "":
                if gender == " f":
                    split_name = split_name.replace("hembra", "f")
                if gender == " m":
                    split_name = split_name.replace("macho", "m")
            # TODO: Maybe handle type forms? At least Arceus?
            # TODO: Definitely Unown too
            # TODO: Shaymin & Shellos Evos
                # Pretty much any variations in earlier games should be taken care of
                    # Otherwise they compound over the generations (+shiny, animated, and back!)
            # Handling Mega evolutions
            mega = ""
            if split_name.startswith("Mega"):
                mega = " Mega"
                split_name = split_name.split("Mega-")[0]
                if split_name.endswith("X"):
                    mega = " MegaX"
                    split_name = split_name.split(" X")[0]
                if split_name.endswith("Y"):
                    mega = " MegaY"
                    split_name = split_name.split(" Y")[0]
            # Handling Gigantamax
            giganta = ""
            if split_name.endswith("Gigamax"):
                giganta = " Gigantamax"
                split_name = split_name.split(" Gigamax")
            # Handling regions
            region = ""
            if split_name.endswith("de Alola"):
                region = " Alolan"
                split_name = split_name.split(" de Alola")
            if split_name.endswith("de Galar"):
                region = " Galarian"
                split_name = split_name.split(" de Galar")

            # TODO: Combine BW & B2W2, 
            #               XY & ORAS, 
            #               Sun-Moon & UltraSun-UltraMoon
            # Since the latters all only have supplemental pokes to the formers
            match = False
            for poke in pokedex:
                if poke.name == split_name:
                    match = True
                    filename = poke.number + " " + poke.name + " " + game + gender + mega + giganta + region
                    # If the filename already exists (and it will for double sprites in DPP), add alt
                    # TODO: Confirm this works lol
                    try:
                        dummy = pokemon_img_dict[filename + file_ext]
                        filename += " alt"
                    except:
                        dummy = "key doesn't exist yet, continue"
                    filename += file_ext
                    pokemon_img_dict[filename] = imgs[i].a.img["src"]
                    # Saves first-frame statics as png from gif for Crystal & Emerald
                    if game == "Gen2 Crystal Animated" or game == "Gen2 Crystal Animated Shiny" or game == "Gen3 Emerald Animated" or game == "Gen3 Emerald Animated Shiny":
                        filename = filename.replace("Animated", "Static")
                        filename = filename.replace(".gif", ".png")
                        pokemon_img_dict[filename] = imgs[i].a.img["src"]
            # This is mainly for pokemon with different forms
                # I will rewrite them by hand since it would take just as long as hardcoding each one
            if match == False:
                outlier_sprites.append(names[i].text.split("\n")[1])
                pokemon_img_dict[names[i].text.split("\n")[1]] = imgs[i].a.img["src"]
                    
        # for k,v in pokemon_img_dict.items():
        #     print(k, ":", v)
        
        # If next game page exists, get its url to parse
        if game_page_soup.find("a", string="página siguiente") != None:
            game_page = game_page_soup.find("a", string="página siguiente").get("href")
            game_page = requests.get("https://www.wikidex.net" + game_page)
            game_page_soup = BeautifulSoup(game_page.content, 'html.parser')
        else:
            # If done with all images for the game, save them
            for k,v in pokemon_img_dict.items():
                print(k, ":", v)
            print(len(outlier_sprites), "outlier pokes: ", outlier_sprites)
            print("\n\n\n")
            #urllib.request.urlretrieve(pokemon_img_link[i], file_name)
            time.sleep(10)
            break
    

print(len(outlier_sprites), "outlier pokes: ", outlier_sprites)