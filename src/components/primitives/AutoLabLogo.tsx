import type { HTMLAttributes } from 'react';

interface AutoLabMarkProps extends HTMLAttributes<HTMLImageElement> { size?: number; }

/** First-party logo exported from the committed production brand asset; no redrawing. */
export function AutoLabMark({size=36,className='',...props}:AutoLabMarkProps){
 return <img src={`${import.meta.env.BASE_URL}brand/autolab-logo.png`} alt="" width={size} height={size * .81} className={`shrink-0 object-contain ${className}`} {...props}/>;
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
      <AutoLabMark size={48} />
      <span className="font-serif text-[20px] leading-none tracking-[-0.01em] text-ink font-medium">
        AutoLab
      </span>
    </button>
  );
}
