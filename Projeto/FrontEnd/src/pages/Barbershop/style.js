import styled from "styled-components";

export const Container = styled.section`
  background-color: #111827;
`;

export const Context = styled.section`
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
  font-size: 1.8rem;
  color: #222;
  margin-bottom: 1rem;
  text-align: center;
`;

export const StyledLink = styled.div`
  margin-top: 1.5rem;
  text-align: center;

  a {
    text-decoration: none;
    color: #444;
    font-weight: 500;
    transition: color 0.2s;

    &:hover {
      color: #000;
    }
  }
`;
