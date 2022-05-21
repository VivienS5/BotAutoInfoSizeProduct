from email import charset
import time
import requests #lib pour la partie web scraping
from bs4 import BeautifulSoup #lib  pour la  partie web scraping
import smtplib #lib pour la partie email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

SMTP_SERVER =  "smtp.gmail.com" #Serveur email
SMTP_PORT = 587 #Port du serveur
GMAIL_USERNAME  = "BotHdws@gmail.com" #Votre adresse  email
GMAIL_PASSWORD = "QSDFGHjklm" #Votre  mot de passe
receiverAddress = "hidaouse.hedws@gmail.com" #Adresse mail destinataire

emailSubject = "Rapport du bot JD \U0001F3AE" #Objet du email 
emailBase = "C'est le moment d'acheter :\n\n" #Début du corps du email
emailContent = "" #Contenu du mail
emailSignature = "\n Cordialement,\n Le bot" #Signature du mail
sendEmail = False #Variable de contrôle permettant de savoir s'il faut envoyer l'email

#Liste des URLs des jeux dont je souhaite surveiller le prix
product_urls = [
"https://www.jdsports.fr/product/blanc-the-north-face-aconcagua-down-jacket/16228080_jdsportsfr/",
# "https://www.jdsports.fr/product/bleu-the-north-face-sweat--capuche-multi-dome-homme/16484779_jdsportsfr/",

]


#Listes dans lesquelles on stockera nom et le boutton M 
product_names = [""]*len(product_urls)
product_dispM = [""]*len(product_urls)

#Boucle qui parcourt la liste des URLs et qui récupère le nom et le boutton M
for i in range(len(product_urls)):
    page = requests.get(product_urls[i])
#    time.sleep(10)
    parser = BeautifulSoup(page.content,'html.parser')
    product_names[i] = parser.find(class_="productRight").h1.text
    product_dispM = parser.findAll(class_="btn options-loading")
    


    # print(product_dispM)
    # print(len(product_dispM))

    while (len(product_dispM) <= 2):
        print("il y en a moins que deux")
        time.sleep(900)
    else:
        print("il y en a plus deux")
        emailContent = emailContent + "C'est le moment ! "
        sendEmail = True
        print("L'email à été envoyé")
        time.sleep(5)
        break
        
            

#Boucle qui vérifie si le boutton M existe sur les produits dans la liste URLS
# for j in range (len(product_names)):
#     if 1 in product_dispM:
#         print(product_dispM)
        


#Envoi de l'email
if(sendEmail == True):
    #Le corps du mail est composé de la phrase de base, si le boutton M est apparu et de la signature
    emailBody = emailBase + emailContent + emailSignature

    #Creation de  l'email
    message = MIMEMultipart()
    message['From'] = GMAIL_USERNAME
    message['To'] = receiverAddress
    message['Subject'] = emailSubject
    message.attach(MIMEText(emailBody, 'plain'))

    #Connexion  au serveur Gmail
    session = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    session.ehlo()
    session.starttls()
    session.ehlo()
 
    #Authentification
    session.login(GMAIL_USERNAME, GMAIL_PASSWORD)

    #Envoi de l'email
    session.sendmail(GMAIL_USERNAME, receiverAddress, message.as_string())
    session.quit

    #Le mail vient d'être envoyé, on remet la variable de controle à False
    sendEmail = False
