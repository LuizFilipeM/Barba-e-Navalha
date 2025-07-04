import { createGlobalStyle } from 'styled-components';

export const GlobalStyle = createGlobalStyle`
  * {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
  }

  html {
    scroll-behavior: smooth;
  }

  body {
    background-color: #f3f4f6; /* bg-gray-100 */
    font-family: 'sans-serif';
    color: #111827; /* text-gray-900 */
  }

  /* Páginas com animação de transição */
  .page {
    display: none;
  }

  .page.active {
    display: block;
    animation: fadeIn 0.5s;
  }

  @keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
  }

  /* Serviços */
  .service-item {
    transition: all 0.3s ease;
  }

  .service-item:hover {
    transform: translateY(-5px);
    box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
  }

  .barbershop-card {
    transition: all 0.3s ease;
  }

  .barbershop-card:hover {
    transform: scale(1.02);
  }

  /* Ícones FontAwesome (caso use via CDN no index.html) */
  @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css');
`;
