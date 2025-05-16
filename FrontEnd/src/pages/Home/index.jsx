import { useNavigate } from 'react-router-dom';

import { Container, Content, TextContainer, Title, Description, ButtonGroup, ImageContainer, HeroImage } from './style';
import { Button } from '../../components/Button';
import barbeariaImage from '../../assets/barbearia.png';
import { Header } from "../../components/Header";
import { Footer } from "../../components/Footer";

export const Home = () => {
  const navigate = useNavigate();
  return (
    <>
      <Header links={[
          { label: 'Home', to: '/' },
          { label: 'Login', to: '/enter' },
          { label: 'Cadastre-se', to: '/register' }
      ]}/>
      <Container>
        <Content>
          <TextContainer>
            <Title>Agende seu corte com os 
              melhores barbeiros</Title>
            <Description>Encontre barbearias próximas, veja serviços e horários disponíveis.
              Agende seu corte com facilidade!</Description>
            <ButtonGroup>
              <Button 
                title="Cadastre-se" 
                onClick={() => navigate('/register')}
              />
              <Button 
                title="Login" 
                onClick={() => navigate('/enter')}
              />
            </ButtonGroup>
          </TextContainer>
          <ImageContainer>
            <HeroImage 
              src={barbeariaImage}
              alt="Barbearia" 
            />
          </ImageContainer>
        </Content>
      </Container>
      <Footer />
    </>
  );
};

