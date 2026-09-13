# Money Transfer App

A full-stack fintech wallet & P2P money transfer platform built to solve real problems with existing remittance apps: high fees, complex onboarding, lack of access for the unbanked, weak security, and poor admin visibility.

**Live Demo:** _coming soon_  
**Author:** [Oliver Moosberger](https://github.com/olivermooz-117) · olivermooz@gmail.com

---

## Problem → Solution

| Problem | How this app addresses it |
|---------|---------------------------|
| High transaction fees | Transparent 1% fee, hard-capped at 100 units |
| Complex onboarding | Register with name + email + password → wallet created instantly |
| Unbanked / underbanked | No bank account or card required |
| Security & fraud risk | bcrypt passwords, JWT auth, admin-gated routes |
| No platform visibility | Full admin dashboard with users, transactions, analytics & monthly fee revenue |

---

## Tech Stack

**Backend**  
Python · Flask · Flask-SQLAlchemy · Flask-JWT-Extended · Flask-Bcrypt · PostgreSQL · pytest

**Frontend**  
React 18 · Redux Toolkit · React Router · Axios · Vite · Jest + React Testing Library

**Design**  
Mobile-first wireframes (Figma)

---

## Features

### User
- Register / Login
- Wallet balance + 30-day analytics
- Add funds
- Manage beneficiaries
- Send money (fee shown transparently)
- Transaction history

### Admin
- CRUD on all users
- View every transaction
- Platform-wide analytics (users, total balance, volume, fees collected)
- Monthly profit (fee revenue) trends

---

## Project Structure
Money-Transfer-App/
├── backend/
│   ├── app/
│   │   ├── models/          # User, Wallet, Beneficiary, Transaction
│   │   ├── routes/          # auth, users, wallet, beneficiaries, transactions, admin
│   │   ├── utils/           # admin_required decorator
│   │   ├── config.py
│   │   └── extensions.py
│   ├── tests/
│   ├── seed.py
│   └── run.py
└── frontend/
├── src/
│   ├── api/
│   ├── app/             # Redux store
│   ├── features/        # auth, wallet, beneficiaries, transactions, admin
│   └── components/
└── package.json
text---

## Quick Start

### 1. Backend

```bash
cd backend
cp .env.example .env
# Edit .env → set DATABASE_URL and a strong JWT_SECRET_KEY

pipenv install && pipenv shell
# or: python3 -m venv venv && source venv/bin/activate && pip install flask flask-sqlalchemy flask-migrate flask-jwt-extended flask-bcrypt flask-cors psycopg2-binary python-dotenv pytest

python seed.py
python run.py
# → http://localhost:5000/api/health
Demo logins:

admin@moneyapp.com / Admin123!
oliver@example.com / Password123!
jane@example.com / Password123!

2. Frontend
Bashcd frontend
cp .env.example .env
# Confirm VITE_API_URL=http://localhost:5000/api

npm install
npm run dev
# → http://localhost:5173
3. Tests
Bashcd backend && python -m pytest -v
cd frontend && npm test

API Overview







































































MethodEndpointAuthDescriptionPOST/api/auth/register—Create user + walletPOST/api/auth/login—Get JWTGET/api/walletuserBalance + analyticsPOST/api/wallet/add-fundsuserTop upGET/POST/api/beneficiariesuserList / addPOST/api/transactions/senduserSend moneyGET/api/transactionsuserOwn historyGET/api/admin/usersadminAll usersGET/api/admin/analyticsadminPlatform totalsGET/api/admin/profit-trendsadminMonthly fee revenue

Architecture Decisions

Wallet-first model — every user gets a wallet on registration.
Transparent low fees — 1% with hard cap, calculated server-side.
JWT + role claims — admin routes protected by is_admin claim.
Feature-sliced frontend — Redux Toolkit slices mirror domain boundaries.
Atomic transfers — money movement uses database row locking to prevent race conditions.