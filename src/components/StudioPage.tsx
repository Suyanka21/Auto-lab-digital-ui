import { useState } from 'react';
import { ArrowUpRight } from 'lucide-react';
import { CONFIGURATION_STEPS } from '@/src/data/catalog';
import { useConfiguration } from '@/src/state/ConfigurationContext';
import type { ConfigurationStepId } from '@/src/types/configuration';
import { CabinViewer } from './CabinViewer';
import { CameraControls } from './CameraControls';
import { ConfigurationPanel } from './ConfigurationPanel';
import './studio-experience.css';
import './studio-samples.css';

export function StudioPage() {
 const state=useConfiguration();
 const [review,setReview]=useState(false);
 const selectStep=(step:ConfigurationStepId)=>{
   const currentIndex=CONFIGURATION_STEPS.findIndex(item=>item.id===state.activeStep);
   const nextIndex=CONFIGURATION_STEPS.findIndex(item=>item.id===step);
   setReview(false);state.setActiveStep(step);
   // Revisiting a choice must not move the cabin away from the user's current view.
   if(nextIndex>currentIndex)state.setActiveCamera(step==='thread'?'stitch-detail':step==='trim'||step==='illumination'?'cabin-pair':'driver-hero');
 };
 const move=(direction:number)=>{
   const index=CONFIGURATION_STEPS.findIndex(step=>step.id===state.activeStep);
   const next=CONFIGURATION_STEPS[index+direction];if(next)selectStep(next.id);
 };
 return <section className="studio-experience" data-component="StudioPage">
   <header className="studio-intro"><div><p className="studio-eyebrow">The Interior Studio</p><h1>Make it <em>personal.</em></h1></div><button type="button" onClick={()=>setReview(true)}>Your specification<ArrowUpRight size={16}/></button></header>
   <div className="studio-workspace">
     <div className="studio-stage"><CabinViewer {...state.configuration}/><CameraControls activeCamera={state.configuration.activeCamera} onSelectCamera={state.setActiveCamera}/></div>
     <ConfigurationPanel configuration={state.configuration} activeStep={state.activeStep} review={review} onCloseReview={()=>setReview(false)} onSelectStep={selectStep} onNextStep={()=>move(1)} onPreviousStep={()=>move(-1)} onReset={state.resetConfiguration} onOpenSpecification={()=>setReview(true)} onChangeMaterial={state.setMaterial} onChangePrimaryColour={state.setPrimaryColour} onChangeSecondaryColour={state.setSecondaryColour} onChangeThread={state.setAccentThread} onChangeComposition={state.setComposition} onChangeTrim={state.setTrim} onChangeIllumination={state.setAmbientIllumination}/>
   </div>
 </section>;
}
