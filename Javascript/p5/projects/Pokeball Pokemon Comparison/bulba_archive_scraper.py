import requests # To retrieve webpages
from bs4 import BeautifulSoup   # To parse webpages
import re   # For filtering what images to download
import urllib   # For downloading those images to my computer
import os   # For downloading those images to my computer
from PIL import Image   # For converting URL image data to PIL Image object 
import openpyxl     # For reading excel workbook
# Must explicitly state this...
from openpyxl import load_workbook

def search_for_forms(pokemon):
    # Custom type forms
    # Pikachu Cosplay & Caps
    get_img_from_string(img, "^\d\d\dPikachu-Alola.png", drawn_save_path + save_name + "-Cap-Alola")
    get_img_from_string(img, "^\d\d\dPikachu-Hoenn.png", drawn_save_path + save_name + "-Cap-Hoenn")
    get_img_from_string(img, "^\d\d\dPikachu-Kalos.png", drawn_save_path + save_name + "-Cap-Kalos")
    get_img_from_string(img, "^\d\d\dPikachu-Original.png", drawn_save_path + save_name + "-Cap-Original")
    get_img_from_string(img, "^\d\d\dPikachu-Partner.png", drawn_save_path + save_name + "-Cap-Partner")
    get_img_from_string(img, "^\d\d\dPikachu-Sinnoh.png", drawn_save_path + save_name + "-Cap-Sinnoh")
    get_img_from_string(img, "^\d\d\dPikachu-Unova.png", drawn_save_path + save_name + "-Cap-Unova")
    get_img_from_string(img, "^\d\d\dPikachu-World.png", drawn_save_path + save_name + "-Cap-World")
    get_img_from_string(img, "^\d\d\dPikachu-Belle.png", drawn_save_path + save_name + "-Cosplay-Belle")
    get_img_from_string(img, "^\d\d\dPikachu-Libre.png", drawn_save_path + save_name + "-Cosplay-Libre")
    get_img_from_string(img, "^\d\d\dPikachu-PhD.png", drawn_save_path + save_name + "-Cosplay-PhD")
    get_img_from_string(img, "^\d\d\dPikachu-Pop Star.png", drawn_save_path + save_name + "-Cosplay-Pop_Star")
    get_img_from_string(img, "^\d\d\dPikachu-Rock Star.png", drawn_save_path + save_name + "-Cosplay-Rock_Star")

    # Spiky-eared Pichu
    get_img_from_string(img, "Spiky-eared Pichu DP 1", drawn_save_path + save_name + "-Spiky_Eared")

    # Unown Characters
    if pokemon.name == "Unown":
        # Only drawn forms are dream versions
        if img["alt"].endswith("Dream.png"):
            # Get form
            form = img["alt"].split(" ")[1]
            if form == "Exclamation":
                form = "!"    
            if form == "Question":
                form = "Qmark"
            form = "-" + form
            get_img_from_string(img, "^\d\d\dUnown [a-zA-z]+ Dream.png", drawn_save_path + save_name + form)

    # Castform Weathers
    get_img_from_string(img, "^\d\d\dCastform-Rainy.png", drawn_save_path + save_name + "-Rainy")
    get_img_from_string(img, "^\d\d\dCastform-Snowy.png", drawn_save_path + save_name + "-Snowy")
    get_img_from_string(img, "^\d\d\dCastform-Sunny.png", drawn_save_path + save_name + "-Sunny")

    # Primal Kyogre & Groudon
    get_img_from_string(img, "^\d\d\dKyogre-Primal 2.png", drawn_save_path + save_name + "-Primal")
    get_img_from_string(img, "^\d\d\dGroudon-Primal.png", drawn_save_path + save_name + "-Primal")

    # Deoxys
    get_img_from_string(img, "^\d\d\dDeoxys-Attack.png", drawn_save_path + save_name + "-Attack")
    get_img_from_string(img, "^\d\d\dDeoxys-Defense.png", drawn_save_path + save_name + "-Defense")
    get_img_from_string(img, "^\d\d\dDeoxys-Speed.png", drawn_save_path + save_name + "-Speed")

    # Burmy & Wormadam Cloaks
    get_img_from_string(img, "^\d\d\dBurmy-Plant.png", drawn_save_path + save_name + "-Plant")
    get_img_from_string(img, "^\d\d\dBurmy-Sandy.png", drawn_save_path + save_name + "-Sandy")
    get_img_from_string(img, "^\d\d\dBurmy-Trash.png", drawn_save_path + save_name + "-Trash")
    get_img_from_string(img, "^\d\d\dWormadam-Plant.png", drawn_save_path + save_name + "-Plant")
    get_img_from_string(img, "^\d\d\dWormadam-Sandy.png", drawn_save_path + save_name + "-Sandy")
    get_img_from_string(img, "^\d\d\dWormadam-Trash.png", drawn_save_path + save_name + "-Trash")

    # Cherrim
    # TODO: No default image, only overcast and sunny
    get_img_from_string(img, "^\d\d\dCherrim-Overcast.png", drawn_save_path + save_name + "-Overcast")
    get_img_from_string(img, "^\d\d\dCherrim-Sunny.png", drawn_save_path + save_name + "-Sunshine")

    # Shellos & Gastrodon East/West
    # TODO: No default image
    get_img_from_string(img, "^\d\d\dShellos-East.png", drawn_save_path + save_name + "-East")
    get_img_from_string(img, "^\d\d\dShellos-West.png", drawn_save_path + save_name + "-West")
    get_img_from_string(img, "^\d\d\dGastrodon-East.png", drawn_save_path + save_name + "-East")
    get_img_from_string(img, "^\d\d\dGastrodon-West.png", drawn_save_path + save_name + "-West")

    # Rotom Appliances
    get_img_from_string(img, "^\d\d\dRotom-Fan.png", drawn_save_path + save_name + "-Fan")
    get_img_from_string(img, "^\d\d\dRotom-Frost.png", drawn_save_path + save_name + "-Frost")
    get_img_from_string(img, "^\d\d\dRotom-Heat.png", drawn_save_path + save_name + "-Heat")
    get_img_from_string(img, "^\d\d\dRotom-Mow.png", drawn_save_path + save_name + "-Mow")
    get_img_from_string(img, "^\d\d\dRotom-Wash.png", drawn_save_path + save_name + "-Wash")

    # Giratina
    # TODO: No default image
    get_img_from_string(img, "^\d\d\dGiratina-Altered.png", drawn_save_path + save_name + "-Altered")
    get_img_from_string(img, "^\d\d\dGiratina-Origin.png", drawn_save_path + save_name + "-Origin")

    # Shaymin
    # TODO: No default image
    get_img_from_string(img, "^\d\d\dShaymin-Land.png", drawn_save_path + save_name + "-Land")
    get_img_from_string(img, "^\d\d\dShaymin-Sky.png", drawn_save_path + save_name + "-Sky")

    # Arceus Types
    # Only drawn forms are dream versions
    if pokemon.name == "Arceus":
        if img["alt"].endswith("Dream.png"):
            # Get form
            form = img["alt"].split(" ")[1]
            form = "-" + form
            get_img_from_string(img, "^\d\d\dArceus [a-zA-z]+ Dream.png", drawn_save_path + save_name + form)

    # Basculin Stripes
    get_img_from_string(img, "^\d\d\dBasculin-Red-Striped_XY_Anime.png", drawn_save_path + save_name + "-Red_Striped")
    get_img_from_string(img, "^\d\d\dBasculin-Blue-Striped_BW_Anime.png", drawn_save_path + save_name + "-Blue_Striped")

    # Darmanitan Modes
    get_img_from_string(img, "^\d\d\dDarmanitan.png", drawn_save_path + save_name + "-Standard")
    get_img_from_string(img, "^\d\d\dDarmanitan-Galar.png", drawn_save_path + save_name + "-Region-Galar-Standard")
    get_img_from_string(img, "^\d\d\dDarmanitan-Zen.png", drawn_save_path + save_name + "-Zen")
    get_img_from_string(img, "^\d\d\dDarmanitan-Galar-Zen.png", drawn_save_path + save_name + "-Region-Galar-Zen")

    # Deerling & Sawsbuck Seasons
    # TODO: No default image
    get_img_from_string(img, "^\d\d\dDeerling-Autumn.png", drawn_save_path + save_name + "-Autumn")
    get_img_from_string(img, "^\d\d\dDeerling-Spring.png", drawn_save_path + save_name + "-Spring")
    get_img_from_string(img, "^\d\d\dDeerling-Summer.png", drawn_save_path + save_name + "-Summer")
    get_img_from_string(img, "^\d\d\dDeerling-Winter.png", drawn_save_path + save_name + "-Winter")
    get_img_from_string(img, "^\d\d\dSawsbuck-Autumn.png", drawn_save_path + save_name + "-Autumn")
    get_img_from_string(img, "^\d\d\dSawsbuck-Spring.png", drawn_save_path + save_name + "-Spring")
    get_img_from_string(img, "^\d\d\dSawsbuck-Summer.png", drawn_save_path + save_name + "-Summer")
    get_img_from_string(img, "^\d\d\dSawsbuck-Winter.png", drawn_save_path + save_name + "-Winter")

    # Forces of nature forms
    get_img_from_string(img, "^\d\d\dTornadus.png", drawn_save_path + save_name + "-Incarnate")
    get_img_from_string(img, "^\d\d\dTornadus-Therian.png", drawn_save_path + save_name + "-Therian")
    get_img_from_string(img, "^\d\d\dThundurus.png", drawn_save_path + save_name + "-Incarnate")
    get_img_from_string(img, "^\d\d\dThundurus-Therian.png", drawn_save_path + save_name + "-Therian")
    get_img_from_string(img, "^\d\d\dLandorus.png", drawn_save_path + save_name + "-Incarnate")
    get_img_from_string(img, "^\d\d\dLandorus-Therian.png", drawn_save_path + save_name + "-Therian")

    # Kyurem Fusions
    get_img_from_string(img, "^\d\d\dKyurem-Black.png", drawn_save_path + save_name + "-Black")
    get_img_from_string(img, "^\d\d\dKyurem-Black2.png", drawn_save_path + save_name + "-Black_Overdrive")
    get_img_from_string(img, "^\d\d\dKyurem-White.png", drawn_save_path + save_name + "-White")
    get_img_from_string(img, "^\d\d\dKyurem-White2.png", drawn_save_path + save_name + "-White_Overdrive")
    
    # Keldeo
    get_img_from_string(img, "^\d\d\dKeldeo.png", drawn_save_path + save_name + "-Ordinary")
    get_img_from_string(img, "^\d\d\dKeldeo-Resolute.png", drawn_save_path + save_name + "-Resolute")

    # Meloetta
    get_img_from_string(img, "^\d\d\dMeloetta.png", drawn_save_path + save_name + "-Aria")
    get_img_from_string(img, "^\d\d\dMeloetta-Pirouette.png", drawn_save_path + save_name + "-Pirouette")

    # Genesect
    # Only drawn forms are dream versions
    if pokemon.name == "Genesect":
        if img["alt"].endswith("Dream.png"):
            # Get form
            form = img["alt"].split(" ")[1]
            if form == "B":
                form = "Burn_Drive"
            if form == "C":
                form = "Chill_Drive"
            if form == "D":
                form = "Douse_Drive"
            if form == "S":
                form = "Shock_Drive"
            form = "-" + form
            get_img_from_string(img, "^\d\d\dGenesect [a-zA-z] Dream.png", drawn_save_path + save_name + form)

    # Ash Greninja
    get_img_from_string(img, "^\d\d\dGreninja-Ash.png", drawn_save_path + save_name + "-Ash")

    # Vivillon Patterns
    get_img_from_string(img, "^\d\d\dVivillon-Archipelago.png", drawn_save_path + save_name + "-Archipelago")
    get_img_from_string(img, "^\d\d\dVivillon-Continental.png", drawn_save_path + save_name + "-Continental")
    get_img_from_string(img, "^\d\d\dVivillon-Elegant.png", drawn_save_path + save_name + "-Elegant")
    get_img_from_string(img, "^\d\d\dVivillon-Fancy.png", drawn_save_path + save_name + "-Fancy")
    get_img_from_string(img, "^\d\d\dVivillon-Garden.png", drawn_save_path + save_name + "-Garden")
    get_img_from_string(img, "^\d\d\dVivillon-High Plains.png", drawn_save_path + save_name + "-High_Plains")
    get_img_from_string(img, "^\d\d\dVivillon-Icy Snow.png", drawn_save_path + save_name + "-Icy_Snow")
    get_img_from_string(img, "^\d\d\dVivillon-Jungle.png", drawn_save_path + save_name + "-Jungle")
    get_img_from_string(img, "^\d\d\dVivillon-Marine.png", drawn_save_path + save_name + "-Marine")
    get_img_from_string(img, "^\d\d\dVivillon-Meadow.png", drawn_save_path + save_name + "-Meadow")
    get_img_from_string(img, "^\d\d\dVivillon-Modern.png", drawn_save_path + save_name + "-Modern")
    get_img_from_string(img, "^\d\d\dVivillon-Monsoon.png", drawn_save_path + save_name + "-Monsoon")
    get_img_from_string(img, "^\d\d\dVivillon-Ocean.png", drawn_save_path + save_name + "-Ocean")
    get_img_from_string(img, "^\d\d\dVivillon-Poké Ball.png", drawn_save_path + save_name + "-Poke_Ball")
    get_img_from_string(img, "^\d\d\dVivillon-Polar.png", drawn_save_path + save_name + "-Polar")
    get_img_from_string(img, "^\d\d\dVivillon-River.png", drawn_save_path + save_name + "-River")
    get_img_from_string(img, "^\d\d\dVivillon-Sandstorm.png", drawn_save_path + save_name + "-Sandstorm")
    get_img_from_string(img, "^\d\d\dVivillon-Savanna.png", drawn_save_path + save_name + "-Savanna")
    get_img_from_string(img, "^\d\d\dVivillon-Sun.png", drawn_save_path + save_name + "-Sun")
    get_img_from_string(img, "^\d\d\dVivillon-Tundra.png", drawn_save_path + save_name + "-Tundra")


    # Flabebe, Floette, and Florges colors
    get_img_from_string(img, "^\d\d\dFlabébé Blue Flower XY anime.png", drawn_save_path + save_name + "-Blue")
    get_img_from_string(img, "^\d\d\dFlabébé Orange Flower XY anime.png", drawn_save_path + save_name + "-Orange")
    get_img_from_string(img, "^\d\d\dFlabébé Red Flower XY anime.png", drawn_save_path + save_name + "-Red")
    get_img_from_string(img, "^\d\d\dFlabébé White Flower XY anime.png", drawn_save_path + save_name + "-White")
    get_img_from_string(img, "^\d\d\dFlabébé Yellow Flower XY anime.png", drawn_save_path + save_name + "-Yellow")
    get_img_from_string(img, "^\d\d\dFloette-Blue XY anime.png", drawn_save_path + save_name + "-Blue")
    get_img_from_string(img, "^\d\d\dFloette-Orange XY anime.png", drawn_save_path + save_name + "-Orange")
    get_img_from_string(img, "^\d\d\dFloette-Red XY anime.png", drawn_save_path + save_name + "-Red")
    get_img_from_string(img, "^\d\d\dFloette-Yellow XY anime.png", drawn_save_path + save_name + "-Yellow")
    #get_img_from_string(img, "^\d\d\d.png", drawn_save_path + save_name + )
    get_img_from_string(img, "^\d\d\dFlorges Blue Flower XY anime.png", drawn_save_path + save_name + "-Blue")
    get_img_from_string(img, "^\d\d\dFlorges Orange Flower XY anime.png", drawn_save_path + save_name + "-Orange")
    get_img_from_string(img, "^\d\d\dFlorges Red Flower XY anime.png", drawn_save_path + save_name + "-Red")
    get_img_from_string(img, "^\d\d\dFlorges White Flower XY anime.png", drawn_save_path + save_name + "-White")
    get_img_from_string(img, "^\d\d\dFlorges Yellow Flower XY anime.png", drawn_save_path + save_name + "-Yellow")

    # Furfrou Trims
    get_img_from_string(img, "^\d\d\dFurfrou-Diamond.png", drawn_save_path + save_name + "-Diamond_Trim")
    get_img_from_string(img, "^\d\d\dFurfrou-Heart.png", drawn_save_path + save_name + "-Heart_Trim")
    get_img_from_string(img, "^\d\d\dFurfrou-Star.png", drawn_save_path + save_name + "-Star_Trim")
    # get_img_from_string(img, "^\d\d\d.png", drawn_save_path + save_name + )
    # get_img_from_string(img, "^\d\d\d.png", drawn_save_path + save_name + )
    # get_img_from_string(img, "^\d\d\d.png", drawn_save_path + save_name + )
    # get_img_from_string(img, "^\d\d\d.png", drawn_save_path + save_name + )
    # get_img_from_string(img, "^\d\d\d.png", drawn_save_path + save_name + )
    # get_img_from_string(img, "^\d\d\d.png", drawn_save_path + save_name + )

    # Aegislash
    get_img_from_string(img, "^\d\d\dAegislash-Blade.png", drawn_save_path + save_name + "-Blade")
    get_img_from_string(img, "^\d\d\dAegislash-Shield.png", drawn_save_path + save_name + "-Shield")

    # Pumpkaboo and Gourgeist Sizes
    # if "Pumpkaboo" == split_name or "Gourgeist" == split_name:
    #     # Average sizes have no indication in filename on this website
    #     form = " 1Average Size"
    # else:
    #     get_img_from_string(img, "^\d\d\d.png", drawn_save_path + save_name + )
    #     get_img_from_string(img, "^\d\d\d.png", drawn_save_path + save_name + )
    #     get_img_from_string(img, "^\d\d\d.png", drawn_save_path + save_name + )
    #     get_img_from_string(img, "^\d\d\d.png", drawn_save_path + save_name + )
    #     get_img_from_string(img, "^\d\d\d.png", drawn_save_path + save_name + )
    #     get_img_from_string(img, "^\d\d\d.png", drawn_save_path + save_name + )

    # Xerneas
    # if "Xerneas" == split_name:
    #     form = " Active"
    # else:
    #     get_img_from_string(img, "^\d\d\d.png", drawn_save_path + save_name + )

    # Zygarde
    get_img_from_string(img, "^\d\d\dZygarde.png", drawn_save_path + save_name + "-50%")
    get_img_from_string(img, "^\d\d\dZygarde-10Percent.png", drawn_save_path + save_name + "-10%")
    get_img_from_string(img, "^\d\d\dZygarde-Complete.png", drawn_save_path + save_name + "-Complete")


    # Hoopa
    get_img_from_string(img, "^\d\d\dHoopa.png", drawn_save_path + save_name + "-Confined")
    get_img_from_string(img, "^\d\d\dHoopa-Unbound.png", drawn_save_path + save_name + "-Unbound")


    # Oricorio
    # TODO: No default
    get_img_from_string(img, "^\d\d\dOricorio-Baile.png", drawn_save_path + save_name + "-Baile")
    get_img_from_string(img, "^\d\d\dOricorio-Pa'u.png", drawn_save_path + save_name + "-Pa'u")
    get_img_from_string(img, "^\d\d\dOricorio-Pom-Pom.png", drawn_save_path + save_name + "-Pom_Pom")
    get_img_from_string(img, "^\d\d\dOricorio-Sensu.png", drawn_save_path + save_name + "-Sensu")

    # Lycanroc
    get_img_from_string(img, "^\d\d\dLycanroc.png", drawn_save_path + save_name + "-Midday")
    get_img_from_string(img, "^\d\d\dLycanroc-Dusk.png", drawn_save_path + save_name + "-Dusk")
    get_img_from_string(img, "^\d\d\dLycanroc-Midnight.png", drawn_save_path + save_name + "-Midnight")

    # Wishiwashi
    # TODO: No default
    get_img_from_string(img, "^\d\d\dWishiwashi-Solo.png", drawn_save_path + save_name + "-Solo")
    get_img_from_string(img, "^\d\d\dWishiwashi-School.png", drawn_save_path + save_name + "-School")

    # Silvally Types
    # Only drawn forms are dream versions
    if pokemon.name == "Silvally":
        if img["alt"].endswith("Dream.png"):
            # Get form
            form = img["alt"].split(" ")[1]
            form = "-" + form
            get_img_from_string(img, "^\d\d\dSilvally [a-zA-z]+ Dream.png", drawn_save_path + save_name + form)

    # Minior
    get_img_from_string(img, "^\d\d\dMinior.png", drawn_save_path + save_name + "-Meteor")
    get_img_from_string(img, "^\d\d\dMinior-Core.png", drawn_save_path + save_name + "-Red_Core")
    # get_img_from_string(img, "^\d\d\d.png", drawn_save_path + save_name + )
    # get_img_from_string(img, "^\d\d\d.png", drawn_save_path + save_name + )
    # get_img_from_string(img, "^\d\d\d.png", drawn_save_path + save_name + )
    # get_img_from_string(img, "^\d\d\d.png", drawn_save_path + save_name + )
    # get_img_from_string(img, "^\d\d\d.png", drawn_save_path + save_name + )
    # get_img_from_string(img, "^\d\d\d.png", drawn_save_path + save_name + )
    # get_img_from_string(img, "^\d\d\d.png", drawn_save_path + save_name + )
    # get_img_from_string(img, "^\d\d\d.png", drawn_save_path + save_name + )
    # # Shiny cores all the same color?
    # get_img_from_string(img, "^\d\d\d.png", drawn_save_path + save_name + )

    # Mimikyu
    get_img_from_string(img, "^\d\d\dMimikyu.png", drawn_save_path + save_name + "-Disguised")
    get_img_from_string(img, "^\d\d\dMimikyu Busted Dream.png", drawn_save_path + save_name + "-Busted")

    # Solgaleo
    get_img_from_string(img, "^\d\d\dSolgaleo-RadiantSunPhase.png", drawn_save_path + save_name + "-Radiant_Sun")

    # Lunala
    get_img_from_string(img, "^\d\d\dLunala-FullMoonPhase.png", drawn_save_path + save_name + "-Full_Moon")

    # Necrozma
    get_img_from_string(img, "^\d\d\dNecrozma-Dawn Wings.png", drawn_save_path + save_name + "-Dawn_Wings")
    get_img_from_string(img, "^\d\d\dNecrozma-Dusk Mane.png", drawn_save_path + save_name + "-Dusk_Mane")
    get_img_from_string(img, "^\d\d\dNecrozma-Ultra.png", drawn_save_path + save_name + "-Ultra")

    # Magearna
    # get_img_from_string(img, "^\d\d\d.png", drawn_save_path + save_name + )

    # Marshadow
    get_img_from_string(img, "^\d\d\dMarshadow-Alt.png", drawn_save_path + save_name + "-Zenith")

    # Cramorant
    get_img_from_string(img, "^\d\d\dCramorant-Gorging.png", drawn_save_path + save_name + "-Gorging")
    get_img_from_string(img, "^\d\d\dCramorant-Gulping.png", drawn_save_path + save_name + "-Gulping")

    # Toxtricity
    get_img_from_string(img, "^\d\d\dToxtricity-Amped.png", drawn_save_path + save_name + "-Amped")
    get_img_from_string(img, "^\d\d\dToxtricity-Low Key.png", drawn_save_path + save_name + "-Low_Key")

    # Alcremie Creams & Sweets
    # Default Alcremie is Vanilla Cream-Strawberry Sweet
    if pokemon.name == "Alcremie":
        # Space after excludes gigantamax img
        if re.search("^869Alcremie-[a-zA-Z]+ ", img.attrs["alt"]):
            # Getting largest image for Alcremie
            img_url = get_largest_png(img)
            # Splits by directory
            img_url = img_url.split("/")
            # Gets last string in sequence (the filename)
            img_url = img_url[len(img_url) - 1]
            # Splits by hyphen to get cream and sweet
            img_url = img_url.split("-")
            cream = "-" + img_url[2]
            sweet = "-" + img_url[3].replace(".png 2x", "_Sweet")
            form = cream + sweet
            get_img_from_string(img, "^869Alcremie-[a-zA-Z]+ ", drawn_save_path + save_name + form)

    # Eiscue
    # TODO: No default
    get_img_from_string(img, "^\d\d\dEiscue-Ice.png", drawn_save_path + save_name + "-Ice_Face")
    get_img_from_string(img, "^\d\d\dEiscue-Noice.png", drawn_save_path + save_name + "-Noice_Face")

    # Morpeko
    get_img_from_string(img, "^\d\d\dMorpeko-Full.png", drawn_save_path + save_name + "-Full")
    get_img_from_string(img, "^\d\d\dMorpeko-Hangry.png", drawn_save_path + save_name + "-Hangry")


    # Zacian and Zamazenta
    get_img_from_string(img, "^\d\d\dZacian.png", drawn_save_path + save_name + "-Crowned_Sword")
    get_img_from_string(img, "^\d\d\dZacian-Hero.png", drawn_save_path + save_name + "-Hero_of_Many_Battles")
    get_img_from_string(img, "^\d\d\dZamazenta.png", drawn_save_path + save_name + "-Crowned_Shield")
    get_img_from_string(img, "^\d\d\dZamazenta-Hero.png", drawn_save_path + save_name + "-Hero_of_Many_Battles")

    # Eternatus Eternamax
    # get_img_from_string(img, "^\d\d\d.png", drawn_save_path + save_name + )

    # Urshifu
    get_img_from_string(img, "^\d\d\dUrshifu-Gigantamax Rapid Strike.png", drawn_save_path + save_name + "Gigantamax-Rapid_Strike")
    get_img_from_string(img, "^\d\d\dUrshifu-Gigantamax Single Strike.png", drawn_save_path + save_name + "Gigantamax-Single_Strike")
    get_img_from_string(img, "^\d\d\dUrshifu-Rapid Strike.png", drawn_save_path + save_name + "-Rapid_Strike")
    get_img_from_string(img, "^\d\d\dUrshifu-Single Strike.png", drawn_save_path + save_name + "-Single_Strike")


    # Zarude
    get_img_from_string(img, "^\d\d\dZarude-Dada JN anime.png", drawn_save_path + save_name + "-Dada")

    # Calyrex Ridings
    get_img_from_string(img, "^\d\d\dCalyrex-Ice Rider.png", drawn_save_path + save_name + "-Ice_Rider")
    get_img_from_string(img, "^\d\d\dCalyrex-Shadow Rider.png", drawn_save_path + save_name + "-Shadow_Rider")


# Gets pokemon info from excel sheet
class Pokemon:
    def __init__(self, name, number, gen, has_f_var, has_mega, has_giganta, reg_forms, has_type_forms, has_misc_forms, is_in_gen8):
        self.name = name
        self.number = number
        self.gen = gen
        self.has_f_var = has_f_var
        self.has_mega = has_mega
        self.has_giganta = has_giganta
        self.reg_forms = reg_forms
        self.has_type_forms = has_type_forms
        self.has_misc_forms = has_misc_forms
        self.is_in_gen8 = is_in_gen8

# SPREADSHEET DATA
pokemon_info = load_workbook(filename = 'C:\\Users\\ejone\\OneDrive\\Desktop\\Code\\Javascript\\p5\\projects\\Pokeball Pokemon Comparison\\Pokemon Info.xlsx', data_only=True)
pokemon_info_sheet = pokemon_info.worksheets[0]
pokemon_files = load_workbook(filename = 'C:\\Users\\ejone\\OneDrive\\Desktop\\Code\\Javascript\\p5\\projects\\Pokeball Pokemon Comparison\\Pokemon File-check.xlsx', data_only=True)
pokemon_files_sheet = pokemon_files.worksheets[0]

def cell_value(row, col, sheet):
    return (sheet.cell(row, col).value)

def isnt_empty(row, col, sheet):
    return (cell_value(row, col, sheet) != None)

def is_empty(row, col, sheet):
    return (cell_value(row, col, sheet) == None)

# Returns column number from column name
def get_col_number(col_name, sheet):
    for col in range(1, sheet.max_column):
        if (cell_value(1, col, sheet) == col_name):
            return col

# Returns column name from column number
def get_col_name(col_number, sheet):
    return(cell_value(1, col_number, sheet))


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

    return (src)

def get_img_from_string(img, s, save_path):
    if re.search(s, img.attrs['alt']) != None:
        save_img = get_largest_png(img)
        print(img.attrs['alt'])
        print(s, " --- ", save_path)
        # urllib.request.urlretrieve(save_img, save_path)

# Determines if a pokemon can only be obtained in SM-USUM (so exclude XY-ORAS in filename)
def sm_usum_exclusivity_test(poke_num, tags):
    if poke_num >= 722:
        return True
    if "-Region-Alola" in tags:
        return True
    # For Cap Pikachu
    if "-Form-Cap" in tags:
        return True
    # For Ash Greninja
    if "-Form-Ash" in tags:
        return True
    # For Zygarde
    if "-Form-10%" in tags or "-Form-Complete" in tags:
        return True

# TODO: TEST
def combine_gen_and_game(game, poke_num, tags):
    if game == "Red-Blue" or game == "Red-Green" or game == "Yellow":
        return ("Gen1 " + game)
    if game == "Crystal" or game == "Gold" or game == "Silver":
        return ("Gen2 " + game)
    if game == "Emerald" or game == "FireRed-LeafGreen" or game == "Ruby-Sapphire":
        return ("Gen3 " + game)
    if game == "Diamond-Pearl" or game == "HGSS" or game == "Platinum":
        return ("Gen4 " + game)
    if game == "BW-B2W2":
        return ("Gen5 " + game)
    # Since XY-ORAS and SM-USUM shared sprites
    if game == "XY-ORAS" or game == "SM-USUM":
        is_sm_usum_exclusive = sm_usum_exclusivity_test(poke_num, tags)
        if is_sm_usum_exclusive:
            return ("Gen7 " + game)
        else:
            return ("Gen6-7 XY-ORAS-SM-USUM")
    if game == "Sword-Shield":
        return ("Gen8 " + game)

# TODO: TEST
def get_back_gen(game, poke_num):
    if game == "Red-Blue" or game == "Red-Green" or game == "Yellow":
        return ("Gen1")
    if game == "Crystal" or game == "Gold" or game == "Silver":
        return ("Gen2")
    if game == "Emerald" or game == "FireRed-LeafGreen" or game == "Ruby-Sapphire":
        return ("Gen3")
    if game == "Diamond-Pearl" or game == "HGSS" or game == "Platinum":
        return ("Gen4")
    if game == "BW-B2W2":
        return ("Gen5")
    # Since XY-ORAS and SM-USUM shared sprites
    if game == "XY-ORAS" or game == "SM-USUM":
        is_sm_usum_exclusive = sm_usum_exclusivity_test(poke_num, tags)
        if is_sm_usum_exclusive:
            return ("Gen7")
        else:
            return ("Gen6-7")
    if game == "Sword-Shield":
        return ("Gen8")


# Gets column numbers from spreadsheet
name_col = get_col_number("Name", pokemon_info_sheet)
num_col = get_col_number("#", pokemon_info_sheet)
gen_col = get_col_number("Gen", pokemon_info_sheet)
f_col = get_col_number("Female Variation", pokemon_info_sheet)
mega_col = get_col_number("Mega", pokemon_info_sheet)
giganta_col = get_col_number("Gigantamax", pokemon_info_sheet)
reg_forms_col = get_col_number("Regional Forms", pokemon_info_sheet)
type_forms_col = get_col_number("Type Forms", pokemon_info_sheet)
misc_forms_col = get_col_number("Misc Forms", pokemon_info_sheet)
gen8_col = get_col_number("Available in Gen 8", pokemon_info_sheet)

# Adds pokemon info from spreadsheet to object array
print("Getting pokemon info from spreadsheet...")
pokedex = []
for i in range(2, 900):
    name = cell_value(i, name_col, pokemon_info_sheet)
    num = cell_value(i, num_col, pokemon_info_sheet)
    gen = int(cell_value(i, gen_col, pokemon_info_sheet))
    has_f_var = isnt_empty(i, f_col, pokemon_info_sheet)
    has_mega = isnt_empty(i, mega_col, pokemon_info_sheet)
    has_giganta = isnt_empty(i, giganta_col, pokemon_info_sheet)
    reg_forms = cell_value(i, reg_forms_col, pokemon_info_sheet)
    has_type_forms = isnt_empty(i, type_forms_col, pokemon_info_sheet)
    has_misc_forms = isnt_empty(i, misc_forms_col, pokemon_info_sheet)
    is_in_gen8 = isnt_empty(i, gen8_col, pokemon_info_sheet)

    pokedex.append(Pokemon(name, num, gen, has_f_var, has_mega, has_giganta, reg_forms, has_type_forms, has_misc_forms, is_in_gen8))

# Getting missing images
print("Getting missing images from spreadsheet...")
missing_imgs = {}
poke_num_col = get_col_number("#", pokemon_files_sheet)
poke_name_col = get_col_number("Name", pokemon_files_sheet)
tags_col = get_col_number("Tags", pokemon_files_sheet)
filename_col = get_col_number("Filename", pokemon_files_sheet)
print(pokemon_files_sheet.max_column)
for row in range(2, pokemon_files_sheet.max_row):
    tags = cell_value(row, tags_col, pokemon_files_sheet)
    poke_num = cell_value(row, poke_num_col, pokemon_files_sheet)
    # Only doing filename_col up because those are where the actual checks need to be made (missing for certain games)
        # And +1 at the end to be inclusive
    for col in range(filename_col + 1, pokemon_files_sheet.max_column + 1):
        # If pokemon image is unavailable, continue
        if cell_value(row, col, pokemon_files_sheet) == "u":
            continue

        col_name = get_col_name(col, pokemon_files_sheet)
        # TODO: Using the below, create a full filename for the missing images
        if is_empty(row, col, pokemon_files_sheet):
            if "-Back" in tags:
                back_gen = get_back_gen(col_name, poke_num, tags)
            else:
                gen_and_game = combine_gen_and_game(col_name, poke_num, tags)

            # TODO: Find best way to organize this
                # Dictionary based off pokemon somehow (since pages are seperated by pokemon)
            print(tags, col_name)

# Origin page (list of pokes by national pokedex)
starter_url = "https://archives.bulbagarden.net"
pokemon_starter_page = requests.get("https://archives.bulbagarden.net/wiki/Category:Pok%C3%A9mon_artwork")
pokemon_starter_page_soup = BeautifulSoup(pokemon_starter_page.content, 'html.parser')
save_path_starter = "C:\\Users\\ejone\\OneDrive\\Desktop\\Code\\Javascript\\p5\\projects\\Pokeball Pokemon Comparison\\Images\\Pokemon"
drawn_save_path = save_path_starter + "\\Drawn\\"
game_save_path = save_path_starter + "\\Game Sprites\\"

pokemon_img_urls = []
curr_page_soup = pokemon_starter_page_soup
print("Starting reading of pokemon archive links...")

page_index = 0
# Loops through pages of archives of pokemon images
while True:
    # Stopping after a certain page for testing
    # if page_index == 2:
    #     break
    # Grabbing each individual pokemons archived image url
    for list_div in curr_page_soup.find_all('div', {'class': 'mw-category-group'}):
        for poke in list_div.find_all('li'):
            # Skipping specific artwork I don't want
            if poke.a.get('href') == "/wiki/Category:Ken_Sugimori_Pok%C3%A9mon_artwork" or poke.a.get('href') == "/wiki/Category:Official_Pok%C3%A9mon_artwork":
                continue
            pokemon_img_urls.append(poke.a.get('href'))

    # Only gets first page of pokemon archive links
    break

    # Moving on to the next page
    try:
        next_page_url = curr_page_soup.find('a', string='next page').get('href')
        next_page = requests.get(starter_url + next_page_url)
        next_page_soup = BeautifulSoup(next_page.content, 'html.parser')
        curr_page_soup = next_page_soup
        page_index += 1
        print("Reading next page of pokemon archive links...")
    # Unless the end of the next pages is reached
    except:
        print("Reached end of pokemon archive links.")
        break

# TODO: Create dict checklist for each of the type of images you want
    # When they're all fulfilled, break so unecessary image processing for each poke isn't occuring
    # If end of page is reached and requirements aren't satisfied (ie Arceus), continue to next page of images
#print(pokemon_img_urls)
print("Processing images...")
for i in range(len(pokemon_img_urls)):
    # Getting relevant pokemon data
    pokemon = pokedex[i]
    print(pokemon.name)

    # For only doing certain pokemon
    # if pokemon.name != "Alcremie":
    #     continue
    # print("Got here")

    save_name = pokemon.number + " " + pokemon.name
    if pokemon.name == "Type: Null":
        save_name = pokemon.number + " Type Null"
    # Getting pokemon archived image page information
    pokemon_starter_page = requests.get(starter_url + pokemon_img_urls[i])
    pokemon_starter_page_soup = BeautifulSoup(pokemon_starter_page.content, 'html.parser')
    pokemon_imgs = pokemon_starter_page_soup.find_all('img')
    # Downloading certain images
    for img in pokemon_imgs:
        #print(img.attrs['alt'], "\n\n")

        # DRAWN IMAGES
        # Drawn standard
        # Done this way so certain images that just have characters after the pokemon number don't match
            # Don't have to do this with the others because the hyphen denoters prevent the possibility
        pokemon_name_len = len(pokemon.name)
        get_img_from_string(img, "^\d\d\d[a-zA-Z]{" + str(pokemon_name_len) + "}.png", drawn_save_path + save_name)
        # Drawn Mega
        if pokemon.has_mega:
            if pokemon.name == "Charizard" or pokemon.name == "Mewtwo":
                get_img_from_string(img, "^\d\d\d[a-zA-Z]-Mega X.png", drawn_save_path + save_name + "-Mega_X")
                get_img_from_string(img, "^\d\d\d[a-zA-Z]-Mega Y.png", drawn_save_path + save_name + "-Mega_Y")
            else:
                get_img_from_string(img, "^\d\d\d[a-zA-Z]-Mega.png", drawn_save_path + save_name + "-Mega")
        # Gigantamax
        if pokemon.has_giganta:
            get_img_from_string(img, "^\d\d\d[a-zA-Z]-Gigantamax.png", drawn_save_path + save_name + "-Gigantamax")
        # Regional forms
        if pokemon.reg_forms != "":
            if "," in pokemon.reg_forms:
                get_img_from_string(img, "^\d\d\d[a-zA-Z]-Alola.png", drawn_save_path + save_name + "-Region-Alola")
                get_img_from_string(img, "^\d\d\d[a-zA-Z]-Galar.png", drawn_save_path + save_name + "-Region-Galar")
            else:
                get_img_from_string(img, "^\d\d\d[a-zA-Z]-" + pokemon.reg_forms + ".png", drawn_save_path + save_name + "-Region-" + pokemon.reg_forms)
        # Other forms
        if pokemon.has_misc_forms or pokemon.has_type_forms:
            search_for_forms(pokemon)


    

# TODO: For Diamond/Pearl, PLatinum, and HGSS check if it's animated
    # If not, open page and see if there's a file history denoted "animated" or "APNG"
# page = requests.get("https://archives.bulbagarden.net/wiki/File:Spr_4h_006_s.png")
# page_soup = BeautifulSoup(page.content, 'html.parser')

# # Get Largest Image possible
# # Inside page
# img_link = "https:" + get_largest_png(page_soup.find(class_ = "fullImageLink").img)
# is_animated = check_if_animated(img_link)


    #print(img.attrs['alt'])