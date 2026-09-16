# Money Transfer App

A full-stack fintech wallet and P2P money transfer platform with **M-Pesa Daraja STK Push** top-ups.

Built to address high fees, complex onboarding, weak security, and poor admin visibility in typical remittance apps.

**Live Demo:** _coming soon_  
**Author:** [Oliver Moosberger](https://github.com/olivermooz-117)

---

## Problem → Solution

| Problem | How this app addresses it |
|---------|---------------------------|
| High transaction fees | Transparent 1% fee, hard-capped |
| Complex onboarding | Register → wallet created instantly |
| Unbanked / underbanked | No bank or card required; M-Pesa top-up |
| Security & fraud risk | bcrypt, JWT, role-based admin routes |
| No platform visibility | Admin analytics, users, fee revenue |

---

## Tech Stack

**Backend:** Python · Flask · SQLAlchemy · JWT · PostgreSQL · M-Pesa Daraja · pytest  

**Frontend:** React 18 · Redux Toolkit · React Router · Axios · Vite  

---

## Features

### User
- Register / Login (JWT)
- Wallet balance + analytics
- Top up via **M-Pesa STK Push**
- Beneficiaries
- Send money (server-side fee)
- Transaction history

### Admin
- User management
- All transactions
- Platform analytics & monthly fee revenue

---

## Project Structure

```text
Money-Transfer-App/
├── backend/
│   ├── app/
│   │   ├── models/       # User, Wallet, Beneficiary, Transaction, MpesaDeposit
│   │   ├── routes/       # auth, users, wallet, beneficiaries, transactions, admin, mpesa
│   │   ├── services/     # mpesa.py (Daraja STK Push)
│   │   ├── utils/
│   │   ├── config.py
│   │   └── extensions.py
│   ├── tests/
│   ├── seed.py
│   └── run.py
└── frontend/
    └── src/
        ├── api/
        ├── app/          # Redux store
        ├── features/     # auth, wallet, beneficiaries, transactions, admin
        └── components/