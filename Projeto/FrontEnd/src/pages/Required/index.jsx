import { useState, useEffect } from "react";
import { useAuth } from "../../hooks/hookAuth";

import { Header } from "../../components/Header";
import { Footer } from "../../components/Footer";

import { Container, Content, Title, List, ListItem } from "./style";
import { api } from "../../services/api";

export function Required() {
  const { signOut, user } = useAuth();
  const [agendamentos, setAgendamentos] = useState([]);

  useEffect(() => {
    async function fetchAgendamentos() {
      try {
        const response = await api.get("/listar-agendamentos/", {
          params: {
            cliente: user.name.trim(),
          },
        });
        setAgendamentos(response.data.agendamentos || []);
      } catch (error) {
        console.error("Erro ao buscar agendamentos:", error);
      }
    }

    fetchAgendamentos();
  }, [user.name]);

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
                <strong>Barbearia: {agendamento.local_nome}</strong><br />
                📍 {agendamento.local_endereco}<br />
                🕒 {agendamento.hora} - 📅 {agendamento.data}
              </ListItem>
            ))}
          </List>
        ) : (
          <p style={{ textAlign: "center", color: "#666" }}>
            Nenhum agendamento encontrado.
          </p>
        )}
      </Content>
      <Footer />
    </Container>
  );
}

