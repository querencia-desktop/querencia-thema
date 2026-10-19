#!/usr/bin/env python3
"""Stellvertreter für org.freedesktop.portal.Documents im isolierten
Portal-Lauf (isoliert.py, QTH_PORTALE=1): belegt nur den Busnamen und
meldet einen leeren Ordner im Profil als Einhängepunkt. Kein FUSE-Mount,
damit im echten Files kein Laufwerk erscheint (PT-1)."""

import os

import gi

gi.require_version("Gio", "2.0")
from gi.repository import Gio, GLib  # noqa: E402

XML = """<node><interface name="org.freedesktop.portal.Documents">
<method name="GetMountPoint"><arg type="ay" direction="out"/></method>
<property name="version" type="u" access="read"/>
</interface></node>"""
ORDNER = os.path.join(os.environ.get("XDG_RUNTIME_DIR", "/nonexistent"), "doc-leer")


def aufruf(_v, _s, _p, _i, methode, _a, antwort):
    if methode == "GetMountPoint":
        antwort.return_value(GLib.Variant("(ay)", (ORDNER.encode() + b"\0",)))
    else:
        antwort.return_dbus_error("org.freedesktop.DBus.Error.NotSupported", "Stellvertreter")


def eigenschaft(*_a):
    return GLib.Variant("u", 4)


def erworben(verb, _n):
    info = Gio.DBusNodeInfo.new_for_xml(XML).interfaces[0]
    verb.register_object("/org/freedesktop/portal/documents", info, aufruf, eigenschaft, None)


os.makedirs(ORDNER, exist_ok=True)
Gio.bus_own_name(Gio.BusType.SESSION, "org.freedesktop.portal.Documents", 0, erworben, None, None)
GLib.MainLoop().run()
