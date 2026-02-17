import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json, os, csv
from datetime import datetime
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# ── Palette ──────────────────────────────────────────────────────
BG      = "#FFF0F5"
PANEL   = "#FFE4EF"
ACCENT  = "#FF85A1"
ACCENT2 = "#FFB3C6"
TEXT    = "#7D3C5A"
SUBTEXT = "#C07A9A"
WHITE   = "#FFFFFF"
GREEN   = "#C8F0D0"
RED     = "#FFD6D6"
GOLD    = "#FFE9A0"
BORDER  = "#F7B8D0"

FNT       = ("Helvetica", 11)
FNT_B     = ("Helvetica", 12, "bold")
FNT_TITLE = ("Helvetica", 18, "bold")
FNT_S     = ("Helvetica", 9)
FNT_BIG   = ("Helvetica", 22, "bold")

DATA_FILE = os.path.join(os.path.expanduser("~"), "girl_do_not_buy_that_data.json")

CATEGORIES = ["🛍️ Shopping","🍔 Food & Dining","🏠 Housing","💅 Self-care",
              "🚗 Transport","💊 Health","📚 Education","🎉 Entertainment",
              "✈️ Travel","💡 Utilities","💼 Income","🎁 Gifts","📦 Other"]

APPLE_CATEGORY_MAP = {
    "food and drink": "🍔 Food & Dining",
    "restaurants": "🍔 Food & Dining",
    "groceries": "🍔 Food & Dining",
    "shopping": "🛍️ Shopping",
    "entertainment": "🎉 Entertainment",
    "travel": "✈️ Travel",
    "transportation": "🚗 Transport",
    "health": "💊 Health",
    "utilities": "💡 Utilities",
    "education": "📚 Education",
    "personal care": "💅 Self-care",
    "gifts": "🎁 Gifts",
}

def map_apple_category(raw):
    if not raw:
        return "📦 Other"
    raw_lower = raw.lower()
    for k, v in APPLE_CATEGORY_MAP.items():
        if k in raw_lower:
            return v
    return "📦 Other"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE) as f:
            return json.load(f)
    return {"transactions": [], "savings_goals": [], "budgets": {}}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

def styled_btn(parent, text, cmd, color=None, fg=WHITE, **kw):
    color = color or ACCENT
    return tk.Button(parent, text=text, command=cmd, font=FNT_B,
                     bg=color, fg=fg, bd=0, padx=16, pady=8,
                     cursor="hand2", activebackground=ACCENT2,
                     activeforeground=WHITE, relief="flat", **kw)

def card_frame(parent, **kw):
    return tk.Frame(parent, bg=WHITE, highlightbackground=BORDER,
                    highlightthickness=1, **kw)


# ══════════════════════════════════════════════════════════════════
class FinanceApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("🚨 Girl Do Not Buy That")
        self.geometry("1100x750")
        self.minsize(950, 680)
        self.configure(bg=BG)
        self.data = load_data()
        self._style()
        self._build_ui()
        self.show_frame("dashboard")

    def _style(self):
        s = ttk.Style()
        s.theme_use("clam")
        s.configure("Pink.Treeview", background=WHITE, fieldbackground=WHITE,
                    foreground=TEXT, font=FNT, rowheight=30)
        s.configure("Pink.Treeview.Heading", background=PANEL,
                    foreground=TEXT, font=FNT_B, relief="flat")
        s.map("Pink.Treeview", background=[("selected", ACCENT2)])
        s.configure("TCombobox", fieldbackground=BG, background=BG,
                    foreground=TEXT, arrowcolor=ACCENT)

    def _build_ui(self):
        # Sidebar
        sb = tk.Frame(self, bg=PANEL, width=195)
        sb.pack(side="left", fill="y")
        sb.pack_propagate(False)

        tk.Label(sb, text="💖", font=("Helvetica", 34), bg=PANEL, fg=ACCENT).pack(pady=(22,2))
        tk.Label(sb, text="Girl Do Not Buy That", font=FNT_B, bg=PANEL,
                 fg=TEXT, justify="center").pack()
        tk.Frame(sb, bg=BORDER, height=1).pack(fill="x", padx=18, pady=14)

        self.nav_btns = {}
        for label, key in [("🏠  Dashboard",    "dashboard"),
                            ("💸  Transactions", "transactions"),
                            ("📥  Import CSV",   "import_csv"),
                            ("🗂️  Budgets",      "budgets"),
                            ("🌟  Savings Goals","savings"),
                            ("📊  Summary",      "summary")]:
            b = tk.Button(sb, text=label, font=FNT, bg=PANEL, fg=TEXT,
                          bd=0, anchor="w", padx=20, pady=11, cursor="hand2",
                          activebackground=ACCENT2, relief="flat",
                          command=lambda k=key: self.show_frame(k))
            b.pack(fill="x")
            self.nav_btns[key] = b

        # Content
        self.content = tk.Frame(self, bg=BG)
        self.content.pack(side="left", fill="both", expand=True)

        self.frames = {}
        for name, cls in [("dashboard",    DashboardFrame),
                           ("transactions", TransactionsFrame),
                           ("import_csv",   ImportCSVFrame),
                           ("budgets",      BudgetsFrame),
                           ("savings",      SavingsFrame),
                           ("summary",      SummaryFrame)]:
            f = cls(self.content, self)
            f.place(relx=0, rely=0, relwidth=1, relheight=1)
            self.frames[name] = f

    def show_frame(self, name):
        for k, b in self.nav_btns.items():
            b.configure(bg=ACCENT if k == name else PANEL,
                        fg=WHITE if k == name else TEXT)
        self.frames[name].tkraise()
        if hasattr(self.frames[name], "refresh"):
            self.frames[name].refresh()

    def add_transaction(self, t):
        self.data["transactions"].append(t)
        save_data(self.data)


# ══════════════════════════════════════════════════════════════════
class DashboardFrame(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=BG)
        self.app = app
        hdr = tk.Frame(self, bg=ACCENT, pady=16)
        hdr.pack(fill="x")
        tk.Label(hdr, text="✨ Welcome to Girl Do Not Buy That 🚨 ✨",
                 font=FNT_TITLE, bg=ACCENT, fg=WHITE).pack()
        self.body = tk.Frame(self, bg=BG)
        self.body.pack(fill="both", expand=True, padx=28, pady=18)

    def refresh(self):
        for w in self.body.winfo_children():
            w.destroy()
        data = self.app.data
        txns = data["transactions"]
        now = datetime.now()
        mt = [t for t in txns
              if datetime.fromisoformat(t["date"]).month == now.month
              and datetime.fromisoformat(t["date"]).year == now.year]

        income  = sum(t["amount"] for t in mt if t["type"] == "income")
        expense = sum(t["amount"] for t in mt if t["type"] == "expense")
        balance = income - expense

        # Summary tiles
        row = tk.Frame(self.body, bg=BG)
        row.pack(fill="x", pady=(0,14))
        for title, val, color, icon in [
            ("Balance",  balance, ACCENT,   "💰"),
            ("Income",   income,  "#7DC99A","📈"),
            ("Expenses", expense, "#E07A7A","📉")]:
            c = card_frame(row, padx=18, pady=14)
            c.pack(side="left", expand=True, fill="both", padx=6)
            tk.Label(c, text=icon, font=("Helvetica",26), bg=WHITE).pack()
            tk.Label(c, text=title, font=FNT, bg=WHITE, fg=SUBTEXT).pack()
            tk.Label(c, text=f"${val:,.2f}", font=FNT_BIG, bg=WHITE, fg=color).pack()
            tk.Label(c, text="this month", font=FNT_S, bg=WHITE, fg=SUBTEXT).pack()

        # Recent transactions
        tk.Label(self.body, text="🕐 Recent Transactions", font=FNT_B,
                 bg=BG, fg=TEXT).pack(anchor="w", pady=(8,4))
        c = card_frame(self.body)
        c.pack(fill="x")
        recent = sorted(txns, key=lambda t: t["date"], reverse=True)[:8]
        if not recent:
            tk.Label(c, text="No transactions yet 🌸  Import a CSV or add one!",
                     font=FNT, bg=WHITE, fg=SUBTEXT, pady=14).pack()
        for t in recent:
            bg   = GREEN if t["type"] == "income" else RED
            sign = "+" if t["type"] == "income" else "-"
            r = tk.Frame(c, bg=WHITE)
            r.pack(fill="x", padx=14, pady=3)
            tk.Label(r, text=t["category"], font=FNT, bg=WHITE, fg=TEXT,
                     width=20, anchor="w").pack(side="left")
            tk.Label(r, text=t.get("note",""), font=FNT_S, bg=WHITE, fg=SUBTEXT,
                     width=24, anchor="w").pack(side="left")
            tk.Label(r, text=t["date"][:10], font=FNT_S, bg=WHITE, fg=SUBTEXT,
                     width=11).pack(side="left")
            tk.Label(r, text=f"{sign}${t['amount']:.2f}", font=FNT_B,
                     bg=bg, fg=TEXT, padx=8).pack(side="right", pady=2)

        styled_btn(self.body, "＋ Add Transaction",
                   lambda: self.app.show_frame("transactions")).pack(pady=12)


# ══════════════════════════════════════════════════════════════════
class TransactionsFrame(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=BG)
        self.app = app
        self._build()

    def _build(self):
        tk.Label(self, text="💸 Transactions", font=FNT_TITLE,
                 bg=BG, fg=TEXT).pack(pady=(18,4))

        form = card_frame(self, padx=22, pady=14)
        form.pack(fill="x", padx=28, pady=(0,10))

        # Type row
        r1 = tk.Frame(form, bg=WHITE)
        r1.pack(fill="x", pady=3)
        tk.Label(r1, text="Type:", font=FNT, bg=WHITE, fg=TEXT).pack(side="left")
        self.type_var = tk.StringVar(value="expense")
        for val, lbl in [("expense","💸 Expense"),("income","💰 Income")]:
            tk.Radiobutton(r1, text=lbl, variable=self.type_var, value=val,
                           font=FNT, bg=WHITE, fg=TEXT, selectcolor=ACCENT2,
                           activebackground=WHITE).pack(side="left", padx=10)

        # Category + Amount
        r2 = tk.Frame(form, bg=WHITE)
        r2.pack(fill="x", pady=3)
        tk.Label(r2, text="Category:", font=FNT, bg=WHITE, fg=TEXT,
                 width=10, anchor="w").pack(side="left")
        self.cat_var = tk.StringVar(value=CATEGORIES[0])
        ttk.Combobox(r2, textvariable=self.cat_var, values=CATEGORIES,
                     font=FNT, width=22, state="readonly").pack(side="left", padx=6)
        tk.Label(r2, text="Amount: $", font=FNT, bg=WHITE, fg=TEXT).pack(side="left", padx=(14,0))
        self.amt_var = tk.StringVar()
        tk.Entry(r2, textvariable=self.amt_var, font=FNT, width=10,
                 bg=BG, fg=TEXT, relief="flat",
                 highlightbackground=BORDER, highlightthickness=1).pack(side="left", padx=4)

        # Date + Note
        r3 = tk.Frame(form, bg=WHITE)
        r3.pack(fill="x", pady=3)
        tk.Label(r3, text="Date:", font=FNT, bg=WHITE, fg=TEXT,
                 width=10, anchor="w").pack(side="left")
        self.date_var = tk.StringVar(value=datetime.now().strftime("%Y-%m-%d"))
        tk.Entry(r3, textvariable=self.date_var, font=FNT, width=13,
                 bg=BG, fg=TEXT, relief="flat",
                 highlightbackground=BORDER, highlightthickness=1).pack(side="left", padx=6)
        tk.Label(r3, text="Note:", font=FNT, bg=WHITE, fg=TEXT).pack(side="left", padx=(14,0))
        self.note_var = tk.StringVar()
        tk.Entry(r3, textvariable=self.note_var, font=FNT, width=28,
                 bg=BG, fg=TEXT, relief="flat",
                 highlightbackground=BORDER, highlightthickness=1).pack(side="left", padx=6)

        styled_btn(form, "＋ Add Transaction", self._add).pack(pady=(10,0))

        # Tree
        tk.Label(self, text="All Transactions", font=FNT_B,
                 bg=BG, fg=TEXT).pack(anchor="w", padx=28, pady=(8,2))
        wrap = tk.Frame(self, bg=BG)
        wrap.pack(fill="both", expand=True, padx=28, pady=(0,4))
        cols = ("Date","Type","Category","Merchant / Note","Amount")
        self.tree = ttk.Treeview(wrap, columns=cols, show="headings",
                                 style="Pink.Treeview")
        for col, w in zip(cols,[100,80,150,230,100]):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=w, anchor="center")
        sb2 = ttk.Scrollbar(wrap, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=sb2.set)
        self.tree.pack(side="left", fill="both", expand=True)
        sb2.pack(side="right", fill="y")

        styled_btn(self, "🗑️ Delete Selected", self._delete,
                   color="#E07A7A").pack(pady=8)

    def _add(self):
        try:
            amt = float(self.amt_var.get())
        except ValueError:
            messagebox.showerror("Oops!", "Please enter a valid amount 💕"); return
        t = {"date": self.date_var.get() + "T00:00:00",
             "type": self.type_var.get(),
             "category": self.cat_var.get(),
             "note": self.note_var.get(),
             "amount": amt}
        self.app.add_transaction(t)
        self.amt_var.set("")
        self.note_var.set("")
        self.refresh()

    def _delete(self):
        sel = self.tree.selection()
        if not sel: return
        iid = sel[0]
        idx = self.tree.index(iid)
        txns_sorted = sorted(self.app.data["transactions"],
                             key=lambda t: t["date"], reverse=True)
        self.app.data["transactions"].remove(txns_sorted[idx])
        save_data(self.app.data)
        self.refresh()

    def refresh(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        txns = sorted(self.app.data["transactions"],
                      key=lambda t: t["date"], reverse=True)
        for t in txns:
            sign = "+" if t["type"] == "income" else "-"
            self.tree.insert("", "end",
                values=(t["date"][:10], t["type"].capitalize(),
                        t["category"], t.get("note",""),
                        f"{sign}${t['amount']:.2f}"))


# ══════════════════════════════════════════════════════════════════
class ImportCSVFrame(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=BG)
        self.app = app
        self.preview_data = []
        self._build()

    def _build(self):
        tk.Label(self, text="📥 Import Apple Wallet CSV", font=FNT_TITLE,
                 bg=BG, fg=TEXT).pack(pady=(18,4))

        # Info card
        info = card_frame(self, padx=22, pady=14)
        info.pack(fill="x", padx=28, pady=(0,10))
        tk.Label(info, text="💡 Expected columns (any order, case-insensitive):",
                 font=FNT_B, bg=WHITE, fg=TEXT).pack(anchor="w")
        tk.Label(info,
                 text="  Transaction Date  •  Description  •  Merchant  •  Category  •  Type  •  Amount",
                 font=FNT, bg=WHITE, fg=SUBTEXT).pack(anchor="w")
        tk.Label(info,
                 text="  Amounts can be positive or negative. 'Debit'/'Credit' in Type are auto-detected.",
                 font=FNT_S, bg=WHITE, fg=SUBTEXT).pack(anchor="w", pady=(2,0))

        btn_row = tk.Frame(self, bg=BG)
        btn_row.pack(pady=6)
        styled_btn(btn_row, "📂 Choose CSV File", self._browse).pack(side="left", padx=6)
        styled_btn(btn_row, "✅ Import All", self._import_all,
                   color="#7DC99A", fg=TEXT).pack(side="left", padx=6)

        self.status = tk.Label(self, text="", font=FNT, bg=BG, fg=SUBTEXT)
        self.status.pack()

        # Preview tree
        tk.Label(self, text="Preview", font=FNT_B, bg=BG, fg=TEXT
                 ).pack(anchor="w", padx=28, pady=(8,2))
        wrap = tk.Frame(self, bg=BG)
        wrap.pack(fill="both", expand=True, padx=28, pady=(0,8))
        cols = ("Date","Type","Category","Description/Merchant","Amount")
        self.tree = ttk.Treeview(wrap, columns=cols, show="headings",
                                 style="Pink.Treeview")
        for col, w in zip(cols,[100,80,150,250,100]):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=w, anchor="center")
        sb2 = ttk.Scrollbar(wrap, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=sb2.set)
        self.tree.pack(side="left", fill="both", expand=True)
        sb2.pack(side="right", fill="y")

    def _browse(self):
        path = filedialog.askopenfilename(
            title="Select Apple Wallet CSV",
            filetypes=[("CSV files","*.csv"),("All files","*.*")])
        if not path:
            return
        self._load_csv(path)

    def _load_csv(self, path):
        self.preview_data = []
        for row in self.tree.get_children():
            self.tree.delete(row)
        try:
            with open(path, newline="", encoding="utf-8-sig") as f:
                reader = csv.DictReader(f)
                # Normalise headers
                raw_headers = reader.fieldnames or []
                header_map = {h.lower().strip(): h for h in raw_headers}

                def get(row, *keys):
                    for k in keys:
                        for hk, orig in header_map.items():
                            if k in hk:
                                return row.get(orig, "").strip()
                    return ""

                count = 0
                for row in reader:
                    date_raw   = get(row, "transaction date","date")
                    desc       = get(row, "description","merchant","memo")
                    merchant   = get(row, "merchant","vendor","description")
                    category   = get(row, "category")
                    type_raw   = get(row, "type","transaction type")
                    amount_raw = get(row, "amount")

                    if not amount_raw:
                        continue

                    # Parse amount
                    amount_str = amount_raw.replace("$","").replace(",","").strip()
                    try:
                        amount = float(amount_str)
                    except ValueError:
                        continue

                    # Determine income vs expense
                    type_lower = type_raw.lower()
                    if "credit" in type_lower or "payment" in type_lower:
                        txn_type = "income"
                    elif "debit" in type_lower or "purchase" in type_lower:
                        txn_type = "expense"
                    elif amount < 0:
                        txn_type = "expense"
                        amount = abs(amount)
                    else:
                        txn_type = "expense"

                    # Ensure amount positive
                    amount = abs(amount)

                    # Map category
                    mapped_cat = map_apple_category(category)

                    # Parse date
                    date_iso = datetime.now().isoformat()
                    for fmt in ["%m/%d/%Y","%Y-%m-%d","%d/%m/%Y","%m-%d-%Y"]:
                        try:
                            date_iso = datetime.strptime(date_raw, fmt).isoformat()
                            break
                        except ValueError:
                            pass

                    note = merchant if merchant else desc

                    txn = {"date": date_iso, "type": txn_type,
                           "category": mapped_cat, "note": note,
                           "amount": amount}
                    self.preview_data.append(txn)

                    sign = "+" if txn_type == "income" else "-"
                    self.tree.insert("","end",
                        values=(date_iso[:10], txn_type.capitalize(),
                                mapped_cat, note, f"{sign}${amount:.2f}"))
                    count += 1

            self.status.configure(
                text=f"✨ Loaded {count} transactions — click 'Import All' to save!",
                fg="#7DC99A")
        except Exception as e:
            messagebox.showerror("Error", f"Could not read CSV:\n{e}")
            self.status.configure(text="❌ Failed to load file.", fg="#E07A7A")

    def _import_all(self):
        if not self.preview_data:
            messagebox.showinfo("Nothing to import",
                                "Please choose a CSV file first 💕"); return
        # Deduplicate by date+note+amount
        existing = {(t["date"][:10], t["note"], t["amount"])
                    for t in self.app.data["transactions"]}
        added = 0
        for t in self.preview_data:
            key = (t["date"][:10], t["note"], t["amount"])
            if key not in existing:
                self.app.data["transactions"].append(t)
                existing.add(key)
                added += 1
        save_data(self.app.data)
        self.status.configure(
            text=f"🎉 Imported {added} new transactions! ({len(self.preview_data)-added} duplicates skipped)",
            fg=ACCENT)
        messagebox.showinfo("Done!", f"Imported {added} transactions 🌸")

    def refresh(self):
        pass


# ══════════════════════════════════════════════════════════════════
class BudgetsFrame(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=BG)
        self.app = app
        self._build()

    def _build(self):
        tk.Label(self, text="🗂️ Budget Categories", font=FNT_TITLE,
                 bg=BG, fg=TEXT).pack(pady=(18,4))

        form = card_frame(self, padx=22, pady=14)
        form.pack(fill="x", padx=28, pady=(0,10))
        r = tk.Frame(form, bg=WHITE)
        r.pack(fill="x")
        tk.Label(r, text="Category:", font=FNT, bg=WHITE, fg=TEXT).pack(side="left")
        self.bcat_var = tk.StringVar(value=CATEGORIES[0])
        ttk.Combobox(r, textvariable=self.bcat_var, values=CATEGORIES,
                     font=FNT, width=22, state="readonly").pack(side="left", padx=8)
        tk.Label(r, text="Monthly Budget: $", font=FNT, bg=WHITE, fg=TEXT).pack(side="left", padx=(14,0))
        self.blimit_var = tk.StringVar()
        tk.Entry(r, textvariable=self.blimit_var, font=FNT, width=10,
                 bg=BG, fg=TEXT, relief="flat",
                 highlightbackground=BORDER, highlightthickness=1).pack(side="left", padx=4)
        styled_btn(form, "Set Budget", self._set_budget).pack(pady=(10,0))

        self.budget_body = tk.Frame(self, bg=BG)
        self.budget_body.pack(fill="both", expand=True, padx=28, pady=8)

    def _set_budget(self):
        try:
            limit = float(self.blimit_var.get())
        except ValueError:
            messagebox.showerror("Oops!", "Enter a valid amount 💕"); return
        self.app.data["budgets"][self.bcat_var.get()] = limit
        save_data(self.app.data)
        self.blimit_var.set("")
        self.refresh()

    def refresh(self):
        for w in self.budget_body.winfo_children():
            w.destroy()
        budgets = self.app.data.get("budgets", {})
        if not budgets:
            tk.Label(self.budget_body, text="No budgets set yet 🌸 Add one above!",
                     font=FNT, bg=BG, fg=SUBTEXT).pack(pady=20); return

        now = datetime.now()
        txns = self.app.data["transactions"]
        mt   = [t for t in txns
                if datetime.fromisoformat(t["date"]).month == now.month
                and datetime.fromisoformat(t["date"]).year == now.year
                and t["type"] == "expense"]

        for cat, limit in budgets.items():
            spent = sum(t["amount"] for t in mt if t["category"] == cat)
            pct   = min(spent / limit, 1.0) if limit > 0 else 0
            color = "#E07A7A" if pct > 0.85 else "#F5C242" if pct > 0.6 else "#7DC99A"

            c = card_frame(self.budget_body, padx=16, pady=10)
            c.pack(fill="x", pady=4)
            top = tk.Frame(c, bg=WHITE)
            top.pack(fill="x")
            tk.Label(top, text=cat, font=FNT_B, bg=WHITE, fg=TEXT).pack(side="left")
            tk.Label(top, text=f"${spent:.2f} / ${limit:.2f}",
                     font=FNT, bg=WHITE, fg=SUBTEXT).pack(side="right")

            bar_bg = tk.Frame(c, bg="#F0E0E8", height=14)
            bar_bg.pack(fill="x", pady=(6,2))
            bar_bg.update_idletasks()
            w = int(bar_bg.winfo_width() * pct)
            tk.Frame(bar_bg, bg=color, height=14, width=max(w,4)).place(x=0, y=0)

            del_btn = tk.Button(c, text="✕ Remove", font=FNT_S,
                                bg=WHITE, fg=SUBTEXT, bd=0, cursor="hand2",
                                command=lambda k=cat: self._remove(k))
            del_btn.pack(anchor="e")

    def _remove(self, cat):
        del self.app.data["budgets"][cat]
        save_data(self.app.data)
        self.refresh()


# ══════════════════════════════════════════════════════════════════
class SavingsFrame(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=BG)
        self.app = app
        self._build()

    def _build(self):
        tk.Label(self, text="🌟 Savings Goals", font=FNT_TITLE,
                 bg=BG, fg=TEXT).pack(pady=(18,4))

        form = card_frame(self, padx=22, pady=14)
        form.pack(fill="x", padx=28, pady=(0,10))
        r1 = tk.Frame(form, bg=WHITE)
        r1.pack(fill="x", pady=3)
        tk.Label(r1, text="Goal name:", font=FNT, bg=WHITE, fg=TEXT,
                 width=12, anchor="w").pack(side="left")
        self.gname_var = tk.StringVar()
        tk.Entry(r1, textvariable=self.gname_var, font=FNT, width=22,
                 bg=BG, fg=TEXT, relief="flat",
                 highlightbackground=BORDER, highlightthickness=1).pack(side="left", padx=6)
        tk.Label(r1, text="Target: $", font=FNT, bg=WHITE, fg=TEXT).pack(side="left", padx=(14,0))
        self.gtarget_var = tk.StringVar()
        tk.Entry(r1, textvariable=self.gtarget_var, font=FNT, width=10,
                 bg=BG, fg=TEXT, relief="flat",
                 highlightbackground=BORDER, highlightthickness=1).pack(side="left", padx=4)

        r2 = tk.Frame(form, bg=WHITE)
        r2.pack(fill="x", pady=3)
        tk.Label(r2, text="Saved so far: $", font=FNT, bg=WHITE, fg=TEXT,
                 width=14, anchor="w").pack(side="left")
        self.gsaved_var = tk.StringVar(value="0")
        tk.Entry(r2, textvariable=self.gsaved_var, font=FNT, width=10,
                 bg=BG, fg=TEXT, relief="flat",
                 highlightbackground=BORDER, highlightthickness=1).pack(side="left", padx=6)
        tk.Label(r2, text="Emoji:", font=FNT, bg=WHITE, fg=TEXT).pack(side="left", padx=(14,0))
        self.gemoji_var = tk.StringVar(value="🎯")
        ttk.Combobox(r2, textvariable=self.gemoji_var,
                     values=["🎯","✈️","🏠","🚗","💍","👗","💻","📱","🌴","🐾"],
                     font=FNT, width=6, state="readonly").pack(side="left", padx=4)

        styled_btn(form, "＋ Add Goal", self._add_goal).pack(pady=(10,0))

        self.goals_body = tk.Frame(self, bg=BG)
        self.goals_body.pack(fill="both", expand=True, padx=28, pady=8)

    def _add_goal(self):
        name = self.gname_var.get().strip()
        if not name:
            messagebox.showerror("Oops!", "Give your goal a name! 🌸"); return
        try:
            target = float(self.gtarget_var.get())
            saved  = float(self.gsaved_var.get())
        except ValueError:
            messagebox.showerror("Oops!", "Enter valid amounts 💕"); return
        goal = {"name": name, "target": target,
                "saved": saved, "emoji": self.gemoji_var.get()}
        self.app.data["savings_goals"].append(goal)
        save_data(self.app.data)
        self.gname_var.set("")
        self.gtarget_var.set("")
        self.gsaved_var.set("0")
        self.refresh()

    def refresh(self):
        for w in self.goals_body.winfo_children():
            w.destroy()
        goals = self.app.data.get("savings_goals", [])
        if not goals:
            tk.Label(self.goals_body,
                     text="No savings goals yet 🌸 Add one above!",
                     font=FNT, bg=BG, fg=SUBTEXT).pack(pady=20); return

        for i, g in enumerate(goals):
            pct   = min(g["saved"] / g["target"], 1.0) if g["target"] > 0 else 0
            c = card_frame(self.goals_body, padx=18, pady=12)
            c.pack(fill="x", pady=5)
            top = tk.Frame(c, bg=WHITE)
            top.pack(fill="x")
            tk.Label(top, text=f"{g['emoji']} {g['name']}", font=FNT_B,
                     bg=WHITE, fg=TEXT).pack(side="left")
            tk.Label(top, text=f"{pct*100:.0f}% complete",
                     font=FNT, bg=WHITE, fg=SUBTEXT).pack(side="right")

            bar_bg = tk.Frame(c, bg="#F0E0E8", height=18)
            bar_bg.pack(fill="x", pady=(6,4))
            bar_bg.update_idletasks()
            bar_w = bar_bg.winfo_width()
            fill_w = max(int(bar_w * pct), 4)
            tk.Frame(bar_bg, bg=GOLD, height=18, width=fill_w).place(x=0, y=0)

            bot = tk.Frame(c, bg=WHITE)
            bot.pack(fill="x")
            tk.Label(bot, text=f"${g['saved']:,.2f} saved of ${g['target']:,.2f}",
                     font=FNT_S, bg=WHITE, fg=SUBTEXT).pack(side="left")

            btn_row = tk.Frame(c, bg=WHITE)
            btn_row.pack(anchor="e")
            styled_btn(btn_row, "＋ Add Savings",
                       lambda idx=i: self._add_to_goal(idx),
                       color=ACCENT2, fg=TEXT).pack(side="left", padx=4)
            tk.Button(btn_row, text="✕", font=FNT_S,
                      bg=WHITE, fg=SUBTEXT, bd=0, cursor="hand2",
                      command=lambda idx=i: self._remove_goal(idx)).pack(side="left")

    def _add_to_goal(self, idx):
        val = tk.simpledialog.askfloat("Add Savings",
                                       "How much did you save? 💰",
                                       parent=self, minvalue=0)
        if val:
            self.app.data["savings_goals"][idx]["saved"] += val
            save_data(self.app.data)
            self.refresh()

    def _remove_goal(self, idx):
        self.app.data["savings_goals"].pop(idx)
        save_data(self.app.data)
        self.refresh()


# ══════════════════════════════════════════════════════════════════
class SummaryFrame(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=BG)
        self.app = app
        self._build()

    def _build(self):
        tk.Label(self, text="📊 Monthly Summary", font=FNT_TITLE,
                 bg=BG, fg=TEXT).pack(pady=(18,4))

        ctrl = tk.Frame(self, bg=BG)
        ctrl.pack()
        now = datetime.now()
        self.month_var = tk.IntVar(value=now.month)
        self.year_var  = tk.IntVar(value=now.year)
        tk.Label(ctrl, text="Month:", font=FNT, bg=BG, fg=TEXT).pack(side="left")
        ttk.Combobox(ctrl, textvariable=self.month_var,
                     values=list(range(1,13)), width=5,
                     state="readonly").pack(side="left", padx=4)
        tk.Label(ctrl, text="Year:", font=FNT, bg=BG, fg=TEXT).pack(side="left", padx=(10,0))
        ttk.Combobox(ctrl, textvariable=self.year_var,
                     values=list(range(2020, now.year+2)), width=7,
                     state="readonly").pack(side="left", padx=4)
        styled_btn(ctrl, "🔍 View", self.refresh).pack(side="left", padx=10)

        self.chart_area = tk.Frame(self, bg=BG)
        self.chart_area.pack(fill="both", expand=True, padx=20, pady=8)

    def refresh(self):
        for w in self.chart_area.winfo_children():
            w.destroy()

        month = self.month_var.get()
        year  = self.year_var.get()
        txns  = self.app.data["transactions"]
        mt    = [t for t in txns
                 if datetime.fromisoformat(t["date"]).month == month
                 and datetime.fromisoformat(t["date"]).year == year]

        income  = sum(t["amount"] for t in mt if t["type"] == "income")
        expense = sum(t["amount"] for t in mt if t["type"] == "expense")

        # Totals
        row = tk.Frame(self.chart_area, bg=BG)
        row.pack(fill="x", pady=(0,10))
        for title, val, col in [("Total Income", income,"#7DC99A"),
                                 ("Total Expenses", expense,"#E07A7A"),
                                 ("Net Savings", income-expense, ACCENT)]:
            c = card_frame(row, padx=16, pady=10)
            c.pack(side="left", expand=True, fill="both", padx=6)
            tk.Label(c, text=title, font=FNT, bg=WHITE, fg=SUBTEXT).pack()
            tk.Label(c, text=f"${val:,.2f}", font=FNT_BIG, bg=WHITE, fg=col).pack()

        # Charts
        exp_by_cat = {}
        for t in mt:
            if t["type"] == "expense":
                exp_by_cat[t["category"]] = exp_by_cat.get(t["category"],0) + t["amount"]

        pastel_colors = ["#FFB3C6","#FFDDC1","#C1F0C8","#C1D4F0",
                         "#E8C1F0","#F0E8C1","#C1EEF0","#F0C1C1",
                         "#D4F0C1","#F0D4C1","#C8C1F0","#F0C1E8"]

        fig = Figure(figsize=(9, 3.4), facecolor=BG)

        # Pie chart
        ax1 = fig.add_subplot(121)
        if exp_by_cat:
            labels = list(exp_by_cat.keys())
            vals   = list(exp_by_cat.values())
            ax1.pie(vals, labels=None, colors=pastel_colors[:len(vals)],
                    autopct="%1.0f%%", startangle=140,
                    wedgeprops={"edgecolor":"white","linewidth":2},
                    textprops={"fontsize":8, "color":TEXT})
            ax1.legend(labels, loc="lower center", bbox_to_anchor=(0.5,-0.3),
                       fontsize=7, ncol=2,
                       frameon=False)
            ax1.set_title("Spending by Category", color=TEXT, fontsize=11, pad=10)
        else:
            ax1.text(0.5,0.5,"No expenses this month 🌸",
                     ha="center",va="center",color=SUBTEXT,fontsize=10)
            ax1.axis("off")

        # Bar chart – income vs expense per day
        ax2 = fig.add_subplot(122)
        days_e = {}
        days_i = {}
        for t in mt:
            d = datetime.fromisoformat(t["date"]).day
            if t["type"] == "expense":
                days_e[d] = days_e.get(d,0) + t["amount"]
            else:
                days_i[d] = days_i.get(d,0) + t["amount"]
        if days_e or days_i:
            all_days = sorted(set(list(days_e.keys())+list(days_i.keys())))
            ie = [days_e.get(d,0) for d in all_days]
            ii = [days_i.get(d,0) for d in all_days]
            x  = range(len(all_days))
            ax2.bar(x, ie, color=ACCENT2, label="Expense", width=0.5)
            ax2.bar(x, ii, color="#A8D8A8", label="Income",
                    width=0.3, alpha=0.8)
            ax2.set_xticks(list(x))
            ax2.set_xticklabels([str(d) for d in all_days], fontsize=7, color=TEXT)
            ax2.set_facecolor(BG)
            ax2.tick_params(axis="y", labelcolor=TEXT, labelsize=7)
            ax2.spines[:].set_edgecolor(BORDER)
            ax2.legend(fontsize=7, frameon=False, labelcolor=TEXT)
            ax2.set_title("Daily Spending & Income", color=TEXT, fontsize=11)
        else:
            ax2.text(0.5,0.5,"No data this month 🌸",
                     ha="center",va="center",color=SUBTEXT,fontsize=10)
            ax2.axis("off")

        fig.tight_layout(pad=2)
        canvas = FigureCanvasTkAgg(fig, self.chart_area)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)


# ══════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    import tkinter.simpledialog as sd
    tk.simpledialog = sd
    app = FinanceApp()
    app.mainloop()