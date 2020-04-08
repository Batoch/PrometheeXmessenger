import threading
import atexit, random
from flask import Flask, request
from bot import Bot
from promethee import *
from dialog import *
from datetime import datetime

POOL_TIME = 3600  # Seconds

# variables that are accessible from anywhere
nomfichierabo = "listeabo"
studenttocheck = []
listname = []
listenumero = []
# lock to control access to variable
dataLock = threading.Lock()
# thread handler
yourThread = threading.Thread()


def create_app():
    app = Flask(__name__)
    ACCESS_TOKEN = 'EAAVvf2GteAABALolELAKiWRETFFhTvRxZCyMwFI5u75KdQVyZBER4DyTQi05SUBntmljWGw05QH3zMZAZB0j1QII5dLumAs3a4hj8smvGJYP8kBHZBIehs1OJMTvnibMg6XMoM7535bnvVL9SdLeYoBJWDLeWBsHuVS3jQjwIbrnNSgbVq76V8y1QDgoEgLUZD'
    VERIFY_TOKEN = 'TESTINGTOKEN'
    bot = Bot(ACCESS_TOKEN)

    def interrupt():
        global yourThread
        yourThread.cancel()

    def doStuff():
        global yourThread
        global studenttocheck
        with dataLock:
            # Do your stuff with commonDataStruct Here

            print(studenttocheck)
            for student in studenttocheck:
                print(str(datetime.now())[11:-7] + " Scan de " + student["prenom"])
                result = checknewnote(student["numero"])
                if result == 0:
                    print("Pas de nouvelle note")
                elif result == -1:
                    print("Erreur lors du check de " + student["prenom"])
                else:
                    for i in result:
                        send_message(student["idmes"], "Nouvelle note en " + i + " : " + result[i])
                        print("Nouvelle note en " + i + " : " + result[i])

        # Set the next thread to happen
        yourThread = threading.Timer(POOL_TIME, doStuff, ())
        yourThread.start()

    def doStuffStart():
        # Do initialisation stuff here
        global listname
        global listenumero
        global studenttocheck

        login()
        falselisteeleves()

        listname = listenom1a + listenom2a
        listenumero = listenumero1a + listenumero2a

        # Ouverture de la liste des personnes

        if is_non_zero_file(nomfichierabo) == 0:
            with open(nomfichierabo, 'wb') as file:
                pickler = pickle.Pickler(file)
                pickler.dump(studenttocheck)
                file.close()
                print("Nouveau fichier creer")
        else:
            # Ouverture des fichier contenant les personnes
            with open(nomfichierabo, 'rb') as file:
                depickler = pickle.Unpickler(file)
                studenttocheck = depickler.load()
                file.close()

        for i in range(len(listname)):
            listname[i] = listname[i].upper()

        global yourThread
        # Create your thread
        yourThread = threading.Timer(POOL_TIME, doStuff, ())
        yourThread.start()

    @app.route("/", methods=['GET', 'POST'])
    def receive_message():
        # print("Message recu")
        if request.method == 'GET':
            """Before allowing people to message your bot, Facebook has implemented a verify token
            that confirms all requests that your bot receives came from Facebook."""
            token_sent = request.args.get("hub.verify_token")
            return verify_fb_token(token_sent)
        # if the request was not get, it must be POST and we can just proceed with sending a message back to user
        else:
            # get whatever message a user sent the bot
            output = request.get_json()
            for event in output['entry']:
                messaging = event['messaging']
                for message in messaging:
                    if message.get('message'):
                        # Facebook Messenger ID for user so we know where to send response back to
                        recipient_id = message['sender']['id']
                        print("Nouveau message de : " + bot.get_user_info(message['sender']['id']) + " :")
                        if message['message'].get('text'):
                            print(message['message'].get('text'))
                            response_sent_text = get_message(message)
                            send_message(recipient_id, response_sent_text)
                        # if user sends us a GIF, photo,video, or any other non-text item
                        if message['message'].get('attachments'):
                            response_sent_nontext = "Merci"
                            send_message(recipient_id, response_sent_nontext)
        return "Message Processed"

    def verify_fb_token(token_sent):
        # take token sent by facebook and verify it matches the verify token you sent
        # if they match, allow the request, else return an error
        if token_sent == VERIFY_TOKEN:
            return request.args.get("hub.challenge")
        return 'Invalid verification token'

    # chooses the message to send to the user
    def get_message(message):
        if not next((item for item in studenttocheck if item["idmes"] == message['sender']['id']),
                    None):  # If the person is not in the list
            # We look for who is the person:
            first_name = bot.get_user_info(message['sender']['id'])["first_name"]
            last_name = bot.get_user_info(message['sender']['id'])["last_name"]
            name = last_name + " " + first_name
            if name.upper() in listname:
                promethee_number = listenumero[listname.index(name.upper())]
                studenttocheck.append({"numero": promethee_number, "idmes": message['sender']['id'], "nom": last_name,
                                       "prenom": first_name})
                with open(nomfichierabo, 'wb') as file:
                    pickler = pickle.Pickler(file)
                    pickler.dump(studenttocheck)
                    file.close()
                response = "Je t'ai ajouté à la liste mon petit " + first_name
            else:
                response = "Je ne sais pas qui t'es, j'ai demandé à baptiste de la faire manuellement"
                bot.send_text_message('2621783057950447',
                                      "Aledfrr j'arrive pas a ajouter " + name + " " + message['sender']['id'])
        else:
            action, response = dialogquerry(message['message'].get('text'))

            if action == "Menu":
                sample_responses = [
                    "Send 'note' to get your grade (you must be in the database) or send 'Quit' to get removed from the database."]
            elif action == "Note":
                notes = noteseleve(
                    next((item for item in studenttocheck if item["idmes"] == message['sender']['id']), None)["numero"])
                answer = "Notes de " + str(bot.get_user_info(message['sender']['id'])["first_name"]) + ":\n"
                for i in notes.keys():
                    answer = answer + i + " : " + str(notes[i]) + "\n"
                response = response + " :\n" + answer
                notes.clear()

            # despicable :

            # nomfichier = "notes/" + str(4379)
            #
            # if is_non_zero_file(nomfichier) == 0:
            #     nouveaufichier = 1
            # else:
            #     # Ouverture des fichier contenant les notes
            #     with open(nomfichier, 'rb') as fichier:
            #         mon_depickler = pickle.Unpickler(fichier)
            #         notesfichier = mon_depickler.load()
            #         fichier.close()
            #
            # sample_responses = [str(notesfichier)]

            elif action == "QUIT":
                sample_responses = ["Je suis triste, à bientot"]
                # Remove the person from the list if exists
                if next((item for item in studenttocheck if item["idmes"] == message['sender']['id']),None) in studenttocheck:
                    studenttocheck.remove(next((item for item in studenttocheck if item["idmes"] == message['sender']['id']), None))
                    with open(nomfichierabo, 'wb') as file:
                        pickler = pickle.Pickler(file)
                        pickler.dump(studenttocheck)
                        file.close()
                else:
                    bot.send_text_message('2621783057950447', "Aledfrr j'arrive pas a supprimer " + bot.get_user_info(message['sender']['id'])["first_name"] + " " + message['sender']['id'])
            elif action == "Default Fallback Intent":
                if message['sender']['id'] == "3190229520988487":
                    response = random.choice(["Ferme la grosse merde", "Je te déteste Arthur", "Get cancer and die plz", "Puterelle",
                                        "Tu vois, ça, c’est la raison pour laquelle les gens parlent mal de toi quand t’es pas là",
                                        "Je trouve ça absolument génial, cette manière bien à toi que tu as de dire des trucs absolument évidents avec la sincère conviction que tu as découvert quelque chose",
                                        "C’est bon, tu as terminé ?", "Tu n’es vraiment pas assez beau pour pouvoir te permettre d’être aussi bête",
                                        "Est-ce que tu te rends compte que les gens ne font que te tolérer ?"])
                else:
                    sample_responses = ["Je suis un bot", "C'est moi qui envoie les messages", "Bonjour a toi"]

        # print(bot.get_user_info(message['sender']['id']))

        # return selected item to the user
        # return random.choice(sample_responses)
        return response

    # uses PyMessenger to send response to user
    def send_message(recipient_id, reply):
        # sends user the text message provided via input response parameter
        bot.send_text_message(recipient_id, reply)
        print("Envoi du message: " + reply)
        return "success"

    # Initiate
    doStuffStart()
    # When you kill Flask (SIGTERM), clear the trigger for the next thread
    atexit.register(interrupt)
    return app


app = create_app()

app.run()
