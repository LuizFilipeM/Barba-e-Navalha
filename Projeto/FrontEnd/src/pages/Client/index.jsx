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
  const [horariosSelecionados, setHorariosSelecionados] = useState({});
  const [agendamentoSelecionado, setAgendamentoSelecionado] = useState(null);

  const toggleDetalhes = (id) => {
    setLocalSelecionado((prevId) => (prevId === id ? null : id));
    setHorariosSelecionados({});
  };

  const toggleHorario = (dia, horario) => {
    setHorariosSelecionados((prev) => {
      const diaHorarios = prev[dia] || [];
      if (diaHorarios.includes(horario)) {
        // Deselecionar
        return {
          ...prev,
          [dia]: diaHorarios.filter((h) => h !== horario),
        };
      } else {
        // Selecionar
        return {
          ...prev,
          [dia]: [...diaHorarios, horario],
        };
      }
    });
  };

  const abrirModalAgendamento = (local) => {
    setAgendamentoSelecionado({
      local,
      horarios: horariosSelecionados,
    });
    const horarios = Object.entries(agendamentoSelecionado.horarios).map(
      ([dia, horarios]) => `${dia}: ${horarios.join(", ")}`
    );
    alert(
      `Confirme o de Agendamento no local ${agendamentoSelecionado.local.nome} no horario:\n${horarios.join(
        "\n"
      )}`
    );
  };

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
          {MOCKED_LOCALS.map((local) => (
            <Card key={local.id}>
              <CardHeader>{local.nome}</CardHeader>
              <Address>
                📍 {local.rua}, {local.bairro}, {local.cidade}
              </Address>
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
                {localSelecionado === local.id
                  ? "Ocultar horários"
                  : "Ver horários"}
              </ToggleButton>

              {localSelecionado === local.id && (
                <ScheduleSection>
                  <h5>Horários disponíveis:</h5>
                  <ul>
                    {Object.entries(local.horarios).map(([dia, periodos]) => (
                      <li key={dia}>
                        <strong>
                          {dia.charAt(0).toUpperCase() + dia.slice(1)}:
                        </strong>
                        <ul>
                          {periodos.map((horario, i) => (
                            <li key={i}>
                              <label>
                                {` ${horario}`}
                                <select
                                  onChange={(e) =>
                                    toggleHorario(dia, e.target.value)
                                  }
                                  style={{ marginLeft: "1rem" }}
                                >
                                  <option value="">Selecionar</option>
                                  <option value="09:00">09:00</option>
                                  <option value="10:00">10:00</option>
                                  <option value="11:00">11:00</option>
                                  <option value="12:00">12:00</option>
                                  <option value="13:00">13:00</option>
                                  <option value="14:00">14:00</option>
                                  <option value="15:00">15:00</option>
                                  <option value="16:00">16:00</option>
                                  <option value="17:00">17:00</option>
                                  <option value="18:00">18:00</option>
                                  <option value="19:00">19:00</option>
                                  <option value="20:00">20:00</option>
                                </select>
                              </label>
                            </li>
                          ))}
                        </ul>
                      </li>
                    ))}
                  </ul>

                  <button onClick={() => abrirModalAgendamento(local)} style={{ marginTop: "1rem" }}>
                    Agendar selecionados
                  </button>
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