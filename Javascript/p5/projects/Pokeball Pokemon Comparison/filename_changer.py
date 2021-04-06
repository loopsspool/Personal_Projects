import os

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
    gigantamax = False
    region = ""
    form = ""
    back = False
    animated = False
    alt = False
    
    if "Shiny" in f:
        shiny = True
    if f.endswith("f.png") or f.endswith("f alt.png") or f.endswith("f.gif")or f.endswith("f alt.gif"):
        female = True
    if "Mega" in f and not "Meganium" in f:
        mega = True
    if "Gigantamax" in f:
        gigantamax = True
    if "Alolan" in f:
        region = "Alola"
    if "Galarian" in f:
        region = "Galar"
    # TODO: For forms split by spaces then do last in the list and lop of file extension?
        # Except if it contains alt, then do second to last?
    if "Back" in f:
        back = True
    if "Animated" in f:
        animated = True
    if " alt" in f:
        alt = True

    file_ext = f[len(f)-4 : len(f)]
    #new_name = 
    #os.rename(game_sprite_path + f, game_sprite_path + new)

