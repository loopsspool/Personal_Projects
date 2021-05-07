from PIL import Image
import os
import xlrd     # For reading excel workbook

# TODO: Purple background when using on animated pngs

# SPREADSHEET DATA
# pokemon_info = xlrd.open_workbook('C:\\Users\\ejone\\OneDrive\\Desktop\\Code\\Javascript\\p5\\projects\\Pokeball Pokemon Comparison\\Pokemon File-check.xlsx')
# sheet = pokemon_info.sheet_by_index(0)

def cell_value(row, col):
    return (sheet.cell_value(row, col))

def isnt_empty(row, col):
    return (str(cell_value(row, col)) != "")

def is_empty(row, col):
    return (cell_value(row, col) == empty_cell.value)

# Returns column number from column name
def get_col_number(col_name):
    for col in range(sheet.ncols):
        if (cell_value(0, col) == col_name):
            return col

# FILES
game_sprite_path = "C:\\Users\\ejone\\OneDrive\\Desktop\\Code\\Javascript\\p5\\projects\\Pokeball Pokemon Comparison\\Images\\Pokemon\\Game Sprites\\"
files = os.listdir(game_sprite_path)

test = ""
for f in files:
    if "Animated" in f:
        test = f
        break

print(test)
# Courtesy of https://stackoverflow.com/questions/4904940/python-converting-gif-frames-to-png
im = Image.open("C:\\Users\\ejone\\Downloads\\Aggron_NB.png")
transparency = im.info['transparency'] 
im.save("C:\\Users\\ejone\\OneDrive\\Desktop\\" + 'test2.png', transparency=transparency)
