import React from "react";
import { Link } from "react-router-dom";
import { useSelector } from "react-redux";
import { Navigate } from "react-router-dom";

const FEATURES = [
  {
    title: "M-Pesa top-ups",
    text: "Fund your wallet in seconds with Lipa Na M-Pesa STK Push — no bank account required.",
  },
  {
    title: "Low, transparent fees",
    text: "Send money at 1% with a hard cap. No surprise charges — the fee is shown before you confirm.",
  },
  {
    title: "Secure by design",
    text: "bcrypt passwords, JWT sessions, and atomic transfers with database locking to protect balances.",
  },
  {
    title: "Built for Kenya",
    text: "KES wallets, phone-based deposits, and a simple flow that works for first-time digital users.",
  },
];

const REVIEWS = [
  {
    name: "Amina K.",
    role: "Small business owner, Nairobi",
    quote:
      "I top up with M-Pesa and pay suppliers the same day. The fee is clear and the app is easy to use.",
  },
  {
    name: "James O.",
    role: "Student, Kisumu",
    quote:
      "Sending money to family used to mean long queues. Now I do it from campus in under a minute.",
  },
  {
    name: "Grace W.",
    role: "Freelancer, Mombasa",
    quote:
      "No bank card needed. M-Pesa STK push feels familiar and the wallet balance is always accurate.",
  },
];

const STEPS = [
  { n: "1", title: "Create an account", text: "Register with name, email, and password. A wallet is created for you instantly." },
  { n: "2", title: "Top up via M-Pesa", text: "Enter your phone number, confirm the STK prompt, and funds land in your wallet." },
  { n: "3", title: "Send in seconds", text: "Add a beneficiary and transfer with a transparent fee — tracked in your history." },
];

export default function Landing() {
  const { token, user } = useSelector((state) => state.auth);

  if (token && user) {
    return <Navigate to="/dashboard" replace />;
  }

  return (
    <div className="landing">
      <section className="landing-hero">
        <div className="landing-hero-inner">
          <p className="landing-eyebrow">Wallet · M-Pesa · P2P transfers</p>
          <h1>Send and receive money without the friction</h1>
          <p className="landing-lead">
            A modern wallet built for everyday Kenyans — top up with M-Pesa, send to friends and family,
            and stay in control with clear fees and full transaction history.
          </p>
          <div className="landing-cta">
            <Link to="/register" className="btn btn-primary">
              Get started free
            </Link>
            <Link to="/login" className="btn btn-ghost">
              Log in
            </Link>
          </div>
          <p className="landing-note">No bank account required · Transparent 1% fee · JWT secured</p>
        </div>
      </section>

      <section className="landing-section">
        <h2>Why people choose Money Transfer</h2>
        <div className="landing-grid features">
          {FEATURES.map((f) => (
            <article key={f.title} className="landing-card">
              <h3>{f.title}</h3>
              <p>{f.text}</p>
            </article>
          ))}
        </div>
      </section>

      <section className="landing-section landing-alt">
        <h2>How it works</h2>
        <div className="landing-grid steps">
          {STEPS.map((s) => (
            <article key={s.n} className="landing-card step">
              <span className="step-num">{s.n}</span>
              <h3>{s.title}</h3>
              <p>{s.text}</p>
            </article>
          ))}
        </div>
      </section>

      <section className="landing-section">
        <h2>What users say</h2>
        <div className="landing-grid reviews">
          {REVIEWS.map((r) => (
            <blockquote key={r.name} className="landing-card review">
              <p className="quote">“{r.quote}”</p>
              <footer>
                <strong>{r.name}</strong>
                <span>{r.role}</span>
              </footer>
            </blockquote>
          ))}
        </div>
        <p className="landing-disclaimer">
          Sample testimonials for demo purposes — replace with real feedback when you launch.
        </p>
      </section>

      <section className="landing-section landing-final">
        <h2>Ready to move money smarter?</h2>
        <p>Create your wallet in under a minute and top up with M-Pesa today.</p>
        <Link to="/register" className="btn btn-primary">
          Create free account
        </Link>
      </section>

      <footer className="landing-footer">
        <span>Money Transfer App</span>
        <span>Built with Flask · React · M-Pesa Daraja</span>
      </footer>
    </div>
  );
}