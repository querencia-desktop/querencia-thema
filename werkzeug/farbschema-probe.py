#!/usr/bin/env python3
"""Thema 0.2: kleines GTK-4-Fenster, das jede Sekunde die Schriftfarbe eines
Labels und die GTK-Einstellungen meldet (gtk-interface-color-scheme:
1 = Standard, 2 = dunkel). Nur im isolierten Lauf (farbschema-start.sh).

Aufruf:  farbschema-probe.py <name> [notify]
notify: nach dem Start einmal Settings.notify("gtk-interface-color-scheme")
        (Abhilfe gegen den GTK-4.22-Startfehler, docs/aufbau.md).
"""

import sys

import gi

gi.require_version("Gtk", "4.0")
from gi.repository import GLib, Gtk  # noqa: E402

NAME = sys.argv[1]


def bericht(lab):
    s = Gtk.Settings.get_default()
    c = lab.get_color()
    print(NAME, "color-scheme", int(s.props.gtk_interface_color_scheme),
          "Schrift #%02x%02x%02x" % (round(c.red * 255), round(c.green * 255), round(c.blue * 255)),
          flush=True)
    return True


def an(app):
    if len(sys.argv) > 2 and sys.argv[2] == "notify":
        Gtk.Settings.get_default().notify("gtk-interface-color-scheme")
    w = Gtk.ApplicationWindow(application=app)
    lab = Gtk.Label(label="Querencia")
    w.set_child(lab)
    w.present()
    GLib.timeout_add(1000, bericht, lab)


app = Gtk.Application()
app.connect("activate", an)
app.run([])
