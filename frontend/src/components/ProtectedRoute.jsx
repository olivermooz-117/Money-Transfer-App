import React from "react";
import { Navigate } from "react-router-dom";
import { useSelector } from "react-redux";

export default function ProtectedRoute({ children, adminOnly = false }) {
  const { user, token } = useSelector((state) => state.auth);

  if (!token || !user) {
    return <Navigate to="/login" replace />;
  }
  if (adminOnly && !user.is_admin) {
    return <Navigate to="/dashboard" replace />;
  }
  return children;
}
