import React, { useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import { fetchAnalytics } from "./adminSlice";

export default function AdminAnalytics() {
  const dispatch = useDispatch();
  const { analytics, trends } = useSelector((state) => state.admin);

  useEffect(() => {
    dispatch(fetchAnalytics());
  }, [dispatch]);

  return (
    <div className="container">
      {analytics && (
        <div className="card">
          <h2>Platform analytics</h2>
          <table>
            <tbody>
              <tr><td>Total users</td><td>{analytics.total_users}</td></tr>
              <tr><td>Total wallet balance</td><td>{analytics.total_wallet_balance}</td></tr>
              <tr><td>Total transfer volume</td><td>{analytics.total_transfer_volume}</td></tr>
              <tr><td>Total fees collected</td><td>{analytics.total_fees_collected}</td></tr>
            </tbody>
          </table>
        </div>
      )}

      <div className="card">
        <h3>Monthly profit trend (fee revenue)</h3>
        <table>
          <thead><tr><th>Year</th><th>Month</th><th>Fees</th><th># Transactions</th></tr></thead>
          <tbody>
            {trends.map((row) => (
              <tr key={`${row.year}-${row.month}`}>
                <td>{row.year}</td>
                <td>{row.month}</td>
                <td>{row.total_fees}</td>
                <td>{row.transaction_count}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
