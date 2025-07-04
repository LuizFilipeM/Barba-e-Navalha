import { useState, useEffect } from "react";
import { useAuth } from "../../hooks/hookAuth";
import { Link } from "react-router-dom";
import { api } from "../../services/api";

import { Button } from "../../components/Button";
import { Input } from "../../components/Input";
import { Header } from "../../components/Header";
import { Footer } from "../../components/Footer";

import {
  Container,
  Context,
  Title,
  DayContainer,
  StyledLink,
  DiaButton,
  ButtonsWrapper,
  IntervaloBox,
} from "./style";

const diasDaSemana = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"];

export function Schedule() {
  const { signOut, user } = useAuth();

  const [horarios, setHorarios] = useState({});
  const [diaSelecionado, setDiaSelecionado] = useState(null);
  const [token, setToken] = useState("");

  useEffect(() => {
    const tokenUser = localStorage.getItem("token");
    if (tokenUser) setToken(tokenUser);
  }, []);

  function handleSelecionarDia(dia) {
    setDiaSelecionado(dia);
    if (!horarios[dia]) {
      setHorarios((prev) => ({
        ...prev,
        [dia]: {
          horaInicio: "",
          horaFim: "",
          intervalos: [],
        },
      }));
    }
  }

  function handleChangeDia(campo, valor) {
    setHorarios((prev) => ({
      ...prev,
      [diaSelecionado]: {
        ...prev[diaSelecionado],
        [campo]: valor,
      },
    }));
  }

  function handleAddIntervalo() {
    setHorarios((prev) => ({
      ...prev,
      [diaSelecionado]: {
        ...prev[diaSelecionado],
        intervalos: [
          ...prev[diaSelecionado].intervalos,
          { inicio: "", duracao: "" },
        ],
      },
    }));
  }

  function handleRemoveIntervalo(index) {
    setHorarios((prev) => {
      const novosIntervalos = [...prev[diaSelecionado].intervalos];
      novosIntervalos.splice(index, 1);
      return {
        ...prev,
        [diaSelecionado]: {
          ...prev[diaSelecionado],
          intervalos: novosIntervalos,
        },
      };
    });
  }

  function handleChangeIntervalo(index, campo, valor) {
    setHorarios((prev) => {
      const novosIntervalos = [...prev[diaSelecionado].intervalos];
      novosIntervalos[index][campo] = valor;
      return {
        ...prev,
        [diaSelecionado]: {
          ...prev[diaSelecionado],
          intervalos: novosIntervalos,
        },
      };
    });
  }

  function validarCampos() {
    const diasSelecionados = Object.keys(horarios);
    if (diasSelecionados.length === 0) return "Selecione ao menos um dia.";

    for (const dia of diasSelecionados) {
      const dados = horarios[dia];
      if (!dados?.horaInicio?.trim() || !dados?.horaFim?.trim()) {
        return `Preencha o horário de início e fim para ${dia}.`;
      }

      for (const [index, intervalo] of dados.intervalos.entries()) {
        if (!intervalo.inicio || !intervalo.duracao) {
          return `Preencha todos os campos dos intervalos (${index + 1}) de ${dia}.`;
        }
      }
    }

    if (!token) return "Usuário não autenticado.";
    return null;
  }

  async function handleSignUpSchedule() {
    const erro = validarCampos();
    if (erro) {
      alert(erro);
      return;
    }

    try {
      const response = await api.post(
        `/schedule/${user.id}/`,
        { horarios, token },
        { headers: { Authorization: `Bearer ${token}` } }
      );

      if (response.data.status === true) {
        alert("Cadastro realizado com sucesso! ✅");
        setHorarios({});
        setDiaSelecionado(null);
      } else {
        alert("Erro: " + response.data.message);
      }
    } catch (error) {
      alert("Erro na requisição: " + error.message);
    }
  }

  return (
    <Container>
      <Header
        links={[
          { label: "Home", to: "/" },
          { label: "Perfil", to: "/profile" },
          { label: "Sair", onClick: signOut },
        ]}
      />

      <Context>
        <Title>Horários de Atendimento</Title>

        <div style={{ marginBottom: "20px" }}>
          {diasDaSemana.map((dia) => (
            <div key={dia} style={{ marginBottom: "8px" }}>
              <strong>{dia}:</strong>{" "}
              {horarios[dia] && horarios[dia].horaInicio && horarios[dia].horaFim ? (
                <span>
                  {horarios[dia].horaInicio} - {horarios[dia].horaFim}
                  {horarios[dia].intervalos.length > 0 &&
                    horarios[dia].intervalos.map(
                      (i, index) => ` (Intervalo ${index + 1}: ${i.inicio} - ${i.duracao} min)`
                    )}
                </span>
              ) : (
                <span style={{ color: "red" }}>Não vai atender</span>
              )}
            </div>
          ))}
        </div>

        {diaSelecionado === null ? (
          <>
            <h3>Selecione os dias de atendimento:</h3>
            <ButtonsWrapper>
              {diasDaSemana.map((dia) => (
                <DiaButton
                  key={dia}
                  title={dia}
                  onClick={() => handleSelecionarDia(dia)}
                  ativo={!!horarios[dia]}
                >
                  {dia}
                </DiaButton>
              ))}
            </ButtonsWrapper>
            <Button title="Cadastrar" onClick={handleSignUpSchedule} />
            <StyledLink>
              <Link to="/">Voltar</Link>
            </StyledLink>
          </>
        ) : (
          <>
            <DayContainer>
              <h4>{diaSelecionado}</h4>
              <Input
                placeholder="Horário de Abertura"
                type="time"
                value={horarios[diaSelecionado]?.horaInicio || ""}
                onChange={(e) => handleChangeDia("horaInicio", e.target.value)}
                label="Horário de Abertura"
              />
              <Input
                placeholder="Horário de Fechamento"
                type="time"
                value={horarios[diaSelecionado]?.horaFim || ""}
                onChange={(e) => handleChangeDia("horaFim", e.target.value)}
                label="Horário de Fechamento"
              />

              <h5>Intervalos</h5>
              {horarios[diaSelecionado]?.intervalos.map((intervalo, index) => (
                <IntervaloBox key={index}>
                  <Input
                    type="time"
                    value={intervalo.inicio}
                    onChange={(e) => handleChangeIntervalo(index, "inicio", e.target.value)}
                    label="Início do Intervalo"
                  />
                  <Input
                    type="number"
                    value={intervalo.duracao}
                    onChange={(e) => handleChangeIntervalo(index, "duracao", e.target.value)}
                    label="Duração (min)"
                  />
                  <Button title="Remover Intervalo" onClick={() => handleRemoveIntervalo(index)} />
                </IntervaloBox>
              ))}
              <Button title="Adicionar Intervalo" onClick={handleAddIntervalo} />
            </DayContainer>

            <Button title="Voltar" onClick={() => setDiaSelecionado(null)} />
          </>
        )}
      </Context>

      <Footer />
    </Container>
  );
}
