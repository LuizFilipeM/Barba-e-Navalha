import { Container, StyledInput, StyledLabel } from './style';

export function Input({ placeholder, type = 'text', onChange, label, name }) {
  return (
    <Container>
      {label && <StyledLabel htmlFor={name}>{label}</StyledLabel>}
      <StyledInput
        id={name}
        name={name}
        placeholder={placeholder}
        type={type}
        onChange={onChange}
      />
    </Container>
  );
}
