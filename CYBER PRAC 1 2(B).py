import tkinter as tk
from tkinter import ttk, messagebox
import math

# 1. CORE CRYPTOGRAPHY LOGIC
def encrypt_rail_fence(text, key):
    if key <= 1: return text
    rails = [['' for _ in range(len(text))] for _ in range(key)]
    row, step = 0, 1
    for i, char in enumerate(text):
        rails[row][i] = char
        if row == 0: step = 1
        elif row == key - 1: step = -1
        row += step
    return "".join(["".join([c for c in r if c != '']) for r in rails])

def decrypt_rail_fence(cipher, key):
    if key <= 1: return cipher
    rails = [['' for _ in range(len(cipher))] for _ in range(key)]
    row, step = 0, 1
    for i in range(len(cipher)):
        rails[row][i] = '*'
        if row == 0: step = 1
        elif row == key - 1: step = -1
        row += step
    index = 0
    for r in range(key):
        for c in range(len(cipher)):
            if rails[r][c] == '*' and index < len(cipher):
                rails[r][c] = cipher[index]
                index += 1
    result, row, step = [], 0, 1
    for i in range(len(cipher)):
        result.append(rails[row][i])
        if row == 0: step = 1
        elif row == key - 1: step = -1
        row += step
    return "".join(result)

def encrypt_columnar(text, keyword):
    if not keyword: return text
    num_cols = len(keyword)
    num_rows = math.ceil(len(text) / num_cols)
    padded_text = text.ljust(num_rows * num_cols, '_')
    grid = [padded_text[i:i+num_cols] for i in range(0, len(padded_text), num_cols)]
    col_order = sorted(list(enumerate(keyword)), key=lambda x: x[1])
    return "".join(["".join([row[col_idx] for row in grid]) for col_idx, _ in col_order])

def decrypt_columnar(cipher, keyword):
    if not keyword: return cipher
    num_cols = len(keyword)
    num_rows = math.ceil(len(cipher) / num_cols)
    grid = [['' for _ in range(num_cols)] for _ in range(num_rows)]
    col_order = sorted(list(enumerate(keyword)), key=lambda x: x[1])
    cipher_idx = 0
    for col_idx, _ in col_order:
        for row_idx in range(num_rows):
            if cipher_idx < len(cipher):
                grid[row_idx][col_idx] = cipher[cipher_idx]
                cipher_idx += 1
    return "".join(["".join(row) for row in grid]).rstrip('_')

# 2. PRETTY MODERN DARK GUI
class ModernCipherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Transposition Cipher Studio")
        self.root.geometry("650x650")
        self.root.configure(bg="#1e1e2e") 
        
        # Color Palette Definitions
        self.BG_MAIN = "#1e1e2e"
        self.BG_CARD = "#252538"
        self.ACCENT_PURPLE = "#cba6f7"
        self.ACCENT_BLUE = "#89b4fa"
        self.ACCENT_GREEN = "#a6e3a1"
        self.TEXT_MAIN = "#cdd6f4"
        self.TEXT_MUTED = "#a6adc8"
        self.INPUT_BG = "#313244"

        # Global Config for Dropdowns/Inputs
        style = ttk.Style()
        style.theme_use('default')
        style.configure("TCombobox", fieldbackground=self.INPUT_BG, background=self.BG_CARD, foreground=self.TEXT_MAIN, arrowcolor=self.ACCENT_PURPLE)
        
        self.setup_ui()

    def setup_ui(self):
        # --- TITLE HERO BANNER ---
        title_frame = tk.Frame(self.root, bg=self.BG_MAIN)
        title_frame.pack(fill="x", pady=(25, 15))
        
        lbl_title = tk.Label(title_frame, text="🔒 TRANSPOSITION STUDIO", font=("Segoe UI", 18, "bold"), fg=self.ACCENT_PURPLE, bg=self.BG_MAIN)
        lbl_title.pack()
        lbl_subtitle = tk.Label(title_frame, text="Secure processing using Rail Fence & Columnar techniques", font=("Segoe UI", 10), fg=self.TEXT_MUTED, bg=self.BG_MAIN)
        lbl_subtitle.pack(pady=(2, 0))

        # --- CONTAINER CARD ---
        main_card = tk.Frame(self.root, bg=self.BG_CARD, bd=0, highlightbackground="#313244", highlightthickness=1)
        main_card.pack(fill="both", expand=True, padx=25, pady=(0, 25))

        # SECTION 1: Algorithm Selector
        lbl_sec1 = tk.Label(main_card, text="ALGORITHM", font=("Segoe UI", 10, "bold"), fg=self.ACCENT_BLUE, bg=self.BG_CARD)
        lbl_sec1.pack(anchor="w", padx=20, pady=(20, 5))
        
        self.cipher_choice = tk.StringVar(value="Rail Fence")
        self.dropdown = ttk.Combobox(main_card, textvariable=self.cipher_choice, values=["Rail Fence", "Columnar Transposition"], state="readonly", font=("Segoe UI", 11))
        self.dropdown.pack(fill="x", padx=20)
        self.dropdown.bind("<<ComboboxSelected>>", self.update_key_helper_text)

        # SECTION 2: Configuration Key
        self.lbl_sec2 = tk.Label(main_card, text="KEY (Number of Rails)", font=("Segoe UI", 10, "bold"), fg=self.ACCENT_BLUE, bg=self.BG_CARD)
        self.lbl_sec2.pack(anchor="w", padx=20, pady=(15, 5))
        
        self.entry_key = tk.Entry(main_card, font=("Segoe UI", 11), bg=self.INPUT_BG, fg=self.TEXT_MAIN, bd=0, insertbackground=self.TEXT_MAIN, highlightthickness=1, highlightbackground="#45475a")
        self.entry_key.pack(fill="x", padx=20, ipady=6)
        self.entry_key.insert(0, "3") 

        # SECTION 3: Input Field
        lbl_sec3 = tk.Label(main_card, text="INPUT STRING", font=("Segoe UI", 10, "bold"), fg=self.ACCENT_BLUE, bg=self.BG_CARD)
        lbl_sec3.pack(anchor="w", padx=20, pady=(15, 5))
        
        self.txt_input = tk.Text(main_card, height=4, font=("Segoe UI", 11), bg=self.INPUT_BG, fg=self.TEXT_MAIN, bd=0, insertbackground=self.TEXT_MAIN, highlightthickness=1, highlightbackground="#45475a", wrap="word")
        self.txt_input.pack(fill="x", padx=20)

        # ACTION BUTTONS GRID
        btn_frame = tk.Frame(main_card, bg=self.BG_CARD)
        btn_frame.pack(fill="x", padx=20, pady=20)

        btn_encrypt = tk.Button(btn_frame, text="EXECUTE ENCRYPTION", font=("Segoe UI", 10, "bold"), bg=self.ACCENT_PURPLE, fg=self.BG_MAIN, activebackground="#b4befe", activeforeground=self.BG_MAIN, bd=0, cursor="hand2", command=self.run_encrypt)
        btn_encrypt.pack(side="left", expand=True, fill="x", padx=(0, 5), ipady=8)
        
        btn_decrypt = tk.Button(btn_frame, text="EXECUTE DECRYPTION", font=("Segoe UI", 10, "bold"), bg=self.ACCENT_GREEN, fg=self.BG_MAIN, activebackground="#94e2d5", activeforeground=self.BG_MAIN, bd=0, cursor="hand2", command=self.run_decrypt)
        btn_decrypt.pack(side="right", expand=True, fill="x", padx=(5, 0), ipady=8)

        # SECTION 4: Output Field
        lbl_sec4 = tk.Label(main_card, text="OUTPUT RESULT", font=("Segoe UI", 10, "bold"), fg=self.ACCENT_BLUE, bg=self.BG_CARD)
        lbl_sec4.pack(anchor="w", padx=20, pady=(5, 5))
        
        self.txt_output = tk.Text(main_card, height=4, font=("Segoe UI", 11, "bold"), bg="#181825", fg=self.ACCENT_PURPLE, bd=0, highlightthickness=1, highlightbackground="#313244", wrap="word")
        self.txt_output.pack(fill="x", padx=20, pady=(0, 20))

    def update_key_helper_text(self, event=None):
        if self.cipher_choice.get() == "Rail Fence":
            self.lbl_sec2.config(text="KEY (Number of Rails - e.g., 3)")
            self.entry_key.delete(0, tk.END)
            self.entry_key.insert(0, "3")
        else:
            self.lbl_sec2.config(text="KEY (Alphabetic Word Phase - e.g., SECRET)")
            self.entry_key.delete(0, tk.END)
            self.entry_key.insert(0, "SECRET")

    def validate_inputs(self):
        text = self.txt_input.get("1.0", tk.END).strip()
        key_raw = self.entry_key.get().strip()
        
        if not text:
            messagebox.showwarning("Empty Input", "Please provide a message inside the Input text area.")
            return None, None
            
        if self.cipher_choice.get() == "Rail Fence":
            try:
                key = int(key_raw)
                if key <= 1: raise ValueError
                return text, key
            except ValueError:
                messagebox.showerror("Key Type Mis-match", "Rail Fence algorithm demands a positive whole integer greater than 1.")
                return None, None
        else:
            if not key_raw.isalpha():
                messagebox.showerror("Key Type Mis-match", "Columnar Transposition requires a purely text alphabet keyword string (A-Z).")
                return None, None
            return text, key_raw

    def run_encrypt(self):
        text, key = self.validate_inputs()
        if text is None: return
        
        if self.cipher_choice.get() == "Rail Fence":
            res = encrypt_rail_fence(text, key)
        else:
            res = encrypt_columnar(text, key)
            
        self.txt_output.config(fg=self.ACCENT_PURPLE)
        self.txt_output.delete("1.0", tk.END)
        self.txt_output.insert(tk.END, res)

    def run_decrypt(self):
        text, key = self.validate_inputs()
        if text is None: return
        
        if self.cipher_choice.get() == "Rail Fence":
            res = decrypt_rail_fence(text, key)
        else:
            res = decrypt_columnar(text, key)
            
        self.txt_output.config(fg=self.ACCENT_GREEN)
        self.txt_output.delete("1.0", tk.END)
        self.txt_output.insert(tk.END, res)

if __name__ == "__main__":
    root = tk.Tk()
    app = ModernCipherApp(root)
    root.mainloop()
