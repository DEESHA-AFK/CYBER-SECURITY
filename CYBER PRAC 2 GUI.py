import math
import tkinter as tk
from tkinter import ttk, messagebox

# RSA Helper Functions
def mod_inverse(e, phi):
    """Calculates modular multiplicative inverse using Extended Euclidean Algorithm."""
    def extended_gcd(a, b):
        if a == 0:
            return b, 0, 1
        gcd, x1, y1 = extended_gcd(b % a, a)
        x = y1 - (b // a) * x1
        y = x1
        return gcd, x, y

    gcd, x, _ = extended_gcd(e, phi)
    if gcd != 1:
        raise ValueError("Modular inverse does not exist")
    return x % phi

EASY_PRIMES = [(11, 13), (13, 17), (17, 19), (19, 23), (23, 29), (61, 53)]

# GUI Application
class RSAGUIApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Easy RSA Cryptosystem Workbench")
        self.geometry("820x680")
        self.minsize(780, 620)
        
        self.prime_index = 0
        
        self.p = None
        self.q = None
        self.n = None
        self.phi = None
        self.e = None
        self.d = None

        self.setup_styles()
        self.create_widgets()
        
        self.set_easy_keys(p_val=11, q_val=13)

    def setup_styles(self):
        self.style = ttk.Style(self)
        self.style.theme_use('clam')

        self.bg_color = "#1E1E2E"
        self.card_bg = "#2A2A3C"
        self.accent_color = "#74C7EC"
        self.text_color = "#CDD6F4"
        self.subtext_color = "#A6ADC8"

        self.configure(bg=self.bg_color)

        self.style.configure(".", background=self.bg_color, foreground=self.text_color, font=("Segoe UI", 10))
        self.style.configure("TLabelframe", background=self.card_bg, borderwidth=1, relief="solid")
        self.style.configure("TLabelframe.Label", background=self.card_bg, foreground=self.accent_color, font=("Segoe UI", 11, "bold"))
        self.style.configure("TButton", font=("Segoe UI", 10, "bold"), background="#313244", foreground=self.text_color, borderwidth=0)
        self.style.map("TButton", background=[("active", "#45475A")])
        self.style.configure("Accent.TButton", background="#89B4FA", foreground="#11111B")
        self.style.map("Accent.TButton", background=[("active", "#B4BEFE")])

    def create_widgets(self):
        header = tk.Frame(self, bg="#11111B", height=60)
        header.pack(fill="x", side="top")
        
        title_lbl = tk.Label(
            header, text="T076 RSA Visualizer", 
            bg="#11111B", fg=self.accent_color, 
            font=("Segoe UI", 16, "bold")
        )
        title_lbl.pack(pady=12)

        main_container = ttk.Frame(self, padding=15)
        main_container.pack(fill="both", expand=True)

        key_frame = ttk.LabelFrame(main_container, text=" 1. Key Parameters (Small Numbers) ", padding=10)
        key_frame.pack(fill="x", pady=5)

        btn_box_keys = ttk.Frame(key_frame)
        btn_box_keys.pack(side="top", anchor="w", pady=(0, 8))

        btn_gen = ttk.Button(btn_box_keys, text="⚡ Load Next Easy Primes", style="Accent.TButton", command=self.cycle_easy_keys)
        btn_gen.pack(side="left", padx=(0, 5))

        math_grid = ttk.Frame(key_frame)
        math_grid.pack(fill="x")

        self.lbl_p = self.create_key_field(math_grid, "Prime p:", 0, 0)
        self.lbl_q = self.create_key_field(math_grid, "Prime q:", 0, 1)
        self.lbl_n = self.create_key_field(math_grid, "Modulus (n = p×q):", 1, 0)
        self.lbl_phi = self.create_key_field(math_grid, "φ(n) = (p-1)(q-1):", 1, 1)
        self.lbl_e = self.create_key_field(math_grid, "Public Exp (e):", 2, 0)
        self.lbl_d = self.create_key_field(math_grid, "Private Exp (d):", 2, 1)

        crypto_frame = ttk.LabelFrame(main_container, text=" 2. Encryption & Decryption Workspace ", padding=10)
        crypto_frame.pack(fill="both", expand=True, pady=10)

        ttk.Label(crypto_frame, text="Plaintext Input:").pack(anchor="w")
        self.txt_input = tk.Text(crypto_frame, height=3, bg="#181825", fg=self.text_color, insertbackground="white", font=("Consolas", 11), relief="flat")
        self.txt_input.pack(fill="x", pady=(2, 8))
        self.txt_input.insert("1.0", "HI")

        btn_box = ttk.Frame(crypto_frame)
        btn_box.pack(fill="x", pady=2)
        
        btn_encrypt = ttk.Button(btn_box, text="🔒 Encrypt Message", command=self.encrypt_message)
        btn_encrypt.pack(side="left", padx=(0, 5))

        btn_decrypt = ttk.Button(btn_box, text="🔓 Decrypt Ciphertext", command=self.decrypt_message)
        btn_decrypt.pack(side="left")

        ttk.Label(crypto_frame, text="Output / Result:").pack(anchor="w", pady=(8, 0))
        self.txt_output = tk.Text(crypto_frame, height=4, bg="#181825", fg=self.accent_color, insertbackground="white", font=("Consolas", 11), relief="flat")
        self.txt_output.pack(fill="x", pady=(2, 0))

    def create_key_field(self, parent, label, row, col):
        frame = ttk.Frame(parent)
        frame.grid(row=row, column=col, sticky="ew", padx=10, pady=2)
        parent.columnconfigure(col, weight=1)

        ttk.Label(frame, text=label, font=("Segoe UI", 9, "bold"), foreground=self.subtext_color).pack(side="left")
        val_lbl = tk.Label(frame, text="-", bg=self.card_bg, fg=self.text_color, font=("Consolas", 10, "bold"))
        val_lbl.pack(side="right")
        return val_lbl

    def set_easy_keys(self, p_val, q_val):
        """Sets small numbers so calculations are easy to trace."""
        self.p = p_val
        self.q = q_val
        self.n = self.p * self.q
        self.phi = (self.p - 1) * (self.q - 1)

        for e_candidate in [7, 17, 3, 5, 11]:
            if e_candidate < self.phi and math.gcd(e_candidate, self.phi) == 1:
                self.e = e_candidate
                break

        self.d = mod_inverse(self.e, self.phi)

        self.lbl_p.config(text=str(self.p))
        self.lbl_q.config(text=str(self.q))
        self.lbl_n.config(text=str(self.n))
        self.lbl_phi.config(text=str(self.phi))
        self.lbl_e.config(text=str(self.e))
        self.lbl_d.config(text=str(self.d))

    def cycle_easy_keys(self):
        self.prime_index = (self.prime_index + 1) % len(EASY_PRIMES)
        p_val, q_val = EASY_PRIMES[self.prime_index]
        self.set_easy_keys(p_val, q_val)

    def encrypt_message(self):
        plaintext = self.txt_input.get("1.0", tk.END).rstrip("\n")
        if not plaintext:
            messagebox.showwarning("Empty Input", "Please enter a plaintext message.")
            return

        cipher_blocks = []
        for char in plaintext:
            m = ord(char)
            if m >= self.n:
                messagebox.showwarning(
                    "Small Modulus Warning", 
                    f"Character '{char}' (ASCII {m}) is larger than n={self.n}.\n"
                    "Click 'Load Next Easy Primes' to get a slightly larger n!"
                )
                return
            c = pow(m, self.e, self.n)
            cipher_blocks.append(c)

        cipher_str = ", ".join(map(str, cipher_blocks))
        self.txt_output.delete("1.0", tk.END)
        self.txt_output.insert(tk.END, cipher_str)

    def decrypt_message(self):
        cipher_input = self.txt_output.get("1.0", tk.END).strip()
        if not cipher_input:
            messagebox.showwarning("Empty Ciphertext", "No ciphertext found to decrypt.")
            return

        try:
            cipher_blocks = [int(x.strip()) for x in cipher_input.split(",") if x.strip()]
            decrypted_chars = [chr(pow(c, self.d, self.n)) for c in cipher_blocks]
            decrypted_text = "".join(decrypted_chars)

            self.txt_input.delete("1.0", tk.END)
            self.txt_input.insert(tk.END, decrypted_text)
            messagebox.showinfo("Success", "Decrypted back to Plaintext!")
        except Exception as err:
            messagebox.showerror("Error", f"Failed to decrypt: {err}")

if __name__ == "__main__":
    app = RSAGUIApp()
    app.mainloop()
