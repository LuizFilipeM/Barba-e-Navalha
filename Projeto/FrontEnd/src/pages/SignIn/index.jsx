import { useState, useEffect } from "react"
import { Link, useNavigate } from "react-router-dom"
import { GoogleLogin } from '@react-oauth/google';
import { api } from "../../services/api"

import { Header } from "../../components/Header"
import { Input } from "../../components/Input"
import { Button } from "../../components/Button"
import { useAuth } from "../../hooks/hookAuth"
import { Footer } from "../../components/Footer"

import { Container, Context, Form, Title, BackLinkWrapper } from "./style"

import { jwtDecode } from 'jwt-decode'

export function SignIn() {
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  const { signIn } = useAuth()
  const navigate = useNavigate()

  useEffect(() => {
    carregarCsrfToken()
  }, [])

  function getCookie(name) {
    let cookieValue = null
    if (document.cookie && document.cookie !== "") {
      const cookies = document.cookie.split(";")
      for (let cookie of cookies) {
        cookie = cookie.trim()
        if (cookie.startsWith(name + "=")) {
          cookieValue = decodeURIComponent(cookie.slice(name.length + 1))
          break
        }
      }
    }
    return cookieValue
  }

  async function carregarCsrfToken() {
  try {
    await api.get("/csrf/", { withCredentials: true }); // Axios precisa disso
    const token = getCookie("csrftoken");
    if (token) {
      alert("CSRF cookie carregado: " + token);
    } else {
      alert("CSRF cookie ainda está ausente após o GET.");
    }
  } catch (err) {
    console.error("Erro ao carregar CSRF token:", err);
  }
}

  async function handleSignIn(event) {
    event.preventDefault()

    if (!email || !password) {
      return alert("⚠️ Preencha todos os campos!")
    }

    const result = await signIn({ email, password })

    if (!result.success) {
      return alert(`❌ ${result.message}`)
    }

    navigate("/")
  }

  const handleLoginSuccess = async (credentialResponse) => {
    const { credential } = credentialResponse

    try {
      const csrfToken = getCookie("csrftoken")
      const response = await api.post("/api/google-login/", {
      token: credential, 
      
});

      if (response.data.success) {

        const data = response.data
        localStorage.setItem("token", data.token)

        if(data.user.tipo === null){
          navigate("/pos-login")
        }
      } else {
        console.error("Erro ao autenticar com o backend")
      }
    } catch (error) {
      console.error("Erro na requisição de login:", error)
    }
  }

  return (
    <>
      <Header
        links={[
          { label: "Home", to: "/" },
          { label: "Login", to: "/enter" },
          { label: "Cadastre-se", to: "/register" },
        ]}
      />

      <Container>
        <Context>
          <Title>Faça o seu login</Title>
          <Form onSubmit={handleSignIn}>
            <Input
              name="email"
              label="E-mail"
              placeholder="E-mail"
              type="email"
              onChange={(e) => setEmail(e.target.value)}
            />
            <Input
              name="password"
              label="Senha"
              placeholder="Senha"
              type="password"
              onChange={(e) => setPassword(e.target.value)}
            />

            <BackLinkWrapper>
              <Link to="/forgotPassword">Esqueceu a senha?</Link>
            </BackLinkWrapper>

            <Button type="submit" title="Entrar" />

            <GoogleLogin
              onSuccess={handleLoginSuccess}
              onError={() => console.log("Login com Google falhou")}
            />

            <BackLinkWrapper style={{ textAlign: "center", marginTop: "1rem" }}>
              <Link to="/">Voltar</Link>
            </BackLinkWrapper>
          </Form>
        </Context>
      </Container>

      <Footer />
    </>
  )
}
