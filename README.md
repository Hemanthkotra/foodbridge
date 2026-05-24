# FoodBridge 🌱

> Connecting restaurants with surplus food to nearby orphanages — reducing waste, ending hunger, one meal at a time.

![Python](https://img.shields.io/badge/Python-3.12-blue?style=flat-square&logo=python)
![Flask](https://img.shields.io/badge/Flask-3.1-lightgrey?style=flat-square&logo=flask)
![SQLite](https://img.shields.io/badge/SQLite-3-blue?style=flat-square&logo=sqlite)
![TailwindCSS](https://img.shields.io/badge/Tailwind_CSS-3-38bdf8?style=flat-square&logo=tailwindcss)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

---

## The Problem

One-third of all food produced globally is wasted, while 690 million people go to bed hungry every night. Restaurants discard enormous quantities of perfectly good surplus food daily — food that could feed children in nearby orphanages.

## The Solution

FoodBridge is a full-stack web application that creates a direct bridge between restaurants with leftover food and orphanages that need it. Restaurants post surplus food listings. Orphanages browse and claim them with one click. No food goes to waste.

---

## Live Demo

🌐 **[https://foodbridge-350g.onrender.com](https://foodbridge-350g.onrender.com)**

> Note: The app is hosted on Render's free tier. The first load after inactivity may take 30–50 seconds to wake up.

---

## Features

- **Role-based accounts** — separate dashboards for restaurants and orphanages
- **Food listings** — restaurants post surplus food with item name, quantity, expiry time, and notes
- **One-click claiming** — orphanages claim available food; listings are instantly locked to prevent double-claims
- **Secure authentication** — passwords hashed with SHA-256, sessions managed server-side
- **Responsive UI** — clean, modern design with Tailwind CSS that works on all screen sizes
- **Auto-expiry logic** — food ordered by expiry time so the most urgent listings appear first

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python, Flask |
| Database | SQLite |
| Frontend | HTML, Tailwind CSS, JavaScript |
| Auth | SHA-256 password hashing, Flask sessions |
| Deployment | Render (free tier) |

---

## Project Structure

```
foodbridge/
├── templates/
│   ├── base.html                   # Shared layout, navbar, footer
│   ├── home.html                   # Landing page
│   ├── register.html               # Registration form (restaurant/orphanage)
│   ├── login.html                  # Login form
│   ├── dashboard_restaurant.html   # Post surplus food listings
│   └── dashboard_orphanage.html    # Browse and claim food
├── app.py                          # Flask routes and application logic
├── database.py                     # SQLite schema and initialization
├── requirements.txt                # Python dependencies
├── Procfile                        # Render deployment config
└── README.md
```

---

## Database Schema

Three tables power the application:

**users** — stores both restaurants and orphanages, distinguished by a `role` field (`restaurant` or `orphanage`)

**food_listings** — each surplus food item posted by a restaurant, with status tracking (`available`, `claimed`, `expired`)

**claims** — links orphanages to the food they claimed, with pickup status (`pending`, `picked_up`, `cancelled`)

---

## Getting Started Locally

### Prerequisites
- Python 3.10+
- pip

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/Hemanthkotra/foodbridge.git
cd foodbridge

# 2. Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Initialise the database
python database.py

# 5. Run the app
python app.py
```

Open your browser and go to `http://127.0.0.1:5000`

---

## How It Works

1. **A restaurant registers** and logs into their dashboard
2. **They post a food listing** — item name, quantity, expiry time, any notes
3. **An orphanage logs in** and sees all available listings ordered by expiry time
4. **They click "Claim this food"** — the listing is instantly marked as claimed
5. **The orphanage contacts the restaurant** directly using the phone number shown on the card to arrange pickup

---

## API Routes

| Method | Route | Description | Access |
|---|---|---|---|
| POST | `/register` | Create a new account | Public |
| POST | `/login` | Log in and start a session | Public |
| POST | `/logout` | Clear the session | Authenticated |
| POST | `/food/add` | Post a new food listing | Restaurant only |
| GET | `/food/available` | Fetch all available listings | Orphanage only |
| POST | `/food/claim/<id>` | Claim a food listing | Orphanage only |

---

## Screenshots

### Homepage
A clean landing page explaining the mission with stats and a step-by-step explainer.

### Restaurant Dashboard
A sticky form for posting surplus food with tips for faster claims.

### Orphanage Dashboard
A card-based grid of available food listings with restaurant contact details and a one-click Claim button.

---

## What I Learned

Building FoodBridge from scratch taught me:

- Designing and implementing a **relational database** with foreign keys
- Building a **REST API** with Flask and handling role-based access control
- Connecting a **Python backend to an HTML/CSS frontend** using Jinja2 templates
- **Password security** — never storing plain text, using SHA-256 hashing
- **Deploying a full-stack app** to a live server using Render and GitHub
- Using **Git** for version control throughout the development process

---

## Future Improvements

- Email/SMS notifications when food is claimed
- Google Maps integration to show restaurant locations
- Admin dashboard to monitor platform activity
- Food expiry auto-update via a background scheduler
- PWA support for mobile app-like experience

---

## Author

**Hemanth Kotra**
- GitHub: [@Hemanthkotra](https://github.com/Hemanthkotra)
- LinkedIn: [linkedin.com/in/hemanthkotra](https://linkedin.com/in/hemanthkotra)

---

## License

This project is open source and available under the [MIT License](LICENSE).

---

*Built with purpose — because no meal should go to waste while a child goes hungry.*
