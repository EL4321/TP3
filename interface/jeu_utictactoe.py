__authors__ = 'Olivier Cardinal et Éric Laflamme'
__date__ = "Ajoutez la date de remise"

"""Ce fichier permet de...(complétez la description de ce que
ce fichier est supposé faire ! """

from tkinter import Tk, Canvas, Label, Entry, Checkbutton, IntVar, Frame, GROOVE, RAISED, messagebox, Button, E, W
from tictactoe.partie import Partie
from tictactoe.joueur import Joueur

class ErreurChoixCase(Exception):
    pass

class EstGagnant(Exception):
    pass

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

        Button(self.canvas_uplateau, text ='Débuter la partie', command =self.demande_confirmation).\
            grid(row =0, column =4)

        self.var = IntVar()
        Checkbutton(self, text= 'VS ordinateur', variable=self.var, onvalue =1, offvalue =0).grid(row =0, column =2)


        # L'entrée du joueur1 est automatiquement demandé
        Label(self.canvas_uplateau, text ="Nom du Joueur 1:").\
            grid(row =0, column =0, sticky=E)
        self.joueur1 = Entry(self.canvas_uplateau, width =14)
        self.joueur1.grid(row =0, column =1, padx=5, pady=5, sticky=E+W)

#        Label (self.canvas_uplateau, text="Le tour: {}".format(self.partie.joueur_courant.nom)).grid(row=3, column=3)

        # L'entrée du joueur2 est selon la checkbox (peut etre l'ordinateur
        Label(self.canvas_uplateau, text ="Nom du Joueur 2:").\
            grid(row =1, column =0, sticky=E)
        self.joueur2 = Entry(self.canvas_uplateau, width =14)
        self.joueur2.grid(row =1, column =1, padx=5, pady=5, sticky=E+W)

        Button(self.canvas_uplateau, text = 'Quitter', command = self.quit).\
            grid (row = 5, column = 4, sticky = E)

        # Création des frames et des canvas du jeu
        for i in range(0, 3):
            for j in range(0, 3):
                cadre = Frame(self, borderwidth=5, relief=GROOVE, background = '#e1e1e1')
                cadre.grid(row=i+3, column=j, padx=5, pady=5)
                cadre.bind('<Enter>', self.entrer_frame)
                cadre.bind('<Leave>', self.sortir_frame)
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
#        p1 = Joueur("VotreNom", "Personne", 'X')
#        p2 = Joueur("Colosse", "Ordinateur", 'O')
#        self.partie.joueurs = [p1,p2]
#        self.partie.joueur_courant = p1

    def selectionner(self, event):
        """
            À completer !.
        """
        print (self.partie.joueur_courant.nom)

        try:

            # On trouve le numéro de ligne/colonne en divisant par le nombre de pixels par case.
            # event.widget représente ici un des 9 canvas !
            ligne = event.y // event.widget.taille_case
            colonne = event.x // event.widget.taille_case

            if not self.partie.uplateau[event.widget.plateau.cordonnees_parent].cases[ligne, colonne].est_vide():
                raise ErreurChoixCase ("La case est déjà sélectionné !")

            self.afficher_message("Case sélectionnée à la position (({},{}),({},{}))."
                                  .format(event.widget.plateau.cordonnees_parent[0],
                                          event.widget.plateau.cordonnees_parent[1],
                                          ligne, colonne))
            self.desactiver_plateau(ligne, colonne)

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

            try:
#Eric           # On vérifie si le joueur courant est gagnant
                if event.widget.plateau.est_gagnant(self.partie.joueur_courant.pion):
                    raise EstGagnant (" Bravo {}, Vous avez gagné un plateau !!!".format (self.partie.joueur_courant.nom))
            except EstGagnant as e:
                messagebox.showwarning("Terminé", str(e))

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

        except ErreurChoixCase as e:
            messagebox.showerror ("Erreur", str(e))

    def desactiver_plateau(self, ligne, colonne):

        for i in range(0, 3):
            for j in range(0, 3):
                if i != ligne or j != colonne:
                    self.canvas_uplateau[i,j]['borderwidth'] = 2
                    self.canvas_uplateau[i,j]['background'] = '#e1e1e1'
                    self.canvas_uplateau[i,j].unbind('<Button-1>')

                else:

                    self.canvas_uplateau[i,j]['borderwidth'] = 2
                    self.canvas_uplateau[i,j]['background'] = 'blue'
                    self.canvas_uplateau[ligne, colonne].bind('<Button-1>', self.selectionner)

    def activer_plateau(self):
        self.canvas_uplateau[0,0].bind('<Button-1>'.self.selectionner)

    def afficher_message(self, message):
        """
            À completer !.
        """
        self.messages['foreground'] = 'black'
        self.messages['text'] = message

    def entrer_frame(self, event):
        event.widget['background'] = 'red'

    def sortir_frame(self, event):
        event.widget['background'] = '#e1e1e1'

    def demande_confirmation(self):

        """
            À compléter !.
        """
        print ('self.var:', self.var.get())     # en provenance du checkbutton (VS ordinateur)
        if self.var.get():                      # la case est cochée pour jouer contre l'ordinateur

            deuxieme_joueur = "Le Gros Colosse"
            type_deuxieme_joueur = "Ordinateur"

        else:       # jouer contre un autre joueur

            deuxieme_joueur = self.joueur2.get()
            type_deuxieme_joueur = "Personne"

        # Création de deux joueurs. Ce code doit être bien sûr modifié,
        # car il faut chercher ces infos dans les widgets de la fenêtre.
        # Vous pouvez également déplacer ce code dans une autre méthode selon votre propre solution.
        p1 = Joueur(self.joueur1.get(), "Personne", 'X')
        p2 = Joueur(deuxieme_joueur, type_deuxieme_joueur, 'O')
        self.partie.joueurs = [p1,p2]
        self.partie.joueur_courant = p1

        self.joueur1['state'] = 'disabled'
        self.joueur2['state'] = 'disabled'