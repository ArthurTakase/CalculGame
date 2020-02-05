from random import *
from tkinter import messagebox
from tkinter import *
from tkinter.filedialog import *

window = Tk()
window.title("Calcul Game")

try :
    f = open("scoreboard.txt", "r")
    f.close()
except:
    f = open("scoreboard.txt", "a+")
    f.write("Nice|420")
    f.close()

#----- MAIN -----
# Variables
various = [[0, 20, ["+", "-"]] , [-5, 30, ["+", "-", "*"]] , [-10, 50, ["+", "-", "*"]] , [-10, 50, ["+", "-", "//", "*"]], [-50, 50, ["+", "-", "//", "*"]]]
reponse = 0
score = 0
mode = 0 # Niveau de difficulté
error = 0 # Nombre d'erreur (si == 5, alors fin du jeu)
cheat = False # Permet de savoir si l'utilsateur a triché

# Création de la solution
def start():
    global symb, reponse, min, max
    nbr1 = randint(various[mode][0],various[mode][1])
    nbr2 = randint(various[mode][0],various[mode][1])
    signe = choice(various[mode][2])

    if nbr1 < 0 :
        ask = f"( {nbr1} )  {signe}  {nbr2}" # str du calcul
    elif nbr2 < 0 :
        ask = f"{nbr1}  {signe}  ( {nbr2} )"
    elif nbr1 < 0 and nbr2 < 0 :
        ask = f"( {nbr1} )  {signe}  ( {nbr2} )"
    elif nbr2 == 0 and mode == 4:
        start()
    else :
        ask = f"{nbr1}  {signe}  {nbr2}"
    reponse = eval(ask) # effectue le calcul

    l_ask.config(text = ask + "   =")

# Vérification de la réponse
def restart():
    global reponse, score, mode, various, error, cheat

    try :
        user_choice = float(e_user.get())

        if user_choice == reponse :
            score += 1
            l_score.config(text = "Score : " + str(score))
            l_answer.config(text = "Bravo ✔", fg = "green")
            e_user.delete(first=0,last=100)

            if score >= 50 :
                pass
            elif score % 10 == 0 and mode != len(various): #score est un multiple de 10 et mode existant
                mode += 1
                l_diff.config(text = "Difficulté : " + (mode + 1)  * "★" + (4 - mode) * "☆")
            start()
        else :
            error += 1
            l_error.config(text = "Erreur  :  " + str(error))
            if error == 5 :
                e_user.delete(first=0,last=100)
                messagebox.showinfo("PERDU", "Tu viens de faire 5 erreurs, c'est la fin...\nVotre score a été enregistré, vous pouvez le voir dans le menu dedié.")
                username = e_pseudo.get()
                f = open("scoreboard.txt", "a")
                if cheat == True:
                    f.write( "\n" + username + "|" + str(score) + "*")
                else :
                    f.write( "\n" + username + "|" + str(score))
                f.close()
                #
                error = 0
                l_error.config(text = "Erreur  :  " + str(error))
                score = 0
                l_score.config(text = "Score : " + str(score))
                cheat = False
            else :
                l_answer.config(text = "Perdu ❌", fg = "red")
                e_user.delete(first=0,last=100)
                start()
    except :
        l_answer.config(text = "Error ⚠️", fg = "orange")
        e_user.delete(first=0,last=100)

#----- CHEAT 2 -----
def cheat2():
    global score, mode, various, cheat
    score += 1
    l_score.config(text = "Score : " + str(score))
    if score >= 50 :
        pass
    elif score % 10 == 0 and mode != len(various): #score est un multiple de 10 et mode existant
        mode += 1
        l_diff.config(text = "Difficulté : " + (mode + 1)  * "★" + (4 - mode) * "☆")
    cheat = True

#----- CHEAT -----
def cheat():
    global reponse, cheat
    e_user.delete(first=0,last=100)
    messagebox.showinfo("cheat", "Tu devrais avoir honte de toi ! Mais voilà ce que tu as demandé : " + str(reponse))
    cheat = True

#---- HELP MSG -----
def help():
    messagebox.showinfo("help", """----- Calcul Game -----
Vous devez trouver la réponse aux différents calculs.
Une bonne réponse : +1 point.

Tous les 10 points, la difficulté augmente.
La difficulté n'augmente plus au delà de 50 points.

Vous perdez si vous faites 5 fautes.
Vous pourrez alors enregistrer votre score dans le scoreboard de l'ordinateur.

Pour valider votre réponse, vous pouvez appuyer sur le bouton ✅ ou sur la touche Entrer.

Difficulté :
★☆☆☆☆ - signes [+  -], nombres de 0 à 20.
★★☆☆☆ - signes [+ - *], nombre de -5 à 30.
★★★☆☆ - signes [+ - *], nombres de -10 à 50.
★★★★☆ - signes [+ - * //], nombres de -10 à 50.
★★★★★ - signes [+ - * //], nombres de -50 à 50.

NB : surprise sur les touches * et +.""")

#----- SCORE MSG ----
def scoreboard_fonction():
    f = open("scoreboard.txt", "r")
    score = f.read().split("\n") # ["Arthur|10", "Quentin|12"]
    f.close()

    scoreboard = []
    for i in range (0, len(score)) :
        scoreboard.append(score[i].split("|")) # [["Arthur", "10"],["Quentin", "12"]]

    scoreboard_str = "-------- SCOREBOARD --------"
    for i in range (1, len(score)) :
        scoreboard_str += "\n" + scoreboard[i][0] + " - " + str(scoreboard[i][1])

    if scoreboard_str == "-------- SCOREBOARD --------" :
        scoreboard_str += "\n\nVous n'avez pas encore enregistré de score sur cet ordidnateur."

    messagebox.showinfo("Scoreboard",scoreboard_str)

#---- ALL MSG ----
def button_help():
    #messagebox.showinfo("help","score")
    MsgBox = messagebox.askquestion ('Menu',"""-------- Start Menu --------

Que voulez vous faire ?

Yes -> Aide et infos supplementaires
No -> Scoreboard de cet ordinateur""")
    if MsgBox == 'yes':
        help()
    else:
        scoreboard_fonction()

#----- TKINTER -----
    # Création des éléments
l_ask = Label(window, text = "Question")
l_answer = Label(window, text = "     ⬇️", width = 10)
l_score = Label(window, text = "Score : 0", width = 10, font='Helvetica 9 bold')
l_title = Label(window, text = 17*"-" + " Calcul Game " + 17*"-", fg = "blue")
l_credit = Label(window, text = "© Arthur Decaen, TS3", font='Helvetica 7')
l_diff = Label(window, text = "Difficulté : ★☆☆☆☆", width = 20, font='Helvetica 9 bold')
l_taux = Label(window, text = "Taux  :  N.C.", width = 12)
l_error = Label(window, text = "Erreur : 0", width = 12)
e_user = Entry(window)
e_pseudo = Entry(window, width = 10)
e_pseudo.insert(0, "NoName")
b_check = Button(window, height = 1, width = 2, command = restart, text = "✅", fg = "blue")
b_help = Button(window, height = 1, width = 2, text = "?", fg = "blue", command = button_help)
b_cheat = Button(window, height = 1, width = 2, command = cheat)
b_cheat2 = Button(window, height = 1, width = 2, command = cheat2)

    # Placement
        # Ligne 1
l_title.grid(row = 0, column = 1, columnspan = 4)
e_pseudo.grid(row = 5, column = 1)
        # Ligne 2
l_score.grid(row = 2, column = 1, pady = 5)
l_diff.grid(row = 2, column = 2)
l_answer.grid(row = 2, column = 3)
        # Ligne 3
l_ask.grid(row = 3, column = 1)
e_user.grid(row = 3, column = 2, padx = 10, pady = 10)
b_check.grid(row = 3, column = 3)
        # Ligne 4
#l_taux.grid(row = 3, column = 2)
l_error.grid(row = 4, column = 2)
        # Ligne 5
l_credit.grid(row = 5, column = 2, columnspan = 1)
        # Autre
b_help.place(relx=1, x=0, y=-1, anchor=NE)

start()


window.bind('<Return>', lambda event=None: b_check.invoke()) #lance le programme si <Entrer>
window.bind('*', lambda event=None: b_cheat.invoke()) # Si touche *, la reponse apparait
window.bind('+', lambda event=None: b_cheat2.invoke()) # Si touche +, augmentation du score

window.mainloop()
