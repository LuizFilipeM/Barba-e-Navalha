import { Routes, Route} from "react-router-dom"

import { Barber } from "../pages/Barber"
import { BarberShop } from "../pages/Barbershop"
import { NotFound } from "../pages/NotFound"

export function RouteBarber() {

  return (
    <Routes>
      <Route path="/" element={<Barber /> } />
      <Route path="/barbershop" element={<BarberShop />} />
      <Route path="*" element={<NotFound />} />
    </Routes>
  )
}

