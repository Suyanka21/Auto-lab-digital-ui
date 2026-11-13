import { Component, lazy, Suspense, useCallback, useState, type ReactNode } from 'react';
import type { CabinViewerProps } from '../types/configuration';
import { mapConfigurationToRuntime } from '../viewer/configuration-adapter';
import { CAMERA_OPTIONS, MATERIAL_OPTIONS } from '../data/catalog';
const Viewer = lazy(()=>import('../viewer/RuntimeViewer').then(module=>({default:module.RuntimeViewer})));
class ViewerCodeBoundary extends Component<{children:ReactNode},{failed:boolean}> {
  state={failed:false};
  static getDerivedStateFromError(){ return {failed:true}; }
  render(){ return this.state.failed ? <div role="alert" className="absolute inset-0 grid place-content-center gap-3 p-6 text-paper"><p>The 3D viewer could not start. Your selections are retained.</p><button className="min-h-[44px] underline" onClick={()=>window.location.reload()}>Reload showroom</button></div> : this.props.children; }
}
export function CabinViewer(props: CabinViewerProps) {
  const [status,setStatus]=useState('loading');
  const onStatus=useCallback((next:string)=>setStatus(next),[]);
  const onStats=useCallback(()=>{},[]);
  return <div className="relative w-full aspect-[4/3] sm:aspect-[16/9] bg-graphite overflow-hidden" data-component="CabinViewer" data-camera={props.activeCamera}>
    <ViewerCodeBoundary><Suspense fallback={<p role="status" className="absolute inset-0 grid place-content-center text-paper text-sm">Preparing your interior…</p>}>
      <Viewer {...mapConfigurationToRuntime(props)} onStatus={onStatus} onStats={onStats}/>
    </Suspense></ViewerCodeBoundary>
    <div className="absolute inset-x-0 top-0 z-20 flex justify-between gap-3 p-4 pointer-events-none text-[11px] text-paper bg-gradient-to-b from-graphite/90 to-transparent">
      <span className="uppercase tracking-[0.12em]">Your interior · Live 3D</span><span>{CAMERA_OPTIONS.find(c=>c.id===props.activeCamera)?.label}</span>
    </div>
    {status==='success' && <div className="absolute inset-x-0 bottom-0 z-20 flex justify-between gap-3 p-4 pointer-events-none text-[11px] text-paper bg-gradient-to-t from-graphite/90 to-transparent">
      <span>{MATERIAL_OPTIONS.find(m=>m.id===props.material)?.label} · Illustrative finish</span><span>Drag to explore · Pinch or scroll to zoom</span>
    </div>}
  </div>;
}
