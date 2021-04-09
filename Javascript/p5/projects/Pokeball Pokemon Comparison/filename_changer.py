import os
import re
import xlrd

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

    pokedex.append(Pokemon(name, num, gen, has_f_var, has_mega, has_giganta, reg_forms, has_type_forms, has_misc_forms))


game_sprite_path = "C:\\Users\\ejone\\OneDrive\\Desktop\\Code\\Javascript\\p5\\projects\\Pokeball Pokemon Comparison\\Images\\Pokemon\\Game Sprites\\"
files = os.listdir(game_sprite_path)
file_ext = ""

# TODO:
# Shiny tag first
# Then form (AND add -Form-____ tag to misc/type forms)
    # So they aren't sorted below shinies
# Then back
# Then by animated
# Then by alt
for f in files:
    shiny = False
    female = False
    mega = False
    mega_x = False
    mega_y = False
    gigantamax = False
    region = ""
    form = ""
    back = False
    animated = False
    alt = False

    old_filename = f
    
    if "Shiny" in f:
        shiny = True
        old_filename = old_filename.replace(" Shiny", "")
    
    if f.endswith("f.png") or f.endswith("f alt.png") or f.endswith("f.gif")or f.endswith("f alt.gif"):
        female = True
        old_filename = old_filename.replace(" f", "")
   
    if "Mega" in f and not "Meganium" in f:
        mega = True
        if "MegaX" or "MegaY" in f:
            try:
                old_filename = old_filename.replace(" MegaX", "")
                mega_x = True
            except:
                old_filename = old_filename.replace(" MegaY", "")
                mega_y = True
        else:
            old_filename = old_filename.replace(" Mega", "")
    
    if "Gigantamax" in f:
        gigantamax = True
        old_filename = old_filename.replace(" Gigantamax", "")
    
    if "Alolan" in f:
        region = "Alola"
        old_filename = old_filename.replace(" Alolan", "")
    if "Galarian" in f:
        region = "Galar"
        old_filename = old_filename.replace(" Galarian", "")
    
    if "Back" in f:
        back = True
        old_filename = old_filename.replace("-Back", "")
    
    if "Animated" in f:
        animated = True
        old_filename = old_filename.replace(" Animated", "")
   
    if " alt" in f:
        alt = True
        old_filename = old_filename.replace(" alt", "")

    file_ext = f[len(f)-4 : len(f)]

    # Getting form
    for poke in pokedex:
        if poke.number == f[0:3]:
            if poke.has_misc_forms or poke.has_type_forms:
                old_filename = old_filename.replace(file_ext, "")
                # Splitting filename by gen
                    # Unfortunately, Genesects name starts with Gen lol
                if poke.name != "Genesect":
                    old_filename = old_filename.split("Gen")[1]
                else:
                    # Handling Genesects case
                    old_filename = old_filename.split("Gen")[2]

                # Then by game
                    # If the file is a back sprite, there's only one space after the gen split
                        # This is due to back sprites being shared by generation
                split_num = -1
                if back == True:
                    split_num = 1
                else:
                    split_num = 2
                old_filename = old_filename.split(" ", split_num)
                # Getting only the last element (which should be form)
                old_filename = old_filename[len(old_filename) - 1]
                # If old_filename is only gen number or game (ie regular forms), skip
                if re.search("\d$", old_filename) or re.search("Red-Blue", old_filename) or re.search("Red-Green", old_filename) or re.search("Yellow", old_filename) or re.search("Crystal", old_filename) or re.search("Gold", old_filename) or re.search("Silver", old_filename) or re.search("Emerald", old_filename) or re.search("FireRed-LeafGreen", old_filename) or re.search("Ruby-Sapphire", old_filename) or re.search("Diamond-Pearl", old_filename) or re.search("HGSS", old_filename) or re.search("Platinum", old_filename) or re.search("XY-ORAS-SM-USUM", old_filename) or re.search("SM-USUM", old_filename) or re.search("Sword-Shield", old_filename):
                    continue

                # Replacing Oricorio style tag I put in before I decided to do form tags
                if " Style" in old_filename:
                    old_filename = old_filename.replace(" Style", "")
                # Replacing spaces with underscores for proper file sorting
                old_filename = old_filename.replace(" ", "_")

                print(poke.number, poke.name, ":", old_filename)


# For testing/slight correction in file names
# for f in files:
#     if "Eiscue" in f:
#         print(f)
        # old = f
        # new = old.replace("3S", "3_S")
        # print(new)
        # os.rename(game_sprite_path + f, game_sprite_path + new)

# TODO: If Gen2-Back and Crystal in name
    # Replace " Crystal" with ""
    # And Replace Gen2-Back with Gen2-Crystal Back? Or Something of the sort to sort files properly



    #new_name = 
    #os.rename(game_sprite_path + f, game_sprite_path + new)

