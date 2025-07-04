import styled from "styled-components";

export const Container = styled.section`
    background-color: #111827;
`;

export const Context = styled.div`
  max-width: 500px;
  margin: 80px auto;
  padding: 20px;
  background-color: #fff;
  border-radius: 12px;
  box-shadow: 0 4px 10px rgba(0,0,0,0.1);

  h1 {
    text-align: center;
    margin-bottom: 30px;
    color: #333;
  }
`;

export const ProfileInfo = styled.div`
  p {
    text-align: center;
    margin: 8px 0;
    font-size: 16px;

    strong {
      color: #444;
    }
  }

  button {
    margin-top: 20px;
    margin-left: 50px;
    margin-right: 10px;
  }
`;

export const ProfileForm = styled.div`
  display: flex;
  flex-direction: column;
  gap: 15px;

  label {
    display: flex;
    flex-direction: column;
    font-weight: 500;
    color: #444;
  }

  input {
    padding: 10px;
    border-radius: 8px;
    border: 1px solid #ccc;
    margin-top: 5px;
    transition: border-color 0.2s;

    &:focus {
      outline: none;
      border-color: #0077ff;
    }
  }

  hr {
    border: none;
    border-top: 1px solid #ddd;
    margin: 20px 0;
  }

  button {
    margin-top: 10px;
    margin-right: 10px;
  }
`;
