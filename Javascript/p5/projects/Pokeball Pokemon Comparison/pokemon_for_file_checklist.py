import xlrd     # For reading excel workbook
import XlsxWriter   # For writing new form rows

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

