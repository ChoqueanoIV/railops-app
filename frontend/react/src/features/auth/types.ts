export interface LoginRequest {
  matricula: string;
  pin: string;
}

export interface LoginResponse {
  access_token: string;
  token_type: 'bearer';
}

export interface PrimeiroAcessoRequest {
  matricula: string;
  codigo_ativacao: string;
  pin: string;
}

export interface PrimeiroAcessoResponse {
  mensagem: string;
}
