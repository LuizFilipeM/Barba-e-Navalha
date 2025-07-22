import { Routes, Route} from "react-router-dom"

import { Barber } from "../pages/Barber"
import { BarberShop } from "../pages/Barbershop"
import { Profile } from "../pages/Profile"
import { NotFound } from "../pages/NotFound"
import { Services } from "../pages/Services"
import { Calendar } from "../pages/Calendar"
import { Schedule } from "../pages/Schedule"
import { EditBarbershop } from "../pages/EditBarbershop"
import { GmailAuth } from "../pages/GmailAuth"

export function RouteBarber() {

  return (
    <Routes>
      <Route path="/" element={<Barber /> } />
      <Route path="/profile" element={<Profile />} />
      <Route path="/calendar" element={<Calendar />} />
      <Route path="/barbershop" element={<BarberShop />} />
      <Route path="/services" element={<Services />} />
      <Route path="/schedule" element={<Schedule />} />
      <Route path="/edit-barbershop" element={<EditBarbershop />} />
      <Route path="/pos-login" element={<GmailAuth />} />
      <Route path="*" element={<NotFound />} />
    </Routes>
  )
}

