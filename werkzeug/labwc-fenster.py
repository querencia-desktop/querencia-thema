#!/usr/bin/env python3
"""Thema 0.2.2: GTK-4-Fenster für die labwc-Belege (Titelleiste hell/dunkel).
Folgt dem Farbschema im Lauf; meldet es nach dem Start einmal neu
(GTK-4.22-Startfalle, docs/aufbau.md). Nur im isolierten Lauf
(labwc-belege.sh).

Aufruf:  labwc-fenster.py <titel>
"""

import sys

import gi

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk  # noqa: E402

TITEL = sys.argv[1]


def an(app):
    Gtk.Settings.get_default().notify("gtk-interface-color-scheme")
    w = Gtk.ApplicationWindow(application=app, title=TITEL)
    w.set_default_size(440, 250)
    box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8,
                  margin_top=12, margin_bottom=12, margin_start=12, margin_end=12)
    box.append(Gtk.Label(label="Querencia Desktop – Fensterinhalt", xalign=0))
    eingabe = Gtk.Entry()
    eingabe.set_text("Eingabefeld")
    box.append(eingabe)
    zeile = Gtk.Box(spacing=8)
    zeile.append(Gtk.CheckButton(label="Kästchen", active=True))
    zeile.append(Gtk.Button(label="Knopf"))
    box.append(zeile)
    liste = Gtk.ListBox()
    for i, t in enumerate(("Erster Eintrag", "Zweiter Eintrag")):
        liste.append(Gtk.Label(label=t, xalign=0))
    liste.select_row(liste.get_row_at_index(0))
    box.append(liste)
    w.set_child(box)
    w.present()


app = Gtk.Application(application_id=None)
app.connect("activate", an)
app.run([])
