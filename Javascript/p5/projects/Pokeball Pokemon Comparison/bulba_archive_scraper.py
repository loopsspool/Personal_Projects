import requests # To retrieve webpages
from bs4 import BeautifulSoup   # To parse webpages
import re   # For filtering what images to download
import urllib   # For downloading those images to my computer
import os   # For downloading those images to my computer
from PIL import Image   # For converting URL image data to PIL Image object 
import xlrd     # For reading excel workbook

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


def check_if_animated(link):
    # Converting URL image to PIL Image Object
    img = Image.open(requests.get(link, stream = True).raw)
    # Checking if it is an animated image
    return(img.is_animated)


def get_largest_png(img):
    # If multiple sized images, grab the largest
    try:
        # Sourceset is a string of urls seperated by a comma
            # This breaks that into a list and takes the last (and largest) png url
        srcset = img['srcset'].split(",")
        src = srcset[len(srcset) - 1]
    # If there's only one photo, theres no srcset and that's the largest
    except:
        src = img['src']

    return (src)

def get_img_from_string(img, s, save_path):
    if re.search(s, img.attrs['alt']) != None:
        save_img = get_largest_png(img)
        # urllib.request.urlretrieve(save_img, save_path)

# Gets pokemon info from excel sheet
class Pokemon:
    def __init__(self, name, number, gen, has_f_var, has_mega, has_giganta, reg_forms, has_type_forms, has_misc_forms, is_in_gen8):
        self.name = name
        self.number = number
        self.gen = gen
        self.has_f_var = has_f_var
        self.has_mega = has_mega
        self.has_giganta = has_giganta
        self.reg_forms = reg_forms
        self.has_type_forms = has_type_forms
        self.has_misc_forms = has_misc_forms
        self.is_in_gen8 = is_in_gen8

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
gen8_col = get_col_number("Available in Gen 8")

# Adds pokemon info from spreadsheet to object array
print("Getting pokemon info from spreadsheet...")
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
    is_in_gen8 = isnt_empty(i, gen8_col)

    pokedex.append(Pokemon(name, num, gen, has_f_var, has_mega, has_giganta, reg_forms, has_type_forms, has_misc_forms, is_in_gen8))

# Origin page (list of pokes by national pokedex)
starter_url = "https://archives.bulbagarden.net"
pokemon_starter_page = requests.get("https://archives.bulbagarden.net/wiki/Category:Pok%C3%A9mon_artwork")
pokemon_starter_page_soup = BeautifulSoup(pokemon_starter_page.content, 'html.parser')
save_path = "C:\\Users\\ejone\\OneDrive\\Desktop\\Code\\Javascript\\p5\\projects\\Pokeball Pokemon Comparison\\Images\\Pokemon"


pokemon_img_urls = []
curr_page_soup = pokemon_starter_page_soup
print("Starting reading of pokemon archive links...")

# Loops through pages of archives of pokemon images
while True:
    # Grabbing each individual pokemons archived image url
    for list_div in curr_page_soup.find_all('div', {'class': 'mw-category-group'}):
        for poke in list_div.find_all('li'):
            # Skipping specific artwork I don't want
            if poke.a.get('href') == "/wiki/Category:Ken_Sugimori_Pok%C3%A9mon_artwork" or poke.a.get('href') == "/wiki/Category:Official_Pok%C3%A9mon_artwork":
                continue
            pokemon_img_urls.append(poke.a.get('href'))

    # Only gets first page of pokemon archive links
    break

    # Moving on to the next page
    try:
        next_page_url = curr_page_soup.find('a', string='next page').get('href')
        next_page = requests.get(starter_url + next_page_url)
        next_page_soup = BeautifulSoup(next_page.content, 'html.parser')
        curr_page_soup = next_page_soup
        print("Reading next page of pokemon archive links...")
    # Unless the end of the next pages is reached
    except:
        print("Reached end of pokemon archive links.")
        break


#print(pokemon_img_urls)
print("Processing images...")
for i in range(len(pokemon_img_urls)):
    # Getting relevant pokemon data
    pokemon = pokedex[i]
    save_name = pokemon.number + " " + pokemon.name
    if pokemon.name == "Type: Null":
        save_name = pokemon.number + " Type Null"
    # Getting pokemon archived image page information
    pokemon_starter_page = requests.get(starter_url + pokemon_img_urls[i])
    pokemon_starter_page_soup = BeautifulSoup(pokemon_starter_page.content, 'html.parser')
    pokemon_imgs = pokemon_starter_page_soup.find_all('img')
    # Downloading certain images
    for img in pokemon_imgs:
        print(img["alt"], "\n\n")

    break
        # DRAWN IMAGES
        # Drawn standard
        get_img_from_string(img, "^\d\d\d[a-zA-Z].png", save_path + "\\Drawn\\" + save_name)
        # Drawn Mega
        if pokemon.has_mega:
            if pokemon.name == "Charizard" or pokemon.name == "Mewtwo":
                get_img_from_string(img, "^\d\d\d[a-zA-Z]-Mega X.png")
                get_img_from_string(img, "^\d\d\d[a-zA-Z]-Mega Y.png")
            else:
                get_img_from_string(img, "^\d\d\d[a-zA-Z]-Mega.png")
        # Gigantamax
        if pokemon.has_giganta:
            get_img_from_string(img, "^\d\d\d[a-zA-Z]-Gigantamax.png")
        # Regional forms
        if pokemon.reg_forms != "":
            if "," in pokemon.reg_forms:
                get_img_from_string(img, "^\d\d\d[a-zA-Z]-Alola.png")
                get_img_from_string(img, "^\d\d\d[a-zA-Z]-Galar.png")
            else:
                get_img_from_string(img, "^\d\d\d[a-zA-Z]-" + pokemon.reg_forms + ".png")
        # TODO: Fill in for custom form drawings
        # Custom type forms
        # Pikachu Cosplay & Caps
        if pokemon.name == "Pikachu":
            get_img_from_string(img, )
            get_img_from_string(img, )
            get_img_from_string(img, )
            get_img_from_string(img, )
            get_img_from_string(img, )
            get_img_from_string(img, )
            get_img_from_string(img, )
            get_img_from_string(img, )
            get_img_from_string(img, )
            get_img_from_string(img, )
            get_img_from_string(img, )
            get_img_from_string(img, )
            get_img_from_string(img, )

            # Spiky-eared Pichu
            get_img_from_string(img, )

            # Unown Characters
            if "Unown" in split_name:
                # Default sprite image for unown is Unown A, so skip in favor of A
                if "Unown" == split_name:
                    continue
                # Get last character (Unown form)
                form = " " + split_name[-1]
                # This splices just Unown name (since ? and ! don't have spaces but the characters do)
                split_name = split_name[0:5]
                # Can't have question marks in file names on Windows
                if form == " ?":
                    form = " Q-Mark"

            # Castform Weathers
            get_img_from_string(img, )
            get_img_from_string(img, )
            get_img_from_string(img, )

            # Primal Kyogre & Groudon
            get_img_from_string(img, )
            get_img_from_string(img, )

            # Deoxys
            get_img_from_string(img, )
            get_img_from_string(img, )
            get_img_from_string(img, )
            # Deoxys only available in FRLG as defense or attack form dependent on game
                # Split must work fine for leading characters, but not trailing. Hence this workaround of sorts
            if names[i].text.startswith("\nDeoxys defensa"):
                form = " Defense"
                split_name = names[i].text.split(" defensa")[0]
                split_name = split_name.split("\n")[1]

            # Burmy & Wormadam Cloaks
            get_img_from_string(img, )
            get_img_from_string(img, )
            get_img_from_string(img, )
            get_img_from_string(img, )
            get_img_from_string(img, )
            get_img_from_string(img, )

            # Cherrim
            get_img_from_string(img, )
            get_img_from_string(img, )

            # Shellos & Gastrodon East/West
                # Done a lil differently since "este" (East) is contained in "oeste" (West)
            if "Shellos" in split_name or "Gastrodon" in split_name:
                if "oeste" in split_name:
                    form = " West"
                    split_name = split_name.split(" oeste")[0]
                else:
                    form = " East"
                    split_name = split_name.split(" este")[0]

            # Rotom Appliances
            get_img_from_string(img, )
            get_img_from_string(img, )
            get_img_from_string(img, )
            get_img_from_string(img, )
            get_img_from_string(img, )

            # Giratina
            get_img_from_string(img, )
            get_img_from_string(img, )

            # Shaymin
            get_img_from_string(img, )
            get_img_from_string(img, )

            # Arceus Types
            if "Arceus" == split_name:
                form = " Normal"
            if "Arceus" in split_name and split_name != "Arceus":
                type_form_translate_split()

            # Basculin Stripes
            get_img_from_string(img, )
            get_img_from_string(img, )

            # Darmanitan Modes
            if "Darmanitan" == split_name:
                form = "Standard"
            else:
                get_img_from_string(img, )

            # Deerling & Sawsbuck Seasons
            get_img_from_string(img, )
            get_img_from_string(img, )
            get_img_from_string(img, )
            get_img_from_string(img, )
            get_img_from_string(img, )
            get_img_from_string(img, )
            get_img_from_string(img, )
            get_img_from_string(img, )

            # Forces of nature forms
            get_img_from_string(img, )
            get_img_from_string(img, )
            get_img_from_string(img, )
            get_img_from_string(img, )
            get_img_from_string(img, )
            get_img_from_string(img, )

            # Kyurem Fusions
            if "negro" in split_name:
                if "activo" in split_name:
                    get_img_from_string(img, )
                if "inactivo" in split_name:
                    get_img_from_string(img, )
                if split_name == "Kyurem negro":
                    get_img_from_string(img, )
            if "blanco" in split_name:
                if "activo" in split_name:
                    get_img_from_string(img, )
                if "inactivo" in split_name:
                    get_img_from_string(img, )
                if split_name == "Kyurem blanco":
                    get_img_from_string(img, )
            
            # Keldeo
            if "Keldeo" in split_name and "brío" in split_name:
                get_img_from_string(img, )
            else:
                if "Keldeo" == split_name:
                    form = " Ordinary"

            # Meloetta
            get_img_from_string(img, )
            get_img_from_string(img, )

            # Genesect
            get_img_from_string(img, )
            get_img_from_string(img, )
            get_img_from_string(img, )
            get_img_from_string(img, )
            # Website named Genesect differenlt in gen8:
            get_img_from_string(img, )
            get_img_from_string(img, )
            get_img_from_string(img, )
            get_img_from_string(img, )

            # Ash Greninja
            get_img_from_string(img, )

            # Vivillon Patterns
            get_img_from_string(img, )
            get_img_from_string(img, )
            get_img_from_string(img, )
            get_img_from_string(img, )
            get_img_from_string(img, )
            get_img_from_string(img, )
            get_img_from_string(img, )
            get_img_from_string(img, )
            get_img_from_string(img, )
            get_img_from_string(img, )
            get_img_from_string(img, )
            get_img_from_string(img, )
            get_img_from_string(img, )
            get_img_from_string(img, )
            get_img_from_string(img, )
            get_img_from_string(img, )
            get_img_from_string(img, )
            get_img_from_string(img, )
            get_img_from_string(img, )
            get_img_from_string(img, )


            # Flabebe, Floette, and Florges colors
            # Unused form in XY
            if "Floette" in split_name and "eterna" in split_name:
                continue
            get_img_from_string(img, )
            get_img_from_string(img, )
            get_img_from_string(img, )
            get_img_from_string(img, )
            get_img_from_string(img, )
            get_img_from_string(img, )
            get_img_from_string(img, )
            get_img_from_string(img, )
            get_img_from_string(img, )
            get_img_from_string(img, )
            get_img_from_string(img, )
            get_img_from_string(img, )
            get_img_from_string(img, )
            get_img_from_string(img, )
            get_img_from_string(img, )

            # Furfrou Trims
            get_img_from_string(img, )
            get_img_from_string(img, )
            get_img_from_string(img, )
            get_img_from_string(img, )
            get_img_from_string(img, )
            get_img_from_string(img, )
            get_img_from_string(img, )
            get_img_from_string(img, )
            get_img_from_string(img, )

            # Aegislash
            get_img_from_string(img, )
            get_img_from_string(img, )

            # Pumpkaboo and Gourgeist Sizes
            if "Pumpkaboo" == split_name or "Gourgeist" == split_name:
                # Average sizes have no indication in filename on this website
                form = " 1Average Size"
            else:
                get_img_from_string(img, )
                get_img_from_string(img, )
                get_img_from_string(img, )
                get_img_from_string(img, )
                get_img_from_string(img, )
                get_img_from_string(img, )

            # Xerneas
            if "Xerneas" == split_name:
                form = " Active"
            else:
                get_img_from_string(img, )

            # Zygarde
            # Cells & Nuclei aren't really sprites, so continue
            if split_name == "Zygarde célula" or split_name == "Zygarde núcleo":
                continue
            if "Zygarde" == split_name:
                form = " 50%"
            else:
                get_img_from_string(img, )
                get_img_from_string(img, )

            # Hoopa
            if "Hoopa" == split_name:
                form = " Confined"
            else:
                get_img_from_string(img, )

            # Oricorio
            get_img_from_string(img, )
            get_img_from_string(img, )
            get_img_from_string(img, )
            get_img_from_string(img, )

            # Lycanroc
            get_img_from_string(img, )
            get_img_from_string(img, )
            get_img_from_string(img, )

            # Wishiwashi
            get_img_from_string(img, )
            get_img_from_string(img, )

            # Silvally Types
            if "Silvally" == split_name:
                form = " Normal"
            if "Silvally" in split_name and split_name != "Silvally":
                type_form_translate_split()

            # Minior
            get_img_from_string(img, )
            get_img_from_string(img, )
            get_img_from_string(img, )
            get_img_from_string(img, )
            get_img_from_string(img, )
            get_img_from_string(img, )
            get_img_from_string(img, )
            get_img_from_string(img, )
            # Shiny cores all the same color?
            get_img_from_string(img, )

            # Mimikyu
            if "Mimikyu" == split_name:
                form = " Disguised"
            else:
                get_img_from_string(img, )

            # Necrozma
            get_img_from_string(img, )
            get_img_from_string(img, )
            if "Ultra-Necrozma" == split_name:
                form = " Ultra"
                split_name = split_name.split("Ultra-")[1]

            # Magearna
            get_img_from_string(img, )

            # Cramorant
            get_img_from_string(img, )
            get_img_from_string(img, )

            # Toxtricity
            get_img_from_string(img, )
            get_img_from_string(img, )

            # Alcremie Creams & Sweets
            # Default Alcremie is Vanilla Cream-Strawberry Sweet, so continue
            if "Alcremie" == split_name:
                continue
            if "Alcremie" in split_name:
                # Ends with, not in because sweet names overlap with come Cream names
                if split_name.endswith("corazón") and not "crema de té corazón" in split_name:
                    form = "Love Sweet"
                if split_name.endswith("estrella"):
                    form = "Star Sweet"
                if split_name.endswith("flor"):
                    form = "Flower Sweet"
                if split_name.endswith("fruto"):
                    form = "Berry Sweet"
                if split_name.endswith("lazo"):
                    form = "Ribbon Sweet"
                if split_name.endswith("trébol"):
                    form = "Clover Sweet"

                if "crema de limón" in split_name:
                    form_translate_split("Alcremie", "crema de limón", "Lemon Cream-" + form)
                if "crema de menta" in split_name:
                    form_translate_split("Alcremie", "crema de menta", "Mint Cream-" + form)
                # Site left out most of the corazón, so I left it out too since theres no te anywhere else
                if "crema de té" in split_name:
                    form_translate_split("Alcremie", "crema de té", "Matcha Cream-" + form)
                if "crema de vainilla" in split_name:
                    form_translate_split("Alcremie", "crema de vainilla", "Vanilla Cream-" + form)
                if "crema rosa" in split_name:
                    form_translate_split("Alcremie", "crema rosa", "Ruby Cream-" + form)
                if "crema salada" in split_name:
                    form_translate_split("Alcremie", "crema salada", "Salted Cream-" + form)
                if "mezcla caramelo" in split_name:
                    form_translate_split("Alcremie", "mezcla caramelo", "Caramel Swirl-" + form)
                if "mezcla rosa" in split_name:
                    form_translate_split("Alcremie", "mezcla rosa", "Ruby Swirl-" + form)
                if "tres sabores" in split_name:
                    form_translate_split("Alcremie", "tres sabores", "Rainbow Swirl-" + form)

                # On website there is no notation if it is Strawberry sweet form, so adding that here
                if form.endswith("-"):
                    form += "Strawberry Sweet"
            # Since shiny Alcremies all have the same base color, split name by sweet
            if game.endswith("Shiny"):
                get_img_from_string(img, )
                get_img_from_string(img, )
                get_img_from_string(img, )
                get_img_from_string(img, )
                get_img_from_string(img, )
                get_img_from_string(img, )


            # Eiscue
            if "Eiscue" == split_name:
                form = "Ice Face"
            else:
                get_img_from_string(img, )

            # Morpeko
            if "Morpeko" == split_name:
                form = "Full Belly"
            else:
                get_img_from_string(img, )

            # Zacian and Zamazenta
            if "Zacian" == split_name:
                form = "Hero of Many Battles"
            else:
                get_img_from_string(img, )
            if "Zamazenta" == split_name:
                form = "Hero of Many Battles"
            else:
                get_img_from_string(img, )

            # Eternatus Eternamax
            get_img_from_string(img, )

            # Urshifu
            get_img_from_string(img, )
            get_img_from_string(img, )

            # Zarude
            get_img_from_string(img, )

            # Calyrex Ridings
            get_img_from_string(img, )
            get_img_from_string(img, )

        

# TODO: For Diamond/Pearl, PLatinum, and HGSS check if it's animated
    # If not, open page and see if there's a file history denoted "animated" or "APNG"
# page = requests.get("https://archives.bulbagarden.net/wiki/File:Spr_4h_006_s.png")
# page_soup = BeautifulSoup(page.content, 'html.parser')

# # Get Largest Image possible
# # Inside page
# img_link = "https:" + get_largest_png(page_soup.find(class_ = "fullImageLink").img)
# is_animated = check_if_animated(img_link)


    #print(img.attrs['alt'])