import os
from datetime import datetime
from flask import Flask, session, request, redirect, url_for, jsonify, render_template_string

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "replace-this-secret-before-production")

COMMANDS = {
    "calibrate": ("Calibrate sensors", "Align navigation and camera sensors"),
    "navigate": ("Move to payload", "Move through the ISS laboratory to the science rack"),
    "deploy": ("Deploy robotic arm", "Extend the arm at low speed"),
    "inspect": ("Inspect payload", "Capture imagery and telemetry"),
    "experiment": ("Run science experiment", "Collect microgravity data"),
    "stow": ("Retract and stow", "Return the arm to a safe position"),
}
OBJECTIVES = [
    ("calibrate", "Calibrate robot sensors", "Establish reliable navigation readings."),
    ("navigate", "Reach the internal science rack", "Move only after calibration."),
    ("deploy", "Deploy the robotic arm", "Reach the internal rack before deploying the arm."),
    ("inspect", "Inspect payload", "Capture imagery and telemetry."),
    ("experiment", "Complete science experiment", "Collect microgravity experiment data."),
    ("stow", "Return to safe configuration", "Retract and stow the robotic arm."),
]
SAFE_PLAN = [x[0] for x in OBJECTIVES]

def fresh():
    return {
        "score": 0, "runs": 0, "status": "READY", "battery": 100,
        "navigation": 55, "science": 0, "program": [],
        "completed": {x[0]: False for x in OBJECTIVES},
        "log": [{"time": "00:00:00", "text": "Mission control initialized. Awaiting commands.", "kind": "ok"}],
        "bonus": False
    }

def state():
    if "game" not in session:
        session["game"] = fresh()
    s = session["game"]
    base = fresh()
    for k, v in base.items():
        s.setdefault(k, v)
    for key, _, _ in OBJECTIVES:
        s.setdefault("completed", {}).setdefault(key, False)
    return s

def event(s, message, kind="ok"):
    s["log"].append({"time": datetime.now().strftime("%H:%M:%S"), "text": message, "kind": kind})
    s["log"] = s["log"][-35:]

def save(s):
    session["game"] = s
    session.modified = True

def progress(s):
    return round(sum(bool(s["completed"].get(k)) for k, _, _ in OBJECTIVES) / len(OBJECTIVES) * 100)

PAGE = r"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>KIBO | Orbital Mission Trainer</title>
<style>
:root{--bg:#07111f;--panel:#11243a;--panel2:#0a192a;--line:#29465e;--text:#eef7ff;--muted:#a5b9cc;--teal:#53e0cf;--blue:#73aaff;--gold:#ffcf70;--red:#ff7888;--green:#80f0ad}
*{box-sizing:border-box}body{margin:0;background:radial-gradient(ellipse at 50% -10%,#183b5b,var(--bg) 58%);color:var(--text);font:15px/1.5 system-ui,-apple-system,Segoe UI,sans-serif;min-height:100vh}
button{cursor:pointer;border:1px solid #3d647f;border-radius:10px;background:#1b3851;color:var(--text);padding:10px 13px;font-weight:750;transition:.18s}button:hover{border-color:var(--teal);background:#234861;transform:translateY(-1px)}button.primary{background:var(--teal);color:#06201f;border-color:var(--teal)}button.danger{background:#3a202e;color:#ffc0c8;border-color:#8d4353}
.top{display:flex;justify-content:space-between;align-items:center;gap:18px;padding:17px clamp(15px,4vw,52px);border-bottom:1px solid var(--line);background:#07111fdd;position:sticky;top:0;z-index:2;backdrop-filter:blur(12px)}
.brand{display:flex;align-items:center;gap:12px;font-weight:950;letter-spacing:.15em}.logo{width:40px;height:40px;border-radius:12px;display:grid;place-items:center;background:linear-gradient(135deg,var(--teal),var(--blue));color:#07111f;font-size:23px}.brand small{display:block;color:var(--muted);font-size:10px;letter-spacing:.18em}
.pills{display:flex;gap:8px;flex-wrap:wrap;justify-content:flex-end}.pill,.tag{font-size:10px;letter-spacing:.12em;border:1px solid var(--line);border-radius:999px;padding:6px 9px;color:var(--muted)}.pill.live{color:var(--green);border-color:#34765c}
main{max-width:1450px;margin:auto;padding:28px clamp(14px,3vw,42px) 50px}.eyebrow{font-size:11px;letter-spacing:.22em;color:var(--teal);font-weight:900}.hero{display:flex;justify-content:space-between;align-items:flex-end;gap:20px;margin:10px 0 24px}.hero h1{font-size:clamp(30px,4vw,48px);line-height:1.05;margin:8px 0;letter-spacing:-.04em}.hero p{max-width:650px;color:var(--muted);margin:0}.actions{display:flex;gap:9px;flex-wrap:wrap}
.notice{border:1px solid #356c68;background:#0d292d;padding:12px 14px;border-radius:10px;color:#c5fff1;font-size:12px;margin-bottom:15px}
.grid{display:grid;grid-template-columns:1.1fr 1fr .9fr;gap:15px;align-items:start}.panel{background:linear-gradient(160deg,#142940,#0c1a2b);border:1px solid var(--line);border-radius:16px;padding:18px;box-shadow:0 18px 50px #0002;min-width:0}.panel h2{font-size:15px;margin:0 0 4px}.sub{font-size:11px;color:var(--muted);margin:0 0 15px}.head{display:flex;justify-content:space-between;align-items:center;gap:10px;margin-bottom:14px}.tag{color:var(--teal);border-color:#2d6e72;border-radius:6px}
.scene{height:245px;position:relative;overflow:hidden;border-radius:12px;background:linear-gradient(180deg,#243b50 0%,#172c40 48%,#0b1928 100%);border:1px solid #3b6078;margin-bottom:14px;isolation:isolate}.cabin-ceiling{position:absolute;left:0;right:0;top:0;height:25px;background:repeating-linear-gradient(90deg,#8aa0ae 0 28px,#526a7a 29px 33px);border-bottom:3px solid #0a1725}.cabin-floor{position:absolute;left:0;right:0;bottom:0;height:29px;background:repeating-linear-gradient(90deg,#627887 0 31px,#354e60 32px 37px);border-top:3px solid #9aabb5}.cabin-wall{position:absolute;inset:24px 0 27px;background:repeating-linear-gradient(90deg,#344e62 0 63px,#1c3449 64px 69px,#466174 70px 74px);border-top:2px solid #8aa2b1;border-bottom:2px solid #536f81}.iss-window{position:absolute;right:16px;top:44px;width:104px;height:74px;border:7px solid #8298a6;border-radius:9px;background:radial-gradient(circle at 32% 35%,#79d5f0,#246da8 55%,#0b2445);box-shadow:0 0 0 2px #0a1725,0 0 20px #4cbde633}.iss-window:after{content:"";position:absolute;inset:7px;background:linear-gradient(135deg,transparent 25%,#77dbb866 26% 36%,transparent 37% 58%,#c1e7a755 59% 67%,transparent 68%);border-radius:50%}.rack{position:absolute;left:13px;top:45px;width:95px;height:119px;background:#15283a;border:3px solid #7b929f;border-radius:7px;box-shadow:inset 0 0 0 4px #253e51}.rack:before{content:"SCIENCE RACK";position:absolute;top:6px;left:5px;right:5px;text-align:center;color:#a6c6d7;font-size:7px;letter-spacing:1px}.rack:after{content:"";position:absolute;left:8px;right:8px;top:27px;height:75px;background:repeating-linear-gradient(180deg,#4a7188 0 11px,#132536 12px 17px);border:1px solid #6e93a7}.rack-light{position:absolute;left:25px;bottom:20px;width:8px;height:8px;border-radius:50%;background:#53e0cf;box-shadow:14px 0 #ffcf70,28px 0 #80f0ad;z-index:1}.handrail{position:absolute;right:7px;top:128px;width:130px;height:9px;border:3px solid #b4c4cc;border-radius:8px;transform:rotate(-10deg);box-shadow:0 0 0 2px #15283a}.robot{position:absolute;left:43%;top:78px;width:70px;height:82px;z-index:1;filter:drop-shadow(0 5px 7px #06101b99)}.robot-head{position:absolute;left:17px;top:0;width:38px;height:30px;border-radius:9px;background:linear-gradient(135deg,#e7f1f4,#7c9baa);border:3px solid #324f62}.robot-eye{position:absolute;left:7px;top:8px;width:19px;height:7px;border-radius:4px;background:#10283b;box-shadow:0 0 7px #53e0cf}.robot-body{position:absolute;left:10px;top:31px;width:53px;height:37px;border-radius:8px;background:linear-gradient(135deg,#d6e4e9,#66899a);border:3px solid #324f62}.robot-body:after{content:"K-01";position:absolute;left:9px;top:8px;font-size:8px;font-weight:900;color:#173448}.robot-arm{position:absolute;left:0;top:38px;width:18px;height:7px;background:#9bb2bf;border:2px solid #324f62;border-radius:6px;transform:rotate(25deg)}.robot-arm:after{content:"";position:absolute;right:-8px;top:-3px;width:10px;height:10px;border:2px solid #53e0cf;border-radius:50%;background:#1d4355}.robot-leg{position:absolute;left:21px;top:64px;width:8px;height:17px;background:#91aab8;border:2px solid #324f62;border-radius:5px;transform:rotate(10deg)}.robot-leg:after{content:"";position:absolute;top:10px;left:-6px;width:16px;height:5px;border-radius:5px;background:#d1e0e6}.robot-label{position:absolute;left:calc(43% - 3px);top:164px;color:#c8f9f1;font-size:8px;font-weight:900;letter-spacing:1px;text-shadow:0 1px 5px #07111f}.screen{position:absolute;right:19px;bottom:42px;width:76px;height:45px;border:4px solid #8298a6;border-radius:5px;background:#071522;box-shadow:inset 0 0 0 2px #253e51}.screen:after{content:"SYS ONLINE\A ARM: STOWED\A O2: NOMINAL";white-space:pre;position:absolute;left:5px;top:4px;font:6px/1.5 monospace;color:#53e0cf}.cabin-label{position:absolute;left:12px;bottom:7px;font-size:9px;letter-spacing:.13em;color:#d2e8f4;z-index:2}.scene-badge{position:absolute;right:12px;top:9px;font-size:8px;letter-spacing:.14em;color:#9dfff2;background:#102c3a;border:1px solid #38747b;border-radius:5px;padding:4px 6px;z-index:2}

.map-wrap{position:relative;width:100%;height:390px;overflow:hidden;border:1px solid #3b6078;border-radius:12px;background:#061321;margin-bottom:12px}
#issMap{display:block;width:100%;height:100%;outline:none;touch-action:none}
.map-hud{position:absolute;left:10px;top:10px;display:flex;gap:6px;flex-wrap:wrap;pointer-events:none}.map-hud span{font-size:9px;letter-spacing:.1em;padding:5px 7px;border:1px solid #3b7182;border-radius:6px;background:#071827dd;color:#bdfaf0}
.map-controls{display:flex;gap:7px;flex-wrap:wrap;align-items:center;margin:0 0 14px}.map-controls button{font-size:11px;padding:7px 10px}.map-help{font-size:10px;color:var(--muted);margin-left:auto}.fail-overlay{position:absolute;inset:0;display:none;place-items:center;background:#070b13df;z-index:5;text-align:center;padding:20px}.fail-overlay.show{display:grid}.fail-card{max-width:330px;padding:24px;border:1px solid #ff7888;border-radius:14px;background:#251824;box-shadow:0 0 45px #ff334422}.fail-card h3{color:#ff7888;margin:0 0 8px;font-size:24px}.fail-card p{color:#f3d9df;font-size:12px}
@media(max-width:700px){.map-wrap{height:330px}.map-help{width:100%;margin:0}}
.metrics{display:grid;grid-template-columns:repeat(3,1fr);gap:8px}.metric{background:var(--panel2);border:1px solid #20394e;padding:11px;border-radius:10px}.metric span{display:block;color:var(--muted);font-size:10px;text-transform:uppercase;letter-spacing:.1em}.metric strong{display:block;font-size:22px;margin-top:3px}.metric small{font-size:10px;color:var(--teal)}
.bar{height:7px;background:#07111f;border-radius:9px;overflow:hidden;margin:8px 0 14px}.bar i{display:block;height:100%;background:linear-gradient(90deg,var(--teal),var(--blue));border-radius:9px;transition:width .3s}.reshead{display:flex;justify-content:space-between;font-size:12px}.reshead span:last-child{color:var(--muted)}
.commandlist,.objectives,.sequence{display:flex;flex-direction:column;gap:8px}.command,.step,.objective{display:flex;align-items:center;gap:10px;background:#0a1929;border:1px solid #263e53;border-radius:10px;padding:10px}.cmdicon{width:30px;height:30px;flex-shrink:0;border-radius:8px;background:#1c4055;display:grid;place-items:center;color:var(--teal);font-weight:900}.command strong,.objective strong{font-size:12px;display:block}.command small,.objective small{font-size:11px;color:var(--muted);display:block}.command button{margin-left:auto;padding:6px 9px;font-size:11px;white-space:nowrap}.step .num{font-size:11px;color:var(--teal);width:20px}.stepname{flex:1;font-size:12px;font-weight:750}.remove{padding:4px 8px;background:#321d2b;color:#ffb6c0;border-color:#633b4c}.empty{border:1px dashed #35536a;border-radius:10px;padding:18px;text-align:center;color:var(--muted);font-size:12px}.check{width:22px;height:22px;flex-shrink:0;border:1px solid #4b6a7c;border-radius:7px;display:grid;place-items:center;color:var(--green)}.objective.done .check{background:#173e34;border-color:#398765}.objective{align-items:flex-start}.objective div:last-child{padding-top:1px}.log{height:150px;overflow:auto;background:#071321;border:1px solid #213b51;border-radius:10px;padding:10px;font:11px/1.7 ui-monospace,monospace;color:#b8d4e5}.log p{margin:0;border-bottom:1px solid #172b3d;padding:3px 0}.ok{color:var(--green)}.warn{color:var(--gold)}.bad{color:var(--red)}.foot{text-align:center;color:#7893a9;font-size:11px;margin-top:18px}
@media(max-width:1100px){.grid{grid-template-columns:1fr 1fr}.side{grid-column:1/-1}.hero{align-items:flex-start;flex-direction:column}}@media(max-width:700px){.grid{grid-template-columns:1fr}.side{grid-column:auto}.top{align-items:flex-start;flex-direction:column}.pills{justify-content:flex-start}.metrics{gap:6px}.metric strong{font-size:19px}}
</style></head><body>
<header class="top"><div class="brand"><div class="logo">⌁</div><div>KIBO <small>ORBITAL MISSION TRAINER</small></div></div><div class="pills"><span class="pill live">● SYSTEM ONLINE</span><span class="pill">ISS · LOW EARTH ORBIT</span><span class="pill">MISSION K-01</span></div></header>
<main><section class="hero"><div><div class="eyebrow">JAXA · INTERNATIONAL SPACE STATION</div><h1>Mission Control<span style="color:var(--teal)">.</span></h1><p>Take direct control of Kibo, a small spherical free-flying robot, and explore the ISS interior. One collision with a solid obstacle ends the run.</p></div><div class="actions"><form method="post" action="/reset"><button class="danger">↺ Reset mission</button></form><button class="primary" onclick="runProgram()">▶ Execute sequence</button></div></section>
<div class="notice">MISSION DIRECTIVE: Explore a larger top-down map of the ISS. Move spherical Kibo through corridors, avoid equipment and blocked areas, and reach the science rack without colliding.</div>
<section class="grid">
<div class="panel"><div class="head"><div><h2>ISS exploration map</h2><p class="sub" style="margin:3px 0 0">LARGE INTERIOR · FREE MOVEMENT</p></div><span class="tag">INSIDE ISS</span></div>
<div class="map-wrap" id="mapWrap"><canvas id="issMap" tabindex="0" aria-label="Move Kibo around the ISS map using arrow keys or WASD"></canvas><div class="map-hud"><span>ISS DECK MAP · FREE ROAM</span><span id="mapStatus">KIBO ONLINE</span></div><div class="fail-overlay" id="failOverlay"><div class="fail-card"><h3>⚠ MISSION FAILED</h3><p id="failReason">Kibo collided with an ISS obstacle.</p><p>Collision detected. The robot has stopped to protect the station.</p><button class="primary" onclick="restartRover()">↻ Restart exploration</button></div></div></div>
<div class="map-controls"><button onclick="restartRover()">↻ Reset position</button><button onclick="toggleMapHelp()">⌨ Controls</button><span class="map-help" id="mapHelp">Move with WASD / arrow keys · Avoid equipment and blocked corridors</span></div>
<div class="metrics"><div class="metric"><span>Mission score</span><strong id="score">{{s.score}}</strong><small>PTS</small></div><div class="metric"><span>Commands run</span><strong id="runs">{{s.runs}}</strong><small>EXECUTIONS</small></div><div class="metric"><span>Status</span><strong id="status" style="font-size:14px">{{s.status}}</strong><small>TRACKING</small></div></div>
<div style="margin-top:18px" class="head"><h2>Mission progress</h2><strong id="progressText" style="color:var(--teal);font-size:12px">{{progress}}%</strong></div><div class="bar"><i id="progressBar" style="width:{{progress}}%"></i></div>
<div class="reshead"><span>🔋 Robot battery</span><span id="batteryText">{{s.battery}}%</span></div><div class="bar"><i id="batteryBar" style="width:{{s.battery}}%;background:linear-gradient(90deg,#80f0ad,#53e0cf)"></i></div>
<div class="reshead"><span>🧭 Navigation confidence</span><span id="navText">{{s.navigation}}%</span></div><div class="bar"><i id="navBar" style="width:{{s.navigation}}%;background:linear-gradient(90deg,#73aaff,#53e0cf)"></i></div>
<div class="reshead"><span>🧪 Experiment readiness</span><span id="scienceText">{{s.science}}%</span></div><div class="bar"><i id="scienceBar" style="width:{{s.science}}%;background:linear-gradient(90deg,#ffcf70,#ff9d70)"></i></div>
</div>
<div class="panel"><div class="head"><div><h2>Robot programming</h2><p class="sub" style="margin:3px 0 0">Build a safe command sequence</p></div><span class="tag">KIBO ARM</span></div>
<div class="commandlist">{% for key, pair in commands.items() %}<div class="command"><div class="cmdicon">{{['⌖','↗','⚙','◎','✦','↙'][loop.index0]}}</div><div><strong>{{pair[0]}}</strong><small>{{pair[1]}}</small></div><button onclick="addCommand('{{key}}')">＋ Add</button></div>{% endfor %}</div>
<div class="head" style="margin:19px 0 10px"><h2>Program sequence</h2><button onclick="clearProgram()" style="padding:6px 9px;font-size:11px">Clear all</button></div><div id="sequence" class="sequence"></div>
<div style="display:flex;gap:8px;margin-top:13px;flex-wrap:wrap"><button class="primary" style="flex:1" onclick="runProgram()">▶ Execute sequence</button><button onclick="addRecommended()">✦ Load safe plan</button></div></div>
<div class="panel side"><div class="head"><div><h2>Mission objectives</h2><p class="sub" style="margin:3px 0 0">Complete all critical operations</p></div><span class="tag">OPS</span></div><div class="objectives" id="objectives">{% for key,title,desc in objectives %}<div class="objective {% if s.completed[key] %}done{% endif %}" id="obj-{{key}}"><div class="check">{% if s.completed[key] %}✓{% else %}{{loop.index}}{% endif %}</div><div><strong>{{title}}</strong><small>{{desc}}</small></div></div>{% endfor %}</div>
<div class="head" style="margin:19px 0 10px"><h2>Mission telemetry</h2><span class="tag">EVENT LOG</span></div><div class="log" id="log">{% for item in s.log %}<p class="{{item.kind}}">[{{item.time}}] {{item.text}}</p>{% endfor %}</div>
<div style="display:flex;gap:8px;margin-top:11px;flex-wrap:wrap"><button onclick="diagnostic()" style="flex:1">⌁ Run diagnostics</button><button onclick="exportSave()">⇩ Export save</button></div><p class="sub" style="margin:12px 0 0">Educational simulation only. Not connected to real spacecraft or live NASA/JAXA systems.</p></div>
</section><div class="foot">KIBO ORBITAL MISSION TRAINER · EDUCATIONAL SIMULATION · BUILD 1.0</div></main>
<script>
let program={{s.program|tojson}}, labels={{command_labels|tojson}};
function draw(){let e=document.getElementById('sequence');if(!program.length){e.innerHTML='<div class="empty">No commands yet. Add commands above or load the safe plan.</div>';return}e.innerHTML=program.map((c,i)=>`<div class="step"><span class="num">${String(i+1).padStart(2,'0')}</span><span class="stepname">${labels[c]}</span><button class="remove" onclick="removeCommand(${i})">×</button></div>`).join('')}
async function act(action,extra={}){try{let r=await fetch('/action',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({action,program,...extra})});let d=await r.json();if(d.program){program=d.program;draw()}if(d.state)update(d.state);(d.messages||[]).forEach(m=>log(m.text,m.kind));if(d.objectives)d.objectives.forEach(o=>{let el=document.getElementById('obj-'+o.key);if(el){el.classList.toggle('done',o.done);el.querySelector('.check').textContent=o.done?'✓':o.number}})}catch(e){log('Connection error. Refresh and try again.','bad')}}
function addCommand(c){act('add',{command:c})}function removeCommand(i){act('remove',{index:i})}function clearProgram(){act('clear')}function addRecommended(){act('recommended')}function runProgram(){act('execute')}function diagnostic(){act('diagnostic')}
function update(s){for(let [id,v] of Object.entries({score:s.score,runs:s.runs,status:s.status,progressText:s.progress+'%',batteryText:s.battery+'%',navText:s.navigation+'%',scienceText:s.science+'%'})){let e=document.getElementById(id);if(e)e.textContent=v}for(let [id,v] of Object.entries({progressBar:s.progress,batteryBar:s.battery,navBar:s.navigation,scienceBar:s.science})){document.getElementById(id).style.width=v+'%'}}
function log(t,k='ok'){let e=document.getElementById('log'),p=document.createElement('p');p.className=k;p.textContent='['+new Date().toLocaleTimeString()+'] '+t;e.appendChild(p);e.scrollTop=e.scrollHeight}
async function exportSave(){let r=await fetch('/save'),d=await r.json(),b=new Blob([JSON.stringify(d,null,2)],{type:'application/json'}),a=document.createElement('a');a.href=URL.createObjectURL(b);a.download='kibo-mission-save.json';a.click();URL.revokeObjectURL(a.href)}

// Free-roam ISS map: Kibo is a spherical robot, not a humanoid.
const mapCanvas=document.getElementById('issMap'), mapCtx=mapCanvas.getContext('2d');
const WORLD={w:1800,h:1120}; let rover={x:250,y:530,r:17,speed:235}; let keys={},lastFrame=0,failed=false,explored=0;
const rooms=[
 {x:90,y:120,w:460,h:310,name:'JEM · JAPANESE EXPERIMENT MODULE',color:'#173d50'},
 {x:590,y:120,w:490,h:330,name:'KIBO LABORATORY',color:'#20394d'},
 {x:1120,y:120,w:560,h:330,name:'NODE 1 · HARMONY',color:'#293c4b'},
 {x:90,y:500,w:430,h:470,name:'AIRLOCK & STORAGE',color:'#203447'},
 {x:560,y:510,w:520,h:450,name:'SCIENCE LAB',color:'#173d50'},
 {x:1120,y:510,w:560,h:450,name:'CREW QUARTERS',color:'#283849'},
];
const obstacles=[
 {x:155,y:180,w:100,h:72,n:'Storage rack'}, {x:355,y:175,w:115,h:90,n:'Equipment rack'},
 {x:660,y:170,w:100,h:100,n:'Science cabinet'}, {x:840,y:185,w:145,h:68,n:'Experiment bench'},
 {x:1230,y:170,w:150,h:100,n:'Supply lockers'}, {x:1480,y:290,w:105,h:90,n:'Life support unit'},
 {x:140,y:590,w:125,h:130,n:'Airlock machinery'}, {x:340,y:780,w:125,h:105,n:'Cargo crate'},
 {x:630,y:590,w:150,h:95,n:'Lab bench'}, {x:840,y:720,w:155,h:115,n:'Experiment rack'},
 {x:1210,y:570,w:130,h:120,n:'Crew locker'}, {x:1460,y:760,w:150,h:100,n:'Water recycler'},
 {x:530,y:445,w:55,h:130,n:'bulkhead'}, {x:1080,y:445,w:45,h:130,n:'bulkhead'},
 {x:1040,y:610,w:55,h:130,n:'bulkhead'}, {x:540,y:820,w:55,h:120,n:'bulkhead'}
];
const scienceTarget={x:850,y:575,r:29};
function resizeMap(){let dpr=Math.min(window.devicePixelRatio||1,2),r=mapCanvas.getBoundingClientRect();mapCanvas.width=Math.round(r.width*dpr);mapCanvas.height=Math.round(r.height*dpr);mapCtx.setTransform(dpr,0,0,dpr,0,0)}
function circleRect(cx,cy,rad,o){let nx=Math.max(o.x,Math.min(cx,o.x+o.w)),ny=Math.max(o.y,Math.min(cy,o.y+o.h));return (cx-nx)**2+(cy-ny)**2<rad*rad}
function restartRover(){rover={x:250,y:530,r:17,speed:235};keys={};failed=false;explored=0;document.getElementById('failOverlay').classList.remove('show');document.getElementById('mapStatus').textContent='KIBO ONLINE';mapCanvas.focus()}
function toggleMapHelp(){let h=document.getElementById('mapHelp');h.textContent=h.textContent.startsWith('Move')?'W / ↑: up · S / ↓: down · A / ←: left · D / →: right · Touch and drag on the map also moves Kibo':'Move with WASD / arrow keys · Avoid equipment and blocked corridors'}
function drawMap(){const ctx=mapCtx,w=mapCanvas.clientWidth,h=mapCanvas.clientHeight;if(!w||!h)return;ctx.clearRect(0,0,w,h);let scale=Math.min(w/900,h/560); // camera view sized to show a large navigable area
scale=Math.min(w/WORLD.w*2.0,h/WORLD.h*2.0);scale=Math.max(.42,Math.min(.78,scale));let vw=w/scale,vh=h/scale,cx=Math.max(vw/2,Math.min(WORLD.w-vw/2,rover.x)),cy=Math.max(vh/2,Math.min(WORLD.h-vh/2,rover.y));let ox=w/2-cx*scale,oy=h/2-cy*scale;
ctx.save();ctx.translate(ox,oy);ctx.scale(scale,scale);ctx.fillStyle='#091827';ctx.fillRect(0,0,WORLD.w,WORLD.h);
// floor grid
ctx.strokeStyle='#29485b';ctx.lineWidth=1;for(let x=0;x<=WORLD.w;x+=40){ctx.beginPath();ctx.moveTo(x,0);ctx.lineTo(x,WORLD.h);ctx.stroke()}for(let y=0;y<=WORLD.h;y+=40){ctx.beginPath();ctx.moveTo(0,y);ctx.lineTo(WORLD.w,y);ctx.stroke()}
// module rooms and corridor layout
for(const rm of rooms){ctx.fillStyle=rm.color;ctx.fillRect(rm.x,rm.y,rm.w,rm.h);ctx.strokeStyle='#8aa6b6';ctx.lineWidth=9;ctx.strokeRect(rm.x,rm.y,rm.w,rm.h);ctx.strokeStyle='#4b6c7d';ctx.lineWidth=2;ctx.strokeRect(rm.x+13,rm.y+13,rm.w-26,rm.h-26);ctx.fillStyle='#d2e9f5';ctx.font='bold 16px system-ui';ctx.fillText(rm.name,rm.x+20,rm.y+32)}
// connect modules with clear corridors
ctx.fillStyle='#30495b';ctx.fillRect(500,420,650,100);ctx.fillRect(480,600,130,170);ctx.fillRect(1030,600,130,160);ctx.fillStyle='#6b8492';ctx.fillRect(500,420,650,7);ctx.fillRect(500,513,650,7);
// handrails along corridors
ctx.strokeStyle='#b6c6cc';ctx.lineWidth=5;for(let x=530;x<1100;x+=70){ctx.beginPath();ctx.moveTo(x,435);ctx.lineTo(x+28,435);ctx.stroke();ctx.beginPath();ctx.moveTo(x,500);ctx.lineTo(x+28,500);ctx.stroke()}
// obstacles
for(const o of obstacles){ctx.fillStyle='#101d2a';ctx.fillRect(o.x+7,o.y+8,o.w,o.h);ctx.fillStyle='#637f8e';ctx.fillRect(o.x,o.y,o.w,o.h);ctx.fillStyle='#8ea7b3';ctx.fillRect(o.x+5,o.y+5,o.w-10,8);ctx.fillStyle='#233e50';ctx.fillRect(o.x+10,o.y+20,o.w-20,o.h-30);ctx.fillStyle='#ffbd63';for(let xx=o.x+12;xx<o.x+o.w-10;xx+=22){ctx.fillRect(xx,o.y+o.h-12,10,4)}ctx.fillStyle='#c5d7e1';ctx.font='11px system-ui';ctx.fillText(o.n,o.x,o.y-7)}
// science destination
ctx.beginPath();ctx.arc(scienceTarget.x,scienceTarget.y,scienceTarget.r+9,0,Math.PI*2);ctx.fillStyle='#52e0cf22';ctx.fill();ctx.beginPath();ctx.arc(scienceTarget.x,scienceTarget.y,scienceTarget.r,0,Math.PI*2);ctx.fillStyle='#123e4c';ctx.fill();ctx.strokeStyle='#53e0cf';ctx.lineWidth=3;ctx.stroke();ctx.fillStyle='#a9fff2';ctx.font='bold 12px system-ui';ctx.textAlign='center';ctx.fillText('SCIENCE',scienceTarget.x,scienceTarget.y-2);ctx.fillText('TARGET',scienceTarget.x,scienceTarget.y+12);ctx.textAlign='left';
// Kibo sphere and glow
ctx.beginPath();ctx.arc(rover.x,rover.y,rover.r+15,0,Math.PI*2);ctx.fillStyle='#4de7ff18';ctx.fill();let grad=ctx.createRadialGradient(rover.x-6,rover.y-8,2,rover.x,rover.y,rover.r+2);grad.addColorStop(0,'#ffffff');grad.addColorStop(.28,'#9beaff');grad.addColorStop(.68,'#329fc6');grad.addColorStop(1,'#12364f');ctx.beginPath();ctx.arc(rover.x,rover.y,rover.r,0,Math.PI*2);ctx.fillStyle=grad;ctx.fill();ctx.strokeStyle='#c4fbff';ctx.lineWidth=2;ctx.stroke();ctx.beginPath();ctx.arc(rover.x+5,rover.y-3,5,0,Math.PI*2);ctx.fillStyle='#071827';ctx.fill();ctx.beginPath();ctx.arc(rover.x+6,rover.y-4,2,0,Math.PI*2);ctx.fillStyle='#53e0cf';ctx.fill();ctx.fillStyle='#e5fbff';ctx.font='bold 13px system-ui';ctx.textAlign='center';ctx.fillText('KIBO',rover.x,rover.y-27);ctx.textAlign='left';
ctx.restore();ctx.fillStyle='#d5f7ff';ctx.font='10px system-ui';ctx.fillText('POSITION '+Math.round(rover.x)+', '+Math.round(rover.y),10,h-12);}
function frame(t){if(!lastFrame)lastFrame=t;let dt=Math.min((t-lastFrame)/1000,.04);lastFrame=t;if(!failed){let dx=0,dy=0;if(keys.ArrowLeft||keys.a)dx--;if(keys.ArrowRight||keys.d)dx++;if(keys.ArrowUp||keys.w)dy--;if(keys.ArrowDown||keys.s)dy++;if(dx&&dy){dx*=.7071;dy*=.7071}let nx=rover.x+dx*rover.speed*dt,ny=rover.y+dy*rover.speed*dt;nx=Math.max(rover.r+12,Math.min(WORLD.w-rover.r-12,nx));ny=Math.max(rover.r+12,Math.min(WORLD.h-rover.r-12,ny));let hit=obstacles.find(o=>circleRect(nx,ny,rover.r,o));if(hit){failed=true;document.getElementById('failReason').textContent='Kibo hit '+hit.n+'. Collision safety protocol triggered.';document.getElementById('failOverlay').classList.add('show');document.getElementById('mapStatus').textContent='COLLISION · RUN FAILED';log('COLLISION: Kibo struck '+hit.n+'. Exploration run failed.','bad')}else{rover.x=nx;rover.y=ny;explored+=Math.abs(dx)+Math.abs(dy);if(Math.hypot(rover.x-scienceTarget.x,rover.y-scienceTarget.y)<scienceTarget.r+rover.r){document.getElementById('mapStatus').textContent='SCIENCE TARGET REACHED';}else if(dx||dy)document.getElementById('mapStatus').textContent='KIBO MOVING · NAVIGATION ACTIVE'}}drawMap();requestAnimationFrame(frame)}
window.addEventListener('keydown',e=>{if(['ArrowUp','ArrowDown','ArrowLeft','ArrowRight',' '].includes(e.key))e.preventDefault();keys[e.key]=true;keys[e.key.toLowerCase()]=true});window.addEventListener('keyup',e=>{keys[e.key]=false;keys[e.key.toLowerCase()]=false});window.addEventListener('blur',()=>keys={});window.addEventListener('resize',resizeMap);let pointerMove=false;mapCanvas.addEventListener('pointerdown',e=>{pointerMove=true;mapCanvas.setPointerCapture(e.pointerId);keys.pointer=true;});mapCanvas.addEventListener('pointerup',()=>{pointerMove=false;keys.pointer=false;keys.a=keys.d=keys.w=keys.s=false});mapCanvas.addEventListener('pointermove',e=>{if(!pointerMove||failed)return;let r=mapCanvas.getBoundingClientRect(),dx=e.clientX-r.left-r.width/2,dy=e.clientY-r.top-r.height/2;keys.a=dx< -10;keys.d=dx>10;keys.w=dy< -10;keys.s=dy>10});
resizeMap();requestAnimationFrame(frame);draw();
</script></body></html>"""

@app.get("/")
def home():
    s = state()
    return render_template_string(PAGE, s=s, commands=COMMANDS,
        command_labels={k:v[0] for k,v in COMMANDS.items()},
        objectives=OBJECTIVES, progress=progress(s))

@app.post("/reset")
def reset():
    session["game"] = fresh()
    session.modified = True
    return redirect(url_for("home"))

@app.get("/save")
def export_save():
    return jsonify(state())

@app.post("/action")
def action():
    s = state()
    d = request.get_json(silent=True) or {}
    act = d.get("action")
    messages = []
    if act == "add":
        c = d.get("command")
        if c not in COMMANDS:
            return jsonify({"messages":[{"text":"Unknown command.","kind":"bad"}]})
        if len(s["program"]) >= 12:
            messages.append({"text":"Program limit reached (12 commands).","kind":"warn"})
        else:
            s["program"].append(c)
            event(s, "Added command: " + COMMANDS[c][0] + ".")
            messages.append({"text":"Added " + COMMANDS[c][0] + ".", "kind":"ok"})
    elif act == "remove":
        i = d.get("index")
        if isinstance(i,int) and 0 <= i < len(s["program"]):
            c = s["program"].pop(i)
            event(s,"Removed command: "+COMMANDS[c][0]+".","warn")
            messages.append({"text":"Removed "+COMMANDS[c][0]+".","kind":"warn"})
    elif act == "clear":
        s["program"] = []
        event(s,"Program sequence cleared.","warn")
        messages.append({"text":"Program sequence cleared.","kind":"warn"})
    elif act == "recommended":
        s["program"] = SAFE_PLAN.copy()
        event(s,"Loaded recommended safe mission plan.")
        messages.append({"text":"Safe plan loaded. Execute it when ready.","kind":"ok"})
    elif act == "diagnostic":
        if s["battery"] < 15:
            s["battery"] = min(100, s["battery"] + 8)
            msg = "Power diagnostic recovered 8% battery reserve."
        else:
            s["navigation"] = min(100, s["navigation"] + 10)
            msg = "Diagnostics complete. Navigation confidence improved."
        event(s,msg)
        messages.append({"text":msg,"kind":"ok"})
    elif act == "execute":
        p = d.get("program",s["program"])
        if not isinstance(p,list) or len(p)>12 or any(c not in COMMANDS for c in p):
            return jsonify({"messages":[{"text":"Invalid command sequence.","kind":"bad"}]})
        s["program"] = p
        s["runs"] += 1
        if not p:
            s["status"] = "WAITING"
            messages.append({"text":"Add commands or load the safe plan first.","kind":"warn"})
        elif s["battery"] < 12:
            s["status"] = "POWER HOLD"
            messages.append({"text":"Execution held: battery reserve too low. Run diagnostics.","kind":"bad"})
        else:
            points = 0
            for c in p:
                if c == "calibrate":
                    s["completed"]["calibrate"] = True
                    s["navigation"] = min(100,s["navigation"]+25)
                    points += 10
                    msg,kind = "Sensors calibrated. Navigation solution stable.","ok"
                elif c == "navigate":
                    if s["completed"]["calibrate"]:
                        s["completed"]["navigate"] = True
                        s["navigation"] = min(100,s["navigation"]+10)
                        s["battery"] = max(0,s["battery"]-8)
                        points += 15
                        msg,kind = "Science rack reached inside the ISS. Relative position verified.","ok"
                    else:
                        s["navigation"] = max(0,s["navigation"]-15)
                        s["battery"] = max(0,s["battery"]-5)
                        msg,kind = "SAFETY HOLD: calibrate sensors before navigation.","bad"
                elif c == "deploy":
                    if s["completed"]["navigate"]:
                        s["completed"]["deploy"] = True
                        s["battery"] = max(0,s["battery"]-12)
                        points += 20
                        msg,kind = "Robot arm deployed inside the ISS laboratory. Joint telemetry nominal.","ok"
                    else:
                        s["battery"] = max(0,s["battery"]-4)
                        msg,kind = "DEPLOYMENT BLOCKED: reach the payload first.","bad"
                elif c == "inspect":
                    if s["completed"]["deploy"]:
                        s["completed"]["inspect"] = True
                        s["science"] = min(100,s["science"]+45)
                        points += 20
                        msg,kind = "Internal science rack inspection complete. Imagery and telemetry received.","ok"
                    else:
                        msg,kind = "Inspection skipped: deploy the arm first.","warn"
                elif c == "experiment":
                    if s["completed"]["inspect"]:
                        s["completed"]["experiment"] = True
                        s["science"] = 100
                        points += 25
                        msg,kind = "Microgravity experiment complete. Science data secured.","ok"
                    else:
                        msg,kind = "Experiment on hold: inspect payload first.","warn"
                else:
                    if s["completed"]["deploy"]:
                        s["completed"]["stow"] = True
                        s["battery"] = max(0,s["battery"]-4)
                        points += 10
                        msg,kind = "Robotic arm retracted and secured.","ok"
                    else:
                        s["completed"]["stow"] = True
                        msg,kind = "Stow confirmed; arm remains in safe configuration.","ok"
                event(s,msg,kind)
                messages.append({"text":msg,"kind":kind})
            s["score"] += points
            s["status"] = "IN PROGRESS"
            if progress(s) == 100:
                s["status"] = "SUCCESS"
                if not s["bonus"]:
                    s["score"] += 100
                    s["bonus"] = True
                    msg = "MISSION COMPLETE! All objectives achieved. +100 mission bonus."
                    event(s,msg)
                    messages.append({"text":msg,"kind":"ok"})
            elif any(m["kind"]=="bad" for m in messages):
                s["status"] = "REVIEW"
            if s["battery"] <= 0 and progress(s) < 100:
                s["status"] = "POWER HOLD"
                messages.append({"text":"Battery depleted. Reset the mission to retry.","kind":"bad"})
    else:
        return jsonify({"messages":[{"text":"Unknown action.","kind":"bad"}]}), 400
    save(s)
    return jsonify({
        "program":s["program"],
        "state":{"score":s["score"],"runs":s["runs"],"status":s["status"],"progress":progress(s),
                 "battery":s["battery"],"navigation":s["navigation"],"science":s["science"]},
        "objectives":[{"key":k,"done":bool(s["completed"][k]),"number":i+1} for i,(k,_,_) in enumerate(OBJECTIVES)],
        "messages":messages
    })

@app.errorhandler(500)
def error(_):
    return "Mission Trainer error. Please refresh the page and check the Render logs if it continues.", 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT","5000")), debug=False)
