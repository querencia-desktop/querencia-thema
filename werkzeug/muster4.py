#!/usr/bin/env python3
"""Musterseite für das GTK-4-Thema: alle Elementarten in einem Fenster.

Aufruf (nur im isolierten Lauf, siehe belege.sh):
  muster4.py [seite] [extra]
  seite: knoepfe | listen | regler | text   (Startreiter, Standard knoepfe)
  extra: tooltip | dialog | popover | klein  (zusätzlich anzeigen)
"""

import sys

import gi

gi.require_version("Gtk", "4.0")
from gi.repository import Gio, GLib, GObject, Gtk  # noqa: E402

SEITE = sys.argv[1] if len(sys.argv) > 1 else "knoepfe"
EXTRA = sys.argv[2] if len(sys.argv) > 2 else ""


def menue():
    m = Gio.Menu()
    datei = Gio.Menu()
    datei.append("Neu", "app.nix")
    datei.append("Öffnen …", "app.nix")
    datei.append("Speichern", "app.nix")
    teil = Gio.Menu()
    teil.append("Deaktiviert", "app.aus")
    teil.append("Beenden", "app.quit")
    datei.append_section(None, teil)
    m.append_submenu("_Datei", datei)
    bearb = Gio.Menu()
    bearb.append("Ausschneiden", "app.nix")
    bearb.append("Kopieren", "app.nix")
    bearb.append("Einfügen", "app.nix")
    opt = Gio.Menu()
    opt.append("Zeilennummern", "app.schalter")
    bearb.append_section(None, opt)
    m.append_submenu("_Bearbeiten", bearb)
    ansicht = Gio.Menu()
    ansicht.append("Symbolleiste", "app.nix")
    m.append_submenu("_Ansicht", ansicht)
    hilfe = Gio.Menu()
    hilfe.append("Info", "app.nix")
    m.append_submenu("_Hilfe", hilfe)
    return m


def knoepfe_seite():
    g = Gtk.Grid(row_spacing=8, column_spacing=8, margin_top=12, margin_bottom=12,
                 margin_start=12, margin_end=12)
    r = 0
    g.attach(Gtk.Label(label="Knöpfe:", xalign=0), 0, r, 1, 1)
    box = Gtk.Box(spacing=6)
    box.append(Gtk.Button(label="Normal"))
    b = Gtk.Button(label="Deaktiviert")
    b.set_sensitive(False)
    box.append(b)
    t = Gtk.ToggleButton(label="Umschalter")
    t.set_active(True)
    box.append(t)
    s = Gtk.Button(label="Übernehmen")
    s.add_css_class("suggested-action")
    box.append(s)
    d = Gtk.Button(label="Löschen")
    d.add_css_class("destructive-action")
    box.append(d)
    f = Gtk.Button(label="Flach")
    f.add_css_class("flat")
    box.append(f)
    box.append(Gtk.Button(icon_name="document-open-symbolic"))
    g.attach(box, 1, r, 1, 1)
    r += 1
    g.attach(Gtk.Label(label="Verbunden:", xalign=0), 0, r, 1, 1)
    lk = Gtk.Box()
    lk.add_css_class("linked")
    for t in ("Links", "Mitte", "Rechts"):
        lk.append(Gtk.ToggleButton(label=t, active=(t == "Mitte")))
    g.attach(lk, 1, r, 1, 1)
    r += 1
    g.attach(Gtk.Label(label="Eingabe:", xalign=0), 0, r, 1, 1)
    eb = Gtk.Box(spacing=6)
    e = Gtk.Entry(text="Querencia Desktop")
    eb.append(e)
    e2 = Gtk.Entry(placeholder_text="Platzhalter")
    eb.append(e2)
    e3 = Gtk.Entry(text="deaktiviert")
    e3.set_sensitive(False)
    eb.append(e3)
    g.attach(eb, 1, r, 1, 1)
    r += 1
    g.attach(Gtk.Label(label="Zahl und Auswahl:", xalign=0), 0, r, 1, 1)
    zb = Gtk.Box(spacing=6)
    zb.append(Gtk.SpinButton.new_with_range(0, 100, 1))
    dd = Gtk.DropDown.new_from_strings(["Ambiance", "Human", "Clearlooks"])
    zb.append(dd)
    sw = Gtk.SearchEntry(placeholder_text="Suchen")
    zb.append(sw)
    g.attach(zb, 1, r, 1, 1)
    r += 1
    g.attach(Gtk.Label(label="Kästchen:", xalign=0), 0, r, 1, 1)
    kb = Gtk.Box(spacing=12)
    kb.append(Gtk.CheckButton(label="An", active=True))
    kb.append(Gtk.CheckButton(label="Aus"))
    c = Gtk.CheckButton(label="Unbestimmt")
    c.set_inconsistent(True)
    kb.append(c)
    c = Gtk.CheckButton(label="Deaktiviert", active=True)
    c.set_sensitive(False)
    kb.append(c)
    g.attach(kb, 1, r, 1, 1)
    r += 1
    g.attach(Gtk.Label(label="Optionen:", xalign=0), 0, r, 1, 1)
    ob = Gtk.Box(spacing=12)
    r1 = Gtk.CheckButton(label="Eins", active=True)
    r2 = Gtk.CheckButton(label="Zwei")
    r2.set_group(r1)
    r3 = Gtk.CheckButton(label="Drei")
    r3.set_group(r1)
    r3.set_sensitive(False)
    for x in (r1, r2, r3):
        ob.append(x)
    g.attach(ob, 1, r, 1, 1)
    r += 1
    g.attach(Gtk.Label(label="Schalter:", xalign=0), 0, r, 1, 1)
    sb = Gtk.Box(spacing=12)
    sb.append(Gtk.Switch(active=True, valign=Gtk.Align.CENTER))
    sb.append(Gtk.Switch(valign=Gtk.Align.CENTER))
    lb = Gtk.LinkButton(uri="https://querencialinux.org", label="Verweis")
    sb.append(lb)
    mb = Gtk.MenuButton(label="Menüknopf")
    mb.set_menu_model(menue())
    sb.append(mb)
    g.attach(sb, 1, r, 1, 1)
    r += 1
    fr = Gtk.Frame(label="Rahmen")
    fr.set_child(Gtk.Label(label="Inhalt eines Rahmens", margin_top=8, margin_bottom=8))
    g.attach(fr, 0, r, 2, 1)
    tip = Gtk.Button(label="Mit Tooltip")
    tip.set_tooltip_text("Ein Tooltip im Stil von Ubuntu 10.04")
    g.attach(tip, 0, r + 1, 1, 1)
    knoepfe_seite.tip = tip
    knoepfe_seite.menuknopf = mb
    return g


class Zeile(GObject.Object):
    def __init__(self, i):
        super().__init__()
        self.name = f"Datei-{i:03d}.txt"
        self.groesse = f"{(i * 37) % 900 + 1} KB"
        self.art = ["Textdokument", "Bild", "Ordner", "Tabelle"][i % 4]


def spalten_liste():
    store = Gio.ListStore(item_type=Zeile)
    for i in range(1, 201):
        store.append(Zeile(i))
    sel = Gtk.SingleSelection(model=store)
    sel.set_selected(2)
    cv = Gtk.ColumnView(model=sel)
    for titel, attr in (("Name", "name"), ("Größe", "groesse"), ("Art", "art")):
        fab = Gtk.SignalListItemFactory()

        def setup(_f, item):
            item.set_child(Gtk.Label(xalign=0))

        def bind(_f, item, attr=attr):
            item.get_child().set_label(getattr(item.get_item(), attr))

        fab.connect("setup", setup)
        fab.connect("bind", bind)
        sp = Gtk.ColumnViewColumn(title=titel, factory=fab)
        sp.set_expand(attr == "name")
        cv.append_column(sp)
    sw = Gtk.ScrolledWindow(vexpand=True, hexpand=True)
    sw.set_child(cv)
    return sw


def baum_liste():
    st = Gtk.TreeStore(str, str)
    for i in range(1, 41):
        it = st.append(None, [f"Ordner {i}", f"{i * 3} Objekte"])
        if i % 5 == 1:
            for j in range(3):
                st.append(it, [f"Unterordner {i}.{j}", "–"])
    tv = Gtk.TreeView(model=st)
    for n, titel in enumerate(("Name", "Inhalt")):
        tv.append_column(Gtk.TreeViewColumn(titel, Gtk.CellRendererText(), text=n))
    tv.expand_row(Gtk.TreePath.new_first(), False)
    tv.get_selection().select_path(Gtk.TreePath.new_from_string("2"))
    sw = Gtk.ScrolledWindow(vexpand=True, hexpand=True)
    sw.set_child(tv)
    return sw


def listen_seite():
    p = Gtk.Paned(orientation=Gtk.Orientation.HORIZONTAL, position=420)
    p.set_start_child(spalten_liste())
    p.set_end_child(baum_liste())
    return p


def regler_seite():
    b = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10, margin_top=12,
                margin_bottom=12, margin_start=12, margin_end=12)
    s = Gtk.Scale.new_with_range(Gtk.Orientation.HORIZONTAL, 0, 100, 1)
    s.set_value(60)
    s.set_draw_value(True)
    b.append(s)
    s2 = Gtk.Scale.new_with_range(Gtk.Orientation.HORIZONTAL, 0, 100, 1)
    s2.set_value(30)
    for v in (0, 25, 50, 75, 100):
        s2.add_mark(v, Gtk.PositionType.BOTTOM, None)
    b.append(s2)
    s3 = Gtk.Scale.new_with_range(Gtk.Orientation.HORIZONTAL, 0, 100, 1)
    s3.set_value(45)
    s3.set_sensitive(False)
    b.append(s3)
    for anteil, text in ((0.35, None), (0.8, "80 %")):
        pb = Gtk.ProgressBar(fraction=anteil)
        if text:
            pb.set_show_text(True)
            pb.set_text(text)
        b.append(pb)
    lv = Gtk.LevelBar(min_value=0, max_value=1, value=0.6)
    b.append(lv)
    h = Gtk.Box(spacing=12)
    vs = Gtk.Scale.new_with_range(Gtk.Orientation.VERTICAL, 0, 100, 1)
    vs.set_value(40)
    vs.set_size_request(-1, 120)
    h.append(vs)
    sp = Gtk.Spinner(spinning=True)
    h.append(sp)
    cal = Gtk.Calendar()
    h.append(cal)
    b.append(h)
    return b


def text_seite():
    b = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8, margin_top=12,
                margin_bottom=12, margin_start=12, margin_end=12)
    l = Gtk.Label(xalign=0, wrap=True, selectable=True)
    l.set_markup("Normaler Text, <b>fett</b>, <i>kursiv</i> und ein "
                 "<a href='https://querencialinux.org'>Verweis</a>. "
                 "Deaktivierter Text folgt.")
    b.append(l)
    d = Gtk.Label(label="Deaktivierter Text", xalign=0)
    d.set_sensitive(False)
    b.append(d)
    dim = Gtk.Label(label="Gedimmter Hinweistext (dim-label)", xalign=0)
    dim.add_css_class("dim-label")
    b.append(dim)
    tv = Gtk.TextView(vexpand=True)
    buf = tv.get_buffer()
    buf.set_text("Ein Textfeld.\nDie Auswahl erscheint in Orange.\n" * 12)
    buf.select_range(buf.get_iter_at_line(1)[1], buf.get_iter_at_line(2)[1])
    sw = Gtk.ScrolledWindow(vexpand=True)
    sw.set_child(tv)
    b.append(sw)
    exp = Gtk.Expander(label="Erweiterer", expanded=True)
    exp.set_child(Gtk.Label(label="Inhalt des Erweiterers", xalign=0))
    b.append(exp)
    return b


def aktivieren(app):
    w = Gtk.ApplicationWindow(application=app, title="Querencia-Klassisch – Musterseite")
    w.set_default_size(820, 600)
    app.set_menubar(menue())
    w.set_show_menubar(True)
    for name in ("nix", "quit"):
        a = Gio.SimpleAction.new(name, None)
        if name == "quit":
            a.connect("activate", lambda *_: app.quit())
        app.add_action(a)
    aus = Gio.SimpleAction.new("aus", None)
    aus.set_enabled(False)
    app.add_action(aus)
    app.add_action(Gio.SimpleAction.new_stateful("schalter", None, GLib.Variant.new_boolean(True)))

    v = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
    tb = Gtk.Box(spacing=2)
    tb.add_css_class("toolbar")
    for icon, text in (("document-new", "Neu"), ("document-open", "Öffnen"), ("document-save", "Speichern")):
        bt = Gtk.Button()
        bb = Gtk.Box(spacing=4)
        bb.append(Gtk.Image(icon_name=icon))
        bb.append(Gtk.Label(label=text))
        bt.set_child(bb)
        tb.append(bt)
    tb.append(Gtk.Separator(orientation=Gtk.Orientation.VERTICAL))
    bt = Gtk.Button(label="Gedrückt")
    tb.append(bt)
    v.append(tb)

    nb = Gtk.Notebook(vexpand=True)
    seiten = {"knoepfe": ("Knöpfe und Felder", knoepfe_seite()),
              "listen": ("Listen", listen_seite()),
              "regler": ("Regler", regler_seite()),
              "text": ("Text", text_seite())}
    for _k, (titel, inhalt) in seiten.items():
        nb.append_page(inhalt, Gtk.Label(label=titel))
    nb.set_current_page(list(seiten).index(SEITE))
    v.append(nb)
    st = Gtk.Box(spacing=6)
    st.add_css_class("statusbar")
    st.append(Gtk.Label(label="Statusleiste: 200 Objekte", xalign=0))
    v.append(st)
    w.set_child(v)
    if EXTRA == "klein":
        w.set_default_size(420, 320)
    w.present()

    def danach():
        if EXTRA == "dialog":
            dlg = Gtk.AlertDialog(message="Änderungen speichern?",
                                  detail="Ohne Speichern gehen die Änderungen verloren.",
                                  buttons=["Abbrechen", "Nicht speichern", "Speichern"],
                                  default_button=2, cancel_button=0)
            dlg.choose(w, None, None)
        elif EXTRA == "popover":
            knoepfe_seite.menuknopf.popup()
        elif EXTRA == "tooltip":
            pass
        return False

    GLib.timeout_add(600, danach)


app = Gtk.Application(application_id="org.querencia.ThemaMuster", flags=Gio.ApplicationFlags.NON_UNIQUE)
app.connect("activate", aktivieren)
app.run([])
