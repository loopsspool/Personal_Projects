import xlrd     # For reading excel workbook
import xlsxwriter   # For writing new form rows
import os   # To check for files

# SPREADSHEET DATA
pokemon_info = xlrd.open_workbook('C:\\Users\\ejone\\OneDrive\\Desktop\\Code\\Javascript\\p5\\projects\\Pokeball Pokemon Comparison\\Pokemon Info.xls')
form_sheet = pokemon_info.sheet_by_name("Form Rows")
info_sheet = pokemon_info.sheet_by_name("Summary")

def cell_value(sheet, row, col):
    return (sheet.cell_value(row, col))

pokedex = {}
form_pokedex = []
class Pokemon:
    def __init__(self, name, number, variation):
        self.name = name
        self.number = number
        self.variation = variation

# Getting pokemon number and name
# Starting at 2 skips header cell
for i in range(2, len(info_sheet.col(3))):
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
games = ["Sword-Shield", "XY-ORAS", "SM-USUM", "BW-B2W2", "Platinum", "HGSS", "Diamond-Pearl", "Ruby-Sapphire", "FRLG", "Emerald", "Silver", "Gold", "Crystal", "Yellow", "Red-Green", "Red-Blue", ]
for i in range(len(games)):
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
game_sprite_path = "C:\\Users\\ejone\\OneDrive\\Desktop\\Code\\Javascript\\p5\\projects\\Pokeball Pokemon Comparison\\Images\\Pokemon\\Game Sprites\\"
game_sprite_files = os.listdir(game_sprite_path)

for i in range(len(filenames)):
    f = filenames[i]
    # Gets pokemon number from filename to find the pokemon name
    poke_num = f[0:3]
    # Figures character length of number (always 4) and name
    insert_index = 4 + len(pokedex[poke_num])
    # Removes space after name for non-back sprites
        # This was added to mimic the file sorting into the excel file
    if not "Back" in f:
        f = f[:insert_index] + f[(insert_index + 1):]

    for game in games:
        # TODO: Add gen for games (maybe a different array to loop through?)
        # TODO: Only do gen for back (except Crystal, gotta check those seperately)
        print(f[:insert_index] + ' ' + game + f[insert_index:])

# Centers "x" in cell
# check_format = file_check_workbook.add_format({'align': 'center'})
# TODO: Put in for loop for each of the game columns
# file_check_worksheet.set_column(4, None, check_format)


file_check_workbook.close()
print("Done!")
print("Remember to sort by filename column to have the spreadsheet line up with your files")

# Row by poke, column by game

# | Number | Name | Tags (incl. variation) |