import { useState, useEffect } from "react";
import { useAuth } from "../hooks/hookAuth";
/*import { api } from "../services/api";*/

export const MOCKED_LOCALS = [
  {
    id: 1,
    userEmail: "barbeir@email.com",
    nome: "Barbearia do João",
    telefone: "(11) 99999-9999",
    cidade: "São Paulo",
    rua: "Av. Paulista, 1000",
    bairro: "Centro",
    cnpj: "00.000.000/0000-00",
    servicos: [
        { id: 1, nome: "Corte de cabelo masculino", price: 50 },
        { id: 2, nome: "Corte de cabelo feminino", price: 50 },
    ],
    horarios: {
      segunda: ["09:00 - 20:00"],
      terca: ["09:00 - 20:00"],
      quarta: ["09:00 - 20:00"],
      quinta: ["09:00 - 20:00"],
      sexta: ["09:00 - 20:00"],
    },
  },
  {
    id: 2,
    userEmail: "ana@email.com",
    nome: "Barbearia da Ana",
    telefone: "(11) 99999-9999",
    cidade: "São Paulo",
    rua: "Av. Paulista, 1000",
    bairro: "Centro",
    cnpj: "00.000.000/0000-00",
    servicos: [
        { id: 1, nome: "Corte de cabelo masculino", price: 50 },
        { id: 2, nome: "Corte de cabelo feminino", price: 50 },
    ],
    horarios: {
      segunda: ["09:00 - 20:00"],
      terca: ["09:00 - 20:00"],
      quarta: ["09:00 - 20:00"],
      quinta: ["09:00 - 20:00"],
      sexta: ["09:00 - 20:00"],
    },
  }
];

export function useLocal() {
  const [hasLocal, setHasLocal] = useState(false);
  const [local, setLocal] = useState(null);
  const { user } = useAuth();

  useEffect(() => {
    if (user && user.email) {
      const localEncontrado = MOCKED_LOCALS.find(
        (item) => item.userEmail === user.email
      );

      if (localEncontrado) {
        setHasLocal(true);
        setLocal(localEncontrado);
      } else {
        setHasLocal(false);
        setLocal(null);
      }
    }
  }, [user]);

  return { hasLocal, local };
}

/*export function useLocal() {
  const [hasLocal, setHasLocal] = useState(false);
  const [local, setLocal] = useState(null);
  const [allLocals, setAllLocals] = useState([]);
  const { user } = useAuth();

  useEffect(() => {
    async function fetchUserLocal() {
      if (!user?.token) return;

      try {
        const response = await api.get("/api/locals/user", {
          headers: {
            Authorization: `Bearer ${user.token}`,
          },
        });

        if (response.data?.local) {
          setHasLocal(true);
          setLocal(response.data.local);
        } else {
          setHasLocal(false);
          setLocal(null);
        }
      } catch (error) {
        console.error("Erro ao buscar local do usuário:", error);
        setHasLocal(false);
        setLocal(null);
      }
    }

    fetchUserLocal();
  }, [user]);

  useEffect(() => {
    async function fetchAllLocals() {
      try {
        const response = await api.get("/api/locals");
        setAllLocals(response.data || []);
      } catch (error) {
        console.error("Erro ao buscar todos os locais:", error);
        setAllLocals([]);
      }
    }

    fetchAllLocals();
  }, []);

  return {
    hasLocal,
    local,
    allLocals,
  };
}*/
