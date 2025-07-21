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
`;

export const Card = styled.div`
  width: 300px;
  height: 300px;
  background-color: #fff;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  transition: all 0.3s ease;
  position: relative;

  &:hover {
    transform: scale(1.01);
  }

  h5 {
    margin-top: 1rem;
    margin-bottom: 0.5rem;
    color: #555;
  }

  p {
    margin: 0.25rem 0;
  }
  
  a {
    position: absolute;
    bottom: 10px;
    left: 50%;
    transform: translateX(-50%);
  }
`;

export const CardHeader = styled.h4`
  text-align: center;
  margin: 0;
  font-size: 1.25rem;
  color: #222;
`;

export const Address = styled.div`
  color: #666;
  font-size: 0.95rem;
`;

export const ServicesList = styled.ul`
  list-style-type: disc;
  padding-left: 1rem;

  li {
    margin-bottom: 0.1rem;
    color: #444;
  }
`;

