import styled from "styled-components";

export const Container = styled.div`
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  background-color: #111827;
`;

export const Context = styled.main`
  max-width: 500px;
  margin: 3rem auto;
  padding: 2rem;
  background-color: #fff;
  border-radius: 16px;
  box-shadow: 0 2px 16px rgba(0, 0, 0, 0.08);

  display: flex;
  flex-direction: column;
  gap: 1.2rem;
`;

export const Title = styled.h2`
  font-size: 2rem;
  margin-bottom: 2rem;
  text-align: center;
`;

export const DayContainer = styled.div`
  margin-top: 1rem;
  padding: 1rem;
  border-radius: 8px;
  background: #f9f9f9;
`;

export const StyledLink = styled.div`
  margin-top: 2rem;
  text-align: center;

  a {
    color: #0077cc;
    text-decoration: none;

    &:hover {
      text-decoration: underline;
    }
  }
`;

export const DiaButton = styled.button`
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 8px;
  font-weight: bold;
  cursor: pointer;
  background-color: color: #0077cc;
  color: black;
  transition: 0.3s ease;
  align-items: center;


  &:hover {
    filter: brightness(0.9);
  }
`;

export const ButtonsWrapper = styled.div`
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-bottom: 20px;
`;

export const IntervaloBox = styled.div`
  border: 1px solid #ccc;
  padding: 1rem;
  margin-bottom: 1rem;
  border-radius: 6px;
  background-color: #fff;
`;
