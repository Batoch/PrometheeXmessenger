import pickle
import os
import requests
from lxml import html
from bs4 import BeautifulSoup
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

Login = 'baptiste.massardier'
Password = '5dsa3y3x'
#Login = input("Login promethee: ")
#Password = input("Password promethee: ")

# creation de la session de login
requestsliste = requests.session()
requests = requests.session()

# Creation des listes d'eleves
listenumero1a = []
listenumero2a = []
listenom1a = []
listenom2a = []
listenote = []
listematieretemp = []
listematiere = []


def is_non_zero_file(fpath):
    return os.path.isfile(fpath) and os.path.getsize(fpath) > 0


def login():
    print("Login en cours...")

    headers = {
        'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
        'Accept-Language': 'fr-FR,fr;q=0.8,ja;q=0.5,ru;q=0.3',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
        'Host': 'promethee.emse.fr',
    }

    params = (
        ('auth', 'default'),
    )

    response = requests.get('https://promethee.emse.fr/OpDotNet/Noyau/Login.aspx', headers=headers, params=params, verify=False)

    tree = html.fromstring(response.content)
    VIEWSTATE = tree.xpath("/html/body/form/div[1]/input[3]/@value")[0]
    VIEWSTATEGENERATOR = tree.xpath("/html/body/form/div[2]/input[1]/@value")[0]
    EVENTVALIDATION = tree.xpath("/html/body/form/div[2]/input[2]/@value")[0]


    headers = {
        'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
        'Accept-Language': 'fr-FR,fr;q=0.8,ja;q=0.5,ru;q=0.3',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
        'Host': 'promethee.emse.fr',
    }

    params = (
        ('auth', 'default'),
    )

    data = {
        '__VIEWSTATE': VIEWSTATE,
        '__VIEWSTATEGENERATOR': VIEWSTATEGENERATOR,
        '__EVENTVALIDATION': EVENTVALIDATION,
        'UcAuthentification1$UcLogin1$txtLogin': Login,
        'UcAuthentification1$UcLogin1$txtPassword': Password,
        'UcAuthentification1$UcLogin1$btnEntrer': 'Connexion'
    }

    response = requests.post('https://promethee.emse.fr/OpDotNet/Noyau/Login.aspx', headers=headers, params=params, verify=False, data=data)


    # tree = html.fromstring(response.content)
    # VIEWSTATE = tree.xpath("/html/body/form/div[1]/input[3]/@value")[0]
    # VIEWSTATEGENERATOR = tree.xpath("/html/body/form/div[2]/input[1]/@value")[0]
    # EVENTVALIDATION = tree.xpath("/html/body/form/div[2]/input[2]/@value")[0]
    #
    # headers = {
    #     'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
    #     'Referer': 'https://promethee.emse.fr/OpDotNet/Noyau/Login.aspx',
    #     'Accept-Language': 'fr-FR,fr;q=0.8,ja;q=0.5,ru;q=0.3',
    #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
    #     'Host': 'promethee.emse.fr',
    #     'Cache-Control': 'no-cache',
    # }
    #
    # data = {
    #     '__EVENTTARGET': '',
    #     '__EVENTARGUMENT': '',
    #     '__VIEWSTATE': VIEWSTATE,
    #     '__VIEWSTATEGENERATOR': VIEWSTATEGENERATOR,
    #     '__EVENTVALIDATION': EVENTVALIDATION,
    #     'UcAuthentification1$UcChangeMdP1$UcChangePassword1$txtOldPassword': '',
    #     'UcAuthentification1$UcChangeMdP1$UcChangePassword1$txtPassword': '',
    #     'UcAuthentification1$UcChangeMdP1$UcChangePassword1$txtConfirmPassword': '',
    #     'UcAuthentification1$UcChangeMdP1$btnChangeLater': 'Changer plus tard'
    # }
    #
    # response = requests.post('https://promethee.emse.fr/OpDotNet/Noyau/Login.aspx', headers=headers, verify=False, data=data)

    # Validation de la connexion

    headers = {
        'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
        'Accept-Language': 'fr-FR,fr;q=0.8,ja;q=0.5,ru;q=0.3',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
        'Host': 'promethee.emse.fr',
    }

    response = requests.get('https://promethee.emse.fr/OpDotNet/Noyau/Bandeau.aspx', headers=headers, verify=False)

    tree = html.fromstring(response.content)
    try:
        nom = tree.xpath("/html/body/form/div[3]/div[3]/div[1]/span[1]/span[1]/text()")[0]
        prenom = tree.xpath("/html/body/form/div[3]/div[3]/div[1]/span[1]/span[2]/text()")[0]
        print("Connecte au compte de " + str(nom) + " " + str(prenom))
    except:
        print("Erreur lors de la connexion")

    return response


def checklogin():
    # Validation de la connexion

    headers = {
        'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
        'Accept-Language': 'fr-FR,fr;q=0.8,ja;q=0.5,ru;q=0.3',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
        'Host': 'promethee.emse.fr',
    }

    response = requests.get('https://promethee.emse.fr/OpDotNet/Noyau/Bandeau.aspx', headers=headers, verify=False)

    tree = html.fromstring(response.content)
    try:
        nom = tree.xpath("/html/body/form/div[3]/div[3]/div[1]/span[1]/span[1]/text()")[0]
        prenom = tree.xpath("/html/body/form/div[3]/div[3]/div[1]/span[1]/span[2]/text()")[0]
        print("Connecte au compte de " + str(nom) + " " + str(prenom))
    except:
        login()


def listeeleves():
    headers = {
        'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
        'Referer': 'https://promethee.emse.fr/OpDotnet/commun/Login/aspxtoasp.aspx?url=/Eplug/Agenda/Agenda.asp?IdApplication=190&TypeAcces=Utilisateur&groupe=31',
        'Accept-Language': 'fr-FR,fr;q=0.8,ja;q=0.5,ru;q=0.3',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
        'Host': 'promethee.emse.fr',
    }

    data = {
        'url': '/Eplug/Agenda/Agenda.asp?IdApplication=190',
        'TypeAcces': 'Utilisateur',
        'groupe': '31',
        'session_IdCommunaute': '2',
        'session_IdUser': '4379',
        'session_IdGroupe': '31',
        'session_IdLangue': '1',
    }
    response = requestsliste.post('https://promethee.emse.fr/commun/aspxtoasp.asp', headers=headers, verify=False, data=data)


    headers = {
        'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
        'Referer': 'https://promethee.emse.fr/EPlug/Agenda/Agenda.asp',
        'Accept-Language': 'fr-FR,fr;q=0.8,ja;q=0.5,ru;q=0.3',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
        'Host': 'promethee.emse.fr',
    }

    params = (
        ('NumEve', '62743'),
        ('DatSrc', '20200312'),
        ('NomCal', 'PRJ6290'),
    )
    response = requestsliste.get('https://promethee.emse.fr/Eplug/Agenda/Eve-Det.asp', headers=headers, params=params, verify=False)

    # scraping
    soup = BeautifulSoup(response.content, 'html.parser')
    body = soup.find('body')
    text = body.find('script').get_text()

    liste = BeautifulSoup(text[15:len(text)-3], 'html.parser')

    eleves = liste.findAll('a')

    for eleve in eleves[1:len(eleves)-1]:            # on evite la merde a la fin
        try:
            nom = eleve.get_text().split("<")[0].replace("\xa0",' ')
            numero = eleve.get('onclick')[8:12]
            listenumero1a.append(numero)
            listenom1a.append(nom)
        except:
            break

    # 2A
    params = (
        ('NumEve', '62685'),
        ('DatSrc', '20200305'),
        ('NomCal', 'USR4379'),
    )
    response = requestsliste.get('https://promethee.emse.fr/Eplug/Agenda/Eve-Det.asp', headers=headers, params=params, verify=False)


    # scraping
    soup = BeautifulSoup(response.content, 'html.parser')
    body = soup.find('body')
    text = body.find('script').get_text()

    liste = BeautifulSoup(text[15:len(text)-3], 'html.parser')

    eleves = liste.findAll('a')

    for eleve in eleves[1:len(eleves)-1]:            # on evite la merde a la fin et au debut
        try:
            nom = eleve.get_text().split("<")[0].replace("\xa0",' ')
            numero = eleve.get('onclick')[8:12]
            listenumero2a.append(numero)
            listenom2a.append(nom)
        except:
            break


def falselisteeleves():
    name_file_list_student = "Listeeleves"
    global listenumero1a
    global listenom1a
    global listenumero2a
    global listenom2a

    if is_non_zero_file(name_file_list_student) == 0:
        listeeleves()
        Listeeleve = {"listenumero1a": listenumero1a, "listenom1a": listenom1a, "listenumero2a": listenumero2a, "listenom2a": listenom2a}

        with open(name_file_list_student, 'wb') as fichier:
            mon_pickler = pickle.Pickler(fichier)
            mon_pickler.dump(Listeeleve)
            fichier.close()
            print("Nouveau fichier creer")
    else:
        # Ouverture des fichier contenant les personnes
        with open(name_file_list_student, 'rb') as fichier:
            mon_depickler = pickle.Unpickler(fichier)
            Listeeleve = mon_depickler.load()
            fichier.close()

    for i in range(len(Listeeleve["listenumero1a"])):
        listenumero1a.append(Listeeleve["listenumero1a"][i])
        listenom1a.append(Listeeleve["listenom1a"][i])
    for i in range(len(Listeeleve["listenumero2a"])):
        listenumero2a.append(Listeeleve["listenumero2a"][i])
        listenom2a.append(Listeeleve["listenom2a"][i])


def noteseleve(student_promethee_number):
    falselisteeleves()
    checklogin()

    if listenumero2a.count(str(student_promethee_number)):  # Si c'est un 2A
        anneeformation = 2
        anneereleve = 2
    elif listenumero1a.count(str(student_promethee_number)):
        anneeformation = 1
        anneereleve = 1
    else:
        return None


    if anneereleve == 1:
        if anneeformation == 1:
            idProcess = 35469
            idIns = 178458
        elif anneeformation == 2:
            idProcess = 29867
            idIns = 130235

    elif anneereleve == 2:
        idProcess = 34751
        idIns = 167715


    headers = {
        'Referer': 'https://promethee.emse.fr/OpDotNet/Eplug/FPC/Process/Annuaire/Parcours/Parcours.aspx?IdObjet=4379&typeRef=process',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'fr-FR,fr;q=0.8,ja;q=0.5,ru;q=0.3',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18363',
        'Host': 'promethee.emse.fr',
    }

    params = (
        ('idProcess', idProcess),
        ('idUser', student_promethee_number),
        ('idIns', idIns),
        ('idProcessUC', '29866'),
        ('typeRef', 'process'),
    )

    response = requests.get(
        'https://promethee.emse.fr/OpDotNet/Eplug/FPC/Process/Annuaire/Parcours/pDetailParcours.aspx', headers=headers, params=params, verify=False, allow_redirects=False)


    # scraping

    soup = BeautifulSoup(response.content, 'html.parser')

    listeclass = soup.findAll('tr', {'class': 'DataGridItem'})
    listematieretemp.clear()
    listenote.clear()
    listematiere.clear()

    for notes in listeclass:
        if (notes.find('td', {'class': 'DataGridColumn EncadrementPaveRL'}) is not None):
            if (notes.find('td', {'class': 'largeurIE DataGridColumn'}).find('a') is None):
                matiere = notes.find('td', {'class': 'largeurIE DataGridColumn'}).get_text()[2:]
                pasnote = 1
            else:
                matiere = notes.find('td', {'class': 'largeurIE DataGridColumn'}).find('a').get_text()
                pasnote = 0
            listematieretemp.append(matiere)

            if pasnote:
                listenote.append("")
            else:
                note = notes.find_all('td', {'align': 'center'})[1].get_text()
                listenote.append(note)

    listenoteeleve = {}
    listenoteeleve.clear()

    for i in range(len(listematieretemp)):
        # print("Matiere: " + listematieretemp[i] + " Note : " + listenote[i])

        if listematieretemp[i] not in listematiere:
            listematiere.append(listematieretemp[i])
        else:                                   # Si 2 matieres avec le meme nom
            listematiere.append(str(listematieretemp[i]) + "_2")

        listenoteeleve[listematiere[i]] = listenote[i]

    return listenoteeleve


def trouverguid(student_promethee_number):
    checklogin()
    headers = {
        'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
        'Referer': 'https://promethee.emse.fr/commun/aspToaspx.asp?IdApplication=142&TypeAcces=Utilisateur&IdTypeObjet=25&IdObjet=4379&IdAnn=&IdProfil=&url=/OpDotNet/eplug/Annuaire/Navigation/Dossier/Dossier.aspx&IdAppliSource=190&AccesPerso=false',
        'Accept-Language': 'fr-FR,fr;q=0.8,ja;q=0.5,ru;q=0.3',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
        'Host': 'promethee.emse.fr',
    }

    data = {
        'IdApplication': '142',
        'TypeAcces': 'Utilisateur',
        'IdTypeObjet': '25',
        'IdObjet': '4379',
        'IdAnn': '',
        'IdProfil': '',
        'url': '/OpDotNet/eplug/Annuaire/Navigation/Dossier/Dossier.aspx',
        'IdAppliSource': '190',
        'AccesPerso': 'false',
        'Eplug_Portail_IdApplication': 'Portail',
        'Eplug_Portail_TypeAcces': 'Portail',
        'Eplug_Portail_IdGroupe': '31',
        'Eplug_118_IdApplication': '118',
        'Eplug_118_TypeAcces': 'FrontOffice',
        'Eplug_118_IdGroupe': '31',
        'Eplug_190_IdApplication': '190',
        'Eplug_190_TypeAcces': 'Utilisateur',
        'Eplug_190_IdGroupe': '31'
    }

    response = requests.post('https://promethee.emse.fr/opdotnet/commun/Login/asptoaspx.aspx', headers=headers, verify=False, data=data)

    headers = {
        'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
        'Referer': 'https://promethee.emse.fr/commun/aspToaspx.asp?IdApplication=142&TypeAcces=Utilisateur&IdTypeObjet=25&IdObjet=4379&IdAnn=&IdProfil=&url=/OpDotNet/eplug/Annuaire/Navigation/Dossier/Dossier.aspx&IdAppliSource=190&AccesPerso=false',
        'Accept-Language': 'fr-FR,fr;q=0.8,ja;q=0.5,ru;q=0.3',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
        'Host': 'promethee.emse.fr',
        'Cache-Control': 'no-cache',
    }

    params = (
        ('IdApplication', '142'),
        ('TypeAcces', 'Utilisateur'),
        ('IdTypeObjet', '25'),
        ('IdObjet', student_promethee_number),
        ('IdAnn', ''),
        ('IdProfil', ''),
        ('url', '/OpDotNet/eplug/Annuaire/Navigation/Dossier/Dossier.aspx'),
        ('IdAppliSource', '190'),
        ('AccesPerso', 'false'),
        ('', ''),
    )

    response = requests.post('https://promethee.emse.fr/OpDotNet/eplug/Annuaire/Navigation/Dossier/Dossier.aspx', headers=headers, params=params, verify=False)

    soup = BeautifulSoup(response.content, 'html.parser')

    image = soup.find('img', {'id': 'imgUcImage1'})['title']
    return(image[:len(image)-4])


def checknewnote(student_promethee_number):
    # Return -1: erreur
    # Rerurn 0 : Pas de nouvelle note
    # Sinon, return le nom des matieres avec une nouvelle note
    nouvellesnotes = {}
    nouveaufichier = 0
    try:
        listenoteeleve = noteseleve(student_promethee_number)
    except:

        return -1

    nomfichier = "notes/" + str(student_promethee_number)
    if is_non_zero_file(nomfichier) == 0:
        nouveaufichier = 1
        with open(nomfichier, 'wb') as fichier:
            mon_pickler = pickle.Pickler(fichier)
            mon_pickler.dump(listenoteeleve)
            fichier.close()
        notesfichier = listenoteeleve
        print("Nouveau fichier creer")
        print("Nouvelle personne ajouté")
    else:
        # Ouverture des fichier contenant les notes
        with open(nomfichier, 'rb') as fichier:
            mon_depickler = pickle.Unpickler(fichier)
            notesfichier = mon_depickler.load()
            fichier.close()


    if not nouveaufichier and listenoteeleve != notesfichier:  # Si les notes sont differentes et ce n'est pas un nouveau fichier
        # envoi une notification
        for i in range(len(listenoteeleve)):

            if listematiere[i] not in notesfichier:  # If field of study not in the file
                # print("Nouvelle note en (Pas dans le fichier): " + listematiere[i] + " : " + listenoteeleve[listematiere[i]])
                nouvellesnotes[listematiere[i]] = listenoteeleve[listematiere[i]]

                # send_message(eleveaverifier[eleve],
                #              "Nouvelle note en (Pas dans le fichier): " + listematiere[i] + " : " +
                #              listenoteeleve[listematiere[i]])
            else:
                if listenoteeleve[listematiere[i]] != notesfichier[listematiere[i]]:
                    nouvellesnotes[listematiere[i]] = listenoteeleve[listematiere[i]]
                    # print("Nouvelle note en " + listematiere[i] + " : " + listenoteeleve[listematiere[i]])
        with open(nomfichier, 'wb') as fichier:
            mon_pickler = pickle.Pickler(fichier)
            mon_pickler.dump(listenoteeleve)
            fichier.close()
        return nouvellesnotes
    # Sinon, pas de nouvelles notes
    else:
        return 0
