from pathlib import Path
from html import escape
import xml.etree.ElementTree as ET
p=['''<svg xmlns="http://www.w3.org/2000/svg" viewBox="-4 -5 55 53" role="img" aria-labelledby="title"><title id="title">Residence floor plan, nominal dimensions in feet</title><defs><marker id="a" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse"><path d="M0 0L10 5L0 10Z" fill="#637671"/></marker></defs><style>text{font-family:Arial,sans-serif;fill:#28433c;paint-order:stroke fill;stroke:#fcfbf5;stroke-width:.12;stroke-linejoin:round}.wall{fill:none;stroke:#304b42;stroke-width:.18}.thin{fill:none;stroke:#788e81;stroke-width:.055}</style><rect x="-4" y="-5" width="55" height="53" fill="#fcfbf5"/>''']
def rect(x,y,w,h,fill='#fbf8ef',stroke='#7b8d80',sw=.055):p.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')
def line(x,y,xx,yy,cls='wall'):p.append(f'<path d="M{x} {y}L{xx} {yy}" class="{cls}"/>')
def txt(x,y,s,size=.5):
 for i,t in enumerate(s if isinstance(s,list) else [s]):p.append(f'<text x="{x}" y="{y+i*.68}" text-anchor="middle" font-size="{size}">{escape(t)}</text>')
def room(x,y,w,h,c):rect(x,y,w,h,c,'#304b42',.18)
def dh(x,y,w=2.4,n=False):
 rect(x,y-.15,w,.3,'#fcfbf5','none');d=-1 if n else 1;line(x,y,x,y+d*w,'thin');p.append(f'<path d="M{x+w} {y}A{w} {w} 0 0 {0 if n else 1} {x} {y+d*w}" class="thin"/>')
def dv(x,y,w=2.4,left=False):
 rect(x-.15,y,.3,w,'#fcfbf5','none');d=-1 if left else 1;line(x,y,x+d*w,y,'thin');p.append(f'<path d="M{x} {y+w}A{w} {w} 0 0 {1 if left else 0} {x+d*w} {y}" class="thin"/>')
def sink(x,y):
 rect(x,y,1.6,1);rect(x+.2,y+.15,1.2,.6);line(x+.8,y,x+.8,y+.35,'thin')
def wc(x,y):
 rect(x+.15,y,1.2,.4);p.append(f'<ellipse cx="{x+.75}" cy="{y+1}" rx=".6" ry=".7" fill="white" stroke="#7b8d80" stroke-width=".06"/>')
def shower(x,y,label=True):
 # Shower arm, rounded spray head, water spray and floor drain; no crossed box.
 line(x+1.35,y+.05,x+1.35,y+.55,'thin')
 p.append(f'<ellipse cx="{x+1.35}" cy="{y+.62}" rx=".55" ry=".18" fill="#dbe7df" stroke="#788e81" stroke-width=".065"/>')
 for offset in (-.4,0,.4):
  p.append(f'<path d="M{x+1.35+offset} {y+.92}l{offset*.6} .8" class="thin" stroke-dasharray=".12 .12"/>')
 p.append(f'<circle cx="{x+1.35}" cy="{y+2.05}" r=".17" class="thin"/>')
 if label: txt(x+1.35,y+2.65,'SHOWER',.34)
def bath(x,y,m=False,basin_bottom=False):
 room(x,y,8,8,'#e7efea');sx=x+4 if m else x;dx=x if m else x+4
 line(x+4,y,x+4,y+8);line(sx,y+4,sx+4,y+4)
 # Opposite toilet rotations put the cistern toward each exterior wall.
 toilet_cx=sx+1.95;toilet_cy=y+1.3
 p.append(f'<g transform="rotate({90 if m else -90} {toilet_cx} {toilet_cy})">')
 wc(sx+1.2,y+.45);p.append('</g>')
 p.append(f'<g transform="rotate(180 {sx+2} {y+5.95})">')
 shower(sx+.65,y+4.6,label=False);p.append('</g>')
 txt(sx+2,y+7.6,'SHOWER',.34)
 sink(dx+1.2,y+(6.5 if basin_bottom else .45))
 # Openings remain near the middle partition. Shower hinges at its lower end
 # and opens inward into the shower, mirrored between the bathrooms.
 dv(x+4,y+2.1,1.8,not m)
 rect(x+3.85,y+4.1,.3,1.8,'#fcfbf5','none')
 shower_leaf_x=x+5.8 if m else x+2.2
 line(x+4,y+5.9,shower_leaf_x,y+5.9,'thin')
 p.append(f'<path d="M{x+4} {y+4.1}A1.8 1.8 0 0 {1 if m else 0} {shower_leaf_x} {y+5.9}" class="thin"/>')
 txt(dx+2,y+3.4,['ATTACHED BATH','8′ × 8′'],.4);txt(dx+2,y+4.8,['WASHBASIN','4′ × 8′'],.34)
def closet(x,y,left_entry=False,right_entry=False):
 room(x,y,6,8,'#edf0e2')
 for a in (x+.3,x+4.4):
  entry_side=(left_entry and a==x+.3) or (right_entry and a==x+4.4)
  rect(a,y+.35,1.3,4.6 if entry_side else 5)
  for i in range(14 if entry_side else 15):line(a+.1,y+.5+i*.3,a+1.2,y+.5+i*.3,'thin')
 txt(x+3,y+3.2,['CLOSET','6′ × 8′'],.43)
def bed(x,y,e=False):
 rect(x,y,6.5,5);a=x+5.25 if e else x+.15
 rect(a,y+.25,1.05,2.1);rect(a,y+2.65,1.05,2.1);line(x+(5.05 if e else 1.45),y,x+(5.05 if e else 1.45),y+5,'thin')
 # Square bedside tables flanking the headboard, above and below in plan.
 table_x=x+5.5 if e else x
 rect(table_x,y-1.1,1,1);rect(table_x,y+5.1,1,1)
def sofa(x,y,w=6,h=2.5):
 rect(x,y,w,h)
 for i in range(3):rect(x+.18+i*(w-.36)/3,y+.4,(w-.36)/3,h-.6)
def swing(x,y,v=False):
 p.append(f'<g transform="translate({x} {y})'+(' rotate(90)' if v else '')+'">');rect(0,0,4,1.6)
 for i in range(5):line(.1,.2+i*.25,3.9,.2+i*.25,'thin')
 line(-.2,-.4,-.2,2,'thin');line(4.2,-.4,4.2,2,'thin');p.append('</g>')
def dim(x,y,xx,yy,s):
 p.append(f'<path d="M{x} {y}L{xx} {yy}" class="thin" marker-start="url(#a)" marker-end="url(#a)"/>')
 if y==yy:
  p.append(f'<text class="dimension-label" x="{(x+xx)/2}" y="{y}" dominant-baseline="middle" text-anchor="middle" font-size=".52">{escape(s)}</text>')
 else:
  p.append(f'<text class="dimension-label" transform="translate({x} {(y+yy)/2}) rotate(-90)" dominant-baseline="middle" text-anchor="middle" font-size=".52">{escape(s)}</text>')
def finish_svg(source):
 # Draw annotations last so later walls, windows and door arcs cannot overwrite text.
 root=ET.fromstring(source);ns='{http://www.w3.org/2000/svg}'
 labels=[]
 def collect(parent,transforms):
  for child in list(parent):
   local=transforms+([child.get('transform')] if child.get('transform') else [])
   if child.tag==ns+'text':
    parent.remove(child);child.attrib.pop('transform',None)
    group=ET.Element(ns+'g',{'transform':' '.join(local)})
    if child.get('class')=='dimension-label':
     size=float(child.get('font-size','.52'));width=len(child.text or '')*size*.57+.3
     x=float(child.get('x','0'));y=float(child.get('y','0'))
     ET.SubElement(group,ns+'rect',{'x':str(x-width/2),'y':str(y-.38),'width':str(width),'height':'.76','rx':'.1','fill':'#fcfbf5'})
    group.append(child);labels.append(group)
   else:collect(child,local)
 collect(root,[])
 for label in labels:root.append(label)
 ET.register_namespace('',ns[1:-1])
 return ET.tostring(root,encoding='unicode')
room(0,0,14,19,'#f7f1e6');room(0,19,14,19,'#f6f1e7');room(14,0,19,38,'#faf8ef');room(33,0,14,22,'#f7f1e6');room(33,22,14,16,'#f6f1e7');room(14,38,19,6,'#e9e5d7')
bath(0,0);closet(8,0,left_entry=True)
# Left attached bathroom: right-hinged door, opening inward.
rect(5.35,7.85,2.4,.3,'#fcfbf5','none');line(7.75,8,7.75,5.6,'thin')
p.append('<path d="M5.35 8A2.4 2.4 0 0 1 7.75 5.6" class="thin"/>')
line(7.75,8,8,8);line(5.35,7.86,5.35,8.14);line(7.75,7.86,7.75,8.14)
dh(8.2,8,2.4,True);bed(1,11)
rect(12.2,8.25,1.55,2.5,'#ece4d3');line(12.975,8.25,12.975,10.75,'thin');txt(12.9,11.35,'CABINET',.3)
txt(10.4,12.1,['SMALL MASTER','14′ × 11′','154 sq ft'],.45);rect(13.85,16,.3,2.5,'#fcfbf5','none');line(14,18.5,11.5,18.5,'thin')
p.append('<path d="M14 16A2.5 2.5 0 0 0 11.5 18.5" class="thin"/>')
closet(33,0,right_entry=True);bath(39,0,True)
# Mirrored closet entrance: right-end opening with right hinge, swinging inward.
rect(36.4,7.85,2.4,.3,'#fcfbf5','none');line(38.8,8,38.8,5.6,'thin')
p.append('<path d="M36.4 8A2.4 2.4 0 0 1 38.8 5.6" class="thin"/>')
dh(39.25,8,2.4,True)
# Retain a visible wall return and door jambs at the edge-mounted opening.
line(39,8,39.25,8);line(39.25,7.86,39.25,8.14);line(41.65,7.86,41.65,8.14)
bed(39.6,15.7,True)
rect(33.25,8.25,1.55,2.5,'#ece4d3');line(34.025,8.25,34.025,10.75,'thin');txt(34,11.35,'CABINET',.3)
rect(44.8,8.5,1.3,6);rect(43.2,10.5,1.25,1.4);txt(41.5,9.4,['WORKSPACE','6′ LONG'],.45)
txt(37.5,14,['LARGE MASTER','14′ × 14′ · 196 sq ft'],.48);dv(33,15.2,2.5)
room(14,0,5,7,'#eceee2');txt(16.5,3,['STORE','5′ × 7′']);rect(14.3,.3,3.2,.6);rect(14.3,3.4,.6,3.2)
room(14,7,5,7,'#e7efea')
# Toilet at northeast, shower centrally, basin beside the door on its right.
p.append('<g transform="rotate(90 17.85 8.25)">');wc(17.1,7.4);p.append('</g>')
p.append('<g transform="translate(.9 0) rotate(90 16.5 10.35)">');shower(15.15,9);p.append('</g>')
p.append('<g transform="rotate(90 17.95 13.1)">');sink(17.15,12.6);p.append('</g>')
txt(15.6,7.8,['COMMON BATH','5′ × 7′'],.36);dh(14.25,14,2.4,True)
line(14,14,14.25,14);line(14.25,13.86,14.25,14.14);line(16.65,13.86,16.65,14.14)
room(19,0,14,14,'#f0eee1')
# Store entry hinges at the lower end and opens inward into the store.
rect(18.85,4,.3,2.4,'#fcfbf5','none');line(19,6.4,16.6,6.4,'thin')
p.append('<path d="M19 4A2.4 2.4 0 0 0 16.6 6.4" class="thin"/>')
dh(19.25,0,3)
rect(19.19,-.15,.12,.3,'#304b42','none');rect(22.19,-.15,.12,.3,'#304b42','none')
rect(22.55,.4,10.05,2);rect(30.6,2.4,2,8)
# Joined double-basin sink at the northeast end of the kitchen counter.
rect(29.1,.7,3.2,1.4,'#fbf8ef')
rect(29.3,.95,1.25,.9,'none');rect(30.85,.95,1.25,.9,'none')
line(30.7,.72,30.7,1.15,'thin')
for x in (23.6,24.5):
 for y in (.9,1.8):p.append(f'<circle cx="{x}" cy="{y}" r=".26" class="thin"/>')
txt(26,7,['KITCHEN','14′ × 14′']);rect(23,13.8,5,.4,'#faf8ef','none')
# Cabinet rotated left and fridge rotated right, anchored to their bottom corners.
p.append('<g transform="translate(19.4 13.6) rotate(-90)">')
rect(0,0,3.5,2.2,'#ece4d3');line(1.75,0,1.75,2.2,'thin');p.append('</g>')
txt(20.5,12,'CABINET',.35)
p.append('<g transform="translate(32.6 10.6) rotate(90)">')
rect(0,0,3,2.3,'#e3e9e6','#647c70',.075);line(1.5,0,1.5,2.3,'thin')
line(1.33,1.7,1.33,2.1,'thin');line(1.67,1.7,1.67,2.1,'thin');p.append('</g>')
txt(31.45,12,'FRIDGE',.38)

dim(19,14.5,23,14.5,'4′');dim(28,14.5,33,14.5,'5′')
for x in (19,23,28,33):line(x,14,x,14.85,'thin')
txt(25.5,13.3,'5′ OPENING',.4)

p.append('<g transform="translate(1 1)">')
rect(17,15.6,4.8,2.6)
for x in (17.5,19.8):rect(x,14.9,1.2,.6);rect(x,18.2,1.2,.6)
p.append('</g>')
txt(20.4,20.2,'DINING');swing(22,22.4);txt(24,21.9,'SWING',.45)
p.append('<g transform="translate(0 2)">')
rect(20.5,22,7,6,'#b9dce2','#668c90',.1);rect(20.8,22.3,6.4,5.4,'none','#8eafb2',.05);txt(24,24.5,['TULSI','7′ × 6′'])
# Reference distances from Tulsi edges, inside the translated (+2 ft) group.
dim(14,23.5,20.5,23.5,'6′ 6″');dim(27.5,23.5,33,23.5,'5′ 6″')
dim(24,12,24,22,'10′ TO KITCHEN');dim(21,28,21,36,'8′ TO FRONT WALL')
# L-shaped staircase: lower flight enters from lobby, quarter-turn landing,
# then upper flight runs north. Geometry is schematic pending rise/run design.
rect(14,26,6,10,'#faf8ef','none')
p.append('<path d="M14 26H17V33H20V36H14Z" fill="#ebece3" stroke="#304b42" stroke-width=".18"/>')
for i in range(8):line(14.2,26.3+i*.85,16.8,26.3+i*.85,'thin')
for i in range(3):line(17.2+i*.85,33.2,17.2+i*.85,35.8,'thin')
line(14,33,17,33,'thin');line(17,33,17,36,'thin')
p.append('<path d="M19.2 34.5H15.5V27" class="thin" marker-end="url(#a)"/>')
txt(15.5,35.4,'LANDING',.32);txt(18.5,32.4,['L STAIRS','UP'],.34)
rect(19.85,33.2,.3,2.5,'#faf8ef','none')
dv(14,23.2,2.5,True)
# Three-sided C arrangement, open toward the TV, with square corner tables.
p.append('<g transform="translate(1 32) rotate(-90)">');sofa(0,0,6);p.append('</g>')
p.append('<g transform="translate(10.5 32) rotate(-90)">');sofa(0,0,6);p.append('</g>')
sofa(3.5,32,7)
rect(1,32,2.5,2.5,'#ece4d3');rect(10.5,32,2.5,2.5,'#ece4d3')
rect(1.2,32.2,2.1,2.1,'none');rect(10.7,32.2,2.1,2.1,'none')
rect(6,28,2.4,3.2);rect(5.3,17.8,3.3,.55)
txt(7,20.5,['MAIN LIVING','14′ × 19′'])
# Living-room dimensions, in feet; this group is shifted 2 ft with the front rooms.
dim(.1,19.25,13.9,19.25,'14′ ROOM WIDTH')
dim(.45,17,.45,36,'19′ ROOM DEPTH')
dim(13.6,25.7,13.6,36,'10.3′ DOOR TO WALL')
line(13.3,25.7,14,25.7,'thin');line(13.3,36,14,36,'thin')

# Pooja is outside the family room in the southeast corner of the central hall.
room(28,31,5,5,'#eee4cf')
# Open entrance on north wall; altar shifted to the opposite wall to keep entry clear.
rect(29.25,30.85,2.5,.3,'#fcfbf5','none')
line(29.25,30.86,29.25,31.14);line(31.75,30.86,31.75,31.14)
rect(28.6,34.7,3.8,.9);txt(30.5,33,['POOJA','5′ × 5′'],.4)
dv(33,25.5,2.5);sofa(39,32.5,6.8);rect(43.5,27,2.3,5);rect(38.5,28.5,3,2.4);txt(40,23,['FAMILY ROOM','14′ × 16′']);txt(39.5,24.6,'Pooja outside, near entrance',.37)
dh(22,36,2.2,True);rect(24.2,35.85,2.2,.3,'#fcfbf5','none');line(26.4,36,26.4,33.8,'thin');p.append('<path d="M24.2 36A2.2 2.2 0 0 1 26.4 33.8" class="thin"/>');txt(25,30.4,['CENTRAL HALL','19′ SECTION WIDTH'],.43)
swing(16.3,37,True);sofa(26,37,6);txt(18.4,40.5,'SWING',.4);txt(29,40.5,'COUCH',.4);txt(23.5,41.3,'PORCH 19′ × 6′')
for i in range(4):rect(21,42+i*.5,6,.5,'#efede2')
txt(23.5,45.2,'SOUTH · FRONT',.6)
p.append('</g>')
for x,y,w in [(2,0,3),(10,0,2),(25,0,3),(36,0,3),(42,0,3),(2,38,4),(8,38,3),(39,38,5)]:rect(x,y-.12,w,.24,'#dbe9e5','#7b8d80',.04)
for x,y,h in [(0,2,2),(0,9,2),(0,23,3),(0,31,3),(47,2,3),(47,7,3),(47,16,3),(47,29,3)]:rect(x-.12,y,.24,h,'#dbe9e5','#7b8d80',.04)
# Dashed outline of the first-floor gallery projected over the front yard.
for x in (0,33):
 p.append(f'<rect x="{x}" y="38" width="14" height="6" fill="none" stroke="#788e81" stroke-width=".07" stroke-dasharray=".3 .2"/>')
# Parking symbols: replace each right blue inset with a motorcycle icon.
for x in (.5,33.5):
 rect(x,38,13,6,'#fbfaf5','#637671',.09)
 rect(x+2,38.4,2.4,5.2,'#dce8e8')
 for wy in (38.85,43.15):
  p.append(f'<ellipse cx="{x+10.4}" cy="{wy}" rx=".18" ry=".42" fill="#637671"/>')
 rect(x+9.95,39.4,.9,3.2,'#e3e1d5','#637671',.06)
 rect(x+10.08,40.3,.64,1.6,'#9aab9b','#637671',.04)
 line(x+10.4,38.85,x+10.4,39.4,'thin');line(x+9.55,39.55,x+11.25,39.55,'thin')
 txt(x+6.5,41,['CAR + BIKE','UNDER GALLERY'],.32)
for x in (0,14,33,47):line(x,-.5,x,-3.8,'thin')
dim(0,-3.6,47,-3.6,'TOTAL WIDTH 47′');dim(0,-1.8,14,-1.8,'14′');dim(14,-1.8,33,-1.8,'19′');dim(33,-1.8,47,-1.8,'14′');txt(23.5,-.45,'NORTH · REAR',.5);dim(-2,0,-2,38,'38′ HOUSE');dim(49,38,49,44,'6′ PORCH');p.append('</svg>')
out=Path(__file__).resolve().parents[2]/'public/floor-plan/plan.svg';out.write_text(finish_svg('\n'.join(p)));print(out)
# Site boundary: 20 ft left, 25 ft right, 10 ft rear, 18 ft front including porch.
site='\n'.join(p).replace('viewBox="-4 -5 55 53"','viewBox="-27 -18 106 82"')
site=site.replace('<rect x="-4" y="-5" width="55" height="53" fill="#fcfbf5"/>','<rect x="-27" y="-18" width="106" height="82" fill="#fcfbf5"/><rect x="-20" y="-10" width="92" height="66" fill="#edf2e3" stroke="#738b65" stroke-width=".2"/>')
p=[site.removesuffix('</svg>')]
# Lawn and badminton occupy the existing side yards without changing the plot.
rect(-18,-4,16,38,'#9cbe7d','#718f56',.12)
txt(-10,18,['GREEN LAWN'],.95)
txt(-10,20,['LEFT-SIDE YARD'],.65)
# Nominal doubles playing lines: 20 ft wide by 44 ft long.
rect(49.5,-6,20,44,'#759f93','#f8fcf8',.10)
for x in (51,68):
 p.append(f'<path d="M{x} -6V38" fill="none" stroke="#f8fcf8" stroke-width=".08"/>')
for y in (-3.5,9.5,22.5,35.5):
 p.append(f'<path d="M49.5 {y}H69.5" fill="none" stroke="#f8fcf8" stroke-width=".08"/>')
p.append('<path d="M59.5 -6V9.5M59.5 22.5V38" fill="none" stroke="#f8fcf8" stroke-width=".08"/>')
p.append('<path d="M49 16H70" fill="none" stroke="#304b42" stroke-width=".16" stroke-dasharray=".3 .15"/>')
txt(59.5,12,['BADMINTON','20′ × 44′'],.8)

for x in (-20,72):line(x,-10,x,-15,'thin')
for y in (-10,56):line(72,y,77,y,'thin')
dim(-20,-14,72,-14,'PLOT WIDTH 92′');dim(76,-10,76,56,'PLOT DEPTH 66′')
dim(-20,33,0,33,'20′');dim(47,33,72,33,'25′')
dim(5,-10,5,0,'10′ REAR YARD')
dim(71,38,71,56,'18′ FRONT BAND');dim(35,44,35,56,'12′ BEYOND PORCH')
txt(23.5,-7,['REAR OPEN YARD'],.75)

txt(17,50,['FRONT OPEN YARD','Porch is within the 18′ front band'],.65)
txt(26,60,['92′ × 66′ PLOT · 6,072 SQ FT'],.9)
p.append('</svg>')
(out.parent/'site.svg').write_text(finish_svg('\n'.join(p)))
print(out.parent/'site.svg')
