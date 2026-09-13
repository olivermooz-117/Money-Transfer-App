import React, { useEffect, useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { fetchBeneficiaries, addBeneficiary, removeBeneficiary } from "./beneficiariesSlice";

export default function Beneficiaries() {
  const dispatch = useDispatch();
  const { list, error } = useSelector((state) => state.beneficiaries);
  const [form, setForm] = useState({ name: "", account_email: "" });

  useEffect(() => {
    dispatch(fetchBeneficiaries());
  }, [dispatch]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    const result = await dispatch(addBeneficiary(form));
    if (addBeneficiary.fulfilled.match(result)) {
      setForm({ name: "", account_email: "" });
    }
  };

  return (
    <div className="container">
      <div className="card">
        <h2>Beneficiaries</h2>
        {error && <p className="error">{error}</p>}
        <form onSubmit={handleSubmit}>
          <label>Name</label>
          <input
            value={form.name}
            onChange={(e) => setForm({ ...form, name: e.target.value })}
            required
          />
          <label>Their account email</label>
          <input
            type="email"
            value={form.account_email}
            onChange={(e) => setForm({ ...form, account_email: e.target.value })}
            required
          />
          <button type="submit">Add beneficiary</button>
        </form>
      </div>

      <div className="card">
        <table>
          <thead>
            <tr><th>Name</th><th>Email</th><th></th></tr>
          </thead>
          <tbody>
            {list.map((b) => (
              <tr key={b.id}>
                <td>{b.name}</td>
                <td>{b.account_email}</td>
                <td>
                  <button onClick={() => dispatch(removeBeneficiary(b.id))}>Remove</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
