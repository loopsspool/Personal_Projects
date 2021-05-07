from PIL import Image
import os
import openpyxl     # For reading excel workbook
# NOTE: openpyxl is a 1 based index

# TODO: Purple background when using on animated pngs
# TODO: Decide if you want this script to update spreadsheet, or to run the file checker again

# SPREADSHEET DATA
pokemon_info = openpyxl.load_workbook('C:\\Users\\ejone\\OneDrive\\Desktop\\Code\\Javascript\\p5\\projects\\Pokeball Pokemon Comparison\\Pokemon File-check.xlsx')
sheet = pokemon_info.worksheets[0]
n_rows = sheet.max_row
n_cols = sheet.max_column

def cell_value(r, c):
    return (sheet.cell(row = r, column = c).value)

def isnt_empty(row, col):
    return (cell_value(row, col) != None)

def is_empty(row, col):
    return (cell_value(row, col) == None)

# Returns column number from column name
def get_col_number(col_name):
    n_cols = sheet.max_column
    for col in range(1, n_cols+1):
        if (cell_value(1, col) == col_name):
            return col

# FILES
game_sprite_path = "C:\\Users\\ejone\\OneDrive\\Desktop\\Code\\Javascript\\p5\\projects\\Pokeball Pokemon Comparison\\Images\\Pokemon\\Game Sprites\\"
files = os.listdir(game_sprite_path)

# Getting row range of cells pokemon are contained in
pokemon_ranges = {}
# Grabbing the name column from the excel file
name_col = sheet[openpyxl.utils.get_column_letter(get_col_number("Name"))]
# Removes header title 
    # Converts to list because it was a tuple before
name_col = list(name_col)
name_col.pop(0)
# Initializing first values
curr_poke = "Bulbasaur"
# Current start range at 2 because 1 is the header row
curr_poke_start_row_range = 2
curr_poke_end_row_range = -1
# Starting at 2 because header row is at 1
row_i = 2
for name in name_col:
    if name.value != curr_poke:
        # Setting end row
        curr_poke_end_row_range = row_i - 1
        # Adding start & end rows to dictionary
        pokemon_ranges[curr_poke] = (curr_poke_start_row_range, curr_poke_end_row_range)

        # Setting new current poke
        curr_poke = name.value
        curr_poke_start_row_range = row_i
        # Setting to -1 just in case
        curr_poke_end_row_range = -1

    # Setting last pokemon since there won't be a name difference because it's out of rows to iterate
    if row_i == n_rows:
        # Setting end row
        curr_poke_end_row_range = n_rows
        # Adding start & end rows to dictionary
        pokemon_ranges[curr_poke] = (curr_poke_start_row_range, curr_poke_end_row_range)
    # Adding to the row iterator
    row_i += 1

#print(pokemon_ranges)
# Keeps track of how many photos I can converted from animated to static
img_count = 0
col_i = 1
for pokemon_range in pokemon_ranges.values():
    # Getting the range of rows for the pokemon
    rows = sheet[pokemon_range[0]:pokemon_range[1]]
    # (Re) initializing dictionary for each poke
    named_rows = {}
    # Iterating through the rows to find their names
    for row in rows:
        # Minus one because tuple indices start at 0
            # But columns in openpyxl start at 1
        name = row[get_col_number("Filename") - 1].value
        named_rows[name] = row

    # Checking if there's an animated but not a static image
    for tags, row in named_rows.items():
        # Skips animated rows, which will be crossed refrenced in their static counterpart
        if "Animated" in tags:
            continue
        else:
            # Get animated counterpart of static tag row
            animated_counterpart_row = named_rows[tags + "-Animated"]
            for i in range(len(row)):
                # Check if there's an animated image and not a static one
                if row[i].value == None and animated_counterpart_row[i].value == "x":
                    img_count += 1
                    filename = tags
                    game = cell_value(1, i+1)
                    # TODO: Figure out how to deal with SM-USUM and XY-ORAS files
                    print(tags, game)

    #break
print(img_count)

# Courtesy of https://stackoverflow.com/questions/4904940/python-converting-gif-frames-to-png
# im = Image.open("C:\\Users\\ejone\\Downloads\\Aggron_NB.png")
# transparency = im.info['transparency'] 
# im.save("C:\\Users\\ejone\\OneDrive\\Desktop\\" + 'test2.png', transparency=transparency)
