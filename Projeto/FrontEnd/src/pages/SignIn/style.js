import styled from "styled-components";

export const Container = styled.section`
  background-color: #111827;
  color: white;
  padding: 2rem 0;
  display: flex;
  justify-content: center;
  gap: 7rem;
`;

export const Context = styled.main`
  background-color: #1f2937;
  width: 60%;
  height: 80%;
  max-width: 500px;
  border-radius: 0.8rem;
  padding: 2rem;
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

export const ImageContainer = styled.div`
  width: 40%;
  display: flex;
  justify-content: center;
  align-items: center;
`;

export const HeroImage = styled.img`
  border-radius: 0.5rem;
  max-width: 100%;
  height: 80%;
`;