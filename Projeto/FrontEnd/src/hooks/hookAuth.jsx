import { useState, useEffect, createContext, useContext } from "react"
import { useNavigate } from "react-router-dom"
import { api } from "../services/api"

const AuthContext = createContext({})

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null)
  const [isAuthenticated, setIsAuthenticated] = useState(false)
  const navigate = useNavigate()

  /*const mockUsers = [
    {
      id: 1,
      tipo: "Cliente", // Cliente
      name: "João",
      cpf: "12345678901",
      telefone: "11999999999",
      cidade: "Rio de Janeiro",
      data_nascimento: "2000-01-01",
      email: "cliente@email.com",
      password: "123456",
    },
    {
      id: 2,
      tipo: "Barbeiro", // Barbeiro
      name: "Maria",
      cpf: "12345678902",
      telefone: "11999999998",
      cidade: "Rio de Janeiro",
      data_nascimento: "2000-01-01",
      email: "barbeiro@email.com",
      password: "123456",
    }
  ]*/

  useEffect(() => {
    const storedUser = localStorage.getItem("user")
    const token = localStorage.getItem("token")
    
    if (storedUser && token) {
      setUser(JSON.parse(storedUser))
      setIsAuthenticated(true)
    }
  }, [])

  
  /*async function signIn({ email, password }) {
    const foundUser = mockUsers.find(
      user => user.email === email && user.password === password
    )

    if (foundUser) {
      const token = btoa(`${email}:${Date.now()}`)

      setUser(foundUser)
      setIsAuthenticated(true)

      localStorage.setItem("user", JSON.stringify(foundUser))
      localStorage.setItem("token", token)

      return { success: true, token }
    }

    const userExists = mockUsers.find(user => user.email === email)
    if (userExists) {
      return { success: false, message: "Senha incorreta!" }
    }

    return { success: false, message: "E-mail não encontrado!" }
  }*/

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

  function signOut() {
    setUser(null)
    setIsAuthenticated(false)
    localStorage.removeItem("user")
    localStorage.removeItem("token")
    navigate("/")
  }


  return (
    <AuthContext.Provider value={{ user, isAuthenticated, signIn, signOut }}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  return useContext(AuthContext)
}

