import React from "react";
import { render, screen, fireEvent } from "@testing-library/react";
import { Provider } from "react-redux";
import { configureStore } from "@reduxjs/toolkit";
import { MemoryRouter } from "react-router-dom";
import authReducer from "../authSlice";
import Login from "../Login";

function renderWithProviders(ui) {
  const store = configureStore({ reducer: { auth: authReducer } });
  return render(
    <Provider store={store}>
      <MemoryRouter>{ui}</MemoryRouter>
    </Provider>
  );
}

test("renders email and password fields and a submit button", () => {
  renderWithProviders(<Login />);
  expect(screen.getByText("Log in", { selector: "h2" })).toBeInTheDocument();
  expect(screen.getByLabelText(/email/i)).toBeInTheDocument();
  expect(screen.getByLabelText(/password/i)).toBeInTheDocument();
});

test("lets the user type into the email field", () => {
  renderWithProviders(<Login />);
  const emailInput = screen.getByLabelText(/email/i);
  fireEvent.change(emailInput, { target: { value: "test@example.com" } });
  expect(emailInput.value).toBe("test@example.com");
});
