import { useAuth } from "../hooks/hookAuth"

import { RouteClient } from "./routeClient"
import { RouteBarber } from "./routeBarber"
import { AuthRoutes } from "./routeAuth"

export function Routes() {
  const { isAuthenticated, user } = useAuth()

  if (isAuthenticated && user) {
    return Number(user.tipo) === 0 ? <RouteClient /> : <RouteBarber />
  } else {
    return <AuthRoutes />
  }
}
