import { Routes, Route } from "react-router-dom";

import { Client } from "../pages/Client"
import { Profile } from "../pages/Profile"
import { NotFound } from "../pages/NotFound"
import { Required } from "../pages/Required"
import { Booking } from "../pages/Booking"

export function RouteClient() {
  return (
    <Routes>
      <Route path="/" element={<Client />} />
      <Route path="/profile" element={<Profile />} />
      <Route path="/required" element={<Required />} />
      <Route path="/booking/:id" element={<Booking />} />
      <Route path="*" element={<NotFound />} />
    </Routes>
  );
}
