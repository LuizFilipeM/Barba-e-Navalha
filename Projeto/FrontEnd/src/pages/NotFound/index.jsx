import { useNavigate } from "react-router-dom"

import image404 from "../../assets/page404.png"
import { Container, Content } from "./style"

import { Header } from "../../components/Header"
import { Button } from "../../components/Button"
import { Footer } from "../../components/Footer"


export function NotFound() {
  const navigate = useNavigate()

  async function handleClick() {
    navigate("/")
  }

  return (
    <Container>
      <Header links={[
        { label: 'Home', to: '/' },
        { label: 'Login', to: '/enter' },
        { label: 'Cadastre-se', to: '/register' }
      ]} />
      <Content>
        <img src={image404} alt="Imagem de um robó quebrado com os números 404" />
        <div>
          <h1>Ops... algo está faltando!</h1>
          <p>A página que você procura não foi encontrada.</p>
        </div>
        <Button type="submit" title="Voltar para a Home" onClick={handleClick} />
      </Content>
      <Footer />
    </Container>
  )
}
