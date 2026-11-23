import json
from pathlib import Path
r=Path(__file__).resolve().parents[2]
m=json.loads((r/'build_pipeline/contracts/src/config/scene-manifest.front-cabin.json').read_text())
m['assetId']='autolab-full-cabin-candidate'
m['status']='LOCAL REVIEW ONLY; provisional geometry; not production replacement'
m['sourceCommit']='0b91e7331ef67178b47cbc4dd799cfc6fed71e56'
m['sourceNodes']=m.pop('nodes')
m['nodes']=[n for n in m['sourceNodes'] if not n['identifier'].startswith('GEO_Console_')]
m['nodes'] += [{'identifier':'GEO_Seat_Stitching_Front_Passenger','allowedMaterialSlots':['MAT_Seat_Stitching']},{'identifier':'GEO_Console_Assembly','allowedMaterialSlots':['MAT_Console_Black','MAT_Console_Carbon','MAT_Console_Metal'],'notes':'Static console batches; original component nodes remain as provenance markers. No application material contract changes.'},{'identifier':'GEO_Cabin_Expansion','allowedMaterialSlots':['MAT_Seat_Primary','MAT_Seat_Secondary','MAT_Cockpit_Black','MAT_Dashboard_Trim','MAT_Console_Carbon','MAT_Console_Metal'],'notes':'Cumulative new components; component index recorded in Blender source and milestone JSON.'}]
m['coordinateFrame']={'units':'metres','up':'+Y','forward':'+Z','driverSide':'+X','floorY':0.27,'roofY':1.57,'rearSeatZ':-1.18,'dimensionStatus':'PROVISIONAL; baseline anchored/photo informed; not OEM measurements'}
m['preservation']={'materialNames':'unchanged','configurationBindings':'unchanged','productionFiles':'read-only hash guarded','threadMask':'original ORM alpha payload and baseline UVs retained','nodeBatching':'console-only; offline scene manifest expanded; source component provenance retained','drawCalls':'primitive count proxy; browser measurements NOT TESTED'}
(r/'build_pipeline/isolated/candidate-manifest.json').write_text(json.dumps(m,indent=2)+'\n')
