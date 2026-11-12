import type { ButtonHTMLAttributes, ReactNode } from 'react';

export type AtelierButtonVariant = 'primary' | 'secondary' | 'outline-cyan' | 'ghost';

interface AtelierButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: AtelierButtonVariant;
  children: ReactNode;
}

const VARIANT_CLASSES: Record<AtelierButtonVariant, string> = {
  primary:
    'bg-graphite text-paper border border-graphite hover:bg-ink active:translate-y-px',
  secondary:
    'bg-paper text-ink border border-fine-border hover:border-ink active:translate-y-px',
  'outline-cyan':
    'bg-graphite text-paper border border-cyan hover:bg-[#191B20] active:translate-y-px',
  ghost:
    'bg-transparent text-ink border border-transparent hover:text-cyan-ink',
};

export function AtelierButton({
  variant = 'primary',
  type = 'button',
  className = '',
  children,
  ...props
}: AtelierButtonProps) {
  const hasCustomJustify = /\bjustify-(?:start|end|between|around|evenly)\b/.test(className);
  const justifyClass = hasCustomJustify ? '' : 'justify-center';

  return (
    <button
      type={type}
      className={`inline-flex items-center ${justifyClass} gap-2.5 min-h-[44px] min-w-0 px-5 py-2.5 text-[13px] font-medium tracking-[0.02em] whitespace-nowrap rounded-[2px] transition-colors duration-150 disabled:opacity-45 disabled:pointer-events-none cursor-pointer ${VARIANT_CLASSES[variant]} ${className}`.trim()}
      {...props}
    >
      {children}
    </button>
  );
}
