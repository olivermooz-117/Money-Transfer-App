import React, { useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { useNavigate } from "react-router-dom";
import { addFunds } from "./walletSlice";

export default function AddFunds() {
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const [amount, setAmount] = useState("");
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    const result = await dispatch(addFunds(Number(amount)));
    if (addFunds.fulfilled.match(result)) {
      navigate("/dashboard");
    } else {
      setError(result.payload);
    }
  };

  return (
    <div className="container">
      <div className="card" style={{ maxWidth: 400, margin: "40px auto" }}>
        <h2>Add funds</h2>
        {error && <p className="error">{error}</p>}
        <form onSubmit={handleSubmit}>
          <label>Amount</label>
          <input
            type="number"
            min="1"
            step="0.01"
            value={amount}
            onChange={(e) => setAmount(e.target.value)}
            required
          />
          <button type="submit">Add funds</button>
        </form>
      </div>
    </div>
  );
}
