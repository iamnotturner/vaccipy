import json
from PyQt5 import QtWidgets


def oeffne_file_dialog_save(parent_widged: QtWidgets.QWidget, titel: str, standard_speicherpfad: str, dateityp="JSON Files (*.json)") -> str:
    """
    Öffnet ein File Dialog, der entsprechend einen Pfad zurück gibt, wohin gespeichert werden soll

    Args:
        parent_widged (PyQt5.QtWidgets.QWidget): 
        titel (str): Titel des Dialogs
        standard_speicherpfad (str): Pfad welcher direkt geöffnet wird als Vorschlag
        dateityp (str, optional): selectedFilter example: "Images (*.png *.xpm *.jpg)". Defaults to "JSON Files (*.json)".

    Raises:
        FileNotFoundError: Wird geworfen, wenn der Dateipfad leer ist

    Returns:
        str: Vollständiger Pfad
    """

    datei_data = QtWidgets.QFileDialog.getSaveFileName(parent_widged, titel, standard_speicherpfad, dateityp)
    dateipfad = datei_data[0]  # (Pfad, Dateityp)

    if not dateipfad:
        raise FileNotFoundError

    return dateipfad


def oeffne_file_dialog_select(parent_widged: QtWidgets.QWidget, titel: str, standard_oeffnungspfad: str, dateityp="JSON Files (*.json)") -> str:
    """
    Öffnet einen File Dialog um eine existierende Datei auszuwählen

    Args:
        parent_widged (QtWidgets.QWidget): Parent QWidget an das der Dialog gehängt werden soll
        titel (str): Titel des Dialogs
        standard_oeffnungspfad (str): Pfad welcher direkt geöffnet wird als Vorschlag
        dateityp (str, optional): selectedFilter example: "Images (*.png *.xpm *.jpg)". Defaults to "JSON Files (*.json)".

    Raises:
        FileNotFoundError: Wird geworfen, wenn der Dateipfad leer ist

    Returns:
        str: Vollständiger Pfad zur Datei
    """

    # Öffnet den "File-Picker" vom System um ein bereits existierende Datei auszuwählen
    datei_data = QtWidgets.QFileDialog.getOpenFileName(parent_widged, titel, standard_oeffnungspfad, "JSON Files (*.json)")
    dateipfad = datei_data[0]  # (pfad, typ)

    if not dateipfad:
        raise FileNotFoundError

    return dateipfad


def speichern(speicherpfad: str, data: dict):
    """
    Speichert die Daten mittels json.dump an den entsprechenden Ort

    Args:
        speicherpfad (str): speicherort
        data (dict): Speicherdaten
    """

    with open(speicherpfad, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)