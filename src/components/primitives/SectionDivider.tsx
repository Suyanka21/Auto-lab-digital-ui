interface SectionDividerProps {
  label?: string;
  className?: string;
}

export function SectionDivider({ label, className = '' }: SectionDividerProps) {
  if (!label) {
    return <hr className={`border-0 border-t border-fine-border ${className}`} />;
  }

  return (
    <div className={`flex items-center gap-4 ${className}`}>
      <span className="h-px flex-1 bg-fine-border" aria-hidden="true" />
      <span className="font-sans text-[11px] tracking-[0.18em] uppercase text-muted-grey whitespace-nowrap">
        {label}
      </span>
      <span className="h-px flex-1 bg-fine-border" aria-hidden="true" />
    </div>
  );
}
