import tkinter as tk
from tkinter import ttk

alphabet = "abcdefghijklmnopqrstuvwxyz"

# Caesar Cipher
def caesar_encrypt(message, shift):
    result = ""
    for letter in message.lower():
        if letter in alphabet:
            old_position = alphabet.index(letter)
            new_position = (old_position + shift) % 26
            result += alphabet[new_position]
        else:
            result += letter
    return result


def caesar_decrypt(message, shift):
    return caesar_encrypt(message, -shift)

# Monoalphabetic (Keyword) Cipher
def build_key_alphabet(keyword):
    keyword = keyword.lower()
    seen = []
    for letter in keyword:
        if letter.isalpha() and letter not in seen:
            seen.append(letter)
    for letter in alphabet:
        if letter not in seen:
            seen.append(letter)
    return "".join(seen)


def mono_encrypt(message, keyword):
    key_alphabet = build_key_alphabet(keyword)
    result = ""
    for letter in message.lower():
        if letter in alphabet:
            position = alphabet.index(letter)
            result += key_alphabet[position]
        else:
            result += letter
    return result


def mono_decrypt(message, keyword):
    key_alphabet = build_key_alphabet(keyword)
    result = ""
    for letter in message.lower():
        if letter in key_alphabet:
            position = key_alphabet.index(letter)
            result += alphabet[position]
        else:
            result += letter
    return result


# Palette — dark "cipher terminal" theme
BG = "#0B0F17"
PANEL = "#131A26"
PANEL_BORDER = "#22303F"
NEON_GREEN = "#39FF88"
NEON_CYAN = "#4CE8FF"
NEON_AMBER = "#FFC24C"
TEXT_MAIN = "#D8E1EC"
TEXT_DIM = "#5F7386"
DANGER = "#FF5C6C"

MONO_FONT = "Consolas"

window = tk.Tk()
window.title("CIPHER://terminal")
window.geometry("880x560")
window.configure(bg=BG)
window.resizable(False, False)

style = ttk.Style()
style.theme_use("clam")
style.configure("Term.TEntry", font=(MONO_FONT, 11), padding=8,
                fieldbackground="#0F1520", foreground=NEON_GREEN, insertcolor=NEON_GREEN)
style.configure("Green.TButton", font=(MONO_FONT, 10, "bold"), foreground=BG,
                background=NEON_GREEN, borderwidth=0, padding=10)
style.map("Green.TButton", background=[("active", "#2FE377")])
style.configure("Cyan.TButton", font=(MONO_FONT, 10, "bold"), foreground=BG,
                background=NEON_CYAN, borderwidth=0, padding=10)
style.map("Cyan.TButton", background=[("active", "#33D2F0")])
style.configure("Outline.TButton", font=(MONO_FONT, 10, "bold"), foreground=TEXT_MAIN,
                background="#1A2432", borderwidth=1, padding=10)
style.map("Outline.TButton", background=[("active", "#22303F")])

# Top bar
topbar = tk.Frame(window, bg=BG, height=64)
topbar.pack(fill="x")
topbar.pack_propagate(False)

tk.Label(topbar, text="●", font=(MONO_FONT, 12), fg=DANGER, bg=BG).place(x=20, y=22)
tk.Label(topbar, text="●", font=(MONO_FONT, 12), fg=NEON_AMBER, bg=BG).place(x=38, y=22)
tk.Label(topbar, text="●", font=(MONO_FONT, 12), fg=NEON_GREEN, bg=BG).place(x=56, y=22)

tk.Label(topbar, text="CLASSICAL SUBSTITUITION TECHNIQUES", font=(MONO_FONT, 14, "bold"),
         fg=NEON_GREEN, bg=BG).place(x=90, y=16)
tk.Label(topbar, text="two classical engines · live decrypt/encrypt", font=(MONO_FONT, 8),
         fg=TEXT_DIM, bg=BG).place(x=90, y=40)

# Split panel container
container = tk.Frame(window, bg=BG)
container.pack(fill="both", expand=True, padx=20, pady=(4, 20))

left_panel = tk.Frame(container, bg=PANEL, highlightbackground=PANEL_BORDER, highlightthickness=1)
left_panel.pack(side="left", fill="both", expand=True, padx=(0, 10))

right_panel = tk.Frame(container, bg=PANEL, highlightbackground=PANEL_BORDER, highlightthickness=1)
right_panel.pack(side="left", fill="both", expand=True, padx=(10, 0))


def panel_header(parent, tag, title, color):
    bar = tk.Frame(parent, bg=PANEL)
    bar.pack(fill="x", padx=18, pady=(16, 4))
    tk.Label(bar, text=tag, font=(MONO_FONT, 8, "bold"), fg=BG, bg=color, padx=6, pady=2).pack(side="left")
    tk.Label(bar, text=title, font=(MONO_FONT, 12, "bold"), fg=TEXT_MAIN, bg=PANEL).pack(side="left", padx=(8, 0))
    sep = tk.Frame(parent, bg=PANEL_BORDER, height=1)
    sep.pack(fill="x", padx=18, pady=(6, 12))


# LEFT: Caesar Cipher
panel_header(left_panel, " CAESAR ", "Shift Cipher", NEON_GREEN)

tk.Label(left_panel, text="$ message", font=(MONO_FONT, 8, "bold"), fg=TEXT_DIM, bg=PANEL).pack(anchor="w", padx=18)
caesar_message_entry = ttk.Entry(left_panel, style="Term.TEntry")
caesar_message_entry.pack(fill="x", padx=18, pady=(4, 12))

tk.Label(left_panel, text="$ shift", font=(MONO_FONT, 8, "bold"), fg=TEXT_DIM, bg=PANEL).pack(anchor="w", padx=18)
caesar_shift_entry = ttk.Entry(left_panel, style="Term.TEntry", width=8)
caesar_shift_entry.insert(0, "3")
caesar_shift_entry.pack(anchor="w", padx=18, pady=(4, 16))

caesar_btn_row = tk.Frame(left_panel, bg=PANEL)
caesar_btn_row.pack(fill="x", padx=18, pady=(0, 14))

caesar_result_var = tk.StringVar(value="awaiting input...")


def caesar_do_encrypt():
    try:
        shift = int(caesar_shift_entry.get())
        caesar_result_var.set(caesar_encrypt(caesar_message_entry.get(), shift))
    except ValueError:
        caesar_result_var.set("ERROR: shift must be an integer")


def caesar_do_decrypt():
    try:
        shift = int(caesar_shift_entry.get())
        caesar_result_var.set(caesar_decrypt(caesar_message_entry.get(), shift))
    except ValueError:
        caesar_result_var.set("ERROR: shift must be an integer")


ttk.Button(caesar_btn_row, text="ENCRYPT »", style="Green.TButton", command=caesar_do_encrypt).pack(
    side="left", expand=True, fill="x", padx=(0, 6))
ttk.Button(caesar_btn_row, text="« DECRYPT", style="Outline.TButton", command=caesar_do_decrypt).pack(
    side="left", expand=True, fill="x", padx=(6, 0))

tk.Label(left_panel, text="$ output", font=(MONO_FONT, 8, "bold"), fg=TEXT_DIM, bg=PANEL).pack(anchor="w", padx=18)
caesar_out = tk.Label(left_panel, textvariable=caesar_result_var, font=(MONO_FONT, 11, "bold"),
                       fg=NEON_GREEN, bg="#0F1520", justify="left", anchor="w",
                       wraplength=330, padx=12, pady=12)
caesar_out.pack(fill="x", padx=18, pady=(4, 18))

# RIGHT: Monoalphabetic Cipher
panel_header(right_panel, " MONO ", "Keyword Substitution", NEON_CYAN)

tk.Label(right_panel, text="$ message", font=(MONO_FONT, 8, "bold"), fg=TEXT_DIM, bg=PANEL).pack(anchor="w", padx=18)
mono_message_entry = ttk.Entry(right_panel, style="Term.TEntry")
mono_message_entry.pack(fill="x", padx=18, pady=(4, 12))

tk.Label(right_panel, text="$ keyword", font=(MONO_FONT, 8, "bold"), fg=TEXT_DIM, bg=PANEL).pack(anchor="w", padx=18)
mono_keyword_entry = ttk.Entry(right_panel, style="Term.TEntry")
mono_keyword_entry.insert(0, "SECURITY")
mono_keyword_entry.pack(fill="x", padx=18, pady=(4, 8))

mono_mapping_var = tk.StringVar()


def mono_update_mapping(*_):
    kw = mono_keyword_entry.get()
    key_alpha = build_key_alphabet(kw) if kw.strip() else alphabet
    mono_mapping_var.set(f"PLAIN  {alphabet.upper()}\nCIPHER {key_alpha.upper()}")


mono_keyword_entry.bind("<KeyRelease>", mono_update_mapping)

tk.Label(right_panel, textvariable=mono_mapping_var, font=(MONO_FONT, 8), fg=NEON_AMBER,
         bg="#0F1520", justify="left", anchor="w", padx=12, pady=8).pack(fill="x", padx=18, pady=(0, 14))
mono_update_mapping()

mono_btn_row = tk.Frame(right_panel, bg=PANEL)
mono_btn_row.pack(fill="x", padx=18, pady=(0, 14))

mono_result_var = tk.StringVar(value="awaiting input...")


def mono_do_encrypt():
    keyword = mono_keyword_entry.get()
    if not keyword.strip():
        mono_result_var.set("ERROR: keyword required")
        return
    mono_result_var.set(mono_encrypt(mono_message_entry.get(), keyword))


def mono_do_decrypt():
    keyword = mono_keyword_entry.get()
    if not keyword.strip():
        mono_result_var.set("ERROR: keyword required")
        return
    mono_result_var.set(mono_decrypt(mono_message_entry.get(), keyword))


ttk.Button(mono_btn_row, text="ENCRYPT »", style="Cyan.TButton", command=mono_do_encrypt).pack(
    side="left", expand=True, fill="x", padx=(0, 6))
ttk.Button(mono_btn_row, text="« DECRYPT", style="Outline.TButton", command=mono_do_decrypt).pack(
    side="left", expand=True, fill="x", padx=(6, 0))

tk.Label(right_panel, text="$ output", font=(MONO_FONT, 8, "bold"), fg=TEXT_DIM, bg=PANEL).pack(anchor="w", padx=18)
mono_out = tk.Label(right_panel, textvariable=mono_result_var, font=(MONO_FONT, 11, "bold"),
                     fg=NEON_CYAN, bg="#0F1520", justify="left", anchor="w",
                     wraplength=330, padx=12, pady=12)
mono_out.pack(fill="x", padx=18, pady=(4, 18))

window.mainloop()
