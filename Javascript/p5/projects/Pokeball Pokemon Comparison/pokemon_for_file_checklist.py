import xlrd     # For reading excel workbook
import xlsxwriter   # For writing new form rows
import os   # To check for files

# SPREADSHEET DATA
pokemon_info = xlrd.open_workbook('C:\\Users\\ejone\\OneDrive\\Desktop\\Code\\Javascript\\p5\\projects\\Pokeball Pokemon Comparison\\Pokemon Info.xls')
form_sheet = pokemon_info.sheet_by_name("Form Rows")
info_sheet = pokemon_info.sheet_by_name("Summary")

def cell_value(sheet, row, col):
    return (sheet.cell_value(row, col))

def gen_finder(num):
    num = int(num)
    if num <= 151:
        return ("Gen1")
    if num > 151 and num <= 251:
        return ("Gen2")
    if num > 251 and num <= 386:
        return ("Gen3")
    if num > 386 and num <= 493:
        return ("Gen4")
    if num > 493 and num <= 649:
        return ("Gen5")
    if num > 649 and num <= 721:
        return ("Gen6")
    if num > 721 and num <= 809:
        return ("Gen7")
    if num > 809 and num <= 898:
        return ("Gen8")

def game_finder_from_gen(gen):
    # Index 4 instead of -1 because on Gen6-7 it would favor Gen7, excluding XY-ORAS
    gen = int(gen[3])

    if gen == 1:
        return(["Yellow", "Red-Green", "Red-Blue"])
    if gen == 2:
        return(["Silver", "Gold", "Crystal"])
    if gen == 3:
        return(["Ruby-Sapphire", "FireRed-LeafGreen", "Emerald"])
    if gen == 4:
        return(["Platinum", "HGSS", "Diamond-Pearl"])
    if gen == 5:
        return(["BW-B2W2"])
    if gen == 6:
        # Including SM-USUM here since gen 7 shared sprites from gen 6
        return(["SM-USUM", "XY-ORAS"])
    if gen == 7:
        return(["SM-USUM"])
    if gen == 8:
        return(["Sword-Shield"])

# TODO: Change to include forms, which is on the Gen8_Pokemon sheet
is_available_in_gen_8 = {}
for i in range(1, len(info_sheet.col(4))):
    # Pokemon name = is available in gen 8
    is_available_in_gen_8[cell_value(info_sheet, i, 4)] = (cell_value(info_sheet, i, 15) == "x")

# TODO: Blocking SM-USUM Regionals
def unobtainable_checker(filename, file_gen, poke_gen):
    ###################     UNIVERSAL UNOBTAINABILITY     ###################
    # If filename is searching gens before pokemon was introduced
    if poke_gen > file_gen:
        return True
    # If filename is searching for animations in games where there weren't any
    if "-Animated" in filename:
        # Animated Back sprites before gen 5
        if "-Back" in filename and file_gen < "Gen5":
            return True
        # No animated sprites in gen 1
        if file_gen == "Gen1":
            return True
        # No animated sprites in these games
        # Gen before game checked because stuff like "Gold" is in "Golduck"s name, etc
        no_animation_games = ["Gold", "Silver", "FireRed-LeafGreen", "Ruby-Sapphire"]
        for game in no_animation_games:
            s = file_gen + " " + game
            if s in filename:
                return True
    # If filename is searching for shinies in gen1
    if "-Shiny" in filename and file_gen == "Gen1":
        return True
    # If filename is searching for females before gen4
    if "-f" in filename and file_gen < "Gen4":
        return True
    # If filename is searching for megas outside of gen 6
    if "-Mega" in filename and file_gen != "Gen6":
        return True
    # If filename is searching for regional variants before gen 7
    if "-Region" in filename and file_gen < "Gen7":
        return True
    # If filename is searching for gigantamax variants before gen 8
    if "-Gigantamax" in filename and file_gen < "Gen8":
        return True

    ###################     INDIVIDUAL POKEMON     ###################
    # Pikachu Cosplay outside of Gen6
    if "-Form-Cosplay" in filename and file_gen != "Gen6":
        return True
    # Pikachu Hat before Gen7
    if "-Form-Cap" in filename and file_gen < "Gen7":
        return True
    # Spiky-Eared Pichu outside of Gen 4
    if "-Form-Spiky_Eared" in filename and file_gen != "Gen4":
        return True
    # Primal Kyogre & Groudon outside of gen 6 & 7
    if "-Primal" in filename and file_gen != "Gen6" and file_gen != "Gen7":
        return True
    
    # Checking if pokemon is available in gen8
    if file_gen == "Gen8":
        for poke, avail in is_available_in_gen_8.items():
            # Adding a space after for pokes like Porygon, whose evolutions contain the name Porygon also
            poke_check = poke + " "
            if poke_check in filename:
                if avail == False:
                    return True

    return False
    

pokedex = {}
form_pokedex = []
class Pokemon:
    def __init__(self, name, number, variation):
        self.name = name
        self.number = number
        self.variation = variation

# Getting pokemon number and name
# Starting at 1 skips header cell
for i in range(1, len(info_sheet.col(3))):
    # Pokedex number = Pokemon name
    pokedex[cell_value(info_sheet, i, 3)] = cell_value(info_sheet, i, 4)

# Gets pokemon numbers, names, and forms
# Starting at 1 skips header cell
for i in range(1, len(form_sheet.col(0))):
    # Can do this with length of the first column since the name and number columns should be the same
    # Have to do form name keys so they're unique
        # (Pikachu-f and Pikachu-Cap share the same national dex number so there can't be repeat keys)
    name = cell_value(form_sheet, i, 1)
    number = cell_value(form_sheet, i, 0)
    variation = ""
    # Multiple variations:
        # Urshifu Gigantamax forms
        # Regional Darmanitan forms
    # Actually doesn't matter and they can still be lumped together
        # Because shiny comes before every other tag
        # Both Gigantamax and Regional tags come before form tag (so it's in proper order)
        # And back and animated tags come after variations
    if "-" in name and name != "Jangmo-o" and name != "Hakamo-o" and name != "Kommo-o" and name != "Porygon-Z" and name != "Ho-Oh":
        variation = "-" + name.split("-", 1)[1]
        name = name.split("-", 1)[0]

    form_pokedex.append(Pokemon(name, number, variation))

# for i in range(len(form_pokedex)):
#     print(form_pokedex[i].number, form_pokedex[i].name, "\n", form_pokedex[i].variation, "\n")

file_check_workbook = xlsxwriter.Workbook('C:\\Users\\ejone\\OneDrive\\Desktop\\Code\\Javascript\\p5\\projects\\Pokeball Pokemon Comparison\\Pokemon File-check.xlsx')
file_check_worksheet = file_check_workbook.add_worksheet()


##########################  HEADER ROW  ########################## 
h_format = file_check_workbook.add_format({'bold': True, 'align': 'center', 'bg_color': 'gray', 'border': 1})
file_check_worksheet.set_row(0, None, h_format)
file_check_worksheet.freeze_panes(1, 0)
file_check_worksheet.write(0, 0, "#")
file_check_worksheet.write(0, 1, "Name")
file_check_worksheet.write(0, 2, "Tags")
file_check_worksheet.write(0, 3, "Filename")
# Games sorted by reverse chronological order for file sorting synchronization between excel and files
    # Also starting with newest game first so excel file doesn't look barren upon opening
games = ["Sword-Shield", "SM-USUM", "XY-ORAS", "BW-B2W2", "Platinum", "HGSS", "Diamond-Pearl", "Ruby-Sapphire", "FireRed-LeafGreen", "Emerald", "Silver", "Gold", "Crystal", "Yellow", "Red-Green", "Red-Blue"]
game_cols = {}
for i in range(len(games)):
    # Saving game columns
    game_cols[games[i]] = i + 4
    # i + 4 to write to the next column after filename
    file_check_worksheet.write(0, i + 4, games[i])
# TODO: Add drawn column somewhere
# if i == len(games) - 1:
#     file_check_worksheet.write(0, 20, "Drawn")

##########################  POKEMON FILENAMES   ##########################
alcremie_shiny_forms_done = []
minior_shiny_form_done = False
filenames = []
# 1 because it's below the header row (row 0)
row_i = 1
for i in range(len(form_pokedex)):
    for i_ in range(8):
        # The below follow order of the microsoft alphabetically file order system that I have utilized in my naming structure
        # Normal
        tags_and_variation = form_pokedex[i].variation

        # To adjust for there only being shiny alcremie sweet forms
        if form_pokedex[i].name == "Alcremie" and (i_ == 2 or i_ == 3 or i_ == 6 or i_ == 7):
            # Not restricting by one hyphen so can get only the sweet at the end
            tags_and_variation = tags_and_variation.split("-")
            # Shiny-Form-Sweet
            tags_and_variation = "-Form-" + tags_and_variation[len(tags_and_variation) - 1]
            # If the shiny sweet form has already been done, continue through the other tags
            if tags_and_variation in alcremie_shiny_forms_done:
                continue
            # If it is the final tag iteration for alcremie, add it's shiny sweet forms to the done array to not be done again
            if i_ == 7:
                alcremie_shiny_forms_done.append(tags_and_variation)

        # To adjust for all colored minior core shinies being the same
        if form_pokedex[i].name == "Minior" and "Core" in tags_and_variation and (i_ == 2 or i_ == 3 or i_ == 6 or i_ == 7):
            tags_and_variation = "-Form-Core"
            # If the shiny core has been done, continue
            if minior_shiny_form_done:
                continue
            # If the shiny core hasn't been done and is on it's last iteration, mark it as done
            if i_ == 7:
                minior_shiny_form_done = True

        # Animated
        if i_ == 1:
            tags_and_variation += "-Animated"
        # Shiny
        if i_ == 2:
            tags_and_variation = "-Shiny" + tags_and_variation
        # Shiny-Animated
        if i_ == 3:
            tags_and_variation = "-Shiny" + tags_and_variation + "-Animated"
        # Back
        if i_ == 4:
            tags_and_variation += "-Back"
        # Back-Animated
        if i_ == 5:
            tags_and_variation += "-Back-Animated"
        # Shiny-Back
        if i_ == 6:
            tags_and_variation = "-Shiny" + tags_and_variation + "-Back"
        # Shiny-Back-Animated
        if i_ == 7:
            tags_and_variation = "-Shiny" + tags_and_variation + "-Back-Animated"

        # Assigning to cells
        # Number
        file_check_worksheet.write(row_i, 0, form_pokedex[i].number)
        # Name
        file_check_worksheet.write(row_i, 1, form_pokedex[i].name)
        # Tags & Variation
        file_check_worksheet.write(row_i, 2, tags_and_variation)
        # Filename (excluding gen & game)
            # Important to sort by so excel sheet has same ordering as file names
        filename = str(form_pokedex[i].number) + " " + form_pokedex[i].name
        # Back tags have no space in filename after gen (backs don't have game denotions), but fronts have spaces between gen and game
            # Adding this space simulates this crucial sorting system in the excel file without adding the gen and game (since those are going into columns)
        if "Back" in tags_and_variation:
            filename += tags_and_variation
        else:
            filename += " " + tags_and_variation
        # Adding too filenames array for file checking process later
        filenames.append(filename)
        file_check_worksheet.write(row_i, 3, filename)

        # Move onto next row
        row_i += 1


##########################  CHECKING FOR FILES   ##########################
# TODO: Incorporate alts
# TODO: Incorporate drawn images
# TODO: Add black fill color for impossible combos (eg mega evolutions in gen1)
# TODO: Green fill for cells with file and red for ones missing?
game_sprite_path = "C:\\Users\\ejone\\OneDrive\\Desktop\\Code\\Javascript\\p5\\projects\\Pokeball Pokemon Comparison\\Images\\Pokemon\\Game Sprites\\"
game_sprite_files = os.listdir(game_sprite_path)
for i in range(len(game_sprite_files)):
    # Removes file extension to just check name
    game_sprite_files[i] = game_sprite_files[i][:len(game_sprite_files[i])-4]

# games = ["Sword-Shield", "SM-USUM", "XY-ORAS", "BW-B2W2", "Platinum", "HGSS", "Diamond-Pearl", "Ruby-Sapphire", "FireRed-LeafGreen", "Emerald", "Silver", "Gold", "Crystal", "Yellow", "Red-Green", "Red-Blue"]
game_denotions = ["Gen8 Sword-Shield", "Gen7 SM-USUM", "Gen6-7 XY-ORAS-SM-USUM", "Gen5 BW-B2W2", "Gen4 Platinum", "Gen4 HGSS", "Gen4 Diamond-Pearl", "Gen3 Ruby-Sapphire", "Gen3 FireRed-LeafGreen", "Gen3 Emerald", "Gen2 Silver", "Gen2 Gold", "Gen2 Crystal", "Gen1 Yellow", "Gen1 Red-Green", "Gen1 Red-Blue"]
back_gen_denotions = ["Gen8", "Gen7", "Gen6-7", "Gen5", "Gen4", "Gen3", "Gen2", "Gen1"]

# Centers "x" in cell and makes fill color green
check_format = file_check_workbook.add_format({'align': 'center', 'bg_color': '#00cf37'})
missing_format = file_check_workbook.add_format({'align': 'center', 'bg_color': '#ff0000'})
unobtainable_format = file_check_workbook.add_format({'align': 'center', 'bg_color': 'black'})

missing_count = 0
row = 1
for i in range(len(filenames)):
    f = filenames[i]
    # Gets pokemon number from filename to find the pokemon name and gen
    poke_num = f[0:3]
    poke_gen = gen_finder(poke_num)
    # Figures character length of number (always 4) and name
    insert_index = 4 + len(pokedex[poke_num])
    # Removes space after name for non-back sprites
        # This was added to mimic the file sorting into the excel file
    if not "Back" in f:
        f = f[:insert_index] + f[(insert_index + 1):]

    col = -1
    if "Back" in f:
        for gen in back_gen_denotions:
            # Adds generation to checking file string
            curr_file = f[:insert_index] + ' ' + gen + f[insert_index:]
            # Getting games in generation to find column
            games_in_gen = game_finder_from_gen(gen)
            # Finding columns of games in gen
            for game in games_in_gen:
                # The unobtainability check was blocking all Alolan Regions in the spreadsheeet
                    # This was due to SM-USUM being contained in the gen6-7 file denotion (bc they share sprites)
                        # And the Region tag for gen 6 was flagged unobtainable
                    # Because SM-USUM was still in the game title, the unobtainability went to that column
                        # AFTER it was cleared for being obtainable when SM-USUM was ran perviously (bc reverse chronological order)
                if "Region-Alola" in f and gen == "Gen6-7" and game == "SM-USUM":
                    continue
                col = game_cols[game]
                # Unobtainability checker
                is_unobtainable = unobtainable_checker(curr_file, gen[:4], poke_gen)
                if is_unobtainable:
                    file_check_worksheet.write(row, col, "u", unobtainable_format)
                    continue
                # Omitting Cosplay Pikachu from SM-USUM column even though it's in filename
                    # Kept in so I don't have to add another game/back gen denotion just for cosplay pikachu
                if game == "SM-USUM" and "-Form-Cosplay" in curr_file:
                    continue
                # Checking for Crystal Backs
                if game == "Crystal":
                    # Adding Crystal into file checker name
                    curr_file = curr_file[:curr_file.find("Back") + 4] + "-Crystal" + curr_file[curr_file.find("Back") + 4:]
                # Writing to the appropriate cell
                if curr_file in game_sprite_files:
                    file_check_worksheet.write(row, col, "x", check_format)
                else:
                    file_check_worksheet.write(row, col, "", missing_format)
                    missing_count += 1

            # print(curr_file)
    else:
        for filegame in game_denotions:
            # Adds game to checking file string
            curr_file = f[:insert_index] + ' ' + filegame + f[insert_index:]
            # Find column of game
            for game in games:
                if game in filegame:
                    # The unobtainability check was blocking all Alolan Regions in the spreadsheeet
                        # This was due to SM-USUM being contained in the gen6-7 file denotion (bc they share sprites)
                            # And the Region tag for gen 6 was flagged unobtainable
                        # Because SM-USUM was still in the game title, the unobtainability went to that column
                            # AFTER it was cleared for being obtainable when SM-USUM was ran perviously (bc reverse chronological order)
                    if "Region-Alola" in f and filegame == "Gen6-7 XY-ORAS-SM-USUM" and game == "SM-USUM":
                        continue
                    col = game_cols[game]
                    # Unobtainability checker
                    is_unobtainable = unobtainable_checker(curr_file, filegame[:4], poke_gen)
                    if is_unobtainable:
                        file_check_worksheet.write(row, col, "u", unobtainable_format)
                        continue
                    # Omitting Cosplay Pikachu from SM-USUM column even though it's in filename
                    # Kept in so I don't have to add another game/back gen denotion just for cosplay pikachu
                    if game == "SM-USUM" and "-Form-Cosplay" in curr_file:
                        continue
                    # Writing to the cell if the file exists
                    # Has to be inside this game loop for XY-ORAS and SM-USUM
                        # These are combined in the filenames since models were shared through the 6th and 7th gen
                        # So if this isn't here the most recent (SM-USUM) will override prior (XY-ORAS) column
                    if curr_file in game_sprite_files:
                        file_check_worksheet.write(row, col, "x", check_format)
                    else:
                        file_check_worksheet.write(row, col, "", missing_format)
                        missing_count += 1

            # print(curr_file)
    row += 1

print("Missing:", missing_count, "images")

file_check_workbook.close()
print("Done!")
print("Remember to sort by filename column to have the spreadsheet line up with your files")

# Row by poke, column by game

# | Number | Name | Tags (incl. variation) |