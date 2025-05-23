import { Routes, Route} from "react-router-dom"

import { Barber } from "../pages/Barber"
import { BarberShop } from "../pages/Barbershop"
import { Profile } from "../pages/Profile"
import { NotFound } from "../pages/NotFound"

export function RouteBarber() {

  return (
    <Routes>
      <Route path="/" element={<Barber /> } />
      <Route path="/barbershop" element={<BarberShop />} />
      <Route path="/profile" element={<Profile />} />
      <Route path="*" element={<NotFound />} />
    </Routes>
  )
}

