# Reference-led R3 shape construction. Mesh budget is spent on silhouette and cross-section.
def build_doors(env):
 import bpy, math
 from mathutils import Vector
 cv,finish,box=[env[k] for k in ('cv','finish','box')];F,K,S,C,M=[env[k] for k in ('F','K','S','C','M')]
 def rounded(poly,steps=3,f=.18):
  points=[]
  for i,p in enumerate(poly):
   prev=Vector(poly[i-1]);v=Vector(p);nxt=Vector(poly[(i+1)%len(poly)]);a=v.lerp(prev,f);b=v.lerp(nxt,f)
   for j in range(steps):
    t=j/(steps-1);points.append((1-t)**2*a+2*(1-t)*t*v+t*t*b)
  return points
 for sign in [-1,1]:
  for row,zc,W in [('Front',.16,1.15),('Rear',-.99,1.10)]:
   prefix=f'{row}_door_{sign}_';ref=f'approved_ai_design/0{1 if row=="Front" else 2}_{row.upper()}_DOOR_PANELS/PRIMARY';H=.67;Y=.30
   def world(u,v,d):return cv((sign*(.845-d),Y+v*H,zc+(.5-u)*W))
   def obj(name,verts,faces,mat):
    mesh=bpy.data.meshes.new(prefix+name);mesh.from_pydata(verts,[],faces);mesh.update();o=bpy.data.objects.new(prefix+name,mesh);bpy.context.collection.objects.link(o)
    for p in mesh.polygons:p.use_smooth=True
    bpy.ops.object.select_all(action='DESELECT');o.select_set(True);bpy.context.view_layer.objects.active=o
    bpy.ops.object.mode_set(mode='EDIT');bpy.ops.mesh.select_all(action='SELECT');bpy.ops.mesh.normals_make_consistent(inside=False);bpy.ops.object.mode_set(mode='OBJECT')
    # Open cosmetic surfaces must face into the cabin; Blender renders both sides by default.
    area=sum(p.area for p in mesh.polygons)
    weighted=sum(p.normal.x*p.area for p in mesh.polygons)/area if area else 0
    if weighted*sign>.05:
     bpy.ops.object.mode_set(mode='EDIT');bpy.ops.mesh.select_all(action='SELECT');bpy.ops.mesh.flip_normals();bpy.ops.object.mode_set(mode='OBJECT')
    o['runtime_material']=mat;o['design_reference']=ref
    return finish(o,prefix+name,mat,ref)
   def patch(name,outline,mat,depth=.025,bulge=.012,back=False):
    # Rounded edge and controlled convex face, with no flat extruded slab and bevel modifier stack.
    ring=rounded(outline);N=len(ring);centre=sum(ring,Vector((0,0)))/N;verts=[];faces=[]
    for scale,delta in [(1,0),(.965,.004),(.78,bulge)]:
     for p in ring:
      q=centre+(p-centre)*scale;verts.append(world(q.x,q.y,depth+delta))
    for j in range(2):
     for i in range(N):a=j*N+i;b=j*N+(i+1)%N;faces.append((a,b,b+N,a+N))
    verts.append(world(centre.x,centre.y,depth+bulge*1.13));idx=len(verts)-1
    for i in range(N):faces.append((2*N+i,2*N+(i+1)%N,idx))
    if back:
     k=len(verts)
     for p in ring:verts.append(world(p.x,p.y,depth-.012))
     for i in range(N):faces.append((i,k+i,k+(i+1)%N,(i+1)%N))
     faces.append(tuple(reversed(range(k,k+N))))
    return obj(name,verts,faces,mat)
   def ribbon(name,path,mat,radius=.0015,sides=6,samples=3,ellipse=1):
    # Catmull-Rom sweep through authored anchors, including variable cross-section support.
    points=[Vector(p[:3]) for p in path];radii=[p[3] if len(p)>3 else radius for p in path];seq=[]
    for i in range(len(points)-1):
     a=points[max(i-1,0)];b=points[i];c=points[i+1];d=points[min(i+2,len(points)-1)]
     for j in range(samples):
      t=j/samples;q=.5*((2*b)+(-a+c)*t+(2*a-5*b+4*c-d)*t*t+(-a+3*b-3*c+d)*t*t*t);rr=radii[i]*(1-t)+radii[i+1]*t;seq.append((q,rr))
    seq.append((points[-1],radii[-1]));verts=[];faces=[]
    for i,(p,rr) in enumerate(seq):
     tangent=seq[min(i+1,len(seq)-1)][0]-seq[max(i-1,0)][0];t=Vector((tangent.x*W,tangent.y*H));t.normalize();perp=Vector((-t.y,t.x))
     for j in range(sides):
      angle=j*2*math.pi/sides;u=p.x+perp.x*rr*math.cos(angle)/W;v=p.y+perp.y*rr*math.cos(angle)/H;depth=p.z+rr*ellipse*math.sin(angle);verts.append(world(u,v,depth))
    for i in range(len(seq)-1):
     for j in range(sides):a=i*sides+j;b=i*sides+(j+1)%sides;faces.append((a,b,b+sides,a+sides))
    faces += [tuple(reversed(range(sides))),tuple(range(len(verts)-sides,len(verts)))]
    return obj(name,verts,faces,mat)
   # Rounded front and distinctive rising rear wheel-arch edge. Camera sees both handings correctly.
   shell=[(.015,.86),(.045,.96),(.99,.985),(.99,.76),(.96,.38),(.90,.10),(.81,.015),(.18,0),(.055,.04),(.015,.16)] if row=='Front' else [(.015,.86),(.045,.96),(.99,.985),(.98,.78),(.89,.48),(.76,.15),(.68,.015),(.17,0),(.055,.04),(.015,.16)]
   patch('sculpted_shell',shell,K,.015,.009,True)
   patch('upper_padded_roll',[(.045,.84),(.985,.87),(.99,.985),(.075,.963),(.04,.91)],F,.035,.022)
   ribbon('window_seal',[(.045,.981,.045),(.50,.99,.044),(.99,1.0,.044)],K,.005,4,2)
   # Recessed fascia band: thin perimeter reveal rather than a solid chrome plate.
   patch('fascia_recess',[(.12,.83),(.96,.86),(.93,.73),(.27,.69),(.20,.72)],K,.027,.002)
   ribbon('fascia_metal_reveal',[(.135,.832,.047),(.20,.73,.047),(.28,.712,.047),(.85,.744,.047),(.92,.77,.047),(.948,.85,.047)],M,.0016,4,2)
   patch('decorative_trim',[(.40,.835),(.94,.852),(.912,.774),(.85,.758),(.45,.745)],C,.039,.004)
   # Bowl recessed behind the release, with a bounded surround and lever clearance.
   patch('release_bowl',[(.15,.826),(.36,.835),(.405,.751),(.26,.73),(.21,.742)],K,.029,.001)
   ribbon('release_surround',[(.15,.826,.048),(.36,.835,.048),(.405,.751,.048),(.26,.73,.048),(.21,.742,.048),(.15,.826,.048)],M,.0015,4,2)
   patch('release_lever',[(.255,.762),(.375,.774),(.36,.800),(.285,.792)],M,.059,.002)
   # Sculpted leather centre follows the sweep down into the armrest rather than a pentagonal plate.
   patch('leather_insert',[(.19,.43),(.25,.55),(.30,.63),(.42,.667),(.95,.70),(.92,.48),(.86,.37),(.42,.34),(.25,.37)],S,.042,.013)
   # Integrated lower armrest saddle, open underneath toward the pull recess.
   patch('armrest_saddle',[(.37,.44),(.64,.46),(.72,.49),(.89,.47),(.91,.40),(.87,.32),(.65,.31),(.49,.34),(.40,.36)],S,.082,.025)
   ribbon('integrated_pull_and_palmrest',[(.275,.615,.055,.025),(.29,.55,.073,.026),(.35,.455,.105,.028),(.46,.415,.13,.030),(.68,.418,.14,.039),(.87,.425,.116,.042),(.90,.43,.072,.028)],S,sides=8,samples=3,ellipse=1.25)
   # Small seam welt follows upholstery boundaries; stitch microdetail remains a master material effect.
   ribbon('insert_seam',[(.22,.426,.060),(.28,.56,.064),(.34,.615,.067),(.48,.637,.068),(.92,.664,.064)],S,.0009,4,2)
   ribbon('armrest_seam',[(.27,.60,.083),(.31,.51,.115),(.39,.43,.152),(.52,.399,.177),(.72,.404,.187),(.87,.414,.164)],S,.0008,4,2)
   # Hollow pocket: curved lower bin face returns into the panel at each end; opening has depth.
   pocket_end=.86 if row=='Front' else .71
   patch('lower_bin_face',[(.23,.05),(pocket_end,.045),(pocket_end+.035,.18),(pocket_end+.04,.245),(.37,.25),(.30,.22)],K,.072,.006)
   ribbon('pocket_upper_lip',[(.30,.22,.035),(.35,.245,.088),(.55,.246,.095),(pocket_end,.245,.084),(pocket_end+.035,.255,.029)],K,.004,4,2)
   # Visible inner floor/back, well below the lip; intentionally no solid top cap.
   verts=[world(.31,.10,.022),world(pocket_end,.10,.022),world(pocket_end,.10,.074),world(.31,.10,.074)];obj('pocket_inner_floor',verts,[(0,1,2,3)],K)
   # Thin circular speaker face with a subtle ring. No modelled bars or fake vertical fins.
   uc,vc=.16,.19;N=40;verts=[];faces=[]
   for rr,dd in [(.086,.055),(.083,.059),(.080,.059)]:
    for j in range(N):a=2*math.pi*j/N;verts.append(world(uc+rr*math.cos(a)/W,vc+rr*math.sin(a)/H,dd))
   for k in range(2):
    for j in range(N):a=k*N+j;b=k*N+(j+1)%N;faces.append((a,b,b+N,a+N))
   obj('speaker_metal_rim',verts,faces,M)
   verts=[world(uc,vc,.059)]+[world(uc+.080*math.cos(2*math.pi*j/N)/W,vc+.080*math.sin(2*math.pi*j/N)/H,.058) for j in range(N)];obj('speaker_perforated_face',verts,[(0,1+j,1+(j+1)%N) for j in range(N)],K)
   # Inset switch pod on the shelf. Four driver switches, one on other door panels.
   sw=4 if row=='Front' and sign==1 else 1
   patch('switch_recess',[(.34,.47),(.51,.474),(.50,.515),(.34,.51)],K,.078,.002)
   for j in range(sw):
    u=.355+j*.035;patch('window_switch_'+str(j),[(u,.48),(u+.026,.48),(u+.026,.498),(u,.498)],K,.087,.001)
   patch('lower_courtesy_lens',[(.67,.035),(.72,.038),(.72,.060),(.67,.058)],M,.083,.001)


