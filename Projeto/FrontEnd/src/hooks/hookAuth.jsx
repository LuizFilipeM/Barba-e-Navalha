import { useState, useEffect, createContext, useContext } from "react"
import { useNavigate } from "react-router-dom"
import { api } from "../services/api"

const AuthContext = createContext({})

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null)
  const [isAuthenticated, setIsAuthenticated] = useState(false)
  const navigate = useNavigate()

  useEffect(() => {
    const storedUser = localStorage.getItem("user")
    const token = localStorage.getItem("token")
    
    if (storedUser && token) {
      setUser(JSON.parse(storedUser))
      setIsAuthenticated(true)
    }
  }, [])

  async function signIn({ email, password }) {
    const response = await api.post("/api/login/", {
      email,
      password
    })
    
    if (response.data.success === true) {
      const userData = response.data
      const token = userData.token

      setUser(userData)
      setIsAuthenticated(true)

      localStorage.setItem("user", JSON.stringify(userData))
      localStorage.setItem("token", token)

      return { success: true, token }
    } else {
      return { success: false, message: "Credenciais inválidas!" }
    }
  }

  async function signInWithGoogle(token) {
    const response = await api.post("/oauth/login/google-oauth2/", {
      token
    })
    
    if (response.data.success === true) {
      const userData = response.data
      const token = userData.token

      setUser(userData)
      setIsAuthenticated(true)

      localStorage.setItem("user", JSON.stringify(userData))
      localStorage.setItem("token", token)

      return { success: true, token }
    } else {
      return { success: false, message: response.data.message || "Falha no login com Google" }
    }
  }

  function signOut() {
    setUser(null)
    setIsAuthenticated(false)
    localStorage.removeItem("user")
    localStorage.removeItem("token")
    navigate("/")
  }

  return (
    <AuthContext.Provider value={{ 
      user, 
      isAuthenticated, 
      signIn, 
      signInWithGoogle, 
      signOut 
    }}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  return useContext(AuthContext)
}