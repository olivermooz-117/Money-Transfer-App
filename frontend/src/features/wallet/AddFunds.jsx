import React, { useState, useEffect, useRef } from "react";
import { useDispatch, useSelector } from "react-redux";
import { useNavigate } from "react-router-dom";
import { mpesaDeposit, pollMpesaDeposit, fetchWallet } from "./walletSlice";

export default function AddFunds() {
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const [amount, setAmount] = useState("");
  const [phone, setPhone] = useState("");
  const [error, setError] = useState(null);
  const [message, setMessage] = useState(null);
  const [isPolling, setIsPolling] = useState(false);

  const { mpesaDeposit: deposit, status } = useSelector((state) => state.wallet);
  const pollIntervalRef = useRef(null);

  // Cleanup on unmount
  useEffect(() => {
    return () => {
      if (pollIntervalRef.current) {
        clearInterval(pollIntervalRef.current);
      }
    };
  }, []);

  const startPolling = (checkoutRequestId) => {
    setIsPolling(true);
    pollIntervalRef.current = setInterval(async () => {
      const result = await dispatch(pollMpesaDeposit(checkoutRequestId));
      if (pollMpesaDeposit.fulfilled.match(result)) {
        const data = result.payload;
        if (data.status === "success") {
          clearInterval(pollIntervalRef.current);
          pollIntervalRef.current = null;
          setIsPolling(false);
          setMessage("Wallet topped up successfully!");
          // Refresh wallet data
          await dispatch(fetchWallet());
          setTimeout(() => navigate("/dashboard"), 1500);
        } else if (data.status === "failed") {
          clearInterval(pollIntervalRef.current);
          pollIntervalRef.current = null;
          setIsPolling(false);
          setError(data.result_desc || "M-Pesa deposit failed");
        }
      } else if (pollMpesaDeposit.rejected.match(result)) {
        clearInterval(pollIntervalRef.current);
        pollIntervalRef.current = null;
        setIsPolling(false);
        setError(result.payload);
      }
    }, 3000);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    setMessage(null);

    if (!phone.trim()) {
      setError("Phone number is required");
      return;
    }
    if (!amount || Number(amount) <= 0) {
      setError("Amount must be a positive number");
      return;
    }
    if (Number(amount) < 1) {
      setError("Amount must be at least 1");
      return;
    }

    const result = await dispatch(mpesaDeposit({ phone: phone.trim(), amount: Number(amount) }));
    if (mpesaDeposit.fulfilled.match(result)) {
      const data = result.payload;
      setMessage(data.message || "Check your phone and enter M-Pesa PIN");
      startPolling(data.deposit.checkout_request_id);
    } else {
      setError(result.payload);
    }
  };

  const isSubmitting = status === "loading" || isPolling;

  return (
    <div className="container">
      <div className="card" style={{ maxWidth: 400, margin: "40px auto" }}>
        <h2>Add funds via M-Pesa</h2>
        {error && <p className="error">{error}</p>}
        {message && !isPolling && <p className="success">{message}</p>}
        {isPolling && <p className="info">Waiting for M-Pesa confirmation...</p>}
        <form onSubmit={handleSubmit}>
          <label>Phone Number</label>
          <input
            type="tel"
            placeholder="07XXXXXXXX or 2547XXXXXXXX"
            value={phone}
            onChange={(e) => setPhone(e.target.value)}
            required
            disabled={isSubmitting}
          />
          <label>Amount (KES)</label>
          <input
            type="number"
            min="1"
            step="0.01"
            value={amount}
            onChange={(e) => setAmount(e.target.value)}
            required
            disabled={isSubmitting}
          />
          <button type="submit" disabled={isSubmitting}>
            {isPolling ? "Waiting for confirmation..." : isSubmitting ? "Processing..." : "Send STK Push"}
          </button>
        </form>
      </div>
    </div>
  );
}
