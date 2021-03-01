import requests # To retrieve webpages
from bs4 import BeautifulSoup   # To parse webpages
import re   # For filtering what images to download
import urllib   # For downloading those images to my computer
import os   # For downloading those images to my computer

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

    urllib.urlretrieve(imgUrl, os.path.basename(imgUrl))
    print (src)

# Origin page (list of pokes by national pokedex)
# starter_url = "https://archives.bulbagarden.net"
# pokemon_starter_page = requests.get("https://archives.bulbagarden.net/w/index.php?title=Category:Pok%C3%A9mon_artwork&subcatuntil=199+Slowking%0ASlowking#mw-subcategories")
# pokemon_starter_page_soup = BeautifulSoup(pokemon_starter_page.content, 'html.parser')

# pokemon_img_urls = []
# curr_page_soup = pokemon_starter_page_soup

# # Loops through pages of archives of pokemon images
# while True:
#     # Grabbing each individual pokemons archived image url
#     for list_div in curr_page_soup.find_all('div', {'class': 'mw-category-group'}):
#         for poke in list_div.find_all('li'):
#             pokemon_img_urls.append(poke.a.get('href'))

#     # Moving on to the next page
#     try:
#         next_page_url = curr_page_soup.find('a', string='next page').get('href')
#         next_page = requests.get(starter_url + next_page_url)
#         next_page_soup = BeautifulSoup(next_page.content, 'html.parser')
#         curr_page_soup = next_page_soup
#     # Unless the end of the next pages is reached
#     except:
#         break

# print(pokemon_img_urls)
save_path = "C:\Users\ejone\OneDrive\Desktop\Code\Javascript\p5\projects\Pokeball Pokemon Comparison\Images\Pokemon"
pokemon_starter_page = requests.get("https://archives.bulbagarden.net/wiki/Category:Charizard")
pokemon_starter_page_soup = BeautifulSoup(pokemon_starter_page.content, 'html.parser')
pokemon_imgs = pokemon_starter_page_soup.find_all('img')
for img in pokemon_imgs:
    # Gigantamax img
    if not re.search("Gigantamax.png$", img.attrs['alt']) == None:
        get_largest_png(img, "")


    #print(img.attrs['alt'])
#print(charizard_imgs)








# pokemon_starter_page = requests.get("https://archives.bulbagarden.net/w/index.php?title=Category:Pok%C3%A9mon_artwork&subcatuntil=399+Bidoof%0ABidoof#mw-subcategories")
# pokemon_starter_page_soup = BeautifulSoup(pokemon_starter_page.content, 'html.parser')
# next_page_url = pokemon_starter_page_soup.find('a', string='next page').get('href')
# print(next_page_url)

# pokemon_links = []

# # Semi-crude way of excluding styling for tables
#     # Since they're split up by pokemon generation
# # Searches table rows
# for poke in nat_pokedex_soup.find_all('th'):
#     # And only appends if there are no attributes (meaning it's a pokemon cell)
#     if poke.attrs == {}:
#         pokemon_links.append(poke.a.get('href'))

# # This line removes duplicates (while maintaining order) from:
#     # Mega evolutions
#     # Different forms
#     # Regional forms
#     # etc.
# pokemon_links = list(dict.fromkeys(pokemon_links))

# # TODO: Apply to all pokemon pages
# # Dealing with individual pokemon pages
# indv_poke_url = starter_url + pokemon_links[0]
# indv_poke_page = requests.get(indv_poke_url)
# indv_poke_soup = BeautifulSoup(indv_poke_page.content, 'html.parser')

# sprite_img_links = []
# # Finds where the sprite point is in the page and grabs it's parent
# sprites_start = indv_poke_soup.find(id="Sprites").parent
# # Then grab the next sibling (sprites image table)
# sprites_table = sprites_start.find_next_sibling()
# sprites_table = sprites_table.find_all('th')
# # TODO: Seperate by game or generation?
# # TODO: Figure out url pattern and determine:
#     # Mega evolutions
#     # Gigantamax
#     # Sex differences
#     # Shinies
#     # Front/Back
# # And filter for images (so no generation headers)
# for cell in sprites_table:
#     if not cell.img == None:
#         sprite_img_links.append(cell.img.get('src'))

# print(sprite_img_links)
