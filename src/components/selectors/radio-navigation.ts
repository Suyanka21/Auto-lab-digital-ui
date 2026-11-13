import type { KeyboardEvent } from 'react';

export function navigateRadio(event: KeyboardEvent<HTMLDivElement>) {
  if (!['ArrowDown', 'ArrowRight', 'ArrowUp', 'ArrowLeft', 'Home', 'End'].includes(event.key)) return;
  const radios = Array.from(event.currentTarget.querySelectorAll<HTMLButtonElement>('[role="radio"]:not(:disabled)'));
  if (!radios.length || !radios.includes(event.target as HTMLButtonElement)) return;
  event.preventDefault();
  const index = radios.indexOf(event.target as HTMLButtonElement);
  const next = event.key === 'Home' ? 0 : event.key === 'End' ? radios.length - 1 :
    (index + (event.key === 'ArrowUp' || event.key === 'ArrowLeft' ? -1 : 1) + radios.length) % radios.length;
  radios[next].focus();
  radios[next].click();
}
