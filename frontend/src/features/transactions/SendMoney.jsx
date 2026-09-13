import React, { useEffect, useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { useNavigate } from "react-router-dom";
import { fetchBeneficiaries } from "../beneficiaries/beneficiariesSlice";
import { sendMoney } from "./transactionsSlice";

export default function SendMoney() {
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const { list: beneficiaries } = useSelector((state) => state.beneficiaries);
  const [form, setForm] = useState({ beneficiary_id: "", amount: "" });
  const [error, setError] = useState(null);

  useEffect(() => {
    dispatch(fetchBeneficiaries());
  }, [dispatch]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    const result = await dispatch(
      sendMoney({ beneficiary_id: Number(form.beneficiary_id), amount: Number(form.amount) })
    );
    if (sendMoney.fulfilled.match(result)) {
      navigate("/dashboard");
    } else {
      setError(result.payload);
    }
  };

  return (
    <div className="container">
      <div className="card" style={{ maxWidth: 420, margin: "40px auto" }}>
        <h2>Send money</h2>
        {error && <p className="error">{error}</p>}
        {beneficiaries.length === 0 && (
          <p>You have no beneficiaries yet. Add one first.</p>
        )}
        <form onSubmit={handleSubmit}>
          <label>Beneficiary</label>
          <select
            value={form.beneficiary_id}
            onChange={(e) => setForm({ ...form, beneficiary_id: e.target.value })}
            required
          >
            <option value="">Select a beneficiary</option>
            {beneficiaries.map((b) => (
              <option key={b.id} value={b.id}>{b.name} ({b.account_email})</option>
            ))}
          </select>
          <label>Amount</label>
          <input
            type="number"
            min="1"
            step="0.01"
            value={form.amount}
            onChange={(e) => setForm({ ...form, amount: e.target.value })}
            required
          />
          <button type="submit" disabled={beneficiaries.length === 0}>Send</button>
        </form>
      </div>
    </div>
  );
}
