import { Check } from 'lucide-react';
import { COLOUR_OPTIONS, COMPOSITION_OPTIONS, ILLUMINATION_OPTIONS, MATERIAL_OPTIONS, THREAD_OPTIONS, TRIM_OPTIONS } from '@/src/data/catalog';
import type { ConfigurationStepId, OptionMetadata } from '@/src/types/configuration';
import type { ConfigurationPanelProps } from './ConfigurationPanel';
import { navigateRadio } from './selectors/radio-navigation';
import { MATERIAL_STUDIES, TRIM_STUDY_POSITION } from '@/src/data/editorial-images';
import type { CSSProperties } from 'react';
import type { MaterialId, TrimId } from '@/src/types/configuration';

type SampleKind = 'material' | 'colour' | 'thread' | 'composition' | 'trim' | 'light';
type SampleStyle = CSSProperties & { '--sample-colour'?: string; '--sample-position'?: string };

function Choices<T extends string>({label,options,value,onChange,disabled,kind}:{label:string;options:OptionMetadata<T>[];value?:T;onChange:(id:T)=>void;disabled?:T;kind:SampleKind}) {
 return <div role="radiogroup" aria-label={label} onKeyDown={navigateRadio} className={`studio-options sample-options sample-${kind}`}>
   {options.map((option,index)=><button key={option.id} type="button" role="radio" aria-label={option.label} aria-checked={value===option.id} tabIndex={value===option.id?0:-1} disabled={disabled===option.id} onClick={()=>onChange(option.id)} title={option.description}>
     {kind==='material'?<img className="material-tab-image" src={MATERIAL_STUDIES[option.id as MaterialId]} alt={`Illustrative ${option.label.toLowerCase()} texture`} loading="lazy"/>:
       <span aria-hidden="true" className={`sample-surface ${option.id==='two-tone'?'sample-split':''}`} style={{'--sample-colour':option.swatchHex,'--sample-position':kind==='trim'?TRIM_STUDY_POSITION[option.id as TrimId]:undefined} as SampleStyle}><span/></span>}
     <span className="sample-label-row"><span className="sample-number">0{index+1}</span><span className="studio-option-label">{option.label}</span></span>
     <span className="studio-option-check" aria-hidden="true">{value===option.id?<Check size={13}/>:null}</span>
   </button>)}
 </div>;
}
function TreatmentStudy({material}:{material:MaterialId}) {
 const selected=MATERIAL_OPTIONS.find(option=>option.id===material)!;
 return <figure className="treatment-study"><img key={material} src={MATERIAL_STUDIES[material]} alt={`AI-generated ${selected.label.toLowerCase()} leather study`} width="1254" height="1254" loading="lazy"/><figcaption><span>Texture study</span><strong>{selected.label}</strong></figcaption></figure>;
}
export function StudioChoices(p:ConfigurationPanelProps & {step:ConfigurationStepId}) {
 const c=p.configuration;
 switch(p.step){
 case 'material':return <div className="studio-choice-content treatment-content"><TreatmentStudy material={c.material}/><Choices label="Upholstery material" options={MATERIAL_OPTIONS} value={c.material} onChange={p.onChangeMaterial} kind="material"/><p className="studio-note">{MATERIAL_OPTIONS.find(o=>o.id===c.material)?.description}</p><p className="studio-caption">AI texture studies · selected colours appear in the live cabin.</p></div>;
 case 'colour':return <div className="studio-choice-content colour-content">
   <div className="studio-choice-heading"><span>Primary · seat centres</span><button type="button" className="studio-tone-toggle" aria-pressed={c.composition==='two-tone'} onClick={()=>p.onChangeComposition(c.composition==='two-tone'?'single-colour':'two-tone')}>{c.composition==='two-tone'?'Two-tone On':'Enable Two-tone'}</button></div>
   <p className="studio-caption">Eight digital colour studies · physical leather samples confirmed in consultation.</p>
   <Choices label="Primary hide colour" options={COLOUR_OPTIONS} value={c.primaryColour} onChange={p.onChangePrimaryColour} kind="colour"/>
   {c.composition==='two-tone'?<><p className="studio-caption">Secondary · bolsters, headrests & steering</p><Choices label="Secondary hide colour" options={COLOUR_OPTIONS} value={c.secondaryColour} disabled={c.primaryColour} onChange={p.onChangeSecondaryColour} kind="colour"/></>:<p className="studio-note">One colour across both seat zones and steering leather. Enable two-tone to separate them.</p>}
 </div>;
 case 'thread':return <div className="studio-choice-content"><Choices label="Accent thread colour" options={THREAD_OPTIONS} value={c.accentThread} onChange={p.onChangeThread} kind="thread"/><p className="studio-note">A quiet contrast or a distinct signature. Updates the stitching, including Diamond quilting.</p></div>;
 case 'composition':return <div className="studio-choice-content"><Choices label="Upholstery composition" options={COMPOSITION_OPTIONS} value={c.composition} onChange={p.onChangeComposition} kind="composition"/><p className="studio-note">{COMPOSITION_OPTIONS.find(o=>o.id===c.composition)?.description}</p><p className="studio-caption">Adjust both tones in Colour. Dashboard leather and console black/metal retain their finishes.</p></div>;
 case 'trim':return <div className="studio-choice-content"><Choices label="Cabin trim finish (illustrative preview)" options={TRIM_OPTIONS} value={c.trim} onChange={p.onChangeTrim} kind="trim"/><p className="studio-note">{TRIM_OPTIONS.find(o=>o.id===c.trim)?.description}</p><p className="studio-caption">AI material studies · illustrative finish on dashboard and console inserts.</p></div>;
 case 'illumination':return <div className="studio-choice-content"><Choices label="Ambient illumination mood (illustrative preview)" options={ILLUMINATION_OPTIONS} value={c.ambientIllumination} onChange={p.onChangeIllumination} kind="light"/><p className="studio-note">A coloured light wash around the cabin. An illustrative mood, not an installed LED specification.</p></div>;
 }
}
