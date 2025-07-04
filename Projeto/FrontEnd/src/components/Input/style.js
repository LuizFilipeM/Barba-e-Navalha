import styled from 'styled-components';

export const Container = styled.div`
  margin-bottom: 1rem;
  display: flex;
  flex-direction: column;
`;

export const StyledLabel = styled.label`
  font-weight: 600;
  margin-bottom: 0.5rem;
  color: #1f2937;
`;

export const StyledInput = styled.input`
  padding: 0.75rem 1rem;
  border: 1px solid #ccc;
  border-radius: 0.5rem;
  font-size: 1rem;
  outline: none;

  &:focus {
    border-color: #2563eb;
    box-shadow: 0 0 0 2px rgba(37, 99, 235, 0.2);
  }
`;
