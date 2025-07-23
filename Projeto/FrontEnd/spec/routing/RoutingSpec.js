import { describe, beforeEach, it, expect } from '@jest/globals';
import jasmine from 'jasmine';
import simulateLogin from '../login'

describe('Routing', () => {
  beforeEach(() => {
    window.router = {
      navigate: jasmine.createSpy('navigate')
    };
  });

  it('deve redirecionar para /barber após login de barbeiro', () => {
    simulateLogin('barber');
    expect(window.router.navigate).toHaveBeenCalledWith('/barber');
  });

  it('deve redirecionar para /client após login de cliente', () => {
    simulateLogin('client');
    expect(window.router.navigate).toHaveBeenCalledWith('/client');
  });
});