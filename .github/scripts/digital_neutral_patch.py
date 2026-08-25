from pathlib import Path
p=Path('index.html')
text=p.read_text(encoding='utf-8')
old="const add=(title,list,color,role)=>{ if(!list.length) return; const lab=document.createElement('div'); lab.className='groupTitle'; lab.textContent=title; col.appendChild(lab); list.forEach(c=>{ const b=document.createElement('button'); b.type='button'; b.className='courseBtn'; b.style.setProperty('--c',color); if(role!=='core'){ b.style.background='#d7dde8'; b.style.color='#111722'; b.style.borderColor='#eef1f5'; }"
new="const add=(title,list,color,role)=>{ if(!list.length) return; const lab=document.createElement('div'); lab.className='groupTitle'; lab.textContent=title; col.appendChild(lab); list.forEach(c=>{ const b=document.createElement('button'); b.type='button'; b.className='courseBtn'; b.style.setProperty('--c',color); if(role!=='core'||activeTrack==='digital'){ b.style.background='#d7dde8'; b.style.color='#111722'; b.style.borderColor='#eef1f5'; }"
if old not in text: raise SystemExit('renderGrid add block not found')
text=text.replace(old,new,1)
old="add(activeTrack==='digital'?'Computer · Tech':'Core branch', data.core, COLORS[activeTrack], 'core');"
new="add(activeTrack==='digital'?'Computer · Tech':'Core branch', data.core, activeTrack==='digital'?COLORS.neutral:COLORS[activeTrack], 'core');"
if old not in text: raise SystemExit('digital grid call not found')
text=text.replace(old,new,1)
old="TRACKS[track].core.forEach(id=>rootGroup.add(createNode(courseMap[id],{track,role:'core',core:true,color:TRACKS[track].color})));"
new="TRACKS[track].core.forEach(id=>rootGroup.add(createNode(courseMap[id],{track,role:'core',core:track!=='digital',color:track==='digital'?COLORS.neutral:TRACKS[track].color})));"
if old not in text: raise SystemExit('core scene creation not found')
text=text.replace(old,new,1)
text=text.replace("regular?.88:0","regular ? .88 : 0").replace("regular?.22:0","regular ? .22 : 0")
p.write_text(text,encoding='utf-8')
print('digital filter neutralized')
