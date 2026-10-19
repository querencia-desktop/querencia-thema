#!/usr/bin/env python3
"""Musterseite für das GTK-3-Thema (Fremdprogramme), über ctypes, weil die
VM kein GObject-Introspection für GTK 3 hat. Nur im isolierten Lauf
(belege.sh muster3).
"""

import ctypes
import sys

gtk = ctypes.CDLL("libgtk-3.so.0")
gobj = ctypes.CDLL("libgobject-2.0.so.0")

P = ctypes.c_void_p
S = ctypes.c_char_p
I = ctypes.c_int
D = ctypes.c_double


def f(name, res, *args):
    fn = getattr(gtk, name)
    fn.restype = res
    fn.argtypes = list(args)
    return fn


gtk_init = f("gtk_init", None, P, P)
win_new = f("gtk_window_new", P, I)
win_title = f("gtk_window_set_title", None, P, S)
win_size = f("gtk_window_set_default_size", None, P, I, I)
box_new = f("gtk_box_new", P, I, I)
pack = f("gtk_box_pack_start", None, P, P, I, I, ctypes.c_uint)
add = f("gtk_container_add", None, P, P)
border = f("gtk_container_set_border_width", None, P, ctypes.c_uint)
label_new = f("gtk_label_new", P, S)
button_new = f("gtk_button_new_with_label", P, S)
toggle_new = f("gtk_toggle_button_new_with_label", P, S)
toggle_set = f("gtk_toggle_button_set_active", None, P, I)
inconsistent = f("gtk_toggle_button_set_inconsistent", None, P, I)
sensitive = f("gtk_widget_set_sensitive", None, P, I)
tooltip = f("gtk_widget_set_tooltip_text", None, P, S)
ctx = f("gtk_widget_get_style_context", P, P)
add_class = f("gtk_style_context_add_class", None, P, S)
entry_new = f("gtk_entry_new", P)
entry_text = f("gtk_entry_set_text", None, P, S)
spin_new = f("gtk_spin_button_new_with_range", P, D, D, D)
combo_new = f("gtk_combo_box_text_new", P)
combo_add = f("gtk_combo_box_text_append_text", None, P, S)
combo_set = f("gtk_combo_box_set_active", None, P, I)
check_new = f("gtk_check_button_new_with_label", P, S)
radio_new = f("gtk_radio_button_new_with_label_from_widget", P, P, S)
switch_new = f("gtk_switch_new", P)
switch_set = f("gtk_switch_set_active", None, P, I)
scale_new = f("gtk_scale_new_with_range", P, I, D, D, D)
range_set = f("gtk_range_set_value", None, P, D)
progress_new = f("gtk_progress_bar_new", P)
progress_set = f("gtk_progress_bar_set_fraction", None, P, D)
menubar_new = f("gtk_menu_bar_new", P)
menu_new = f("gtk_menu_new", P)
mitem_new = f("gtk_menu_item_new_with_mnemonic", P, S)
mitem_sub = f("gtk_menu_item_set_submenu", None, P, P)
shell_append = f("gtk_menu_shell_append", None, P, P)
sep_item = f("gtk_separator_menu_item_new", P)
toolbar_new = f("gtk_toolbar_new", P)
toolbar_style = f("gtk_toolbar_set_style", None, P, I)
toolbutton_new = f("gtk_tool_button_new", P, P, S)
toolbutton_icon = f("gtk_tool_button_set_icon_name", None, P, S)
toolbar_insert = f("gtk_toolbar_insert", None, P, P, I)
nb_new = f("gtk_notebook_new", P)
nb_append = f("gtk_notebook_append_page", I, P, P, P)
sw_new = f("gtk_scrolled_window_new", P, P, P)
frame_new = f("gtk_frame_new", P, S)
status_new = f("gtk_statusbar_new", P)
status_push = f("gtk_statusbar_push", ctypes.c_uint, P, ctypes.c_uint, S)
store_new = f("gtk_list_store_newv", P, I, ctypes.POINTER(ctypes.c_size_t))
store_append = f("gtk_list_store_append", None, P, P)
store_set = gtk.gtk_list_store_set
store_set.restype = None
tv_new = f("gtk_tree_view_new_with_model", P, P)
renderer_new = f("gtk_cell_renderer_text_new", P)
tv_col = gtk.gtk_tree_view_insert_column_with_attributes
tv_col.restype = I
tv_sel = f("gtk_tree_view_get_selection", P, P)
path_new = f("gtk_tree_path_new_from_string", P, S)
sel_path = f("gtk_tree_selection_select_path", None, P, P)
show_all = f("gtk_widget_show_all", None, P)
main = f("gtk_main", None)
textview_new = f("gtk_text_view_new", P)
linkbutton_new = f("gtk_link_button_new_with_label", P, S, S)


def klasse(w, name):
    add_class(ctx(w), name.encode())


def b(s):
    return s.encode()


gtk_init(None, None)
w = win_new(0)
win_title(w, b("Querencia-Klassisch – GTK-3-Musterseite"))
win_size(w, 760, 560)
v = box_new(1, 0)
add(w, v)

mb = menubar_new()
for titel, eintraege in (("_Datei", ["Neu", "Öffnen …", "-", "Beenden"]),
                         ("_Bearbeiten", ["Ausschneiden", "Kopieren", "Einfügen"]),
                         ("_Hilfe", ["Info"])):
    top = mitem_new(b(titel))
    m = menu_new()
    for e in eintraege:
        shell_append(m, sep_item() if e == "-" else mitem_new(b(e)))
    mitem_sub(top, m)
    shell_append(mb, top)
pack(v, mb, 0, 0, 0)

tb = toolbar_new()
toolbar_style(tb, 2)  # Symbol und Text
for i, (icon, text) in enumerate((("document-new", "Neu"), ("document-open", "Öffnen"),
                                  ("document-save", "Speichern"))):
    t = toolbutton_new(None, b(text))
    toolbutton_icon(t, b(icon))
    toolbar_insert(tb, t, i)
pack(v, tb, 0, 0, 0)

nb = nb_new()
pack(v, nb, 1, 1, 0)

# Seite 1: Knöpfe und Felder
s1 = box_new(1, 8)
border(s1, 12)
r = box_new(0, 6)
for text, kl, an in (("Normal", None, True), ("Deaktiviert", None, False),
                     ("Übernehmen", "suggested-action", True), ("Löschen", "destructive-action", True)):
    k = button_new(b(text))
    if kl:
        klasse(k, kl)
    sensitive(k, int(an))
    pack(r, k, 0, 0, 0)
t = toggle_new(b("Umschalter"))
toggle_set(t, 1)
pack(r, t, 0, 0, 0)
pack(s1, r, 0, 0, 0)
r = box_new(0, 6)
e = entry_new()
entry_text(e, b("Querencia Desktop"))
pack(r, e, 0, 0, 0)
e = entry_new()
entry_text(e, b("deaktiviert"))
sensitive(e, 0)
pack(r, e, 0, 0, 0)
pack(r, spin_new(0, 100, 1), 0, 0, 0)
c = combo_new()
for x in ("Ambiance", "Human", "Clearlooks"):
    combo_add(c, b(x))
combo_set(c, 0)
pack(r, c, 0, 0, 0)
pack(s1, r, 0, 0, 0)
r = box_new(0, 12)
k = check_new(b("An"))
toggle_set(k, 1)
pack(r, k, 0, 0, 0)
pack(r, check_new(b("Aus")), 0, 0, 0)
k = check_new(b("Unbestimmt"))
inconsistent(k, 1)
pack(r, k, 0, 0, 0)
r1 = radio_new(None, b("Eins"))
pack(r, r1, 0, 0, 0)
pack(r, radio_new(r1, b("Zwei")), 0, 0, 0)
sw = switch_new()
switch_set(sw, 1)
pack(r, sw, 0, 0, 0)
pack(s1, r, 0, 0, 0)
sc = scale_new(0, 0, 100, 1)
range_set(sc, 60)
pack(s1, sc, 0, 0, 0)
pb = progress_new()
progress_set(pb, 0.45)
pack(s1, pb, 0, 0, 0)
fr = frame_new(b("Rahmen"))
add(fr, label_new(b("Inhalt eines Rahmens")))
pack(s1, fr, 0, 0, 0)
k = button_new(b("Mit Tooltip"))
tooltip(k, b("Ein Tooltip im Stil von Ubuntu 10.04"))
pack(s1, k, 0, 0, 0)
pack(s1, linkbutton_new(b("https://querencialinux.org"), b("Verweis")), 0, 0, 0)
nb_append(nb, s1, label_new(b("Knöpfe und Felder")), None)

# Seite 2: Liste mit Spalten
G_TYPE_STRING = 16 << 2
typen = (ctypes.c_size_t * 3)(G_TYPE_STRING, G_TYPE_STRING, G_TYPE_STRING)
st = store_new(3, typen)
it = ctypes.create_string_buffer(64)
for i in range(1, 121):
    store_append(st, it)
    store_set(P(st), it, I(0), S(b(f"Datei-{i:03d}.txt")), I(1), S(b(f"{(i * 37) % 900 + 1} KB")),
              I(2), S(b(["Textdokument", "Bild", "Ordner"][i % 3])), I(-1))
tv = tv_new(st)
for n, titel in enumerate(("Name", "Größe", "Art")):
    tv_col(P(tv), I(-1), S(b(titel)), P(renderer_new()), S(b"text"), I(n), P(None))
sel_path(tv_sel(tv), path_new(b"2"))
sc = sw_new(None, None)
add(sc, tv)
nb_append(nb, sc, label_new(b("Liste")), None)
nb_append(nb, textview_new(), label_new(b("Text")), None)

sb = status_new()
status_push(sb, 1, b("Statusleiste: 120 Objekte"))
pack(v, sb, 0, 0, 0)

show_all(w)
if len(sys.argv) > 1 and sys.argv[1] == "liste":
    f("gtk_notebook_set_current_page", None, P, I)(nb, 1)
main()
