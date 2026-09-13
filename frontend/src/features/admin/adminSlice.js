import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";
import api from "../../api/axios";

export const fetchAllUsers = createAsyncThunk("admin/fetchUsers", async (_, { rejectWithValue }) => {
  try {
    const res = await api.get("/admin/users");
    return res.data;
  } catch (err) {
    return rejectWithValue(err.response?.data?.error || "Could not load users");
  }
});

export const updateUser = createAsyncThunk(
  "admin/updateUser",
  async ({ id, changes }, { rejectWithValue }) => {
    try {
      const res = await api.put(`/admin/users/${id}`, changes);
      return res.data;
    } catch (err) {
      return rejectWithValue(err.response?.data?.error || "Could not update user");
    }
  }
);

export const deleteUser = createAsyncThunk(
  "admin/deleteUser",
  async (id, { rejectWithValue }) => {
    try {
      await api.delete(`/admin/users/${id}`);
      return id;
    } catch (err) {
      return rejectWithValue(err.response?.data?.error || "Could not delete user");
    }
  }
);

export const fetchAllTransactions = createAsyncThunk(
  "admin/fetchTransactions",
  async (_, { rejectWithValue }) => {
    try {
      const res = await api.get("/admin/transactions");
      return res.data;
    } catch (err) {
      return rejectWithValue(err.response?.data?.error || "Could not load transactions");
    }
  }
);

export const fetchAnalytics = createAsyncThunk(
  "admin/fetchAnalytics",
  async (_, { rejectWithValue }) => {
    try {
      const [analyticsRes, trendsRes] = await Promise.all([
        api.get("/admin/analytics"),
        api.get("/admin/profit-trends"),
      ]);
      return { analytics: analyticsRes.data, trends: trendsRes.data };
    } catch (err) {
      return rejectWithValue(err.response?.data?.error || "Could not load analytics");
    }
  }
);

const adminSlice = createSlice({
  name: "admin",
  initialState: {
    users: [],
    transactions: [],
    analytics: null,
    trends: [],
    status: "idle",
    error: null,
  },
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(fetchAllUsers.fulfilled, (state, action) => {
        state.users = action.payload;
      })
      .addCase(updateUser.fulfilled, (state, action) => {
        state.users = state.users.map((u) => (u.id === action.payload.id ? action.payload : u));
      })
      .addCase(deleteUser.fulfilled, (state, action) => {
        state.users = state.users.filter((u) => u.id !== action.payload);
      })
      .addCase(fetchAllTransactions.fulfilled, (state, action) => {
        state.transactions = action.payload;
      })
      .addCase(fetchAnalytics.fulfilled, (state, action) => {
        state.analytics = action.payload.analytics;
        state.trends = action.payload.trends;
      })
      .addMatcher(
        (a) => a.type.endsWith("/rejected") && a.type.startsWith("admin/"),
        (state, action) => {
          state.error = action.payload;
        }
      );
  },
});

export default adminSlice.reducer;
