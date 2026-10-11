from flask import Flask, render_template_string, jsonify, request

app = Flask(__name__)

PAGE = r"""
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Kibo Mission Trainer</title>
<style>
:root{--bg:#07111f;--panel:#101f32;--line:#27415c;--cyan:#56e5ff;--green:#7dffbd;--text:#e9f4ff;--muted:#9bb1c8;--red:#ff687d}
*{box-sizing:border-box}body{margin:0;background:radial-gradient(ellipse at top,#142c45,#07111f 65%);font-family:Inter,Segoe UI,Arial,sans-serif;color:var(--text)}
header{padding:20px 24px;border-bottom:1px solid var(--line);display:flex;align-items:center;justify-content:space-between;gap:15px;flex-wrap:wrap}
.brand{font-weight:900;letter-spacing:2px;font-size:20px}.brand span{color:var(--cyan)}.sub{color:var(--muted);font-size:12px;margin-top:4px}
.pill{border:1px solid #31536e;padding:8px 12px;border-radius:30px;color:var(--green);font-size:12px}
main{max-width:1400px;margin:auto;padding:18px;display:grid;grid-template-columns:minmax(0,1.8fr) minmax(280px,1fr);gap:16px}
.panel{background:linear-gradient(145deg,#112239,#0c1929);border:1px solid var(--line);border-radius:16px;overflow:hidden;box-shadow:0 15px 40px #0003}
.panel h2{font-size:13px;letter-spacing:1.5px;text-transform:uppercase;margin:0;padding:15px 17px;border-bottom:1px solid var(--line);color:#c6d9ec}
.canvas-wrap{padding:12px}canvas{width:100%;display:block;border-radius:10px;background:#081522;border:1px solid #203b55;touch-action:none}
.stats{display:grid;grid-template-columns:repeat(4,1fr);gap:8px;padding:0 12px 12px}
.stat{background:#0a1726;border:1px solid #1d354e;border-radius:10px;padding:10px}.stat label{display:block;color:var(--muted);font-size:10px;text-transform:uppercase;letter-spacing:1px}.stat strong{display:block;margin-top:6px;font-size:19px}
.controls{padding:14px;display:grid;grid-template-columns:1fr 1fr;gap:9px}
button{background:#17324b;color:var(--text);border:1px solid #315675;border-radius:9px;padding:11px 12px;font-weight:700;cursor:pointer;transition:.15s}
button:hover{background:#214968;border-color:var(--cyan)}button.primary{background:#087c99;border-color:#29cce9}button.danger{border-color:#78394a;color:#ff9eaa}
button:disabled{opacity:.4;cursor:not-allowed}
.readout{padding:0 14px 14px;color:var(--muted);font-size:12px;line-height:1.6}
.mission{padding:14px}.objective{display:flex;gap:10px;align-items:flex-start;padding:10px;border-bottom:1px solid #1d354e;font-size:13px}.objective:last-child{border:0}.dot{width:9px;height:9px;border-radius:50%;background:#536d84;margin-top:4px;flex-shrink:0}.dot.done{background:var(--green);box-shadow:0 0 10px #7dffbd77}
.log{height:155px;overflow:auto;background:#071321;margin:0 14px 14px;border:1px solid #1b334a;border-radius:9px;padding:10px;font:12px/1.6 ui-monospace,Consolas,monospace;color:#a9c3d9}.log div{border-bottom:1px solid #13283b;padding:3px 0}.log .good{color:var(--green)}.log .warn{color:#ffcc7a}
.slider-row{display:grid;grid-template-columns:1fr auto;gap:10px;align-items:center;padding:10px 14px;color:var(--muted);font-size:12px}.slider-row input{grid-column:1/-1;width:100%;accent-color:var(--cyan)}
footer{text-align:center;color:#718ba4;padding:12px 20px 24px;font-size:11px}
@media(max-width:900px){main{grid-template-columns:1fr}.stats{grid-template-columns:repeat(2,1fr)}}
</style>
</head>
<body>
<header><div><div class="brand">KIBO <span>MISSION TRAINER</span></div><div class="sub">IN-BROWSER PRACTICE SIMULATION · NOT THE OFFICIAL JAXA SIMULATOR</div></div><div class="pill">● TRAINING ENVIRONMENT ONLINE</div></header>
<main>
<section class="panel">
<h2>01 / Kibo module · local navigation arena</h2>
<div class="canvas-wrap"><canvas id="arena" width="900" height="570" aria-label="Top-down training arena"></canvas></div>
<div class="stats">
<div class="stat"><label>Mission score</label><strong id="score">0000</strong></div>
<div class="stat"><label>Checkpoints</label><strong id="cp">0 / 5</strong></div>
<div class="stat"><label>Collisions</label><strong id="collisions">0</strong></div>
<div class="stat"><label>Elapsed</label><strong id="elapsed">00:00</strong></div>
</div>
<div class="controls">
<button id="auto" class="primary">▶ Start autonomous run</button><button id="reset">↻ Reset mission</button>
<button id="up">↑ Forward</button><button id="down">↓ Backward</button>
<button id="left">← Strafe left</button><button id="right">→ Strafe right</button>
<button id="yawL">⟲ Rotate left</button><button id="yawR">⟳ Rotate right</button>
</div>
<div class="slider-row"><label for="speed">Translation step</label><strong id="speedVal">8</strong><input id="speed" type="range" min="2" max="18" value="8"></div>
<div class="readout">Keyboard: <b>W/S</b> forward/back · <b>A/D</b> strafe · <b>Q/E</b> rotate · <b>Space</b> pause/resume autonomous mode. The drone must visit all inspection checkpoints without touching module walls or equipment.</div>
</section>
<aside>
<section class="panel">
<h2>02 / Mission objectives</h2><div class="mission" id="objectives"></div>
</section>
<section class="panel" style="margin-top:16px">
<h2>03 / Flight telemetry</h2>
<div class="readout" id="telemetry">Position: X 0.0 · Y 0.0<br>Attitude: 0°<br>Mode: MANUAL<br>Status: READY</div>
<div class="slider-row"><label>Attitude adjustment</label><strong id="yawVal">0°</strong><input id="yaw" type="range" min="0" max="359" value="0"></div>
<div class="readout">Simplified educational model: movement, collision and scoring are illustrative. Coordinates and controls do not represent validated Int-Ball2 commands.</div>
</section>
<section class="panel" style="margin-top:16px">
<h2>04 / Event log</h2><div class="log" id="log" aria-live="polite"></div>
</section>
</aside>
</main>
<footer>Independent student practice project · Not affiliated with JAXA, JAXA Kibo-RPC, or PhilSA. Verify all competition requirements against the official rulebook.</footer>
<script>
(() => {
const canvas=document.getElementById('arena'), ctx=canvas.getContext('2d');
const W=canvas.width,H=canvas.height;
const checkpoints=[
 {x:155,y:115,name:'JOINT A',desc:'Inspect structural joint'},
 {x:450,y:105,name:'HATCH B',desc:'Inspect hatch perimeter'},
 {x:745,y:145,name:'RACK C',desc:'Inspect experiment rack'},
 {x:730,y:435,name:'JOINT D',desc:'Inspect lower structural joint'},
 {x:250,y:455,name:'HATCH E',desc:'Inspect return hatch'}
];
const obstacles=[
 {x:300,y:175,w:95,h:75,name:'EXPERIMENT RACK'},
 {x:505,y:255,w:115,h:80,name:'EQUIPMENT BAY'},
 {x:160,y:285,w:90,h:75,name:'STORAGE'},
 {x:390,y:405,w:90,h:55,name:'WORKSTATION'}
];
let drone,visited,collisions,score,started,startAt,elapsed,autoRun,autoIndex,last,events;
const $=id=>document.getElementById(id);
function reset(){
 drone={x:85,y:285,yaw:0};visited=new Set();collisions=0;score=0;started=false;startAt=0;elapsed=0;autoRun=false;autoIndex=0;last=0;events=[];
 $('auto').textContent='▶ Start autonomous run';$('auto').classList.add('primary');
 $('yaw').value=0;log('Mission initialized. Awaiting pilot command.');renderObjectives();draw();updateUI();
}
function log(msg,kind=''){events.unshift({msg,kind,time:new Date().toLocaleTimeString()});events=events.slice(0,35);$('log').innerHTML=events.map(e=>`<div class="${e.kind}">[${e.time}] ${e.msg}</div>`).join('')}
function renderObjectives(){
 $('objectives').innerHTML=checkpoints.map((c,i)=>`<div class="objective"><span class="dot ${visited.has(i)?'done':''}"></span><div><b>${String(i+1).padStart(2,'0')} · ${c.name}</b><div style="color:#91a9c0;margin-top:3px">${c.desc}</div><div style="color:${visited.has(i)?'#7dffbd':'#6e8aa3'};font-size:11px;margin-top:3px">${visited.has(i)?'INSPECTION COMPLETE':'AWAITING INSPECTION'}</div></div></div>`).join('');
}
function insideRect(x,y,r,pad=0){return x>r.x-pad&&x<r.x+r.w+pad&&y>r.y-pad&&y<r.y+r.h+pad}
function blocked(x,y){return x<45||x>W-45||y<45||y>H-45||obstacles.some(o=>insideRect(x,y,o,16))}
function move(dx,dy){
 if(!started){started=true;startAt=performance.now();log('Manual flight control enabled.')}
 const nx=drone.x+dx,ny=drone.y+dy;
 if(blocked(nx,ny)){collisions++;score=Math.max(0,score-15);log('Collision warning: movement blocked. Score penalty −15.','warn');}
 else {drone.x=nx;drone.y=ny;score=Math.max(0,score-1);checkCheckpoint();}
 updateUI();draw();
}
function rotate(d){drone.yaw=(drone.yaw+d+360)%360;$('yaw').value=Math.round(drone.yaw);updateUI();draw()}
function checkCheckpoint(){
 checkpoints.forEach((c,i)=>{if(!visited.has(i)&&Math.hypot(c.x-drone.x,c.y-drone.y)<34){visited.add(i);score+=250;log(`${c.name} inspected. +250 points.`,'good');renderObjectives();if(visited.size===checkpoints.length){autoRun=false;score+=500;log('ALL INSPECTIONS COMPLETE. Mission bonus +500.','good');$('auto').textContent='✓ Mission complete';}}});
}
function startAuto(){
 if(visited.size===checkpoints.length){log('Mission already complete. Reset to practice again.','warn');return}
 autoRun=!autoRun;started=true;if(!startAt)startAt=performance.now();
 $('auto').textContent=autoRun?'Ⅱ Pause autonomous run':'▶ Resume autonomous run';
 log(autoRun?'Autonomous waypoint routine started.':'Autonomous routine paused.',autoRun?'good':'');
}
function autoStep(dt){
 if(!autoRun)return;
 while(autoIndex<checkpoints.length&&visited.has(autoIndex))autoIndex++;
 if(autoIndex>=checkpoints.length){autoRun=false;return}
 const target=checkpoints[autoIndex],dx=target.x-drone.x,dy=target.y-drone.y;
 const desired=Math.atan2(dy,dx)*180/Math.PI;
 let diff=((desired-drone.yaw+540)%360)-180;
 drone.yaw=(drone.yaw+Math.sign(diff)*Math.min(Math.abs(diff),100*dt)+360)%360;
 const dist=Math.hypot(dx,dy),step=Math.min(dist,Number($('speed').value)*dt*9);
 const nx=drone.x+(dx/(dist||1))*step,ny=drone.y+(dy/(dist||1))*step;
 if(!blocked(nx,ny)){drone.x=nx;drone.y=ny;}else{collisions++;score=Math.max(0,score-5)}
 if(dist<24){drone.x=target.x;drone.y=target.y;checkCheckpoint();autoIndex++}
}
function draw(){
 ctx.clearRect(0,0,W,H);
 ctx.fillStyle='#091827';ctx.fillRect(0,0,W,H);
 ctx.strokeStyle='#18314a';ctx.lineWidth=1;
 for(let x=45;x<W-45;x+=30){ctx.beginPath();ctx.moveTo(x,45);ctx.lineTo(x,H-45);ctx.stroke()}
 for(let y=45;y<H-45;y+=30){ctx.beginPath();ctx.moveTo(45,y);ctx.lineTo(W-45,y);ctx.stroke()}
 ctx.strokeStyle='#56e5ff';ctx.lineWidth=3;ctx.strokeRect(45,45,W-90,H-90);
 ctx.fillStyle='#183148';ctx.font='bold 12px Arial';ctx.fillText('KIBO MODULE · SIMULATED INTERIOR',60,28);
 obstacles.forEach(o=>{ctx.fillStyle='#243c50';ctx.fillRect(o.x,o.y,o.w,o.h);ctx.strokeStyle='#5b7891';ctx.lineWidth=2;ctx.strokeRect(o.x,o.y,o.w,o.h);ctx.fillStyle='#9bb1c8';ctx.font='10px Arial';ctx.textAlign='center';ctx.fillText(o.name,o.x+o.w/2,o.y+o.h/2+4);ctx.textAlign='left'});
 checkpoints.forEach((c,i)=>{ctx.beginPath();ctx.arc(c.x,c.y,visited.has(i)?18:15,0,Math.PI*2);ctx.fillStyle=visited.has(i)?'#174c3d':'#153b50';ctx.fill();ctx.strokeStyle=visited.has(i)?'#7dffbd':'#56e5ff';ctx.lineWidth=2;ctx.stroke();ctx.fillStyle=visited.has(i)?'#7dffbd':'#d9f8ff';ctx.font='bold 11px Arial';ctx.textAlign='center';ctx.fillText(visited.has(i)?'✓':String(i+1),c.x,c.y+4);ctx.textAlign='left';ctx.fillStyle='#a8c3d9';ctx.font='10px Arial';ctx.fillText(c.name,c.x-25,c.y+31)});
 // direction vector and drone body
 const a=drone.yaw*Math.PI/180;
 ctx.beginPath();ctx.moveTo(drone.x,drone.y);ctx.lineTo(drone.x+34*Math.cos(a),drone.y+34*Math.sin(a));ctx.strokeStyle='#7dffbd';ctx.lineWidth=4;ctx.stroke();
 ctx.beginPath();ctx.arc(drone.x,drone.y,13,0,Math.PI*2);ctx.fillStyle='#e8fbff';ctx.fill();ctx.strokeStyle='#56e5ff';ctx.lineWidth=3;ctx.stroke();
 ctx.fillStyle='#07111f';ctx.beginPath();ctx.arc(drone.x,drone.y,4,0,Math.PI*2);ctx.fill();
 ctx.textAlign='left';
}
function updateUI(){
 $('score').textContent=String(score).padStart(4,'0');$('cp').textContent=`${visited.size} / ${checkpoints.length}`;$('collisions').textContent=collisions;
 $('elapsed').textContent=String(Math.floor(elapsed/60)).padStart(2,'0')+':'+String(Math.floor(elapsed%60)).padStart(2,'0');
 $('yawVal').textContent=Math.round(drone.yaw)+'°';
 $('telemetry').innerHTML=`Position: X ${(drone.x/10).toFixed(1)} · Y ${(drone.y/10).toFixed(1)}<br>Attitude: ${Math.round(drone.yaw)}°<br>Mode: ${autoRun?'AUTONOMOUS':'MANUAL'}<br>Status: ${visited.size===5?'MISSION COMPLETE':collisions?'COLLISION CAUTION':'NOMINAL'}`;
 $('speedVal').textContent=$('speed').value;
}
function frame(t){if(last){const dt=Math.min((t-last)/1000,.05);if(started&&!autoRun)elapsed=(t-startAt)/1000;else if(started&&autoRun)elapsed=(t-startAt)/1000;autoStep(dt);updateUI();draw()}last=t;requestAnimationFrame(frame)}
function manual(dx,dy){if(autoRun){autoRun=false;$('auto').textContent='▶ Resume autonomous run';log('Manual override: autonomous routine paused.','warn')}move(dx,dy)}
const step=()=>Number($('speed').value);
$('up').onclick=()=>manual(0,-step());$('down').onclick=()=>manual(0,step());$('left').onclick=()=>manual(-step(),0);$('right').onclick=()=>manual(step(),0);
$('yawL').onclick=()=>rotate(-10);$('yawR').onclick=()=>rotate(10);$('auto').onclick=startAuto;$('reset').onclick=reset;
$('yaw').oninput=e=>{drone.yaw=Number(e.target.value);updateUI();draw()};
$('speed').oninput=()=>updateUI();
document.addEventListener('keydown',e=>{if(['INPUT'].includes(document.activeElement.tagName))return;const k=e.key.toLowerCase();if(k==='w')manual(0,-step());if(k==='s')manual(0,step());if(k==='a')manual(-step(),0);if(k==='d')manual(step(),0);if(k==='q')rotate(-10);if(k==='e')rotate(10);if(e.code==='Space'){e.preventDefault();startAuto()}});
reset();requestAnimationFrame(frame);
})();
</script>
</body>
</html>
"""

@app.get("/")
def home():
    return render_template_string(PAGE)

@app.get("/health")
def health():
    return jsonify(status="ok", app="Kibo Mission Trainer", mode="training-only")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
