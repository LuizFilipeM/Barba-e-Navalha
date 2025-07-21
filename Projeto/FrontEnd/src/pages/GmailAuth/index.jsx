import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { api } from "../../services/api";

import { Header } from "../../components/Header";
import { Input } from "../../components/Input";
import { Button } from "../../components/Button";
import { Footer } from "../../components/Footer";

import { Container, Context, Form, Title, Select, BackLinkWrapper } from "./style";

const TipoUsuario = {
  Cliente: "0",
  Barbeiro: "1",
};

export function GmailAuth() {
  const [formData, setFormData] = useState({
    tipo: TipoUsuario.Cliente,  
    cpf: "",
    telefone: "",
    cidade: "",
    data_nascimento: "",
  });

  const [googleUser, setGoogleUser] = useState(null);

  function getCookie(name) {
    return document.cookie
      .split('; ')
      .find(row => row.startsWith(name + '='))
      ?.split('=')[1];
  }

  const navigate = useNavigate();

  function handleChange(e) {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  }

  function validarCampos() {
    const campos = [
      { nome: "CPF", valor: formData.cpf },
      { nome: "Telefone", valor: formData.telefone },
      { nome: "Cidade", valor: formData.cidade },
      { nome: "Data de Nascimento", valor: formData.data_nascimento },
    ];

    for (const campo of campos) {
      if (!campo.valor.trim()) {
        return `Preencha o campo: ${campo.nome}`;
      }
    }

    if (!googleUser) {
      return "Você precisa fazer login com o Google primeiro";
    }

    return null;
  }

  function limparCampos() {
    setFormData({
      tipo: TipoUsuario.Cliente,
      cpf: "",
      telefone: "",
      cidade: "",
      data_nascimento: "",
    });
    setGoogleUser(null);
  }

  async function handleSignUp(e) {
    e.preventDefault();

    const erro = validarCampos();
    if (erro) {
      alert(erro);
      return;
    }
    
    const csrftoken = getCookie('csrftoken');
    
    const dados = {
      ...formData,
      tipo: formData.tipo === TipoUsuario.Cliente ? "Cliente" : "Barbeiro",
      google_id: googleUser.sub,
      email: googleUser.email,
      nome: googleUser.name,
    };

    try {
      const response = await api.post("/cadastro-google/", dados, {
        headers: { 
          "Content-Type": "application/json",
          "X-CSRFToken": csrftoken
        },
      });

      if (response.data.status === true) {
        alert("Cadastro realizado com sucesso! ");
        limparCampos();
        navigate("/");
      } else {
        alert("Erro: " + response.data.message);
      }
    } catch (error) {
      alert("Ocorreu um erro durante o cadastro.");
      console.error(error);
    }
  }

  return (
    <>
      <Header
        links={[
          { label: "Home", to: "/" },
          { label: "Login", to: "/enter" },
          { label: "Cadastre-se", to: "/register" },
        ]}
      />

      <Container>
        <Context>
          <Title>Faça o seu cadastro com Google</Title>

          {!googleUser ? (
            <div id="googleSignInButton" style={{ margin: '20px 0' }}></div>
          ) : (
            <div style={{ margin: '20px 0' }}>
              <p>Logado como: {googleUser.name} ({googleUser.email})</p>
            </div>
          )}

          {googleUser && (
            <Form onSubmit={handleSignUp}>
              <label htmlFor="tipo">Tipo de usuário</label>
              <Select id="tipo" name="tipo" value={formData.tipo} onChange={handleChange}>
                <option value={TipoUsuario.Cliente}>Cliente</option>
                <option value={TipoUsuario.Barbeiro}>Barbeiro</option>
              </Select>

              <Input 
                name="cpf" 
                label="CPF" 
                placeholder="CPF" 
                type="text" 
                value={formData.cpf} 
                onChange={handleChange} 
              />
              <Input 
                name="telefone" 
                label="Telefone" 
                placeholder="Telefone" 
                type="text" 
                value={formData.telefone} 
                onChange={handleChange} 
              />
              <Input 
                name="cidade" 
                label="Cidade" 
                placeholder="Cidade" 
                type="text" 
                value={formData.cidade} 
                onChange={handleChange} 
              />
              <Input
                name="data_nascimento"
                label="Data de Nascimento"
                placeholder="DD/MM/AAAA"
                type="date"
                value={formData.data_nascimento}
                onChange={handleChange}
              />

              <Button type="submit" title="Completar Cadastro" />

              <BackLinkWrapper>
                <Link to="/">Voltar</Link>
              </BackLinkWrapper>
            </Form>
          )}
        </Context>
      </Container>

      <Footer />
    </>
  );
}