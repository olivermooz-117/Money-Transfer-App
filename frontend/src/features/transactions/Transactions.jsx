import React, { useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import { fetchMyTransactions } from "./transactionsSlice";

export default function Transactions() {
  const dispatch = useDispatch();
  const { list, status } = useSelector((state) => state.transactions);

  useEffect(() => {
    dispatch(fetchMyTransactions());
  }, [dispatch]);

  return (
    <div className="container">
      <div className="card">
        <h2>Transaction history</h2>
        {status === "loading" && <p>Loading...</p>}
        <table>
          <thead>
            <tr><th>Date</th><th>Type</th><th>Direction</th><th>Amount</th><th>Fee</th></tr>
          </thead>
          <tbody>
            {list.map((t) => (
              <tr key={t.id}>
                <td>{new Date(t.created_at).toLocaleString()}</td>
                <td>{t.type}</td>
                <td><span className={`badge ${t.direction}`}>{t.direction}</span></td>
                <td>{t.amount}</td>
                <td>{t.fee}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
