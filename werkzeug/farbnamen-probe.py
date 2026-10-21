#!/usr/bin/env python3
"""Thema 0.2.1: prüft die benannten Farben (@sidebar_bg_color u. a.) aus
der Sicht eines Programms. Ein eigener GtkCssProvider (wie die Programm-CSS,
OHNE Bindung an gtk-interface-color-scheme) färbt je ein Label mit einem
Namen; das Fenster meldet jede Sekunde die aufgelösten Farben.
Nur im isolierten Lauf (farbnamen-probe.sh).

Aufruf:  farbnamen-probe.py <name> [notify]
"""

import sys

import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Gdk", "4.0")
from gi.repository import Gdk, GLib, Gtk  # noqa: E402

NAME = sys.argv[1]
FARBEN = ["sidebar_bg_color", "sidebar_fg_color", "menu_bg_color", "menu_fg_color"]


def bericht(labels):
    s = Gtk.Settings.get_default()
    teile = []
    for n, lab in labels:
        c = lab.get_color()
        teile.append("%s=#%02x%02x%02x" % (n, round(c.red * 255), round(c.green * 255), round(c.blue * 255)))
    print(NAME, "color-scheme", int(s.props.gtk_interface_color_scheme), " ".join(teile), flush=True)
    return True


def an(app):
    if len(sys.argv) > 2 and sys.argv[2] == "notify":
        Gtk.Settings.get_default().notify("gtk-interface-color-scheme")
    prov = Gtk.CssProvider()
    prov.load_from_string("".join(f"label.n-{n} {{ color: @{n}; }}\n" for n in FARBEN))
    Gtk.StyleContext.add_provider_for_display(Gdk.Display.get_default(), prov,
                                              Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
    w = Gtk.ApplicationWindow(application=app)
    box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
    labels = []
    for n in FARBEN:
        lab = Gtk.Label(label=n)
        lab.add_css_class("n-" + n)
        box.append(lab)
        labels.append((n, lab))
    w.set_child(box)
    w.present()
    GLib.timeout_add(1000, bericht, labels)


app = Gtk.Application()
app.connect("activate", an)
app.run([])
