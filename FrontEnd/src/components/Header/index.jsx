import { Link } from 'react-router-dom';
import { Container, Nav, Logo, MobileMenuButton } from './style';
import { FaBars } from 'react-icons/fa';
import logoimage from '../../assets/BarbaENavalhaLogoBrancoSemFundo.png';

export const Header = ({ links = [] }) => {
  return (
    <Container>
      <div className="wrapper">
        <div className="logo-area">
          <Link to="/" className="logo-link">
            <img
              src={logoimage}
              alt="BarbaENavalha"
              className="icon"
            />
            <Logo>Barba&Navalha</Logo>
          </Link>
        </div>

        <Nav>
          {links.map((link, index) =>
            link.to ? (
              <Link key={index} to={link.to} className="link">
                {link.label}
              </Link>
            ) : (
              <button
                key={index}
                onClick={link.onClick}
                className="link"
              >
                {link.label}
              </button>
            )
          )}
        </Nav>

        <MobileMenuButton>
          <FaBars />
        </MobileMenuButton>
      </div>
    </Container>
  );
};
