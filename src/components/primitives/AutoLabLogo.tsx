import type { HTMLAttributes } from 'react';

interface AutoLabMarkProps extends HTMLAttributes<SVGSVGElement> {
  size?: number;
}

/**
 * Geometric "A" monogram faithfully traced from AUTOLAB LOGO .pdf.
 * Renders on a Graphite (#101114) square plate with Ivory/White left bar
 * and Cyan (#72C4E1) structural right leg.
 */
export function AutoLabMark({ size = 36, className = '', ...props }: AutoLabMarkProps) {
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 64 64"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      aria-hidden="true"
      className={`shrink-0 ${className}`}
      {...props}
    >
      <rect width="64" height="64" rx="2" fill="#101114" />
      {/* Left angled bar */}
      <polygon points="33,12 16,42 22,50 38,21" fill="#FAF8F3" />
      {/* Cyan right leg & crossbar */}
      <polygon points="39,25 29,43 40,43 44,50 49,42" fill="#72C4E1" />
    </svg>
  );
}

interface AutoLabBrandProps {
  onClick?: () => void;
}

export function AutoLabBrand({ onClick }: AutoLabBrandProps) {
  return (
    <button
      type="button"
      onClick={onClick}
      className="inline-flex items-center gap-3 text-left whitespace-nowrap shrink-0 min-h-[44px] py-1 focus-visible:outline-2 focus-visible:outline-cyan-ink"
    >
      <AutoLabMark size={32} />
      <span className="font-serif text-[20px] leading-none tracking-[-0.01em] text-ink font-medium">
        AutoLab
      </span>
    </button>
  );
}
