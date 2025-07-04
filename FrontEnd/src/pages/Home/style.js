import styled from 'styled-components';

export const Container = styled.section`
  background-color: #111827;
  color: white;
  padding: 3rem 0;
`;

export const Content = styled.div`
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1rem;
  display: flex;
  flex-direction: column;

  @media (min-width: 768px) {
    flex-direction: row;
    align-items: center;
  }
`;

export const TextContainer = styled.div`
  width: 100%;
  margin-bottom: 2.5rem;

  @media (min-width: 768px) {
    width: 50%;
    margin-bottom: 0;
  }
`;

export const Title = styled.h1`
  font-size: 2.25rem;
  font-weight: 700;
  margin-bottom: 1rem;

  @media (min-width: 768px) {
    font-size: 3rem;
  }
`;

export const Description = styled.p`
  font-size: 1.25rem;
  margin-bottom: 2rem;
  color: #d1d5db;
`;

export const ButtonGroup = styled.div`
  display: flex;
  gap: 1rem;
`;

export const ImageContainer = styled.div`
  width: 100%;

  @media (min-width: 768px) {
    width: 50%;
  }
`;

export const HeroImage = styled.img`
  border-radius: 0.5rem;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
  width: 100%;
  height: auto;
`;