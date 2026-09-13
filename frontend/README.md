# Money Transfer App

By Oliver Moosberger

## Description

Money Transfer App is a fintech wallet and remittance platform built to tackle five real problems with existing money transfer apps: high transaction fees, complex onboarding, poor access for unbanked/underbanked users, security/fraud risk, and lack of interoperability for cross-border transfers. Every user gets a wallet the moment they register (no bank account required), fees are capped low and shown up front, and admins get full visibility into users, transactions, and platform-wide trends.

## Technologies Used

**Backend:** Python, Flask, Flask-SQLAlchemy, Flask-JWT-Extended, Flask-Bcrypt, PostgreSQL, pytest
**Frontend:** React, Redux Toolkit, React Router, Axios, Vite, Jest + React Testing Library
**Design:** Figma (mobile-first wireframes)

## Project Structure

```
money-transfer-app/
├── backend/
│   ├── app/
│   │   ├── models/        # User, Wallet, Beneficiary, Transaction
│   │   ├── routes/        # auth, users, wallet, beneficiaries, transactions, admin
│   │   ├── utils/         # admin_required decorator
│   │   ├── config.py
│   │   └── extensions.py
│   ├── tests/              # pytest suite
│   ├── seed.py              # creates tables + demo data
│   ├── run.py                # entrypoint
│   └── Pipfile
└── frontend/
    ├── src/
    │   ├── api/axios.js      # shared axios instance with auth header
    │   ├── app/store.js      # Redux store
    │   ├── features/         # auth, wallet, beneficiaries, transactions, admin
    │   └── components/        # Navbar, ProtectedRoute
    └── package.json
```

## MVP Features

**As a user, I can:**
- Create an account and log in
- View my wallet analytics
- View and update my profile
- Add funds to my wallet
- Add beneficiaries as contacts
- Send money to a beneficiary
- View a summary of my transactions

**As an admin, I can:**
- Perform CRUD operations on all users and accounts
- View a summary of all user transactions
- View analytics of all wallet accounts
- View profit (fee revenue) trends to support business decisions

## Backend Setup — Step by Step

1. **Install PostgreSQL** if you don't already have it, and create a database:
   ```
   createdb money_transfer_db
   ```
2. **Move into the backend folder:**
   ```
   cd backend
   ```
3. **Create your environment file:**
   ```
   cp .env.example .env
   ```
   Then edit `.env` and set `DATABASE_URL` to match your Postgres user/password, and set `JWT_SECRET_KEY` to a long random string.
4. **Install dependencies** (using pipenv, matching your usual workflow):
   ```
   pipenv install
   pipenv shell
   ```
   If you hit Python version issues (e.g. system Python doesn't match the Pipfile), fall back to:
   ```
   python3 -m venv venv
   source venv/bin/activate
   pip install flask flask-sqlalchemy flask-migrate flask-jwt-extended flask-bcrypt flask-cors psycopg2-binary python-dotenv pytest
   ```
5. **Create the tables and seed demo data:**
   ```
   python seed.py
   ```
   This prints three demo logins (one admin, two regular users) you can use immediately.
6. **Run the server:**
   ```
   python run.py
   ```
   The API will be live at `http://localhost:5000/api`. Check `http://localhost:5000/api/health` to confirm it's running.
7. **Run the test suite** (all 7 tests should pass):
   ```
   python -m pytest -v
   ```

### Backend API Reference

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| POST | /api/auth/register | — | Create a user + wallet |
| POST | /api/auth/login | — | Get a JWT |
| GET | /api/users/me | user | View own profile |
| PUT | /api/users/me | user | Update own profile |
| GET | /api/wallet | user | Balance + analytics |
| POST | /api/wallet/add-funds | user | Top up wallet |
| GET/POST | /api/beneficiaries | user | List / add beneficiaries |
| DELETE | /api/beneficiaries/:id | user | Remove beneficiary |
| POST | /api/transactions/send | user | Send money to a beneficiary |
| GET | /api/transactions | user | Own transaction history |
| GET | /api/admin/users | admin | List all users |
| PUT/DELETE | /api/admin/users/:id | admin | Update/deactivate/delete a user |
| GET | /api/admin/transactions | admin | All transactions |
| GET | /api/admin/analytics | admin | Platform-wide totals |
| GET | /api/admin/profit-trends | admin | Monthly fee revenue |

## Frontend Setup — Step by Step

1. **Move into the frontend folder:**
   ```
   cd frontend
   ```
2. **Create your environment file:**
   ```
   cp .env.example .env
   ```
   Confirm `VITE_API_URL=http://localhost:5000/api` points at your running backend.
3. **Install dependencies:**
   ```
   npm install
   ```
4. **Run the dev server:**
   ```
   npm run dev
   ```
   Open the URL Vite prints (typically `http://localhost:5173`).
5. **Run the Jest test suite:**
   ```
   npm test
   ```
6. **Build for production when ready to deploy:**
   ```
   npm run build
   ```
   The static output lands in `frontend/dist`.

## Trying It End to End

1. Start the backend (`python run.py`) and frontend (`npm run dev`).
2. Register a new account, or log in with a seeded demo user (see `seed.py` output).
3. Add funds to your wallet from the dashboard.
4. Go to **Beneficiaries** and add another seeded user by their email (e.g. `jane@example.com`).
5. Go to **Send money**, pick that beneficiary, and send an amount — you'll see the 1% fee (capped at 100) applied automatically.
6. Log in as `admin@moneyapp.com` to see the admin views: all users, all transactions, platform analytics, and the monthly profit trend.

## How This Addresses the Problem Statement

- **High fees** → fee is capped at 1% (max 100 units), shown transparently in the response and in the transaction table.
- **Complex onboarding** → registration only asks for name, email, password; a wallet is created automatically.
- **Unbanked/underbanked access** → no bank account or card is required to hold or receive funds; wallet balance starts at 0 and is topped up in-app.
- **Security** → passwords are hashed with bcrypt, all wallet/transaction endpoints require a JWT, and admin routes are separately gated.
- **Interoperability** → the API is a standard REST/JSON service, and the fee/currency fields on `Wallet` and `Transaction` are structured to extend to multi-currency and cross-border transfers later.

## Author

Oliver Moosberger — GitHub: [olivermooz-117](https://github.com/olivermooz-117) · Email: olivermooz@gmail.com

## License

This project is open source and available for educational use.
