import React from "react";
import ReactDOM from "react-dom/client";
import { GoogleOAuthProvider } from '@react-oauth/google';
import { BrowserRouter } from "react-router-dom";

import { GlobalStyle } from "./styles/globalStyles.js";
import { Routes } from "./router";
import { AuthProvider } from "./hooks/hookAuth";

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <BrowserRouter>
      <AuthProvider>
        <GoogleOAuthProvider clientId='483286834912-9clasapa8op0ftt23sur6dr25fjdff2l.apps.googleusercontent.com'>
          <GlobalStyle />
          <Routes />
        </GoogleOAuthProvider>
      </AuthProvider>
    </BrowserRouter>
  </React.StrictMode>
);
