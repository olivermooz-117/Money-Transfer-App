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
    navigate("/login");
  };

  return (
    <div className="navbar">
      <div>
        <Link to="/dashboard">Dashboard</Link>
        {user && (
          <>
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
      <div>
        {user ? (
          <button onClick={handleLogout}>Log out</button>
        ) : (
          <Link to="/login">Log in</Link>
        )}
      </div>
    </div>
  );
}
