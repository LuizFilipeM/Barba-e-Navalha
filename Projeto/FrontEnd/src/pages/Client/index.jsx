import { useState, useEffect } from "react";
import { useAuth } from "../../hooks/hookAuth";
import { api } from "../../services/api";
import { Link } from "react-router-dom";

import {
  Main,
  Section,
  Card,
  CardHeader,
  Address,
  ServicesList,
  Title
} from "./style";

import { Header } from "../../components/Header";
import { Footer } from "../../components/Footer";

export function Client() {
  const { signOut } = useAuth();

  const [barbearias, setBarbearias] = useState([]);
  const [services, setServices] = useState([]);
  const [horarios, setHorarios] = useState([]);

  useEffect(() => {
    async function fetchBarbearias() {
      try {
        const response = await api.get("/barbershops/");
        const locais = response.data.data;
        setBarbearias(locais);

        if (response.data.status === true) {
          console.log("Barbearias carregadas com sucesso!");
        } else {
          alert("Erro: BARBEARIA - " + response.data.message);
        }
      } catch (error) {
        console.error("Erro ao buscar barbearias:", error);
        alert("Erro ao buscar barbearias. Tente novamente mais tarde.");
      }
    }

    async function fetchServices() {
      try {
        const response = await api.get("/list-services/");
        const servicos = response.data.data;
        setServices(servicos);

        if (response.data.status === true) {
          console.log("Serviços carregados com sucesso!");
        } else {
          alert("Erro: SERVIÇOS - " + response.data.message);
        }
      } catch (error) {
        console.error("Erro ao buscar serviços:", error);
        alert("Erro ao buscar serviços. Tente novamente mais tarde.");
      }
    }

    async function fetchHorarios() {
      try {
        const response = await api.get("/list-schedule/");
        const horariosData = response.data.data;
        setHorarios(horariosData);

        if (response.data.status === true) {
          console.log("Horários carregados com sucesso!");
        } else {
          alert("Erro: HORÁRIOS - " + response.data.message);
        }
      } catch (error) {
        console.error("Erro ao buscar horários:", error);
        alert("Erro ao buscar horários. Tente novamente mais tarde.");
      }
    }

    fetchBarbearias();
    fetchServices();
    fetchHorarios();
  }, []);

  return (
    <>
      <Header
        links={[
          { label: "Home", to: "/" },
          { label: "Pedidos", to: "/required" },
          { label: "Perfil", to: "/profile" },
          { label: "Sair", onClick: signOut },
        ]}
      />

      <Main>
        <Title>Barbearias disponíveis</Title>
        <Section>
          {Array.isArray(barbearias) && barbearias.length === 0 ? (
            <p style={{ textAlign: "center", color: "#666" }}>
              Nenhuma barbearia disponível no momento.
            </p>
          ) : (
            barbearias.map((local) => (
              <Link
                to={`/barbearia/${local.id}`}
                key={local.id}
                style={{ textDecoration: "none", color: "inherit" }}
              >
                <Card>
                  <CardHeader>{local.nome_local}</CardHeader>
                  <Address>
                    <p><strong>Endereço:</strong> {local.endereco}</p>
                    <p><strong>Telefone:</strong> {local.telefone}</p>

                    <h4>Serviços:</h4>
                    {services
                      .filter((service) => service.id === local.idservicos)
                      .map((service) => (
                        <ServicesList key={service.id}>
                          <li>
                            <strong>{service.servico}</strong>: {service.descricao} — R${service.preco} ({service.tempo} min)
                          </li>
                        </ServicesList>
                      ))}

                    <h4>Horários:</h4>
                    {horarios
                      .filter((horario) => horario.id_local === local.id)
                      .map((horario) => (
                        <ul key={horario.id}>
                          <li>
                            {horario.dia_semana}: {horario.hora_inicio} - {horario.hora_fim}
                          </li>
                        </ul>
                      ))}
                  </Address>
                </Card>
              </Link>
            ))
          )}
        </Section>
      </Main>

      <Footer />
    </>
  );
}
