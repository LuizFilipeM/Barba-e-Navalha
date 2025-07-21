import styled from "styled-components";

export const Main = styled.main`
  padding: 5rem;
  background-color: #111827;
  min-height: 80vh;
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
  background-color: #fff;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 4px 12px rgba(0,0,0,0.05);
  transition: all 0.3s ease;

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
`;

export const CardHeader = styled.h4`
  margin: 0;
  font-size: 1.25rem;
  color: #222;
`;

export const Address = styled.p`
  color: #666;
  font-size: 0.95rem;
`;

export const ServicesList = styled.ul`
  list-style-type: disc;
  padding-left: 1.25rem;
  margin-bottom: 1rem;

  li {
    margin-bottom: 0.3rem;
    color: #444;
  }
`;

export const ToggleButton = styled.button`
  background-color: #0077b6;
  color: white;
  border: none;
  padding: 0.6rem 1.2rem;
  border-radius: 8px;
  cursor: pointer;
  margin-top: 1rem;

  &:hover {
    background-color: #005f87;
  }
`;

export const ScheduleSection = styled.div`
  margin-top: 1rem;
  background-color: #f1f1f1;
  padding: 1rem;
  border-radius: 8px;

  ul {
    list-style-type: none;
    padding-left: 0;

    li {
      margin-bottom: 0.4rem;
    }
  }
`;
