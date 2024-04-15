from bs4 import BeautifulSoup
import requests
import pathlib
import csv
import os

savePath = str(pathlib.Path(__file__).parent.resolve()) + "/img/"
savePathCsv = str(pathlib.Path(__file__).parent.resolve()) + "/"
baseUrl = "https://idleon.wiki"
req = requests.get("https://idleon.wiki/wiki/Farming")

date_conv = [60, 60, 24]

fields_names = ["num", "type", "path_img", "name", "evolution chance", "speed", "exp"]
datas =[]

#function
def date_to_sec(date_s) :
    pass

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
                with open(tempSavePath + name.replace(" ", "_") + ".jpg", "wb") as f:
                    f.write(picReq.content)

                #sauvegarde du path et du nom
                datas[-1][fields_names[2]] = tempSavePath + name + ".jpg"
                datas[-1][fields_names[3]] = name

            #Evolution chance, speed, exp
            else :
                #récupération d'une des info qui peut être Evolution chance, speed ou exp
                info = data.get_text(strip=True)
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

