import { Check } from 'lucide-react';
import { COLOUR_OPTIONS, COMPOSITION_OPTIONS, ILLUMINATION_OPTIONS, MATERIAL_OPTIONS, THREAD_OPTIONS, TRIM_OPTIONS } from '@/src/data/catalog';
import type { ConfigurationStepId, OptionMetadata } from '@/src/types/configuration';
import type { ConfigurationPanelProps } from './ConfigurationPanel';
import { navigateRadio } from './selectors/radio-navigation';
import classic from '@/src/assets/images/autolab_material_classic_1794511172047.jpg';
import diamond from '@/src/assets/images/autolab_material_diamond_quilted_1794511173024.jpg';
import perforated from '@/src/assets/images/autolab_material_leather_1794510358246.jpg';
import carbon from '@/src/assets/images/autolab_trim_carbon_fibre_1794511173303.jpg';
import poplar from '@/src/assets/images/autolab_trim_poplar_wood_1794511173150.jpg';
import walnut from '@/src/assets/images/autolab_trim_walnut_wood_1794511174478.jpg';
import lacquer from '@/src/assets/images/autolab_trim_piano_lacquer_1794511174129.jpg';

const photos:Record<string,string>={classic,'diamond-quilted':diamond,perforated,'carbon-fibre':carbon,'poplar-wood':poplar,'walnut-wood':walnut,'piano-lacquer':lacquer};
function Choices<T extends string>({label,options,value,onChange,disabled,images=false}:{label:string;options:OptionMetadata<T>[];value?:T;onChange:(id:T)=>void;disabled?:T;images?:boolean}) {
 return <div role="radiogroup" aria-label={label} onKeyDown={navigateRadio} className={`studio-options ${images?'studio-photo-options':''}`} style={{gridTemplateColumns:`repeat(${options.length===5?3:options.length},minmax(0,1fr))`}}>
   {options.map(option=><button key={option.id} type="button" role="radio" aria-label={option.label} aria-checked={value===option.id} tabIndex={value===option.id?0:-1} disabled={disabled===option.id} onClick={()=>onChange(option.id)} title={option.description}>
     {images?<img src={photos[option.id]} alt="" loading="lazy"/>:option.swatchHex?<span className="studio-swatch" style={{backgroundColor:option.swatchHex}}/>:null}
     <span className="studio-option-label">{option.label}</span><span className="studio-option-check" aria-hidden="true">{value===option.id?<Check size={13}/>:null}</span>
   </button>)}
 </div>;
}
export function StudioChoices(p:ConfigurationPanelProps & {step:ConfigurationStepId}) {
 const c=p.configuration;
 switch(p.step){
 case 'material':return <div className="studio-choice-content"><Choices label="Upholstery material" options={MATERIAL_OPTIONS} value={c.material} onChange={p.onChangeMaterial} images/><p className="studio-note">{MATERIAL_OPTIONS.find(o=>o.id===c.material)?.description}</p><p className="studio-caption">Illustrative samples · select a treatment to see it in the cabin.</p></div>;
 case 'colour':return <div className="studio-choice-content">
   <div className="studio-choice-heading"><span>Primary · seat centres</span><button type="button" className="studio-tone-toggle" aria-pressed={c.composition==='two-tone'} onClick={()=>p.onChangeComposition(c.composition==='two-tone'?'single-colour':'two-tone')}>{c.composition==='two-tone'?'Two-tone On':'Enable Two-tone'}</button></div>
   <Choices label="Primary hide colour" options={COLOUR_OPTIONS} value={c.primaryColour} onChange={p.onChangePrimaryColour}/>
   {c.composition==='two-tone'?<><p className="studio-caption">Secondary · bolsters, headrests & steering</p><Choices label="Secondary hide colour" options={COLOUR_OPTIONS} value={c.secondaryColour} disabled={c.primaryColour} onChange={p.onChangeSecondaryColour}/></>:<p className="studio-note">One colour across both seat zones and steering leather. Enable two-tone to separate them.</p>}
 </div>;
 case 'thread':return <div className="studio-choice-content"><Choices label="Accent thread colour" options={THREAD_OPTIONS} value={c.accentThread} onChange={p.onChangeThread}/><p className="studio-note">A quiet contrast or a distinct signature. Updates the stitching, including Diamond quilting.</p></div>;
 case 'composition':return <div className="studio-choice-content"><Choices label="Upholstery composition" options={COMPOSITION_OPTIONS} value={c.composition} onChange={p.onChangeComposition}/><p className="studio-note">{COMPOSITION_OPTIONS.find(o=>o.id===c.composition)?.description}</p><p className="studio-caption">Adjust both tones in Colour. Dashboard leather and console black/metal retain their finishes.</p></div>;
 case 'trim':return <div className="studio-choice-content"><Choices label="Cabin trim finish (illustrative preview)" options={TRIM_OPTIONS} value={c.trim} onChange={p.onChangeTrim} images/><p className="studio-note">{TRIM_OPTIONS.find(o=>o.id===c.trim)?.description}</p><p className="studio-caption">Shared finish on dashboard and console inserts. Illustrative preview.</p></div>;
 case 'illumination':return <div className="studio-choice-content"><Choices label="Ambient illumination mood (illustrative preview)" options={ILLUMINATION_OPTIONS} value={c.ambientIllumination} onChange={p.onChangeIllumination}/><p className="studio-note">A coloured light wash around the cabin. An illustrative mood, not an installed LED specification.</p></div>;
 }
}
