import tkinter as tk
from tkinter import ttk, filedialog, messagebox

import numpy as np
import matplotlib.pyplot as plt

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import pandas as pd


class SmartBuildingExplorer:
    """Interface graphique d'exploration du dataset Smart Building."""

    THEMES = {
        "clair": {
            "background": "#f5f5f5",
            "surface": "#ffffff",
            "foreground": "#202020",
            "secondary": "#666666",
            "border": "#d0d0d0",
        },
        "sombre": {
            "background": "#1e1e1e",
            "surface": "#2b2b2b",
            "foreground": "#f2f2f2",
            "secondary": "#b0b0b0",
            "border": "#444444",
        },
    }

    def __init__(self, fenetre):
        self.fenetre = fenetre

        self.fenetre.title("Smart Building Data Explorer")
        self.fenetre.geometry("1100x700")
        self.fenetre.minsize(800, 500)

        self.df = None
        self.chemin_fichier = None
        self.theme = "clair"
        self.canvas = None

        self._configurer_fenetre()
        self._creer_styles()
        self._creer_interface()

        self._creer_tableau_donnees()
        self._creer_analyse()

        self._appliquer_theme()

    def _configurer_fenetre(self):
        self.fenetre.columnconfigure(0, weight=1)
        self.fenetre.rowconfigure(0, weight=1)

    def _creer_styles(self):
        self.style = ttk.Style()

        # Utilisation du thème ttk disponible sur le système
        try:
            self.style.theme_use("clam")
        except tk.TclError:
            pass

    def _creer_interface(self):
        self.conteneur = ttk.Frame(
            self.fenetre,
            padding=10
        )

        self.conteneur.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        self.conteneur.columnconfigure(0, weight=1)
        self.conteneur.rowconfigure(2, weight=1)

        # -------------------------
        # En-tête
        # -------------------------

        self.entete = ttk.Frame(
            self.conteneur
        )

        self.entete.grid(
            row=0,
            column=0,
            sticky="ew",
            pady=(0, 10)
        )

        self.entete.columnconfigure(1, weight=1)

        self.titre = ttk.Label(
            self.entete,
            text="",
            font=("Arial", 20, "bold")
        )

        self.titre.grid(
            row=0,
            column=0,
            sticky="w"
        )

        self.bouton_theme = ttk.Button(
            self.entete,
            text="☾ Mode sombre",
            command=self._changer_theme
        )

        self.bouton_theme.grid(
            row=0,
            column=2,
            sticky="e"
        )

        # -------------------------
        # Barre d'actions
        # -------------------------

        self.barre_actions = ttk.Frame(
            self.conteneur
        )

        self.barre_actions.grid(
            row=1,
            column=0,
            sticky="ew",
            pady=(0, 10)
        )

        self.barre_actions.columnconfigure(1, weight=1)

        self.bouton_charger = ttk.Button(
            self.barre_actions,
            text="Charger un CSV",
            command=self._charger_dataset
        )

        self.bouton_charger.grid(
            row=0,
            column=0,
            padx=(0, 10)
        )

        self.statut = ttk.Label(
            self.barre_actions,
            text="Aucun dataset chargé."
        )

        self.statut.grid(
            row=0,
            column=1,
            sticky="w"
        )

        # -------------------------
        # Onglets
        # -------------------------

        self.onglets = ttk.Notebook(
            self.conteneur
        )

        self.onglets.grid(
            row=2,
            column=0,
            sticky="nsew"
        )

        self.dashboard = ttk.Frame(
            self.onglets,
            padding=15
        )

        self.donnees = ttk.Frame(
            self.onglets,
            padding=15
        )

        self.analyse = ttk.Frame(
            self.onglets,
            padding=15
        )

        self.onglets.add(
            self.dashboard,
            text="Dashboard"
        )

        self.onglets.add(
            self.donnees,
            text="Données"
        )

        self.onglets.add(
            self.analyse,
            text="Analyse"
        )

        self._creer_dashboard()

    def _charger_dataset(self):
        chemin = filedialog.askopenfilename(
            title="Sélectionner un dataset CSV",
            filetypes=[
                ("Fichiers CSV", "*.csv"),
                ("Tous les fichiers", "*.*")
            ]
        )

        if not chemin:
            return

        try:
            self.df = pd.read_csv(chemin)
            self.chemin_fichier = chemin

            nom_fichier = chemin.replace("\\", "/").split("/")[-1]

            self.statut.config(
                text=f"Dataset chargé : {nom_fichier}"
            )

            self._mettre_a_jour_dashboard()
            self._mettre_a_jour_tableau()
            self._mettre_a_jour_analyse()

        except Exception as erreur:
            messagebox.showerror(
                "Erreur de chargement",
                f"Impossible de charger le fichier.\n\n{erreur}"
            )

    def _changer_theme(self):
        if self.theme == "clair":
            self.theme = "sombre"
        else:
            self.theme = "clair"

        self._appliquer_theme()

        if self.df is not None and self.variable_selectionnee.get():
            self._analyser_variable()

    def _appliquer_theme(self):
        couleurs = self.THEMES[self.theme]

        self.fenetre.configure(
            background=couleurs["background"]
        )

        self.style.configure(
            ".",
            background=couleurs["background"],
            foreground=couleurs["foreground"]
        )

        self.style.configure(
            "TFrame",
            background=couleurs["background"]
        )

        self.style.configure(
            "TLabel",
            background=couleurs["background"],
            foreground=couleurs["foreground"]
        )

        self.style.configure(
            "TButton",
            background=couleurs["surface"],
            foreground=couleurs["foreground"],
            bordercolor=couleurs["border"]
        )

        self.style.map(
            "TButton",
            background=[
                ("active", couleurs["border"]),
                ("pressed", couleurs["border"])
            ],
            foreground=[
                ("active", couleurs["foreground"]),
                ("pressed", couleurs["foreground"])
            ]
        )

        self.style.configure(
            "TNotebook",
            background=couleurs["background"],
            bordercolor=couleurs["border"]
        )

        self.style.configure(
            "TNotebook.Tab",
            background=couleurs["surface"],
            foreground=couleurs["foreground"]
        )

        self.style.map(
            "TNotebook.Tab",
            background=[
                ("selected", couleurs["border"]),
                ("active", couleurs["border"])
            ],
            foreground=[
                ("selected", couleurs["foreground"]),
                ("active", couleurs["foreground"])
            ]
        )

        self.style.configure(
            "TLabelframe",
            background=couleurs["background"],
            foreground=couleurs["foreground"]
        )

        self.style.configure(
            "TLabelframe.Label",
            background=couleurs["background"],
            foreground=couleurs["foreground"]
        )

        self.style.configure(
            "TCombobox",
            fieldbackground=couleurs["surface"],
            background=couleurs["surface"],
            foreground=couleurs["foreground"]
        )

        self.style.map(
            "TCombobox",
            fieldbackground=[
                ("readonly", couleurs["surface"])
            ],
            foreground=[
                ("readonly", couleurs["foreground"])
            ],
            selectbackground=[
                ("readonly", couleurs["border"])
            ],
            selectforeground=[
                ("readonly", couleurs["foreground"])
            ]
        )

        # -------------------------
        # Tableau de données
        # -------------------------

        self.style.configure(
            "Treeview",
            background=couleurs["surface"],
            fieldbackground=couleurs["surface"],
            foreground=couleurs["foreground"],
            bordercolor=couleurs["border"]
        )

        self.style.map(
            "Treeview",
            background=[
                ("selected", couleurs["border"])
            ],
            foreground=[
                ("selected", couleurs["foreground"])
            ]
        )

        self.style.configure(
            "Treeview.Heading",
            background=couleurs["surface"],
            foreground=couleurs["foreground"],
            bordercolor=couleurs["border"]
        )

        self.style.map(
            "Treeview.Heading",
            background=[
                ("active", couleurs["border"])
            ],
            foreground=[
                ("active", couleurs["foreground"])
            ]
        )

        if self.theme == "sombre":
            self.bouton_theme.config(
                text="☀ Mode clair"
            )
        else:
            self.bouton_theme.config(
                text="☾ Mode sombre"
            )

    def _creer_dashboard(self):
        self.dashboard.columnconfigure(0, weight=1)
        self.dashboard.columnconfigure(1, weight=1)
        self.dashboard.rowconfigure(0, weight=1)
        self.dashboard.rowconfigure(1, weight=1)
        self.dashboard.rowconfigure(2, weight=1)

        self.indicateurs = {}

        indicateurs = [
            ("lignes", "Lignes"),
            ("colonnes", "Colonnes"),
            ("manquants", "Valeurs manquantes"),
            ("doublons", "Doublons"),
        ]

        for index, (cle, titre) in enumerate(indicateurs):
            ligne = index // 2
            colonne = index % 2

            cadre = ttk.LabelFrame(
                self.dashboard,
                text=titre,
                padding=20
            )

            cadre.grid(
                row=ligne,
                column=colonne,
                padx=10,
                pady=10,
                sticky="nsew"
            )

            cadre.columnconfigure(0, weight=1)
            cadre.rowconfigure(0, weight=1)

            valeur = ttk.Label(
                cadre,
                text="—",
                font=("Arial", 24, "bold")
            )

            valeur.grid(
                row=0,
                column=0
            )

            self.indicateurs[cle] = valeur

        self.cadre_alerte = ttk.LabelFrame(
            self.dashboard,
            text="Répartition de alerte",
            padding=20
        )

        self.cadre_alerte.grid(
            row=2,
            column=0,
            columnspan=2,
            padx=10,
            pady=10,
            sticky="nsew"
        )

        self.alerte_resultat = ttk.Label(
            self.cadre_alerte,
            text="Aucune donnée chargée."
        )

        self.alerte_resultat.pack(
            expand=True
        )

    def _mettre_a_jour_dashboard(self):
        if self.df is None:
            return

        self.indicateurs["lignes"].config(
            text=f"{len(self.df):,}"
        )

        self.indicateurs["colonnes"].config(
            text=f"{len(self.df.columns):,}"
        )

        nombre_manquants = self.df.isna().sum().sum()

        self.indicateurs["manquants"].config(
            text=f"{nombre_manquants:,}"
        )

        nombre_doublons = self.df.duplicated().sum()

        self.indicateurs["doublons"].config(
            text=f"{nombre_doublons:,}"
        )

        if "alerte" in self.df.columns:
            repartition = (
                self.df["alerte"]
                .value_counts(normalize=True)
                .mul(100)
                .round(1)
            )

            texte = "\n".join(
                f"{classe} : {pourcentage} %"
                for classe, pourcentage in repartition.items()
            )

            self.alerte_resultat.config(
                text=texte
            )
        else:
            self.alerte_resultat.config(
                text="La colonne 'alerte' n'est pas présente."
            )

    def _creer_tableau_donnees(self):
        self.donnees.columnconfigure(0, weight=1)
        self.donnees.rowconfigure(0, weight=1)

        conteneur_tableau = ttk.Frame(
            self.donnees
        )

        conteneur_tableau.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        conteneur_tableau.columnconfigure(0, weight=1)
        conteneur_tableau.rowconfigure(0, weight=1)

        self.tableau = ttk.Treeview(
            conteneur_tableau,
            show="headings"
        )

        self.scroll_verticale = ttk.Scrollbar(
            conteneur_tableau,
            orient="vertical",
            command=self.tableau.yview
        )

        self.scroll_horizontale = ttk.Scrollbar(
            conteneur_tableau,
            orient="horizontal",
            command=self.tableau.xview
        )

        self.tableau.configure(
            yscrollcommand=self.scroll_verticale.set,
            xscrollcommand=self.scroll_horizontale.set
        )

        self.tableau.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        self.scroll_verticale.grid(
            row=0,
            column=1,
            sticky="ns"
        )

        self.scroll_horizontale.grid(
            row=1,
            column=0,
            sticky="ew"
        )

    def _mettre_a_jour_tableau(self):
        if self.df is None:
            return

        self.tableau.delete(
            *self.tableau.get_children()
        )

        colonnes = list(self.df.columns)

        self.tableau["columns"] = colonnes

        for colonne in colonnes:
            self.tableau.heading(
                colonne,
                text=colonne
            )

            self.tableau.column(
                colonne,
                width=130,
                minwidth=80,
                anchor="center"
            )

        for _, ligne in self.df.iterrows():
            valeurs = [
                "" if pd.isna(valeur) else valeur
                for valeur in ligne
            ]

            self.tableau.insert(
                "",
                "end",
                values=valeurs
            )

    def _creer_analyse(self):
        self.analyse.columnconfigure(0, weight=1)
        self.analyse.rowconfigure(1, weight=1)

        # -------------------------
        # Barre d'analyse
        # -------------------------

        barre_analyse = ttk.Frame(
            self.analyse
        )

        barre_analyse.grid(
            row=0,
            column=0,
            sticky="ew",
            pady=(0, 10)
        )

        barre_analyse.columnconfigure(1, weight=1)

        self.label_variable = ttk.Label(
            barre_analyse,
            text="Variable à analyser :"
        )

        self.label_variable.grid(
            row=0,
            column=0,
            padx=(0, 10)
        )

        self.variable_selectionnee = tk.StringVar()

        self.selecteur_variable = ttk.Combobox(
            barre_analyse,
            textvariable=self.variable_selectionnee,
            state="readonly"
        )

        self.selecteur_variable.grid(
            row=0,
            column=1,
            sticky="ew"
        )

        self.bouton_analyser = ttk.Button(
            barre_analyse,
            text="Analyser",
            command=self._analyser_variable
        )

        self.bouton_analyser.grid(
            row=0,
            column=2,
            padx=(10, 0)
        )

        self.bouton_correlation = ttk.Button(
            barre_analyse,
            text="Corrélations",
            command=self._afficher_correlation
        )

        self.bouton_correlation.grid(
            row=0,
            column=3,
            padx=(10, 0)
        )

        # -------------------------
        # Zone d'analyse
        # -------------------------

        self.resultat_analyse = ttk.LabelFrame(
            self.analyse,
            text="Analyse",
            padding=10
        )

        self.resultat_analyse.grid(
            row=1,
            column=0,
            sticky="nsew"
        )

        self.resultat_analyse.columnconfigure(0, weight=1)
        self.resultat_analyse.rowconfigure(1, weight=1)

        self.statistiques = ttk.Label(
            self.resultat_analyse,
            text="Chargez un dataset pour commencer l'analyse.",
            justify="left"
        )

        self.statistiques.grid(
            row=0,
            column=0,
            sticky="w",
            pady=(0, 10)
        )

        self.zone_graphique = ttk.Frame(
            self.resultat_analyse
        )

        self.zone_graphique.grid(
            row=1,
            column=0,
            sticky="nsew"
        )

        self.zone_graphique.columnconfigure(0, weight=1)
        self.zone_graphique.rowconfigure(0, weight=1)

    def _mettre_a_jour_analyse(self):
        if self.df is None:
            return

        colonnes = list(self.df.columns)

        self.selecteur_variable["values"] = colonnes

        if colonnes:
            self.selecteur_variable.current(0)

            self.statistiques.config(
                text=(
                    "Sélectionnez une variable puis cliquez sur "
                    "« Analyser »."
                )
            )

            self._nettoyer_graphique()

    def _analyser_variable(self):
        if self.df is None:
            return

        variable = self.variable_selectionnee.get()

        if not variable:
            return

        serie = self.df[variable]

        self._nettoyer_graphique()

        if pd.api.types.is_numeric_dtype(serie):
            self._analyser_numerique(
                variable,
                serie
            )
        else:
            self._analyser_categorielle(
                variable,
                serie
            )

    def _analyser_numerique(self, variable, serie):
        moyenne = serie.mean()
        mediane = serie.median()
        ecart_type = serie.std()
        minimum = serie.min()
        maximum = serie.max()

        texte = (
            f"Variable : {variable}\n\n"
            f"Moyenne : {moyenne:.2f}\n"
            f"Médiane : {mediane:.2f}\n"
            f"Écart-type : {ecart_type:.2f}\n"
            f"Minimum : {minimum:.2f}\n"
            f"Maximum : {maximum:.2f}"
        )

        self.statistiques.config(
            text=texte
        )

        valeurs = serie.dropna()

        figure, axe = plt.subplots(
            figsize=(7, 4)
        )

        axe.hist(
            valeurs,
            bins=20,
            edgecolor="black"
        )

        axe.set_title(
            f"Distribution de {variable}"
        )

        axe.set_xlabel(variable)
        axe.set_ylabel("Fréquence")

        self._configurer_graphique(
            figure,
            axe
        )

        figure.tight_layout()

        self.canvas = FigureCanvasTkAgg(
            figure,
            master=self.zone_graphique
        )

        self.canvas.draw()

        self.canvas.get_tk_widget().grid(
            row=0,
            column=0,
            sticky="nsew"
        )

    def _analyser_categorielle(self, variable, serie):
        frequences = (
            serie
            .fillna("Valeur manquante")
            .value_counts()
            .head(15)
        )

        texte = (
            f"Variable : {variable}\n\n"
            f"Nombre de catégories : "
            f"{serie.nunique(dropna=True)}"
        )

        self.statistiques.config(
            text=texte
        )

        figure, axe = plt.subplots(
            figsize=(7, 4)
        )

        frequences.sort_values().plot.barh(
            ax=axe
        )

        axe.set_title(
            f"Fréquence de {variable}"
        )

        axe.set_xlabel("Nombre d'occurrences")
        axe.set_ylabel(variable)

        self._configurer_graphique(
            figure,
            axe
        )

        figure.tight_layout()

        self.canvas = FigureCanvasTkAgg(
            figure,
            master=self.zone_graphique
        )

        self.canvas.draw()

        self.canvas.get_tk_widget().grid(
            row=0,
            column=0,
            sticky="nsew"
        )

    def _afficher_correlation(self):
        if self.df is None:
            return

        variables_numeriques = self.df.select_dtypes(
            include="number"
        )

        if variables_numeriques.shape[1] < 2:
            messagebox.showinfo(
                "Corrélation",
                "Il faut au moins deux variables numériques."
            )
            return

        correlation = variables_numeriques.corr()

        self._nettoyer_graphique()

        figure, axe = plt.subplots(
            figsize=(8, 6)
        )

        image = axe.imshow(
            correlation,
            vmin=-1,
            vmax=1,
            aspect="auto"
        )

        axe.set_xticks(
            range(len(correlation.columns))
        )

        axe.set_yticks(
            range(len(correlation.columns))
        )

        axe.set_xticklabels(
            correlation.columns,
            rotation=45,
            ha="right"
        )

        axe.set_yticklabels(
            correlation.columns
        )

        figure.colorbar(
            image,
            ax=axe,
            label="Corrélation"
        )

        axe.set_title(
            "Matrice de corrélation"
        )

        self._configurer_graphique(
            figure,
            axe
        )

        figure.tight_layout()

        self.canvas = FigureCanvasTkAgg(
            figure,
            master=self.zone_graphique
        )

        self.canvas.draw()

        self.canvas.get_tk_widget().grid(
            row=0,
            column=0,
            sticky="nsew"
        )

    def _nettoyer_graphique(self):
        for widget in self.zone_graphique.winfo_children():
            widget.destroy()

        if self.canvas is not None:
            plt.close(self.canvas.figure)
            self.canvas = None

    def _configurer_graphique(self, figure, axe):
        couleurs = self._couleurs_graphique()

        figure.patch.set_facecolor(
            couleurs["fond"]
        )

        axe.set_facecolor(
            couleurs["fond"]
        )

        axe.tick_params(
            colors=couleurs["texte"]
        )

        for bordure in axe.spines.values():
            bordure.set_color(
                couleurs["grille"]
            )

        axe.title.set_color(
            couleurs["texte"]
        )

        axe.xaxis.label.set_color(
            couleurs["texte"]
        )

        axe.yaxis.label.set_color(
            couleurs["texte"]
        )

        # Les graduations et les textes doivent également suivre le thème
        for etiquette in axe.get_xticklabels():
            etiquette.set_color(
                couleurs["texte"]
            )

        for etiquette in axe.get_yticklabels():
            etiquette.set_color(
                couleurs["texte"]
            )

    def _couleurs_graphique(self):
        if self.theme == "sombre":
            return {
                "fond": "#2b2b2b",
                "texte": "#f2f2f2",
                "grille": "#555555"
            }

        return {
            "fond": "#ffffff",
            "texte": "#202020",
            "grille": "#dddddd"
        }


def main():
    fenetre = tk.Tk()

    SmartBuildingExplorer(fenetre)

    fenetre.mainloop()


if __name__ == "__main__":
    main()
