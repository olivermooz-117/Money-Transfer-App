import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";
import api from "../../api/axios";

export const fetchBeneficiaries = createAsyncThunk(
  "beneficiaries/fetch",
  async (_, { rejectWithValue }) => {
    try {
      const res = await api.get("/beneficiaries");
      return res.data;
    } catch (err) {
      return rejectWithValue(err.response?.data?.error || "Could not load beneficiaries");
    }
  }
);

export const addBeneficiary = createAsyncThunk(
  "beneficiaries/add",
  async (payload, { rejectWithValue }) => {
    try {
      const res = await api.post("/beneficiaries", payload);
      return res.data;
    } catch (err) {
      return rejectWithValue(err.response?.data?.error || "Could not add beneficiary");
    }
  }
);

export const removeBeneficiary = createAsyncThunk(
  "beneficiaries/remove",
  async (id, { rejectWithValue }) => {
    try {
      await api.delete(`/beneficiaries/${id}`);
      return id;
    } catch (err) {
      return rejectWithValue(err.response?.data?.error || "Could not remove beneficiary");
    }
  }
);

const beneficiariesSlice = createSlice({
  name: "beneficiaries",
  initialState: { list: [], status: "idle", error: null },
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(fetchBeneficiaries.fulfilled, (state, action) => {
        state.list = action.payload;
        state.status = "succeeded";
      })
      .addCase(addBeneficiary.fulfilled, (state, action) => {
        state.list.push(action.payload);
      })
      .addCase(removeBeneficiary.fulfilled, (state, action) => {
        state.list = state.list.filter((b) => b.id !== action.payload);
      })
      .addMatcher(
        (a) => a.type.endsWith("/rejected") && a.type.startsWith("beneficiaries/"),
        (state, action) => {
          state.error = action.payload;
        }
      );
  },
});

export default beneficiariesSlice.reducer;
