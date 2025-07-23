import { describe, it, expect, beforeEach, spyOn } from '@jest/globals';

describe('Login Page', () => {
  let loginButton;
  let emailInput, passwordInput;

  beforeEach(() => {
    document.body.innerHTML = `
      <input id="email" type="email">
      <input id="password" type="password">
      <button id="login-button">Entrar</button>
    `;

    loginButton = document.getElementById('login-button');
    emailInput = document.getElementById('email');
    passwordInput = document.getElementById('password');

    spyOn(window, 'handleLogin').and.callThrough();
  });

  it('deve chamar handleLogin ao clicar no botão', () => {
    emailInput.value = 'test@example.com';
    passwordInput.value = 'senha123';
    loginButton.click();
    expect(window.handleLogin).toHaveBeenCalled();
  });

  it('não deve chamar handleLogin se campos estiverem vazios', () => {
    loginButton.click();
    expect(window.handleLogin).not.toHaveBeenCalled();
  });
});