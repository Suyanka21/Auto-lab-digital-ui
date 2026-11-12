import type { ElementType, HTMLAttributes, ReactNode } from 'react';

type HeadingVariant = 'display' | 'section' | 'title' | 'kicker' | 'body' | 'caption';
type HeadingTone = 'default' | 'muted' | 'inverse' | 'inverse-muted';

interface EditorialHeadingProps extends HTMLAttributes<HTMLElement> {
  as?: ElementType;
  variant?: HeadingVariant;
  tone?: HeadingTone;
  children: ReactNode;
}

const VARIANT_CLASSES: Record<HeadingVariant, string> = {
  display: 'font-serif text-[clamp(2.25rem,4.2vw,3.75rem)] leading-[1.05] tracking-[-0.02em] font-normal',
  section: 'font-serif text-[clamp(1.5rem,2.4vw,2.125rem)] leading-[1.15] tracking-[-0.015em] font-normal',
  title: 'font-serif text-[1.25rem] leading-[1.25] tracking-[-0.01em] font-normal',
  kicker: 'font-sans text-[11px] leading-[1.4] tracking-[0.16em] uppercase font-medium',
  body: 'font-sans text-[15px] leading-[1.6] font-normal',
  caption: 'font-sans text-[13px] leading-[1.5] font-normal',
};

const TONE_CLASSES: Record<HeadingTone, string> = {
  default: 'text-ink',
  muted: 'text-muted-grey',
  inverse: 'text-paper',
  'inverse-muted': 'text-[#C8C4BC]',
};

const DEFAULT_ELEMENT: Record<HeadingVariant, ElementType> = {
  display: 'h1',
  section: 'h2',
  title: 'h3',
  kicker: 'p',
  body: 'p',
  caption: 'p',
};

const EXPLICIT_TEXT_COLOR_RE = /\btext-(?:ink|paper|muted-grey|cyan|cyan-ink|white|black|\[#)/;

export function EditorialType({
  as,
  variant = 'body',
  tone = 'default',
  className = '',
  children,
  ...props
}: EditorialHeadingProps) {
  const Component = as ?? DEFAULT_ELEMENT[variant];
  const hasExplicitColor = EXPLICIT_TEXT_COLOR_RE.test(className);
  const toneClass = hasExplicitColor ? '' : TONE_CLASSES[tone];

  return (
    <Component
      className={`${VARIANT_CLASSES[variant]} ${toneClass} ${className}`.trim()}
      {...props}
    >
      {children}
    </Component>
  );
}
