import { useState, useEffect } from "react";
import { api } from "../../services/api";
import { Link } from "react-router-dom";
import { useAuth } from "../../hooks/hookAuth";

import { Input } from "../../components/Input";
import { Button } from "../../components/Button";
import { Header } from "../../components/Header";
import { Footer } from "../../components/Footer";

import { Container, Context, Title, StyledLink } from "./style";

export function BarberShop() {
  
  const [nomeLocal, setNomeLocal] = useState("");
  const [rua, setRua] = useState("");
  const [bairro, setBairro] = useState("");
  const [cidadeLocal, setCidadeLocal] = useState("");
  const [cnpj, setCnpj] = useState("");
  const [token, setToken] = useState("");
  const { signOut } = useAuth();

  useEffect(() => {
    const tokenUser = localStorage.getItem("token");
    if (tokenUser) {
      setToken(tokenUser);
    }
  }, []);

  function validarCampos() {
    if (!nomeLocal.trim()) return "Preencha o nome do local.";
    if (!rua.trim()) return "Preencha a rua.";
    if (!bairro.trim()) return "Preencha o bairro.";
    if (!cidadeLocal.trim()) return "Preencha a cidade.";
    if (!cnpj.trim()) return "Preencha o CNPJ.";
    if (!token) return "Usuário não autenticado.";
    return null;
  }

  async function handleSignUp() {
    const erro = validarCampos();
    if (erro) {
      alert(erro);
      return;
    }

    const newLocal = {
      nomeLocal,
      rua,
      bairro,
      cidadeLocal,
      cnpj,
    };

    try {
      await api.post("/locals", newLocal, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      alert("Cadastro realizado com sucesso! ✅");

      setNomeLocal("");
      setRua("");
      setBairro("");
      setCidadeLocal("");
      setCnpj("");

    } catch (error) {
      const msg = error.response?.data?.message || "Erro ao cadastrar local.";
      alert(`Erro: ${msg}`);
    }
  }


  return (
    <Container>
      <Header
        links={[
          { label: "Home", to: "/" },
          { label: "Perfil", to: "/" },
          { label: "Sair", onClick: signOut },
        ]}
      />

      <Context>
        <Title>Faça o cadastro do local</Title>

        <Input
          placeholder="Nome do Local"
          type="text"
          value={nomeLocal}
          onChange={(e) => setNomeLocal(e.target.value)}
          label="Nome do Local"
        />

        <Input
          placeholder="Rua"
          type="text"
          value={rua}
          onChange={(e) => setRua(e.target.value)}
          label="Rua"
        />

        <Input
          placeholder="Bairro"
          type="text"
          value={bairro}
          onChange={(e) => setBairro(e.target.value)}
          label="Bairro"
        />

        <Input
          placeholder="Cidade"
          type="text"
          value={cidadeLocal}
          onChange={(e) => setCidadeLocal(e.target.value)}
          label="Cidade"
        />

        <Input
          placeholder="CNPJ"
          type="text"
          value={cnpj}
          onChange={(e) => setCnpj(e.target.value)}
          label="CNPJ"
        />

        <Button title="Cadastrar" onClick={handleSignUp} />

        <StyledLink>
          <Link to="/">Voltar</Link>
        </StyledLink>
      </Context>

      <Footer />
    </Container>
  );
}
