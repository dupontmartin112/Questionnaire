import os
import json
import os.path
from os import listdir
from os.path import isfile, join

"""
-----------  Questionnaire  -----------

Class Questionnaires:

    Enregistrer_Questionnaire_Json():
        - enregistrer au format json
        - gérer les données

    Poser_Questions_score():
        - poser les questions
        - gérer les erreurs
        - score


Créer_Questions():
    - demander questions
    - gérer erreurs
    - retourne un liste avec les données

Menu_Principal():
    - afficher menu
    - appeler la fonction choisie
    
Retour_Menu_Principal():
    - retourner au menu principal


"""


""" Questionnaire = [["question", ["reponse a", "reponse b", "reponse c" ...], "bonne réponse"]]"""


class Questionnaires:
    def __init__(self, questionnaire: list):
        self.questionnaire = questionnaire

    def enregistrer_questionnaire_json(self):
        global Questionnaire

        if not os.path.exists('Questionnaires_json'):
            os.mkdir('Questionnaires_json')

        # enregistrer au format Json (toutes les questions)
        questionnaire_dict = []

        for i in self.questionnaire:
            question = i[0]
            choix = i[1]
            bonne_reponse = i[2]

            question = {'Question': question, 'Choix': choix, 'Bonne reponse': bonne_reponse}
            questionnaire_dict.append(question)

        questionnaire_json = json.dumps(questionnaire_dict)
        while True:
            nom_fichier_json = f"Questionnaires_json/{input('Rentrez le nom du Questionnaire: ')}.txt"
            if not os.path.exists(nom_fichier_json):
                break
            print('ERROR: Ce nom existe déjà. Veuillez en rentrer un nouveau: ')

        f = open(nom_fichier_json, "w")
        f.write(questionnaire_json)
        f.close()

        Questionnaire = []
        retour_menu_principal()

    def poser_questions_et_calculer_score(self):
        questionnaire_choisi = input('Rentrez le nom du questionnaire auquel vous voulez répondre: ')
        try:
            f = open(f'Questionnaires_json/{questionnaire_choisi}.txt', "r")
        except FileNotFoundError:
            print("ERROR: Ce questionnaire n'existe pas")
            retour_menu_principal()

        donnees_json = f.read()
        f.close()
        questionnaire = json.loads(donnees_json)

        print()
        print(f'------ QUESTIONNAIRE {questionnaire_choisi.upper()} ------')

        score = 0
        for question in questionnaire:
            print()           # index de la question, pour afficher que c'est la première, la 2e, etc
            print(f'Question {questionnaire.index(question)+1}: ' + question['Question'])

            for i in question['Choix']:
                print(' - ' + i)
            print()

            while True:
                reponse_utilisateur = input(f"Saisissez votre réponse: ")
                if reponse_utilisateur in question['Choix'] or reponse_utilisateur.isdigit():
                    break
                print("ERROR: Cette réponse n'existe pas. Réessayez: ")
                                                                    # si l'utilisateur rentre le bon numero de la réponse (donc l'index + 1 du mot)
            if reponse_utilisateur == question['Bonne reponse'] or int(reponse_utilisateur) == int(question['Choix'].index(question['Bonne reponse'])+1):
                score += 1
                print(f"Bonne réponse ! Votre score actuel est de: {score}")
            else:
                print(f"Mauvaise réponse... Votre score actuel est toujours de: {score}")

        print()
        print(f"> votre score final est de {score}/{len(questionnaire)}")
        print()
        retour_menu_principal()


# ============================================================================================================
Questionnaire = []
# ============================================================================================================


def creer_questions():
    global Questionnaire

    print()
    # 1- Question -----------------------------------------------
    if len(Questionnaire) == 0:
        print('------ CRÉATION DU QUESTIONNAIRE ------')
        print()
    question = input('Saisissez votre question: ')

    # 2- Choix --------------------------------------------------
    print("(tapez ENTRÉ quand vous avez rentré tous les choix)")
    choix = []

    for i in range(100):
        saisie = input(f'    choix {i + 1}: ')
        if saisie == "" and len(choix) < 2:
            print("    ERROR: Vous devez rentrer au moins 2 choix")
        elif saisie == "":
            print("    > okay, fin des choix")
            break
        elif saisie != "":
            choix.append(saisie)

    # 3- Bonne réponse ------------------------------------------
    while True:
        bonne_reponse = input("Saisissez la bonne réponse: ")
        if bonne_reponse in choix:
            break
        print("ERROR: Votre réponse doit faire partie des choix. Réessayez: ")

    Questionnaire.append([question, choix, bonne_reponse])

    # Si l'on veut continuer à ajouter des questions
    autre_question = input("""Voulez-vous ajouter une autre question ? 
    > OUI
    > NON
    """)
    if autre_question == 'OUI' or autre_question == '1':
        creer_questions()
    elif autre_question == 'NON' or autre_question == '2':
        return Questionnaire


def menu_principal():
    print()
    print('------ MENU PRINCIPAL ------')
    print()
    print("Choisissez ce que vous voulez faire: ")
    print("""
        > créer questionnaire
        > voir questionnaires
        > répondre
        > terminer """)

    action = input(':: ')

    # > créer questionnaire
    if action == 'créer questionnaire' or action == "1":
        print(Questionnaire)
        creer_questions()
        Questionnaires(Questionnaire).enregistrer_questionnaire_json()

    # > voir questionnaires
    elif action == 'voir questionnaires' or action == "2":
        try:
            fichiers = [f for f in listdir('Questionnaires_json') if isfile(join('Questionnaires_json', f))]
            print()
            for i in fichiers:
                print(f'    - {i}')
            print()

            while True:
                print('> Optionnel (ENTRÉ pour passer)')
                supprimer_questionnaire = input('  Pour supprimer un questionnaire, rentrez son nom: ')
                if supprimer_questionnaire + '.txt' in fichiers:
                    os.remove(f'Questionnaires_json/{supprimer_questionnaire}.txt')
                    print()
                    print('  ... fichier supprimé ...')
                    print()
                else:
                    print()
                    print('  ... aucun fichier supprimé ...')
                    break

        except FileNotFoundError:
            print("""
            - Aucun questionnaire disponible - """)

    # > répondre
    elif action == 'répondre' or action == "3":
        Questionnaires(Questionnaire).poser_questions_et_calculer_score()

    # > terminer
    elif action == 'terminer' or action == "4":
        exit()

    else:
        print("ERROR: Veuillez rentrer une des 4 actions proposées ")
        retour_menu_principal()

    print()
    retour_menu_principal()


def retour_menu_principal():
    while True:
        if input('> tapez ENTRÉ pour revenir au Menu Principal ') == '':
            # nettoie l'écran en plus
            if os.name == 'posix':
                os.system('clear')
            else:
                os.system('cls')
            menu_principal()
            break


# lancer le menu_principal() =================================================================================
menu_principal()
