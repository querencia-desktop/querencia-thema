#!/usr/bin/env python3
"""Thema 0.2.1: Fokus-Probe zur Systemmonitor-Notiz („nach einem
Farbschema-Wechsel liegt der Tastaturfokus anders“). Fenster mit Menüleiste,
Reitern, Liste und Knopf wie Systemmonitor; meldet jede Sekunde das Fokus-Widget,
Window:focus-visible und den Zustand :focus-visible des Fokus-Widgets.
Nur im isolierten Lauf (fokus-probe.sh).

Aufruf:  fokus-probe.py <name>
"""

import sys

import gi

gi.require_version("Gtk", "4.0")
from gi.repository import Gio, GLib, Gtk  # noqa: E402

NAME = sys.argv[1]


def bericht(w):
    s = Gtk.Settings.get_default()
    f = w.get_focus()
    if f is None:
        fokus = "-"
    else:
        fokus = f"{f.get_css_name()}({type(f).__name__})"
        st = f.get_state_flags()
        for flag, txt in ((Gtk.StateFlags.FOCUS_VISIBLE, ":focus-visible"),
                          (Gtk.StateFlags.FOCUSED, ":focus"),
                          (Gtk.StateFlags.SELECTED, ":selected"),
                          (Gtk.StateFlags.PRELIGHT, ":hover")):
            fokus += " " + txt if st & flag else ""
    print(NAME, "color-scheme", int(s.props.gtk_interface_color_scheme),
          "focus-visible", int(w.get_focus_visible()), "fokus", fokus, flush=True)
    return True


def an(app):
    menue = Gio.Menu()
    datei = Gio.Menu()
    datei.append("Beenden", "app.beenden")
    menue.append_submenu("Datei", datei)
    app.set_menubar(menue)
    a = Gio.SimpleAction.new("beenden", None)
    a.connect("activate", lambda *_: app.quit())
    app.add_action(a)
    app.set_accels_for_action("app.beenden", ["<Control>q"])
    w = Gtk.ApplicationWindow(application=app, title="Fokus-Probe", show_menubar=True)
    w.set_default_size(420, 300)
    nb = Gtk.Notebook()
    for titel in ("Prozesse", "Ressourcen"):
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        liste = Gtk.ListBox()
        for i in range(5):
            liste.append(Gtk.Label(label=f"{titel} {i}", xalign=0))
        box.append(liste)
        box.append(Gtk.Button(label="Beenden"))
        nb.append_page(box, Gtk.Label(label=titel))
    w.set_child(nb)
    w.present()
    GLib.timeout_add(1000, bericht, w)


app = Gtk.Application()
app.connect("activate", an)
app.run([])
