import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json, os, csv, re
from datetime import datetime
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

# ── Icon paths (sit next to the script) ──────────────────────────
_DIR       = os.path.dirname(os.path.abspath(__file__))
ICON_ICO   = os.path.join(_DIR, "icon.ico")
ICON_PNG   = os.path.join(_DIR, "icon.png")

MONTHS = ["January","February","March","April","May","June",
          "July","August","September","October","November","December"]

# ── Theme definitions ─────────────────────────────────────────────
THEMES = {
    "💖 Tickle-me-pink": {
        "BG":"#FFF0F5","PANEL":"#FFE4EF","ACCENT":"#FF85A1","ACCENT2":"#FFB3C6",
        "TEXT":"#7D3C5A","SUBTEXT":"#C07A9A","BORDER":"#F7B8D0","WHITE":"#FFFFFF",
        "GREEN":"#C8F0D0","RED":"#FFD6D6","GOLD":"#FFE9A0",
        "CHART":["#FFB3C6","#FFDDC1","#C1F0C8","#C1D4F0","#E8C1F0",
                 "#F0E8C1","#C1EEF0","#F0C1C1","#D4F0C1","#F0C1E8"],
    },
    "🌸 Barbie's Dreamhouse": {
        "BG":"#FFF0FA","PANEL":"#FF69B4","ACCENT":"#FF1493","ACCENT2":"#FF69B4",
        "TEXT":"#4A0030","SUBTEXT":"#C2185B","BORDER":"#FF69B4","WHITE":"#FFFFFF",
        "GREEN":"#C8F0D0","RED":"#FFD6D6","GOLD":"#FFE9A0",
        "CHART":["#FF69B4","#FF1493","#FFB3C6","#FF85A1","#FFDDE8",
                 "#FF4081","#F48FB1","#FCE4EC","#FF80AB","#F06292"],
    },
    "💜 Lavender Haze": {
        "BG":"#F5F0FF","PANEL":"#E8DAFF","ACCENT":"#9B59B6","ACCENT2":"#C39BD3",
        "TEXT":"#4A235A","SUBTEXT":"#8E44AD","BORDER":"#D2B4DE","WHITE":"#FFFFFF",
        "GREEN":"#D5F5E3","RED":"#FADBD8","GOLD":"#FEF9E7",
        "CHART":["#C39BD3","#A569BD","#D7BDE2","#E8DAFF","#F4ECF7",
                 "#BB8FCE","#8E44AD","#9B59B6","#6C3483","#D2B4DE"],
    },
    "🌿 Minty Fresh": {
        "BG":"#F0FFF8","PANEL":"#CCFCE8","ACCENT":"#00B894","ACCENT2":"#55EFC4",
        "TEXT":"#1B5E3B","SUBTEXT":"#27AE60","BORDER":"#A8E6CF","WHITE":"#FFFFFF",
        "GREEN":"#D5F5E3","RED":"#FADBD8","GOLD":"#FEF9E7",
        "CHART":["#A8E6CF","#55EFC4","#00CEC9","#81ECEC","#00B894",
                 "#DCEDC8","#B2DFDB","#80CBC4","#4DB6AC","#26A69A"],
    },
    "🌙 Midnight Glam": {
        "BG":"#1A1A2E","PANEL":"#16213E","ACCENT":"#2D1B4E","ACCENT2":"#8970A7",
        "TEXT":"#C084FC","SUBTEXT":"#C084FC","BORDER":"#7C3AED","WHITE":"#2D2D4E",
        "GREEN":"#1A472A","RED":"#4A1020","GOLD":"#3D3000",
        "CHART":["#E91E8C","#FF6B9D","#C084FC","#7C3AED","#F472B6",
                "#A855F7","#EC4899","#8B5CF6","#DB2777","#7C3AED"],
    },
    "🍑 Peachy Ken": {
        "BG":"#FFF8F0","PANEL":"#FFE5CC","ACCENT":"#FF7043","ACCENT2":"#FFAB91",
        "TEXT":"#4E2012","SUBTEXT":"#BF360C","BORDER":"#FFCCBC","WHITE":"#FFFFFF",
        "GREEN":"#C8F0D0","RED":"#FFD6D6","GOLD":"#FFE9A0",
        "CHART":["#FFAB91","#FF8A65","#FF7043","#FFCCBC","#FFE0B2",
                 "#FFCA28","#FFA726","#FF7043","#FF5722","#BF360C"],
    },
    "☁️ Cloud Baby": {
        "BG":"#F8F9FF","PANEL":"#E3E8FF","ACCENT":"#7986CB","ACCENT2":"#9FA8DA",
        "TEXT":"#283593","SUBTEXT":"#5C6BC0","BORDER":"#C5CAE9","WHITE":"#FFFFFF",
        "GREEN":"#E8F5E9","RED":"#FCE4EC","GOLD":"#FFF9C4",
        "CHART":["#9FA8DA","#7986CB","#5C6BC0","#C5CAE9","#E3E8FF",
                 "#B0BEC5","#90CAF9","#80DEEA","#A5D6A7","#F48FB1"],
    },
    "🌺 Tropical Creamsicle": {
        "BG":"#FFFDE7","PANEL":"#FFF9C4","ACCENT":"#F9A825","ACCENT2":"#FFD54F",
        "TEXT":"#4A3000","SUBTEXT":"#F57F17","BORDER":"#FFE082","WHITE":"#FFFFFF",
        "GREEN":"#C8F0D0","RED":"#FFD6D6","GOLD":"#FFF3CD",
        "CHART":["#FFD54F","#FFCA28","#FFC107","#FFB300","#FFA000",
                 "#FF8F00","#FF6F00","#FF7043","#FF5722","#BF360C"],
    },
}

T = dict(THEMES["💖 Tickle-me-pink"])

FNT       = ("Helvetica", 13)
FNT_B     = ("Helvetica", 14, "bold")
FNT_TITLE = ("Helvetica", 20, "bold")
FNT_S     = ("Helvetica", 11)
FNT_BIG   = ("Helvetica", 24, "bold")

DATA_FILE = os.path.join(os.path.expanduser("~"), "girl_do_not_buy_that_data.json")

CATEGORIES = ["🛍️ Shopping","🍔 Restaurants","🫑 Grocery","💅 Self-care",
              "🚗 Transport","🎉 Entertainment","✈️ Travel","💡 Utilities",
              "🏥 Medical","💼 Income","🔂 Subscriptions","🤕 Insurance","🅿️ Parking",
              "📦 Other"]

# All keys must be LOWERCASE — map_cat lowercases the raw value before matching
APPLE_MAP = {
    "restaurants":    "🍔 Restaurants",
    "groceries":      "🫑 Grocery",
    "grocery":        "🫑 Grocery",
    "shopping":       "🛍️ Shopping",
    "entertainment":  "🎉 Entertainment",
    "travel":         "✈️ Travel",
    "transportation": "🚗 Transport",
    "transport":      "🚗 Transport",
    "health":         "🏥 Medical",
    "medical":        "🏥 Medical",
    "parking":        "🅿️ Parking",
    "utilities":      "💡 Utilities",
    "subscriptions":  "🔂 Subscriptions",
    "self care":      "💅 Self-care",
    "personal care":  "💅 Self-care",
    "gifts":          "🎁 Gifts",
    "insurance":      "🤕 Insurance",
    "food and drink": "🍔 Restaurants",
    "education":      "📚 Education",
}

def map_cat(raw, unmatched_set=None):
    if not raw: return "📦 Other"
    raw_low = raw.lower().strip()
    # exact match first (Apple Card sends clean category names)
    if raw_low in APPLE_MAP:
        return APPLE_MAP[raw_low]
    # substring fallback for partial matches
    for k, v in APPLE_MAP.items():
        if k in raw_low:
            return v
    # No match — record the original value if caller wants to know
    if unmatched_set is not None and raw.strip():
        unmatched_set.add(raw.strip())
    return "📦 Other"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE) as f: return json.load(f)
    return {"transactions":[],"savings_goals":[],"budgets":{},"theme":"💖 Tickle-me-pink","starting_balance":0.0}

def save_data(data):
    with open(DATA_FILE,"w") as f: json.dump(data,f,indent=2)

def strip_emoji(text):
    return re.sub(r'[^\x00-\x7F\u00C0-\u024F\u1E00-\u1EFF]+', '', text).strip()

def btn(parent, text, cmd, color=None, fg=None, **kw):
    bg = color or T["ACCENT"]
    fg = fg or "#4A0030"
    return tk.Button(parent, text=text, command=cmd, font=FNT_B,
                     bg=bg, fg=fg, bd=0, padx=14, pady=7,
                     cursor="hand2", relief="flat",
                     activebackground=T["ACCENT2"],
                     activeforeground=T["TEXT"], **kw)


# ══════════════════════════════════════════════════════════════════
class FinanceApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("🚨 Girl Don't Buy That 🚨")
        self.geometry("1120x760")
        self.minsize(960,680)
        self.data = load_data()
        saved = self.data.get("theme","💖 Tickle-me-pink")
        if saved in THEMES: T.update(THEMES[saved])
        self.configure(bg=T["BG"])
        self._set_icon()
        self._ttk_style()
        self._build()
        self.show_frame("dashboard")

    def _set_icon(self):
        try:
            if os.name == "nt" and os.path.exists(ICON_ICO):
                self.iconbitmap(ICON_ICO)
            elif os.path.exists(ICON_PNG):
                from tkinter import PhotoImage
                try:
                    from PIL import Image, ImageTk
                    img = Image.open(ICON_PNG).resize((64, 64), Image.LANCZOS)
                    self._icon_img = ImageTk.PhotoImage(img)
                    self.iconphoto(True, self._icon_img)
                except ImportError:
                    ico = PhotoImage(file=ICON_PNG)
                    self.iconphoto(True, ico)
        except Exception:
            pass

    def _ttk_style(self):
        s = ttk.Style()
        s.theme_use("clam")
        s.configure("A.Treeview", background=T["WHITE"], fieldbackground=T["WHITE"],
                    foreground=T["TEXT"], font=FNT, rowheight=30)
        s.configure("A.Treeview.Heading", background=T["PANEL"],
                    foreground=T["TEXT"], font=FNT_B, relief="flat")
        s.map("A.Treeview", background=[("selected",T["ACCENT2"])])
        s.configure("TCombobox", fieldbackground=T["BG"], foreground=T["TEXT"])

    def _build(self):
        self.configure(bg=T["BG"])
        self.sb = tk.Frame(self, bg=T["PANEL"], width=205)
        self.sb.pack(side="left", fill="y")
        self.sb.pack_propagate(False)

        self.sb_ico = tk.Label(self.sb, text="🚨", font=("Helvetica",32), bg=T["PANEL"], fg=T["ACCENT"])
        self.sb_ico.pack(pady=(20,2))
        self.sb_ttl = tk.Label(self.sb, text="Girl Don't\nBuy That",
                                font=FNT_B, bg=T["PANEL"], fg=T["TEXT"], justify="center")
        self.sb_ttl.pack()
        self.sb_div = tk.Frame(self.sb, bg=T["BORDER"], height=1)
        self.sb_div.pack(fill="x", padx=18, pady=12)

        self.nav = {}
        nav_items = [("🏠  Home Base","dashboard"),("💸  The Damage","transactions"),
                     ("📥  Drop the Receipts","import_csv"),("🗂️  Damage Control","budgets"),
                     ("🌟  Dream Big Sis","savings"),("💰  Income Flow","income"),
                     ("📊  The Hard Truth","summary"),("🎨  Switch Vibes","themes")]
        for label, key in nav_items:
            b = tk.Button(self.sb, text=label, font=FNT, bg=T["PANEL"], fg=T["TEXT"],
                          bd=0, anchor="w", padx=20, pady=10, cursor="hand2",
                          activebackground=T["ACCENT2"], relief="flat",
                          command=lambda k=key: self.show_frame(k))
            b.pack(fill="x")
            self.nav[key] = b

        self.ct = tk.Frame(self, bg=T["BG"])
        self.ct.pack(side="left", fill="both", expand=True)

        self.frames = {}
        for name, cls in [("dashboard",DashboardFrame),("transactions",TransactionsFrame),
                           ("import_csv",ImportCSVFrame),("budgets",BudgetsFrame),
                           ("savings",SavingsFrame),("income",IncomeFrame),
                           ("summary",SummaryFrame),("themes",ThemesFrame)]:
            f = cls(self.ct, self)
            f.place(relx=0, rely=0, relwidth=1, relheight=1)
            self.frames[name] = f

    def apply_theme(self, name):
        T.update(THEMES[name])
        self.data["theme"] = name
        save_data(self.data)
        self.configure(bg=T["BG"])
        self._ttk_style()
        self.sb.configure(bg=T["PANEL"])
        self.sb_ico.configure(bg=T["PANEL"], fg=T["ACCENT"])
        self.sb_ttl.configure(bg=T["PANEL"], fg=T["TEXT"])
        self.sb_div.configure(bg=T["BORDER"])
        for b in self.nav.values():
            b.configure(bg=T["PANEL"], fg=T["TEXT"], activebackground=T["ACCENT2"])
        self.ct.configure(bg=T["BG"])
        for f in self.frames.values():
            if hasattr(f,"retheme"): f.retheme()
        self.show_frame("themes")

    def show_frame(self, name):
        for k,b in self.nav.items():
            b.configure(bg=T["ACCENT"] if k==name else T["PANEL"],
                        fg="#4A0030"   if k==name else T["TEXT"],
                        font=FNT_B     if k==name else FNT)
        self.frames[name].tkraise()
        if hasattr(self.frames[name],"refresh"): self.frames[name].refresh()


# ══════════════════════════════════════════════════════════════════
class ThemesFrame(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=T["BG"])
        self.app = app
        self.grid_f = None
        self._header()

    def _header(self):
        self.ttl = tk.Label(self, text="🎨 Switch Vibes", font=FNT_TITLE,
                             bg=T["BG"], fg=T["TEXT"])
        self.ttl.pack(pady=(20,2))
        self.sub = tk.Label(self, text="Pick your aesthetic, queen 👑 Changes save automatically ✨",
                             font=FNT, bg=T["BG"], fg=T["SUBTEXT"])
        self.sub.pack(pady=(0,14))
        self.grid_f = tk.Frame(self, bg=T["BG"])
        self.grid_f.pack(fill="both", expand=True, padx=30, pady=4)

    def retheme(self):
        self.configure(bg=T["BG"])
        self.ttl.configure(bg=T["BG"], fg=T["TEXT"])
        self.sub.configure(bg=T["BG"], fg=T["SUBTEXT"])
        self.grid_f.configure(bg=T["BG"])
        self._populate()

    def refresh(self):
        self.retheme()

    def _populate(self):
        for w in self.grid_f.winfo_children(): w.destroy()
        current = self.app.data.get("theme","💖 Tickle-me-pink")
        col = row = 0
        for name, th in THEMES.items():
            active = (name == current)
            rim = tk.Frame(self.grid_f, bg=th["ACCENT"] if active else th["BORDER"], padx=3, pady=3)
            rim.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
            card = tk.Frame(rim, bg=th["BG"], padx=16, pady=14, cursor="hand2")
            card.pack(fill="both", expand=True)
            sw = tk.Frame(card, bg=th["BG"])
            sw.pack(pady=(0,6))
            for c in [th["PANEL"],th["ACCENT"],th["ACCENT2"],th["BORDER"]]:
                tk.Frame(sw, bg=c, width=24, height=24).pack(side="left", padx=2)
            tk.Label(card, text=name, font=FNT_B, bg=th["BG"], fg=th["TEXT"]).pack()
            if active:
                tk.Label(card, text="✓ Slay Choice", font=FNT_S,
                         bg=th["BG"], fg=th["ACCENT"]).pack(pady=(4,0))
            else:
                tk.Button(card, text="Wear This One 💅", font=FNT_S,
                          bg=th["ACCENT"], fg="#4A0030", bd=0, padx=10, pady=5,
                          cursor="hand2", relief="flat",
                          command=lambda n=name: self.app.apply_theme(n)
                          ).pack(pady=(6,0))
            col += 1
            if col >= 4: col=0; row+=1
        for c in range(4): self.grid_f.columnconfigure(c, weight=1)


# ══════════════════════════════════════════════════════════════════
class DashboardFrame(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=T["BG"])
        self.app = app
        self.hdr = tk.Frame(self, bg=T["ACCENT"], pady=16)
        self.hdr.pack(fill="x")
        self.hdr_l = tk.Label(self.hdr, text="Girl Math Time!!",
                               font=FNT_TITLE, bg=T["ACCENT"], fg=T["ACCENT2"])
        self.hdr_l.pack()
        self.body = tk.Frame(self, bg=T["BG"])
        self.body.pack(fill="both", expand=True, padx=28, pady=18)

    def retheme(self):
        self.configure(bg=T["BG"])
        self.hdr.configure(bg=T["ACCENT"])
        self.hdr_l.configure(bg=T["ACCENT"], fg=T["ACCENT2"])
        self.body.configure(bg=T["BG"])
        self.refresh()

    def refresh(self):
        self.configure(bg=T["BG"])
        self.body.configure(bg=T["BG"])
        for w in self.body.winfo_children(): w.destroy()
        txns = self.app.data["transactions"]
        now  = datetime.now()
        mt   = [t for t in txns if
                datetime.fromisoformat(t["date"]).month==now.month and
                datetime.fromisoformat(t["date"]).year==now.year]
        income  = sum(t["amount"] for t in mt if t["type"]=="income")
        expense = sum(t["amount"] for t in mt if t["type"]=="expense")

        # All-time net worth
        total_in   = sum(t["amount"] for t in txns if t["type"]=="income")
        total_out  = sum(t["amount"] for t in txns if t["type"]=="expense")
        starting   = float(self.app.data.get("starting_balance", 0.0))
        net_worth  = starting + total_in - total_out
        nw_color   = "#7DC99A" if net_worth >= 0 else "#E07A7A"

        # ── Net worth banner ──────────────────────────────────────
        nw = tk.Frame(self.body, bg=T["WHITE"], highlightbackground=T["BORDER"],
                      highlightthickness=1, padx=18, pady=12)
        nw.pack(fill="x", pady=(0,10))
        left = tk.Frame(nw, bg=T["WHITE"]); left.pack(side="left", expand=True)
        tk.Label(left, text="💎 Total Net Worth", font=FNT_B, bg=T["WHITE"], fg=T["SUBTEXT"]).pack(anchor="w")
        tk.Label(left, text=f"${net_worth:,.2f}", font=FNT_BIG, bg=T["WHITE"], fg=nw_color).pack(anchor="w")
        if starting != 0:
            tk.Label(left, text=f"incl. ${starting:,.2f} starting balance",
                     font=FNT_S, bg=T["WHITE"], fg=T["SUBTEXT"]).pack(anchor="w")
        # mini breakdown on the right
        right = tk.Frame(nw, bg=T["WHITE"]); right.pack(side="right", padx=20)
        if starting != 0:
            tk.Label(right, text=f"starting:      +${starting:,.2f}", font=FNT_S, bg=T["WHITE"], fg="#7DC99A", anchor="e").pack(anchor="e")
        tk.Label(right, text=f"all-time in:   +${total_in:,.2f}",  font=FNT_S, bg=T["WHITE"], fg="#7DC99A", anchor="e").pack(anchor="e")
        tk.Label(right, text=f"all-time out:  -${total_out:,.2f}", font=FNT_S, bg=T["WHITE"], fg="#E07A7A", anchor="e").pack(anchor="e")
        tk.Label(right, text=f"{len(txns)} transactions tracked", font=FNT_S, bg=T["WHITE"], fg=T["SUBTEXT"], anchor="e").pack(anchor="e", pady=(4,0))
        def _set_starting():
            cur = self.app.data.get("starting_balance", 0.0)
            val = tk.simpledialog.askfloat("Starting Balance 💰",
                f"Enter your balance before you started tracking\n(current: ${cur:,.2f})",
                parent=self, initialvalue=cur)
            if val is not None:
                self.app.data["starting_balance"] = val
                save_data(self.app.data)
                self.refresh()
        tk.Button(nw, text="✏️ Set Starting Balance", font=FNT_S,
                  bg=T["PANEL"], fg=T["TEXT"], bd=0, padx=10, pady=5,
                  cursor="hand2", relief="flat", command=_set_starting
                  ).pack(side="bottom", anchor="w", pady=(8,0))

        # ── This month cards ──────────────────────────────────────
        row = tk.Frame(self.body, bg=T["BG"])
        row.pack(fill="x", pady=(0,14))
        for title, val, color, icon in [
                ("What's Left 😬", income-expense, T["ACCENT2"],"💰"),
                ("Money In 🙏",    income,          "#7DC99A", "📈"),
                ("Crimes 💀",      expense,         "#E07A7A", "📉")]:
            c = tk.Frame(row, bg=T["WHITE"], highlightbackground=T["BORDER"],
                         highlightthickness=1, padx=18, pady=14)
            c.pack(side="left", expand=True, fill="both", padx=6)
            tk.Label(c, text=icon, font=("Helvetica",26), bg=T["WHITE"]).pack()
            tk.Label(c, text=title, font=FNT, bg=T["WHITE"], fg=T["SUBTEXT"]).pack()
            tk.Label(c, text=f"${val:,.2f}", font=FNT_BIG, bg=T["WHITE"], fg=color).pack()
            tk.Label(c, text="this month", font=FNT_S, bg=T["WHITE"], fg=T["SUBTEXT"]).pack()

        tk.Label(self.body, text="🕐 Recent Bad Decisions", font=FNT_B,
                 bg=T["BG"], fg=T["TEXT"]).pack(anchor="w", pady=(8,4))
        c = tk.Frame(self.body, bg=T["WHITE"], highlightbackground=T["BORDER"], highlightthickness=1)
        c.pack(fill="x")
        recent = sorted(txns, key=lambda t: t["date"], reverse=True)[:8]
        if not recent:
            tk.Label(c, text="Nothing here yet... suspicious 👀  Import a CSV or confess a purchase!",
                     font=FNT, bg=T["WHITE"], fg=T["SUBTEXT"], pady=14).pack()
        for t in recent:
            bg_c = T["GREEN"] if t["type"]=="income" else T["RED"]
            sign = "+" if t["type"]=="income" else "-"
            r = tk.Frame(c, bg=T["WHITE"])
            r.pack(fill="x", padx=14, pady=3)
            tk.Label(r, text=t["category"], font=FNT, bg=T["WHITE"], fg=T["TEXT"],
                     width=20, anchor="w").pack(side="left")
            tk.Label(r, text=t.get("note",""), font=FNT_S, bg=T["WHITE"], fg=T["SUBTEXT"],
                     width=24, anchor="w").pack(side="left")
            tk.Label(r, text=t["date"][:10], font=FNT_S, bg=T["WHITE"],
                     fg=T["SUBTEXT"], width=11).pack(side="left")
            tk.Label(r, text=f"{sign}${t['amount']:.2f}", font=FNT_B,
                     bg=bg_c, fg=T["TEXT"], padx=8).pack(side="right", pady=2)

        btn(self.body, "＋ Confess a Purchase 🛍️",
            lambda: self.app.show_frame("transactions")).pack(pady=12)


# ══════════════════════════════════════════════════════════════════
class TransactionsFrame(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=T["BG"])
        self.app = app
        self._build()

    def _build(self):
        tk.Label(self, text="💸 The Confessional Booth", font=FNT_TITLE,
                 bg=T["BG"], fg=T["TEXT"]).pack(pady=(18,4))
        form = tk.Frame(self, bg=T["WHITE"], highlightbackground=T["BORDER"],
                        highlightthickness=1, padx=22, pady=14)
        form.pack(fill="x", padx=28, pady=(0,10))

        r1 = tk.Frame(form, bg=T["WHITE"]); r1.pack(fill="x", pady=3)
        tk.Label(r1, text="Type:", font=FNT, bg=T["WHITE"], fg=T["TEXT"]).pack(side="left")
        self.type_var = tk.StringVar(value="expense")
        for val,lbl in [("expense","💸 Expense"),("income","💰 Income")]:
            tk.Radiobutton(r1, text=lbl, variable=self.type_var, value=val,
                           font=FNT, bg=T["WHITE"], fg=T["TEXT"],
                           selectcolor=T["ACCENT2"], activebackground=T["WHITE"]
                           ).pack(side="left", padx=10)

        r2 = tk.Frame(form, bg=T["WHITE"]); r2.pack(fill="x", pady=3)
        tk.Label(r2, text="Category:", font=FNT, bg=T["WHITE"], fg=T["TEXT"],
                 width=10, anchor="w").pack(side="left")
        self.cat_var = tk.StringVar(value=CATEGORIES[0])
        ttk.Combobox(r2, textvariable=self.cat_var, values=CATEGORIES,
                     font=FNT, width=22, state="readonly").pack(side="left", padx=6)
        tk.Label(r2, text="Amount: $", font=FNT, bg=T["WHITE"],
                 fg=T["TEXT"]).pack(side="left", padx=(14,0))
        self.amt_var = tk.StringVar()
        tk.Entry(r2, textvariable=self.amt_var, font=FNT, width=10, bg=T["BG"],
                 fg=T["TEXT"], relief="flat", highlightbackground=T["BORDER"],
                 highlightthickness=1).pack(side="left", padx=4)

        r3 = tk.Frame(form, bg=T["WHITE"]); r3.pack(fill="x", pady=3)
        tk.Label(r3, text="Date:", font=FNT, bg=T["WHITE"], fg=T["TEXT"],
                 width=10, anchor="w").pack(side="left")
        self.date_var = tk.StringVar(value=datetime.now().strftime("%Y-%m-%d"))
        tk.Entry(r3, textvariable=self.date_var, font=FNT, width=13, bg=T["BG"],
                 fg=T["TEXT"], relief="flat", highlightbackground=T["BORDER"],
                 highlightthickness=1).pack(side="left", padx=6)
        tk.Label(r3, text="Note:", font=FNT, bg=T["WHITE"], fg=T["TEXT"]).pack(side="left", padx=(14,0))
        self.note_var = tk.StringVar()
        tk.Entry(r3, textvariable=self.note_var, font=FNT, width=28, bg=T["BG"],
                 fg=T["TEXT"], relief="flat", highlightbackground=T["BORDER"],
                 highlightthickness=1).pack(side="left", padx=6)

        bf = tk.Frame(form, bg=T["WHITE"]); bf.pack(pady=(10,0))
        btn(bf, "＋ Add It (I Won't Judge... Much) 👀", self._add).pack(side="left", padx=4)
        self.edit_btn = btn(bf, "✏️ Save Edits", self._save_edit, color=T["ACCENT2"])
        self.edit_btn.pack(side="left", padx=4)
        self.edit_btn.pack_forget()  # hidden until a row is selected for editing
        btn(bf, "✕ Cancel Edit", self._cancel_edit, color="#E0E0E0", fg="#555555").pack(side="left", padx=4)
        self._cancel_widgets = [bf.winfo_children()[-1]]
        self._cancel_widgets[-1].pack_forget()

        self._editing_idx = None  # index into sorted transactions of row being edited

        # ── Filter + header row ───────────────────────────────────
        flt = tk.Frame(self, bg=T["BG"])
        flt.pack(fill="x", padx=28, pady=(8,2))
        tk.Label(flt, text="The Full Evidence File 🗂️", font=FNT_B,
                 bg=T["BG"], fg=T["TEXT"]).pack(side="left")
        tk.Label(flt, text="  Double-click to edit ✏️", font=FNT_S,
                 bg=T["BG"], fg=T["SUBTEXT"]).pack(side="left")
        btn(flt, "☑ Select All",   self._select_all,   color=T["PANEL"], fg=T["TEXT"]).pack(side="right", padx=4)
        btn(flt, "☐ Deselect All", self._deselect_all, color=T["PANEL"], fg=T["TEXT"]).pack(side="right", padx=4)

        # Category filter
        self.filter_cat = tk.StringVar(value="All")
        ttk.Combobox(flt, textvariable=self.filter_cat,
                     values=["All"] + CATEGORIES,
                     width=16, state="readonly", font=FNT_S).pack(side="right", padx=4)
        tk.Label(flt, text="Cat:", font=FNT_S, bg=T["BG"], fg=T["SUBTEXT"]).pack(side="right")
        self.filter_cat.trace_add("write", lambda *_: self.refresh())

        # ── Date filter row ───────────────────────────────────────
        now = datetime.now()
        dflt = tk.Frame(self, bg=T["BG"])
        dflt.pack(fill="x", padx=28, pady=(0,2))
        tk.Label(dflt, text="Month:", font=FNT_S, bg=T["BG"], fg=T["SUBTEXT"]).pack(side="left")
        self.filter_month = tk.StringVar(value="All")
        ttk.Combobox(dflt, textvariable=self.filter_month,
                     values=["All"] + MONTHS,
                     width=11, state="readonly", font=FNT_S).pack(side="left", padx=4)
        tk.Label(dflt, text="Year:", font=FNT_S, bg=T["BG"], fg=T["SUBTEXT"]).pack(side="left", padx=(8,0))
        self.filter_year = tk.StringVar(value="All")
        ttk.Combobox(dflt, textvariable=self.filter_year,
                     values=["All"] + [str(y) for y in range(2020, now.year+2)],
                     width=7, state="readonly", font=FNT_S).pack(side="left", padx=4)
        btn(dflt, "✕ Clear Filters", self._clear_filters,
            color=T["PANEL"], fg=T["SUBTEXT"]).pack(side="left", padx=8)
        self.filter_month.trace_add("write", lambda *_: self.refresh())
        self.filter_year.trace_add("write", lambda *_: self.refresh())

        self.wrap = tk.Frame(self, bg=T["BG"])
        self.wrap.pack(fill="both", expand=True, padx=28, pady=(2,0))
        cols = ("✓","Date","Category","Merchant / Note","Amount")
        self.tree = ttk.Treeview(self.wrap, columns=cols, show="headings", style="A.Treeview")
        col_widths = [32,110,160,240,110]
        for col,w in zip(cols, col_widths):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=w, anchor="center", minwidth=w)
        sb2 = ttk.Scrollbar(self.wrap, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=sb2.set)
        self.tree.pack(side="left", fill="both", expand=True)
        sb2.pack(side="right", fill="y")
        self.tree.bind("<Double-1>", self._on_double_click)
        self.tree.bind("<Button-1>", self._on_click)  # toggle checkbox on click

        # checked state: maps tree item id -> bool
        self._checked = {}

        # bottom action bar
        bot = tk.Frame(self, bg=T["BG"])
        bot.pack(fill="x", padx=28, pady=6)
        self.sel_label = tk.Label(bot, text="0 selected", font=FNT_S,
                                   bg=T["BG"], fg=T["SUBTEXT"])
        self.sel_label.pack(side="left", padx=4)
        btn(bot, "🗑️ Delete Selected", self._delete, color="#E07A7A").pack(side="right", padx=4)

    def _on_double_click(self, event):
        sel = self.tree.selection()
        if not sel: return
        iid = sel[0]
        master_idx = getattr(self, "_iid_to_txn", {}).get(iid, -1)
        if master_idx < 0 or master_idx >= len(self.app.data["transactions"]): return
        t = self.app.data["transactions"][master_idx]
        self._editing_idx = master_idx

        # Populate form fields with selected transaction
        self.type_var.set(t["type"])
        self.cat_var.set(t["category"])
        self.amt_var.set(str(t["amount"]))
        self.date_var.set(t["date"][:10])
        self.note_var.set(t.get("note",""))

        # Show edit/cancel buttons, hide add button
        self.edit_btn.pack(side="left", padx=4)
        self._cancel_widgets[-1].pack(side="left", padx=4)

    def _save_edit(self):
        if self._editing_idx is None: return
        try: amt = float(self.amt_var.get())
        except ValueError:
            messagebox.showerror("Girl...","That's not a number bestie 💀"); return
        self.app.data["transactions"][self._editing_idx] = {
            "date": self.date_var.get() + "T00:00:00",
            "type": self.type_var.get(),
            "category": self.cat_var.get(),
            "note": self.note_var.get(),
            "amount": amt
        }
        save_data(self.app.data)
        self._cancel_edit()
        messagebox.showinfo("Okay bestie 🌸", "Transaction updated!")

    def _cancel_edit(self):
        self._editing_idx = None
        self.amt_var.set(""); self.note_var.set("")
        self.date_var.set(datetime.now().strftime("%Y-%m-%d"))
        self.edit_btn.pack_forget()
        self._cancel_widgets[-1].pack_forget()
        self.refresh()

    def retheme(self):
        self.configure(bg=T["BG"])
        for w in self.winfo_children(): w.destroy()
        self._build(); self.refresh()

    def _add(self):
        try: amt = float(self.amt_var.get())
        except ValueError:
            messagebox.showerror("Girl...","Bestie that's not a number 💀"); return
        self.app.data["transactions"].append({
            "date":self.date_var.get()+"T00:00:00","type":self.type_var.get(),
            "category":self.cat_var.get(),"note":self.note_var.get(),"amount":amt})
        save_data(self.app.data)
        self.amt_var.set(""); self.note_var.set("")
        self.refresh()

    def _on_click(self, event):
        """Toggle checkbox when clicking the check column or row."""
        region = self.tree.identify_region(event.x, event.y)
        if region not in ("cell", "tree"): return
        iid = self.tree.identify_row(event.y)
        col = self.tree.identify_column(event.x)
        if not iid: return
        # Toggle on click anywhere on the row (or specifically col #1)
        if col == "#1" or True:
            self._checked[iid] = not self._checked.get(iid, False)
            self._refresh_row(iid)
            self._update_sel_label()

    def _refresh_row(self, iid):
        """Re-render the checkbox cell for a given row."""
        vals = list(self.tree.item(iid, "values"))
        vals[0] = "☑" if self._checked.get(iid) else "☐"
        self.tree.item(iid, values=vals)

    def _select_all(self):
        for iid in self.tree.get_children():
            self._checked[iid] = True
            self._refresh_row(iid)
        self._update_sel_label()

    def _deselect_all(self):
        for iid in self.tree.get_children():
            self._checked[iid] = False
            self._refresh_row(iid)
        self._update_sel_label()

    def _clear_filters(self):
        self.filter_cat.set("All")
        self.filter_month.set("All")
        self.filter_year.set("All")

    def _update_sel_label(self):
        n = sum(1 for v in self._checked.values() if v)
        self.sel_label.configure(text=f"{n} selected")

    def _delete(self):
        to_delete = [iid for iid, checked in self._checked.items() if checked]
        if not to_delete:
            messagebox.showinfo("Girl...", "Select some transactions first! Use the checkboxes 👀")
            return
        if not messagebox.askyesno("Delete?", f"Delete {len(to_delete)} transaction(s)? No take-backs 💀"):
            return
        # Map iid -> transaction via the sorted order stored at insert time
        txns_sorted = sorted(self.app.data["transactions"], key=lambda t: t["date"], reverse=True)
        indices_to_delete = set()
        for iid in to_delete:
            row_idx = self.tree.index(iid)
            if row_idx < len(txns_sorted):
                orig_idx = self.app.data["transactions"].index(txns_sorted[row_idx])
                indices_to_delete.add(orig_idx)
        self.app.data["transactions"] = [
            t for i, t in enumerate(self.app.data["transactions"])
            if i not in indices_to_delete
        ]
        save_data(self.app.data)
        self._checked.clear()
        self.refresh()

    def refresh(self):
        self._checked.clear()
        for row in self.tree.get_children(): self.tree.delete(row)
        cat_filter   = self.filter_cat.get()   if hasattr(self, "filter_cat")   else "All"
        month_filter = self.filter_month.get() if hasattr(self, "filter_month") else "All"
        year_filter  = self.filter_year.get()  if hasattr(self, "filter_year")  else "All"
        txns = sorted(self.app.data["transactions"], key=lambda t:t["date"], reverse=True)
        if cat_filter != "All":
            txns = [t for t in txns if t["category"] == cat_filter]
        if month_filter != "All":
            m = MONTHS.index(month_filter) + 1
            txns = [t for t in txns if datetime.fromisoformat(t["date"]).month == m]
        if year_filter != "All":
            txns = [t for t in txns if datetime.fromisoformat(t["date"]).year == int(year_filter)]
        self._iid_to_txn = {}  # iid → index in self.app.data["transactions"]
        all_txns = self.app.data["transactions"]
        for t in txns:
            sign = "+" if t["type"]=="income" else "-"
            # Find index in master list for this transaction
            try: master_idx = all_txns.index(t)
            except ValueError: master_idx = -1
            iid = self.tree.insert("","end", values=(
                "☐",
                t["date"][:10],
                t["category"], t.get("note",""),
                f"{sign}${t['amount']:.2f}"
            ))
            self._checked[iid] = False
            self._iid_to_txn[iid] = master_idx
        self._update_sel_label()


# ══════════════════════════════════════════════════════════════════
# Skip phrases for payments TOWARD credit cards (debit statement)
CREDIT_CARD_PAYMENT_PHRASES = [
    "chase credit crd", "applecard gsbank", "apple card gsbank",
    "citi card", "amex payment", "discover payment",
    "credit card payment", "credit card autopay",
    "automatic payment", "autopay",
]

def detect_csv_format(path):
    """Sniff CSV headers to auto-detect statement format."""
    try:
        for enc in ("utf-8-sig", "utf-8", "latin-1"):
            try:
                with open(path, newline="", encoding=enc) as f:
                    for _ in range(8):
                        line = f.readline().lower()
                        if "account statement" in line or ("datetime" in line and "funding source" in line):
                            return "venmo"
                        if "datetime" in line and "from" in line and "to" in line:
                            return "venmo"
                        if "transaction date" in line and "description" in line:
                            return "credit"
                        if "posting date" in line and "details" in line:
                            return "debit"
                break
            except UnicodeDecodeError:
                continue
    except Exception:
        pass
    return "credit"

def clean_venmo_note(note):
    return re.sub(r"[^\x00-\x7F]+", "", note).strip() or "Venmo"


class ImportCSVFrame(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=T["BG"])
        self.app = app
        self.preview_data = []
        self._loaded_files = {}
        self._current_file_label = ""
        self._active_filter = None
        self._build()

    def _build(self):
        tk.Label(self, text="📥 Drop the Evidence, Bestie", font=FNT_TITLE,
                 bg=T["BG"], fg=T["TEXT"]).pack(pady=(18,4))

        # ── Month/Year filter ──────────────────────────────────────
        filter_f = tk.Frame(self, bg=T["BG"]); filter_f.pack(pady=(4,2))
        tk.Label(filter_f, text="Import for:", font=FNT, bg=T["BG"], fg=T["TEXT"]).pack(side="left")
        now = datetime.now()
        self.filter_month = tk.StringVar(value=MONTHS[now.month-1])
        ttk.Combobox(filter_f, textvariable=self.filter_month, values=MONTHS,
                     width=11, state="readonly", font=FNT).pack(side="left", padx=6)
        self.filter_year = tk.IntVar(value=now.year)
        ttk.Combobox(filter_f, textvariable=self.filter_year,
                     values=list(range(2020, now.year+2)),
                     width=7, state="readonly", font=FNT).pack(side="left", padx=4)
        tk.Label(filter_f, text="(only rows in this month/year will import)",
                 font=FNT_S, bg=T["BG"], fg=T["SUBTEXT"]).pack(side="left", padx=8)

        # ── Buttons ────────────────────────────────────────────────
        br = tk.Frame(self, bg=T["BG"]); br.pack(pady=6)
        btn(br, "📂 Add Files", self._browse).pack(side="left", padx=6)
        btn(br, "🗑️ Clear All", self._clear_files,
            color="#888888", fg="#ffffff").pack(side="left", padx=6)
        btn(br, "😤 Import All (Deep Breath)", self._import_all,
            color="#7DC99A", fg="#000000").pack(side="left", padx=6)

        # ── Loaded files list ──────────────────────────────────────
        self.files_frame = tk.Frame(self, bg=T["BG"])
        self.files_frame.pack(fill="x", padx=28, pady=(0,4))

        self.status = tk.Label(self, text="", font=FNT, bg=T["BG"], fg=T["SUBTEXT"])
        self.status.pack()
        self.unmatched_frame = tk.Frame(self, bg=T["BG"])
        self.unmatched_frame.pack(fill="x", padx=28, pady=(0,4))
        self._cat_vars = {}

        # ── Preview header + filter bar ───────────────────────────
        prev_hdr = tk.Frame(self, bg=T["BG"]); prev_hdr.pack(fill="x", padx=28, pady=(8,2))
        tk.Label(prev_hdr, text="Crime Scene Preview 🔍", font=FNT_B,
                 bg=T["BG"], fg=T["TEXT"]).pack(side="left")
        # filter chips live here (rebuilt by _refresh_filter_bar)
        self.filter_bar = tk.Frame(prev_hdr, bg=T["BG"])
        self.filter_bar.pack(side="left", padx=12)

        wrap = tk.Frame(self, bg=T["BG"])
        wrap.pack(fill="both", expand=True, padx=28, pady=(0,8))
        cols = ("File","Date","Type","Category","Description/Merchant","Amount")
        self.tree = ttk.Treeview(wrap, columns=cols, show="headings", style="A.Treeview")
        for col,w in zip(cols,[130,90,75,140,250,100]):
            self.tree.heading(col,text=col); self.tree.column(col,width=w,anchor="center")
        sb2 = ttk.Scrollbar(wrap, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=sb2.set)
        self.tree.pack(side="left", fill="both", expand=True); sb2.pack(side="right", fill="y")

        # Track loaded file paths, detected types, and active filter
        self._loaded_files = {}       # path → fmt
        self._active_filter = None    # None = show all, str = show only this file label

    def retheme(self):
        self.configure(bg=T["BG"])
        for w in self.winfo_children(): w.destroy()
        self._build()


    def _debug_csv(self):
        import io as _io, csv as _csv, traceback as _tb
        path = filedialog.askopenfilename(title="Select CSV to Debug",
               filetypes=[("CSV files","*.csv"),("All files","*.*")])
        if not path: return
        out = [f"FILE: {path}"]
        content_lines = None
        for enc in ("utf-8-sig", "utf-8", "latin-1", "cp1252"):
            try:
                with open(path, newline="", encoding=enc) as f:
                    content_lines = f.readlines()
                out.append(f"Encoding OK: {enc} — {len(content_lines)} lines")
                break
            except UnicodeDecodeError as e:
                out.append(f"  {enc}: FAILED")
        if not content_lines:
            messagebox.showerror("Debug", "No encoding worked"); return
        out.append("First 5 lines:")
        for i, line in enumerate(content_lines[:5]):
            out.append(f"  [{i}] {repr(line[:100])}")
        header_idx = None
        for i, line in enumerate(content_lines):
            ll = line.lower()
            if "datetime" in ll and "from" in ll and "to" in ll:
                header_idx = i
                out.append(f"Header at line {i}: {repr(line[:80])}")
                break
        if header_idx is None:
            out.append("NO HEADER FOUND - checking partial matches:")
            for i, line in enumerate(content_lines):
                ll = line.lower()
                if "datetime" in ll or ("from" in ll and "to" in ll):
                    out.append(f"  Line {i}: {repr(line[:80])}")
        else:
            data_block = "".join(content_lines[header_idx:])
            reader = _csv.DictReader(_io.StringIO(data_block), delimiter="\t")
            raw_fields = reader.fieldnames or []
            clean_fields = [f.strip() if f else "" for f in raw_fields]
            reader.fieldnames = clean_fields
            out.append(f"Fields: {clean_fields[:12]}")
            def gv(row, *keys):
                for k in keys:
                    for field in clean_fields:
                        if field and k.lower() in field.lower():
                            return row.get(field, "").strip()
                return ""
            out.append("Rows:")
            for i, row in enumerate(reader):
                s = gv(row, "status")
                a = gv(row, "amount (total)", "amount")
                d = gv(row, "datetime")
                fr = gv(row, "from")
                fn = gv(row, "funding source")
                out.append(f"  [{i}] status={repr(s)} amt={repr(a)} dt={repr(d[:19])} from={repr(fr[:20])} fund={repr(fn[:25])}")
        win = tk.Toplevel(self)
        win.title("CSV Debug")
        win.geometry("900x500")
        txt = tk.Text(win, font=("Courier", 10), wrap="none")
        sy = ttk.Scrollbar(win, orient="vertical", command=txt.yview)
        sx = ttk.Scrollbar(win, orient="horizontal", command=txt.xview)
        txt.configure(yscrollcommand=sy.set, xscrollcommand=sx.set)
        sy.pack(side="right", fill="y")
        sx.pack(side="bottom", fill="x")
        txt.pack(fill="both", expand=True)
        txt.insert("1.0", "\n".join(out))
        txt.configure(state="disabled")

    def _browse(self):
        paths = filedialog.askopenfilenames(title="Select CSV files",
               filetypes=[("CSV files","*.csv"),("All files","*.*")])
        for path in paths:
            if path and path not in self._loaded_files:
                self._load_csv(path)

    def _clear_files(self):
        self._loaded_files = {}
        self._active_filter = None
        self.preview_data = []
        for row in self.tree.get_children(): self.tree.delete(row)
        for w in self.files_frame.winfo_children(): w.destroy()
        for w in self.unmatched_frame.winfo_children(): w.destroy()
        self.status.configure(text="")
        self._refresh_filter_bar()

    def _refresh_files_panel(self):
        """Rebuild the file chips panel — each chip is clickable to filter preview."""
        for w in self.files_frame.winfo_children(): w.destroy()
        if not self._loaded_files: return
        for path, fmt in self._loaded_files.items():
            fname = os.path.basename(path)
            flabel = fname[:18]
            icon = {"credit":"💳","debit":"🏦","venmo":"💸"}.get(fmt,"📄")
            tag = {"credit":"Credit Card","debit":"Bank/Debit","venmo":"Venmo"}.get(fmt, fmt)
            active = (self._active_filter == flabel)
            bg_col = T["ACCENT2"] if active else T["WHITE"]
            fg_col = "white" if active else T["TEXT"]
            sub_col = "white" if active else T["SUBTEXT"]
            chip = tk.Frame(self.files_frame, bg=bg_col,
                            highlightbackground=T["ACCENT2"] if active else T["BORDER"],
                            highlightthickness=2 if active else 1,
                            padx=10, pady=4, cursor="hand2")
            chip.pack(side="left", padx=4, pady=4)
            lbl1 = tk.Label(chip, text=f"{icon} {fname}", font=FNT_S, bg=bg_col, fg=fg_col)
            lbl1.pack(side="left")
            lbl2 = tk.Label(chip, text=f"  [{tag}]", font=FNT_S, bg=bg_col, fg=sub_col)
            lbl2.pack(side="left")
            # Click to filter (toggle off if already active)
            def make_click(fl=flabel):
                def on_click(e=None):
                    self._active_filter = None if self._active_filter == fl else fl
                    self._refresh_files_panel()
                    self._refresh_filter_bar()
                    self._apply_tree_filter()
                return on_click
            cb = make_click()
            for w in (chip, lbl1, lbl2): w.bind("<Button-1>", cb)

    def _refresh_filter_bar(self):
        """Show active filter indicator next to preview label."""
        if not hasattr(self, "filter_bar"): return
        for w in self.filter_bar.winfo_children(): w.destroy()
        if self._active_filter:
            pill = tk.Frame(self.filter_bar, bg=T["ACCENT2"], padx=8, pady=2)
            pill.pack(side="left")
            tk.Label(pill, text=f"showing: {self._active_filter}  ✕",
                     font=FNT_S, bg=T["ACCENT2"], fg="white", cursor="hand2").pack()
            pill.bind("<Button-1>", lambda e: self._clear_filter())
            pill.winfo_children()[0].bind("<Button-1>", lambda e: self._clear_filter())
        else:
            tk.Label(self.filter_bar, text="(click a file to filter)",
                     font=FNT_S, bg=T["BG"], fg=T["SUBTEXT"]).pack(side="left")

    def _clear_filter(self):
        self._active_filter = None
        self._refresh_files_panel()
        self._refresh_filter_bar()
        self._apply_tree_filter()

    def _apply_tree_filter(self):
        """Show/hide tree rows based on active file filter."""
        for row in self.tree.get_children():
            vals = self.tree.item(row, "values")
            file_col = vals[0] if vals else ""
            if self._active_filter is None or file_col == self._active_filter:
                self.tree.item(row, tags=())
            else:
                # Detach rows that don't match — we rebuild instead
                pass
        # Easier: just repopulate the tree from preview_data filtered
        for row in self.tree.get_children(): self.tree.delete(row)
        for t in self.preview_data:
            flabel = t.get("_file","")
            if self._active_filter and flabel != self._active_filter:
                continue
            sign = "+" if t["type"] == "income" else "-"
            self.tree.insert("", "end", values=(
                flabel, t["date"][:10], t["type"].capitalize(),
                t["category"], t["note"], f"{sign}${t['amount']:.2f}"))

    def _remember_cat(self, note, cat):
        """Store description→category mapping for future auto-matching."""
        mem = self.app.data.setdefault("cat_memory", {})
        # Use first 3 meaningful words as key
        words = re.sub(r"[^a-z0-9 ]", "", note.lower()).split()
        key = " ".join(words[:3]) if words else note.lower()[:20]
        if key and cat != "📦 Other":
            mem[key] = cat
            save_data(self.app.data)

    def _lookup_cat_memory(self, note):
        """Check if we've seen a similar description before."""
        mem = self.app.data.get("cat_memory", {})
        words = re.sub(r"[^a-z0-9 ]", "", note.lower()).split()
        key = " ".join(words[:3]) if words else note.lower()[:20]
        return mem.get(key)

    def _parse_amount(self, raw):
        # Handle: "$17.00", "($40.00)", "+ $17.00", "- $40.00", "-20.71"
        raw = raw.replace("$", "").replace(",", "").replace("(", "-").replace(")", "")
        raw = raw.replace("+ ", "").replace("- ", "-").strip()
        try: return float(raw)
        except ValueError: return None

    def _parse_date(self, raw):
        if not raw: return None
        raw = raw.strip()
        # Try ISO with time first (Venmo: 2026-02-02T16:32:19)
        for fmt in ["%Y-%m-%dT%H:%M:%S", "%Y-%m-%d"]:
            try: return datetime.strptime(raw, fmt).isoformat()
            except: pass
        # Try date-only slice for M/D/Y formats
        date_part = raw[:10]
        for fmt in ["%m/%d/%Y", "%m/%d/%y", "%d/%m/%Y", "%m-%d-%Y"]:
            try: return datetime.strptime(date_part, fmt).isoformat()
            except: pass
        return None

    def _load_csv(self, path):
        """Load one CSV file, auto-detect its type, append to preview."""
        target_month = MONTHS.index(self.filter_month.get()) + 1
        target_year  = int(self.filter_year.get())
        fmt = detect_csv_format(path)
        self._loaded_files[path] = fmt
        self._refresh_files_panel()
        # Short label for the File column in preview tree
        self._current_file_label = os.path.basename(path)[:18]

        try:
            if fmt == "credit":
                count, ignored, _ = self._parse_credit(path, target_month, target_year)
            elif fmt == "debit":
                count, ignored, _ = self._parse_debit(path, target_month, target_year)
            elif fmt == "venmo":
                count, ignored, _ = self._parse_venmo(path, target_month, target_year)
            else:
                count, ignored, _ = self._parse_credit(path, target_month, target_year)

            total = len(self.preview_data)
            m_label = f"{self.filter_month.get()} {int(self.filter_year.get())}"
            self.status.configure(
                text=f"👀 {total} transactions across {len(self._loaded_files)} file(s) — "
                     f"last file: {count} loaded, {ignored} skipped. "
                     f"Import saves {m_label} rows (dupes skipped automatically).",
                fg="#7DC99A")
            self._refresh_filter_bar()
            self._show_unmatched_panel()
        except Exception as e:
            import traceback
            messagebox.showerror("Error", f"Could not read CSV:\n{e}\n\n{traceback.format_exc()}")
            self.status.configure(text=f"❌ Error: {e}", fg="#E07A7A")
            self._loaded_files.pop(path, None)
            self._refresh_files_panel()

    def _add_txn(self, date_iso, txn_type, note, amount, raw_cat, target_month, target_year):
        """Always add to preview — month filter and dupe check happen at import time."""
        cat = self._lookup_cat_memory(note)
        if not cat:
            # If raw_cat is already a known final category, use it directly
            if raw_cat in CATEGORIES:
                cat = raw_cat
            else:
                cat = map_cat(raw_cat)
        raw_for_panel = None
        if cat == "📦 Other":
            raw_for_panel = raw_cat or note[:30]
        file_label = getattr(self, "_current_file_label", "")
        txn = {"date": date_iso, "type": txn_type, "category": cat,
               "note": note, "amount": abs(amount), "_raw_cat": raw_for_panel,
               "_file": file_label}
        self.preview_data.append(txn)
        sign = "+" if txn_type == "income" else "-"
        self.tree.insert("", "end", values=(
            file_label, date_iso[:10], txn_type.capitalize(), cat, note,
            f"{sign}${abs(amount):.2f}"))
        return "added"

    def _parse_credit(self, path, target_month, target_year):
        """
        Handles Apple Card and Chase credit card (7472) CSVs.

        Apple Card columns: Transaction Date, Description, Merchant, Category, Type, Amount (USD)
          Type=Purchase  → expense  (amount is positive)
          Type=Debit     → cashback (amount is positive, treat as ↩️ Returns & Cashback)
          Type=Credit    → return   (amount is negative, treat as ↩️ Returns & Cashback)
          Type=Payment   → skip     (credit card payment from bank)

        Chase credit (7472) columns: Transaction Date, Post Date, Description, Category, Type, Amount
          Type=Sale      → expense  (amount is negative)
          Type=Return    → return   (amount is positive, ↩️ Returns & Cashback)
          skip: autopay / online payment rows
        """
        SKIP_DESCS = ["automatic payment", "autopay", "online payment",
                      "mobile payment", "ach payment", "internet transfer"]
        count = ignored = 0
        with open(path, newline="", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            hmap = {h.lower().strip(): h for h in (reader.fieldnames or [])}
            def get(*keys):
                for k in keys:
                    for hk, orig in hmap.items():
                        if k in hk: return lambda row, o=orig: row.get(o, "").strip()
                return lambda row: ""
            get_date = get("transaction date", "date")
            get_desc = get("description", "merchant")
            get_cat  = get("category")
            get_type = get("type")
            get_amt  = get("amount")

            for row in reader:
                amt  = self._parse_amount(get_amt(row))
                if amt is None: continue
                note = get_desc(row).strip()
                if not note: continue
                note_low = note.lower()
                if any(p in note_low for p in SKIP_DESCS):
                    ignored += 1; continue

                tl = get_type(row).lower().strip()

                # Payment rows (credit card payment from bank account) — skip
                if tl == "payment":
                    ignored += 1; continue

                # Cashback (Apple Card "Debit" = Daily Cash → Income)
                if tl == "debit":
                    txn_type = "income"
                    raw_cat  = "💼 Income"
                # Return or Credit — income but keep the SAME category as the purchase
                # so it offsets that category's total (e.g. Best Buy return → Shopping)
                elif tl in {"return", "credit", "refund"}:
                    txn_type = "income"
                    raw_cat  = get_cat(row)   # keep original category (Shopping, Grocery, etc.)
                # Normal purchase / sale
                elif tl in {"purchase", "sale"}:
                    txn_type = "expense"
                    raw_cat  = get_cat(row)
                else:
                    # Fallback: positive = income, negative = expense
                    txn_type = "income" if amt > 0 else "expense"
                    raw_cat  = get_cat(row)

                date_iso = self._parse_date(get_date(row))
                if not date_iso: ignored += 1; continue
                self._add_txn(date_iso, txn_type, note, abs(amt), raw_cat,
                              target_month, target_year)
                count += 1
        return count, ignored, 0

    def _parse_debit(self, path, target_month, target_year):
        """
        Chase bank/debit (8510) CSV.
        Columns: Details, Posting Date, Description, Amount, Type, Balance

        Details col:
          DEBIT  → expense (money out)
          CREDIT → income  (money in)

        Type col (used as fallback / additional signal):
          ACH_DEBIT / CHASE_TO_PARTNERFI → expense
          ACH_CREDIT                     → income

        Skip: payments to own credit cards and internal transfers.
        """
        SKIP_DESCS = CREDIT_CARD_PAYMENT_PHRASES + [
            "zelle payment to", "external transfer", "internet transfer",
            "venmo payment",  # already tracked in Venmo CSV
        ]
        count = ignored = 0
        with open(path, newline="", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            hmap = {h.lower().strip(): h for h in (reader.fieldnames or [])}
            def get(*keys):
                for k in keys:
                    for hk, orig in hmap.items():
                        if k in hk: return lambda row, o=orig: row.get(o, "").strip()
                return lambda row: ""
            get_details = get("details")
            get_date    = get("posting date", "date")
            get_desc    = get("description")
            get_type    = get("type")
            get_amt     = get("amount")

            for row in reader:
                amt = self._parse_amount(get_amt(row))
                if amt is None: continue
                note = re.sub(r"\s+", " ", get_desc(row).strip())
                if not note: continue
                note_low = note.lower()
                if any(p in note_low for p in SKIP_DESCS):
                    ignored += 1; continue

                details = get_details(row).strip().upper()
                type_col = get_type(row).strip().upper()

                # Primary signal: Details column
                if details == "DEBIT":
                    txn_type = "expense"
                elif details == "CREDIT":
                    txn_type = "income"
                # Fallback: Type column
                elif type_col in {"ACH_DEBIT", "CHASE_TO_PARTNERFI"}:
                    txn_type = "expense"
                elif type_col == "ACH_CREDIT":
                    txn_type = "income"
                else:
                    txn_type = "expense" if amt < 0 else "income"

                date_iso = self._parse_date(get_date(row))
                if not date_iso: ignored += 1; continue
                self._add_txn(date_iso, txn_type, note, abs(amt), "",
                              target_month, target_year)
                count += 1
        return count, ignored, 0

    def _parse_venmo(self, path, target_month, target_year):
        """
        Venmo CSV (comma-separated with 2 junk header rows).
        Columns: ID, Datetime, Type, Status, Note, From, To, Amount (total), ...

        Amount: positive (+ $17.00) = received = income
                negative (- $40.00) = sent     = expense
        Status must be "Complete". No bank-funded filter (user tracks at face value).
        """
        count = ignored = 0

        # Read with multiple encoding fallbacks
        content_lines = None
        for enc in ("utf-8-sig", "utf-8", "latin-1", "cp1252"):
            try:
                with open(path, newline="", encoding=enc) as f:
                    content_lines = f.readlines()
                break
            except UnicodeDecodeError:
                continue
        if not content_lines:
            return 0, 0, 0

        # Find the real header row (contains "Datetime" and "From")
        header_idx = None
        for i, line in enumerate(content_lines):
            ll = line.lower()
            if "datetime" in ll and "from" in ll:
                header_idx = i
                break
        if header_idx is None:
            return 0, 0, 0

        import io
        data_block = "".join(content_lines[header_idx:])
        reader = csv.DictReader(io.StringIO(data_block))
        # Strip whitespace from field names (leading blank column in Venmo)
        clean_fields = [f.strip() if f else "" for f in (reader.fieldnames or [])]
        reader.fieldnames = clean_fields

        def gv(row, *keys):
            for k in keys:
                for field in clean_fields:
                    if field and k.lower() in field.lower():
                        return row.get(field, "").strip()
            return ""

        for row in reader:
            if gv(row, "status").lower() != "complete":
                continue
            amt = self._parse_amount(gv(row, "amount (total)", "amount"))
            if amt is None or amt == 0:
                continue

            frm  = gv(row, "from")
            to   = gv(row, "to")
            note = clean_venmo_note(gv(row, "note")) or "Venmo"

            # Skip if funded from bank account (will appear on Chase debit statement)
            fund = gv(row, "funding source").lower()
            if any(x in fund for x in ("jpmorgan", "chase", "checking", "bank")):
                ignored += 1
                continue

            # Positive amount = received (income), negative = sent (expense)
            if amt > 0:
                txn_type     = "income"
                other_person = frm if frm else to
            else:
                txn_type     = "expense"
                other_person = to if to else frm

            full_note = f"{note} ({other_person})" if other_person else note
            date_iso  = self._parse_date(gv(row, "datetime"))
            if not date_iso:
                ignored += 1
                continue

            self._add_txn(date_iso, txn_type, full_note, abs(amt), "Venmo",
                          target_month, target_year)
            count += 1
        return count, ignored, 0

    def _show_unmatched_panel(self):
        """Build the per-transaction category assignment panel for 📦 Other rows."""
        for w in self.unmatched_frame.winfo_children(): w.destroy()
        self._cat_vars.clear()
        other_txns = [(i, t) for i, t in enumerate(self.preview_data)
                      if t["category"] == "📦 Other"]
        if not other_txns:
            return
        hdr_txt = f"⚠️ {len(other_txns)} transaction{'s' if len(other_txns)>1 else ''} landed in 📦 Other — assign categories below:"
        tk.Label(self.unmatched_frame, text=hdr_txt,
                 font=FNT_S, bg=T["BG"], fg="#E07A7A").pack(anchor="w", pady=(4,2))
        outer = tk.Frame(self.unmatched_frame, bg=T["BG"],
                         highlightbackground=T["BORDER"], highlightthickness=1)
        outer.pack(fill="x")
        canvas_w = tk.Canvas(outer, bg=T["BG"], highlightthickness=0,
                             height=min(len(other_txns), 5) * 46)
        vsb = ttk.Scrollbar(outer, orient="vertical", command=canvas_w.yview)
        canvas_w.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y")
        canvas_w.pack(side="left", fill="both", expand=True)
        inner = tk.Frame(canvas_w, bg=T["BG"])
        inner_id = canvas_w.create_window((0,0), window=inner, anchor="nw")
        canvas_w.bind("<Configure>", lambda e, c=canvas_w, iid=inner_id: c.itemconfig(iid, width=e.width))
        inner.bind("<Configure>", lambda e, c=canvas_w: c.configure(scrollregion=c.bbox("all")))
        # Column headers
        hdr_row = tk.Frame(inner, bg=T["PANEL"], padx=10, pady=5)
        hdr_row.pack(fill="x")
        for htext, w in [("Date",11),("Type",9),("Amount",11),
                          ("Merchant / Note",32),("CSV Category",22),("",3),("Assign To",22)]:
            tk.Label(hdr_row, text=htext, font=FNT_S, bg=T["PANEL"],
                     fg=T["SUBTEXT"], width=w or 2, anchor="w").pack(side="left", padx=4)
        for idx, (txn_i, t) in enumerate(other_txns):
            var = tk.StringVar(value="📦 Other")
            self._cat_vars[txn_i] = var
            row_bg = T["WHITE"] if idx % 2 == 0 else T["BG"]
            row_f  = tk.Frame(inner, bg=row_bg, padx=10, pady=7)
            row_f.pack(fill="x")
            sign     = "+" if t["type"]=="income" else "-"
            type_col = "#7DC99A" if t["type"]=="income" else "#E07A7A"
            tk.Label(row_f, text=t["date"][:10], font=FNT_S,
                     bg=row_bg, fg=T["SUBTEXT"], width=11, anchor="w").pack(side="left")
            tk.Label(row_f, text=t["type"].capitalize(), font=FNT_S,
                     bg=type_col, fg="#FFFFFF", padx=5, pady=1, width=7).pack(side="left", padx=4)
            tk.Label(row_f, text=f"{sign}${t['amount']:.2f}", font=FNT_B,
                     bg=row_bg, fg=T["TEXT"], width=11, anchor="w").pack(side="left", padx=4)
            tk.Label(row_f, text=(t.get("note") or "—")[:32], font=FNT_S,
                     bg=row_bg, fg=T["TEXT"], width=32, anchor="w").pack(side="left", padx=4)
            tk.Label(row_f, text=(t.get("_raw_cat") or "—")[:22], font=FNT_S,
                     bg=row_bg, fg="#E07A7A", width=22, anchor="w").pack(side="left", padx=4)
            tk.Label(row_f, text="→", font=FNT_S, bg=row_bg,
                     fg=T["SUBTEXT"]).pack(side="left", padx=2)
            cb = ttk.Combobox(row_f, textvariable=var, values=CATEGORIES,
                              width=22, state="readonly", font=FNT_S)
            cb.pack(side="left", padx=4)
            var.trace_add("write", lambda *_, ti=txn_i, v=var: self._remap_cat_by_idx(ti, v.get()))
        tk.Label(self.unmatched_frame,
                 text="Pick a category → preview updates instantly. Import saves your choices 🌸",
                 font=FNT_S, bg=T["BG"], fg=T["SUBTEXT"]).pack(anchor="w", pady=(4,0))

    def _remap_cat_by_idx(self, txn_idx, new_cat):
        """Live-update a single transaction by its index in preview_data."""
        if txn_idx >= len(self.preview_data):
            return
        self.preview_data[txn_idx]["category"] = new_cat
        # Match tree row by date + note + amount rather than by position
        t = self.preview_data[txn_idx]
        target_date = t["date"][:10]
        target_note = t.get("note", "")
        target_amt  = ("+" if t["type"]=="income" else "-") + f"${t['amount']:.2f}"
        for iid in self.tree.get_children():
            vals = list(self.tree.item(iid, "values"))
            # tree cols: Date, Type, Category, Note, Amount
            if vals[0] == target_date and vals[3] == target_note and vals[4] == target_amt:
                vals[2] = new_cat
                self.tree.item(iid, values=vals)
                break

    def _import_all(self):
        if not self.preview_data:
            messagebox.showinfo("Babe...","Bestie, you need to pick a file 😭"); return
        target_month = MONTHS.index(self.filter_month.get()) + 1
        target_year  = int(self.filter_year.get())
        existing = {(t["date"][:10],t["note"],t["amount"]) for t in self.app.data["transactions"]}
        added = dupes = skipped_month = 0
        mem = self.app.data.setdefault("cat_memory", {})
        for t in self.preview_data:
            # Apply month/year filter at import time
            row_dt = datetime.fromisoformat(t["date"])
            if row_dt.month != target_month or row_dt.year != target_year:
                skipped_month += 1
                continue
            key = (t["date"][:10], t["note"], t["amount"])
            if key not in existing:
                clean = {k:v for k,v in t.items() if k != "_raw_cat"}
                self.app.data["transactions"].append(clean)
                existing.add(key)
                added += 1
                # Save category memory
                if t["category"] != "📦 Other" and t.get("note"):
                    words = re.sub(r"[^a-z0-9 ]","",t["note"].lower()).split()
                    mem_key = " ".join(words[:3]) if words else t["note"].lower()[:20]
                    if mem_key:
                        mem[mem_key] = t["category"]
            else:
                dupes += 1
        save_data(self.app.data)
        self.app.frames["dashboard"].refresh()
        self.app.frames["transactions"].refresh()
        self.status.configure(
            text=f"🎉 Imported {added} transactions for {self.filter_month.get()} {target_year}! "
                 f"({dupes} dupes skipped, {skipped_month} other-month rows ignored 🗓️)",
            fg=T["ACCENT2"])
        messagebox.showinfo("Okay... 😤", f"Imported {added} transactions. We're gonna be okay 🌸")

    def refresh(self): pass


# ══════════════════════════════════════════════════════════════════
class BudgetsFrame(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=T["BG"])
        self.app = app; self._build()

    def _build(self):
        tk.Label(self, text="🗂️ Damage Control HQ", font=FNT_TITLE,
                 bg=T["BG"], fg=T["TEXT"]).pack(pady=(18,4))
        form = tk.Frame(self, bg=T["WHITE"], highlightbackground=T["BORDER"],
                        highlightthickness=1, padx=22, pady=14)
        form.pack(fill="x", padx=28, pady=(0,10))
        r = tk.Frame(form, bg=T["WHITE"]); r.pack(fill="x")
        tk.Label(r,text="Category:",font=FNT,bg=T["WHITE"],fg=T["TEXT"]).pack(side="left")
        self.bcat_var = tk.StringVar(value=CATEGORIES[0])
        ttk.Combobox(r,textvariable=self.bcat_var,values=CATEGORIES,
                     font=FNT,width=22,state="readonly").pack(side="left",padx=8)
        tk.Label(r,text="Monthly Limit (try not to laugh): $",font=FNT,
                 bg=T["WHITE"],fg=T["TEXT"]).pack(side="left",padx=(14,0))
        self.blimit_var = tk.StringVar()
        tk.Entry(r,textvariable=self.blimit_var,font=FNT,width=10,bg=T["BG"],
                 fg=T["TEXT"],relief="flat",highlightbackground=T["BORDER"],
                 highlightthickness=1).pack(side="left",padx=4)
        btn(form,"Lock It In 🔒",self._set).pack(pady=(10,0))
        self.body = tk.Frame(self, bg=T["BG"])
        self.body.pack(fill="both", expand=True, padx=28, pady=8)

    def retheme(self):
        self.configure(bg=T["BG"])
        for w in self.winfo_children(): w.destroy()
        self._build(); self.refresh()

    def _set(self):
        try: limit = float(self.blimit_var.get())
        except ValueError:
            messagebox.showerror("Girl...","That's not a number, babe 😭"); return
        self.app.data["budgets"][self.bcat_var.get()] = limit
        save_data(self.app.data); self.blimit_var.set(""); self.refresh()

    def refresh(self):
        for w in self.body.winfo_children(): w.destroy()
        self.body.configure(bg=T["BG"])
        budgets = self.app.data.get("budgets",{})
        if not budgets:
            tk.Label(self.body,text="No budgets set... which honestly explains a lot 👀",
                     font=FNT,bg=T["BG"],fg=T["SUBTEXT"]).pack(pady=20); return

        # ── Month/year picker ─────────────────────────────────────
        ctrl = tk.Frame(self.body, bg=T["BG"]); ctrl.pack(fill="x", pady=(0,10))
        tk.Label(ctrl, text="Viewing:", font=FNT, bg=T["BG"], fg=T["TEXT"]).pack(side="left")
        now = datetime.now()
        if not hasattr(self, "_bmonth_var"):
            self._bmonth_var = tk.StringVar(value=MONTHS[now.month-1])
            self._byear_var  = tk.IntVar(value=now.year)
        ttk.Combobox(ctrl, textvariable=self._bmonth_var, values=MONTHS,
                     width=11, state="readonly", font=FNT).pack(side="left", padx=6)
        ttk.Combobox(ctrl, textvariable=self._byear_var,
                     values=list(range(2020, now.year+2)),
                     width=7, state="readonly", font=FNT).pack(side="left", padx=4)
        btn(ctrl, "Go 🔍", self.refresh, color=T["PANEL"], fg=T["TEXT"]).pack(side="left", padx=8)

        month = MONTHS.index(self._bmonth_var.get()) + 1
        year  = self._byear_var.get()
        is_current = (month == now.month and year == now.year)

        mt = [t for t in self.app.data["transactions"]
              if datetime.fromisoformat(t["date"]).month==month and
              datetime.fromisoformat(t["date"]).year==year and t["type"]=="expense"]

        # ── Budget history: show past months as a summary row ─────
        # Collect all months that have transaction data
        all_months = sorted({
            (datetime.fromisoformat(t["date"]).year, datetime.fromisoformat(t["date"]).month)
            for t in self.app.data["transactions"] if t["type"]=="expense"
        }, reverse=True)

        if len(all_months) > 1:
            hist_frame = tk.Frame(self.body, bg=T["WHITE"], highlightbackground=T["BORDER"],
                                  highlightthickness=1, padx=14, pady=10)
            hist_frame.pack(fill="x", pady=(0,10))
            tk.Label(hist_frame, text="📅 Budget History", font=FNT_B,
                     bg=T["WHITE"], fg=T["TEXT"]).pack(anchor="w", pady=(0,6))
            scroll_f = tk.Frame(hist_frame, bg=T["WHITE"])
            scroll_f.pack(fill="x")
            for ym in all_months[:12]:  # show last 12 months
                y, m = ym
                mmt = [t for t in self.app.data["transactions"]
                       if datetime.fromisoformat(t["date"]).month==m and
                       datetime.fromisoformat(t["date"]).year==y and t["type"]=="expense"]
                passed = sum(1 for cat,lim in budgets.items()
                             if sum(t["amount"] for t in mmt if t["category"]==cat) <= lim)
                total  = len(budgets)
                all_pass = passed == total
                is_sel = (m == month and y == year)
                bg_c = T["ACCENT"] if is_sel else (T["GREEN"] if all_pass else T["RED"])
                mon_str = MONTHS[m-1][:3] + " " + str(y)[2:]
                status_str = "OK" if all_pass else (str(passed)+"/"+str(total))
                lbl = mon_str + "\n" + status_str
                tk.Button(scroll_f,
                          text=lbl,
                          font=FNT_S, bg=bg_c, fg=T["TEXT"], bd=0, padx=8, pady=6,
                          cursor="hand2", relief="flat",
                          command=lambda mo=m,yo=y: self._jump_to(mo,yo)
                          ).pack(side="left", padx=3, pady=2)

        # ── Current month detail ──────────────────────────────────
        month_label = f"{MONTHS[month-1]} {year}"
        tk.Label(self.body, text=f"{'📍 This Month' if is_current else f'📆 {month_label}'}",
                 font=FNT_B, bg=T["BG"], fg=T["TEXT"]).pack(anchor="w", pady=(4,4))

        for cat,limit in budgets.items():
            spent = sum(t["amount"] for t in mt if t["category"]==cat)
            pct   = min(spent/limit,1.0) if limit>0 else 0
            passed = spent <= limit
            bar_c = "#E07A7A" if pct>0.85 else "#F5C242" if pct>0.6 else "#7DC99A"
            c = tk.Frame(self.body,bg=T["WHITE"],highlightbackground=T["BORDER"],
                         highlightthickness=1,padx=16,pady=10)
            c.pack(fill="x",pady=4)
            top = tk.Frame(c,bg=T["WHITE"]); top.pack(fill="x")
            status = "✅ Under budget!" if passed else "❌ Over budget 💀"
            status_col = "#7DC99A" if passed else "#E07A7A"
            tk.Label(top,text=cat,font=FNT_B,bg=T["WHITE"],fg=T["TEXT"]).pack(side="left")
            tk.Label(top,text=status,font=FNT_S,bg=T["WHITE"],fg=status_col).pack(side="left",padx=10)
            tk.Label(top,text=f"${spent:.2f} / ${limit:.2f}",font=FNT,
                     bg=T["WHITE"],fg=T["SUBTEXT"]).pack(side="right")
            bar_bg = tk.Frame(c,bg=T["BORDER"],height=14)
            bar_bg.pack(fill="x",pady=(6,2))
            bar_bg.update_idletasks()
            tk.Frame(bar_bg,bg=bar_c,height=14,width=max(int(bar_bg.winfo_width()*pct),4)
                     ).place(x=0,y=0)
            if is_current:
                tk.Button(c,text="✕ Abandon Ship",font=FNT_S,bg=T["WHITE"],fg=T["SUBTEXT"],
                          bd=0,cursor="hand2",command=lambda k=cat:self._rm(k)).pack(anchor="e")

    def _jump_to(self, month, year):
        self._bmonth_var.set(MONTHS[month-1])
        self._byear_var.set(year)
        self.refresh()

    def _rm(self,cat):
        del self.app.data["budgets"][cat]; save_data(self.app.data); self.refresh()


# ══════════════════════════════════════════════════════════════════
class SavingsFrame(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=T["BG"])
        self.app = app; self._build()

    def _build(self):
        tk.Label(self,text="🌟 Future Rich Girl Plans",font=FNT_TITLE,
                 bg=T["BG"],fg=T["TEXT"]).pack(pady=(18,4))
        form = tk.Frame(self,bg=T["WHITE"],highlightbackground=T["BORDER"],
                        highlightthickness=1,padx=22,pady=14)
        form.pack(fill="x",padx=28,pady=(0,10))
        r1=tk.Frame(form,bg=T["WHITE"]); r1.pack(fill="x",pady=3)
        tk.Label(r1,text="What are we saving for queen?:",font=FNT,
                 bg=T["WHITE"],fg=T["TEXT"]).pack(side="left")
        self.gname=tk.StringVar()
        tk.Entry(r1,textvariable=self.gname,font=FNT,width=20,bg=T["BG"],fg=T["TEXT"],
                 relief="flat",highlightbackground=T["BORDER"],highlightthickness=1
                 ).pack(side="left",padx=6)
        tk.Label(r1,text="How much it'll cost us: $",font=FNT,
                 bg=T["WHITE"],fg=T["TEXT"]).pack(side="left",padx=(10,0))
        self.gtarget=tk.StringVar()
        tk.Entry(r1,textvariable=self.gtarget,font=FNT,width=10,bg=T["BG"],fg=T["TEXT"],
                 relief="flat",highlightbackground=T["BORDER"],highlightthickness=1
                 ).pack(side="left",padx=4)
        r2=tk.Frame(form,bg=T["WHITE"]); r2.pack(fill="x",pady=3)
        tk.Label(r2,text="What we've managed so far: $",font=FNT,
                 bg=T["WHITE"],fg=T["TEXT"]).pack(side="left")
        self.gsaved=tk.StringVar(value="0")
        tk.Entry(r2,textvariable=self.gsaved,font=FNT,width=10,bg=T["BG"],fg=T["TEXT"],
                 relief="flat",highlightbackground=T["BORDER"],highlightthickness=1
                 ).pack(side="left",padx=6)
        tk.Label(r2,text="Emoji:",font=FNT,bg=T["WHITE"],fg=T["TEXT"]).pack(side="left",padx=(14,0))
        self.gemoji=tk.StringVar(value="🎯")
        ttk.Combobox(r2,textvariable=self.gemoji,
                     values=["🎯","✈️","🏠","🚗","💍","👗","💻","📱","🌴","🐾"],
                     font=FNT,width=6,state="readonly").pack(side="left",padx=4)
        btn(form,"＋ Manifest It 💅",self._add).pack(pady=(10,0))
        self.goals_body=tk.Frame(self,bg=T["BG"])
        self.goals_body.pack(fill="both",expand=True,padx=28,pady=8)

    def retheme(self):
        self.configure(bg=T["BG"])
        for w in self.winfo_children(): w.destroy()
        self._build(); self.refresh()

    def _add(self):
        name=self.gname.get().strip()
        if not name:
            messagebox.showerror("Girl...","Your goal needs a name, queen! 👑"); return
        try: target=float(self.gtarget.get()); saved=float(self.gsaved.get())
        except: messagebox.showerror("Girl...","Those aren't numbers, bestie 😭"); return
        self.app.data["savings_goals"].append(
            {"name":name,"target":target,"saved":saved,"emoji":self.gemoji.get()})
        save_data(self.app.data)
        self.gname.set(""); self.gtarget.set(""); self.gsaved.set("0"); self.refresh()

    def refresh(self):
        for w in self.goals_body.winfo_children(): w.destroy()
        self.goals_body.configure(bg=T["BG"])
        goals=self.app.data.get("savings_goals",[])
        if not goals:
            tk.Label(self.goals_body,text="No goals yet?? Girl, DREAM BIGGER. Add one above 💅",
                     font=FNT,bg=T["BG"],fg=T["SUBTEXT"]).pack(pady=20); return
        for i,g in enumerate(goals):
            pct=min(g["saved"]/g["target"],1.0) if g["target"]>0 else 0
            c=tk.Frame(self.goals_body,bg=T["WHITE"],highlightbackground=T["BORDER"],
                       highlightthickness=1,padx=18,pady=12)
            c.pack(fill="x",pady=5)
            top=tk.Frame(c,bg=T["WHITE"]); top.pack(fill="x")
            tk.Label(top,text=f"{g['emoji']} {g['name']}",font=FNT_B,
                     bg=T["WHITE"],fg=T["TEXT"]).pack(side="left")
            done = "DONE! Treat yourself (responsibly) 🎉" if pct>=1 else f"{pct*100:.0f}% there 💪"
            tk.Label(top,text=done,font=FNT,bg=T["WHITE"],fg=T["SUBTEXT"]).pack(side="right")
            bar=tk.Frame(c,bg=T["BORDER"],height=18); bar.pack(fill="x",pady=(6,4))
            bar.update_idletasks()
            tk.Frame(bar,bg=T["GOLD"],height=18,width=max(int(bar.winfo_width()*pct),4)
                     ).place(x=0,y=0)
            tk.Label(c,text=f"${g['saved']:,.2f} saved of ${g['target']:,.2f} — you got this 💖",
                     font=FNT_S,bg=T["WHITE"],fg=T["SUBTEXT"]).pack(anchor="w")
            br=tk.Frame(c,bg=T["WHITE"]); br.pack(anchor="e")
            tk.Button(br,text="＋ I Saved Money! 🎉",command=lambda idx=i:self._add_to(idx),
                      font=FNT_S,bg=T["ACCENT2"],fg=T["TEXT"],bd=0,padx=10,pady=5,
                      cursor="hand2",relief="flat").pack(side="left",padx=4)
            tk.Button(br,text="✕",font=FNT_S,bg=T["WHITE"],fg=T["SUBTEXT"],bd=0,
                      cursor="hand2",command=lambda idx=i:self._rm(idx)).pack(side="left")

    def _add_to(self,idx):
        val=tk.simpledialog.askfloat("Proud of You! 🎉",
                                     "How much did you NOT spend?? Proud of you 💰",
                                     parent=self,minvalue=0)
        if val:
            self.app.data["savings_goals"][idx]["saved"]+=val
            save_data(self.app.data); self.refresh()

    def _rm(self,idx):
        self.app.data["savings_goals"].pop(idx); save_data(self.app.data); self.refresh()


# ══════════════════════════════════════════════════════════════════
class IncomeFrame(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=T["BG"])
        self.app = app
        self._build()

    def _build(self):
        tk.Label(self, text="💰 Income Flow", font=FNT_TITLE,
                 bg=T["BG"], fg=T["TEXT"]).pack(pady=(18,4))
        tk.Label(self, text="Let's talk about the money coming IN, queen 👑",
                 font=FNT, bg=T["BG"], fg=T["SUBTEXT"]).pack(pady=(0,10))

        form = tk.Frame(self, bg=T["WHITE"], highlightbackground=T["BORDER"],
                        highlightthickness=1, padx=22, pady=14)
        form.pack(fill="x", padx=28, pady=(0,10))
        tk.Label(form, text="Log Some Income (love that for you) 💸",
                 font=FNT_B, bg=T["WHITE"], fg=T["TEXT"]).pack(anchor="w", pady=(0,8))

        r1 = tk.Frame(form, bg=T["WHITE"]); r1.pack(fill="x", pady=3)
        tk.Label(r1, text="Source:", font=FNT, bg=T["WHITE"], fg=T["TEXT"],
                 width=10, anchor="w").pack(side="left")
        self.src_var = tk.StringVar(value="💼 Income")
        income_cats = ["💼 Income","💻 Freelance","🎁 Gift / Transfer",
                       "📈 Investment","🏦 Refund","💡 Side Hustle","📦 Other Income"]
        ttk.Combobox(r1, textvariable=self.src_var, values=income_cats,
                     font=FNT, width=22, state="readonly").pack(side="left", padx=6)
        tk.Label(r1, text="Amount: $", font=FNT, bg=T["WHITE"],
                 fg=T["TEXT"]).pack(side="left", padx=(14,0))
        self.inc_amt = tk.StringVar()
        tk.Entry(r1, textvariable=self.inc_amt, font=FNT, width=10, bg=T["BG"],
                 fg=T["TEXT"], relief="flat", highlightbackground=T["BORDER"],
                 highlightthickness=1).pack(side="left", padx=4)

        r2 = tk.Frame(form, bg=T["WHITE"]); r2.pack(fill="x", pady=3)
        tk.Label(r2, text="Date:", font=FNT, bg=T["WHITE"], fg=T["TEXT"],
                 width=10, anchor="w").pack(side="left")
        self.inc_date = tk.StringVar(value=datetime.now().strftime("%Y-%m-%d"))
        tk.Entry(r2, textvariable=self.inc_date, font=FNT, width=13, bg=T["BG"],
                 fg=T["TEXT"], relief="flat", highlightbackground=T["BORDER"],
                 highlightthickness=1).pack(side="left", padx=6)
        tk.Label(r2, text="Note:", font=FNT, bg=T["WHITE"],
                 fg=T["TEXT"]).pack(side="left", padx=(14,0))
        self.inc_note = tk.StringVar()
        tk.Entry(r2, textvariable=self.inc_note, font=FNT, width=28, bg=T["BG"],
                 fg=T["TEXT"], relief="flat", highlightbackground=T["BORDER"],
                 highlightthickness=1).pack(side="left", padx=6)

        btn(form, "💰 Log That Bag", self._add).pack(pady=(10,0))

        self.stats_row = tk.Frame(self, bg=T["BG"])
        self.stats_row.pack(fill="x", padx=28, pady=(4,6))

        tk.Label(self, text="📊 Income by Source (this month)",
                 font=FNT_B, bg=T["BG"], fg=T["TEXT"]).pack(anchor="w", padx=28, pady=(4,2))
        self.src_row = tk.Frame(self, bg=T["BG"])
        self.src_row.pack(fill="x", padx=28, pady=(0,6))

        tk.Label(self, text="💸 Income History (slay!)",
                 font=FNT_B, bg=T["BG"], fg=T["TEXT"]).pack(anchor="w", padx=28, pady=(4,2))
        wrap = tk.Frame(self, bg=T["BG"])
        wrap.pack(fill="both", expand=True, padx=28, pady=(0,8))
        cols = ("Date","Source","Note","Amount")
        self.tree = ttk.Treeview(wrap, columns=cols, show="headings", style="A.Treeview")
        for col, w in zip(cols, [110,180,260,110]):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=w, anchor="center")
        sb2 = ttk.Scrollbar(wrap, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=sb2.set)
        self.tree.pack(side="left", fill="both", expand=True)
        sb2.pack(side="right", fill="y")

    def _add(self):
        try: amt = float(self.inc_amt.get())
        except ValueError:
            messagebox.showerror("Girl...", "That is not a number bestie 💀"); return
        self.app.data["transactions"].append({
            "date": self.inc_date.get() + "T00:00:00",
            "type": "income",
            "category": self.src_var.get(),
            "note": self.inc_note.get(),
            "amount": amt
        })
        save_data(self.app.data)
        self.inc_amt.set(""); self.inc_note.set("")
        self.refresh()

    def retheme(self):
        self.configure(bg=T["BG"])
        for w in self.winfo_children(): w.destroy()
        self._build(); self.refresh()

    def refresh(self):
        for w in self.stats_row.winfo_children(): w.destroy()
        for w in self.src_row.winfo_children(): w.destroy()

        txns = self.app.data["transactions"]
        income_all = [t for t in txns if t["type"] == "income"]
        now = datetime.now()

        def month_income(m, y):
            return sum(t["amount"] for t in income_all
                       if datetime.fromisoformat(t["date"]).month == m
                       and datetime.fromisoformat(t["date"]).year == y)

        this_total = month_income(now.month, now.year)
        pm = now.month - 1 if now.month > 1 else 12
        py = now.year if now.month > 1 else now.year - 1
        last_total = month_income(pm, py)
        all_total  = sum(t["amount"] for t in income_all)
        diff       = this_total - last_total
        diff_txt   = (f"up ${diff:,.2f} vs last month!" if diff >= 0
                      else f"down ${abs(diff):,.2f} vs last month")
        diff_col   = "#7DC99A" if diff >= 0 else "#E07A7A"

        this_month_inc = [t for t in income_all
                          if datetime.fromisoformat(t["date"]).month == now.month
                          and datetime.fromisoformat(t["date"]).year == now.year]
        by_src = {}
        for t in this_month_inc:
            by_src[t["category"]] = by_src.get(t["category"], 0) + t["amount"]
        top_src = max(by_src, key=by_src.get) if by_src else "Nothing yet"

        for title, val, color, sub, sub_col in [
                ("This Month 💰",  this_total, "#7DC99A",  diff_txt,  diff_col),
                ("Last Month",     last_total, T["SUBTEXT"],"keep stacking!", T["SUBTEXT"]),
                ("All Time 👑",    all_total,  T["ACCENT"], f"Top: {top_src}", T["SUBTEXT"])]:
            c = tk.Frame(self.stats_row, bg=T["WHITE"], highlightbackground=T["BORDER"],
                         highlightthickness=1, padx=16, pady=12)
            c.pack(side="left", expand=True, fill="both", padx=6)
            tk.Label(c, text=title, font=FNT, bg=T["WHITE"], fg=T["SUBTEXT"]).pack()
            tk.Label(c, text=f"${val:,.2f}", font=FNT_BIG, bg=T["WHITE"], fg=color).pack()
            tk.Label(c, text=sub, font=FNT_S, bg=T["WHITE"], fg=sub_col).pack()

        if by_src:
            max_val = max(by_src.values())
            for src, amt in sorted(by_src.items(), key=lambda x: x[1], reverse=True):
                pct = amt / max_val if max_val > 0 else 0
                row = tk.Frame(self.src_row, bg=T["BG"])
                row.pack(fill="x", pady=2)
                tk.Label(row, text=src, font=FNT_S, bg=T["BG"], fg=T["TEXT"],
                         width=22, anchor="w").pack(side="left")
                bar_bg = tk.Frame(row, bg=T["BORDER"], height=16)
                bar_bg.pack(side="left", fill="x", expand=True, padx=(6,8))
                bar_bg.update_idletasks()
                fill_w = max(int(bar_bg.winfo_width() * pct), 4)
                tk.Frame(bar_bg, bg="#7DC99A", height=16, width=fill_w).place(x=0, y=0)
                tk.Label(row, text=f"${amt:,.2f}", font=FNT_S, bg=T["BG"],
                         fg=T["TEXT"], width=10, anchor="e").pack(side="left")
        else:
            tk.Label(self.src_row,
                     text="No income this month yet... the bag is incoming though 💅",
                     font=FNT, bg=T["BG"], fg=T["SUBTEXT"]).pack(anchor="w")

        for row in self.tree.get_children(): self.tree.delete(row)
        if not income_all:
            self.tree.insert("","end", values=("—","No income logged yet","Add some above!","—"))
            return
        for t in sorted(income_all, key=lambda t: t["date"], reverse=True):
            self.tree.insert("","end",
                values=(t["date"][:10], t["category"],
                        t.get("note",""), f"+${t['amount']:,.2f}"))


# ══════════════════════════════════════════════════════════════════
class SummaryFrame(tk.Frame):
    CAT_COLORS = [
        "#FF6B9D","#45B7D1","#FFA500","#96CEB4","#DDA0DD",
        "#F7DC6F","#E74C3C","#3498DB","#2ECC71","#E67E22",
        "#9B59B6","#1ABC9C","#E91E63","#00BCD4",
    ]

    def __init__(self, parent, app):
        super().__init__(parent, bg=T["BG"])
        self.app = app; self._build()

    def _build(self):
        tk.Label(self, text="📊 The Hard Truth", font=FNT_TITLE,
                 bg=T["BG"], fg=T["TEXT"]).pack(pady=(18,4))
        now = datetime.now()
        years = list(range(2020, now.year+2))

        # ── Mode toggle ───────────────────────────────────────────
        mode_f = tk.Frame(self, bg=T["BG"]); mode_f.pack()
        self.range_mode = tk.StringVar(value="single")
        for txt, val in [("Single Month","single"),("Full Year","year"),("Date Range","range")]:
            tk.Radiobutton(mode_f, text=txt, variable=self.range_mode, value=val,
                           font=FNT, bg=T["BG"], fg=T["TEXT"], selectcolor=T["ACCENT2"],
                           activebackground=T["BG"], command=self._toggle_mode
                           ).pack(side="left", padx=10)

        # ── Single month ──────────────────────────────────────────
        self.single_f = tk.Frame(self, bg=T["BG"]); self.single_f.pack(pady=(4,0))
        self.month_var = tk.StringVar(value=MONTHS[now.month-1])
        self.year_var  = tk.IntVar(value=now.year)
        tk.Label(self.single_f, text="Month:", font=FNT, bg=T["BG"], fg=T["TEXT"]).pack(side="left")
        ttk.Combobox(self.single_f, textvariable=self.month_var, values=MONTHS,
                     width=10, state="readonly").pack(side="left", padx=4)
        tk.Label(self.single_f, text="Year:", font=FNT, bg=T["BG"], fg=T["TEXT"]).pack(side="left", padx=(10,0))
        ttk.Combobox(self.single_f, textvariable=self.year_var,
                     values=years, width=7, state="readonly").pack(side="left", padx=4)

        # ── Full year ─────────────────────────────────────────────
        self.year_f = tk.Frame(self, bg=T["BG"])
        self.year_only_var = tk.IntVar(value=now.year)
        tk.Label(self.year_f, text="Year:", font=FNT, bg=T["BG"], fg=T["TEXT"]).pack(side="left")
        ttk.Combobox(self.year_f, textvariable=self.year_only_var,
                     values=years, width=7, state="readonly").pack(side="left", padx=4)

        # ── Date range ────────────────────────────────────────────
        self.range_f = tk.Frame(self, bg=T["BG"])
        tk.Label(self.range_f, text="From:", font=FNT, bg=T["BG"], fg=T["TEXT"]).pack(side="left")
        self.from_month = tk.StringVar(value=MONTHS[0])
        self.from_year  = tk.IntVar(value=now.year)
        ttk.Combobox(self.range_f, textvariable=self.from_month, values=MONTHS,
                     width=10, state="readonly").pack(side="left", padx=4)
        ttk.Combobox(self.range_f, textvariable=self.from_year,
                     values=years, width=7, state="readonly").pack(side="left", padx=2)
        tk.Label(self.range_f, text="  To:", font=FNT, bg=T["BG"], fg=T["TEXT"]).pack(side="left")
        self.to_month = tk.StringVar(value=MONTHS[now.month-1])
        self.to_year  = tk.IntVar(value=now.year)
        ttk.Combobox(self.range_f, textvariable=self.to_month, values=MONTHS,
                     width=10, state="readonly").pack(side="left", padx=4)
        ttk.Combobox(self.range_f, textvariable=self.to_year,
                     values=years, width=7, state="readonly").pack(side="left", padx=2)

        ctrl2 = tk.Frame(self, bg=T["BG"]); ctrl2.pack(pady=4)
        btn(ctrl2, "🔍 Show Me the Damage", self.refresh).pack()
        self.chart_area = tk.Frame(self, bg=T["BG"])
        self.chart_area.pack(fill="both", expand=True, padx=20, pady=8)

    def _toggle_mode(self):
        self.single_f.pack_forget()
        self.year_f.pack_forget()
        self.range_f.pack_forget()
        m = self.range_mode.get()
        if m == "single":   self.single_f.pack(pady=(4,0))
        elif m == "year":   self.year_f.pack(pady=(4,0))
        else:               self.range_f.pack(pady=(4,0))

    def retheme(self):
        self.configure(bg=T["BG"])
        for w in self.winfo_children(): w.destroy()
        self._build(); self.refresh()

    def _get_filtered(self):
        """Return (transactions, range_label, x_mode) based on current mode.
        x_mode: 'day' | 'month'
        """
        txns = self.app.data["transactions"]
        mode = self.range_mode.get()
        if mode == "single":
            month = MONTHS.index(self.month_var.get()) + 1
            year  = self.year_var.get()
            mt = [t for t in txns
                  if datetime.fromisoformat(t["date"]).month == month
                  and datetime.fromisoformat(t["date"]).year == year]
            self._current_month = month
            self._current_year  = year
            return mt, f"{self.month_var.get()} {year}", "day"
        elif mode == "year":
            year = self.year_only_var.get()
            mt = [t for t in txns if datetime.fromisoformat(t["date"]).year == year]
            self._current_month = None
            self._current_year  = year
            return mt, str(year), "month"
        else:
            fm = MONTHS.index(self.from_month.get()) + 1
            fy = int(self.from_year.get())
            tm = MONTHS.index(self.to_month.get()) + 1
            ty = int(self.to_year.get())
            from_dt = datetime(fy, fm, 1)
            to_dt   = datetime(ty, tm, 1)
            if from_dt > to_dt: from_dt, to_dt = to_dt, from_dt
            mt = [t for t in txns
                  if from_dt <= datetime.fromisoformat(t["date"]).replace(day=1) <= to_dt]
            self._current_month = None
            self._current_year  = None
            return mt, f"{self.from_month.get()} {fy} – {self.to_month.get()} {ty}", "month"

    def refresh(self):
        for w in self.chart_area.winfo_children(): w.destroy()
        self.chart_area.configure(bg=T["BG"])

        mt, range_label, x_mode = self._get_filtered()
        income  = sum(t["amount"] for t in mt if t["type"] == "income")
        expense = sum(t["amount"] for t in mt if t["type"] == "expense")

        # ── Summary cards ─────────────────────────────────────────
        row = tk.Frame(self.chart_area, bg=T["BG"]); row.pack(fill="x", pady=(0,10))
        tk.Label(row, text=range_label, font=FNT_B, bg=T["BG"], fg=T["SUBTEXT"]).pack(side="left", padx=6)
        for title, val, col in [("Money In 🙏", income, "#7DC99A"),
                                 ("Money Gone 💀", expense, "#E07A7A"),
                                 ("What's Left 😬", income-expense, T["ACCENT"])]:
            c = tk.Frame(row, bg=T["WHITE"], highlightbackground=T["BORDER"],
                         highlightthickness=1, padx=16, pady=10)
            c.pack(side="left", expand=True, fill="both", padx=6)
            tk.Label(c, text=title, font=FNT, bg=T["WHITE"], fg=T["SUBTEXT"]).pack()
            tk.Label(c, text=f"${val:,.2f}", font=FNT_BIG, bg=T["WHITE"], fg=col).pack()

        # ── Expense by category ───────────────────────────────────
        exp_by_cat = {}
        for t in mt:
            if t["type"] == "expense":
                exp_by_cat[t["category"]] = exp_by_cat.get(t["category"], 0) + t["amount"]

        # ── Build line plot data ──────────────────────────────────
        # x_mode "day" → x = day-of-month, x_mode "month" → x = (year,month) bucket
        if x_mode == "day":
            bucket_e = {}; bucket_i = {}
            for t in mt:
                d = datetime.fromisoformat(t["date"]).day
                if t["type"] == "expense": bucket_e[d] = bucket_e.get(d,0) + t["amount"]
                else:                      bucket_i[d] = bucket_i.get(d,0) + t["amount"]
            all_keys = sorted(set(list(bucket_e) + list(bucket_i)))
            x_labels = [str(k) for k in all_keys]
            e_vals   = [bucket_e.get(k,0) for k in all_keys]
            i_vals   = [bucket_i.get(k,0) for k in all_keys]
            line_title = "Daily Spending"
        else:
            bucket_e = {}; bucket_i = {}
            for t in mt:
                dt = datetime.fromisoformat(t["date"])
                key = (dt.year, dt.month)
                if t["type"] == "expense": bucket_e[key] = bucket_e.get(key,0) + t["amount"]
                else:                      bucket_i[key] = bucket_i.get(key,0) + t["amount"]
            all_keys = sorted(set(list(bucket_e) + list(bucket_i)))
            x_labels = [f"{MONTHS[k[1]-1][:3]}'{str(k[0])[2:]}" for k in all_keys]
            e_vals   = [bucket_e.get(k,0) for k in all_keys]
            i_vals   = [bucket_i.get(k,0) for k in all_keys]
            line_title = "Monthly Spending"

        # ── Figure ────────────────────────────────────────────────
        fig = Figure(figsize=(9, 3.4), facecolor=T["BG"])
        ax1 = fig.add_subplot(121)

        # PIE CHART
        labels = list(exp_by_cat.keys())
        vals   = list(exp_by_cat.values())
        if exp_by_cat:
            clean_labels = [strip_emoji(l) for l in labels]
            cat_colors = [self.CAT_COLORS[CATEGORIES.index(l) % len(self.CAT_COLORS)]
                          if l in CATEGORIES else self.CAT_COLORS[0] for l in labels]
            ax1.pie(vals, labels=None, colors=cat_colors, autopct="%1.0f%%",
                    startangle=140, wedgeprops={"edgecolor":"white","linewidth":2},
                    textprops={"fontsize":8,"color":T["TEXT"]})
            ax1.legend(clean_labels, loc="lower center", bbox_to_anchor=(0.5,-0.35),
                       fontsize=7, ncol=2, frameon=False, labelcolor=T["TEXT"])
            ax1.set_title("Crimes by Category", color=T["TEXT"], fontsize=11, pad=10)
            ax1.set_facecolor(T["BG"])
        else:
            ax1.text(0.5, 0.5, "No expenses yet!", ha="center", va="center",
                     color=T["SUBTEXT"], fontsize=10)
            ax1.axis("off")

        # LINE PLOT
        ax2 = fig.add_subplot(122)
        if all_keys:
            xs = list(range(len(all_keys)))
            if any(v > 0 for v in e_vals):
                ax2.plot(xs, e_vals, color=T["ACCENT2"], marker="o", markersize=4,
                         linewidth=2, label="Expenses")
                ax2.fill_between(xs, e_vals, alpha=0.12, color=T["ACCENT2"])
            if any(v > 0 for v in i_vals):
                ax2.plot(xs, i_vals, color="#7DC99A", marker="o", markersize=4,
                         linewidth=2, label="Income")
                ax2.fill_between(xs, i_vals, alpha=0.10, color="#7DC99A")
            ax2.set_xticks(xs)
            tick_labels = x_labels if len(x_labels) <= 20 else                           [x_labels[i] if i % max(1, len(x_labels)//12) == 0 else "" for i in range(len(x_labels))]
            ax2.set_xticklabels(tick_labels, fontsize=7, color=T["TEXT"], rotation=45 if len(x_labels)>10 else 0)
            ax2.set_facecolor(T["BG"])
            ax2.tick_params(axis="y", labelcolor=T["TEXT"], labelsize=7)
            ax2.spines[:].set_edgecolor(T["BORDER"])
            ax2.legend(fontsize=7, frameon=False, labelcolor=T["TEXT"])
            ax2.set_title(line_title, color=T["TEXT"], fontsize=11)
            ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda v,_: f"${v:,.0f}"))
        else:
            ax2.text(0.5, 0.5, "Nothing here yet...", ha="center", va="center",
                     color=T["SUBTEXT"], fontsize=10)
            ax2.axis("off")

        fig.tight_layout(pad=2)
        canvas = FigureCanvasTkAgg(fig, self.chart_area)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

        # ── Hover tooltip ─────────────────────────────────────────
        tooltip = tk.Label(self.chart_area, text="", font=FNT_S,
                           bg="#2D2D2D", fg="white", padx=8, pady=4, relief="flat", bd=0)

        # Build key→transactions lookup for line hover
        key_txns = {}
        for t in mt:
            dt = datetime.fromisoformat(t["date"])
            k = dt.day if x_mode == "day" else (dt.year, dt.month)
            key_txns.setdefault(k, []).append(t)

        pie_wedges = [c for c in ax1.get_children() if c.__class__.__name__ == "Wedge"]

        def on_hover(event):
            tooltip.place_forget()
            if event.inaxes is None: return
            # Pie hover
            if event.inaxes == ax1 and exp_by_cat:
                for i, wedge in enumerate(pie_wedges):
                    if wedge.contains_point([event.x, event.y]):
                        total = sum(vals)
                        pct = vals[i]/total*100 if total else 0
                        tooltip.configure(text=f"{labels[i]}\n${vals[i]:,.2f}  ({pct:.1f}%)")
                        tooltip.place(x=int(event.x)+12,
                                      y=int(canvas.get_tk_widget().winfo_height()-event.y)+12)
                        return
            # Line plot hover — find nearest point by x
            if event.inaxes == ax2 and all_keys and event.xdata is not None:
                xi = int(round(event.xdata))
                if 0 <= xi < len(all_keys):
                    k = all_keys[xi]
                    txns_pt = key_txns.get(k, [])
                    if not txns_pt: return
                    hdr = f"── {x_labels[xi]} ──"
                    lines = [hdr]
                    for t in sorted(txns_pt, key=lambda t: t["amount"], reverse=True)[:8]:
                        sign = "+" if t["type"] == "income" else "-"
                        note = t.get("note","") or strip_emoji(t["category"])
                        note = note[:22]+"…" if len(note)>22 else note
                        lines.append(f"{sign}${t['amount']:.2f}  {note}")
                    if len(txns_pt) > 8: lines.append(f"…+{len(txns_pt)-8} more")
                    tooltip.configure(text="\n".join(lines))
                    tooltip.place(x=int(event.x)+12,
                                  y=int(canvas.get_tk_widget().winfo_height()-event.y)+12)
                    return
            tooltip.place_forget()

        canvas.mpl_connect("motion_notify_event", on_hover)

        # Pie click → navigate to transactions filtered by category
        def on_click(event):
            if event.inaxes != ax1 or not exp_by_cat: return
            for i, wedge in enumerate(pie_wedges):
                if wedge.contains_point([event.x, event.y]):
                    txn_frame = self.app.frames["transactions"]
                    mode = self.range_mode.get()
                    # Set category filter
                    txn_frame.filter_cat.set(labels[i])
                    # Set month/year to match the chart's date selection
                    if mode == "single":
                        txn_frame.filter_month.set(self.month_var.get())
                        txn_frame.filter_year.set(str(self.year_var.get()))
                    elif mode == "year":
                        txn_frame.filter_month.set("All")
                        txn_frame.filter_year.set(str(self.year_only_var.get()))
                    else:
                        # Date range — can't map cleanly to single month/year, show all time for that category
                        txn_frame.filter_month.set("All")
                        txn_frame.filter_year.set("All")
                    self.app.show_frame("transactions")
                    return
        canvas.mpl_connect("button_press_event", on_click)


# ══════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    import tkinter.simpledialog as sd
    tk.simpledialog = sd
    app = FinanceApp()
    app.mainloop()