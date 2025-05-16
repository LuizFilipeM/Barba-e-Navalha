import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { api } from "../../services/api";

import { Header } from "../../components/Header";
import { Input } from "../../components/Input";
import { Button } from "../../components/Button";
import { Footer } from "../../components/Footer";

import { Container, Context, Form, Title, Select, BackLinkWrapper } from "./style";

export function SignUp() {
  const [formData, setFormData] = useState({
    tipo: "0",
    name: "",
    cpf: "",
    telefone: "",
    cidade: "",
    dataNascimento: "",
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
      { nome: "Data de Nascimento", valor: formData.dataNascimento },
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
      tipo: "0",
      name: "",
      cpf: "",
      telefone: "",
      cidade: "",
      dataNascimento: "",
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
      token: btoa(`${formData.email}:${Date.now()}`),
    };

    try {
      await api.post("/api/cadastro/", dados, {
        headers: { "Content-Type": "application/json" },
      });

      alert("Cadastro realizado com sucesso! ✅");
      limparCampos();
      navigate("/");
    } catch (erro) {
      const msg = erro.response?.data?.message || "Erro ao cadastrar usuário!";
      alert(`Erro: ${msg}`);
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

          <Form onSubmit={handleSignUp}>
            <label htmlFor="tipo">Tipo de usuário</label>
            <Select id="tipo" name="tipo" value={formData.tipo} onChange={handleChange}>
              <option value="0">Cliente</option>
              <option value="1">Barbeiro</option>
            </Select>

            <Input name="name" label="Nome" placeholder="Nome" type="text" value={formData.name} onChange={handleChange} />
            <Input name="cpf" label="CPF" placeholder="CPF" type="text" value={formData.cpf} onChange={handleChange} />
            <Input name="telefone" label="Telefone" placeholder="Telefone" type="text" value={formData.telefone} onChange={handleChange} />
            <Input name="cidade" label="Cidade" placeholder="Cidade" type="text" value={formData.cidade} onChange={handleChange} />
            <Input
              name="dataNascimento"
              label="Data de Nascimento"
              placeholder="DD/MM/AAAA"
              type="text"
              value={formData.dataNascimento}
              onChange={handleChange}
            />
            <Input name="email" label="E-mail" placeholder="E-mail" type="email" value={formData.email} onChange={handleChange} />
            <Input name="password" label="Senha" placeholder="Senha" type="password" value={formData.password} onChange={handleChange} />

            <Button type="submit" title="Cadastrar" />

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
