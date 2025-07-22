import { useState, useEffect } from "react";
import { useAuth } from "../../hooks/hookAuth";

import { Header } from "../../components/Header";
import { Footer } from "../../components/Footer";

import { Container, Content, Title, List, ListItem, DeleteButton, ClickableAddress } from "./style";
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

  const handleDelete = async (id) => {
    try {
      const response = await api.delete(`/remover-agendamento/`, {
        params: { id: id }
      });
      if (response.data.success) {
        setAgendamentos(agendamentos.filter(agendamento => agendamento.id !== id));
        alert(`Agendamento excluído com sucesso! ✅\n`);
      } else {
        alert(`Erro ao excluir agendamento ❌\n`);
      }
    } catch (error) {
      console.error("Erro ao excluir agendamento:", error);
      if (error.response) {
        alert(`Erro: ${error.response.data.message || 'Não foi possível excluir o agendamento'}`);
      } else {
        alert('Não foi possível se conectar ao servidor. Tente novamente.');
      }
    }
  };

  const handleAddressClick = (mapUrl) => {
    if (mapUrl) {
      window.open(mapUrl, '_blank');
    }
  };

  return (
    <Container>
      <Header
        links={[
          { label: "Home", to: "/" },
          { label: "Agenda", to: "/required" },
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
                <ClickableAddress 
                  onClick={() => handleAddressClick(agendamento.map_url)}
                  title="Clique para ver no mapa"
                >
                  📍 {agendamento.local_endereco}
                </ClickableAddress><br />
                🕒 {agendamento.hora} - 📅 {agendamento.data} <br />
                <DeleteButton onClick={() => handleDelete(agendamento.id)}>
                  Excluir
                </DeleteButton>
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