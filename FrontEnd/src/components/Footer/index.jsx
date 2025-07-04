import { Container, Subtitle, Paragraph } from './style';

export function Footer() {
  return (
    <Container>
      <div className="content">
        <Subtitle>Junte-se a milhares de clientes e barbeiros que já usam o Barba&Navalha.</Subtitle>
        <Paragraph>© {new Date().getFullYear()} Barba&Navalha. Todos os direitos reservados.</Paragraph>
      </div>
    </Container>
  );
}
