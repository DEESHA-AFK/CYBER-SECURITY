import hmac
import hashlib
import time
import secrets
import math
import tkinter as tk
from tkinter import ttk, messagebox


class PrettyMACStudio(tk.Tk):
    THEMES = {
        "dark": {
            "bg": "#0B0F19",
            "sidebar": "#111827",
            "card": "#1F2937",
            "card_border": "#374151",
            "input_bg": "#111827",
            "text": "#F9FAFB",
            "muted": "#9CA3AF",
            "accent_grad_start": "#6366F1",  
            "accent_grad_end": "#EC4899",    
            "btn_bg": "#8B5CF6",           
            "btn_hover": "#A855F7",
            "success": "#10B981",            
            "danger": "#EF4444",            
            "chip_bg": "#374151",
            "toggle_bg": "#374151",
            "toggle_fg": "#F9FAFB"
        },
        "light": {
            "bg": "#F3F4F6",
            "sidebar": "#FFFFFF",
            "card": "#FFFFFF",
            "card_border": "#E5E7EB",
            "input_bg": "#F9FAFB",
            "text": "#111827",
            "muted": "#6B7280",
            "accent_grad_start": "#3B82F6",  
            "accent_grad_end": "#8B5CF6",    
            "btn_bg": "#4F46E5",
            "btn_hover": "#6366F1",
            "success": "#059669",
            "danger": "#DC2626",
            "chip_bg": "#E5E7EB",
            "toggle_bg": "#E5E7EB",
            "toggle_fg": "#111827"
        }
    }

    def __init__(self):
        super().__init__()

        self.title("✨ HMAC Security Operations Studio")
        self.geometry("960x700")
        self.minsize(880, 620)

        self.current_theme = "dark"
        self.c = self.THEMES[self.current_theme]
        self.active_tab = "generate"
        self.anim_step = 0

        self.init_layout()
        self.apply_theme()
        self.animate_gradient()

    def init_layout(self):
        self.shell = tk.Frame(self)
        self.shell.pack(fill="both", expand=True)

#1. SIDEBAR (Left Navigation)
        self.sidebar = tk.Frame(self.shell, width=230, bd=0)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        self.brand_box = tk.Frame(self.sidebar, pady=25, padx=20)
        self.brand_box.pack(fill="x")

        self.lbl_logo = tk.Label(
            self.brand_box, text="⚡ SECURE.MAC",
            font=("Segoe UI", 13, "bold")
        )
        self.lbl_logo.pack(anchor="w")

        self.lbl_sublogo = tk.Label(
            self.brand_box, text="Crypto Signature Studio",
            font=("Segoe UI", 8)
        )
        self.lbl_sublogo.pack(anchor="w")

        self.nav_box = tk.Frame(self.sidebar, padx=12, pady=10)
        self.nav_box.pack(fill="x")

        self.btn_nav_gen = self.create_nav_pill("⚡  Generator", "generate")
        self.btn_nav_ver = self.create_nav_pill("🛡️  Verification", "verify")
        self.btn_nav_log = self.create_nav_pill("📜  Audit Log", "audit")

        self.theme_toggle_btn = tk.Button(
            self.sidebar, text="🌙 Dark Mode", font=("Segoe UI", 8, "bold"),
            bd=0, cursor="hand2", pady=8, command=self.toggle_theme
        )
        self.theme_toggle_btn.pack(side="bottom", fill="x", padx=15, pady=20)

#2. MAIN WORKSPACE
        self.workspace = tk.Frame(self.shell)
        self.workspace.pack(side="right", fill="both", expand=True)

        self.header_canvas = tk.Canvas(self.workspace, height=75, bd=0, highlightthickness=0)
        self.header_canvas.pack(fill="x")

        self.view_container = tk.Frame(self.workspace, padx=25, pady=20)
        self.view_container.pack(fill="both", expand=True)

        self.view_gen = tk.Frame(self.view_container)
        self.view_ver = tk.Frame(self.view_container)
        self.view_log = tk.Frame(self.view_container)

        self.build_generator_tab()
        self.build_verifier_tab()
        self.build_audit_tab()

        self.switch_view("generate")

    def create_nav_pill(self, label, tab_id):
        btn = tk.Button(
            self.nav_box, text=label, font=("Segoe UI", 9, "bold"),
            anchor="w", bd=0, cursor="hand2", pady=10, padx=14,
            command=lambda: self.switch_view(tab_id)
        )
        btn.pack(fill="x", pady=4)
        return btn

    def switch_view(self, tab_id):
        self.active_tab = tab_id
        self.view_gen.pack_forget()
        self.view_ver.pack_forget()
        self.view_log.pack_forget()

        if tab_id == "generate":
            self.view_gen.pack(fill="both", expand=True)
        elif tab_id == "verify":
            self.view_ver.pack(fill="both", expand=True)
        elif tab_id == "audit":
            self.view_log.pack(fill="both", expand=True)

        self.apply_theme()

    def create_pretty_card(self, parent, title_text=""):
        card = tk.Frame(parent, padx=18, pady=14, bd=1)
        card.pack(fill="x", pady=(0, 15))

        if title_text:
            lbl = tk.Label(card, text=title_text, font=("Segoe UI", 8, "bold"))
            lbl.pack(anchor="w", pady=(0, 8))
        else:
            lbl = None

        return card, lbl

    def build_generator_tab(self):
        card1, self.lbl_g1 = self.create_pretty_card(self.view_gen, "CRYPTOGRAPHIC SETTINGS")

        row1 = tk.Frame(card1)
        row1.pack(fill="x", pady=(0, 6))

        tk.Label(row1, text="Algorithm:", font=("Segoe UI", 8)).pack(side="left")
        self.algo_var = tk.StringVar(value="SHA-256")
        self.algo_menu = ttk.OptionMenu(row1, self.algo_var, "SHA-256", "SHA-256", "SHA-512", "SHA3-256", "MD5")
        self.algo_menu.pack(side="left", padx=(8, 0))

        self.btn_gen_key = tk.Button(
            row1, text="✨ Random Key", font=("Segoe UI", 8, "bold"),
            bd=0, cursor="hand2", padx=10, command=self.generate_random_key
        )
        self.btn_gen_key.pack(side="right")

        self.gen_key = tk.Entry(card1, font=("Consolas", 10), bd=1, relief="solid")
        self.gen_key.insert(0, "b4a8e291f0c3d456789abcdef12345678")
        self.gen_key.pack(fill="x", ipady=5)

        card2, self.lbl_g2 = self.create_pretty_card(self.view_gen, "PAYLOAD DATA")
        self.gen_msg = tk.Text(card2, font=("Consolas", 9), height=5, bd=1, relief="solid")
        self.gen_msg.insert("1.0", '{\n  "user_id": "usr_99824",\n  "status": "authenticated",\n  "access_level": "admin"\n}')
        self.gen_msg.pack(fill="x")

        self.btn_compute = tk.Button(
            self.view_gen, text="GENERATE SIGNATURE", font=("Segoe UI", 9, "bold"),
            bd=0, cursor="hand2", pady=8, command=self.on_generate
        )
        self.btn_compute.pack(fill="x", pady=(0, 15))

        card3, self.lbl_g3 = self.create_pretty_card(self.view_gen, "COMPUTED HMAC SIGNATURE (HEX)")
        self.gen_out = tk.Entry(card3, font=("Consolas", 10, "bold"), bd=1, relief="solid")
        self.gen_out.pack(fill="x", ipady=6)

    def build_verifier_tab(self):
        card1, self.lbl_v1 = self.create_pretty_card(self.view_ver, "SHARED SECRET KEY")
        self.ver_key = tk.Entry(card1, font=("Consolas", 10), bd=1, relief="solid")
        self.ver_key.insert(0, "b4a8e291f0c3d456789abcdef12345678")
        self.ver_key.pack(fill="x", ipady=5)

        card2, self.lbl_v2 = self.create_pretty_card(self.view_ver, "")
        hdr_row = tk.Frame(card2)
        hdr_row.pack(fill="x", pady=(0, 6))

        self.lbl_v_hdr = tk.Label(hdr_row, text="RECEIVED PAYLOAD", font=("Segoe UI", 8, "bold"))
        self.lbl_v_hdr.pack(side="left")

        self.btn_tamper = tk.Button(
            hdr_row, text="⚡ Simulate Tamper", font=("Segoe UI", 8, "bold"),
            bd=0, cursor="hand2", padx=8, command=self.on_tamper
        )
        self.btn_tamper.pack(side="right")

        self.ver_msg = tk.Text(card2, font=("Consolas", 9), height=4, bd=1, relief="solid")
        self.ver_msg.insert("1.0", '{\n  "user_id": "usr_99824",\n  "status": "authenticated",\n  "access_level": "admin"\n}')
        self.ver_msg.pack(fill="x")

        card3, self.lbl_v3 = self.create_pretty_card(self.view_ver, "EXPECTED SIGNATURE")
        self.ver_target = tk.Entry(card3, font=("Consolas", 10), bd=1, relief="solid")
        self.ver_target.pack(fill="x", ipady=5)

        self.btn_verify = tk.Button(
            self.view_ver, text="VERIFY AUTHENTICITY", font=("Segoe UI", 9, "bold"),
            bd=0, cursor="hand2", pady=8, command=self.on_verify
        )
        self.btn_verify.pack(fill="x", pady=(0, 15))

        self.ver_status_card = tk.Frame(self.view_ver, padx=15, pady=10, bd=1)
        self.ver_status_card.pack(fill="x")
        self.lbl_status = tk.Label(
            self.ver_status_card, text="STATUS: AWAITING SIGNATURE VERIFICATION",
            font=("Segoe UI", 9, "bold")
        )
        self.lbl_status.pack(anchor="w")

    def build_audit_tab(self):
        card, self.lbl_l1 = self.create_pretty_card(self.view_log, "REAL-TIME AUDIT LOG CONSOLE")
        self.log_text = tk.Text(card, font=("Consolas", 9), bd=1, relief="solid")
        self.log_text.pack(fill="both", expand=True)
        self.log_event("SYSTEM", "Cryptographic studio ready.")

# ACTIONS & LOGIC
    def generate_random_key(self):
        key = secrets.token_hex(16)
        self.gen_key.delete(0, tk.END)
        self.gen_key.insert(0, key)
        self.log_event("KEYGEN", f"New key generated: {key[:8]}...")

    def on_generate(self):
        key = self.gen_key.get().encode("utf-8")
        msg = self.gen_msg.get("1.0", tk.END).strip().encode("utf-8")
        algo = self.algo_var.get().replace("-", "").lower()

        hash_func = getattr(hashlib, algo, hashlib.sha256)
        sig = hmac.new(key, msg, hash_func).hexdigest()

        self.gen_out.delete(0, tk.END)
        self.gen_out.insert(0, sig)
        self.log_event("SIGN", f"Algorithm: {self.algo_var.get()} | MAC: {sig[:12]}...")

    def on_tamper(self):
        msg = self.ver_msg.get("1.0", tk.END).strip()
        if '"admin"' in msg:
            msg = msg.replace('"admin"', '"root_hacked"')
        else:
            msg += "\n/* ATTACKER TAMPERED */"
        self.ver_msg.delete("1.0", tk.END)
        self.ver_msg.insert("1.0", msg)
        self.log_event("TAMPER", "Modified message stream in verification editor.")

    def on_verify(self):
        key = self.ver_key.get().encode("utf-8")
        msg = self.ver_msg.get("1.0", tk.END).strip().encode("utf-8")
        target = self.ver_target.get().strip()

        if not target:
            self.lbl_status.config(text="⚠️ STATUS: MISSING SIGNATURE TO VERIFY", fg="#EAB308")
            return

        algo = self.algo_var.get().replace("-", "").lower()
        hash_func = getattr(hashlib, algo, hashlib.sha256)
        expected = hmac.new(key, msg, hash_func).hexdigest()

        if hmac.compare_digest(expected, target):
            self.lbl_status.config(text="✓ STATUS: AUTHENTIC (SIGNATURE & PAYLOAD MATCH)", fg=self.c["success"])
            self.log_event("VERIFY_PASS", "Payload integrity confirmed.")
        else:
            self.lbl_status.config(text="❌ STATUS: TAMPERED (SIGNATURE MISMATCH)", fg=self.c["danger"])
            self.log_event("VERIFY_FAIL", "Signature verification failure!")

    def log_event(self, category, msg):
        ts = time.strftime("%H:%M:%S")
        self.log_text.insert(tk.END, f"[{ts}] [{category}] {msg}\n")
        self.log_text.see(tk.END)

# VISUAL & ANIMATION ENGINE
    def toggle_theme(self):
        self.current_theme = "light" if self.current_theme == "dark" else "dark"
        self.c = self.THEMES[self.current_theme]
        self.theme_toggle_btn.config(text="☀️ Light Mode" if self.current_theme == "dark" else "🌙 Dark Mode")
        self.apply_theme()

    def animate_gradient(self):
        self.anim_step += 0.05
        w = self.header_canvas.winfo_width() or 700
        h = 75

        self.header_canvas.delete("all")

        self.header_canvas.create_rectangle(0, 0, w, h, fill=self.c["sidebar"], width=0)

        shift = (math.sin(self.anim_step) + 1) / 2
        r1, g1, b1 = int(99 + shift * 50), int(102 + shift * 30), 241
        color_hex = f"#{r1:02x}{g1:02x}{b1:02x}"

        self.header_canvas.create_rectangle(0, h-4, w, h, fill=color_hex, width=0)

        titles = {
            "generate": ("HMAC Signature Generator", "Create cryptographic digests using SHA-256/512 keys"),
            "verify": ("Payload Integrity Verifier", "Validate data streams and protect against tampering"),
            "audit": ("System Security & Audit Log", "Real-time audit history of cryptographic operations")
        }
        title, subtitle = titles[self.active_tab]

        self.header_canvas.create_text(25, 25, text=title, fill=self.c["text"], font=("Segoe UI", 12, "bold"), anchor="w")
        self.header_canvas.create_text(25, 48, text=subtitle, fill=self.c["muted"], font=("Segoe UI", 8), anchor="w")

        self.after(50, self.animate_gradient)

    def apply_theme(self):
        c = self.c

        self.configure(bg=c["bg"])
        self.shell.configure(bg=c["bg"])
        self.sidebar.configure(bg=c["sidebar"])
        self.brand_box.configure(bg=c["sidebar"])
        self.nav_box.configure(bg=c["sidebar"])

        self.lbl_logo.configure(bg=c["sidebar"], fg=c["text"])
        self.lbl_sublogo.configure(bg=c["sidebar"], fg=c["muted"])

        for btn, tab_id in [(self.btn_nav_gen, "generate"), (self.btn_nav_ver, "verify"), (self.btn_nav_log, "audit")]:
            is_active = self.active_tab == tab_id
            btn.configure(
                bg=c["btn_bg"] if is_active else c["sidebar"],
                fg="#FFFFFF" if is_active else c["muted"],
                activebackground=c["btn_hover"] if is_active else c["card_border"],
                activeforeground="#FFFFFF"
            )

        self.theme_toggle_btn.configure(
            bg=c["toggle_bg"], fg=c["toggle_fg"], activebackground=c["card_border"]
        )

        self.workspace.configure(bg=c["bg"])
        self.view_container.configure(bg=c["bg"])
        self.view_gen.configure(bg=c["bg"])
        self.view_ver.configure(bg=c["bg"])
        self.view_log.configure(bg=c["bg"])

        for view in [self.view_gen, self.view_ver, self.view_log]:
            for child in view.children.values():
                if isinstance(child, tk.Frame):
                    child.configure(bg=c["card"], highlightbackground=c["card_border"], highlightthickness=1)
                    for sub in child.children.values():
                        if isinstance(sub, tk.Label):
                            sub.configure(bg=c["card"], fg=c["muted"])
                        elif isinstance(sub, tk.Frame):
                            sub.configure(bg=c["card"])
                            for inner in sub.children.values():
                                if isinstance(inner, tk.Label):
                                    inner.configure(bg=c["card"], fg=c["text"])

        self.btn_compute.configure(bg=c["btn_bg"], fg="#FFFFFF", activebackground=c["btn_hover"])
        self.btn_verify.configure(bg=c["btn_bg"], fg="#FFFFFF", activebackground=c["btn_hover"])
        self.btn_gen_key.configure(bg=c["chip_bg"], fg=c["text"], activebackground=c["card_border"])
        self.btn_tamper.configure(bg=c["chip_bg"], fg=c["danger"], activebackground=c["card_border"])

        # Text Inputs
        for entry in [self.gen_key, self.gen_out, self.ver_key, self.ver_target]:
            entry.configure(bg=c["input_bg"], fg=c["text"], insertbackground=c["text"],
                            highlightbackground=c["card_border"], highlightthickness=1)

        for txt in [self.gen_msg, self.ver_msg, self.log_text]:
            txt.configure(bg=c["input_bg"], fg=c["text"], insertbackground=c["text"],
                          highlightbackground=c["card_border"], highlightthickness=1)

        self.ver_status_card.configure(bg=c["card"], highlightbackground=c["card_border"], highlightthickness=1)
        self.lbl_status.configure(bg=c["card"], fg=c["muted"])


if __name__ == "__main__":
    app = PrettyMACStudio()
    app.mainloop()
