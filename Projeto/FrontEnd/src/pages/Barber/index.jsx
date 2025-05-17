import { useAuth } from "../../hooks/hookAuth";
import { useLocal } from "../../hooks/hookLocal";

import { Header } from "../../components/Header";
import { Footer } from "../../components/Footer";
import { Container, Context, Title, Paragraph, SubTitle, List, RegisterLink } from "./style";

import { Link } from "react-router-dom";

export function Barber() {
  const { signOut } = useAuth();
  const { local, hasLocal } = useLocal();

  return (
    <Container>
      <Header
        links={[
          { label: "Home", to: "/" },
          { label: "Perfil", to: "/" },
          { label: "Sair", onClick: signOut },
        ]}
      />

      {hasLocal ? (
        <Context>
          <Title>Minha barbearia</Title>
          <Paragraph><strong>Nome:</strong> {local.nome}</Paragraph>
          <Paragraph><strong>Endereço:</strong> {local.rua}, {local.bairro}, {local.cidade}</Paragraph>
          <Paragraph><strong>Telefone:</strong> {local.telefone}</Paragraph>

          {local.servicos?.length > 0 && (
            <>
              <SubTitle>Serviços:</SubTitle>
              <List>
                {local.servicos.map((servico, index) => (
                  <li key={index}>
                    {servico.nome} — R$ {servico.price},00
                  </li>
                ))}
              </List>
            </>
          )}

          {local.horarios && (
            <>
              <SubTitle>Horários disponíveis:</SubTitle>
              <List>
                {Object.entries(local.horarios).map(([dia, periodos]) => (
                  <li key={dia}>
                    <strong>{dia.charAt(0).toUpperCase() + dia.slice(1)}:</strong> {periodos.join(", ")}
                  </li>
                ))}
              </List>
            </>
          )}
        </Context>
      ) : (
        <RegisterLink>
          <Link to="/barbershop">Cadastrar barbearia</Link>
        </RegisterLink>
      )}

      <Footer />
    </Container>
  );
}
