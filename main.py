# Autorin: Eszter Bukovszky, Datum: 30.09.2024
# Zweck der Datei: Implementierung des Hauptspiels mit der Verwendung von den
# importierten Funktionen/Modulen.
# Quellen: Importierte Module (beschreibungen, feedback_1, feedback_2)

from beschreibungen import (leistungsuebersicht_erstellen,
                            noteneintragung, user_eingabe, evaluation_erhalten,
                            report_einsehen, nochmal_spielen)
from feedback_1 import feedback_sitzung_1
from feedback_2 import feedback_sitzung_2
import nltk


class Spiel:
    """
    Diese Klasse stellt den Hauptablauf des Spiels dar: der Spieler kann
    verschiedene Befehle eingeben, um die Noten einzugeben/ die
    Feedback-Sitzungen durchzuführen/das Spiel zu gewinnen.

    Attribute:
    leistungsuebersicht (dict): die Leistungsübersicht von den Studenten und
    Punkten als Dictionary.
    schokolade_gegessen (bool): boolescher Wert, ob Schokolade schon
    gegessen wurde.
    feedback_1_abgeschlossen (bool): boolescher Wert, ob die erste
    Feedback-Sitzung abgeschlossen wurde.
    feedback_2_abgeschlossen (bool): boolescher Wert, ob die zweite
    Feedback-Sitzung abgeschlossen wurde.
    """
    def __init__(self):
        """
        Eine Instanz des Spiels wird initialisiert: die Leistungsübersicht,
        eine Variable als Zwischenspeicher für die Evaluationspunkte werden
        erstellt, und die booleschen Werte für Schokolade und die zwei
        Feedback-Sitzungen werden auf False gesetzt.
        """
        self.temp_punkte = 0
        self.leistungsuebersicht = leistungsuebersicht_erstellen()
        self.schokolade_gegessen = False
        self.feedback_1_abgeschlossen = False
        self.feedback_2_abgeschlossen = False

    def main(self):
        """
        Beginnt den eigentlichen Spielverlauf. Der Spieler hat die Möglichkeit,
        verschiedene Befehle einzugeben.
        Das Spiel wird beendet wenn entweder der Spieler keine Energie mehr
        hat, oder wenn die Feedback-Sitzungen erfolgreich abgeschlossen
        und die Evaluation erhalten wurden.
        """
        with open("einfuehrung.txt", "r", encoding="utf-8") as file:
            wilkommen = file.read()
            print(wilkommen)

        while True:
            # Wenn die zweite Feedback-Sitzung abgeschlossen ist, darf die
            # Evaluation eingesehen werden.
            if self.feedback_2_abgeschlossen:
                print("Nun darfst du die Evaluation einsehen.")
                befehl = input("\nMöchtest du die Evaluation erhalten? ")

                if befehl == "get eval":
                    # Hier werden die im Zwischenspeicher gespeicherten
                    # Evaluationspunkte in die Leistungsübersicht übertragen.
                    self.leistungsuebersicht[
                        "Evaluationspunkte"] += self.temp_punkte
                    evaluation_erhalten(self.leistungsuebersicht,
                                        self.feedback_1_abgeschlossen,
                                        self.feedback_2_abgeschlossen)
                    print("Glückwunsch! Du hast das Spiel gewonnen!")
                    break

                elif befehl == "inspect report":
                    print(self.leistungsuebersicht)
                    continue

                else:
                    print("Ungültiger Befehl. Gib bitte 'get eval' ein, "
                          "um die Evaluation einsehen zu können.")
                    continue

            else:
                befehl = user_eingabe("\nWas möchtest du machen? Du "
                                      "kannst die Noten für deine Studenten "
                                      "eintragen oder willst du sofort die "
                                      "Feedback-Sitzung starten?: ",
                                      self.leistungsuebersicht, self)

            if befehl == "exit":
                print("Das Spiel wurde beendet.")
                exit()

            if befehl == "inspect report":
                report_einsehen(self.leistungsuebersicht)
                break

            if befehl == "grade":
                # Prüfen, ob keine Note am Anfang des Spiels eingetragen ist.
                noten_status_anfang = (
                    all(note is None for student in
                        self.leistungsuebersicht["Studenten"].values()
                        for note in student.values()))

                # Wenn die 1. Feedback-Sitzung abgeschlossen oder keine Note
                # eingetragen ist, können wir Noten eintragen.
                if self.feedback_1_abgeschlossen or noten_status_anfang:
                    self.schokolade_gegessen = (
                        noteneintragung(self.leistungsuebersicht,
                                        self.feedback_1_abgeschlossen))
                else:
                    if not self.feedback_1_abgeschlossen:
                        print("Du musst erst die erste Feedback-Sitzung "
                              "erfolgreich absolvieren. ")

            elif befehl == "get eval":
                # Prüfen ob Feedback 1 und 2 erfolgreich abgeschlossen sind.
                if (self.feedback_2_abgeschlossen
                        and self.feedback_1_abgeschlossen):
                    self.leistungsuebersicht[
                        "Evaluationspunkte"] += self.temp_punkte
                    # Die Evaluation darf nun eingesehen werden.
                    evaluation_erhalten(self.leistungsuebersicht,
                                        self.feedback_1_abgeschlossen,
                                        self.feedback_2_abgeschlossen)
                    print("Glückwunsch! Du hast das Spiel gewonnen!")
                    break
                else:
                    print("Du musst beide Feedback-Sitzungen erfolgreich "
                          "abschließen, bevor du die Evaluation einsehen "
                          "kannst.")

            elif befehl == "delay grade":
                if not self.feedback_1_abgeschlossen:
                    # Prüfen, ob die Noten in der 1. Runde eingetragen sind.
                    if all(student["1. Note"] is None for student
                           in self.leistungsuebersicht["Studenten"].values()):
                        # Die 1. Feedback-Sitzung durchführen.
                        punkte = feedback_sitzung_1(self.leistungsuebersicht)
                        if punkte > 0:
                            self.feedback_1_abgeschlossen = True
                            self.temp_punkte = punkte  # Speichert die
                            # Evaluationspunkte im Zwischenspeicher.
                        else:
                            print("Du hast die erste Feedback-Sitzung leider "
                                  "nicht erfolgreich abgeschlossen. Du hast "
                                  "das Spiel verloren.")
                            break

                    else:
                        print("Ungültiger Befehl. Du hast schon angefangen, "
                              "die Noten einzutragen.")

                elif (self.feedback_1_abgeschlossen and
                      not self.feedback_2_abgeschlossen):
                    # Die 2. Feedback-Sitzung wird durchgeführt.
                    punkte = feedback_sitzung_2(self.leistungsuebersicht)
                    if punkte > 0:
                        self.feedback_2_abgeschlossen = True
                        # Punkte werden im Zwischenspeicher gespeichert.
                        self.temp_punkte += punkte
                        print(f"Du hast die zweite Feedback-Sitzung "
                              f"abgeschlossen. ")
                    else:
                        print("Die zweite Feedback-Sitzung war nicht "
                              "erfolgreich. Du hast das Spiel verloren.")
                        break
                else:
                    print("Ungültiger Befehl. Du hast schon in der zweiten "
                          "Runde die Noten eingetragen.")

            elif befehl == "give feedback":
                # Feedback 1/2 starten, wenn alle Noten in der entsprechenden
                # Runde schon eingetragen sind.
                if not self.feedback_1_abgeschlossen:
                    if all(noten["1. Note"] is not None for noten in
                           self.leistungsuebersicht["Studenten"].values()):
                        # Die erste Feedback-Sitzung durchführen.
                        punkte = feedback_sitzung_1(self.leistungsuebersicht)
                        if punkte > 0:
                            self.feedback_1_abgeschlossen = True
                            self.temp_punkte = punkte  # Speichert die Punkte
                            # im Zwischenspeicher.
                        else:
                            print("Du hast die erste Feedback-Sitzung nicht "
                                  "erfolgreich abgeschlossen. Du hast das "
                                  "Spiel verloren.")
                            break
                    else:
                        print("Du musst zuerst die Noten eintragen, bevor du "
                              "diesen Befehl eingeben darfst.")

                elif not self.feedback_2_abgeschlossen:
                    # Prüfen, ob die Noten in der 2. Runde eingetragen sind.
                    if all(noten["2. Note"] is not None for noten in
                           self.leistungsuebersicht["Studenten"].values()):
                        # Feedback 2 durchführen.
                        punkte = feedback_sitzung_2(self.leistungsuebersicht)
                        if punkte > 0:
                            self.feedback_2_abgeschlossen = True
                            # Punkte werden im Zwischenspeicher gespeichert.
                            self.temp_punkte += punkte
                            print(f"Du hast die zweite Feedback-Sitzung "
                                  f"erfolgreich abgeschlossen.")
                        else:
                            print("Die zweite Feedback-Sitzung war nicht "
                                  "erfolgreich. Du hast das Spiel verloren.")
                            break
                    else:
                        print("Du musst zuerst weitere Noten eintragen, bevor "
                              "du diesen Befehl benutzen darfst.")
                else:
                    print("Alle Feedback-Sitzungen wurden bereits erfolgreich "
                          "abgeschlossen.")

            else:
                print("Bitte gib einen gültigen Befehl ein! ")

            # Prüfen, ob der Spieler weniger als 1 EP hat. (Das macht glaube
            # ich mehr Sinn als 0 EP, weil in dem Fall hat der Spieler auch
            # keine Energie mehr, also mit 0 EP verliert man auch.)
            if self.leistungsuebersicht["Energiepunkte"] < 1:
                print("Du hast keine Energie mehr und das Spiel verloren.")
                break

        # Wenn das Spiel zu Ende ist es kann beendet oder neu gestartet werden.
        while True:
            befehl = input(
                "\nMöchtest du nochmal spielen? "
                "(play again/exit): ").strip().lower()
            if befehl == "play again":
                nochmal_spielen()
                self.main()
            elif befehl == "exit":
                print("Das Spiel wurde beendet.")
                exit()
            elif befehl == "inspect report":
                # Die Leistungsübersicht kann auch hier eingesehen werden.
                report_einsehen(self.leistungsuebersicht)
            else:
                print("Ungültiger Befehl.")


if __name__ == "__main__":
    spiel_instanz = Spiel()  # Erstellt eine Instanz des Spiels.
    spiel_instanz.main()  # Das Spiel wird gestartet, indem die main-Methode
    # aufgerufen wird.
