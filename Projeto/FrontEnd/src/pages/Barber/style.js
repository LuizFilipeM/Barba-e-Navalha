import styled from "styled-components";

export const Container = styled.section`
  background-color: #111827;
`;

export const Context = styled.section`
  max-width: 800px;
  margin: 2rem auto;
  padding: 2rem;
  background-color: #fff;
  border-radius: 16px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
`;

export const Title = styled.h1`
  font-size: 2rem;
  margin-bottom: 1.5rem;
  color: #333;
`;

export const TitleH1 = styled.h1`
  font-size: 2rem;
  margin-bottom: 1.5rem;
  color: white;
`;

export const Paragraph = styled.p`
  font-size: 1rem;
  color: #444;
  margin-bottom: 0.5rem;

  strong {
    font-weight: bold;
    color: #222;
  }
`;

export const SubTitle = styled.h3`
  margin-top: 1.5rem;
  margin-bottom: 0.5rem;
  font-size: 1.2rem;
  color: #222;
`;

export const List = styled.ul`
  list-style: none;
  padding-left: 0;

  li {
    padding: 0.4rem 0;
    border-bottom: 1px solid #eee;
    font-size: 1rem;
    color: #555;
  }
`;

export const RegisterLink = styled.div`
  text-align: center;
  margin-top: 2rem;
  padding: 12rem;

  a {
    text-decoration: none;
    background-color: #111;
    color: #fff;
    padding: 0.6rem 1.2rem;
    border-radius: 8px;
    font-weight: bold;
    transition: background 0.2s;

    &:hover {
      background-color: #333;
    }
  }
`;
