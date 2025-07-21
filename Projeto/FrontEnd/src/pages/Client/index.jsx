import { useState, useEffect } from "react";
import { useAuth } from "../../hooks/hookAuth";
import { api } from "../../services/api";
import { Link } from "react-router-dom";

import { Main, Section, Card, CardHeader, Address, ServicesList, Title } from "./style";

import { Button } from "../../components/Button";
import { Header } from "../../components/Header";
import { Footer } from "../../components/Footer";

export function Client() {
  const { signOut } = useAuth();

  const [barbearias, setBarbearias] = useState([]);
  const [services, setServices] = useState([]);
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
          {barbearias.map((local) => (
                <Card>
                  <CardHeader key={local.id}>{local.nome_local}</CardHeader>
                  <Address>
                    <p><strong>Endereço:</strong> {local.endereco}</p>
                    <p><strong>Telefone:</strong> {local.telefone}</p>

                    <h4>Alguns Serviços Ofertados:</h4>
                    {services.filter(service => service.local_id === local.id).length > 0 ? (
                      <>
                        {services.filter((service) => service.local_id === local.id).slice(0, 3).map((service) => (
                            <ServicesList key={service.id}>
                              <li>
                                <strong>{service.nome}</strong>: R${service.preco}
                              </li>
                            </ServicesList>
                          ))}
                      </>
                    ) : (
                      <p>
                        Nenhum serviço disponível no momento.
                      </p>
                    )}
                  </Address>
                  {services.filter(service => service.local_id === local.id).length > 0 && horarios.filter(horario => horario.local_nome === local.nome_local).length > 0 ? (
                    <Link to={`/booking/${local.id}`}>
                      <Button title="Agendar"/>
                    </Link>
                  ) : (
                    <a href={`tel:${local.telefone}`}>
                      <Button title="Ligue"/>
                    </a>
                  )}
                </Card>
            ))}
        </Section>
      </Main>
      <Footer />
    </>
  );
}
