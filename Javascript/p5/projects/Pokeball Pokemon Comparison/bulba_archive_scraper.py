import requests # To retrieve webpages
from bs4 import BeautifulSoup   # To parse webpages
import re   # For filtering what images to download
import urllib   # For downloading those images to my computer
import os   # For downloading those images to my computer
from PIL import Image   # For converting URL image data to PIL Image object 

def check_if_animated(link):
    # Converting URL image to PIL Image Object
    img = Image.open(requests.get(link, stream = True).raw)
    # Checking if it is an animated image
    return(img.is_animated)


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

    #urllib.urlretrieve(imgUrl, os.path.basename(imgUrl))
    return (src)

# Origin page (list of pokes by national pokedex)
# starter_url = "https://archives.bulbagarden.net"
# pokemon_starter_page = requests.get("https://archives.bulbagarden.net/wiki/Category:Pok%C3%A9mon_artwork")
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

# TODO: For Diamond/Pearl, PLatinum, and HGSS check if it's animated
    # If not, open page and see if there's a file history denoted "animated" or "APNG"
page = requests.get("https://archives.bulbagarden.net/wiki/File:Spr_4h_006_s.png")
page_soup = BeautifulSoup(page.content, 'html.parser')

# Get Largest Image possible
img_link = "https:" + get_largest_png(page_soup.find(class_ = "fullImageLink").img)
is_animated = check_if_animated(img_link)

# print(pokemon_img_urls)
# save_path = "C:\Users\ejone\OneDrive\Desktop\Code\Javascript\p5\projects\Pokeball Pokemon Comparison\Images\Pokemon"
# pokemon_starter_page = requests.get("https://archives.bulbagarden.net/wiki/Category:Charizard")
# pokemon_starter_page_soup = BeautifulSoup(pokemon_starter_page.content, 'html.parser')
# pokemon_imgs = pokemon_starter_page_soup.find_all('img')
# for img in pokemon_imgs:
#     # Gigantamax img
#     if not re.search("Gigantamax.png$", img.attrs['alt']) == None:
#         get_largest_png(img, "")


    #print(img.attrs['alt'])
#print(charizard_imgs)
