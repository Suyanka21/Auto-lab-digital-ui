# New reference-led door geometry. Imported by build_cabin_r2.py; no baseline edits.
def build_doors(env):
    import bpy, math
    from mathutils import Vector
    from mathutils.geometry import tessellate_polygon
    cv,finish,box,disc=[env[k] for k in ('cv','finish','box','disc')]
    F,K,S,C,M=[env[k] for k in ('F','K','S','C','M')]
    def panel(name,sign,z,length,outline,x,depth,mat,ref,bevel=.009):
        # Outline points (longitudinal fraction, absolute height); thin extruded cosmetic panel.
        points=[cv((sign*x,h,z+u*length)) for u,h in outline]; n=len(points)
        verts=[tuple(p) for p in points]+[tuple(p+Vector((sign*depth,0,0))) for p in points]
        triangles=tessellate_polygon([points]); lookup={tuple(p):i for i,p in enumerate(points)}
        faces=[]
        for t in triangles:
            ids=[v if isinstance(v,int) else lookup[tuple(v)] for v in t];faces += [tuple(ids),tuple(i+n for i in reversed(ids))]
        faces += [(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)]
        mesh=bpy.data.meshes.new(name);mesh.from_pydata(verts,[],faces);mesh.update()
        obj=bpy.data.objects.new(name,mesh);bpy.context.collection.objects.link(obj)
        bpy.ops.object.select_all(action='DESELECT');obj.select_set(True);bpy.context.view_layer.objects.active=obj
        bpy.ops.object.mode_set(mode='EDIT');bpy.ops.mesh.select_all(action='SELECT');bpy.ops.mesh.normals_make_consistent(inside=False);bpy.ops.object.mode_set(mode='OBJECT')
        if bevel:
            mod=obj.modifiers.new('Soft panel edges','BEVEL');mod.width=bevel;mod.segments=2;mod.limit_method='ANGLE';bpy.ops.object.modifier_apply(modifier=mod.name)
            for p in mesh.polygons:p.use_smooth=True
            mod=obj.modifiers.new('Weighted surface normals','WEIGHTED_NORMAL');mod.keep_sharp=True;bpy.ops.object.modifier_apply(modifier=mod.name)
        return finish(obj,name,mat,ref)
    def cord(name,points,r,mat,ref):
        data=bpy.data.curves.new(name,'CURVE');data.dimensions='3D';data.bevel_depth=r;data.bevel_resolution=1;data.resolution_u=3
        sp=data.splines.new('BEZIER');sp.bezier_points.add(len(points)-1)
        for b,p in zip(sp.bezier_points,points):b.co=cv(p);b.handle_left_type='AUTO';b.handle_right_type='AUTO'
        o=bpy.data.objects.new(name,data);bpy.context.collection.objects.link(o);bpy.ops.object.select_all(action='DESELECT');o.select_set(True);bpy.context.view_layer.objects.active=o;bpy.ops.object.convert(target='MESH')
        return finish(bpy.context.object,name,mat,ref)
    for sign in [-1,1]:
      for row,z,length in [('Front',.16,1.15),('Rear',-.99,1.10)]:
        key=f'{row}_door_{sign}_';ref=f'approved_ai_design/0{1 if row=="Front" else 2}_{row.upper()}_DOOR_PANELS/PRIMARY'
        # Lower rear edge tapers around the wheel arch on rear doors.
        outline=[(-.49,.98),(.47,.98),(.50,.90),(.48,.40),(.40,.32),(.30,.30),(-.30,.30),(-.43,.35),(-.48,.48)] if row=='Front' else [(-.49,.98),(.47,.98),(.50,.90),(.48,.40),(.40,.32),(.29,.30),(-.18,.30),(-.28,.39),(-.38,.57),(-.48,.73)]
        panel(key+'shell',sign,z,length,outline,.823,.032,K,ref,.014)
        panel(key+'padded_upper',sign,z,length,[(-.46,.925),(.47,.925),(.47,.982),(-.46,.982)],.795,.035,F,ref,.014)
        panel(key+'trim_frame',sign,z,length,[(-.43,.84),(.37,.84),(.40,.902),(-.43,.902)],.788,.021,M,ref,.006)
        panel(key+'decorative_insert',sign,z,length,[(-.40,.852),(.10,.852),(.15,.89),(-.40,.89)],.780,.014,C,ref,.007)
        panel(key+'upholstered_middle',sign,z,length,[(-.40,.61),(.35,.61),(.27,.705),(.13,.815),(-.42,.815)],.767,.038,S,ref,.023)
        # Broad ledge with lower return and a substantial upholstered pull.
        box(key+'armrest',(sign*.72,.604,z-.035),(.17,.075,length*.68),S,.025,ref)
        cord(key+'grab_handle',[(sign*.70,.616,z-.03),(sign*.68,.645,z+.13),(sign*.70,.735,z+.25),(sign*.75,.79,z+.28)],.022,S,ref)
        box(key+'handle_recess',(sign*.776,.871,z+.285),(.028,.055,.18),K,.012,ref)
        box(key+'release_handle',(sign*.75,.857,z+.285),(.015,.016,.115),M,.006,ref)
        # Open storage: lower floor and outward lip, backed by the shell; no solid block fill.
        box(key+'pocket_floor',(sign*.764,.375,z-.08),(.12,.025,length*.49),K,.009,ref)
        panel(key+'pocket_lip',sign,z,length,[(-.31,.36),(.16,.36),(.19,.43),(.13,.465),(-.30,.465)],.699,.018,K,ref,.01)
        for u in [-.30,.16]:box(key+'pocket_end',(sign*.76,.409,z+u*length),(.10,.07,.018),K,.008,ref)
        speaker=(sign*.777,.425,z+.34*length)
        disc(key+'speaker_rim',speaker,.091,.012,M,ref=ref)
        disc(key+'speaker_grille',(sign*.767,.425,z+.34*length),.085,.013,K,ref=ref)
        # Sparse geometric grille ribs; micro perforation is intentionally deferred, no new texture slot.
        for j in range(-5,6):
            dz=j*.013;half=math.sqrt(.078**2-dz**2)
            box(key+'speaker_rib_'+str(j),(sign*.758,.425,z+.34*length+dz),(.003,half*2,.0028),K,.0005,ref)
        switches=4 if row=='Front' and sign==1 else 1
        box(key+'switch_pod',(sign*.709,.648,z+.10),(.073,.02,.115 if switches==4 else .05),K,.008,ref)
        for j in range(switches):box(key+'window_switch_'+str(j),(sign*.707,.662,z+.13-j*.026),(.036,.008,.018),K,.002,ref)
        if switches==4:
            disc(key+'mirror_control',(sign*.71,.661,z+.19),.012,.007,K,axis='Y',ref=ref)

