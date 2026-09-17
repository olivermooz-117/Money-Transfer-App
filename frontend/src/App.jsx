import React from "react";
import { Routes, Route, Navigate } from "react-router-dom";
import Navbar from "./components/Navbar";
import ProtectedRoute from "./components/ProtectedRoute";

import Landing from "./features/home/Landing";
import Login from "./features/auth/Login";
import Register from "./features/auth/Register";
import Dashboard from "./features/wallet/Dashboard";
import AddFunds from "./features/wallet/AddFunds";
import Beneficiaries from "./features/beneficiaries/Beneficiaries";
import SendMoney from "./features/transactions/SendMoney";
import Transactions from "./features/transactions/Transactions";
import AdminUsers from "./features/admin/AdminUsers";
import AdminTransactions from "./features/admin/AdminTransactions";
import AdminAnalytics from "./features/admin/AdminAnalytics";

export default function App() {
  return (
    <>
      <Navbar />
      <Routes>
        <Route path="/" element={<Landing />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />

        <Route path="/dashboard" element={<ProtectedRoute><Dashboard /></ProtectedRoute>} />
        <Route path="/wallet/add-funds" element={<ProtectedRoute><AddFunds /></ProtectedRoute>} />
        <Route path="/beneficiaries" element={<ProtectedRoute><Beneficiaries /></ProtectedRoute>} />
        <Route path="/transactions/send" element={<ProtectedRoute><SendMoney /></ProtectedRoute>} />
        <Route path="/transactions" element={<ProtectedRoute><Transactions /></ProtectedRoute>} />

        <Route path="/admin/users" element={<ProtectedRoute adminOnly><AdminUsers /></ProtectedRoute>} />
        <Route path="/admin/transactions" element={<ProtectedRoute adminOnly><AdminTransactions /></ProtectedRoute>} />
        <Route path="/admin/analytics" element={<ProtectedRoute adminOnly><AdminAnalytics /></ProtectedRoute>} />

        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </>
  );
}