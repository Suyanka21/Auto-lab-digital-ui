"""Render an existing review camera without saving or modifying the master file."""
import argparse,json,sys,time
from pathlib import Path
import bpy

def main():
 p=argparse.ArgumentParser();p.add_argument('--camera',required=True);p.add_argument('--out',type=Path,required=True);p.add_argument('--samples',type=int,default=64);p.add_argument('--width',type=int,default=1440);p.add_argument('--height',type=int,default=1000);p.add_argument('--threads',type=int,default=4);p.add_argument('--neutral',action='store_true');a=p.parse_args(sys.argv[sys.argv.index('--')+1:])
 if min(a.samples,a.width,a.height,a.threads)<1:raise ValueError('Render settings must be positive')
 if a.out.suffix.lower()!='.png':raise ValueError('Use a PNG output path')
 if a.out.exists() or a.out.with_suffix('.json').exists():raise ValueError('Choose a new output filename; preserve previous evidence')
 camera=bpy.data.objects.get(a.camera)
 if camera is None or camera.type!='CAMERA':raise ValueError('Unknown review camera: '+a.camera)
 s=bpy.context.scene;s.camera=camera;s.render.engine='CYCLES';s.cycles.device='CPU';s.cycles.samples=a.samples;s.cycles.use_denoising=True;s.render.threads_mode='FIXED';s.render.threads=a.threads
 s.render.resolution_x=a.width;s.render.resolution_y=a.height;s.render.resolution_percentage=100;s.render.image_settings.file_format='PNG'
 if a.neutral:
  m=bpy.data.materials.new('REVIEW_ONLY_NEUTRAL');m.use_nodes=True;n=m.node_tree.nodes.get('Principled BSDF');n.inputs['Base Color'].default_value=(.24,.24,.24,1);n.inputs['Roughness'].default_value=.62;s.view_layers[0].material_override=m
 a.out.parent.mkdir(parents=True,exist_ok=True);s.render.filepath=str(a.out);start=time.monotonic();bpy.ops.render.render(write_still=True)
 record={'source':bpy.data.filepath,'blender':bpy.app.version_string,'camera':a.camera,'position':list(camera.location),'rotation':list(camera.rotation_euler),'samples':a.samples,'resolution':[a.width,a.height],'engine':'CYCLES','device':'CPU','denoising':True,'viewTransform':s.view_settings.view_transform,'look':s.view_settings.look,'exposure':s.view_settings.exposure,'neutralOverride':a.neutral,'wallSeconds':round(time.monotonic()-start,3),'sourceSaved':False}
 a.out.with_suffix('.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8');print(json.dumps(record,indent=2))
if __name__=='__main__':main()
