import { useState } from "react";
import { useAuth } from "../../hooks/hookAuth";

import { Header } from "../../components/Header";
import { Footer } from "../../components/Footer";

import { Container, Content, Title, List, ListItem } from "./style";

const MOCKED_AGENDAMENTOS = [
  {
    id: 1,
    barbearia: {
      nome: "Barbearia do Zé",
      endereco: "Rua A, Centro, São Paulo",
    },
    data: "2025-06-12",
    horario: "10:00",
  },
  {
    id: 2,
    barbearia: {
      nome: "Barbearia Fina",
      endereco: "Av. B, Jardim, Rio de Janeiro",
    },
    data: "2025-06-13",
    horario: "14:00",
  },
  {
    id: 3,
    barbearia: {
      nome: "Estilo & Corte",
      endereco: "Rua das Flores, Curitiba",
    },
    data: "2025-06-13",
    horario: "16:00",
  },
];

export function Required() {
  const { signOut } = useAuth();
  const [agendamentos] = useState(MOCKED_AGENDAMENTOS);

  return (
    <Container>
      <Header
        links={[
          { label: "Home", to: "/" },
          { label: "Agenda", to: "/calendar" },
          { label: "Perfil", to: "/profile" },
          { label: "Sair", onClick: signOut },
        ]}
      />
      <Content>
        <Title>Meus Pedidos</Title>
        {agendamentos.length > 0 ? (
          <List>
            {agendamentos.map((agendamento) => (
              <ListItem key={agendamento.id}>
                <strong>{agendamento.barbearia.nome}</strong><br />
                📍 {agendamento.barbearia.endereco}<br />
                🕒 {agendamento.horario} - 📅 {agendamento.data}
              </ListItem>
            ))}
          </List>
        ) : (
          <p style={{ textAlign: "center", color: "#666" }}>
            Nenhum pedido encontrado.
          </p>
        )}
      </Content>
      <Footer />
    </Container>
  );
}

