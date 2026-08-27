# The Sharp Edge Barber Shop — Web App

> A full-stack web application built with **Python**, **Streamlit**, and **SQLite**.  
> Designed as a portfolio project for junior web developer job applications.

---

## 📋 Project Overview

**The Sharp Edge Barber Shop** is a multi-page booking and management web app that demonstrates:

- Real CRUD functionality (Create, Read, Update, Delete) with SQLite
- Form validation (presence checks, regex, double-booking prevention)
- Admin authentication using session state
- Custom dark-themed UI via CSS injected into Streamlit
- Clean code architecture (data layer, database layer, presentation layer)

---

## 🗂️ Project Structure

```
barber_shop_app/
├── app.py                  # Main entry point — page config, CSS, DB init
├── database.py             # All SQLite functions (init, insert, fetch, delete)
├── data.py                 # Static data: services, barbers, shop info, time slots
├── style.css               # Custom CSS injected globally via st.markdown()
├── requirements.txt        # Python dependencies
├── pages/
│   ├── 1_Home.py           # Landing page: hero, hours, location
│   ├── 2_Services.py       # Service menu with cards and stats
│   ├── 3_Barbers.py        # Team page with barber cards
│   ├── 4_Book_Appointment.py  # Booking form with full validation
│   ├── 5_Admin_Dashboard.py   # Password-protected booking management
│   └── 6_Contact.py        # Contact info + contact form
└── barber_shop.db          # SQLite database file (auto-created on first run)
```

---

## 🗄️ Database Schema

### Table: `appointments`

| Column      | Type    | Constraint          | Purpose                        |
|-------------|---------|---------------------|--------------------------------|
| id          | INTEGER | PRIMARY KEY AUTO    | Unique booking reference       |
| name        | TEXT    | NOT NULL            | Customer's full name           |
| phone       | TEXT    | NOT NULL            | Customer phone number          |
| email       | TEXT    | NOT NULL            | Customer email                 |
| service     | TEXT    | NOT NULL            | Service chosen                 |
| barber      | TEXT    | NOT NULL            | Barber name                    |
| appt_date   | TEXT    | NOT NULL            | Date in YYYY-MM-DD format      |
| appt_time   | TEXT    | NOT NULL            | Time in HH:MM 24-hour format   |
| created_at  | TEXT    | NOT NULL            | ISO timestamp of submission    |

### Table: `messages`

| Column      | Type    | Constraint          | Purpose                        |
|-------------|---------|---------------------|--------------------------------|
| id          | INTEGER | PRIMARY KEY AUTO    | Unique message ID              |
| sender_name | TEXT    | NOT NULL            | Contact form submitter's name  |
| message     | TEXT    | NOT NULL            | Message body                   |
| sent_at     | TEXT    | NOT NULL            | ISO timestamp of submission    |

---

## 🚀 Local Setup

### Prerequisites

- Python 3.9 or higher
- pip

### Installation Steps

```bash
# 1. Clone or download this repository
git clone https://github.com/YOUR_USERNAME/barber-shop-app.git
cd barber-shop-app

# 2. Create a virtual environment (recommended)
python -m venv venv

# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
streamlit run app.py
```

The app will open at **http://localhost:8501** in your browser.

> **Note:** The SQLite database file (`barber_shop.db`) is created automatically  
> in the project folder on first run. You don't need to do anything.

### Admin Dashboard

- Navigate to **Admin Dashboard** in the sidebar
- Default password: `sharpedge2024`
- **Change this before deploying!** See the Secrets section below.

---

## ☁️ Deployment on Streamlit Community Cloud (Free)

### Step 1: Push to GitHub

```bash
# Initialize a git repo (if not already done)
git init
git add .
git commit -m "Initial commit: Barber Shop App"

# Create a new repo on GitHub, then:
git remote add origin https://github.com/YOUR_USERNAME/barber-shop-app.git
git branch -M main
git push -u origin main
```

> **Important:** Add `barber_shop.db` to your `.gitignore` so you don't  
> commit the database file. The cloud server will create it fresh on deploy.

Create a `.gitignore` file:
```
barber_shop.db
__pycache__/
*.pyc
.env
venv/
```

### Step 2: Create a Streamlit Community Cloud Account

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with your GitHub account
3. Click **"New app"**

### Step 3: Configure the App

Fill in the deployment form:
- **Repository:** `YOUR_USERNAME/barber-shop-app`
- **Branch:** `main`
- **Main file path:** `app.py`

Click **"Deploy!"** — Streamlit will install `requirements.txt` automatically.

### Step 4: Set Up the Admin Password as a Secret

Instead of hardcoding the password in `data.py`, use Streamlit Secrets for production:

1. In your deployed app dashboard, click **"Settings"** → **"Secrets"**
2. Add this in the secrets editor:
   ```toml
   admin_password = "your_secure_password_here"
   ```
3. In `data.py`, replace the `ADMIN_PASSWORD` line with:
   ```python
   import streamlit as st
   ADMIN_PASSWORD = st.secrets.get("admin_password", "sharpedge2024")
   ```

> `st.secrets.get("key", "fallback")` uses the secret if deployed,  
> falls back to the default if running locally without a secrets file.

### Step 5: Verify Deployment

- Your app will be live at:  
  `https://YOUR_USERNAME-barber-shop-app-app-XXXXX.streamlit.app`
- Test all pages: Home, Services, Barbers, Book Appointment, Admin, Contact
- Make a test booking and verify it appears in the Admin Dashboard

---

## 🔒 Security Notes

| Topic | This App | Production Standard |
|-------|----------|---------------------|
| Admin password | Plaintext comparison | bcrypt hash + env var |
| SQL queries | Parameterized (`?`) ✅ | Parameterized (`?`) ✅ |
| Input validation | Python-side regex | Python + DB constraints |
| Session auth | `st.session_state` | JWT / session token |
| DB file | Local SQLite | PostgreSQL on cloud |

The parameterized queries (`?` placeholders) used throughout `database.py`  
**prevent SQL injection** — the most important security practice in this codebase.

---

## 🛠️ Tech Stack

| Technology | Version | Role |
|------------|---------|------|
| Python | 3.9+ | Backend logic and scripting |
| Streamlit | Latest | Web framework + UI rendering |
| SQLite (sqlite3) | Built-in | Database (no install needed) |
| pandas | Latest | DataFrame display in admin |
| Pillow | Latest | Image support (future use) |
| Custom CSS | — | Injected via `st.markdown()` |

---

## 💡 Potential Improvements (for interviews)

1. **Migrate to PostgreSQL** for multi-user concurrent access
2. **Add email confirmation** using Python's `smtplib` or SendGrid API
3. **Add barber availability schedules** (a barbers table with day/time availability)
4. **Implement proper auth** with `streamlit-authenticator` library
5. **Add SMS reminders** using Twilio API
6. **Deploy on Heroku/Render** instead of Streamlit Cloud for persistent DB storage
7. **Add unit tests** with pytest for the database functions

---

## 📄 License

MIT License — free to use, modify, and share.

---

*Built with ❤️ as a junior developer portfolio project.*
