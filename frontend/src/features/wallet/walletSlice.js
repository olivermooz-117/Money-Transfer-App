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

export const mpesaDeposit = createAsyncThunk(
  "wallet/mpesaDeposit",
  async ({ phone, amount }, { rejectWithValue }) => {
    try {
      const res = await api.post("/mpesa/deposit", { phone, amount });
      return res.data;
    } catch (err) {
      return rejectWithValue(err.response?.data?.error || "Could not initiate M-Pesa deposit");
    }
  }
);

export const pollMpesaDeposit = createAsyncThunk(
  "wallet/pollMpesaDeposit",
  async (checkoutRequestId, { rejectWithValue }) => {
    try {
      const res = await api.get(`/mpesa/deposit/${checkoutRequestId}`);
      return res.data;
    } catch (err) {
      return rejectWithValue(err.response?.data?.error || "Could not fetch deposit status");
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
      })
      .addCase(mpesaDeposit.fulfilled, (state, action) => {
        // Store the checkoutRequestId for polling
        state.mpesaDeposit = action.payload.deposit;
      })
      .addCase(pollMpesaDeposit.fulfilled, (state, action) => {
        state.mpesaDeposit = action.payload;
        if (action.payload.status === "success") {
          state.data = action.payload.wallet;
        }
      });
  },
});

export default walletSlice.reducer;
