import { useState } from "react"
import { Link, useNavigate} from "react-router-dom"

import { Header } from "../../components/Header"
import { Input } from "../../components/Input"
import { Button } from "../../components/Button"
import { useAuth } from "../../hooks/hookAuth"
import { Footer } from "../../components/Footer"

import { Container, Context, Form, Title, BackLinkWrapper } from "./style";

export function SignIn() {
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  const { signIn } = useAuth()

  const navigate = useNavigate()

  async function handleSignIn(event) {
    event.preventDefault();

    if (!email || !password) {
      return alert("⚠️ Preencha todos os campos!")
    }

    const result = await signIn({ email, password })

    if (!result.success) {
      return alert(`❌ ${result.message}`)
    }

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
            <Button type="submit" title="Entrar" />
            <BackLinkWrapper>
              <Link to="/">Voltar</Link>
            </BackLinkWrapper>
          </Form>
        </Context>
      </Container>

      <Footer />
    </>
  )
}
