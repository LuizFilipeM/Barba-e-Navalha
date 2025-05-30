import { Routes, Route } from "react-router-dom"

import { SignIn } from "../pages/SignIn"
import { SignUp } from "../pages/SignUp"
import { NotFound } from "../pages/NotFound"
import { Home } from "../pages/Home"
import { ForgotPassword } from "../pages/ForgotPassword"

export function AuthRoutes() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/enter" element={<SignIn />} />
      <Route path="/forgotPassword" element={<ForgotPassword />} />
      <Route path="/register" element={<SignUp />} />
      <Route path="*" element={<NotFound />} />
    </Routes>
  )
}
