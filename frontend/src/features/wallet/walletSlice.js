import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";
import api from "../../api/axios";

export const fetchWallet = createAsyncThunk("wallet/fetch", async (_, { rejectWithValue }) => {
  try {
    const res = await api.get("/wallet");
    return res.data;
  } catch (err) {
    return rejectWithValue(err.response?.data?.error || "Could not load wallet");
  }
});

export const addFunds = createAsyncThunk(
  "wallet/addFunds",
  async (amount, { rejectWithValue }) => {
    try {
      const res = await api.post("/wallet/add-funds", { amount });
      return res.data;
    } catch (err) {
      return rejectWithValue(err.response?.data?.error || "Could not add funds");
    }
  }
);

const walletSlice = createSlice({
  name: "wallet",
  initialState: { data: null, analytics: null, status: "idle", error: null },
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(fetchWallet.pending, (state) => {
        state.status = "loading";
      })
      .addCase(fetchWallet.fulfilled, (state, action) => {
        state.status = "succeeded";
        state.data = action.payload.wallet;
        state.analytics = action.payload.analytics;
      })
      .addCase(fetchWallet.rejected, (state, action) => {
        state.status = "failed";
        state.error = action.payload;
      })
      .addCase(addFunds.fulfilled, (state, action) => {
        state.data = action.payload.wallet;
      });
  },
});

export default walletSlice.reducer;
