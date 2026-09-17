import React from "react";
import { Link, useNavigate } from "react-router-dom";
import { useDispatch, useSelector } from "react-redux";
import { logout } from "../features/auth/authSlice";

export default function Navbar() {
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const { user } = useSelector((state) => state.auth);

  const handleLogout = () => {
    dispatch(logout());
    navigate("/");
  };

  return (
    <div className="navbar">
      <div>
        <Link to={user ? "/dashboard" : "/"} className="nav-brand">
          Money Transfer
        </Link>
        {user && (
          <>
            <Link to="/dashboard">Dashboard</Link>
            <Link to="/beneficiaries">Beneficiaries</Link>
            <Link to="/transactions">Transactions</Link>
            {user.is_admin && (
              <>
                <Link to="/admin/users">Admin: Users</Link>
                <Link to="/admin/transactions">Admin: Transactions</Link>
                <Link to="/admin/analytics">Admin: Analytics</Link>
              </>
            )}
          </>
        )}
      </div>
      <div className="nav-actions">
        {user ? (
          <button type="button" onClick={handleLogout}>
            Log out
          </button>
        ) : (
          <>
            <Link to="/login">Log in</Link>
            <Link to="/register" className="nav-cta">
              Get started
            </Link>
          </>
        )}
      </div>
    </div>
  );
}