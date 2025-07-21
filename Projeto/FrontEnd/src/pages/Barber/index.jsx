import { useState, useEffect } from "react";
import { useAuth } from "../../hooks/hookAuth";
import { Link } from "react-router-dom";
import { api } from "../../services/api";
import { Header } from "../../components/Header";
import { Footer } from "../../components/Footer";
import { Container, Context, Title, Paragraph, SubTitle, List, RegisterLink, NotificationTitle, RegisterButtons, RegisterButton, ServiceItem, ScheduleItem } from "./style";

export function Barber() {
  const { signOut, user} = useAuth();
  const [barbearias, setBarbearias] = useState([]);
  const [servicos, setServices] = useState([]);
  const [horarios, setHorarios] = useState([]);

  useEffect(() => {
    async function fetchData() {
        try {
            const [resBarbearias, resServicos, resHorarios] = await Promise.all([
                api.get("/barbershops/"),
                api.get("/list-services/"),
                api.get("/list-schedule/")
            ]);

            setBarbearias(resBarbearias.data.data);
            setServices(resServicos.data.data);
            setHorarios(resHorarios.data.data);
        } catch (error) {
            alert("Erro ao carregar dados.");
            console.error(error);
        }
    }

    fetchData();
  }, []);

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
    <Context>
      {barbearias.filter(local => local.barbeirousuarioid === user.id).length === 0 ? (
        <RegisterLink>
          <NotificationTitle>Você não possui uma barbearia cadastrada!</NotificationTitle>
          <RegisterButtons>
            <RegisterButton to="/barbershop" className="primary">Cadastrar Barbearia</RegisterButton>
          </RegisterButtons>
        </RegisterLink>
      ) : (
        <>
          <Title>Minha barbearia</Title>
          {barbearias.filter(local => local.barbeirousuarioid === user.id).map((local) => (
            <div key={`local-${local.id}`}>
              <Paragraph><strong>Nome:</strong> {local.nome_local}</Paragraph>
              <Paragraph><strong>Endereço:</strong> {local.endereco}</Paragraph>
              <Paragraph><strong>Telefone:</strong> {local.telefone}</Paragraph>
              <Paragraph><strong>CNPJ:</strong> {local.cnpj}</Paragraph>
              
              <Link to="/barbershop">Editar Barbearia</Link> {/*Editar Barbearia*/}

              <SubTitle>Serviços oferecidos:</SubTitle>
                {servicos.filter(servico => servico.local_id === local.id).length > 0 ? (
                  <>
                    <List>
                      {servicos.filter(servico => servico.local_id === local.id).map((service) => (
                        <ServiceItem key={service.id}>
                          <strong>{service.nome}</strong>: {service.descricao} — R${service.preco} — ({service.tempo} min)
                        </ServiceItem>
                      ))}
                    </List>
                    <Link to="/services">Editar Serviços</Link>
                  </>
                ) : (
                  <>
                    <Paragraph>Nenhum serviço cadastrado.</Paragraph>
                    <Link to="/services">Cadastrar Serviços</Link>
                  </>
                )}

              <SubTitle>Horários de funcionamento:</SubTitle>
              {horarios.filter(horario => horario.local_nome === local.nome_local).length > 0  ? (
                <>
                  <>
                    {horarios.filter(horario => horario.local_nome === local.nome_local).map((horario) => (
                      <ScheduleItem key={`horario-${horario.id_horario}`}>
                        <strong>{horario.dia_semana}</strong>
                        <div>
                          <p>{horario.hora_inicio}</p>
                          <p>até {horario.hora_fim}</p>
                        </div>
                      </ScheduleItem>
                    ))}
                  </>
                  <Link to="/schedule">Editar Horários</Link>
                </>
              ) : (
                <>
                  <Paragraph>Nenhum horário cadastrado.</Paragraph>
                  <Link to="/schedule">Cadastrar Horários</Link>
                </>
              )}
            </div>
          ))}
        </>
      )}
    </Context>
    <Footer />
  </Container>
);
}
