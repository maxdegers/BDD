# importation des outils utiles de flask.
from flask import Flask, render_template, request
from sqlite3 import *
import json
# création d’un outil app.
app = Flask(__name__)
# décorateur (hors programme) qui permet d’exécuter la fonction lorsque le serveur recevra une requête http avec comme URL la racine du site (‘/’).


def n_professeur(id, nom, prenom):
    # fontion qui rajoute un professeur dans la base de donnée
    # preconditions : id de professeur unique, nom et prenom
    # postconditions : une ligne dans le tableau PROFESSEUR avec une id de professeur unique, un nom et un prenom
    conn = connect('BDD_projet.db')
    cur = conn.cursor()
    
    # BEGIN SOLUTION
    data = [id, nom, prenom]
    cur.execute(
        "INSERT INTO PROFESSEUR(Id_prof,Nom_prof,Prenom_prof) VALUES(?,?,?)", data
    )
    # END SOLUTION

    conn.commit()
    cur.close()
    conn.close()


def n_option(id_o, matiere, id_p):
    # fonction qui rajoute une matiere avec sont professeur dans la base de donnée
    # preconditions : id d'option unique, nom de matiere et id d'un professeur
    # postconditions : une ligne dans le tableau OPTION avec une id_o unique, nom de matiere et id d'un professeur
    conn = connect('BDD_projet.db')
    cur = conn.cursor()

    # BEGIN SOLUTION
    data = [id_o, matiere, id_p]
    cur.execute(
        "INSERT INTO OPTION(Id_option,Matiere_option,Id_prof) VALUES(?,?,?)", data
    )
    # END SOLUTION

    conn.commit()
    cur.close()
    conn.close()


def n_eleve(id, nom, prenom, ddn, option):
    # fonction qui rajoute un eleve et sont option dans la base de donnée
    # preconditions : id d'un eleve unique, nom, prenom, date de naissance et l'option de l'eleve
    # postconditions : une ligne dans le tableau ELEVE avec l'id d'un eleve, sont nom, sont prenom, sa date de naissance et sont option
    conn = connect('BDD_projet.db')
    cur = conn.cursor()

    # BEGIN SOLUTION
    data = [id, nom, prenom, ddn, option]
    cur.execute(
        "INSERT INTO ELEVE(Id_eleve,Nom_eleve,Prenom_eleve,Ddn_eleve,Id_option) VALUES(?,?,?,?,?)", data
    )
    # END SOLUTION

    conn.commit()
    cur.close()
    conn.close()


def s_eleve(id):
    # fonction qui suprime un eleve de la base de donnée
    # preconditions : id d'un eleve unique
    # postconditions : suprime la ligne de l'eleve ou l'id choisie corespond a sont id
    conn = connect('BDD_projet.db')
    cur = conn.cursor()

    # BEGIN SOLUTION
    cur.execute(
        'DELETE FROM ELEVE WHERE Id_eleve ="' + id+'"'
    )
    # END SOLUTION

    conn.commit()
    cur.close()
    conn.close()


def j_professeur(id, nom, prenom):
    # fonction qui change le nom et prenom du prosseur selectioner dans la base de donnée
    # preconditions : id d'un professeur unique, nom et prenom
    # postconditions : change le nom et prenom du professeur qui a le meme id que l'id choisi
    conn = connect('BDD_projet.db')
    cur = conn.cursor()

    # BEGIN SOLUTION
    cur.execute(
        'UPDATE PROFESSEUR SET Nom_prof = "'+nom +
        '", Prenom_prof = "'+prenom+'" WHERE Id_prof ="'+id+'"'
    )
    # END SOLUTION

    conn.commit()
    cur.close()
    conn.close()


def e_option(option):
    # fonction qui donne la liste des eleve qui on l'option choisie
    # preconditions : id d'une fonction unique
    # postconditions : la liste des eleve dont l'option et la meme que l'option choisie
    conn = connect('BDD_projet.db')
    cur = conn.cursor()

    # BEGIN SOLUTION
    cur.execute(
        'SELECT Nom_eleve, Prenom_eleve FROM ELEVE WHERE Id_option = "'+option+'"'
    )
    resp = cur.fetchall()

    # END SOLUTION
    conn.commit()
    cur.close()
    conn.close()
    return resp


def e_matiere(m):
    # fonction qui donne la liste des eleve qui on la matiere choisi
    # preconditions : nom d'une matiere
    # postconditions : la liste des eleve qui font la matiere choisie
    conn = connect('BDD_projet.db')
    cur = conn.cursor()

    # BEGIN SOLUTION
    cur.execute(
        'SELECT ELEVE.Nom_eleve, ELEVE.Prenom_eleve FROM ELEVE INNER JOIN OPTION WHERE ELEVE.Id_option = OPTION.Id_option AND OPTION.Matiere_option = "'+m+'"'
    )
    resp = cur.fetchall()

    # END SOLUTION
    conn.commit()
    cur.close()
    conn.close()
    return resp


def p_eleve(id):
    # fontion qui donne le professeur d'un eleve
    # preconditions : id d'un eleve
    # postconditions : le professeur d'un eleve
    conn = connect('BDD_projet.db')
    cur = conn.cursor()

    # BEGIN SOLUTION
    cur.execute(
        'SELECT PROFESSEUR.Nom_prof, PROFESSEUR.Prenom_prof FROM PROFESSEUR INNER JOIN OPTION, ELEVE WHERE PROFESSEUR.Id_prof = OPTION.Id_prof AND OPTION.Id_option = ELEVE.Id_option AND ELEVE.Id_eleve = "'+id+'"'
    )
    resp = cur.fetchall()

    # END SOLUTION
    conn.commit()
    cur.close()
    conn.close()
    return resp


@app.route('/')
def menu():
    return render_template("menu.html ")


@app.route('/nouveau-professeur', methods=['POST', 'GET'])
def nouveau_professeur():
    if request.method == 'POST':
        # on obtient la réponse du formulaire sous form d'un dictionnaire.
        reponse = request.form
        # récupération du nom = valeur de la clé 'nom' du dictionnaire
        n = reponse['nom']
        # récupération du prénom = valeur de la clé 'prenom' du dictionnaire
        p = reponse['prenom']
        id = n[:2] + p[:2]
        n_professeur(id, n, p)
        return render_template("nouveau-professeur.html", nom=n, prenom=p, id=id, success=True)
    else:
        return render_template("nouveau-professeur.html")


@app.route('/nouvelle-option', methods=['POST', 'GET'])
def nouvelle_option():
    if request.method == 'POST':
        # on obtient la réponse du formulaire sous form d'un dictionnaire.
        reponse = request.form
        # récupération du nom = valeur de la clé 'matiere' du dictionnaire
        m = reponse['matiere']
        # récupération du prénom = valeur de la clé 'id_p' du dictionnaire
        id_p = reponse['id_p']
        # récupération du prénom = valeur de la clé 'id_o' du dictionnaire
        id_o = reponse['id_o']
        n_option(id_o, m, id_p)
        return render_template("nouvelle-option.html", id_o=id_o, matiere=m, id_p=id_p, success=True)
    else:
        return render_template("nouvelle-option.html")


@app.route('/nouvelle-eleve', methods=['POST', 'GET'])
def nouvelle_eleve():
    if request.method == 'POST':
        # on obtient la réponse du formulaire sous form d'un dictionnaire.
        reponse = request.form
        # récupération du nom = valeur de la clé 'nom' du dictionnaire
        n = reponse['nom']
        # récupération du prénom = valeur de la clé 'prenom' du dictionnaire
        p = reponse['prenom']
        # récupération du prénom = valeur de la clé 'ddn' du dictionnaire
        ddn = reponse['ddn']
        # récupération du prénom = valeur de la clé 'option' du dictionnaire
        option = reponse['option']
        id = n[:2] + p[:2] + ddn[-5] + ddn[-4] + ddn[2] + ddn[3]
        n_eleve(id, n, p, ddn, option)
        return render_template("nouvelle-eleve.html", nom=n, prenom=p, id=id, ddn=ddn, option=option, success=True)

    else:
        return render_template("nouvelle-eleve.html")


@app.route('/supprimer-eleve', methods=['POST', 'GET'])
def supprimer_eleve():
    if request.method == 'POST':
        # on obtient la réponse du formulaire sous form d'un dictionnaire.
        reponse = request.form
        # récupération du nom = valeur de la clé 'id' du dictionnaire
        id = reponse['id']
        s_eleve(id)
        return render_template("supprimer-eleve.html", id=id, success=True)
    else:
        return render_template("supprimer-eleve.html")


@app.route('/jour-professeur', methods=['POST', 'GET'])
def jour_professeur():
    if request.method == 'POST':
        # on obtient la réponse du formulaire sous form d'un dictionnaire.
        reponse = request.form
        # récupération du nom = valeur de la clé 'nom' du dictionnaire
        n = reponse['nom']
        # récupération du prénom = valeur de la clé 'prenom' du dictionnaire
        p = reponse['prenom']
        # récupération du prénom = valeur de la clé 'id' du dictionnaire
        id = reponse['id']
        j_professeur(id, n, p)
        return render_template("jour-professeur.html", nom=n, prenom=p, id=id, success=True)
    else:
        return render_template("jour-professeur.html")


@app.route('/eleve-option', methods=['POST', 'GET'])
def eleve_option():
    if request.method == 'POST':
        # on obtient la réponse du formulaire sous form d'un dictionnaire.
        reponse = request.form
        # récupération du nom = valeur de la clé 'option' du dictionnaire
        option = reponse['option']
        resp = e_option(option)
        return render_template("eleve-option.html", option=option, resp=resp, success=True)
    else:
        return render_template("eleve-option.html")


@app.route('/eleve-matiere', methods=['POST', 'GET'])
def eleve_matiere():
    if request.method == 'POST':
        # on obtient la réponse du formulaire sous form d'un dictionnaire.
        reponse = request.form
        # récupération du nom = valeur de la clé 'matiere' du dictionnaire
        matiere = reponse['matiere']
        resp = e_matiere(matiere)
        return render_template("eleve-matiere.html", matiere=matiere, resp=resp, success=True)
    else:
        return render_template("eleve-matiere.html")


@app.route('/professeur-eleve', methods=['POST', 'GET'])
def professeur_eleve():
    if request.method == 'POST':
        # on obtient la réponse du formulaire sous form d'un dictionnaire.
        reponse = request.form
        # récupération du nom = valeur de la clé 'id' du dictionnaire
        id = reponse['id']
        resp = p_eleve(id)
        return render_template("professeur-eleve.html", id=id, resp=resp, success=True)
    else:
        return render_template("professeur-eleve.html")


# lancement du serveur
app.run()