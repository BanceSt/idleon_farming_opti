from bs4 import BeautifulSoup
import requests
import pathlib
import csv
import os

savePath = str(pathlib.Path(__file__).parent.resolve()) + "/img/"
savePathCsv = str(pathlib.Path(__file__).parent.resolve()) + "/"
baseUrl = "https://idleon.wiki"
req = requests.get("https://idleon.wiki/wiki/Farming")

date_conv = {
    "D" : 86400,
    "H" : 3600,
    "M" : 60,
    "S" : 1
}

fields_names = ["num", "type", "path_img", "name", "evolution chance", "speed", "exp"]
datas =[]

#function
def date_to_sec(date_s) :
    """ Cette fonction change un date en format \"xxD xxH xxM xxS\" en secondes"""
    date_split = date_s.split(" ")
    date_sec = 0

    for part in date_split :
        date_sec += int(part[:-1]) * date_conv[part[-1]]

    return date_sec

if (req.status_code == 200) :
    soup = BeautifulSoup(req.text, "html5lib")


    # Récupération des tableaux avec les infos sur les fruits
    tabs_soup = soup.find_all("article", class_="tabber__panel")


    # parcourt des tableaux
    for tab_soup in tabs_soup :

        # chemin de sauvegarde des images
        tempSavePath = savePath + tab_soup.get("data-title") + "/"

        # Vérification si le path existe, sinon créer les dossiers
        if not os.path.exists(tempSavePath):
            os.makedirs(tempSavePath)
        
        # Récupération des données :
        i = 0
        i2 = 0
        for data in tab_soup.find_all("td") :
            #Image et nom
            if (i%4 == 0) :
                #nouveau champ de donnée
                datas.append({})
                datas[-1][fields_names[0]] = i//4
                datas[-1][fields_names[1]] = tab_soup.get("data-title")

                #récupération Image
                picHttp = baseUrl + data.find("img").get("src")
                picReq = requests.get(picHttp)

                #récupération nom
                name = data.get_text(strip=True).replace("?", "")
                if (name == "") :
                    name = tab_soup.get("data-title") + "_" + str(i//4)

                #Télécharger l'image
                img_save_path = tempSavePath + name.replace(" ", "_") + ".jpg"
                if not(os.path.exists(img_save_path)) :
                    with open(img_save_path, "wb") as f:
                        f.write(picReq.content)

                #sauvegarde du path et du nom
                datas[-1][fields_names[2]] = tempSavePath + name + ".jpg"
                datas[-1][fields_names[3]] = name

            #Evolution chance, speed, exp
            else :
                #récupération d'une des info qui peut être Evolution chance, speed ou exp
                info = data.get_text(strip=True)

                #convertion de la date
                if ((i2%3)==1) :
                    info = date_to_sec(info)

                #enregistrement des infos
                datas[-1][fields_names[i2%3 + 4]] = info
                i2 += 1

            i += 1

    #sauvegarde csv
    with open(savePathCsv + "info_all_fruits.csv", "w") as csvfile :
        writer = csv.DictWriter(csvfile, fieldnames = fields_names) 
        writer.writeheader() 
        writer.writerows(datas)  
        


    #.find_all("tr")[1].find("td").get_text(strip=True))
    # pic = baseUrl + tab_soup[0].find("img").get("src")
    # picReq = requests.get(pic)

    # with open(str(savePath) + "/img/test.jpg", "wb") as f :
    #     f.write(picReq.content)

else :
    print("Echec de la requete")

