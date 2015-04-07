__authors__ = 'Ajoutez les noms des membres de votre équipe!'
__date__ = "Ajoutez la date de remise"

"""Ce fichier permet de...(complétez la description de ce que
ce fichier est supposé faire ! """

from tkinter import Tk, Canvas, Label, Frame, GROOVE
from tictactoe.partie import Partie
from tictactoe.joueur import Joueur


class CanvasPlateau(Canvas):
    """
        À completer !.
    """
    def __init__(self, parent, plateau, taille_case=60):

        # Une instance d'un des 9 plateaux du jeu ultimate Tic-Tac-Toe.
        self.plateau = plateau

        # Nombre de pixels par case.
        self.taille_case = taille_case

        # Appel du constructeur de la classe de base (Canvas).
        super().__init__(parent, width=self.plateau.n_lignes * taille_case,
                         height=self.plateau.n_colonnes * self.taille_case)

        # Dessiner le plateau du jeu ultimate Tic-Tac-Toe.
        self.dessiner_plateau()


    def dessiner_plateau(self):
        """
            À completer !.
        """
        for i in range(self.plateau.n_lignes):
            for j in range(self.plateau.n_colonnes):
                debut_ligne = i * self.taille_case
                fin_ligne = debut_ligne + self.taille_case
                debut_colonne = j * self.taille_case
                fin_colonne = debut_colonne + self.taille_case
                # On dessine le rectangle représentant une case!
                self.create_rectangle(debut_colonne, debut_ligne, fin_colonne, fin_ligne,
                                      fill='#e1e1e1', width = 2, outline = "white")


class Fenetre(Tk):
    """
        À completer !.
    """
    def __init__(self):
        """
            À completer !.
        """
        super().__init__()

        # Nom de la fenêtre.
        self.title("Ultimate Tic-Tac-Toe")

        # La partie de ultimate Tic-Tac-Toe
        self.partie = Partie()

        # Un ditionnaire contenant les 9 canvas des 9 plateaux du jeu
        self.canvas_uplateau = {}

        # Création des frames et des canvas du jeu
        for i in range(0, 3):
            for j in range(0, 3):
                cadre = Frame(self, borderwidth=5, relief=GROOVE)
                cadre.grid(row=i, column=j, padx=5, pady=5)
                self.canvas_uplateau[i,j] = CanvasPlateau(cadre, self.partie.uplateau[i,j])
                self.canvas_uplateau[i,j].grid()
                # On lie un clic sur le Canvas à une méthode.
                self.canvas_uplateau[i,j].bind('<Button-1>', self.selectionner)

        # Ajout d'une étiquette d'information.
        self.messages = Label(self)
        self.messages.grid(columnspan=3)

        # Création de deux joueurs. Ce code doit être bien sûr modifié,
        # car il faut chercher ces infos dans les widgets de la fenêtre.
        # Vous pouvez également déplacer ce code dans une autre méthode selon votre propre solution.
        p1 = Joueur("VotreNom", "Personne", 'X')
        p2 = Joueur("Colosse", "Ordinateur", 'O')
        self.partie.joueurs = [p1,p2]
        self.partie.joueur_courant = p1

    def selectionner(self, event):
        """
            À completer !.
        """
        # On trouve le numéro de ligne/colonne en divisant par le nombre de pixels par case.
        # event.widget représente ici un des 9 canvas !
        ligne = event.y // event.widget.taille_case
        colonne = event.x // event.widget.taille_case

        self.afficher_message("Case sélectionnée à la position (({},{}),({},{}))."
                              .format(event.widget.plateau.cordonnees_parent[0],
                                      event.widget.plateau.cordonnees_parent[1],
                                      ligne, colonne))

        # On dessine le pion dans le canvas, au centre de la case.
        # On utilise l'attribut "tags" pour être en mesure de récupérer
        # les éléments dans le canvas afin de les effacer par exemple.
        coordonnee_y = ligne * event.widget.taille_case + event.widget.taille_case // 2
        coordonnee_x = colonne * event.widget.taille_case + event.widget.taille_case // 2
        event.widget.create_text(coordonnee_x, coordonnee_y, text=self.partie.joueur_courant.pion,
                                 font=('Helvetica', event.widget.taille_case//2), tags='pion')

        # Mettre à jour la case sélectionnée
        self.partie.uplateau[event.widget.plateau.cordonnees_parent]\
            .selectionner_case(ligne, colonne, self.partie.joueur_courant.pion)

        # Changer le joueur courant.
        # Vous pouvez modifier ou déplacer ce code dans une autre méthode selon votre propre solution.
        if self.partie.joueur_courant == self.partie.joueurs[0]:
            self.partie.joueur_courant = self.partie.joueurs[1]
        else:
            self.partie.joueur_courant = self.partie.joueurs[0]

        # Effacer le contenu du widget (canvas) et du plateau (dictionnaire) quand ce dernier devient plein.
        # Vous pouvez modifier ou déplacer ce code dans une autre méthode selon votre propre solution.
        if not event.widget.plateau.non_plein():
            event.widget.delete('pion')
            event.widget.plateau.initialiser()

    def afficher_message(self, message):
        """
            À completer !.
        """
        self.messages['foreground'] = 'black'
        self.messages['text'] = message

