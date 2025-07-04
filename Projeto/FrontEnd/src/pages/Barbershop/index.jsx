import { useState, useEffect } from "react";
import { api } from "../../services/api";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../../hooks/hookAuth";

import { Input } from "../../components/Input";
import { Button } from "../../components/Button";
import { Header } from "../../components/Header";
import { Footer } from "../../components/Footer";

import { Container, Context, Title, StyledLink } from "./style";

export function BarberShop() {
  const navigate = useNavigate();
  const { signOut} = useAuth();

  const [formData, setFormData] = useState({
    nomeLocal: "",
    rua: "",
    bairro: "",
    cidadeLocal: "",
    cnpj: "",
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
      { nome: "Nome do Local", valor: formData.nomeLocal },
      { nome: "Rua", valor: formData.rua },
      { nome: "Bairro", valor: formData.bairro },
      { nome: "Cidade do Local", valor: formData.cidadeLocal },
      { nome: "CNPJ", valor: formData.cnpj },
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
      nomeLocal: "",
      rua: "",
      bairro: "",
      cidadeLocal: "",
      cnpj: "",
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
      token: token,
    };

    const userId = JSON.parse(localStorage.getItem("user"));

    const response = await api.post(`/locals/${userId.id}`, dados, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });

    if (response.data.success) {
      alert("Cadastro realizado com sucesso! ✅");
      limparCampos();
      navigate("/");
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
        <Title>Faça o cadastro do Local</Title>

        <Input
          placeholder="Nome do Local"
          type="text"
          name="nomeLocal"
          value={formData.nomeLocal}
          onChange={handleChange}
          label="Nome do Local"
        />

        <Input
          placeholder="Rua"
          type="text"
          name="rua"
          value={formData.rua}
          onChange={handleChange}
          label="Rua"
        />

        <Input
          placeholder="Bairro"
          type="text"
          name="bairro"
          value={formData.bairro}
          onChange={handleChange}
          label="Bairro"
        />

        <Input
          placeholder="Cidade"
          type="text"
          name="cidadeLocal"
          value={formData.cidadeLocal}
          onChange={handleChange}
          label="Cidade"
        />

        <Input
          placeholder="CNPJ"
          type="text"
          name="cnpj"
          value={formData.cnpj}
          onChange={handleChange}
          label="CNPJ"
        />

        <Button title="Cadastrar" onClick={handleSignUpBarber} />

        <StyledLink>
          <Link to="/">Voltar</Link>
        </StyledLink>
      </Context>

      <Footer />
    </Container>
  );
}
