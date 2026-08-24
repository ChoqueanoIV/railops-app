export interface ApiErrorDetail {
  code: string;
  message: string;
  details: unknown | null;
}

export interface ApiErrorEnvelope {
  detail: unknown;
  error: ApiErrorDetail;
}
