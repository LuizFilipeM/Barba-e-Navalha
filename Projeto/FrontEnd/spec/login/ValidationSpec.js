import { describe, it, expect } from '@jest/globals';
import {validateDate, validateEmail, validatePassword} from '../user'

describe('Validation Service', () => {
  it('deve validar formato de data (DD/MM/YYYY)', () => {
    expect(validateDate('30/12/2023')).toBeTrue();
    expect(validateDate('2023/12/30')).toBeFalse();
  });

  it('deve validar email corretamente', () => {
    expect(validateEmail('user@example.com')).toBeTrue();
    expect(validateEmail('invalid-email')).toBeFalse();
  });

  it('deve validar senha (mínimo 6 caracteres)', () => {
    expect(validatePassword('Senha123')).toBeTrue();
    expect(validatePassword('123')).toBeFalse();
  });
});