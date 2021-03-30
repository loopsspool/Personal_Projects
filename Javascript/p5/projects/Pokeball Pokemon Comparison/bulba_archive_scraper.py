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
        print(s, " --- ", save_path)
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
save_path_starter = "C:\\Users\\ejone\\OneDrive\\Desktop\\Code\\Javascript\\p5\\projects\\Pokeball Pokemon Comparison\\Images\\Pokemon"
drawn_save_path = save_path_starter + "\\Drawn\\"
game_save_path = save_path_starter + "\\Game Sprites\\"

pokemon_img_urls = []
curr_page_soup = pokemon_starter_page_soup
print("Starting reading of pokemon archive links...")

page_index = 0
# Loops through pages of archives of pokemon images
while True:
    # Stopping after a certain page for testing
    # if page_index == 2:
    #     break
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
        page_index += 1
        print("Reading next page of pokemon archive links...")
    # Unless the end of the next pages is reached
    except:
        print("Reached end of pokemon archive links.")
        break

# TODO: Create dict checklist for each of the type of images you want
    # When they're all fulfilled, break so unecessary image processing for each poke isn't occuring
    # If end of page is reached and requirements aren't satisfied (ie Arceus), continue to next page of images
#print(pokemon_img_urls)
print("Processing images...")
for i in range(len(pokemon_img_urls)):
    # Getting relevant pokemon data
    pokemon = pokedex[i]
    # For only doing certain pokemon
    # if pokemon.name != "Unown":
    #     continue
    # print("Got here")

    save_name = pokemon.number + " " + pokemon.name
    if pokemon.name == "Type: Null":
        save_name = pokemon.number + " Type Null"
    # Getting pokemon archived image page information
    pokemon_starter_page = requests.get(starter_url + pokemon_img_urls[i])
    pokemon_starter_page_soup = BeautifulSoup(pokemon_starter_page.content, 'html.parser')
    pokemon_imgs = pokemon_starter_page_soup.find_all('img')
    # Downloading certain images
    for img in pokemon_imgs:
        #print(img["alt"], "\n\n")

        # DRAWN IMAGES
        # Drawn standard
        get_img_from_string(img, "^\d\d\d[a-zA-Z].png", drawn_save_path + save_name)
        # Drawn Mega
        if pokemon.has_mega:
            if pokemon.name == "Charizard" or pokemon.name == "Mewtwo":
                get_img_from_string(img, "^\d\d\d[a-zA-Z]-Mega X.png", drawn_save_path + save_name + "-Mega_X")
                get_img_from_string(img, "^\d\d\d[a-zA-Z]-Mega Y.png", drawn_save_path + save_name + "-Mega_Y")
            else:
                get_img_from_string(img, "^\d\d\d[a-zA-Z]-Mega.png", drawn_save_path + save_name + "-Mega")
        # Gigantamax
        if pokemon.has_giganta:
            get_img_from_string(img, "^\d\d\d[a-zA-Z]-Gigantamax.png", drawn_save_path + save_name + "-Gigantamax")
        # Regional forms
        if pokemon.reg_forms != "":
            if "," in pokemon.reg_forms:
                get_img_from_string(img, "^\d\d\d[a-zA-Z]-Alola.png", drawn_save_path + save_name + "-Region-Alola")
                get_img_from_string(img, "^\d\d\d[a-zA-Z]-Galar.png", drawn_save_path + save_name + "-Region-Galar")
            else:
                get_img_from_string(img, "^\d\d\d[a-zA-Z]-" + pokemon.reg_forms + ".png", drawn_save_path + save_name + "-Region-" + pokemon.reg_forms)

        # Custom type forms
        # Pikachu Cosplay & Caps
        get_img_from_string(img, "^\d\d\dPikachu-Alola.png", drawn_save_path + save_name + "-Cap-Alola")
        get_img_from_string(img, "^\d\d\dPikachu-Hoenn.png", drawn_save_path + save_name + "-Cap-Hoenn")
        get_img_from_string(img, "^\d\d\dPikachu-Kalos.png", drawn_save_path + save_name + "-Cap-Kalos")
        get_img_from_string(img, "^\d\d\dPikachu-Original.png", drawn_save_path + save_name + "-Cap-Original")
        get_img_from_string(img, "^\d\d\dPikachu-Partner.png", drawn_save_path + save_name + "-Cap-Partner")
        get_img_from_string(img, "^\d\d\dPikachu-Sinnoh.png", drawn_save_path + save_name + "-Cap-Sinnoh")
        get_img_from_string(img, "^\d\d\dPikachu-Unova.png", drawn_save_path + save_name + "-Cap-Unova")
        get_img_from_string(img, "^\d\d\dPikachu-World.png", drawn_save_path + save_name + "-Cap-World")
        get_img_from_string(img, "^\d\d\dPikachu-Belle.png", drawn_save_path + save_name + "-Cosplay-Belle")
        get_img_from_string(img, "^\d\d\dPikachu-Libre.png", drawn_save_path + save_name + "-Cosplay-Libre")
        get_img_from_string(img, "^\d\d\dPikachu-PhD.png", drawn_save_path + save_name + "-Cosplay-PhD")
        get_img_from_string(img, "^\d\d\dPikachu-Pop Star.png", drawn_save_path + save_name + "-Cosplay-Pop_Star")
        get_img_from_string(img, "^\d\d\dPikachu-Rock Star.png", drawn_save_path + save_name + "-Cosplay-Rock_Star")

        # Spiky-eared Pichu
        get_img_from_string(img, "Spiky-eared Pichu DP 1", drawn_save_path + save_name + "-Spiky_Eared")

        # Unown Characters
        if pokemon.name == "Unown":
            # Only drawn forms are dream versions
            if img["alt"].endswith("Dream.png"):
                # Get form
                form = img["alt"].split(" ")[1]
                if form == "Exclamation":
                    form = "!"    
                if form == "Question":
                    form = "Qmark"
                form = "-" + form
                get_img_from_string(img, "^\d\d\dUnown [a-zA-z]+ Dream.png", drawn_save_path + save_name + form)

        # Castform Weathers
        get_img_from_string(img, "^\d\d\dCastform-Rainy.png", drawn_save_path + save_name + "-Rainy")
        get_img_from_string(img, "^\d\d\dCastform-Snowy.png", drawn_save_path + save_name + "-Snowy")
        get_img_from_string(img, "^\d\d\dCastform-Sunny.png", drawn_save_path + save_name + "-Sunny")

        # Primal Kyogre & Groudon
        get_img_from_string(img, "^\d\d\dKyogre-Primal 2.png", drawn_save_path + save_name + "-Primal")
        get_img_from_string(img, "^\d\d\dGroudon-Primal.png", drawn_save_path + save_name + "-Primal")

        # Deoxys
        get_img_from_string(img, "^\d\d\dDeoxys-Attack.png", drawn_save_path + save_name + "-Attack")
        get_img_from_string(img, "^\d\d\dDeoxys-Defense.png", drawn_save_path + save_name + "-Defense")
        get_img_from_string(img, "^\d\d\dDeoxys-Speed.png", drawn_save_path + save_name + "-Speed")

        # Burmy & Wormadam Cloaks
        get_img_from_string(img, "^\d\d\dBurmy-Plant.png", drawn_save_path + save_name + "-Plant")
        get_img_from_string(img, "^\d\d\dBurmy-Sandy.png", drawn_save_path + save_name + "-Sandy")
        get_img_from_string(img, "^\d\d\dBurmy-Trash.png", drawn_save_path + save_name + "-Trash")
        get_img_from_string(img, "^\d\d\dWormadam-Plant.png", drawn_save_path + save_name + "-Plant")
        get_img_from_string(img, "^\d\d\dWormadam-Sandy.png", drawn_save_path + save_name + "-Sandy")
        get_img_from_string(img, "^\d\d\dWormadam-Trash.png", drawn_save_path + save_name + "-Trash")

        # Cherrim
        # TODO: No default image, only overcast and sunny
        get_img_from_string(img, "^\d\d\dCherrim-Overcast.png", drawn_save_path + save_name + "-Overcast")
        get_img_from_string(img, "^\d\d\dCherrim-Sunny.png", drawn_save_path + save_name + "-Sunshine")

        # Shellos & Gastrodon East/West
        # TODO: No default image
        get_img_from_string(img, "^\d\d\dShellos-East.png", drawn_save_path + save_name + "-East")
        get_img_from_string(img, "^\d\d\dShellos-West.png", drawn_save_path + save_name + "-West")
        get_img_from_string(img, "^\d\d\dGastrodon-East.png", drawn_save_path + save_name + "-East")
        get_img_from_string(img, "^\d\d\dGastrodon-West.png", drawn_save_path + save_name + "-West")

        # Rotom Appliances
        get_img_from_string(img, "^\d\d\dRotom-Fan.png", drawn_save_path + save_name + "-Fan")
        get_img_from_string(img, "^\d\d\dRotom-Frost.png", drawn_save_path + save_name + "-Frost")
        get_img_from_string(img, "^\d\d\dRotom-Heat.png", drawn_save_path + save_name + "-Heat")
        get_img_from_string(img, "^\d\d\dRotom-Mow.png", drawn_save_path + save_name + "-Mow")
        get_img_from_string(img, "^\d\d\dRotom-Wash.png", drawn_save_path + save_name + "-Wash")

        # Giratina
        # TODO: No default image
        get_img_from_string(img, "^\d\d\dGiratina-Altered.png", drawn_save_path + save_name + "-Altered")
        get_img_from_string(img, "^\d\d\dGiratina-Origin.png", drawn_save_path + save_name + "-Origin")

        # Shaymin
        # TODO: No default image
        get_img_from_string(img, "^\d\d\dShaymin-Land.png", drawn_save_path + save_name + "-Land")
        get_img_from_string(img, "^\d\d\dShaymin-Sky.png", drawn_save_path + save_name + "-Sky")

        # Arceus Types
        # Only drawn forms are dream versions
        if img["alt"].endswith("Dream.png"):
            # Get form
            form = img["alt"].split(" ")[1]
            form = "-" + form
            get_img_from_string(img, "^\d\d\dArceus [a-zA-z]+ Dream.png", drawn_save_path + save_name + form)

        # Basculin Stripes
        get_img_from_string(img, "^\d\d\dBasculin-Red-Striped_XY_Anime.png", drawn_save_path + save_name + "-Red_Striped")
        get_img_from_string(img, "^\d\d\dBasculin-Blue-Striped_BW_Anime.png", drawn_save_path + save_name + "-Blue_Striped")

        # Darmanitan Modes
        get_img_from_string(img, "^\d\d\dDarmanitan.png", drawn_save_path + save_name + "-Standard")
        get_img_from_string(img, "^\d\d\dDarmanitan-Galar.png", drawn_save_path + save_name + "-Region-Galar-Standard")
        get_img_from_string(img, "^\d\d\dDarmanitan-Zen.png", drawn_save_path + save_name + "-Zen")
        get_img_from_string(img, "^\d\d\dDarmanitan-Galar-Zen.png", drawn_save_path + save_name + "-Region-Galar-Zen")

        # Deerling & Sawsbuck Seasons
        # TODO: No default image
        get_img_from_string(img, "^\d\d\dDeerling-Autumn.png", drawn_save_path + save_name + "-Autumn")
        get_img_from_string(img, "^\d\d\dDeerling-Spring.png", drawn_save_path + save_name + "-Spring")
        get_img_from_string(img, "^\d\d\dDeerling-Summer.png", drawn_save_path + save_name + "-Summer")
        get_img_from_string(img, "^\d\d\dDeerling-Winter.png", drawn_save_path + save_name + "-Winter")
        get_img_from_string(img, "^\d\d\dSawsbuck-Autumn.png", drawn_save_path + save_name + "-Autumn")
        get_img_from_string(img, "^\d\d\dSawsbuck-Spring.png", drawn_save_path + save_name + "-Spring")
        get_img_from_string(img, "^\d\d\dSawsbuck-Summer.png", drawn_save_path + save_name + "-Summer")
        get_img_from_string(img, "^\d\d\dSawsbuck-Winter.png", drawn_save_path + save_name + "-Winter")

        # Forces of nature forms
        get_img_from_string(img, "^\d\d\dTornadus.png", drawn_save_path + save_name + "-Incarnate")
        get_img_from_string(img, "^\d\d\dTornadus-Therian.png", drawn_save_path + save_name + "-Therian")
        get_img_from_string(img, "^\d\d\dThundurus.png", drawn_save_path + save_name + "-Incarnate")
        get_img_from_string(img, "^\d\d\dThundurus-Therian.png", drawn_save_path + save_name + "-Therian")
        get_img_from_string(img, "^\d\d\dLandorus.png", drawn_save_path + save_name + "-Incarnate")
        get_img_from_string(img, "^\d\d\dLandorus-Therian.png", drawn_save_path + save_name + "-Therian")

        # Kyurem Fusions
        get_img_from_string(img, "^\d\d\dKyurem-Black.png", drawn_save_path + save_name + "-Black")
        get_img_from_string(img, "^\d\d\dKyurem-Black2.png", drawn_save_path + save_name + "-Black_Overdrive")
        get_img_from_string(img, "^\d\d\dKyurem-White.png", drawn_save_path + save_name + "-White")
        get_img_from_string(img, "^\d\d\dKyurem-White2.png", drawn_save_path + save_name + "-White_Overdrive")
        
        # Keldeo
        get_img_from_string(img, "^\d\d\dKeldeo.png", drawn_save_path + save_name + "-Ordinary")
        get_img_from_string(img, "^\d\d\dKeldeo-Resolute.png", drawn_save_path + save_name + "-Resolute")

        # Meloetta
        get_img_from_string(img, "^\d\d\dMeloetta.png", drawn_save_path + save_name + "-Aria")
        get_img_from_string(img, "^\d\d\dMeloetta-Pirouette.png", drawn_save_path + save_name + "-Pirouette")

        # Genesect
        # Only drawn forms are dream versions
        if img["alt"].endswith("Dream.png"):
            # Get form
            form = img["alt"].split(" ")[1]
            if form == "B":
                form = "Burn_Drive"
            if form == "C":
                form = "Chill_Drive"
            if form == "D":
                form = "Douse_Drive"
            if form == "S":
                form = "Shock_Drive"
            form = "-" + form
            get_img_from_string(img, "^\d\d\dGenesect [a-zA-z] Dream.png", drawn_save_path + save_name + form)

        # Ash Greninja
        get_img_from_string(img, "^\d\d\d.png", drawn_save_path + save_name + )

        # Vivillon Patterns
        get_img_from_string(img, "^\d\d\d.png", drawn_save_path + save_name + )
        get_img_from_string(img, "^\d\d\d.png", drawn_save_path + save_name + )
        get_img_from_string(img, "^\d\d\d.png", drawn_save_path + save_name + )
        get_img_from_string(img, "^\d\d\d.png", drawn_save_path + save_name + )
        get_img_from_string(img, "^\d\d\d.png", drawn_save_path + save_name + )
        get_img_from_string(img, "^\d\d\d.png", drawn_save_path + save_name + )
        get_img_from_string(img, "^\d\d\d.png", drawn_save_path + save_name + )
        get_img_from_string(img, "^\d\d\d.png", drawn_save_path + save_name + )
        get_img_from_string(img, "^\d\d\d.png", drawn_save_path + save_name + )
        get_img_from_string(img, "^\d\d\d.png", drawn_save_path + save_name + )
        get_img_from_string(img, "^\d\d\d.png", drawn_save_path + save_name + )
        get_img_from_string(img, "^\d\d\d.png", drawn_save_path + save_name + )
        get_img_from_string(img, "^\d\d\d.png", drawn_save_path + save_name + )
        get_img_from_string(img, "^\d\d\d.png", drawn_save_path + save_name + )
        get_img_from_string(img, "^\d\d\d.png", drawn_save_path + save_name + )
        get_img_from_string(img, "^\d\d\d.png", drawn_save_path + save_name + )
        get_img_from_string(img, "^\d\d\d.png", drawn_save_path + save_name + )
        get_img_from_string(img, "^\d\d\d.png", drawn_save_path + save_name + )
        get_img_from_string(img, "^\d\d\d.png", drawn_save_path + save_name + )
        get_img_from_string(img, "^\d\d\d.png", drawn_save_path + save_name + )


        # Flabebe, Floette, and Florges colors
        # Unused form in XY
        if "Floette" in split_name and "eterna" in split_name:
            continue
        get_img_from_string(img, "^\d\d\d.png", drawn_save_path + save_name + )
        get_img_from_string(img, "^\d\d\d.png", drawn_save_path + save_name + )
        get_img_from_string(img, "^\d\d\d.png", drawn_save_path + save_name + )
        get_img_from_string(img, "^\d\d\d.png", drawn_save_path + save_name + )
        get_img_from_string(img, "^\d\d\d.png", drawn_save_path + save_name + )
        get_img_from_string(img, "^\d\d\d.png", drawn_save_path + save_name + )
        get_img_from_string(img, "^\d\d\d.png", drawn_save_path + save_name + )
        get_img_from_string(img, "^\d\d\d.png", drawn_save_path + save_name + )
        get_img_from_string(img, "^\d\d\d.png", drawn_save_path + save_name + )
        get_img_from_string(img, "^\d\d\d.png", drawn_save_path + save_name + )
        get_img_from_string(img, "^\d\d\d.png", drawn_save_path + save_name + )
        get_img_from_string(img, "^\d\d\d.png", drawn_save_path + save_name + )
        get_img_from_string(img, "^\d\d\d.png", drawn_save_path + save_name + )
        get_img_from_string(img, "^\d\d\d.png", drawn_save_path + save_name + )
        get_img_from_string(img, "^\d\d\d.png", drawn_save_path + save_name + )

        # Furfrou Trims
        get_img_from_string(img, "^\d\d\d.png", drawn_save_path + save_name + )
        get_img_from_string(img, "^\d\d\d.png", drawn_save_path + save_name + )
        get_img_from_string(img, "^\d\d\d.png", drawn_save_path + save_name + )
        get_img_from_string(img, "^\d\d\d.png", drawn_save_path + save_name + )
        get_img_from_string(img, "^\d\d\d.png", drawn_save_path + save_name + )
        get_img_from_string(img, "^\d\d\d.png", drawn_save_path + save_name + )
        get_img_from_string(img, "^\d\d\d.png", drawn_save_path + save_name + )
        get_img_from_string(img, "^\d\d\d.png", drawn_save_path + save_name + )
        get_img_from_string(img, "^\d\d\d.png", drawn_save_path + save_name + )

        # Aegislash
        get_img_from_string(img, "^\d\d\d.png", drawn_save_path + save_name + )
        get_img_from_string(img, "^\d\d\d.png", drawn_save_path + save_name + )

        # Pumpkaboo and Gourgeist Sizes
        if "Pumpkaboo" == split_name or "Gourgeist" == split_name:
            # Average sizes have no indication in filename on this website
            form = " 1Average Size"
        else:
            get_img_from_string(img, "^\d\d\d.png", drawn_save_path + save_name + )
            get_img_from_string(img, "^\d\d\d.png", drawn_save_path + save_name + )
            get_img_from_string(img, "^\d\d\d.png", drawn_save_path + save_name + )
            get_img_from_string(img, "^\d\d\d.png", drawn_save_path + save_name + )
            get_img_from_string(img, "^\d\d\d.png", drawn_save_path + save_name + )
            get_img_from_string(img, "^\d\d\d.png", drawn_save_path + save_name + )

        # Xerneas
        if "Xerneas" == split_name:
            form = " Active"
        else:
            get_img_from_string(img, "^\d\d\d.png", drawn_save_path + save_name + )

        # Zygarde
        # Cells & Nuclei aren't really sprites, so continue
        if split_name == "Zygarde célula" or split_name == "Zygarde núcleo":
            continue
        if "Zygarde" == split_name:
            form = " 50%"
        else:
            get_img_from_string(img, "^\d\d\d.png", drawn_save_path + save_name + )
            get_img_from_string(img, "^\d\d\d.png", drawn_save_path + save_name + )

        # Hoopa
        if "Hoopa" == split_name:
            form = " Confined"
        else:
            get_img_from_string(img, "^\d\d\d.png", drawn_save_path + save_name + )

        # Oricorio
        get_img_from_string(img, "^\d\d\d.png", drawn_save_path + save_name + )
        get_img_from_string(img, "^\d\d\d.png", drawn_save_path + save_name + )
        get_img_from_string(img, "^\d\d\d.png", drawn_save_path + save_name + )
        get_img_from_string(img, "^\d\d\d.png", drawn_save_path + save_name + )

        # Lycanroc
        get_img_from_string(img, "^\d\d\d.png", drawn_save_path + save_name + )
        get_img_from_string(img, "^\d\d\d.png", drawn_save_path + save_name + )
        get_img_from_string(img, "^\d\d\d.png", drawn_save_path + save_name + )

        # Wishiwashi
        get_img_from_string(img, "^\d\d\d.png", drawn_save_path + save_name + )
        get_img_from_string(img, "^\d\d\d.png", drawn_save_path + save_name + )

        # Silvally Types
        if "Silvally" == split_name:
            form = " Normal"
        if "Silvally" in split_name and split_name != "Silvally":
            type_form_translate_split()

        # Minior
        get_img_from_string(img, "^\d\d\d.png", drawn_save_path + save_name + )
        get_img_from_string(img, "^\d\d\d.png", drawn_save_path + save_name + )
        get_img_from_string(img, "^\d\d\d.png", drawn_save_path + save_name + )
        get_img_from_string(img, "^\d\d\d.png", drawn_save_path + save_name + )
        get_img_from_string(img, "^\d\d\d.png", drawn_save_path + save_name + )
        get_img_from_string(img, "^\d\d\d.png", drawn_save_path + save_name + )
        get_img_from_string(img, "^\d\d\d.png", drawn_save_path + save_name + )
        get_img_from_string(img, "^\d\d\d.png", drawn_save_path + save_name + )
        # Shiny cores all the same color?
        get_img_from_string(img, "^\d\d\d.png", drawn_save_path + save_name + )

        # Mimikyu
        if "Mimikyu" == split_name:
            form = " Disguised"
        else:
            get_img_from_string(img, "^\d\d\d.png", drawn_save_path + save_name + )

        # Necrozma
        get_img_from_string(img, "^\d\d\d.png", drawn_save_path + save_name + )
        get_img_from_string(img, "^\d\d\d.png", drawn_save_path + save_name + )
        if "Ultra-Necrozma" == split_name:
            form = " Ultra"
            split_name = split_name.split("Ultra-")[1]

        # Magearna
        get_img_from_string(img, "^\d\d\d.png", drawn_save_path + save_name + )

        # Cramorant
        get_img_from_string(img, "^\d\d\d.png", drawn_save_path + save_name + )
        get_img_from_string(img, "^\d\d\d.png", drawn_save_path + save_name + )

        # Toxtricity
        get_img_from_string(img, "^\d\d\d.png", drawn_save_path + save_name + )
        get_img_from_string(img, "^\d\d\d.png", drawn_save_path + save_name + )

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
            get_img_from_string(img, "^\d\d\d.png", drawn_save_path + save_name + )
            get_img_from_string(img, "^\d\d\d.png", drawn_save_path + save_name + )
            get_img_from_string(img, "^\d\d\d.png", drawn_save_path + save_name + )
            get_img_from_string(img, "^\d\d\d.png", drawn_save_path + save_name + )
            get_img_from_string(img, "^\d\d\d.png", drawn_save_path + save_name + )
            get_img_from_string(img, "^\d\d\d.png", drawn_save_path + save_name + )


        # Eiscue
        if "Eiscue" == split_name:
            form = "Ice Face"
        else:
            get_img_from_string(img, "^\d\d\d.png", drawn_save_path + save_name + )

        # Morpeko
        if "Morpeko" == split_name:
            form = "Full Belly"
        else:
            get_img_from_string(img, "^\d\d\d.png", drawn_save_path + save_name + )

        # Zacian and Zamazenta
        if "Zacian" == split_name:
            form = "Hero of Many Battles"
        else:
            get_img_from_string(img, "^\d\d\d.png", drawn_save_path + save_name + )
        if "Zamazenta" == split_name:
            form = "Hero of Many Battles"
        else:
            get_img_from_string(img, "^\d\d\d.png", drawn_save_path + save_name + )

        # Eternatus Eternamax
        get_img_from_string(img, "^\d\d\d.png", drawn_save_path + save_name + )

        # Urshifu
        get_img_from_string(img, "^\d\d\d.png", drawn_save_path + save_name + )
        get_img_from_string(img, "^\d\d\d.png", drawn_save_path + save_name + )

        # Zarude
        get_img_from_string(img, "^\d\d\d.png", drawn_save_path + save_name + )

        # Calyrex Ridings
        get_img_from_string(img, "^\d\d\d.png", drawn_save_path + save_name + )
        get_img_from_string(img, "^\d\d\d.png", drawn_save_path + save_name + )

    

# TODO: For Diamond/Pearl, PLatinum, and HGSS check if it's animated
    # If not, open page and see if there's a file history denoted "animated" or "APNG"
# page = requests.get("https://archives.bulbagarden.net/wiki/File:Spr_4h_006_s.png")
# page_soup = BeautifulSoup(page.content, 'html.parser')

# # Get Largest Image possible
# # Inside page
# img_link = "https:" + get_largest_png(page_soup.find(class_ = "fullImageLink").img)
# is_animated = check_if_animated(img_link)


    #print(img.attrs['alt'])