import { useState, useEffect, createContext, useContext } from "react";
import { useNavigate } from "react-router-dom";
import { api } from "../services/api";

const AuthContext = createContext({});

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    const storedUser = localStorage.getItem("user");
    const token = localStorage.getItem("token");
    
    if (storedUser && token) {
      setUser(JSON.parse(storedUser));
      setIsAuthenticated(true);
    }
  }, []);

  const updateUser = (newUserData) => {
    setUser(prevUser => {
      const updatedUser = { ...prevUser, ...newUserData };
      localStorage.setItem("user", JSON.stringify(updatedUser));
      return updatedUser;
    });
  };

  async function signIn({ email, password }) {
    const response = await api.post("/api/login/", { email, password });
    
    if (response.data.success === true) {
      const userData = response.data;
      const token = userData.token;

      updateUser(userData);
      setIsAuthenticated(true);
      localStorage.setItem("token", token);

      return { success: true, token };
    } else {
      return { success: false, message: "Credenciais inválidas!" };
    }
  }

  async function signInWithGoogle(token) {
    try {
      const response = await api.post("/api/google-login/", { token });
      if (response.data.success === true) {
        const userData = response.data.user;
        const token = response.data.token;

        updateUser(userData);
        setIsAuthenticated(true);
        localStorage.setItem("token", token);

        if (response.data.requires_profile_completion) {
          return { 
            success: true, 
            token,
            redirectTo: response.data.redirect_to
          };
        }

        return { success: true, token };
      } else {
        return { success: false, message: response.data.message || "Falha no login com Google" };
      }
    } catch (error) {
      return { 
        success: false, 
        message: error.response?.data?.message || "Erro ao conectar com o servidor" 
      };
    }
  }

  function signOut() {
    setUser(null);
    setIsAuthenticated(false);
    localStorage.removeItem("user");
    localStorage.removeItem("token");
    navigate("/");
  }

  return (
    <AuthContext.Provider value={{ 
      user, 
      isAuthenticated, 
      signIn, 
      signInWithGoogle, 
      signOut,
      updateUser
    }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  return useContext(AuthContext);
}