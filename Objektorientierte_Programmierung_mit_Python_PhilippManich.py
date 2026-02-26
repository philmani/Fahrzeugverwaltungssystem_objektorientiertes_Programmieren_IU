"""
Erweiterte Fahrzeugverwaltung mit OOP, Abstraktion, Polymorphismus und Datenpersistenz

Dieses Skript demonstriert moderne OOP-Prinzipien mit einer Fahrzeugverwaltung:
- Abstrakte Basisklasse für Fahrzeuge
- Methodenüberschreibung und Polymorphismus
- Kapselung mit Getter/Setter (@property)
- Fehlerhandling mit try-except
- Speichern und Laden von Fahrzeugdaten mit JSON
- Benutzerinteraktion über ein Menü
"""

import json
from abc import ABC, abstractmethod

# Abstrakte Basisklasse für Fahrzeuge
class Fahrzeug(ABC):
    def __init__(self, marke: str, modell: str, baujahr: int, geschwindigkeit: int, beschleunigung: int):
        self.marke = marke
        self.modell = modell
        self.baujahr = baujahr
        self.geschwindigkeit = geschwindigkeit
        self.beschleunigung = beschleunigung

    @abstractmethod
    def beschleunigen(self) -> str:
        return f" {self.marke} {self.modell} beschleunigt in {self.beschleunigung} Sekunden auf 100 km/h!"

    def __str__(self) -> str:
        return f"{self.marke} {self.modell} ({self.baujahr}) | {self.geschwindigkeit} km/h"
    
    def to_dict(self) -> dict:
        return {
            "typ": self.__class__.__name__,
            "marke": self.marke,
            "modell": self.modell,
            "baujahr": self.baujahr,
            "geschwindigkeit": self.geschwindigkeit,
            "beschleunigung": self.beschleunigung
        }

    @staticmethod
    def from_dict(data: dict):
        typ = data.get("typ", None)
        data = dict(data)  # Kopie, damit original nicht verändert wird
        data.pop("typ", None)  # Entfernt 'typ', falls vorhanden

        if typ == "Auto":
            return Auto(**data)
        elif typ == "Elektroauto":
            return Elektroauto(**data)
        elif typ == "Motorrad":
            return Motorrad(**data)
        return None


# Klasse Auto (erbt von Fahrzeug)
class Auto(Fahrzeug):
    def __init__(self, marke: str, modell: str, baujahr: int, geschwindigkeit: int, beschleunigung: int, kraftstoff: str):
        super().__init__(marke, modell, baujahr, geschwindigkeit, beschleunigung)
        self.kraftstoff = kraftstoff
        
    def beschleunigen(self) -> str:
        return super().beschleunigen()

    def __str__(self) -> str:
        return super().__str__() + f" | Kraftstoff: {self.kraftstoff}"

    def to_dict(self) -> dict:
        data = super().to_dict()
        data["kraftstoff"] = self.kraftstoff
        return data
    
# Klasse Motorrad (erbt von Fahrzeug)
class Motorrad(Fahrzeug):
    def __init__(self, marke: str, modell: str, baujahr: int, geschwindigkeit: int, beschleunigung: int, kraftstoff: str):
        super().__init__(marke, modell, baujahr, geschwindigkeit, beschleunigung)
        self.kraftstoff = kraftstoff
        
    def beschleunigen(self) -> str:
        return super().beschleunigen()

    def __str__(self) -> str:
        return super().__str__() + f" | Kraftstoff: {self.kraftstoff}"

    def to_dict(self) -> dict:
        data = super().to_dict()
        data["kraftstoff"] = self.kraftstoff
        return data

# Klasse Elektroauto (erbt von Fahrzeug)
class Elektroauto(Fahrzeug):
    def __init__(self, marke: str, modell: str, baujahr: int, geschwindigkeit: int, beschleunigung: int, energiequelle: str):
        super().__init__(marke, modell, baujahr, geschwindigkeit, beschleunigung)
        self.energiequelle = energiequelle
    
    def beschleunigen(self) -> str:
        return super().beschleunigen()

    def __str__(self) -> str:
        return super().__str__() + f" | Energiequelle: {self.energiequelle}"

    def to_dict(self) -> dict:
        data = super().to_dict()
        data["energiequelle"] = self.energiequelle
        return data

# Klasse Fahrzeugverwaltung mit Datenpersistenz
class Fahrzeugverwaltung:
    DATEI = "fahrzeuge.json"

    def __init__(self):
        self.fahrzeuge = []
        self.laden()

    def fahrzeug_hinzufuegen(self, fahrzeug: Fahrzeug) -> None:
        self.fahrzeuge.append(fahrzeug)
        self.speichern()

    def alle_fahrzeuge_anzeigen(self) -> None:
        if not self.fahrzeuge:
            print(" Keine Fahrzeuge vorhanden.")
        else:
            print("\n Fahrzeugliste:")
            for f in self.fahrzeuge:
                print(f"  - {f} | Beschleunigung: {f.beschleunigung} Sek")


    def beschleunigungsinfo(self) -> None:
        if not self.fahrzeuge:
            print(" Keine Fahrzeuge vorhanden.")
        else:
            print("\n Beschleunigung der Fahrzeuge:")
            for f in self.fahrzeuge:
                print(f"  {f.beschleunigen()}")

    def speichern(self) -> None:
        try:
            with open(self.DATEI, "w") as file:
                json.dump([f.to_dict() for f in self.fahrzeuge], file, indent=4)
        except Exception as e:
            print(f" Fehler beim Speichern: {e}")

    def laden(self) -> None:
        try:
            with open(self.DATEI, "r") as file:
                daten = json.load(file)
                self.fahrzeuge = []
                for item in daten:
                    try:
                        fzg = Fahrzeug.from_dict(item)
                        if fzg:
                            self.fahrzeuge.append(fzg)
                    except Exception as e:
                        print(f" Ungültiger Eintrag übersprungen: {e}")
        except (FileNotFoundError, json.JSONDecodeError):
            pass  # Falls Datei fehlt oder leer ist, nichts tun
            
            
# ------------------
# Eingabe-Funktionen
# ------------------

def eingabe_string(prompt: str) -> str:
    wert = ""
    while not wert.strip():
        wert = input(prompt).strip()
        if not wert:
            print(" Eingabe darf nicht leer sein.")
    return wert

def eingabe_int(prompt: str) -> int:
    while True:
        eingabe = input(prompt)
        if not eingabe.strip():
            print(" Eingabe darf nicht leer sein.")
            continue
        try:
            return int(eingabe)
        except ValueError:
            print(" Bitte eine gültige Zahl eingeben.")

def eingabe_float(prompt: str) -> float:
    while True:
        eingabe = input(prompt).replace(",", ".")
        if not eingabe.strip():
            print(" Eingabe darf nicht leer sein.")
            continue
        try:
            return float(eingabe)
        except ValueError:
            print(" Bitte eine gültige Kommazahl eingeben.")



# Benutzerinteraktion
if __name__ == "__main__":
    verwaltung = Fahrzeugverwaltung()

    while True:
        print("\nMenü Fahrzeugverwaltung:")
        print("1. Auto hinzufügen")
        print("2. Elektroauto hinzufügen")
        print("3. Motorrad hinzufügen")
        print("4. Alle Fahrzeuge anzeigen")
        print("5. Beschleunigung der Fahrzeuge")
        print("6. Beenden")
        
        auswahl = input("-> Option wählen: ")

        if auswahl == "1":
            marke = eingabe_string(" Marke: ")
            modell = eingabe_string(" Modell: ")
            baujahr = eingabe_int(" Baujahr: ")
            geschwindigkeit = eingabe_int(" Höchstgeschwindigkeit (km/h): ")
            beschleunigung = eingabe_float(" Beschleunigung (Sekunden auf 100 km/h): ")
            kraftstoff = eingabe_string(" Kraftstoff: ")
            verwaltung.fahrzeug_hinzufuegen(Auto(marke, modell, baujahr, geschwindigkeit, beschleunigung, kraftstoff))
        
        elif auswahl == "2":
            marke = eingabe_string(" Marke: ")
            modell = eingabe_string(" Modell: ")
            baujahr = eingabe_int(" Baujahr: ")
            geschwindigkeit = eingabe_int(" Höchstgeschwindigkeit (km/h): ")
            beschleunigung = eingabe_float(" Beschleunigung (Sekunden auf 100 km/h): ")
            energiequelle = eingabe_string(" Energiequelle: ")
            verwaltung.fahrzeug_hinzufuegen(Elektroauto(marke, modell, baujahr, geschwindigkeit, beschleunigung, energiequelle))

        elif auswahl == "3":
            marke = eingabe_string(" Marke: ")
            modell = eingabe_string(" Modell: ")
            baujahr = eingabe_int(" Baujahr: ")
            geschwindigkeit = eingabe_int(" Höchstgeschwindigkeit (km/h): ")
            beschleunigung = eingabe_float(" Beschleunigung (Sekunden auf 100 km/h): ")
            kraftstoff = eingabe_string(" Kraftstoff: ")
            verwaltung.fahrzeug_hinzufuegen(Motorrad(marke, modell, baujahr, geschwindigkeit, beschleunigung, kraftstoff))

        elif auswahl == "4":
            verwaltung.alle_fahrzeuge_anzeigen()
        
        elif auswahl == "5":
            verwaltung.beschleunigungsinfo()

        elif auswahl == "6":
            print(" Programm beendet.")
            break

        else:
            print(" Ungültige Eingabe. Bitte erneut versuchen.")
