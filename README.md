# 🚨 girl-do-not-buy-that

A sassy personal finance tracker for people who need their money app to match their energy. Built with Python + tkinter. No subscriptions, no ads, no judgment (okay, a little judgment).

---

## ✨ Features

- **💎 Net Worth tracker** — see your total money across all time, with optional starting balance
- **💸 Transaction logging** — manually add expenses and income, or import from CSV
- **📥 Apple Card CSV import** — drag in your Apple Card export and it auto-categorizes everything
- **🗂️ Budget tracking** — set monthly limits per category and see if you stayed under
- **📅 Budget history** — browse past months to see which ones you actually behaved in
- **🌟 Savings goals** — track progress toward things you're manifesting
- **💰 Income flow** — separate view for money coming IN
- **📊 Charts** — pie chart by category + daily bar chart, with hover tooltips
- **🎨 8 themes** — because aesthetics matter
- **🔍 Filters** — filter transactions by month, year, and category

---

## 🖥️ Tabs

| Tab | Vibe |
|-----|------|
| 🏠 Home Base | Dashboard — net worth, this month's stats, recent transactions |
| 💸 The Damage | Full transaction list with filters and editing |
| 📥 Drop the Receipts | CSV import with preview |
| 🗂️ Damage Control | Budget limits + history by month |
| 🌟 Future Rich Girl Plans | Savings goals |
| 💰 Income Flow | Income logging and breakdown |
| 📊 The Hard Truth | Charts — pie by category, daily bar chart |
| 🎨 Switch Vibes | Theme picker |

---

## 📊 Charts

### Pie Chart (Crimes by Category)
- Shows spending breakdown for the selected month or date range
- **Hover** over a slice to see the category name, amount, and percentage
- **Click** a slice to jump straight to The Damage tab filtered by that category

### Bar Chart (Daily Damage Report)
- Shows expenses and income by day of the month
- **Hover** over a bar to see every transaction from that day

### Date Range
Toggle between **Single Month** and **Date Range** mode to aggregate charts across multiple months or an entire year.

---

## 📥 CSV Import

Supports **Apple Card** CSV exports out of the box.

Expected columns:
```
Transaction Date  •  Description  •  Merchant  •  Category  •  Type  •  Amount
```

**Apple Card behavior:**
- `Type = Payment` → logged as an **expense**
- `Type = Debit` → logged as **income** (cash back)
- ACH bank transfers (payments to the card) are **automatically skipped**

---

## 🛍️ Categories

| Category | Category |
|----------|----------|
| 🛍️ Shopping | 🍔 Restaurants |
| 🫑 Grocery | 💅 Self-care |
| 🚗 Transport | 🎉 Entertainment |
| ✈️ Travel | 💡 Utilities |
| 🏥 Medical | 💼 Income |
| 🔂 Subscriptions | 🤕 Insurance |
| 🅿️ Parking | 📦 Other |

---

## 🎨 Themes

| Theme | Aesthetic |
|-------|-----------|
| 💖 Tickle-me-pink | Classic bimbo pink |
| 💜 Lavender Haze | Soft purple dreamscape |
| 🌿 Minty Fresh | Clean green energy |
| 🌙 Midnight Glam | Dark mode, but make it fashion |
| 🍑 Peachy Ken | Warm peachy tones |

Themes save automatically. Pick your aesthetic, queen 👑

---

## 💬 The Language

| Generic | Girl Don't Buy That |
|--------|---------------------|
| 🏠 Dashboard | 🏠 Home Base |
| 💸 Transactions | 💸 The Damage |
| 📥 Import CSV | 📥 Drop the Receipts |
| 🗂️ Budgets | 🗂️ Damage Control |
| Expenses | Crimes Committed 💀 |
| Recent Transactions | Recent Bad Decisions |
| Add Transaction | Confess a Purchase 🛍️ |
| Delete Selected | Delete the Evidence 🗑️ |
| No budgets set yet | No budgets set... which honestly explains a lot 👀 |
| Total Expenses | Money Gone 💀 |
| Spending by Category | Crimes by Category 💀 |
| Savings Goals | Future Rich Girl Plans 🌟 |
| Income | Money Coming IN 💰 |
| Net Worth | 💎 Total Net Worth |
| Summary / Charts | The Hard Truth 📊 |
| Theme Settings | Switch Vibes 🎨 |
| Budget History | 📅 Budget History |
| Submit / Confirm | Lock It In 🔒 |
| Remove Budget | Abandon Ship ✕ |
| No savings goals yet | No goals yet?? Girl, DREAM BIGGER 💅 |
| Add funds to goal | I Saved Money! 🎉 |
| Transaction updated | Okay bestie 🌸 |
| Delete confirmation | No take-backs 💀 |
| Invalid number | That's not a number bestie 💀 |

---

## 🚀 Running It

```bash
python app.py
```

**Requirements:** Python 3.x with tkinter and matplotlib

```bash
pip install matplotlib
```

---

## 💾 Data

All data is saved locally to `finance_data.json` in the same directory as the app. No cloud, no sync, no one else's business 💅