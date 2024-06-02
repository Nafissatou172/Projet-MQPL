# This is a sample Python script.

# Press Maj+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


# Press Ctrl+F8 to toggle the breakpoint.

# Projet de Mesures Qualite et Performance logiciel
# PARTIE A : Conception et Implementation
# 1) Definition des classes principales  ainsi que des methodes necessaires pour les besoins fonctionnelles :

from datetime import datetime
from typing import List, Optional
import unittest


class Membre:
    def __init__(self, nom: str, role: str):
        self.nom = nom
        self.role = role


class Equipe:
    def __init__(self):
        self.membres = []

    def ajouter_membre(self, membre: Membre):
        self.membres.append(membre)

    def obtenir_membres(self) -> List[Membre]:
        return self.membres


class Tache:
    def __init__(
        self,
        nom: str,
        description: str,
        date_debut: datetime,
        date_fin: datetime,
        responsable: Membre,
        statut: str,
    ):
        self.nom = nom
        self.description = description
        self.date_debut = date_debut
        self.date_fin = date_fin
        self.responsable = responsable
        self.statut = statut
        self.dependances = []

    def ajouter_dependance(self, tache: "Tache"):
        self.dependances.append(tache)

    def mettre_a_jour_statut(self, statut: str):
        self.statut = statut


class Jalon:
    def __init__(self, nom: str, date: datetime):
        self.nom = nom
        self.date = date


class Risque:
    def __init__(self, description: str, probabilite: float, impact: str):
        self.description = description
        self.probabilite = probabilite
        self.impact = impact


class Changement:
    def __init__(self, description: str, version: int, date: datetime):
        self.description = description
        self.version = version
        self.date = date


class Projet:
    def __init__(
        self,
        nom: str,
        description: str,
        date_debut: datetime,
        date_fin: datetime,
        budget: float,
    ):
        self.nom = nom
        self.description = description
        self.date_debut = date_debut
        self.date_fin = date_fin
        self.budget = budget
        self.taches = []
        self.equipe = Equipe()
        self.risques = []
        self.jalons = []
        self.changements = []
        self.version = 1
        self.chemin_critique = []
        self.notification_context = NotificationContext(EmailNotificationStrategy())

    def set_notification_strategy(self, strategy: "NotificationStrategy"):
        self.notification_context = NotificationContext(strategy)

    # methode ajouter une tache qui permet aussi de notifier lors de l'ajout
    def ajouter_tache(self, tache: Tache):
        self.taches.append(tache)
        self.notifier(
            f"Nouvelle tâche ajoutée: {tache.nom}", self.equipe.obtenir_membres()
        )

    # methode ajouter des membres au projet qui permet aussi de notifier lorsqu'un membre est ajoute
    def ajouter_membre(self, membre: Membre):
        self.equipe.ajouter_membre(membre)
        self.notifier(
            f"Nouveau membre ajouté: {membre.nom}", self.equipe.obtenir_membres()
        )

    def definir_budget(self, budget: float):
        self.budget = budget

    # methode ajouter risque qui permet aussi de notifier lorsqu'un nouveau risque est ajoute
    def ajouter_risque(self, risque: Risque):
        self.risques.append(risque)
        self.notifier(
            f"Nouveau risque ajouté: {risque.description}",
            self.equipe.obtenir_membres(),
        )

    # methode ajouter jalons qui permet aussi de notifier lorsqu'un jalon est ajoute
    def ajouter_jalon(self, jalon: Jalon):
        self.jalons.append(jalon)
        self.notifier(
            f"Nouveau jalon ajouté: {jalon.nom}", self.equipe.obtenir_membres()
        )

    # methode pour enregistrer des changements
    def enregistrer_changement(self, description: str):
        changement = Changement(description, self.version, datetime.now())
        self.changements.append(changement)
        self.version += 1
        self.notifier(
            f"Nouveau changement enregistré: {changement.description}",
            self.equipe.obtenir_membres(),
        )

    def generer_rapport_performance(self):
        rapport = f"Rapport du projet {self.nom}:\n"
        rapport += f"Description: {self.description}\n"
        rapport += f"Date de début: {self.date_debut}\n"
        rapport += f"Date de fin: {self.date_fin}\n"
        rapport += f"Budget: {self.budget}\n"
        rapport += "Tâches:\n"
        for tache in self.taches:
            rapport += f"  - {tache.nom}: {tache.description} (Responsable: {tache.responsable.nom}, Statut: {tache.statut})\n"
        rapport += "Membres de l'équipe:\n"
        for membre in self.equipe.obtenir_membres():
            rapport += f"  - {membre.nom} ({membre.role})\n"
        rapport += "Risques:\n"
        for risque in self.risques:
            rapport += f"  - {risque.description} (Probabilité: {risque.probabilite}, Impact: {risque.impact})\n"
        rapport += "Jalons:\n"
        for jalon in self.jalons:
            rapport += f"  - {jalon.nom} (Date: {jalon.date})\n"
        rapport += "Changements:\n"
        for changement in self.changements:
            rapport += f"  - {changement.description} (Version: {changement.version}, Date: {changement.date})\n"
        return rapport

    def calculer_chemin_critique(self):
        def find_longest_path(tache, memo):
            if tache in memo:
                return memo[tache]
            if not tache.dependances:
                memo[tache] = (0, [tache])
                return memo[tache]
            max_length, max_path = 0, []
            for dep in tache.dependances:
                dep_length, dep_path = find_longest_path(dep, memo)
                if dep_length > max_length:
                    max_length = dep_length
                    max_path = dep_path
            total_length = max_length + (tache.date_fin - tache.date_debut).days
            memo[tache] = (total_length, max_path + [tache])
            return memo[tache]

        memo = {}
        all_paths = [find_longest_path(tache, memo) for tache in self.taches]
        self.chemin_critique = max(all_paths, key=lambda x: x[0])[1]

    def notifier(self, message: str, destinataires: List[Membre]): 
        self.notification_context.notifier(message, destinataires)


# 2) Gestion des Notifications avec le pattern strategy
from abc import ABC, abstractmethod


class NotificationStrategy(ABC):
    @abstractmethod
    def envoyer(self, message: str, destinataire: Membre):
        pass


class EmailNotificationStrategy(NotificationStrategy):
    def envoyer(self, message: str, destinataire: Membre):
        print(f"Envoi d'un email à {destinataire.nom}: {message}")


class SMSNotificationStrategy(NotificationStrategy):
    def envoyer(self, message: str, destinataire: Membre):
        print(f"Envoi d'un SMS à {destinataire.nom}: {message}")


class PushNotificationStrategy(NotificationStrategy):
    def envoyer(self, message: str, destinataire: Membre):
        print(f"Envoi d'une notification push à {destinataire.nom}: {message}")


class NotificationContext:
    def __init__(self, strategy: NotificationStrategy):
        self._strategy = strategy

    def notifier(self, message: str, destinataires: List[Membre]):
        for destinataire in destinataires:
            self._strategy.envoyer(message, destinataire)


# Exemple d'utilisation :
# Création d'un projet
projet = Projet(
    nom="MEVC",
    description="Projet operationel de fin de cycle",
    date_debut=datetime(2024, 1, 28),
    date_fin=datetime(2024, 4, 30),
    budget=100000,
)

# Ajout de membres à l'équipe
membre1 = Membre(nom="Nafissatou Sow", role="Chef de projet")
membre2 = Membre(nom="Mohameth Mbaye ", role="Développeur")
projet.ajouter_membre(membre1)
projet.ajouter_membre(membre2)

# Ajout de tâches au projet
tache1 = Tache(
    nom="Tâche 1",
    description="Implementer un systeme de notification par email",
    date_debut=datetime(2024, 2, 10),
    date_fin=datetime(2024, 2, 20),
    responsable=membre1,
    statut="En cours",
)
tache2 = Tache(
    nom="Tâche 2",
    description="Implementer la page de connexion",
    date_debut=datetime(2024, 3, 2),
    date_fin=datetime(2024, 3, 8),
    responsable=membre2,
    statut="Pas commencé",
)
projet.ajouter_tache(tache1)
projet.ajouter_tache(tache2)

# Génération du rapport de performance
print(projet.generer_rapport_performance())


# Partie B : Test , Mesure et Qualite du code :
class TestProjet(unittest.TestCase):

    def setUp(self):
        self.projet = Projet(
            nom="MEVC",
            description="Projet operationel de fin de cycle",
            date_debut=datetime(2024, 1, 28),
            date_fin=datetime(2024, 4, 30),
            budget=100000,
        )
        self.membre1 = Membre(nom="Nafissatou Sow", role="Chef de projet")
        self.membre2 = Membre(nom="Mohameth Mbaye", role="Développeur")
        self.tache1 = Tache(
            nom="Tâche 1",
            description="Implementer un systeme de notification par email",
            date_debut=datetime(2024, 2, 10),
            date_fin=datetime(2024, 2, 20),
            responsable=self.membre1,
            statut="En cours",
        )
        self.tache2 = Tache(
            nom="Tâche 2",
            description="Implementer la page de connexion",
            date_debut=datetime(2024, 3, 2),
            date_fin=datetime(2024, 3, 8),
            responsable=self.membre2,
            statut="Pas commencé",
        )

    def test_ajouter_membre(self):
        self.projet.ajouter_membre(self.membre1)
        self.assertIn(self.membre1, self.projet.equipe.obtenir_membres())
        self.projet.ajouter_membre(self.membre2)
        self.assertIn(self.membre2, self.projet.equipe.obtenir_membres())

    def test_ajouter_tache(self):
        self.projet.ajouter_tache(self.tache1)
        self.assertIn(self.tache1, self.projet.taches)
        self.projet.ajouter_tache(self.tache2)
        self.assertIn(self.tache2, self.projet.taches)

    def test_generer_rapport_performance(self):
        self.projet.ajouter_membre(self.membre1)
        self.projet.ajouter_tache(self.tache1)
        rapport = self.projet.generer_rapport_performance()
        self.assertIn("Rapport du projet MEVC:", rapport)
        self.assertIn("Nafissatou Sow", rapport)
        self.assertIn("Tâche 1", rapport)


unittest.main()


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
