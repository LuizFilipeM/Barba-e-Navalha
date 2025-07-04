import { Link } from "react-router-dom"

import { Header } from "../../components/Header"
import { Footer } from "../../components/Footer"


export function NotFound() {
  return (
    <>
      <Header links={[
        { label: 'Home', to: '/' },
        { label: 'Login', to: '/enter' },
        { label: 'Cadastre-se', to: '/register' }
      ]} />
        <div>
          <h1>Ops... algo está faltando!</h1>

          <p>A página que você procura não foi encontrada.</p>

          <Link to="/">Vá para a página inicial</Link>
        </div>
      <Footer />
    </>
  )
}
