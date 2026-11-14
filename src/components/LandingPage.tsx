import { useState } from 'react';
import { ArrowRight, ArrowUpRight } from 'lucide-react';
import { EDITORIAL_IMAGES, MATERIAL_STUDIES } from '@/src/data/editorial-images';
import { MATERIAL_OPTIONS } from '@/src/data/catalog';
import type { MaterialId } from '@/src/types/configuration';
import { EditorialCover } from './EditorialCover';
import { navigateRadio } from './selectors/radio-navigation';
import './editorial-showroom.css';

export interface LandingPageProps { onEnterStudio: () => void; }

export function LandingPage({ onEnterStudio }: LandingPageProps) {
  const [material, setMaterial] = useState<MaterialId>('diamond-quilted');
  const selected = MATERIAL_OPTIONS.find(option => option.id === material)!;
  return <div className="editorial-showroom" data-component="LandingPage">
    <EditorialCover onEnterStudio={onEnterStudio}/>
    <section id="materials" className="material-edit" aria-labelledby="material-edit-title">
      <header className="editorial-section-head"><p className="editorial-kicker">01 / The material edit</p><h2 id="material-edit-title">Texture tells<br/><em>the story.</em></h2><p>Quiet grain. Sculpted quilting. Precise perforations. Three ways to give an interior its character.</p></header>
      <div className="material-feature">
        <figure><img key={material} src={MATERIAL_STUDIES[material]} alt={`AI-generated ${selected.label.toLowerCase()} leather texture study`} width="1254" height="1254" loading="lazy"/><figcaption>Illustrative material study / {selected.label}</figcaption></figure>
        <div className="material-feature-copy"><span className="editorial-kicker">Look closer</span><h3>{selected.label}</h3><p>{selected.description}</p>
          <div className="material-index" role="radiogroup" aria-label="Explore material studies" onKeyDown={navigateRadio}>{MATERIAL_OPTIONS.map((option,i)=><button type="button" key={option.id} role="radio" aria-checked={material===option.id} tabIndex={material===option.id?0:-1} onClick={()=>setMaterial(option.id)}><span>0{i+1}</span><span>{option.label}</span><ArrowUpRight size={18} aria-hidden="true"/></button>)}</div>
          <button className="editorial-text-link" type="button" onClick={onEnterStudio}>Explore these treatments in 3D<ArrowRight size={18}/></button>
          <p className="editorial-disclosure">AI-generated studies illustrate texture. The live cabin shows the available digital treatments.</p>
        </div>
      </div>
    </section>
    <section className="finishing-edit" aria-labelledby="finish-title">
      <div><p className="editorial-kicker">02 / A considered contrast</p><h2 id="finish-title">Soft hide.<br/><em>Strong character.</em></h2><p>Pair a quiet leather palette with the grain of wood, the depth of lacquer or the precision of twill carbon fibre.</p><button className="editorial-text-link" type="button" onClick={onEnterStudio}>Find your composition<ArrowRight size={18}/></button><p className="editorial-disclosure">Trim and ambient lighting are illustrative previews. Workshop availability is discussed separately.</p></div>
      <figure><img src={EDITORIAL_IMAGES.trims} alt="AI-generated poplar, walnut, lacquer and carbon fibre material board" width="1536" height="1024" loading="lazy"/><figcaption>Poplar / Walnut / Piano lacquer / Carbon fibre</figcaption></figure>
    </section>
    <section id="experience" className="experience-edit" aria-labelledby="experience-title">
      <header><p className="editorial-kicker">03 / From feeling to specification</p><h2 id="experience-title">The cabin stays.<br/><em>The possibilities move.</em></h2></header>
      <div className="experience-steps">{[
        ['Choose your surface','Explore three treatments and eight leather colours, from quiet neutrals to deep green, navy and burgundy.'],
        ['Make the details yours','Tune thread and composition; preview trim and ambient light.'],
        ['See the whole picture','Four camera views. One live cabin. Every choice gathered in your specification.'],
      ].map(([title,detail],i)=><article key={title}><span>0{i+1}</span><div><h3>{title}</h3><p>{detail}</p></div></article>)}</div>
    </section>
    <section className="editorial-invitation" aria-label="Enter the Studio"><img className="invitation-background" src={EDITORIAL_IMAGES.workshop} alt="Illustrative upholstery cutting table with leather hides, tailoring tools and thread" width="1536" height="1024" loading="lazy"/><div className="invitation-copy"><p className="editorial-kicker">AutoLab Digital Showroom</p><h2>Your interior.<br/><em>Your point of view.</em></h2><p>Explore the live cabin, then carry your choices into a conversation.</p><span className="invitation-disclosure">AI-generated atelier study</span></div><button className="editorial-cta" type="button" onClick={onEnterStudio}>Enter the Studio<ArrowRight size={18}/></button></section>
  </div>;
}
