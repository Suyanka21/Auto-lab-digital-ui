import { useState } from 'react';
import { ArrowRight, ArrowDown, Pause, Play } from 'lucide-react';
import { EDITORIAL_IMAGES } from '@/src/data/editorial-images';

const SHOTS = [
  { name: 'The atelier', image: EDITORIAL_IMAGES.workshop, caption: '01 / The work behind the details', alt: 'Imagined upholstery atelier: draped leather hides, waxed thread, worn tailor shears and chalk patterns on a cutting table' },
  { name: 'Diamond Quilted', image: EDITORIAL_IMAGES.diamond, caption: '02 / The rhythm of a stitch', alt: 'AI macro study of softly padded black diamond quilting and fine double stitching' },
  { name: 'Finishing touches', image: EDITORIAL_IMAGES.trims, caption: '03 / Grain. Weave. Reflection.', alt: 'AI study of poplar, walnut, piano lacquer and twill carbon fibre samples' },
];

export function EditorialCover({ onEnterStudio }: { onEnterStudio: () => void }) {
  const [shot, setShot] = useState(0);
  const [still, setStill] = useState(false);
  const current = SHOTS[shot];
  const explore = () => document.getElementById('materials')?.scrollIntoView({
    behavior: window.matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth',
  });
  return <section className="editorial-cover" data-component="EditorialCover" data-motion={still ? 'still' : 'moving'} aria-labelledby="cover-title">
    <div className="cover-masthead"><span>AutoLab Interior Studio</span><span>Nairobi · The material edition</span><span>Digital Showroom / 01</span></div>
    <div className="cover-spread">
      <div className="cover-copy">
        <p className="editorial-kicker">An interior, considered.</p>
        <h1 id="cover-title" aria-label="A feeling. Made yours."><span className="word-mask" aria-hidden="true"><span>A feeling.</span></span><span className="word-mask" aria-hidden="true"><em>Made yours.</em></span></h1>
        <p className="cover-deck">The grain. The colour. The smallest stitch.<br/>Find your own expression in the details.</p>
        <button className="editorial-cta" type="button" onClick={onEnterStudio}>Enter the Studio<ArrowRight size={18} aria-hidden="true"/></button>
        <button className="editorial-text-link" type="button" onClick={explore}>Explore the material edit<ArrowDown size={18} aria-hidden="true"/></button>
        <div className="cover-footnote"><span>Designed around you.</span><p>A tactile introduction.<br/>A live cabin to make it your own.</p></div>
      </div>
      <div className="cover-film">
        <figure className="cover-art" key={shot}>
          <img src={current.image} alt={current.alt} width="1536" height="1024" fetchPriority="high"/>
          <figcaption>{current.caption}</figcaption>
        </figure>
        <div className="cover-controls">
          <div role="group" aria-label="Editorial studies">{SHOTS.map((item,i)=><button key={item.name} type="button" aria-label={`View study: ${item.name}`} aria-pressed={shot===i} onClick={()=>setShot(i)}><span>0{i+1}</span><span>{item.name}</span></button>)}</div>
          <button className="motion-control" type="button" onClick={()=>setStill(s=>!s)} aria-label={still?'Resume motion':'Pause motion'} aria-pressed={still}>{still?<Play size={16}/>:<Pause size={16}/>}</button>
        </div>
      </div>
    </div>
    <div className="cover-caption"><span>Material / Colour / Character</span><span>AI-generated material studies · Imagined atelier</span></div>
  </section>;
}
