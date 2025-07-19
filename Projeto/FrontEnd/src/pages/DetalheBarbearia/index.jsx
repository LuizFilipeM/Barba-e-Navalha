import { useParams } from "react-router-dom";
import { useEffect, useState } from "react";
import { api } from "../../services/api";

import {
  Main,
  Card,
  CardHeader,
  Address,
  ServicesList,
  Title
} from "./style";

import { Header } from "../../components/Header";
import { Footer } from "../../components/Footer";

export function DetalheBarbearia() {
  const { id } = useParams();
  const [barbearia, setBarbearia] = useState(null);
  const [servico, setServico] = useState(null);
  const [horarios, setHorarios] = useState([]);

  useEffect(() => {
    async function fetchData() {
        const resBarbearia = await api.get(`/barbershops/`);
        setBarbearia(resBarbearia.data.data[0]);
        //alert(resBarbearia.data.data.nome_local);
        const resServicos = await api.get("/list-services/");
        const serv = resServicos.data.data.find(s => s.local_nome === resBarbearia.data.data[0].nome_local);
        setServico(serv);
        //alert(servico.descricao);
        

        const resHorarios = await api.get("/list-schedule/");
        const hrs = resHorarios.data.data.filter(h => h.local_nome === resBarbearia.data.data[0].nome_local);
        setHorarios(hrs);
        alert(servico.descricao);
    }

    fetchData();
  }, [id]);

  if (!barbearia) return <p>Carregando...</p>;

  return (
    <>
      <Header links={[{ label: "Voltar", to: "/" }]} />

      <Main>
        <Title>{barbearia.nome_local}</Title>
        <Card>
          <CardHeader>Detalhes da Barbearia</CardHeader>
          <Address>
            <p><strong>Endereço: </strong> {barbearia.endereco}</p>
            <p><strong>Telefone: </strong> {barbearia.telefone}</p>
            <p><strong>CNPJ: </strong> {barbearia.cnpj}</p>

            
            
            {servico && (
            <>
                <h4>Serviço:</h4>
                <ServicesList>
                <li>
                    <strong>{servico.nome}: </strong> {servico.descricao} — R${servico.preco} ({servico.tempo} min)
                </li>
                </ServicesList>
            </>
            )}

             
            {horarios && (
            <>
                <h4>Horários:</h4>
                {horarios.map((h) => (
                <ul key={h.id}>
                    <li>
                        <strong>{h.dia_semana}: </strong> {h.hora_inicio} - {h.hora_fim}
                    </li>
                </ul>
                ))}
            </>
            )}
          </Address>
        </Card>
      </Main>

      <Footer />
    </>
  );
}
