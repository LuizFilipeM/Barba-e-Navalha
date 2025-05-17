import { Routes, Route } from "react-router-dom"

import { Client } from "../pages/Client"
import { NotFound } from "../pages/NotFound"

export function RouteClient() {
  return (
    <Routes>
      <Route path="/" element={<Client />} />
      <Route path="*" element={<NotFound />} />
    </Routes>
  )
}
