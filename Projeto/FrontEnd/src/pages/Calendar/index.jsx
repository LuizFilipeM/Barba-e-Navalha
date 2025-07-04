import { useState } from "react";
import { useAuth } from "../../hooks/hookAuth";

import { Header } from "../../components/Header";
import { Footer } from "../../components/Footer";

import { Container, Content, Title, List, ListItem } from "./style";

const MOCKED_AGENDAMENTOS = [
    {
        id: 1,
        cliente: { name: "João" },
        servico: { name: "Corte de cabelo" },
        horario: "10:00",
        data: "2025-06-12", // ontem
    },
    {
        id: 2,
        cliente: { name: "Maria" },
        servico: { name: "Pintura de unha" },
        horario: "14:00",
        data: "2025-06-11", // antes de ontem
    },
    {
        id: 3,
        cliente: { name: "José" },
        servico: { name: "Massagem" },
        horario: "16:00",
        data: "2025-06-13", // hoje
    },
];

export function Calendar() {
    //const { signOut, user } = useAuth();
    //const [agendamentos, setAgendamentos] = useState([]);
    const { signOut } = useAuth();
    const [agendamentos] = useState(MOCKED_AGENDAMENTOS);
    const dataAtual = new Date().toISOString().split("T")[0];

     const agendamentosHoje = agendamentos.filter(
        (agendamento) => agendamento.data === dataAtual
    );

    /*useEffect(() => {
        api.get(`agendamento/barbeiro/${user.id}`)
            .then(response => {
                setAgendamentos(response.data);
            })
            .catch(error => {
                console.log(error);
            });
    }, [user]);*/

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
                <Title>Agenda</Title>
                {agendamentosHoje.length > 0 ? (
                    <List>
                        {agendamentosHoje.map((agendamento) => (
                            <ListItem key={agendamento.id}>
                                {agendamento.cliente.name} - {agendamento.servico.name} - {agendamento.horario}
                            </ListItem>
                        ))}
                    </List>
                ) : (
                    <p style={{ textAlign: "center", color: "#666" }}>
                        Nenhum agendamento para hoje.
                    </p>
                )}
            </Content>
            <Footer />
        </Container>
    );
}


