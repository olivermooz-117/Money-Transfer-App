import React, { useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import { fetchAllTransactions } from "./adminSlice";

export default function AdminTransactions() {
  const dispatch = useDispatch();
  const { transactions } = useSelector((state) => state.admin);

  useEffect(() => {
    dispatch(fetchAllTransactions());
  }, [dispatch]);

  return (
    <div className="container">
      <div className="card">
        <h2>All transactions (admin)</h2>
        <table>
          <thead>
            <tr><th>Date</th><th>Type</th><th>Amount</th><th>Fee</th><th>Status</th></tr>
          </thead>
          <tbody>
            {transactions.map((t) => (
              <tr key={t.id}>
                <td>{new Date(t.created_at).toLocaleString()}</td>
                <td>{t.type}</td>
                <td>{t.amount}</td>
                <td>{t.fee}</td>
                <td>{t.status}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
