import React, { useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import { Link } from "react-router-dom";
import { fetchWallet } from "./walletSlice";

export default function Dashboard() {
  const dispatch = useDispatch();
  const { data: wallet, analytics, status } = useSelector((state) => state.wallet);
  const { user } = useSelector((state) => state.auth);

  useEffect(() => {
    dispatch(fetchWallet());
  }, [dispatch]);

  return (
    <div className="container">
      <h2>Welcome back, {user?.full_name}</h2>

      <div className="card">
        <p>Wallet balance</p>
        {status === "loading" && <p>Loading...</p>}
        {wallet && (
          <p className="balance">
            {wallet.currency} {wallet.balance.toLocaleString()}
          </p>
        )}
        <Link to="/wallet/add-funds"><button>Add funds</button></Link>{" "}
        <Link to="/transactions/send"><button>Send money</button></Link>
      </div>

      {analytics && (
        <div className="card">
          <h3>Wallet analytics</h3>
          <table>
            <tbody>
              <tr><td>Total sent</td><td>{analytics.total_sent}</td></tr>
              <tr><td>Total received</td><td>{analytics.total_received}</td></tr>
              <tr><td>Transactions (all time)</td><td>{analytics.transaction_count}</td></tr>
              <tr><td>Transactions (last 30 days)</td><td>{analytics.transactions_last_30_days}</td></tr>
            </tbody>
          </table>
        </div>
      )}

      <Link to="/transactions">View transaction history</Link>
    </div>
  );
}
