import { useState, useEffect } from "react";
import { useAuth } from "../../hooks/hookAuth";

import { Header } from "../../components/Header";
import { Footer } from "../../components/Footer";

import { Container, Content, Title, List, ListItem } from "./style";
import { api } from "../../services/api";

export function Calendar() {
  const { signOut, user } = useAuth();
  const [agendamentos, setAgendamentos] = useState([]);

  useEffect(() => {
    async function fetchAgendamentos() {
      try {
        const response = await api.get("/lista-agenda-barber/", {
          params: {
            barbeiro_id: user.id,
          },
        });
        setAgendamentos(response.data.agendamentos || []);
      } catch (error) {
        console.error("Erro ao buscar agendamentos:", error);
      }
    }

    fetchAgendamentos();
  }, [user.id]);

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
                <strong>🕒 {agendamento.hora} - 📅 {agendamento.data}</strong><br />
                {agendamento.cliente_nome}<br />
                {agendamento.servico_nome}
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

