import type { ElementType, HTMLAttributes, ReactNode } from 'react';

export type SurfaceTone = 'ivory' | 'paper' | 'graphite';

interface SurfaceProps extends HTMLAttributes<HTMLElement> {
  as?: ElementType;
  tone?: SurfaceTone;
  bordered?: boolean;
  children: ReactNode;
}

const TONE_CLASSES: Record<SurfaceTone, string> = {
  ivory: 'bg-ivory text-ink',
  paper: 'bg-paper text-ink',
  graphite: 'bg-graphite text-paper',
};

const BORDER_CLASSES: Record<SurfaceTone, string> = {
  ivory: 'border border-fine-border',
  paper: 'border border-fine-border',
  graphite: 'border border-[#2A2B30]',
};

export function Surface({
  as: Component = 'div',
  tone = 'paper',
  bordered = true,
  className = '',
  children,
  ...props
}: SurfaceProps) {
  return (
    <Component
      className={`${TONE_CLASSES[tone]} ${bordered ? BORDER_CLASSES[tone] : ''} ${className}`}
      {...props}
    >
      {children}
    </Component>
  );
}
