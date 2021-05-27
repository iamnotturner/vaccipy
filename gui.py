#!/usr/bin/env python3

import sys
import os
import json
import threading

from PyQt5 import QtWidgets, uic
from tools.gui import *
from tools.gui.qtzeiten import QtZeiten
from tools.gui.qtkontakt import QtKontakt
from tools.its import ImpfterminService

PATH = os.path.dirname(os.path.realpath(__file__))


class HauptGUI(QtWidgets.QMainWindow):

    # Folgende Widgets stehen zur Verfügung:

    ### QLineEdit ###
    # i_kontaktdaten_pfad
    # i_zeitspanne_pfad

    ### Buttons ###
    # b_termin_suchen
    # b_code_generieren
    # b_dateien_kontaktdaten
    # b_dateien_zeitspanne
    # b_neue_kontaktdaten
    # b_neue_zeitspanne

    # TODO: Ausgabe der cmd in der GUI wiederspiegelen - wenn sowas überhaupt geht
    def __init__(self, pfad_fenster_layout: str = os.path.join(PATH, "tools/gui/main.ui")):
        """
        Main der GUI Anwendung

        Args:
            pfad_fenster_layout (str, optional): Ladet das angegebene Layout (wurde mit QT Designer erstellt https://www.qt.io/download).
            Defaults to os.path.join(PATH, "tools/gui/main.ui").
        """

        super().__init__()

        # Laden der .ui Datei und Anpassungen
        uic.loadUi(pfad_fenster_layout, self)

        # Funktionen den Buttons zuweisen
        self.b_termin_suchen.clicked.connect(self.__termin_suchen)
        self.b_code_generieren.clicked.connect(self.__code_generieren)
        self.b_dateien_kontaktdaten.clicked.connect(self.__update_kontaktdaten_pfad)
        self.b_dateien_zeitspanne.clicked.connect(self.__update_zeitspanne_pfad)
        self.b_neue_kontaktdaten.clicked.connect(self.kontaktdaten_erstellen)
        self.b_neue_zeitspanne.clicked.connect(self.zeitspanne_erstellen)

        # Standard Pfade
        self.pfad_kontaktdaten: str = os.path.join(PATH, "data", "kontaktdaten.json")
        self.pfad_zeitspanne: str = os.path.join(PATH, "data", "zeitspanne.json")

        # Pfade in der GUI anzeigen
        self.i_kontaktdaten_pfad.setText(self.pfad_kontaktdaten)
        self.i_zeitspanne_pfad.setText(self.pfad_zeitspanne)

        # Events für Eingabefelder
        self.i_kontaktdaten_pfad.textChanged.connect(self.__update_kontaktdaten_pfad)
        self.i_zeitspanne_pfad.textChanged.connect(self.__update_zeitspanne_pfad)

        # Speichert alle termin_suchen Threads
        self.such_threads = list()

        # GUI anzeigen
        self.show()

        # Workaround, damit das Fenster hoffentlich im Vordergrund ist
        self.activateWindow()

    @staticmethod
    def start_gui():
        """
        Startet die GUI Anwendung
        """

        app = QtWidgets.QApplication(list())
        window = HauptGUI()
        app.exec_()

    def kontaktdaten_erstellen(self):
        """
        Ruft den Dialog für die Kontaktdaten auf
        """

        dialog = QtKontakt(self.pfad_kontaktdaten)
        dialog.show()
        dialog.exec_()

    def zeitspanne_erstellen(self):
        """
        Ruft den Dialog für die Zeitspanne auf
        """

        dialog = QtZeiten(self.pfad_zeitspanne)
        dialog.show()
        dialog.exec_()

    def __termin_suchen(self):
        """
        Startet den Prozess der terminsuche mit Impfterminservice.terminsuche in einem neuen Thread
        Dieser wird in self.such_threads hinzugefügt.
        Alle Threads sind deamon Thread (Sofort töten sobald der Bot beendet wird)
        """

        kontaktdaten = self.__get_kontaktdaten()
        zeitspanne = self.__get_zeitspanne()

        terminsuche_thread = threading.Thread(target=self.__start_terminsuche, args=(kontaktdaten, zeitspanne), daemon=True)
        terminsuche_thread.setName(kontaktdaten["code"])

        try:

            terminsuche_thread.start()
            if not terminsuche_thread.is_alive():
                raise RuntimeError(
                    f"Terminsuche wurde gestartet, lebt aber nicht mehr!\n\nTermin mit Code: {terminsuche_thread.getName()}\nBitte Daten Prüfen!"
                )

        except Exception as error:
            QtWidgets.QMessageBox.critical(self, "Fehler - Suche nicht gestartet!", str(error))

        else:
            self.such_threads.append(terminsuche_thread)

    def __start_terminsuche(self, kontaktdaten: dict, zeitspanne: dict):
        """
        Startet die Terminsuche. Dies nur mit einem Thread starten, da die GUI sonst hängt

        Args:
            kontaktdaten (dict): kontakdaten aus kontaktdaten.json
            zeitspanne (dict): zeitspanne aus zeitspanne.json
        """

        kontakt = kontaktdaten["kontakt"]
        code = kontaktdaten["code"]
        plz_impfzentren = kontaktdaten["plz_impfzentren"]

        # Startet das eigentliche suchen
        ImpfterminService.terminsuche(code=code, plz_impfzentren=plz_impfzentren, kontakt=kontakt, zeitspanne=zeitspanne, PATH=PATH)

    def __code_generieren(self):
        """
        Startet den Prozess der Codegenerierung
        """

        # TODO: code generierung implementieren
        pass

    def __get_kontaktdaten(self) -> dict:
        """
        Ladet die Kontakdaten aus dem in der GUI hinterlegten Pfad

        Returns:
            dict: Kontakdaten
        """

        if not os.path.isfile(self.pfad_kontaktdaten):
            self.kontaktdaten_erstellen()

        with open(self.pfad_kontaktdaten, "r", encoding='utf-8') as f:
            kontaktdaten = json.load(f)

        return kontaktdaten

    def __get_zeitspanne(self) -> dict:
        """
        Ladet die Zeitspanne aus dem in der GUI hinterlegtem Pfad

        Returns:
            dict: Zeitspanne
        """

        if not os.path.isfile(self.pfad_zeitspanne):
            self.zeitspanne_erstellen()

        with open(self.pfad_zeitspanne, "r", encoding='utf-8') as f:
            zeitspanne = json.load(f)

        return zeitspanne

    def __update_kontaktdaten_pfad(self):
        try:
            pfad = oeffne_file_dialog_select(self, "Kontakdaten", self.pfad_kontaktdaten)
            self.pfad_kontaktdaten = pfad
        except FileNotFoundError:
            pass

    def __update_zeitspanne_pfad(self):
        try:
            pfad = oeffne_file_dialog_select(self, "Zeitspanne", self.pfad_zeitspanne)
            self.pfad_zeitspanne = pfad
        except FileNotFoundError:
            pass

def main():
    """
    Startet die GUI-Anwendung
    """

    HauptGUI.start_gui()


if __name__ == "__main__":
    main()