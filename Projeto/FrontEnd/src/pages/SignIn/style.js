import styled from "styled-components";

export const Container = styled.section`
  background-color: #111827;
  color: white;
  padding: 3rem 0;
`;

export const Context = styled.main`
  background-color: #1f2937;
  max-width: 500px;
  margin: 0rem auto;
  border-radius: 0.8rem;
  padding: 1rem;
`;

export const Title = styled.h2`
  text-align: center;
  margin-bottom: 1rem;
  font-size: 1.5rem;
  font-weight: bold;
`;

export const Form = styled.form`
  display: flex;
  flex-direction: column;
  gap: 0.3rem;

  label {
    color: white;
    font-weight: bold;
  }
`;

export const BackLinkWrapper = styled.div`
  a {
    color: #2563eb;
    text-decoration: none;

    &:hover {
      text-decoration: underline;
    }
  }
`;
