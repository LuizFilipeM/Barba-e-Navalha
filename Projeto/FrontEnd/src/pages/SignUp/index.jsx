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

export function SignUp() {
  const [formData, setFormData] = useState({
    tipo: TipoUsuario.Cliente,
    name: "",
    cpf: "",
    telefone: "",
    cidade: "",
    data_nascimento: "",
    email: "",
    password: "",
  });

  const navigate = useNavigate();

  function handleChange(e) {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  }

  function validarCampos() {
    const campos = [
      { nome: "Nome", valor: formData.name },
      { nome: "CPF", valor: formData.cpf },
      { nome: "Telefone", valor: formData.telefone },
      { nome: "Cidade", valor: formData.cidade },
      { nome: "Data de Nascimento", valor: formData.data_nascimento },
      { nome: "E-mail", valor: formData.email },
      { nome: "Senha", valor: formData.password },
    ];

    for (const campo of campos) {
      if (!campo.valor.trim()) {
        return `Preencha o campo: ${campo.nome}`;
      }
    }

    return null;
  }

  function limparCampos() {
    setFormData({
      tipo: TipoUsuario.Cliente,
      name: "",
      cpf: "",
      telefone: "",
      cidade: "",
      data_nascimento: "",
      email: "",
      password: "",
    });
  }

  async function handleSignUp(e) {
    e.preventDefault();

    const erro = validarCampos();
    if (erro) {
      alert(erro);
      return;
    }

    const dados = {
      ...formData,
      tipo: formData.tipo === TipoUsuario.Cliente ? "Cliente" : "Barbeiro",
      token: btoa(`${formData.email}:${Date.now()}`),
    };

   
    const response = await api.post("/api/cadastro/", dados, {
      headers: { "Content-Type": "application/json" },
    });

    if (response.data.status === true) {
      alert("Cadastro realizado com sucesso! ");
      limparCampos();
      navigate("/");
    } else {
      alert("Erro: " + response.data.msg);
      limparCampos();
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
          <Title>Faça o seu cadastro</Title>

          <Form>
            <label htmlFor="tipo">Tipo de usuário</label>
            <Select id="tipo" name="tipo" value={formData.tipo} onChange={handleChange}>
              <option value={TipoUsuario.Cliente}>Cliente</option>
              <option value={TipoUsuario.Barbeiro}>Barbeiro</option>
            </Select>
            <Input 
              name="name" 
              label="Nome" 
              placeholder="Nome" 
              type="text" value={formData.name} 
              onChange={handleChange} />
            <Input 
              name="cpf" 
              label="CPF" 
              placeholder="CPF" 
              type="number" 
              value={formData.cpf} 
              onChange={handleChange} />
            <Input 
              name="telefone" 
              label="Telefone" 
              placeholder="Telefone" 
              type="number" 
              value={formData.telefone} 
              onChange={handleChange} />
          </Form>
        </Context>
        <Context>
          <Form>
            <Input 
              name="cidade" 
              label="Cidade" 
              placeholder="Cidade" 
              type="text" 
              value={formData.cidade} 
              onChange={handleChange} />
            <Input
              name="data_nascimento"
              label="Data de Nascimento"
              placeholder="DD/MM/AAAA"
              type="date"
              value={formData.data_nascimento}
              onChange={handleChange}
            />
            <Input
              style="padding: 0.5rem 0;"
              name="email" 
              label="E-mail" 
              placeholder="E-mail" 
              type="email" 
              value={formData.email} 
              onChange={handleChange} />
            <Input 
              name="password" 
              label="Senha" 
              placeholder="Senha" 
              type="password" 
              value={formData.password} 
              onChange={handleChange} />

            <Button type="submit" title="Cadastrar" onClick={handleSignUp} />

            <BackLinkWrapper>
              <Link to="/">Voltar</Link>
            </BackLinkWrapper>
          </Form>
        </Context>
      </Container>

      <Footer />
    </>
  );
}

