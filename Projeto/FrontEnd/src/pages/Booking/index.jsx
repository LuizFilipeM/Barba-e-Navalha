import { useState, useEffect } from "react";
import { useAuth } from "../../hooks/hookAuth";
import { api } from "../../services/api";

import { Main, Section, Card, Title } from "./style";

import { Button } from "../../components/Button";
import { Header } from "../../components/Header";
import { Footer } from "../../components/Footer";

export function Booking() {
  const { signOut, user } = useAuth();

  const [barbearias, setBarbearias] = useState([]);
  const [services, setServices] = useState([]);
  const [horarios, setHorarios] = useState([]);

  const [servicoSelecionado, setServicoSelecionado] = useState("");
  const [diaSelecionado, setDiaSelecionado] = useState("");
  const [horarioSelecionado, setHorarioSelecionado] = useState("");
  const [horariosGerados, setHorariosGerados] = useState([]);

  const barbeariaId = parseInt(window.location.pathname.split('/booking/').pop());

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
        console.log(resHorarios.data.data);
      } catch (error) {
        alert("Erro ao carregar dados.");
        console.error(error);
      }
    }

    fetchData();
  }, []);

  function getCSRFToken() {
    const cookies = document.cookie.split(";");
    for (let cookie of cookies) {
      if (cookie.trim().startsWith("csrftoken=")) {
        return cookie.trim().split("=")[1];
      }
    }
    return null;
  }

  function gerarHorarios(horaInicioStr, horaFimStr) {
      const horarios = [];

      const [hInicio, mInicio] = horaInicioStr.split(":").map(Number);
      const [hFim, mFim] = horaFimStr.split(":").map(Number);

      let minutosInicio = hInicio * 60 + mInicio;
      const minutosFim = hFim * 60 + mFim;

      while (minutosInicio <= minutosFim) {
          const hora = Math.floor(minutosInicio / 60).toString().padStart(2, "0");
          const minuto = (minutosInicio % 60).toString().padStart(2, "0");
          horarios.push(`${hora}:${minuto}`);
          minutosInicio += 10;
      }

      return horarios;
  }

  function handleDiaChange(dia) {
      setDiaSelecionado(dia);
      setHorarioSelecionado("");
      const horarioDia = horarios.find(
          (h) =>
              h.local_nome === barbeariaSelecionada?.nome_local &&
              h.dia_semana === dia
      );
      if (horarioDia) {
          const gerados = gerarHorarios(horarioDia.hora_inicio, horarioDia.hora_fim);
          setHorariosGerados(gerados);
      }
  }

  async function handleAgendamento() {
    if (!servicoSelecionado || !diaSelecionado || !horarioSelecionado) {
      return alert("Preencha todos os campos!");
    }
    const hoje = new Date();
    const diasSemana = ["Domingo", "Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado"];
    const indiceDia = diasSemana.indexOf(diaSelecionado.trim());
    const dataAgendamento = new Date(hoje);
    dataAgendamento.setDate(hoje.getDate() + ((7 + indiceDia - hoje.getDay()) % 7));
    const dataFormatada = dataAgendamento.toISOString().split("T")[0];

    try {
      const data = {
        cliente: user.name,
        barbeiro: barbeariaSelecionada.barbeirousuarioid,
        servico: servicoSelecionado.toString(),
        data: dataFormatada,
        horario: horarioSelecionado
      };
      const response = await api.post("/inserir-agendamento/", data,{
          headers: {
            "X-CSRFToken": getCSRFToken(),
          },
        }
      );
      if (response.data.success) {
        alert("Agendamento inserido com sucesso!✅" + response.data.message);
      } else {
        alert("Erro ao realizar agendamento.❌" + response.data.message);
      }
    } catch (error) {
      alert("Erro ao realizar agendamento.");
      console.error(error);
    }
  }

  const barbeariaSelecionada = barbearias.find(b => b.id === barbeariaId);
  const servicosDaBarbearia = services.filter(s => s.local_id === barbeariaId);
  const diasDisponiveis = horarios.filter(h => h.local_nome === barbeariaSelecionada?.nome_local).map(h => h.dia_semana);

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
        <Title>Agendamento</Title>

        <Section>
          {barbeariaSelecionada && (
            <Card>
              <h2>{barbeariaSelecionada.nome_local}</h2>

              <h3>Serviços</h3>
              {servicosDaBarbearia.map((servico) => (
                <div key={servico.id}>
                  <label>
                    <input
                        type="radio"
                        name="servico"
                        value={servico.id}
                        onChange={() => setServicoSelecionado(servico.id)}
                    />
                    {servico.nome} - R${servico.preco}
                  </label>
                </div>
              ))}

              <label>
                <strong>Dia da semana:</strong><br />
                <select value={diaSelecionado} onChange={(e) => handleDiaChange(e.target.value)}>
                  <option value="">Selecione um dia</option>
                  {[...new Set(diasDisponiveis)].map((dia, index) => (
                      <option key={index} value={dia}>{dia}</option>
                  ))}
                </select>
              </label>

              <br /> <br />

              {horariosGerados.length > 0 ? (
                <label>
                  <strong>Horário:</strong><br />
                  <select value={horarioSelecionado} onChange={(e) => setHorarioSelecionado(e.target.value)}>
                    <option value="">Selecione um horário</option>
                    {horariosGerados.map((hora, index) => (
                        <option key={index} value={hora}>{hora}</option>
                    ))}
                  </select>
                </label>
              ) : (
                <>
                    <strong>Horário:</strong><br />
                    <p>Selecione o Dia da Semana</p>
                </>
              )}
              <div style={{ marginTop: "1rem" }}>
                <Button title="Confirmar Agendamento" onClick={handleAgendamento} />
              </div>
            </Card>
          )}
        </Section>
      </Main>

      <Footer />
    </>
  );
}