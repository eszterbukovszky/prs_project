# Autorin: Eszter Bukovszky, Datum: 30.09.2024
# Zweck der Datei: Funktionen für: Initialisierung der Leistungsübersicht und
# Energiepunkte für das Spiel, Noteneintragung(+Schokolade und Ausruhen) und
# zufällige Events, Erhalten der Evaluation, Starten eines neuen Spiels,
# Verwaltung von den User-Interaktionen.
# Quellen: NLTK names corpus, random-Modul

import random
from nltk.corpus import names
import nltk
nltk.download('names')


def leistungsuebersicht_erstellen():
    """
    Erstellt eine Leistungsübersicht mit 8 zufällig ausgewählten Studenten,
    Energiepunkten und Evaluationspunkten. Zu jedem Studenten gehören genau
    2 Noten, die im Laufe des Spiels eingetragen werden können.

    Return:
        dict: die Leistungsübersicht, die die oben genannten Informationen
        enthält.
    """
    studenten = random.sample(names.words(), 8)  # 8 random Namen auswählen.
    # Die Leistungsübersicht mit leeren Noten wird erstellt.
    leistungsuebersicht = {
        "Energiepunkte": 10,
        "Evaluationspunkte": 0,
        "Studenten": {student: {"1. Note": None, "2. Note": None}
                      for student in studenten}
    }
    return leistungsuebersicht


def report_einsehen(leistungsuebersicht):
    """
    Zeigt immer die aktuellste Leistungsübersicht an, die die Noten von den
    Studenten, Energiepunkte und Evaluationspunkte enthält.

    Parameter:
    leistungsuebersicht (dict): Das Dictionary, das die oben genannten
    Informationen enthält.
    """
    print("\nLeistungsübersicht:")
    print(f"Energiepunkte: {leistungsuebersicht['Energiepunkte']}")
    print(f"Evaluationspunkte: {leistungsuebersicht['Evaluationspunkte']}")
    print("Noten:")
    # Wenn eine Note nicht eingetragen ist, wird "Noch keine Note" angezeigt.
    for student, note in leistungsuebersicht['Studenten'].items():
        eingetragene_note = note if note is not None else "Noch keine Note"
        print(f"{student}: {eingetragene_note}")
    print()  # Eine leere Zeile wird noch hinzugefügt, damit alles
    # übersichtlicher aussieht.


def random_event(leistungsuebersicht):
    """
    Vier mögliche Ereignissen können mit bestimmten Wahrscheinlichkeiten
    auftreten: Verlängerung, Debugging, Danksagung und Neubewertung.
    All diese kosten Energiepunkte, außer Danksagung (+3EP).

    Parameter:
    leistungsuebersicht (dict): die aktualisierte Leistungsübersicht
    als Dictionary, die die aktualisierten Energiepunkte enthält.
    """
    event_wahrscheinlichkeiten = {
        "verlängerung": (0.2, -3, "Dein Student hat eine Verlängerung "
                                  "beantragt. Dies hat dir 3 EPs gekostet"),
        "neubewertung": (0.2, -2, "Dein Student hat eine Neubewertung "
                                  "beantragt. Dies hat dir 2 EPs gekostet"),
        "debugging": (0.3, -1, "Es war übermäßiger Aufwand an Debugging "
                               "erforderlich. Dies kostet dir 1 EP."),
        "danksagung": (0.1, +3, "Dein Student hat sich für deine Hilfe "
                                "bedankt. "
                                "Deine Energie erhöht sich um 3 Punkte.")}

    # Es wird über die möglichen Ereignissen iteriert und vielleicht eins
    # ausgewählt.
    for event, (wahrscheinlichkeit, ep_aenderung, nachricht) \
            in event_wahrscheinlichkeiten.items():
        if random.random() < wahrscheinlichkeit:
            leistungsuebersicht["Energiepunkte"] += ep_aenderung
            print(nachricht)
            print(f"Aktuelle Energie: {leistungsuebersicht['Energiepunkte']}")


def noteneintragung(leistungsuebersicht, feedback_1_abgeschlossen):
    """
    Die Noten werden für jeden Studenten eingetragen. Während der
    Noteneintragung können zufällige Ereignisse auftreten. Der Spieler kann
    auch seine Energie durch die Befehle 'rest' oder 'eat chocolate' erhöhen.

    Parameter:
    leistungsuebersicht (dict): Die aktuelle Leistungsübersicht, die die Noten
    und Energiepunkte enthält.
    feedback_1_abgeschlossen (bool): Boolescher Wert, ob die erste Feedback-
    Sitzung abgeschlossen wurde.
    """
    with open("noteneintragung.txt", "r", encoding="utf-8") as file:
        wilkommen = file.read()
        print(wilkommen)

    schokolade_gegessen = False  # Zustand, ob Schokolade schon gegessen wurde.

    def sind_gueltige_noten(note):
        """
        Überprüft, ob eine eingegebene Note gültig ist.

        Parameter:
        note (str): Die Note, die überprüft werden soll.

        Return:
        bool: True, wenn die Note gültig ist, sonst False.
        """
        gueltige_noten = ["1,0", "1,3", "1,7", "2,0", "2,3", "2,7", "3,0",
                          "3,3", "3,7", "4,0", "5,0"]
        return note in gueltige_noten

    def ausruhen():
        """
        Erhöht die Energiepunkte des Spielers um 5, bis zu einem
        Maximum von 100, damit der Spieler nicht unendlich viele Energiepunkte
        sammeln kann.
        """
        with open("ausruhen.txt", "r", encoding="utf-8") as file:
            text_ausruhen = file.read()
            print(text_ausruhen)

        leistungsuebersicht["Energiepunkte"] = (
            min(100, leistungsuebersicht["Energiepunkte"] + 5))
        print(f"Du hast dich schön ausgeruht. "
              f"Energie: {leistungsuebersicht['Energiepunkte']}")

    def schokolade_essen():
        """
        Erhöht die Energiepunkte des Spielers um 10. Dieser Befehl kann nur
        einmal während einer Runde der Noteneintragung benutzt werden.
        """
        with open("schokolade_essen.txt", "r", encoding="utf-8") as file:
            text_schokolade_essen = file.read()
            print(text_schokolade_essen)

        # Auf die schokolade_gegessen Variable zugreifen.
        nonlocal schokolade_gegessen
        if schokolade_gegessen:
            print("Du hast die ganze Tafel Schokolade aufgegessen, leider "
                  "gibt es keine mehr.")
        else:
            schokolade_gegessen = True
            leistungsuebersicht["Energiepunkte"] = (
                min(100, leistungsuebersicht["Energiepunkte"] + 10))
            print(f"Du hast eine Tafel Schokolade gegessen. "
                  f"Energie: {leistungsuebersicht['Energiepunkte']}")

    # Noteneintragung für jeden Studenten.
    for student, noten in leistungsuebersicht['Studenten'].items():
        while True:
            befehl = input(f"Gib eine Note für {student} ein oder möchtest du "
                           f"dich lieber ausruhen?: ").strip().lower()

            if befehl == "rest":
                ausruhen()
                # Bleibt im Ausruhen-Modus, bis der "grade"-Befehl erneut
                # eingegeben wird.
                while True:
                    naechste_befehl = input("Möchtest du die Notenvergabe "
                                            "fortsetzen oder dir mehr Zeit "
                                            "nehmen? "
                                            "(grade/rest): ").strip().lower()
                    if naechste_befehl == "grade":
                        break
                    elif naechste_befehl == "rest":
                        ausruhen()
                    elif naechste_befehl == "exit":
                        exit()
                    elif naechste_befehl == "inspect report":
                        report_einsehen(leistungsuebersicht)
                    else:
                        print("Ungültiger Befehl. Bitte versuche es nochmal.")

            elif befehl == "eat chocolate":
                schokolade_essen()
                # Bleibt im "Schokolade"-Modus, bis der "grade"-Befehl erneut
                # eingegeben wird.
                while True:
                    naechste_befehl = input("Möchtest du die restlichen Noten "
                                            "eintragen?: ").strip().lower()
                    if naechste_befehl == "grade":
                        break
                    elif naechste_befehl == "exit":
                        exit()
                    elif naechste_befehl == "inspect report":
                        report_einsehen(leistungsuebersicht)
                    else:
                        print("Ungültiger Befehl, bitte versuche es erneut.")

            elif befehl == "exit":
                exit()

            elif befehl == "inspect report":
                # Die Leistungsübersicht wird angezeigt und das Spiel
                # fortgesetzt.
                report_einsehen(leistungsuebersicht)
                continue

            elif sind_gueltige_noten(befehl):
                # Wenn die 1. Feedback-Sitzung noch nicht abgeschlossen wurde,
                # Noten eintragen.
                if not feedback_1_abgeschlossen:
                    if noten["1. Note"] is None:
                        noten["1. Note"] = befehl
                        leistungsuebersicht["Energiepunkte"] -= 5
                        print(f"Du hast die Note {befehl} für {student} "
                              f"erfolgreich eingetragen. Energie: "
                              f"{leistungsuebersicht['Energiepunkte']}")
                    else:
                        print("Die ersten Noten wurden bereits eingetragen.")
                else:
                    if noten["2. Note"] is None:
                        noten["2. Note"] = befehl
                        leistungsuebersicht["Energiepunkte"] -= 5
                        print(f"Du hast die Note {befehl} für {student} "
                              f"erfolgreich eingetragen. Energie: "
                              f"{leistungsuebersicht['Energiepunkte']}")
                    else:
                        print("Die zweiten Noten wurden bereits eingetragen.")
                break
            else:
                print("Ungültige Note. Gib bitte eine gültige Note ein!")

        if leistungsuebersicht["Energiepunkte"] < 1:
            print("Keine Energie mehr! Du hast leider das Spiel verloren.")
            return

        random_event(leistungsuebersicht)  # Ereignisse können auftreten.

    print("Glückwunsch! Du hast alle Noten eingetragen, und darfst nun mit "
          "der Feedback-Sitzung fortfahren!")


def evaluation_erhalten(leistungsuebersicht, feedback_1_abgeschlossen,
                        feedback_2_abgeschlossen):
    """
    Die Evaluation wird gestartet und zeigt die erhaltenen Evaluationspunkte
    an, wenn beide Feedback-Sitzungen erfolgreich abgeschlossen wurden.

    Parameter:
    leistungsuebersicht (dict): Die aktuelle Leistungsübersicht als Dictionary.
    feedback_1_abgeschlossen (bool): Status von der ersten Feedback-Sitzung.
    feedback_2_abgeschlossen (bool): Status von der zweiten Feedback-Sitzung.
    """
    # Prüfen, ob beide Feedback-Sitzungen abgeschlossen sind.
    if not feedback_1_abgeschlossen or not feedback_2_abgeschlossen:
        print("Achtung! Du musst zuerst beide Feedback-Sitzungen abschließen, "
              "bevor du die Evaluation erhalten kannst.")
        return

    with open("evaluation_erhalten.txt", "r", encoding="utf-8") as file:
        text_evaluation_erhalten = file.read()
        print(text_evaluation_erhalten)

    # Die gespeicherten Evaluationspunkte und die Leistungsübersicht werden
    # angezeigt.
    print(f"Du hast die Evaluation erhalten. Du hast "
          f"{leistungsuebersicht['Evaluationspunkte']} Evaluationspunkte.")
    print(leistungsuebersicht)


def nochmal_spielen():
    """
    Das Spiel wird neu gestartet, indem eine neue Instanz von der
    'Spiel'-Klasse erstellt und die `main`-Methode aufgerufen wird.
    """
    from main import Spiel
    spiel_instanz = Spiel()
    spiel_instanz.main()


def user_eingabe(eingabe, leistungsuebersicht, spiel_instanz):
    """
    Verarbeitet die Usereingabe und führt die entsprechenden Aktionen aus.

    Parameter:
        eingabe (str): Ein Befehl vom User.
        leistungsuebersicht (dict): Die aktuelle Leistungsübersicht.
        spiel_instanz (Spiel): Die Instanz von der 'Spiel'-Klasse.
    Return:
        str: Gibt den Befehl zurück, wenn der eine Aktion auslösen muss.
             Gibt None zurück, wenn der Befehl eine Aktion direkt ausführt
             oder wenn der ungültig ist.
    """
    # Befehle vom Spieler werden eingegeben, Leerzeichen entfernt und alles
    # klein geschrieben.
    befehl = input(eingabe).strip().lower()

    # Zeigt die aktuelle Leistungsübersicht an.
    if befehl == "inspect report":
        report_einsehen(leistungsuebersicht)
        return None

    elif befehl == "get eval":
        evaluation_erhalten(leistungsuebersicht,
                            spiel_instanz.feedback_1_abgeschlossen,
                            spiel_instanz.feedback_2_abgeschlossen)
        return None

    # Noteneintragung wird verzögert, wenn noch keine Note eingetragen wurde.
    elif befehl == "delay grade":
        noten_status_anfang = all(note is None for student in
                                  leistungsuebersicht['Studenten'].values()
                                  for note in student.values())
        zweite_runde_noten = all(student['2. Note'] is None for student in
                                 leistungsuebersicht["Studenten"].values())

        if noten_status_anfang or (spiel_instanz.feedback_1_abgeschlossen and
                                   zweite_runde_noten):
            return "delay grade"

        else:
            print("Der Befehl ist ungültig.")
            return None

    # Wenn die Noten schon eingetragen sind, wird die entsprechende
    # Feedback-Sitzung gestartet.
    elif befehl == "give feedback":
        if any(note is None for note in
               leistungsuebersicht["Studenten"].values()):
            print("Du musst zuerst Noten eintragen, bevor du mit der "
                  "Feedback-Sitzung fortfahren kannst.")
            return None

        if spiel_instanz.feedback_1_abgeschlossen:
            if spiel_instanz.feedback_2_abgeschlossen:
                print("Die zweite Feedback-Sitzung wurde bereits "
                      "abgeschlossen.")
                return None

            return "give feedback"

        return "give feedback"

    elif befehl == "exit":
        exit()

    elif befehl == "play again":
        return "play again"

    elif befehl == "grade":
        return "grade"
