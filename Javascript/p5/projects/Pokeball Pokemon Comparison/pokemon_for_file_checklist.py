import xlrd     # For reading excel workbook
import xlsxwriter   # For writing new form rows

# SPREADSHEET DATA
pokemon_info = xlrd.open_workbook('C:\\Users\\ejone\\OneDrive\\Desktop\\Code\\Javascript\\p5\\projects\\Pokeball Pokemon Comparison\\Pokemon Info.xls')
poke_sheet = pokemon_info.sheet_by_name("Form Rows")

def cell_value(row, col):
    return (poke_sheet.cell_value(row, col))

def isnt_empty(row, col):
    return (str(cell_value(row, col)) != "")

def is_empty(row, col):
    return (cell_value(row, col) == empty_cell.value)

# Returns column number from column name
def get_col_number(col_name):
    for col in range(poke_sheet.ncols):
        if (cell_value(1, col) == col_name):
            return col

pokedex = []
class Pokemon:
    def __init__(self, name, number, variation):
        self.name = name
        self.number = number
        self.variation = variation

# Gets pokemon numbers, names, and forms
# Starting at 1 skips header cell
for i in range(1, len(poke_sheet.col(0))):
    # Can do this with length of the first column since the name and number columns should be the same
    # Have to do form name keys so they're unique
        # (Pikachu-f and Pikachu-Cap share the same national dex number so there can't be repeat keys)
    name = cell_value(i, 1)
    number = cell_value(i, 0)
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

    pokedex.append(Pokemon(name, number, variation))
    #poke_form_dict[cell_value(i, 1)] = cell_value(i, 0)

# for i in range(len(pokedex)):
#     print(pokedex[i].number, pokedex[i].name, "\n", pokedex[i].variation, "\n")

file_check_workbook = xlsxwriter.Workbook('C:\\Users\\ejone\\OneDrive\\Desktop\\Code\\Javascript\\p5\\projects\\Pokeball Pokemon Comparison\\Pokemon File-check.xlsx')
file_check_worksheet = file_check_workbook.add_worksheet()


##########################  HEADER ROW  ########################## 
h_format = file_check_workbook.add_format({'bold': True, 'align': 'center', 'bg_color': 'gray', 'border': 1})
file_check_worksheet.set_row(0, 1, h_format)
file_check_worksheet.write(0, 0, "#")
file_check_worksheet.write(0, 1, "Name")
file_check_worksheet.write(0, 2, "Tags")
file_check_worksheet.write(0, 3, "Filename")
# Games sorted by reverse chronological order for file sorting synchronization between excel and files
    # Also starting with newest game first so excel file doesn't look barren upon opening
file_check_worksheet.write(0, 4, "Sword-Shield")
file_check_worksheet.write(0, 5, "XY-ORAS")
file_check_worksheet.write(0, 6, "SM-USUM")
file_check_worksheet.write(0, 7, "BW-B2W2")
file_check_worksheet.write(0, 8, "Platinum")
file_check_worksheet.write(0, 9, "HGSS")
file_check_worksheet.write(0, 10, "Diamond-Pearl")
file_check_worksheet.write(0, 11, "Ruby-Sapphire")
file_check_worksheet.write(0, 12, "FRLG")
file_check_worksheet.write(0, 13, "Emerald")
file_check_worksheet.write(0, 14, "Silver")
file_check_worksheet.write(0, 15, "Gold")
file_check_worksheet.write(0, 16, "Crystal")
file_check_worksheet.write(0, 17, "Yellow")
file_check_worksheet.write(0, 18, "Red-Green")
file_check_worksheet.write(0, 19, "Red-Blue")


##########################  POKEMON FILES   ##########################
alcremie_shiny_forms_done = []
minior_shiny_form_done = False
row_i = 1
for i in range(len(pokedex)):
    for i_ in range(8):
        # The below follow order of the microsoft alphabetically file order system that I have utilized in my naming structure
        # Normal
        tags_and_variation = pokedex[i].variation

        # To adjust for there only being shiny alcremie sweet forms
        if pokedex[i].name == "Alcremie" and (i_ == 2 or i_ == 3 or i_ == 6 or i_ == 7):
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
        if pokedex[i].name == "Minior" and "Core" in tags_and_variation and (i_ == 2 or i_ == 3 or i_ == 6 or i_ == 7):
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
        file_check_worksheet.write(row_i, 0, pokedex[i].number)
        # Name
        file_check_worksheet.write(row_i, 1, pokedex[i].name)
        # Tags & Variation
        file_check_worksheet.write(row_i, 2, tags_and_variation)
        # Filename (excluding gen & game)
            # Important to sort by so excel sheet has same ordering as file names
        filename = str(pokedex[i].number) + " " + pokedex[i].name
        # Back tags have no space in filename, which is what sorts them after all of the front shots
        if "Back" in tags_and_variation:
            filename += tags_and_variation
        else:
            filename += " " + tags_and_variation
        file_check_worksheet.write(row_i, 3, filename)

        # Move onto next row
        row_i += 1

file_check_workbook.close()
print("Done!")
print("Remember to sort by filename column to have the spreadsheet line up with your files")

# Row by poke, column by game

# | Number | Name | Tags (incl. variation) |