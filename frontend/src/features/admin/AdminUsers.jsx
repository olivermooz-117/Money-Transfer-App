import React, { useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import { fetchAllUsers, updateUser, deleteUser } from "./adminSlice";

export default function AdminUsers() {
  const dispatch = useDispatch();
  const { users, error } = useSelector((state) => state.admin);

  useEffect(() => {
    dispatch(fetchAllUsers());
  }, [dispatch]);

  return (
    <div className="container">
      <div className="card">
        <h2>All users (admin)</h2>
        {error && <p className="error">{error}</p>}
        <table>
          <thead>
            <tr><th>Name</th><th>Email</th><th>Balance</th><th>Active</th><th>Admin</th><th></th></tr>
          </thead>
          <tbody>
            {users.map((u) => (
              <tr key={u.id}>
                <td>{u.full_name}</td>
                <td>{u.email}</td>
                <td>{u.wallet?.balance}</td>
                <td>{u.is_active ? "Yes" : "No"}</td>
                <td>{u.is_admin ? "Yes" : "No"}</td>
                <td>
                  <button
                    onClick={() =>
                      dispatch(updateUser({ id: u.id, changes: { is_active: !u.is_active } }))
                    }
                  >
                    {u.is_active ? "Deactivate" : "Activate"}
                  </button>{" "}
                  <button onClick={() => dispatch(deleteUser(u.id))}>Delete</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
