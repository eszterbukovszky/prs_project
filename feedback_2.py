# Autorin: Eszter Bukovszky, Datum: 30.09.2024
# Zweck der Datei: Implementierung der zweiten Feedback-Sitzung, in der
# Codesätze auf Gültigkeit geprüft werden.

def gueltige_codesaetze(satz):
    """
    Überprüft rekursiv, ob ein gegebener Satz ein gültiger Codesatz ist.
    Ein Codesatz ist gültig, wenn folgende Bedingungen erfüllt sind:

    Bei Sätzen mit gerander Anzahl an Tokens muss gelten:
    1. Buchstabe vom ersten Token <= 1. Buchstabe vom letzten Token,
    1. Buchstabe vom zweiten Token <= 1. Buchstabe vom vorletzten Token,
    der letzte Buchstabe vom letzten Token <= der letzte Buchstabe vom 1. Token
    der letzte Buchstabe vom vorletzten Token <= der letzte Buchstabe vom 2.
    Token, usw.
    Bei Sätzen mit ungerader Anzahl an Tokens müssen die gleichen Bedingungen
    erfüllt werden, aber zusätzlich gilt, dass bei dem mittleren Token  der
    1. Buchstabe <= als der letzte ist.

    Parameter:
        satz (str): Der zu überprüfende Satz.
    Return:
        bool: True, wenn der Satz ein gültiger Codesatz ist, sonst False.
    """
    tokens = satz.split()
    n = len(tokens)

    def rekursive_check(worte, i):
        # Basisfall, wenn i den Mittelwert erreicht oder überschreitet, ist
        # der Satz gültig.
        if i >= (n - i - 1):
            return True

        # Zeichen der Wörter zum Vergleich abrufen.
        erste_wort_erste_char = worte[i][0].lower()
        erste_wort_letzte_char = worte[i][-1].lower()
        gepaart_wort_erste_char = worte[n - i - 1][0].lower()
        gepaart_wort_letzte_char = worte[n - i - 1][-1].lower()

        # Überprüfen, ob die Bedingungen erfüllt sind.
        if not (erste_wort_erste_char <= gepaart_wort_erste_char
                and gepaart_wort_letzte_char <= erste_wort_letzte_char):
            return False

        # Rekursive Überprüfung für das nächste Wortpaar.
        return rekursive_check(worte, i + 1)

    # Überprüfung für Sätze mit ungerader Anzahl an Wörtern
    # Bedingung für das mittlere Wort.
    if n % 2 == 1:
        mittel_index = n // 2
        mittel_wort_erste_char = tokens[mittel_index][0].lower()
        mittel_wort_letzte_char = tokens[mittel_index][-1].lower()
        if not (mittel_wort_erste_char <= mittel_wort_letzte_char):
            return False

    return rekursive_check(tokens, 0)


def feedback_sitzung_2(leistungsuebersicht):
    """
    Führt die zweite Feedback-Sizung durch, in der der Spieler einen gültigen
    Codesatz eingeben muss. Der Spieler hat bis zu drei Versuche.
    Bei erfolgreicher Eingabe eines gültigen Codesatzes werden
    80 Evaluationspunkte vergeben.

    Parameter:
        leistungsuebersicht (dict): Die Leistungsübersicht als Dictionary, die
        die Noten für Studenten, Energie- und Evaluationspunkte enthält.
    Return:
        int: Die Anzahl der erhaltenen Evaluationspunkten (80 oder 0).
    """
    with open("feedback_2.txt", "r", encoding="utf-8") as file:
        wilkommen = file.read()
        print(wilkommen)

    versuche = 0
    max_versuche = 3
    punkte = 0

    while versuche < max_versuche:
        eingabe = input(f"Versuch {versuche + 1}: "
                        f"Gib einen gültigen Codesatz ein: ").strip().lower()

        if eingabe == "exit":
            print("Das Spiel wird beendet.")
            exit()

        if eingabe == "inspect report":
            print("Leistungsübersicht:")
            print(leistungsuebersicht)
            continue

        if gueltige_codesaetze(eingabe):
            punkte = 80
            print("Richtig!")
            break
        else:
            print("Der Codesatz ist ungültig.")
            versuche += 1

    if punkte == 0:
        print("Du hast keinen gültigen Codesatz eingegeben. Du verlierst "
              "das Spiel.")

    return punkte
