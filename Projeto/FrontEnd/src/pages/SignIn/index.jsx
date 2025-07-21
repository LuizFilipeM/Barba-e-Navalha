import { useState } from "react"
import { Link, useNavigate } from "react-router-dom"
import { api } from "../../services/api"

import { GoogleLogin } from '@react-oauth/google';

import { Header } from "../../components/Header"
import { Input } from "../../components/Input"
import { Button } from "../../components/Button"
import { useAuth } from "../../hooks/hookAuth"
import { Footer } from "../../components/Footer"

import logoBarber from "../../assets/BarbaENavalhaLogoBrancoSemFundo.png"

import { Container, Context, Form, Title, BackLinkWrapper, ImageContainer, HeroImage } from "./style"

export function SignIn() {
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  const { signIn, signInWithGoogle } = useAuth()
  const navigate = useNavigate()

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
    await api.get('/csrf/')
      
    const { credential } = credentialResponse
    const result = await signInWithGoogle(credential)
      
    if (!result.success) {
      alert(`❌ ${result.message}`)
    } else {
      navigate("/")
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
              onError={() => alert("Falha no login com Google")}
              useOneTap
            />

            <BackLinkWrapper style={{ textAlign: "center", marginTop: "1rem" }}>
              <Link to="/">Voltar</Link>
            </BackLinkWrapper>
          </Form>
        </Context>
        <ImageContainer>
          <HeroImage 
            src={logoBarber}
            alt="Barbearia" 
          />
        </ImageContainer>
      </Container>

      <Footer />
    </>
  )
}
