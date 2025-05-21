# Autorin: Eszter Bukovszky, Datum: 30.09.2024
# Zweck der Datei: Implementierung der ersten Feedback-Sitzung, bei der
# der Spieler Themen von (maskierten) Sätzen erraten muss.
# Quellen: NLTK Reuters corpus, random-Modul, re-Modul, time-Modul

import nltk
import random
import re
import time
from nltk.corpus import reuters
nltk.download('punkt')


def random_thema_auswaehlen():
    """
    Diese Funktion wählt ein zufälliges Thema aus der Reuters-Datenbank aus,
    und gibt ein zu diesem Thema gehörenden Satz zurück, der maximal 20 Wörter,
    nicht mehr als 3 numerische Tokens, und nicht mehr als 4 Sonderzeichen
    enthält.
    Wenn der ausgewählte Satz den Namen des Thema enthält, wird
    dieses Wort mit [HIDDEN] maskiert.

    Return:
        tuple: Ein zufällig ausgewähltes Thema und (maskierter) Satz.
    """
    # Zufälliges Thema aus den Reuters-Kategorien auswählen.
    topic = random.choice(reuters.categories())
    # Sätze zu dem vorherigen Thema abrufen.
    saetze = reuters.sents(categories=topic)

    gueltige_saetze = []
    for satz in saetze:  # Überprüfen ob der Satz den Bedingungen entspricht.
        if len(satz) < 20:
            # Nur maximum 3 numerische Tokens sind erlaubt.
            numerische_token_count = 0
            for token in satz:
                if re.search(r'\d', token):
                    numerische_token_count += 1
                if numerische_token_count > 3:
                    break

            # Nur maximum 3 Sonderzeichen sind erlaubt.
            sonderzeichen_count = 0
            for token in satz:
                if re.search(r"[!#$%^&*()\-_=+[\]{};:'\".<>?/\\]",
                             token):
                    sonderzeichen_count += 1
                if sonderzeichen_count > 4:
                    break

            if numerische_token_count <= 3 and sonderzeichen_count <= 4:
                # Teile des Satzes werden maskiert, wenn der das Thema enthält.
                maskierter_satz = [token if token.lower() != topic.lower()
                                   else "[HIDDEN]" for token in satz]
                gueltige_saetze.append(maskierter_satz)

    # Wenn keine gültige Sätze gefunden wurden, wird ein anderes Thema gesucht.
    if not gueltige_saetze:
        return random_thema_auswaehlen()
    else:
        satz = random.choice(gueltige_saetze)
        return topic, satz


def feedback_sitzung_1(leistungsuebersicht):
    """
    Die erste Feedback-Sitzung wird durchgeführt, wobei der Spieler 3 Themen
    erraten soll, und wofür man Evaluationspunkte erhält. Mit dem "clarify"
    Befehl darf der Spieler für jedes Thema genau einen Tipp bekommen.

    Parameter:
        leistungsuebersicht (dict): Die Leistungsübersicht als Dictionary, die
        die Noten für Studenten, Energie- und Evaluationspunkte enthält.
    Return:
        int: Die gesamten Evaluationspunkte, die der Spieler während dieser
        Sitzung bekommt.
    """

    with open("feedback_1.txt", "r", encoding="utf-8") as file:
        wilkommen = file.read()
        print(wilkommen)

    totale_punkte = 0

    # Folgende Nachrichten erscheinen vor dem entsprechenden Satz.
    for i in range(3):
        if i == 0:
            print("Hier folgt der erste Satz, dessen Thema du erraten musst:")
        elif i == 1:
            print("Hier folgt der zweite Satz, dessen Thema du erraten musst:")
        elif i == 2:
            print("Hier folgt der dritte Satz, dessen Thema du erraten musst:")

        # Das Thema und der Satz werden ausgewählt.
        topic, satz = random_thema_auswaehlen()
        maskierter_satz = " ".join(satz)

        print("Der Satz: " + maskierter_satz)

        versuche = 1
        start_zeit = time.time()  # Startzeit, die Zeit wird gemessen.
        clarify_benutzt = False
        # Wenn mehr als 1 Minute gebraucht wird, das Spiel wird verloren.
        while versuche <= 3:
            if time.time() - start_zeit > 60:
                print("Leider hast du das Spiel verloren, weil du mehr als "
                      "eine Minute gebraucht hast.")
                return totale_punkte

            user_eingabe = input(f"Versuch {versuche}: Bitte gib das Thema an "
                                 f"oder 'clarify' für einen "
                                 f"Tipp. ").strip().lower()

            if user_eingabe == "exit":
                print("Das Spiel wird beendet.")
                exit()

            if user_eingabe == "inspect report":
                print("Leistungsübersicht:")
                print(leistungsuebersicht)
                continue

            if user_eingabe == "clarify":  # Max. 1 Tipp pro Thema verwenden.
                if not clarify_benutzt:
                    clarify_benutzt = True
                    tipp_satz = random_thema_auswaehlen()[1]
                    print(f"Hier ist ein weiterer Satz "
                          f"zum Thema als Tipp: {' '.join(tipp_satz)}")
                else:
                    print("Du hast den Tipp bereits verwendet, bitte rate "
                          "das Thema.")

            elif user_eingabe == topic.lower():  # Wenn das Thema erraten wurde
                # Punkte vergeben, abhängig davon, wie oft man raten musste.
                if versuche == 1:
                    punkte = 40
                elif versuche == 2:
                    punkte = 30
                else:
                    punkte = 20
                print("Richtig!")
                totale_punkte += punkte
                break

            else:  # Wenn der Spieler das falsche Thema geraten hat.
                uebrige_versuche = 3 - versuche
                if uebrige_versuche > 0:
                    print(f"Leider falsch. Du hast noch "
                          f"{uebrige_versuche} Versuch(e) übrig.")
                versuche += 1
                if versuche > 3:
                    print("Leider falsch. Du hast keinen Versuch mehr "
                          "zu diesem Thema.")
                    break

    return totale_punkte
