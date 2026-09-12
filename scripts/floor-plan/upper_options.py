"""Current first-floor concept aligned to the ground floor."""
import runpy
from pathlib import Path
state=runpy.run_path(str(Path(__file__).with_name('generate.py')))
g=state['room'].__globals__
# Retain the shared yard and parking drawing before starting the upper sheet.
site_context=list(g['p'][1:-1])
room,rect,line,txt,dh,dv,bed,sofa,bath,closet,dim=[state[n] for n in ('room','rect','line','txt','dh','dv','bed','sofa','bath','closet','dim')]
base='\n'.join(g['p']).split('<rect x="-27"')[0]
# Standalone sheet: use the house stylesheet, never embed the site plan.
raw=(Path(__file__).resolve().parents[2]/'public/floor-plan/plan.svg').read_text()
import xml.etree.ElementTree as ET
root=ET.fromstring(raw);ns='{http://www.w3.org/2000/svg}'
style=ET.tostring(root.find(ns+'style'),encoding='unicode')
def start(title):
 g['p']=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="-4 -6 55 54"><title>{title}</title>'+style+'<defs><marker id="a" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse"><path d="M0 0L10 5L0 10Z" fill="#637671"/></marker></defs>']
 rect(-4,-6,55,54,'#fcfbf5','none')
def label(x,y,title,size):txt(x,y,[title,size],.52)
def suite(x,depth,name,right=False,entry=None):
 room(x,0,14,depth,'#f7f1e6')
 bedroom_y=22
 service_y=14
 room(x,0,14,service_y,'#edf0e2')
 if right:
  label(x+7,6.4,'OPEN ROOF TERRACE','14′ × 14′')
  txt(x+7,7.8,'Open to sky',.38)
 else:
  label(x+7,6.4,'OPEN ROOF TERRACE','14′ × 14′')
  txt(x+7,7.8,'Open to sky',.38)
 # Move the complete service block down while retaining all inward door swings.
 g['p'].append(f'<g transform="translate(0 {service_y})">')
 if right:
  closet(x,0,right_entry=True);bath(x+6,0,True)
  rect(x+3.4,7.85,2.4,.3,'#fcfbf5','none');line(x+5.8,8,x+5.8,5.6,'thin')
  g['p'].append(f'<path d="M{x+3.4} 8A2.4 2.4 0 0 1 {x+5.8} 5.6" class="thin"/>')
  dh(x+6.25,8,2.4,True)
  line(x+6,8,x+6.25,8);line(x+6.25,7.86,x+6.25,8.14);line(x+8.65,7.86,x+8.65,8.14)
 else:
  bath(x,0);closet(x+8,0,left_entry=True)
  rect(x+5.35,7.85,2.4,.3,'#fcfbf5','none');line(x+7.75,8,x+7.75,5.6,'thin')
  g['p'].append(f'<path d="M{x+5.35} 8A2.4 2.4 0 0 1 {x+7.75} 5.6" class="thin"/>')
  line(x+7.75,8,x+8,8);line(x+5.35,7.86,x+5.35,8.14);line(x+7.75,7.86,x+7.75,8.14)
  dh(x+8.2,8,2.4,True)
 g['p'].append('</g>')
 # Service-room doors now lead directly into the bedroom.
 # Keep the original 14 × 14 bedrooms, shifted forward to the balconies.
 rect(x+.1,29.85,13.8,.3,'#f7f1e6','none')
 room(x,22,14,14,'#f7f1e6')
 bed(x+(6.3 if right else 1),25,right)
 label(x+(3.5 if right else 10),27,name,'14′ × 14′')
 txt(x+7,35,'196 sq ft',.4)
 dv(x if right else x+14,24,2.5,left=not right)
start('First floor · Front bedrooms and continuous covered gallery')
room(0,0,47,38,'#faf8ef');room(14,0,19,38,'#faf8ef')
suite(0,30,'BEDROOM 1');suite(33,30,'BEDROOM 2',True)
# The former center bedroom becomes a long open terrace.
room(14,0,19,14,'#e5ecd8')
line(14.35,.35,32.65,.35,'thin');line(14.35,.35,14.35,13.65,'thin')
line(32.65,.35,32.65,13.65,'thin');line(14.35,13.65,32.65,13.65,'thin')
label(23.5,5.6,'OPEN TERRACE','19′ × 14′ · 266 sq ft')
txt(23.5,7.1,'Open to sky · 3′ 6″ parapet',.4)
sofa(16,9.4,4.8,1.7);rect(28.5,9.5,2.2,2.2)
dh(23,14,2.8,True)
txt(24,16.8,'OPEN HALL',.48)
for x in (0,33):
 # 14-ft-wide by 8-ft-deep balconies are set flush with the south/front edge.
 room(x,36,14,8,'#e5ecd8');label(x+7,39.2,'COVERED BALCONY','14′ × 8′ · FRONT GALLERY')
 opening=x+5.5
 rect(opening,35.8,3,.4,'#faf8ef','none')
 for column in (x+.2,x+13.3):rect(column,43.1,.5,.5,'#a6b9a4','#637671',.06)
 txt(x+7,41.1,'Roof above · open sides',.38)
 txt(x+7,42.7,'CAR + BIKE BELOW',.34)
 for yy in (43.6,44):line(x,yy,x+14,yy,'thin')
rect(20.5,24,7,6,'#dcecef','#668c90',.12)
for x in (20.25,27.75):line(x,23.75,x,30.25,'thin')
for y in (23.75,30.25):line(20.25,y,27.75,y,'thin')
txt(24,26.3,['OPEN TO BELOW','TULSI · 7′ × 6′'],.46)
# One stacked L-shaped stairwell: ground to first, then first to roof.
g['p'].append('<path d="M14 28H17V35H20V38H14Z" fill="#ebece3" stroke="#304b42" stroke-width=".18"/>')
for i in range(8):line(14.2,28.3+i*.85,16.8,28.3+i*.85,'thin')
for i in range(3):line(17.2+i*.85,35.2,17.2+i*.85,37.8,'thin')
line(14,35,17,35,'thin');line(17,35,17,38,'thin')
rect(14.1,27.85,2.8,.3,'#faf8ef','none')
# Opposing arrows distinguish the flights above and below on the same footprint.
rect(19.85,35.2,.3,2.5,'#faf8ef','none')
g['p'].append('<path d="M19.2 36.2H15.2V29" class="thin" marker-end="url(#a)"/>')
g['p'].append('<path d="M15.8 29V36.8H19.2" class="thin" stroke-dasharray=".18 .12" marker-end="url(#a)"/>')
txt(15.5,37.6,'LANDING',.3)
txt(18.6,30.8,['L STAIRS','UP TO ROOF','DOWN TO GROUND'],.3)
txt(18.6,33.2,['SAME STAIRWELL','AS GROUND FLOOR'],.27)
txt(24.5,33,['UPPER HALL','Access around Tulsi void'],.43)
room(14,38,19,6,'#e5ecd8')
# Continuous gallery across the porch roof, with open side connections.
for x in (14,33):rect(x-.15,38.15,.3,5.6,'#e5ecd8','none')
rect(23,37.85,4,.3,'#faf8ef','none')
label(23.5,40.5,'COVERED FRONT GALLERY','19′ × 6′ · PORCH BELOW')
line(14,43.6,33,43.6,'thin')
for x in (17,28,36,42):rect(x,-.1,2.5,.2,'#dbe9e5','#7b8d80',.04)
for x,y in ((0,25),(47,20),(47,27)):rect(x-.1,y,.2,3,'#dbe9e5','#7b8d80',.04)
txt(23.5,46,'CONCEPT PLAN · Structure, balcony support and stair rise/run to be verified',.45)
for x in (0,14,33,47):line(x,-.4,x,-3,'thin')
dim(0,-3,47,-3,'47′ OVERALL');dim(0,-1.6,14,-1.6,'14′');dim(14,-1.6,33,-1.6,'19′');dim(33,-1.6,47,-1.6,'14′')
dim(-2,0,-2,38,'38′ MAIN BODY');txt(23.5,-4.8,'FIRST FLOOR · FRONT BEDROOMS + COVERED GALLERY',.65)
g['p'].append('</svg>')
out=Path(__file__).resolve().parents[2]/'public/floor-plan/upper-family.svg'
out.write_text(state['finish_svg']('\n'.join(g['p'])))
print(out)

# First-floor plot view shares the ground-floor yard and parking coordinates.
upper_parts=list(g['p'])
site_header=upper_parts[0].replace('viewBox="-4 -6 55 54"','viewBox="-27 -18 106 82"')
site_parts=[site_header,
 '<rect x="-27" y="-18" width="106" height="82" fill="#fcfbf5"/>',
 '<rect x="-20" y="-10" width="92" height="66" fill="#edf2e3" stroke="#738b65" stroke-width=".2"/>']
site_parts.extend(part for part in upper_parts[2:-1] if 'CONCEPT PLAN' not in part)
site_parts.extend(part.replace('Porch is within the 18′ front band','Covered front gallery above porch').replace('COVERED CAR BAY','CARPORT BELOW').replace('12′ BEYOND PORCH','12′ BEYOND GALLERY') for part in site_context)
site_parts.append('</svg>')
site_out=out.with_name('upper-site.svg')
site_out.write_text(state['finish_svg']('\n'.join(site_parts)))
print(site_out)

# Roof floor: a clear kite-flying terrace, separate tiled roof zones, and the
# same stair footprint that serves the levels below.
g['p']=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="-4 -6 55 53"><title>Roof terrace plan</title>'+style+'<defs><marker id="a" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse"><path d="M0 0L10 5L0 10Z" fill="#637671"/></marker></defs>']
rect(-4,-6,55,53,'#fcfbf5','none')
room(0,0,47,44,'#faf8ef')
# Hipped-tile roof footprints above enclosed upper-floor rooms.
for x,y,w,h,label_text in ((0,14,14,30,'LEFT ROOF'),(33,14,14,30,'RIGHT ROOF'),(14,0,19,14,'CENTER ROOF')):
 rect(x,y,w,h,'#dfad9c','#b78274',.12)
 txt(x+w/2,y+h/2,[label_text,'TERRACOTTA TILES'],.4)
# Open first-floor terraces below, mirrored at both outer corners.
for x in (0,33):
 rect(x,0,14,14,'#e5ecd8','#304b42',.18)
 line(x+.35,.35,x+13.65,.35,'thin');line(x+.35,.35,x+.35,13.65,'thin')
 line(x+13.65,.35,x+13.65,13.65,'thin');line(x+.35,13.65,x+13.65,13.65,'thin')
 txt(x+7,6.2,['FIRST-FLOOR TERRACE','14′ × 14′ BELOW'],.4)
# Tiled canopy across the porch joins the two extended side roofs.
rect(14,38,19,6,'#dfad9c','#b78274',.12)
txt(23.5,41,['PORCH ROOF','TERRACOTTA TILES'],.38)
# Main open roof terrace for kite flying: 19 x 24 less Tulsi void and stair.
rect(14,14,19,24,'#ece4d3','#304b42',.18)
for x in (14.35,32.65):line(x,14.35,x,37.65,'thin')
for y in (14.35,37.65):line(14.35,y,32.65,y,'thin')
txt(25.2,19.6,['OPEN KITE-FLYING TERRACE','Approx. 354 sq ft clear usable area'],.52)
txt(25.2,21.3,'Non-slip tile · 3′ 6″ parapet',.38)
# Tulsi void remains open through every level.
rect(20.5,24,7,6,'#dcecef','#668c90',.12)
txt(24,26.2,['OPEN TO BELOW','TULSI · 7′ × 6′'],.44)
# Aligned L stair to the roof, terminating at its roof-level landing.
g['p'].append('<path d="M14 28H17V35H20V38H14Z" fill="#ebece3" stroke="#304b42" stroke-width=".18"/>')
for i in range(8):line(14.2,28.3+i*.85,16.8,28.3+i*.85,'thin')
for i in range(3):line(17.2+i*.85,35.2,17.2+i*.85,37.8,'thin')
line(14,35,17,35,'thin');line(17,35,17,38,'thin')
g['p'].append('<path d="M15.5 37V29.2" class="thin" marker-end="url(#a)"/>')
txt(18.2,32.8,['ROOF STAIR','6′ × 10′'],.32)
# Simple kite / seating markers, kept out of the clear center.
g['p'].append('<path d="M29 31l1.2 1.2L29 33.4l-1.2-1.2Z" fill="#e7b36d" stroke="#788e81" stroke-width=".06"/><path d="M27.8 32.2h-2.2" class="thin" stroke-dasharray=".14 .1"/>')
rect(28,35,3.4,1.4,'#e3e1d5');txt(29.7,36.9,'SEATING',.3)
txt(23.5,47,'ROOF FLOOR · TILED ROOFS EXTEND TO FRONT PORCH',.52)
for x in (0,14,33,47):line(x,-.4,x,-3,'thin')
dim(0,-3,47,-3,'47′ OVERALL');dim(-2,0,-2,38,'38′ MAIN BODY');dim(49,38,49,44,'6′ FRONT ROOF EXTENSION')
g['p'].append('</svg>')
roof_out=out.with_name('terrace.svg')
roof_out.write_text(state['finish_svg']('\n'.join(g['p'])))
print(roof_out)
