import { useState } from "react"
import { Link, useNavigate} from "react-router-dom"
import { api } from "../../services/api"

import { Header } from "../../components/Header"
import { Input } from "../../components/Input"
import { Button } from "../../components/Button"
import { Footer } from "../../components/Footer"

import { Container, Context, Form, Title, BackLinkWrapper } from "./style";

export function ForgotPassword() {
  const [email, setEmail] = useState("")

  const navigate = useNavigate()

  async function handleSignIn(event) {
    event.preventDefault();

    if (!email) {
      return alert("⚠️ Preencha todos os campos!")
    }

    await api.post("/forgotPassword", { email });

    alert("Acesse seu email para recuperar a senha.");
    navigate("/");
  }

  return (
    <>
      <Header links={[
        { label: 'Home', to: '/' },
        { label: 'Login', to: '/enter' },
        { label: 'Cadastre-se', to: '/register' }
      ]} />

      <Container>
        <Context>
          <Title>Recuperar Senha</Title>
          <Form onSubmit={handleSignIn}>
            <Input
              name="email"
              label="E-mail"
              placeholder="E-mail"
              type="email"
              onChange={(e) => setEmail(e.target.value)}
            />
            <Button type="submit" title="Enviar"/> 
            <BackLinkWrapper style={{ textAlign: "center", marginTop: "1rem"}}>
              <Link to="/register">Voltar</Link>
            </BackLinkWrapper>
          </Form>
        </Context>
      </Container>

      <Footer />
    </>
  )
}
