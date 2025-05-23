import { useState } from "react";
import { useAuth } from "../../hooks/hookAuth";
/*import { useNavigate } from "react-router-dom";*/
/*import { useLocal } from "../../hooks/hookLocal";*/

import { Main, Section, Card, CardHeader, Address, ServicesList, ScheduleSection, ToggleButton, Title } from "./style";

import { Header } from "../../components/Header";
import { Footer } from "../../components/Footer";
import { MOCKED_LOCALS } from "../../hooks/hookLocal";

export function Client() {
  const { signOut } = useAuth();
  /*const navigate = useNavigate();*/
  /*const { allLocals, loading } = useLocal();*/

  const [localSelecionado, setLocalSelecionado] = useState(null);

  const toggleDetalhes = (id) => {
    setLocalSelecionado((prevId) => (prevId === id ? null : id));
  };

  return (
    <>
      <Header
        links={[
          { label: "Home", to: "/" },
          { label: "Pedidos", to: "/" },
          { label: "Perfil", to: "/profile" },
          { label: "Sair", onClick: signOut },
        ]}
      />
      
      <Main>
        <Title>Barbearias disponíveis</Title>
        <Section>
          {MOCKED_LOCALS.map((local) => (
            <Card key={local.id}>
              <CardHeader>{local.nome}</CardHeader>
              <Address>📍 {local.rua}, {local.bairro}, {local.cidade}</Address>
              <p>Telefone: {local.telefone}</p>

              {local.servicos?.length > 0 && (
                <>
                  <h5>Serviços:</h5>
                  <ServicesList>
                    {local.servicos.map((servico, index) => (
                      <li key={index}>
                        {servico.nome} — R$ {servico.price},00
                      </li>
                    ))}
                  </ServicesList>
                </>
              )}

              <ToggleButton onClick={() => toggleDetalhes(local.id)}>
                {localSelecionado === local.id ? "Ocultar horários" : "Ver horários"}
              </ToggleButton>

              {localSelecionado === local.id && (
                <ScheduleSection>
                  <h5>Horários disponíveis:</h5>
                  <ul>
                    {Object.entries(local.horarios).map(([dia, periodos]) => (
                      <li key={dia}>
                        <strong>{dia.charAt(0).toUpperCase() + dia.slice(1)}:</strong> {periodos.join(", ")}
                      </li>
                    ))}
                  </ul>
                </ScheduleSection>
              )}
            </Card>
          ))}
        </Section>
      </Main>


      {/*<div>
        <h3>Locais disponíveis:</h3>
          <ul>
            {allLocals.map((local) => (
              <li key={local.id}>
                {local.nome} 
              </li>
            ))}
          </ul>
      </div> */}

      <Footer />
    </>
  );
}