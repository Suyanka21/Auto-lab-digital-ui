import { useRef, type TouchEvent } from 'react';
import { ArrowLeft, ArrowRight, RotateCcw } from 'lucide-react';
import { CONFIGURATION_STEPS } from '@/src/data/catalog';
import type { CabinConfiguration, ColourId, CompositionId, ConfigurationStepId, IlluminationId, MaterialId, ThreadId, TrimId } from '@/src/types/configuration';
import { StudioChoices } from './StudioChoices';
import { SpecificationSummary } from './SpecificationSummary';

export interface ConfigurationPanelProps {
  review: boolean;
  onCloseReview: () => void;
  configuration: CabinConfiguration;
  activeStep: ConfigurationStepId;
  onSelectStep: (step: ConfigurationStepId) => void;
  onNextStep: () => void;
  onPreviousStep: () => void;
  onReset: () => void;
  onOpenSpecification: () => void;
  onChangeMaterial: (material: MaterialId) => void;
  onChangePrimaryColour: (colour: ColourId) => void;
  onChangeSecondaryColour: (colour: ColourId) => void;
  onChangeThread: (thread: ThreadId) => void;
  onChangeComposition: (composition: CompositionId) => void;
  onChangeTrim: (trim: TrimId) => void;
  onChangeIllumination: (illumination: IlluminationId) => void;
}


/** A single sliding control rail. The live cabin is its stable sibling, never remounted. */
export function ConfigurationPanel(props: ConfigurationPanelProps) {
  const {configuration, activeStep, review, onSelectStep, onNextStep, onPreviousStep, onReset, onOpenSpecification, onCloseReview} = props;
  const index = review ? CONFIGURATION_STEPS.length : Math.max(0, CONFIGURATION_STEPS.findIndex(s=>s.id===activeStep));
  const heading = useRef<HTMLHeadingElement>(null);
  const gesture = useRef<{x:number;y:number}|null>(null);
  const next = () => index < 5 ? onNextStep() : onOpenSpecification();
  const previous = () => review ? onCloseReview() : onPreviousStep();
  const startSwipe = (event:TouchEvent) => {
    if (event.touches.length !== 1 || (event.target as HTMLElement).closest('button,a,input')) { gesture.current=null; return; }
    gesture.current={x:event.touches[0].clientX,y:event.touches[0].clientY};
  };
  const endSwipe = (event:TouchEvent) => {
    const start=gesture.current;gesture.current=null;
    if(!start || !event.changedTouches.length)return;
    const dx=event.changedTouches[0].clientX-start.x,dy=event.changedTouches[0].clientY-start.y;
    if(Math.abs(dx)<60 || Math.abs(dx)<Math.abs(dy)*1.5)return;
    if(dx<0 && !review)next(); else if(dx>0 && index>0)previous();
  };
  const edit = (step:ConfigurationStepId) => {onSelectStep(step);heading.current?.focus({preventScroll:true});};
  return <section className="studio-panel" data-component="ConfigurationPanel" aria-label="Interior configuration">
    <nav className="studio-chapters" aria-label="Configuration steps">
      {CONFIGURATION_STEPS.map((step,i)=><button key={step.id} type="button" aria-label={`${step.index} ${step.label}`} title={step.label} aria-current={index===i?'step':undefined} onClick={()=>onSelectStep(step.id)}><span>{step.index}</span><span className="chapter-label">{step.label}</span></button>)}
    </nav>
    <header className="studio-panel-heading" onTouchStart={startSwipe} onTouchEnd={endSwipe} onTouchCancel={()=>{gesture.current=null;}}>
      <div><p className="studio-eyebrow">{review?'Your interior':`${CONFIGURATION_STEPS[index].classification==='illustrative'?'Illustrative preview':'Sample selection'} · ${index+1} / 6`}</p><h2 ref={heading} tabIndex={-1}>{review?'The final composition.':CONFIGURATION_STEPS[index].label}</h2></div>
      <button className="studio-reset" type="button" onClick={()=>{onReset();onCloseReview();}} aria-label="Reset configuration" title="Reset configuration"><RotateCcw size={16}/></button>
    </header>
    <div className="studio-slide-window" onTouchStart={startSwipe} onTouchEnd={endSwipe} onTouchCancel={()=>{gesture.current=null;}}>
      <div className="studio-slide-track" style={{transform:`translateX(-${index*100}%)`}}>
        {CONFIGURATION_STEPS.map((step,i)=><section key={step.id} className="studio-slide" aria-label={`${step.label} choices`} aria-hidden={index!==i} inert={index!==i || undefined}>
          <StudioChoices {...props} step={step.id}/>
        </section>)}
        <section className="studio-slide studio-review" aria-label="Review specification" aria-hidden={!review} inert={!review || undefined}><SpecificationSummary configuration={configuration} onEditStep={edit}/></section>
      </div>
    </div>
    <footer className="studio-panel-footer">
      <button type="button" className="studio-back" onClick={previous} disabled={index===0} aria-label="Previous step"><ArrowLeft size={18}/><span>Back</span></button>
      {review?<button type="button" className="studio-next" onClick={()=>onSelectStep('material')}>Keep exploring<ArrowRight size={18}/></button>:<button type="button" className="studio-next" onClick={next}>{index===5?'Review Specification':`Continue to ${CONFIGURATION_STEPS[index+1].label}`}<ArrowRight size={18}/></button>}
    </footer>
  </section>;
}
