import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";
import api from "../../api/axios";

export const fetchMyTransactions = createAsyncThunk(
  "transactions/fetch",
  async (_, { rejectWithValue }) => {
    try {
      const res = await api.get("/transactions");
      return res.data;
    } catch (err) {
      return rejectWithValue(err.response?.data?.error || "Could not load transactions");
    }
  }
);

export const sendMoney = createAsyncThunk(
  "transactions/send",
  async (payload, { rejectWithValue }) => {
    try {
      const res = await api.post("/transactions/send", payload);
      return res.data;
    } catch (err) {
      return rejectWithValue(err.response?.data?.error || "Transfer failed");
    }
  }
);

const transactionsSlice = createSlice({
  name: "transactions",
  initialState: { list: [], status: "idle", error: null },
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(fetchMyTransactions.pending, (state) => {
        state.status = "loading";
      })
      .addCase(fetchMyTransactions.fulfilled, (state, action) => {
        state.status = "succeeded";
        state.list = action.payload;
      })
      .addCase(sendMoney.rejected, (state, action) => {
        state.error = action.payload;
      });
  },
});

export default transactionsSlice.reducer;
