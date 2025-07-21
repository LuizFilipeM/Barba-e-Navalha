import styled from "styled-components";

export const Main = styled.main`
  padding: 1rem 2rem;
  background-color: #111827;
  min-height: 80vh;
  max-height: 100vh;
`;

export const Title = styled.h1`
  text-align: center;
  margin-bottom: 2rem;
  color: #f9f9f9;
`;

export const Section = styled.section`
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
`;

export const Card = styled.div`
  background-color: #fff;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  transition: all 0.3s ease;
  position: relative;

  &:hover {
    transform: scale(1.01);
  }

  h2 {
    text-align: center;
  }
`;

