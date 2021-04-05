import os

game_sprite_path = "C:\\Users\\ejone\\OneDrive\\Desktop\\Code\\Javascript\\p5\\projects\\Pokeball Pokemon Comparison\\Images\\Pokemon\\Game Sprites"
files = os.listdir("C:\\Users\\ejone\\OneDrive\\Desktop")
file_ext = ""

# TODO:
# Shiny tag first
# Then form (AND add -Form-____ tag to misc/type forms)
    # So they aren't sorted below shinies
# Then back
# Then by animated (AND delete static tag, only do -Animated for proper sorting)
for f in files:
    if f == "test.txt":
        file_ext = f[len(f)-4 : len(f)]
        os.rename("C:\\Users\\ejone\\OneDrive\\Desktop\\" + f, "C:\\Users\\ejone\\OneDrive\\Desktop\\new_test" + file_ext)
        print(f)
    #if " static" in f:
    
    #print(f, "\n")

