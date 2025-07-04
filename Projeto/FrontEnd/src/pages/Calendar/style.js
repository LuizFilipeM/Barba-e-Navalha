import styled from "styled-components";

export const Container = styled.section`
  background-color: #111827;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
`;

export const Content = styled.main`
  flex: 1;
  max-width: 600px;
  margin: 3rem auto;
  padding: 2rem;
  background-color: #fff;
  border-radius: 16px;
  box-shadow: 0 2px 16px rgba(0, 0, 0, 0.08);

  display: flex;
  flex-direction: column;
  gap: 1.5rem;
`;

export const Title = styled.h1`
  font-size: 1.8rem;
  color: #222;
  text-align: center;
`;

export const List = styled.ul`
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 1rem;
`;

export const ListItem = styled.li`
  background: #f3f4f6;
  border-radius: 8px;
  padding: 1rem;
  color: #111;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.05);
  font-size: 1rem;
  font-weight: 500;
`;
