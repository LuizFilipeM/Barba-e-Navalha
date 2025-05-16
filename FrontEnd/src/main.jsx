import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter } from "react-router-dom";

import { GlobalStyle } from "./styles/globalStyles.js";
import { Routes } from "./router";
import { AuthProvider } from "./hooks/hookAuth";

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <BrowserRouter>
      <AuthProvider>
        <GlobalStyle />
        <Routes />
      </AuthProvider>
    </BrowserRouter>
  </React.StrictMode>
);
