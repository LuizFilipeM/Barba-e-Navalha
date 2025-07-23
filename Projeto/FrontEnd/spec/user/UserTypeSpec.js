import { describe, beforeEach, it, expect } from '@jest/globals';

describe('User Type Selection', () => {
  let userTypeSelect;

  beforeEach(() => {
    document.body.innerHTML = `
      <select id="user-type">
        <option value="client">Cliente</option>
        <option value="barber">Barbeiro</option>
      </select>
    `;
    userTypeSelect = document.getElementById('user-type');
  });

  it('deve ter "client" como valor padrão', () => {
    expect(userTypeSelect.value).toBe('client');
  });

  it('deve mudar para "barber" quando selecionado', () => {
    userTypeSelect.value = 'barber';
    userTypeSelect.dispatchEvent(new Event('change'));
    expect(userTypeSelect.value).toBe('barber');
  });
});