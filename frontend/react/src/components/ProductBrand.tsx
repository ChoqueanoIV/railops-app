interface ProductBrandProps {
  compact?: boolean;
}

export function ProductBrand({ compact = false }: ProductBrandProps) {
  return (
    <div className={`product-brand${compact ? ' product-brand--compact' : ''}`}>
      <span className="product-brand__mark" aria-hidden="true">
        PT
      </span>
      <span className="product-brand__text">
        <strong>Passagem de Turno Digital</strong>
        <small>Operação ferroviária</small>
      </span>
      <span className="pilot-badge">Piloto</span>
    </div>
  );
}
