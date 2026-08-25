from pathlib import Path
import re
import sys

p = Path('index.html')
text = p.read_text(encoding='utf-8')
marker = '<!-- readability-tech-fix-2026-08-25 -->'
if marker in text:
    print('Patch already applied')
    sys.exit(0)

def sub(pattern, repl, label, flags=0):
    global text
    text2, n = re.subn(pattern, repl, text, count=1, flags=flags)
    if n != 1:
        raise SystemExit(f'{label}: expected 1 match, got {n}')
    text = text2

def replace(old, new, label):
    global text
    if old not in text:
        raise SystemExit(f'{label}: expected text missing')
    text = text.replace(old, new, 1)

# ---- UI: fifth filter button, but it is not part of the four major-track overview ----
replace(
    '.trackBtn[data-track="mobility"]{--track:var(--violet)}',
    '.trackBtn[data-track="mobility"]{--track:var(--violet)}.trackBtn[data-track="digital"]{--track:#39caff}',
    'digital button color'
)
replace(
    '<button class="trackBtn" data-track="mobility" type="button">자동차 · 미래모빌리티</button></div></div>',
    '<button class="trackBtn" data-track="mobility" type="button">자동차 · 미래모빌리티</button><button class="trackBtn" data-track="digital" type="button">컴퓨터 · 테크</button></div></div>',
    'digital button'
)
replace(
    '<div style="color:var(--violet)"><i></i>모빌리티 중심 가지</div></div>',
    '<div style="color:var(--violet)"><i></i>모빌리티 중심 가지</div><div style="color:#39caff"><i></i>컴퓨터 · 테크 필터</div></div>',
    'digital legend'
)

# ---- extra mobile/readability CSS ----
extra_css = r'''
<style>
/* readability-tech-fix-2026-08-25 */
.semHud{display:block!important;top:0!important;bottom:0!important;height:100%!important}
.semHud .semTag{position:absolute;left:0;right:0;transform:translateY(-50%);margin:0;transition:top .12s linear}
.semHud .semTag strong{display:block;font-size:16px;line-height:1.05;letter-spacing:-.03em}
.semHud .semTag small{font-size:11px;line-height:1.15;margin-top:5px}
.courseBtn strong{font-size:15px}.courseBtn small{font-size:11px}
@media(max-width:720px){
  .sceneWrap{min-height:900px}
  canvas{height:900px;width:calc(100% - 104px);margin-left:104px}
  .semHud{width:98px!important;left:3px!important}
  .semHud div{font-size:16px!important;padding:10px 8px!important;border-radius:14px!important}
  .semHud small{font-size:11px!important}
}
@media(max-width:430px){
  .sceneWrap{min-height:900px}
  canvas{height:900px;width:calc(100% - 100px);margin-left:100px}
  .semHud{width:94px!important;left:3px!important}
}
</style>
'''
replace('</head>', extra_css + marker + '\n</head>', 'readability css')

# ---- Data: computer / technology-only filter ----
sub(
    r'^const TRACKS=.*?;$',
    '''const TRACKS={"product":{"label":"제품디자인","color":"#ff43ce","core":["style","bp1","bp2","prod1","prod2","eye1","eye2","ps1","ps2"],"support":["idea","fab","tech","ds1","ds2","ds3","portfolio","cap1","cap2"]},"ux":{"label":"UX · UI · 서비스","color":"#baff39","core":["newmedia","ux","ui","pub1","pub2"],"support":["pres","cont3d","tech","img3d","col","portfolio","cap1","cap2"]},"space":{"label":"공간 · 환경","color":"#ff9f38","core":["be1","be2","env1","env2","pub1","pub2","es1","es2","spacework"],"support":["fab","tech","col","portfolio","cap1","cap2"]},"mobility":{"label":"자동차 · 미래모빌리티","color":"#9a78ff","core":["style","bm","mob1","mob2","ms1","ms2"],"support":["idea","cont3d","tech","img3d","ds1","ds2","ds3","portfolio","cap1","cap2"]},"digital":{"label":"컴퓨터 · 테크","color":"#39caff","core":["2d","3d","newmedia","fab","cont3d","tech","ds1","img3d","ds2","ds3","ui"],"support":[]}};''',
    'TRACKS',
    re.M
)
replace("const TRACK_ORDER=['product','ux','space','mobility'];", "const TRACK_ORDER=['product','ux','space','mobility','digital'];", 'TRACK_ORDER')
replace(
    "const COLORS={common:'#d7dde8',neutral:'#d7dde8',product:'#ff43ce',ux:'#baff39',space:'#ff9f38',mobility:'#9a78ff'};",
    "const COLORS={common:'#d7dde8',neutral:'#d7dde8',product:'#ff43ce',ux:'#baff39',space:'#ff9f38',mobility:'#9a78ff',digital:'#39caff'};",
    'COLORS'
)

# ---- Semester HUD: use actual projected Y positions instead of space-between ----
sub(
    r"semHud\.innerHTML=.*?;\n",
    "semHud.innerHTML=SEMS.map((s,i)=>`<div class=\"semTag\" data-sem=\"${s}\"><strong>${s.replace('-','학년 ')}학기</strong><small>${i<2?'공통 기반':i<4?'분기 시작':i<6?'전공 심화':'시스템·포트폴리오'}</small></div>`).join('');\n",
    'semHud markup'
)

# ---- Overview copy includes a separate filter description ----
sub(
    r"function setOverview\(\)\{.*?\n(?=function groupedForTrack)",
    '''function setOverview(){ const copy={ all:{title:'전체 브랜치 로드맵',desc:'전체 보기에서는 제품, UX·UI·서비스, 공간·환경, 자동차·미래모빌리티의 4개 전공트랙만 펼쳐집니다. 컴퓨터·테크 관련 교과는 상단의 별도 필터에서 따로 볼 수 있습니다.',keywords:['공통 기반','4개 전공트랙','브랜치 비교','학기 흐름'],note:'전체 보기에서는 실제 전공트랙 네 개의 핵심 과목만 비교합니다. 컴퓨터·테크는 전공트랙과 혼합하지 않고 별도 보기로 분리했습니다.'}, product:{title:'제품디자인 브랜치',desc:'제품디자인 브랜치는 기초스타일스튜디오와 기초제품디자인에서 출발해 제품 종합설계, 아이웨어, 제품시스템디자인으로 이어집니다. 디지털 제작과 포트폴리오 과목이 주변 베이스 가지로 연결됩니다.',keywords:['기초제품디자인','제품 종합설계','아이웨어','제품시스템디자인'],note:'제품디자인 핵심 과목은 분홍색 Core로, 트랙을 보조하는 과목은 밝은 회색으로 표시됩니다.'}, ux:{title:'UX · UI · 서비스 브랜치',desc:'UX 브랜치는 뉴미디어콘텐츠기획과 UX디자인에서 시작해 인터페이스디자인과 공공디자인으로 이어집니다.',keywords:['뉴미디어','UX디자인','인터페이스디자인','공공디자인'],note:'UX 트랙의 핵심 과목은 연두색 Core로, 표현·콘텐츠·리서치 과목은 밝은 회색으로 표시됩니다.'}, space:{title:'공간 · 환경 브랜치',desc:'공간·환경 브랜치는 기초환경디자인에서 환경디자인 종합설계, 공공디자인, 환경시스템디자인, 공간디자인워크샵으로 발전합니다.',keywords:['기초환경디자인','환경디자인 종합설계','공공디자인','환경시스템디자인'],note:'공간·환경 핵심 과목은 주황색 Core로 표시됩니다.'}, mobility:{title:'자동차 · 미래모빌리티 브랜치',desc:'모빌리티 브랜치는 스타일링과 기초모빌리티디자인에서 출발해 모빌리티 종합설계와 모빌리티시스템디자인으로 이어집니다.',keywords:['기초모빌리티','모빌리티 종합설계','모빌리티시스템디자인','스타일링'],note:'모빌리티 핵심 과목은 보라색 Core로 표시됩니다.'}, digital:{title:'컴퓨터 · 테크 관련 교과',desc:'디지털2D디자인, 디지털3D디자인, 뉴미디어콘텐츠기획, 디지털패브리케이션, 3D콘텐츠디자인, 디자인과테크놀로지, 디지털디자인스튜디오, 디지털3D영상기법, 인터페이스디자인 등 컴퓨터·디지털 제작·기술 관련 교과만 모아 보여줍니다.',keywords:['디지털2D·3D','3D콘텐츠','패브리케이션','디자인과테크놀로지'],note:'이 보기는 정식 전공트랙이 아니라 컴퓨터·테크 관련 교과를 빠르게 찾아보기 위한 별도 필터입니다.'} }[activeTrack]; chips.innerHTML=`<span class="chip">${activeTrack==='all'?'전체 펼침':TRACKS[activeTrack].label}</span><span class="chip">1학년 → 4학년</span>`; detailTitle.textContent=copy.title; detailDesc.textContent=copy.desc; keywordList.innerHTML=copy.keywords.map(v=>`<span class="badge2">${v}</span>`).join(''); pathNote.textContent=copy.note; }
''',
    'setOverview',
    re.S
)

# Digital filter should show ONLY the digital/tech set; no generic foundation duplicates.
sub(
    r"function groupedForTrack\(track\)\{.*?\n(?=function renderGrid)",
    '''function groupedForTrack(track){ const bySem=Object.fromEntries(SEMS.map(s=>[s,{foundation:[],core:[],support:[]}])); if(track!=='digital') FOUNDATION.forEach(id=>bySem[courseMap[id].s].foundation.push(courseMap[id])); if(track && track!=='all'){ TRACKS[track].core.forEach(id=>bySem[courseMap[id].s].core.push(courseMap[id])); TRACKS[track].support.forEach(id=>bySem[courseMap[id].s].support.push(courseMap[id])); } return bySem; }
''',
    'groupedForTrack',
    re.S
)

# Use a clearer group title in the tech-only filter.
replace(
    "} else { add('Core branch', data.core, COLORS[activeTrack], 'core'); add('Extended base', data.support, COLORS.neutral, 'support'); }",
    "} else { add(activeTrack==='digital'?'Computer · Tech':'Core branch', data.core, COLORS[activeTrack], 'core'); add('Extended base', data.support, COLORS.neutral, 'support'); }",
    'renderGrid digital label'
)

# ---- Camera: selected branch is closer; overview remains zoomed out ----
replace(
    "camera.position.z=activeTrack==='all'?215:126; camera.fov=activeTrack==='all'?58:44;",
    "camera.position.z=activeTrack==='all'?215:110; camera.fov=activeTrack==='all'?58:40;",
    'track camera'
)

# ---- Higher-resolution course-card texture without mipmaps (sharper, less memory growth) ----
sub(
    r"function labelTexture\(text, color, core=false, foundation=false\)\{.*?\n(?=function createNode)",
    '''function labelTexture(text, color, core=false, foundation=false){ const cv=document.createElement('canvas'); cv.width=1024; cv.height=288; const x=cv.getContext('2d'); const neutral=!core; const border=core?color:'#f5f7fa'; x.fillStyle=neutral?'rgba(222,227,236,.995)':'rgba(18,28,44,.995)'; x.strokeStyle=border; x.lineWidth=core?10:7; x.shadowColor=core?border:'rgba(255,255,255,.40)'; x.shadowBlur=core?34:10; x.beginPath(); x.roundRect(10,10,1004,268,26); x.fill(); x.stroke(); x.shadowBlur=0; x.fillStyle=neutral?'#0d1420':'#ffffff'; x.textAlign='center'; x.textBaseline='middle'; const font1=core?68:64; const font2=core?59:55; x.font=`900 ${font1}px sans-serif`; const max=830; let lines=[text]; if(x.measureText(text).width>max){ let split=Math.ceil(text.length/2); const near=text.lastIndexOf(' ',split); if(near>0) split=near; lines=[text.slice(0,split),text.slice(split).trim()]; } if(lines.length===1){ x.fillText(lines[0],512,139,max); } else { x.font=`900 ${font2}px sans-serif`; x.fillText(lines[0],512,116,max+50); x.fillText(lines[1],512,169,max+50); } const sub=foundation?'FOUNDATION':(core?'CORE BRANCH':'EXTENDED BASE'); x.fillStyle=neutral?'#555f70':'rgba(226,234,248,.98)'; x.font='900 23px sans-serif'; x.fillText(sub,512,238,820); const t=new THREE.CanvasTexture(cv); t.colorSpace=THREE.SRGBColorSpace; t.generateMipmaps=false; t.minFilter=THREE.LinearFilter; t.magFilter=THREE.LinearFilter; return t; }
''',
    'labelTexture',
    re.S
)

# Larger screen-space nodes.
sub(
    r"function createNode\(course, opts\)\{.*?\n(?=function buildScene)",
    '''function createNode(course, opts){ const group=new THREE.Group(); const shadow=new THREE.Sprite(new THREE.SpriteMaterial({map:glowTexture('#000000'),transparent:true,depthTest:false,depthWrite:false,opacity:.12})); shadow.scale.set(opts.foundation?14.2:(opts.core?16.4:15.4),opts.foundation?4.0:(opts.core?4.8:4.4),1); shadow.position.z=-0.3; group.add(shadow); const haloColor=opts.core?opts.color:COLORS.neutral; const halo=new THREE.Sprite(new THREE.SpriteMaterial({map:glowTexture(haloColor),transparent:true,depthTest:false,depthWrite:false,opacity:0})); halo.scale.set(opts.foundation?16:(opts.core?18:16.8),opts.foundation?4.7:(opts.core?5.5:5.0),1); group.add(halo); const sprite=new THREE.Sprite(new THREE.SpriteMaterial({map:labelTexture(course.n,opts.color,opts.core,opts.foundation),transparent:true,depthTest:false,depthWrite:false,opacity:1})); sprite.scale.set(opts.foundation?15.2:(opts.core?17.4:16.2),opts.foundation?4.3:(opts.core?5.0:4.55),1); sprite.renderOrder=10; group.add(sprite); group.userData.course=course; group.userData.track=opts.track||'common'; group.userData.role=opts.foundation?'foundation':opts.role; nodeRegistry.push({track:opts.track||'common',role:opts.foundation?'foundation':opts.role,course,group,sprite,halo,shadow,current:new THREE.Vector3(),target:new THREE.Vector3(),opacity:0,targetOpacity:1,scale:1,targetScale:1}); return group; }
''',
    'createNode',
    re.S
)

# More device pixels on iPhone; keep the previous low-power renderer.
replace(
    "renderer.setPixelRatio(Math.min(devicePixelRatio,innerWidth<=720?1.15:1.5));",
    "renderer.setPixelRatio(Math.min(devicePixelRatio,innerWidth<=720?1.75:1.65));",
    'pixel ratio'
)

# The fifth filter is hidden in overview, so no extra clutter there.
sub(
    r"function trackBase\(track\)\{.*?\n(?=function trackPosMap)",
    '''function trackBase(track){ if(activeTrack==='all') return {product:-30,ux:-10,space:10,mobility:30,digital:0}[track]; if(activeTrack===track) return 0; const others=TRACK_ORDER.filter(t=>t!==activeTrack); const idx=others.indexOf(track); return [-60,-30,30,60][idx]??0; }
''',
    'trackBase',
    re.S
)

# Give side subjects more room around the enlarged core cards.
sub(
    r"function trackPosMap\(track\)\{.*?\n(?=function updateTargets)",
    '''function trackPosMap(track){ const base=trackBase(track); const config=TRACKS[track]; const out={}; const buckets={}; config.core.forEach(id=>{ const s=courseMap[id].s; (buckets[s]||(buckets[s]={core:[],support:[]})).core.push(id); }); config.support.forEach(id=>{ const s=courseMap[id].s; (buckets[s]||(buckets[s]={core:[],support:[]})).support.push(id); }); SEMS.forEach(sem=>{ const bucket=buckets[sem]||{core:[],support:[]}; bucket.core.forEach((id,i)=>{ const gap=bucket.core.length>1?5.5:0; out[id]=new THREE.Vector3(base,semY(sem)+(i-(bucket.core.length-1)/2)*gap,semZ(sem)); }); const slots=[[-17.5,-2.7],[17.5,2.7],[-17.5,2.7],[17.5,-2.7],[-22,0],[22,0]]; bucket.support.forEach((id,i)=>{ const slot=slots[i]||[(i%2?-22:22),(Math.floor(i/2)+1)*2.6]; out[id]=new THREE.Vector3(base+slot[0],semY(sem)+slot[1],semZ(sem)+0.7); }); }); return out; }
''',
    'trackPosMap',
    re.S
)

# Foundation disappears in the tech-only filter. Digital nodes disappear in the normal overview.
sub(
    r"function updateTargets\(initial=false\)\{.*?\n(?=function updateLines)",
    '''function updateTargets(initial=false){ if(!selectedNode) setOverview(); const posByTrack={}; TRACK_ORDER.forEach(t=>posByTrack[t]=trackPosMap(t)); nodeRegistry.forEach(node=>{ if(node.role==='foundation'){ node.target.copy(foundationPos(node.course)); node.targetOpacity=activeTrack==='digital'?0:1; node.targetScale=1; } else { node.target.copy(posByTrack[node.track][node.course.id]); const isSelTrack=activeTrack===node.track; if(activeTrack==='all'){ node.targetOpacity=(node.track!=='digital' && node.role==='core')?1:0; node.targetScale=node.role==='core'?1:.92; } else if(isSelTrack){ node.targetOpacity=1; node.targetScale=node.role==='core'?1.08:1.0; } else { node.targetOpacity=0; node.targetScale=.84; } const selected=selectedNode && selectedNode.course.id===node.course.id && selectedNode.track===node.track && selectedNode.role===node.role; if(selected){ node.targetOpacity=1; node.targetScale=node.role==='core'?1.15:1.08; } } if(initial){ node.current.copy(node.target); node.opacity=node.targetOpacity; node.scale=node.targetScale; } }); }
''',
    'updateTargets',
    re.S
)

# Hide digital guide line in normal overview; show it only when the tech filter is selected.
sub(
    r"function updateLines\(time=0\)\{.*?\n(?=function animate)",
    '''function updateLines(time=0){ TRACK_ORDER.forEach(track=>{ const config=TRACKS[track]; const branch=nodeRegistry.filter(n=>n.track===track); const byId=Object.fromEntries(branch.map(n=>[n.course.id,n])); const coreNodes=config.core.map(id=>byId[id]).filter(Boolean).sort((a,b)=>SEMS.indexOf(a.course.s)-SEMS.indexOf(b.course.s)); if(!coreNodes.length) return; const start=new THREE.Vector3(trackBase(track),semY(track==='digital'?'1-1':'1-2')+(track==='digital'?2.2:-2.4),semZ(track==='digital'?'1-1':'1-2')+1.2); const pts=[start,...coreNodes.map(n=>n.current.clone())]; const curve=new THREE.CatmullRomCurve3(pts,false,'centripetal'); const curvePts=curve.getPoints(48); branchLines[track].mainLine.geometry.setFromPoints(curvePts); branchLines[track].glowLine.geometry.setFromPoints(curvePts); const coreBySem={}; coreNodes.forEach(n=>{ if(!coreBySem[n.course.s]) coreBySem[n.course.s]=n; }); const seg=[]; config.support.forEach(id=>{ const sNode=byId[id]; if(!sNode) return; let attach=coreBySem[sNode.course.s]; if(!attach){ const idx=SEMS.indexOf(sNode.course.s); for(let i=idx;i>=0&&!attach;i--) attach=coreBySem[SEMS[i]]; } attach=attach||coreNodes[0]; if(attach) seg.push(sNode.current.clone(),attach.current.clone()); }); branchLines[track].supportLine.geometry.setFromPoints(seg); const pulse=.55+Math.sin(time*.003)*.14; if(activeTrack==='all'){ const regular=track!=='digital'; branchLines[track].mainLine.material.opacity=regular?.88:0; branchLines[track].glowLine.material.opacity=regular?.22:0; branchLines[track].supportLine.material.opacity=0; } else if(activeTrack===track){ branchLines[track].mainLine.material.opacity=1; branchLines[track].glowLine.material.opacity=pulse; branchLines[track].supportLine.material.opacity=.62; } else { branchLines[track].mainLine.material.opacity=0; branchLines[track].glowLine.material.opacity=0; branchLines[track].supportLine.material.opacity=0; } }); }
''',
    'updateLines',
    re.S
)

# Project each semester's actual 3D row into screen coordinates for exact vertical alignment.
sub(
    r"function resize\(\)\{.*?\n(?=function clampOffset)",
    '''function resize(){ const c=renderer.domElement; const w=Math.max(1,c.clientWidth),h=Math.max(1,c.clientHeight); renderer.setSize(w,h,false); camera.aspect=w/h; camera.updateProjectionMatrix(); updateSemHudPositions(); }
function updateSemHudPositions(){ if(!camera||!renderer||!rootGroup||!THREE) return; const h=renderer.domElement.clientHeight||1; SEMS.forEach(sem=>{ const tag=semHud.querySelector(`[data-sem="${sem}"]`); if(!tag) return; const v=new THREE.Vector3(0,semY(sem),semZ(sem)); rootGroup.localToWorld(v); v.project(camera); let y=((1-v.y)*.5)*h; y=Math.max(48,Math.min(h-48,y)); tag.style.top=`${y}px`; }); }
''',
    'resize + semester projection',
    re.S
)
replace(
    '}); updateLines(t); renderer.render(scene,camera); requestAnimationFrame(animate); }',
    '}); updateLines(t); updateSemHudPositions(); renderer.render(scene,camera); requestAnimationFrame(animate); }',
    'animate sem alignment'
)

p.write_text(text, encoding='utf-8')
print('Patched index.html')
