import { useState, useEffect } from "react";
import { api } from "../../services/api";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../../hooks/hookAuth";

import { Input } from "../../components/Input";
import { Button } from "../../components/Button";
import { Header } from "../../components/Header";
import { Footer } from "../../components/Footer";

import { Container, Context, Title, StyledLink } from "./style";

export function Services() {
  const navigate = useNavigate();
  const { signOut } = useAuth();

  const [formData, setFormData] = useState({
    nomeServico: "",
    descricao: "",
    preco: "",
    duracao: "",
  });

  const [token, setToken] = useState("");

  useEffect(() => {
    const tokenUser = localStorage.getItem("token");
    if (tokenUser) {
      setToken(tokenUser);
    }
  }, []);

  function handleChange(e) {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  }

  function validarCampos() {
    const campos = [
      { nome: "Nome do Serviço", valor: formData.nomeServico},
      { nome: "Preço", valor: formData.preco},
      { nome: "Duração", valor: formData.duracao},
    ];

    for (const campo of campos) {
      if (!campo.valor.trim()) {
        return `Preencha o campo: ${campo.nome}`;
      }
    }

    if (!token) {
      return "Usuário não autenticado.";
    }

    return null;
  }

  function limparCampos() {
    setFormData({
        nomeServico: "",
        descricao: "",
        preco: "",
        duracao: "",
    });
  }

  async function handleSignUpBarber() {
    const erro = validarCampos();
    if (erro) {
      alert(erro);
      return;
    }

    const dados = {
      ...formData,
      descricao: formData.descricao || null,
      token: token,
    };

    const response = await api.post("/services", dados, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });

    if (response.data.success) {
      alert("Cadastro realizado com sucesso! ✅");
      limparCampos();
      navigate("/services");
    } else {
      alert("Erro: " + response.data.message);
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
        <Title>Faça o cadastro dos Serviços</Title>

        <Input
          placeholder="Nome do Serviço"
          type="text"
          name="nomeServico"
          value={formData.nomeServico}
          onChange={handleChange}
          label="Nome do Serviço"
        />

        <Input
          placeholder="Descrição"
          type="text"
          name="descricao"
          value={formData.descricao}
          onChange={handleChange}
          label="Descrição"
        />

        <Input
          placeholder="Preço"
          type="text"
          name="preco"
          value={formData.preco}
          onChange={handleChange}
          label="Preço"
        />

        <Input
          placeholder="Duração"
          type="text"
          name="duracao"
          value={formData.duracao}
          onChange={handleChange}
          label="Duração"
        />

        <Button title="Adicionar outro Serviço" onClick={handleSignUpBarber} />

        <StyledLink>
          <Link to="/">Voltar</Link>
        </StyledLink>
      </Context>

      <Footer />
    </Container>
  );
}
