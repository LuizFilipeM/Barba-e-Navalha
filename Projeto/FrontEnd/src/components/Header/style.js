import styled from 'styled-components';

export const Container = styled.header`
  background-color: #1f2937;
  color: white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  padding: 0.7rem 1rem; /* Mantido original */
  height: auto; /* Garante que não force altura fixa */

  .wrapper {
    max-width: 1200px;
    margin: 0 auto;
    display: flex;
    justify-content: space-between;
    align-items: center;
    height: 100%;
  }

  .logo-area {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    height: 100%;
  }

  .logo-link {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    text-decoration: none;
    color: inherit;
    
    &:hover {
      opacity: 0.9;
    }
  }

  .icon {
    width: 3rem;
    height: 2.5rem;
    object-fit: contain;
    margin: -0.5rem 0;
  }
`;

export const Logo = styled.span`
  font-size: 1.25rem; /* Mantido original */
  font-weight: bold;
`;

export const Nav = styled.nav`
  display: flex;
  gap: 1rem;

  .link {
    color: white;
    font-weight: bold;
    background: none;
    border: none;
    cursor: pointer;
    text-decoration: none;
    font-size: 1rem;

    &:hover {
      text-decoration: underline;
    }
  }

  button.link {
    padding: 0;
    font-family: inherit;
  }
`;


export const MobileMenuButton = styled.button`
  display: none;

  @media (max-width: 768px) {
    display: block;
    background: none;
    border: none;
    font-size: 1.5rem;
    color: white;
  }
`;