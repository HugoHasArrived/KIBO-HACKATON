```python
import os
from flask import Flask, jsonify, render_template_string

app = Flask(__name__)

PAGE = r"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Kibo | Junior Astronaut Mission Trainer</title>
<style>
:root {
  --bg:#060914;
  --panel:#10182a;
  --panel2:#151f34;
  --line:#283956;
  --text:#edf5ff;
  --muted:#9baecc;
  --cyan:#53e7ff;
  --green:#73f5b0;
  --orange:#ffbd69;
  --red:#ff647c;
}
*{box-sizing:border-box}
body{
  margin:0;background:radial-gradient(ellipse at 50% 0%,#14274a 0%,#080e1d 46%,#04060d 100%);
  color:var(--text);font-family:Inter,Segoe UI,Arial,sans-serif;min-height:100vh;
}
button{font:inherit;cursor:pointer}
button:focus-visible{outline:2px solid white;outline-offset:3px}
.topbar{
  display:flex;align-items:center;justify-content:space-between;gap:15px;
  padding:15px 22px;border-bottom:1px solid #283956;background:#080d18eF;
  position:sticky;top:0;z-index:10;backdrop-filter:blur(12px)
}
.brand{display:flex;align-items:center;gap:12px}
.logo{
  width:43px;height:43px;border-radius:12px;background:linear-gradient(135deg,#43dfff,#647bff);
  display:grid;place-items:center;color:#061020;font-size:24px;font-weight:900;
  box-shadow:0 0 24px #45dfff44
}
.brand h1{font-size:17px;letter-spacing:2px;margin:0}
.brand p{font-size:11px;color:var(--muted);margin:4px 0 0}
.top-status{display:flex;gap:8px;align-items:center;flex-wrap:wrap}
.pill{border:1px solid var(--line);border-radius:30px;padding:7px 11px;font-size:11px;color:#c6d6ef}
.dot{display:inline-block;width:7px;height:7px;border-radius:50%;background:var(--green);margin-right:6px}
main{max-width:1500px;margin:auto;padding:18px}
.layout{display:grid;grid-template-columns:minmax(0,1fr) 310px;gap:16px}
.left,.right{min-width:0}
.panel{background:linear-gradient(145deg,#111a2c,#0b1120);border:1px solid var(--line);border-radius:15px;overflow:hidden}
.panel-head{display:flex;align-items:center;justify-content:space-between;gap:10px;padding:13px 15px;border-bottom:1px solid #24324b}
.panel-head h2{font-size:12px;letter-spacing:1.6px;margin:0}
.eyebrow{font-size:10px;letter-spacing:1.4px;color:var(--cyan);text-transform:uppercase}
.small{font-size:11px;color:var(--muted)}
.stage{position:relative;background:#030713;min-height:340px}
canvas{display:block;width:100%;height:auto;aspect-ratio:16/9;max-height:620px;touch-action:none}
.hud{position:absolute;inset:12px;display:flex;justify-content:space-between;align-items:flex-start;pointer-events:none}
.hud-group{display:grid;gap:7px}
.hud-chip{background:#080e1bdc;border:1px solid #30415f;border-radius:7px;padding:7px 9px;font-size:10px;letter-spacing:.6px;backdrop-filter:blur(6px)}
.hud-chip strong{color:var(--cyan);font-size:12px}
.stage-bottom{position:absolute;left:12px;right:12px;bottom:12px;display:flex;justify-content:space-between;align-items:end;gap:8px;pointer-events:none}
.message{max-width:75%;background:#080e1be8;border:1px solid #344663;padding:9px 11px;border-radius:8px;font-size:11px;color:#d8e8ff}
.crosshair{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);color:#9aefff;font-size:23px;opacity:.5;pointer-events:none}
.actions{display:flex;gap:7px;flex-wrap:wrap}
.btn{
  border:1px solid #354967;background:#19263c;color:#e9f4ff;padding:9px 12px;border-radius:8px;
  font-size:11px;font-weight:700;transition:.15s
}
.btn:hover{background:#243754;border-color:#6b91bd}
.btn.primary{background:linear-gradient(135deg,#4be1ff,#73b9ff);color:#061020;border:0}
.btn.danger{color:#ff9baa;border-color:#73394a}
.btn:disabled{opacity:.35;cursor:not-allowed}
.toolbar{display:flex;align-items:center;justify-content:space-between;gap:10px;padding:11px 13px;border-top:1px solid var(--line);flex-wrap:wrap}
.metrics{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:10px;margin-top:12px}
.metric{padding:13px;border:1px solid var(--line);border-radius:12px;background:#10182a}
.metric label{font-size:10px;color:var(--muted);letter-spacing:1px}
.metric strong{display:block;font-size:22px;margin:8px 0 9px;font-variant-numeric:tabular-nums}
.unit{font-size:10px;color:var(--muted);font-weight:500}
.track{height:5px;background:#27334a;border-radius:5px;overflow:hidden}
.fill{height:100%;width:100%;background:var(--cyan);transition:width .2s}
.fill.green{background:var(--green)}.fill.orange{background:var(--orange)}.fill.red{background:var(--red)}
.right{display:grid;align-content:start;gap:12px}
.pad{padding:14px}
.progress-head{display:flex;justify-content:space-between;gap:10px;font-size:11px;margin-bottom:10px}
.progress{height:6px;background:#27334a;border-radius:5px;overflow:hidden;margin-bottom:14px}
.progress div{height:100%;width:0;background:linear-gradient(90deg,#4ae4ff,#8a9dff);transition:width .2s}
.objectives{display:grid;gap:9px}
.objective{display:flex;gap:10px;align-items:flex-start;border:1px solid #263650;background:#10192b;padding:10px;border-radius:9px}
.obj-check{width:20px;height:20px;border:1px solid #415574;border-radius:6px;display:grid;place-items:center;flex-shrink:0;font-size:12px}
.objective.done{opacity:.65}.objective.done .obj-check{background:#164c3d;border-color:#42bd8f;color:#8bffca}
.obj-title{font-size:11px;font-weight:700;line-height:1.4}
.obj-desc{font-size:10px;color:var(--muted);line-height:1.5;margin-top:4px}
.statusline{display:flex;justify-content:space-between;gap:10px;font-size:11px;padding:8px 0;border-bottom:1px solid #22304a}
.statusline:last-child{border-bottom:0}
.statusline span{color:var(--muted)}
.value{color:#eaf5ff;font-weight:700;text-align:right}
.console{font-family:Consolas,monospace;font-size:10px;line-height:1.7;color:#a8c4e8;background:#050a14;border:1px solid #202e45;border-radius:8px;padding:10px;min-height:90px;max-height:145px;overflow:auto}
.console p{margin:0 0 3px}
.console .good{color:#7af4bd}.console .warn{color:#ffcc7c}.console .bad{color:#ff8fa1}
.controls-grid{display:grid;grid-template-columns:1fr 1fr;gap:7px}
.control-card{background:#111b2d;border:1px solid #2a3b56;border-radius:9px;padding:9px}
.control-card strong{font-size:11px;display:block}
.control-card span{font-size:10px;color:var(--muted);line-height:1.5}
.key{display:inline-grid;place-items:center;min-width:23px;height:22px;padding:0 5px;border:1px solid #435a7b;border-radius:5px;background:#1c2b43;color:#eaf5ff;font-size:10px;margin-right:4px}
.mobile-controls{display:none;grid-template-columns:repeat(3,1fr);gap:8px;margin-top:12px}
.mobile-controls button{min-height:47px;font-weight:800;font-size:15px;touch-action:none;user-select:none}
.footer{text-align:center;color:#7587a5;font-size:10px;padding:22px 0 10px;line-height:1.7}
.overlay{
  position:absolute;inset:0;z-index:5;display:flex;align-items:center;justify-content:center;
  padding:18px;background:#020612d9;backdrop-filter:blur(6px)
}
.overlay-card{width:min(470px,100%);padding:27px;border:1px solid #405778;border-radius:17px;
  background:linear-gradient(150deg,#15233a,#080d1a);box-shadow:0 20px 80px #0009;text-align:center}
.overlay-card .symbol{font-size:42px;margin-bottom:9px}
.overlay-card h2{font-size:25px;letter-spacing:2px;margin:0 0 10px}
.overlay-card p{font-size:12px;line-height:1.7;color:#aebfda}
.overlay-card .btn{margin-top:7px}
.countdown{font-size:52px;color:var(--cyan);font-weight:900;margin:15px}
.select{background:#10192b;border:1px solid #334965;color:#eaf5ff;padding:9px;border-radius:8px}
.notice{font-size:10px;color:var(--muted);line-height:1.6;margin-top:10px}
.hidden{display:none!important}
@media(max-width:1000px){.layout{grid-template-columns:minmax(0,1fr)}.right{grid-template-columns:repeat(2,minmax(0,1fr))}.right .wide{grid-column:1/-1}}
@media(max-width:620px){
  main{padding:10px}.topbar{padding:11px 12px}.brand h1{font-size:14px}.brand p{font-size:10px}
  .top-status .pill:nth-child(2){display:none}.metrics{grid-template-columns:repeat(2,minmax(0,1fr))}
  .right{grid-template-columns:1fr}.right .wide{grid-column:auto}
  .stage{min-height:220px}.hud{inset:7px}.hud-chip{padding:5px 6px;font-size:9px}
  .hud-chip strong{font-size:10px}.message{font-size:10px;max-width:90%}
  .mobile-controls{display:grid}.panel-head{padding:11px}.metric{padding:11px}.metric strong{font-size:20px}
}
</style>
</head>
<body>
<header class="topbar">
  <div class="brand">
    <div class="logo">K</div>
    <div><h1>KIBO <span style="color:var(--cyan)">MISSION TRAINER</span></h1>
      <p>JUNIOR ASTRONAUT PROGRAM · INTERACTIVE SIMULATION</p></div>
  </div>
  <div class="top-status">
    <div class="pill"><span class="dot"></span><span id="connection">SIMULATION READY</span></div>
    <div class="pill">MISSION <strong id="missionCode">KBT-01</strong></div>
  </div>
</header>

<main>
<div class="layout">
<section class="left">
  <div class="panel">
    <div class="panel-head">
      <div><div class="eyebrow">Flight deck / external view</div><h2 style="margin-top:5px">ORBITAL OPERATIONS</h2></div>
      <div class="actions">
        <button class="btn" id="pauseBtn" onclick="togglePause()">Ⅱ PAUSE</button>
        <button class="btn danger" onclick="resetMission()">↻ RESET</button>
      </div>
    </div>
    <div class="stage">
      <canvas id="space" width="960" height="540" aria-label="Interactive spaceflight simulation"></canvas>
      <div class="crosshair">+</div>
      <div class="hud">
        <div class="hud-group">
          <div class="hud-chip">FLIGHT MODE<br><strong id="flightMode">PRE-LAUNCH</strong></div>
          <div class="hud-chip">VELOCITY<br><strong id="hudSpeed">0.0 m/s</strong></div>
        </div>
        <div class="hud-group" style="text-align:right">
          <div class="hud-chip">ALTITUDE<br><strong id="hudAlt">0.0 km</strong></div>
          <div class="hud-chip">TARGET RANGE<br><strong id="hudRange">— km</strong></div>
        </div>
      </div>
      <div class="stage-bottom">
        <div class="message" id="missionMessage">Welcome, cadet. Complete the pre-flight checklist to begin.</div>
        <div class="hud-chip">UTC <strong id="clock">00:00:00</strong></div>
      </div>
      <div class="overlay" id="overlay">
        <div class="overlay-card" id="overlayCard">
          <div class="symbol">🛰️</div>
          <div class="eyebrow">Training mission 01</div>
          <h2>KIBO: ORBITAL RESCUE</h2>
          <p>You are the pilot of a small training spacecraft. Launch, inspect orbital modules, manage your resources, and practice a careful docking approach.</p>
          <p><strong>Mission briefing:</strong> Your spacecraft is in a simulated environment. Learn how thrust, inertia, scanning, and docking work through guided objectives.</p>
          <div style="display:flex;gap:8px;justify-content:center;flex-wrap:wrap">
            <button class="btn primary" onclick="beginCountdown()">▶ START LAUNCH SEQUENCE</button>
            <button class="btn" onclick="quickStart()">QUICK START</button>
          </div>
          <p class="notice">Educational game only. This is not an official NASA, JAXA, or space-agency simulator.</p>
        </div>
      </div>
    </div>
    <div class="toolbar">
      <div class="small">FLIGHT CONTROLS · KEYBOARD OR TOUCH</div>
      <div class="actions">
        <button class="btn" onclick="scanTarget()">⌖ SCAN TARGET [ENTER]</button>
        <button class="btn" onclick="brake()">◉ COUNTER-THRUST [SPACE]</button>
      </div>
    </div>
  </div>

  <div class="metrics">
    <div class="metric"><label>PROPELLANT</label><strong id="fuelText">100 <span class="unit">%</span></strong><div class="track"><div class="fill green" id="fuelBar"></div></div></div>
    <div class="metric"><label>BATTERY</label><strong id="batteryText">100 <span class="unit">%</span></strong><div class="track"><div class="fill" id="batteryBar"></div></div></div>
    <div class="metric"><label>HULL INTEGRITY</label><strong id="hullText">100 <span class="unit">%</span></strong><div class="track"><div class="fill green" id="hullBar"></div></div></div>
    <div class="metric"><label>MISSION SCORE</label><strong id="scoreText">0000 <span class="unit">PTS</span></strong><div class="track"><div class="fill" id="scoreBar"></div></div></div>
  </div>

  <div class="mobile-controls">
    <button class="btn" data-control="forward">▲ THRUST</button>
    <button class="btn" data-control="brake">● BRAKE</button>
    <button class="btn" data-control="scan">⌖ SCAN</button>
    <button class="btn" data-control="left">↶ ROTATE</button>
    <button class="btn" data-control="back">▼ REVERSE</button>
    <button class="btn" data-control="right">ROTATE ↷</button>
    <button class="btn" data-control="strafeLeft">◀ STRAFE</button>
    <button class="btn" data-control="strafeRight">STRAFE ▶</button>
    <button class="btn" data-control="pause">Ⅱ PAUSE</button>
  </div>
</section>

<aside class="right">
  <div class="panel">
    <div class="panel-head"><h2>MISSION OBJECTIVES</h2><span class="small" id="objectiveCount">0 / 7</span></div>
    <div class="pad">
      <div class="progress-head"><span>MISSION PROGRESS</span><strong id="progressText">0%</strong></div>
      <div class="progress"><div id="progressBar"></div></div>
      <div class="objectives" id="objectives"></div>
    </div>
  </div>

  <div class="panel">
    <div class="panel-head"><h2>SPACECRAFT TELEMETRY</h2><span class="eyebrow">LIVE</span></div>
    <div class="pad">
      <div class="statusline"><span>Flight state</span><strong class="value" id="stateText">Standby</strong></div>
      <div class="statusline"><span>Position X</span><strong class="value" id="posX">0.0</strong></div>
      <div class="statusline"><span>Position Y</span><strong class="value" id="posY">0.0</strong></div>
      <div class="statusline"><span>Relative speed</span><strong class="value" id="speedValue">0.0 m/s</strong></div>
      <div class="statusline"><span>Nearest target</span><strong class="value" id="targetText">Not acquired</strong></div>
      <div class="statusline"><span>Docking alignment</span><strong class="value" id="alignText">—</strong></div>
    </div>
  </div>

  <div class="panel">
    <div class="panel-head"><h2>LOCAL RADAR</h2><span class="small">RELATIVE POSITION</span></div>
    <div class="pad"><canvas id="radar" width="280" height="180" style="aspect-ratio:14/9;border-radius:8px;border:1px solid #273b57"></canvas>
      <div class="notice">Blue = spacecraft · Cyan = modules · Green = docking port</div>
    </div>
  </div>

  <div class="panel">
    <div class="panel-head"><h2>MISSION CONTROL</h2><span class="eyebrow">COMMS</span></div>
    <div class="pad"><div class="console" id="console"><p class="good">[SYSTEM] Trainer initialized.</p><p>[FLIGHT] Awaiting pilot command.</p></div>
      <div class="actions" style="margin-top:9px">
        <button class="btn" onclick="requestStatus()">REQUEST STATUS</button>
        <button class="btn" onclick="scanTarget()">RUN SCAN</button>
      </div>
    </div>
  </div>

  <div class="panel wide">
    <div class="panel-head"><h2>FLIGHT CONTROL GUIDE</h2><span class="small">KEYBOARD</span></div>
    <div class="pad">
      <div class="controls-grid">
        <div class="control-card"><strong><span class="key">W</span> Main thrust</strong><span>Accelerate forward in the direction you face.</span></div>
        <div class="control-card"><strong><span class="key">S</span> Reverse thrust</strong><span>Apply thrust in the opposite direction.</span></div>
        <div class="control-card"><strong><span class="key">A</span><span class="key">D</span> Rotate</strong><span>Turn the spacecraft left or right.</span></div>
        <div class="control-card"><strong><span class="key">Q</span><span class="key">E</span> Strafe</strong><span>Translate sideways without turning.</span></div>
        <div class="control-card"><strong><span class="key">SPACE</span> Brake</strong><span>Counter-thrust to reduce drift.</span></div>
        <div class="control-card"><strong><span class="key">ENTER</span> Scan</strong><span>Inspect nearby objectives and modules.</span></div>
      </div>
      <p class="notice">Tip: space has inertia. Release thrust early and use short braking pulses before approaching the docking port.</p>
    </div>
  </div>
</aside>
</div>
<div class="footer">KIBO JUNIOR ASTRONAUT MISSION TRAINER · EDUCATIONAL SPACEFLIGHT GAME<br>All positions, distances, speeds, and spacecraft systems are simplified for gameplay and are not real flight data.</div>
</main>

<script>
"use strict";

const canvas = document.getElementById("space");
const ctx = canvas.getContext("2d");
const radar = document.getElementById("radar");
const rctx = radar.getContext("2d");

const missions = [
  {name:"Launch sequence",desc:"Complete launch and enter the orbital training area.",x:-380,y:160,range:120,score:100},
  {name:"Alpha Joint",desc:"Approach the first orbital module and scan it.",x:-120,y:-90,range:85,score:150},
  {name:"Rack 01",desc:"Inspect the equipment rack. Keep your speed under control.",x:120,y:-145,range:80,score:150},
  {name:"Bravo Node",desc:"Reach the connection node and run a system scan.",x:310,y:35,range:85,score:200},
  {name:"Hatch Inspection",desc:"Approach the service hatch and inspect the outer structure.",x:100,y:235,range:75,score:200},
  {name:"Rack 02",desc:"Inspect the second equipment rack.",x:-155,y:205,range:80,score:200},
  {name:"Docking Port",desc:"Approach the green docking port slowly and complete docking.",x:390,y:-230,range:55,score:500}
];

const state = {
  mode:"PRE-LAUNCH",
  running:false,
  paused:false,
  complete:false,
  countdown:0,
  launchTime:0,
  elapsed:0,
  fuel:100,
  battery:100,
  hull:100,
  score:0,
  x:-440,
  y:290,
  vx:0,
  vy:0,
  angle:-0.55,
  altitude:0,
  scanned:{},
  current:0,
  message:"Welcome, cadet. Complete the pre-flight checklist to begin.",
  scanCooldown:0,
  thrusting:false,
  lastFrame:0,
  sessionStart:Date.now()
};

const stars = [];
let seed = 529;
function rand(){
  seed=(seed*16807)%2147483647;
  return (seed-1)/2147483646;
}
for(let i=0;i<240;i++){
  stars.push({x:rand()*canvas.width,y:rand()*canvas.height,r:rand()*1.5+.3,a:rand()*.65+.25,p:rand()*6});
}

function log(text,type=""){
  const box=document.getElementById("console");
  const p=document.createElement("p");
  p.textContent="["+new Date().toLocaleTimeString([], {hour12:false})+"] "+text;
  if(type)p.className=type;
  box.appendChild(p);
  while(box.children.length>35)box.removeChild(box.firstChild);
  box.scrollTop=box.scrollHeight;
}

function setMessage(text){
  state.message=text;
  document.getElementById("missionMessage").textContent=text;
}

function beginCountdown(){
  if(state.running)return;
  state.countdown=10;
  state.mode="COUNTDOWN";
  state.paused=false;
  document.getElementById("overlayCard").innerHTML=
    '<div class="symbol">🚀</div><div class="eyebrow">Launch sequence initiated</div>'+
    '<h2>ALL SYSTEMS GO</h2><p>Strap in, cadet. Watch the countdown and prepare for orbital insertion.</p>'+
    '<div class="countdown" id="countdownNumber">10</div><p>Keep your hands clear of the controls during automated ascent.</p>'+
    '<button class="btn danger" onclick="resetMission()">ABORT / RESET</button>';
  log("Launch sequence initiated.","warn");
  setMessage("Launch countdown initiated. Automated ascent will begin at T-0.");
  tickCountdown();
}

function tickCountdown(){
  if(state.mode!=="COUNTDOWN")return;
  document.getElementById("countdownNumber").textContent=Math.max(0,Math.ceil(state.countdown));
  if(state.countdown<=0){
    startMission(true);
    return;
  }
  state.countdown-=1;
  setTimeout(tickCountdown,1000);
}

function quickStart(){
  document.getElementById("overlay").classList.add("hidden");
  startMission(false);
}

function startMission(automated){
  state.running=true;
  state.paused=false;
  state.mode=automated?"ASCENT":"ORBIT";
  state.launchTime=automated?performance.now():0;
  state.elapsed=0;
  document.getElementById("overlay").classList.add("hidden");
  document.getElementById("pauseBtn").textContent="Ⅱ PAUSE";
  document.getElementById("connection").textContent="FLIGHT ACTIVE";
  log(automated?"Liftoff confirmed. Automated ascent started.":"Quick-start mode engaged. Orbital training active.","good");
  log("Telemetry and objective tracking online.");
  setMessage(automated?"Liftoff! Hold position while the ascent sequence completes.":"Orbital training started. Head toward the first module.");
  if(!automated)completeObjective(0);
  updateObjectives();
}

function resetMission(){
  state.mode="PRE-LAUNCH";
  state.running=false;
  state.paused=false;
  state.complete=false;
  state.countdown=0;
  state.launchTime=0;
  state.elapsed=0;
  state.fuel=100;
  state.battery=100;
  state.hull=100;
  state.score=0;
  state.x=-440;
  state.y=290;
  state.vx=0;
  state.vy=0;
  state.angle=-0.55;
  state.altitude=0;
  state.scanned={};
  state.current=0;
  state.scanCooldown=0;
  state.sessionStart=Date.now();
  document.getElementById("overlay").classList.remove("hidden");
  document.getElementById("overlayCard").innerHTML=
    '<div class="symbol">🛰️</div><div class="eyebrow">Training mission 01</div>'+
    '<h2>KIBO: ORBITAL RESCUE</h2>'+
    '<p>You are the pilot of a small training spacecraft. Launch, inspect orbital modules, manage your resources, and practice a careful docking approach.</p>'+
    '<p><strong>Mission briefing:</strong> Your spacecraft is in a simulated environment. Learn how thrust, inertia, scanning, and docking work through guided objectives.</p>'+
    '<div style="display:flex;gap:8px;justify-content:center;flex-wrap:wrap">'+
    '<button class="btn primary" onclick="beginCountdown()">▶ START LAUNCH SEQUENCE</button>'+
    '<button class="btn" onclick="quickStart()">QUICK START</button></div>'+
    '<p class="notice">Educational game only. This is not an official NASA, JAXA, or space-agency simulator.</p>';
  document.getElementById("connection").textContent="SIMULATION READY";
  document.getElementById("pauseBtn").textContent="Ⅱ PAUSE";
  document.getElementById("console").innerHTML="";
  log("Simulation reset. Awaiting pilot.","good");
  setMessage("Welcome, cadet. Complete the pre-flight checklist to begin.");
  updateObjectives();
  updateUI();
}

function togglePause(){
  if(!state.running)return;
  state.paused=!state.paused;
  document.getElementById("pauseBtn").textContent=state.paused?"▶ RESUME":"Ⅱ PAUSE";
  if(state.paused){
    state.mode="PAUSED";
    log("Flight simulation paused.","warn");
    setMessage("Simulation paused. Press Resume or P to continue.");
  }else{
    state.mode="ORBIT";
    log("Flight simulation resumed.","good");
    setMessage("Simulation resumed. Monitor your drift and remaining resources.");
  }
  if(state.complete)state.mode="COMPLETE";
}

function completeObjective(index){
  if(state.scanned[index])return;
  state.scanned[index]=true;
  state.score+=missions[index].score;
  log("Objective complete: "+missions[index].name+". +" + missions[index].score+" points.","good");
  if(index===missions.length-1){
    state.complete=true;
    state.mode="COMPLETE";
    state.running=false;
    setMessage("Docking complete! You have completed the orbital training mission.");
    log("MISSION SUCCESS. All training objectives completed.","good");
    document.getElementById("connection").textContent="MISSION COMPLETE";
  }else{
    const next=missions.findIndex((m,i)=>i>index&&!state.scanned[i]);
    state.current=next<0?index:next;
    setMessage("Objective complete: "+missions[index].name+". Next: "+missions[state.current].name+".");
  }
  updateObjectives();
}

function distanceTo(m){
  return Math.hypot(state.x-m.x,state.y-m.y);
}

function getNearest(){
  let best=-1,dist=Infinity;
  missions.forEach((m,i)=>{
    if(!state.scanned[i]){
      const d=distanceTo(m);
      if(d<dist){dist=d;best=i;}
    }
  });
  return {index:best,distance:dist};
}

function scanTarget(){
  if(!state.running||state.paused||state.complete){
    log("Scan unavailable: start or resume the mission first.","warn");
    return;
  }
  if(state.scanCooldown>0){
    log("Scanner cooling down. Please wait.","warn");
    return;
  }
  if(state.battery<1){
    log("Scanner offline: insufficient battery.","bad");
    return;
  }
  state.battery=Math.max(0,state.battery-1.5);
  state.scanCooldown=1.2;
  const nearest=getNearest();
  if(nearest.index<0){
    log("All objectives already completed.","good");
    return;
  }
  const m=missions[nearest.index];
  if(nearest.distance<=m.range){
    if(nearest.index===missions.length-1){
      const speed=Math.hypot(state.vx,state.vy);
      const targetAngle=Math.atan2(m.y-state.y,m.x-state.x);
      const diff=Math.abs(Math.atan2(Math.sin(state.angle-targetAngle),Math.cos(state.angle-targetAngle)));
      if(speed>18){
        log("Docking denied: relative speed too high. Reduce speed below 18 m/s.","warn");
        setMessage("Docking approach too fast. Use counter-thrust until relative speed is below 18 m/s.");
        return;
      }
      if(nearest.distance>35){
        log("Docking port acquired. Move closer to complete docking.","warn");
        return;
      }
      if(diff>0.95){
        log("Docking alignment poor. Rotate toward the docking port.","warn");
        setMessage("Docking alignment poor. Rotate toward the green docking port.");
        return;
      }
      completeObjective(nearest.index);
      return;
    }
    completeObjective(nearest.index);
  }else{
    log("Scan detected "+m.name+" at "+nearest.distance.toFixed(0)+" km. Move closer.","warn");
    setMessage(m.name+" detected. Distance: "+nearest.distance.toFixed(0)+" km. Approach carefully to scan.");
  }
}

function brake(){
  if(!state.running||state.paused)return;
  const speed=Math.hypot(state.vx,state.vy);
  if(speed<.15){
    state.vx=0;state.vy=0;
    log("Drift already stabilized.");
    return;
  }
  const factor=Math.max(0,1-0.85/(speed||1));
  state.vx*=factor;
  state.vy*=factor;
  state.fuel=Math.max(0,state.fuel-.12);
  log("Counter-thrust pulse applied.");
}

function requestStatus(){
  const speed=Math.hypot(state.vx,state.vy);
  log("State: "+state.mode+" | speed "+speed.toFixed(1)+" m/s | fuel "+state.fuel.toFixed(1)+"% | hull "+state.hull.toFixed(1)+"%.");
}

const keys=new Set();
window.addEventListener("keydown",e=>{
  const key=e.key.toLowerCase();
  if([" ","arrowup","arrowdown","arrowleft","arrowright"].includes(key))e.preventDefault();
  if(["w","a","s","d","q","e"," ","enter","p","r","arrowup","arrowdown","arrowleft","arrowright"].includes(key)){
    keys.add(key);
  }
  if(key==="enter"&&!e.repeat)scanTarget();
  if(key==="p"&&!e.repeat)togglePause();
  if(key==="r"&&!e.repeat)resetMission();
});
window.addEventListener("keyup",e=>keys.delete(e.key.toLowerCase()));
window.addEventListener("blur",()=>keys.clear());

function bindTouch(button,control){
  let timer=null;
  const start=e=>{
    e.preventDefault();
    if(control==="scan"){scanTarget();return}
    if(control==="brake"){brake();return}
    if(control==="pause"){togglePause();return}
    const map={forward:"w",back:"s",left:"a",right:"d",strafeLeft:"q",strafeRight:"e"};
    const k=map[control];
    if(k)keys.add(k);
  };
  const end=e=>{
    e.preventDefault();
    const map={forward:"w",back:"s",left:"a",right:"d",strafeLeft:"q",strafeRight:"e"};
    const k=map[control];
    if(k)keys.delete(k);
  };
  button.addEventListener("pointerdown",start);
  button.addEventListener("pointerup",end);
  button.addEventListener("pointercancel",end);
  button.addEventListener("pointerleave",end);
}
document.querySelectorAll("[data-control]").forEach(b=>bindTouch(b,b.dataset.control));

function updatePhysics(dt){
  if(!state.running||state.paused||state.complete)return;
  state.elapsed+=dt;
  state.scanCooldown=Math.max(0,state.scanCooldown-dt);
  state.battery=Math.max(0,state.battery-dt*.025);

  if(state.mode==="ASCENT"){
    const t=(performance.now()-state.launchTime)/1000;
    state.altitude=Math.min(420,t*55);
    if(t<2.5){
      state.y+=dt*30;
      state.vy=-35;
    }else if(t<5.5){
      state.x+=dt*24;
      state.y-=dt*12;
      state.vx=24;
      state.vy=-12;
    }else if(t<8){
      state.x+=dt*15;
      state.y+=dt*9;
      state.vx=15;
      state.vy=9;
    }else{
      state.mode="ORBIT";
      state.vx=0;
      state.vy=0;
      state.altitude=420;
      completeObjective(0);
      log("Orbital insertion complete. Manual flight controls enabled.","good");
      setMessage("Orbital insertion complete. Manual controls are now enabled. Head to Alpha Joint.");
    }
    return;
  }

  const rotateSpeed=2.3;
  if(keys.has("a")||keys.has("arrowleft"))state.angle-=rotateSpeed*dt;
  if(keys.has("d")||keys.has("arrowright"))state.angle+=rotateSpeed*dt;

  let ax=0,ay=0;
  const thrust=keys.has("w")||keys.has("arrowup");
  const reverse=keys.has("s")||keys.has("arrowdown");
  const strafeLeft=keys.has("q");
  const strafeRight=keys.has("e");
  const braking=keys.has(" ");

  if(thrust&&state.fuel>0){
    ax+=Math.cos(state.angle)*95;
    ay+=Math.sin(state.angle)*95;
    state.fuel=Math.max(0,state.fuel-dt*1.4);
    state.thrusting=true;
  }
  if(reverse&&state.fuel>0){
    ax-=Math.cos(state.angle)*48;
    ay-=Math.sin(state.angle)*48;
    state.fuel=Math.max(0,state.fuel-dt*.9);
    state.thrusting=true;
  }
  if(strafeLeft&&state.fuel>0){
    ax+=Math.cos(state.angle-Math.PI/2)*55;
    ay+=Math.sin(state.angle-Math.PI/2)*55;
    state.fuel=Math.max(0,state.fuel-dt*.8);
    state.thrusting=true;
  }
  if(strafeRight&&state.fuel>0){
    ax+=Math.cos(state.angle+Math.PI/2)*55;
    ay+=Math.sin(state.angle+Math.PI/2)*55;
    state.fuel=Math.max(0,state.fuel-dt*.8);
    state.thrusting=true;
  }
  if(braking){
    const speed=Math.hypot(state.vx,state.vy);
    if(speed>.05){
      const amount=Math.min(1,dt*2.4);
      state.vx*=1-amount;
      state.vy*=1-amount;
      state.fuel=Math.max(0,state.fuel-dt*.45);
    }
  }
  if(state.fuel<=0&&(thrust||reverse||strafeLeft||strafeRight)){
    state.message="Propellant depleted. Use your remaining drift carefully.";
  }

  state.vx+=ax*dt;
  state.vy+=ay*dt;

  const maxSpeed=115;
  const speed=Math.hypot(state.vx,state.vy);
  if(speed>maxSpeed){
    state.vx=state.vx/speed*maxSpeed;
    state.vy=state.vy/speed*maxSpeed;
  }

  state.x+=state.vx*dt;
  state.y+=state.vy*dt;

  const bounds=600;
  if(state.x>bounds){state.x=bounds;state.vx*=-.35;state.hull=Math.max(0,state.hull-2)}
  if(state.x<-bounds){state.x=-bounds;state.vx*=-.35;state.hull=Math.max(0,state.hull-2)}
  if(state.y>bounds){state.y=bounds;state.vy*=-.35;state.hull=Math.max(0,state.hull-2)}
  if(state.y<-bounds){state.y=-bounds;state.vy*=-.35;state.hull=Math.max(0,state.hull-2)}

  state.altitude=Math.max(100,420+state.y*.04);
  if(state.hull<=0){
    state.running=false;
    state.mode="DISABLED";
    log("Hull integrity critical. Flight controls disabled. Reset to try again.","bad");
    setMessage("Spacecraft disabled. Reset the simulation to begin a new attempt.");
    document.getElementById("connection").textContent="CRAFT DISABLED";
  }
}

function drawBackground(time){
  const w=canvas.width,h=canvas.height;
  const grad=ctx.createRadialGradient(w*.48,h*.46,20,w*.48,h*.46,w*.8);
  grad.addColorStop(0,"#101e3b");
  grad.addColorStop(.55,"#070e20");
  grad.addColorStop(1,"#02040c");
  ctx.fillStyle=grad;ctx.fillRect(0,0,w,h);

  for(const s of stars){
    const twinkle=.7+.3*Math.sin(time*.001+s.p);
    ctx.globalAlpha=s.a*twinkle;
    ctx.fillStyle="#d9eeff";
    ctx.fillRect(s.x,s.y,s.r,s.r);
  }
  ctx.globalAlpha=1;

  ctx.save();
  ctx.translate(w*.78,h*.73);
  const earth=ctx.createRadialGradient(-30,-35,5,0,0,170);
  earth.addColorStop(0,"#3b94bf");
  earth.addColorStop(.55,"#15517c");
  earth.addColorStop(1,"#06142d");
  ctx.fillStyle=earth;
  ctx.beginPath();ctx.arc(0,0,170,0,Math.PI*2);ctx.fill();
  ctx.strokeStyle="#65d8ff33";ctx.lineWidth=3;
  ctx.beginPath();ctx.ellipse(0,0,185,48,-.4,0,Math.PI*2);ctx.stroke();
  ctx.fillStyle="#7ed8c7";
  ctx.beginPath();ctx.ellipse(-40,-48,48,17,-.5,0,Math.PI*2);ctx.fill();
  ctx.beginPath();ctx.ellipse(45,24,65,21,.3,0,Math.PI*2);ctx.fill();
  ctx.fillStyle="#d4f5ff22";
  ctx.beginPath();ctx.arc(-20,-10,155,3.4,5.5);ctx.fill();
  ctx.restore();
}

function worldToScreen(x,y){
  const scale=canvas.width/1050;
  return {x:canvas.width*.48+(x-state.x)*scale,y:canvas.height*.5+(y-state.y)*scale};
}

function drawStation(time){
  const p=worldToScreen(0,0);
  ctx.save();
  ctx.translate(p.x,p.y);
  ctx.globalAlpha=.95;
  ctx.strokeStyle="#8da7c9";
  ctx.lineWidth=8;
  ctx.beginPath();ctx.moveTo(-125,0);ctx.lineTo(125,0);ctx.stroke();
  ctx.lineWidth=3;ctx.strokeStyle="#c0d6ec";
  ctx.beginPath();ctx.moveTo(-170,0);ctx.lineTo(170,0);ctx.stroke();

  drawModule(-100,-12,52,42,"#405e80");
  drawModule(0,-12,55,48,"#334c70");
  drawModule(104,-12,49,42,"#4b5f7b");
  drawModule(0,66,45,38,"#374f71");
  drawModule(0,-86,45,38,"#374f71");

  ctx.fillStyle="#253e5c";
  ctx.fillRect(-230,-22,45,44);
  ctx.fillRect(185,-22,45,44);
  ctx.strokeStyle="#b5d8ff";ctx.lineWidth=2;
  ctx.strokeRect(-230,-22,45,44);ctx.strokeRect(185,-22,45,44);

  ctx.fillStyle="#1d6f9e";
  for(let i=0;i<4;i++){
    ctx.fillRect(-215+i*9,-15,6,30);
    ctx.fillRect(194+i*8,-15,5,30);
  }

  ctx.strokeStyle="#70edb8";ctx.lineWidth=3;
  ctx.beginPath();ctx.arc(235,-100,24,0,Math.PI*2);ctx.stroke();
  ctx.fillStyle="#4df0b5";
  ctx.beginPath();ctx.arc(235,-100,7,0,Math.PI*2);ctx.fill();
  ctx.globalAlpha=1;
  ctx.restore();

  function drawModule(x,y,w,h,color){
    ctx.fillStyle=color;ctx.strokeStyle="#aec9e8";ctx.lineWidth=2;
    ctx.beginPath();ctx.roundRect(x-w/2,y-h/2,w,h,8);ctx.fill();ctx.stroke();
    ctx.fillStyle="#80c5e7";
    for(let i=0;i<3;i++)ctx.fillRect(x-w/2+8+i*11,y-5,6,10);
    ctx.strokeStyle="#b6e4ff";
    ctx.beginPath();ctx.moveTo(x-w/2+5,y-h/2+7);ctx.lineTo(x+w/2-5,y-h/2+7);ctx.stroke();
  }
}

function drawObjectives(){
  missions.forEach((m,i)=>{
    if(state.scanned[i])return;
    const p=worldToScreen(m.x,m.y);
    if(p.x<-50||p.x>canvas.width+50||p.y<-50||p.y>canvas.height+50)return;
    const isDock=i===missions.length-1;
    const color=isDock?"#70ffc0":"#4be9ff";
    const pulse=1+Math.sin(performance.now()*.004+i)*.15;
    ctx.save();
    ctx.strokeStyle=color;ctx.fillStyle=color;
    ctx.globalAlpha=.8;
    ctx.lineWidth=2;
    ctx.beginPath();ctx.arc(p.x,p.y,13*pulse,0,Math.PI*2);ctx.stroke();
    ctx.beginPath();ctx.arc(p.x,p.y,3,0,Math.PI*2);ctx.fill();
    ctx.font="11px Segoe UI,Arial";
    ctx.fillText(m.name,p.x+18,p.y-10);
    ctx.restore();
  });
}

function drawShip(time){
  const x=canvas.width*.48,y=canvas.height*.5;
  ctx.save();
  ctx.translate(x,y);
  ctx.rotate(state.angle);
  if(state.thrusting&&state.running&&!state.paused){
    ctx.fillStyle="#ffbb69";
    ctx.beginPath();ctx.moveTo(-15,-5);ctx.lineTo(-34,0);ctx.lineTo(-15,5);ctx.closePath();ctx.fill();
    ctx.fillStyle="#53e7ff";
    ctx.beginPath();ctx.moveTo(-15,-3);ctx.lineTo(-26,0);ctx.lineTo(-15,3);ctx.closePath();ctx.fill();
  }
  ctx.fillStyle="#d7e7f6";
  ctx.strokeStyle="#65e6ff";ctx.lineWidth=2;
  ctx.beginPath();ctx.moveTo(19,0);ctx.lineTo(-12,-11);ctx.lineTo(-8,0);ctx.lineTo(-12,11);ctx.closePath();
  ctx.fill();ctx.stroke();
  ctx.fillStyle="#3985b7";
  ctx.beginPath();ctx.arc(1,0,4,0,Math.PI*2);ctx.fill();
  ctx.strokeStyle="#b6d4ee";ctx.lineWidth=1.5;
  ctx.beginPath();ctx.moveTo(-3,-7);ctx.lineTo(-9,-15);ctx.moveTo(-3,7);ctx.lineTo(-9,15);ctx.stroke();
  ctx.restore();

  ctx.save();
  ctx.strokeStyle="#6deeff66";ctx.setLineDash([4,5]);
  ctx.beginPath();ctx.arc(x,y,29,0,Math.PI*2);ctx.stroke();
  ctx.restore();
}

function drawRadar(){
  const w=radar.width,h=radar.height;
  rctx.fillStyle="#050b17";rctx.fillRect(0,0,w,h);
  rctx.strokeStyle="#243a58";rctx.lineWidth=1;
  for(let i=1;i<4;i++){
    rctx.beginPath();rctx.moveTo(w*i/4,0);rctx.lineTo(w*i/4,h);rctx.stroke();
    rctx.beginPath();rctx.moveTo(0,h*i/4);rctx.lineTo(w,h*i/4);rctx.stroke();
  }
  rctx.strokeStyle="#2e4d71";
  rctx.beginPath();rctx.arc(w/2,h/2,42,0,Math.PI*2);rctx.stroke();
  const range=650;
  missions.forEach((m,i)=>{
    if(state.scanned[i])return;
    const dx=m.x-state.x,dy=m.y-state.y;
    const px=w/2+dx/range*w*.45,py=h/2+dy/range*h*.45;
    if(px<3||px>w-3||py<3||py>h-3)return;
    rctx.fillStyle=i===missions.length-1?"#6bffc1":"#50e8ff";
    rctx.beginPath();rctx.arc(px,py,3,0,Math.PI*2);rctx.fill();
  });
  rctx.save();rctx.translate(w/2,h/2);rctx.rotate(state.angle);
  rctx.fillStyle="#a6caff";rctx.beginPath();rctx.moveTo(9,0);rctx.lineTo(-6,-5);rctx.lineTo(-4,0);rctx.lineTo(-6,5);rctx.closePath();rctx.fill();
  rctx.restore();
}

function updateObjectives(){
  const el=document.getElementById("objectives");
  el.innerHTML="";
  let done=0;
  missions.forEach((m,i)=>{
    if(state.scanned[i])done++;
    const item=document.createElement("div");
    item.className="objective"+(state.scanned[i]?" done":"");
    const check=document.createElement("div");
    check.className="obj-check";check.textContent=state.scanned[i]?"✓":String(i+1).padStart(2,"0");
    const text=document.createElement("div");
    const title=document.createElement("div");title.className="obj-title";title.textContent=m.name;
    const desc=document.createElement("div");desc.className="obj-desc";desc.textContent=state.scanned[i]?"Completed · +"+m.score+" points":m.desc;
    text.append(title,desc);item.append(check,text);el.appendChild(item);
  });
  const pct=Math.round(done/missions.length*100);
  document.getElementById("objectiveCount").textContent=done+" / "+missions.length;
  document.getElementById("progressText").textContent=pct+"%";
  document.getElementById("progressBar").style.width=pct+"%";
}

function setBar(id,value){
  const el=document.getElementById(id);
  el.style.width=Math.max(0,Math.min(100,value))+"%";
  el.className="fill"+(value<20?" red":value<50?" orange":" green");
}

function updateUI(){
  const speed=Math.hypot(state.vx,state.vy);
  const nearest=getNearest();
  document.getElementById("flightMode").textContent=state.mode;
  document.getElementById("hudSpeed").textContent=speed.toFixed(1)+" m/s";
  document.getElementById("hudAlt").textContent=state.altitude.toFixed(1)+" km";
  document.getElementById("hudRange").textContent=nearest.index<0?"COMPLETE":nearest.distance.toFixed(0)+" km";
  document.getElementById("fuelText").innerHTML=state.fuel.toFixed(0)+' <span class="unit">%</span>';
  document.getElementById("batteryText").innerHTML=state.battery.toFixed(0)+' <span class="unit">%</span>';
  document.getElementById("hullText").innerHTML=state.hull.toFixed(0)+' <span class="unit">%</span>';
  document.getElementById("scoreText").innerHTML=String(state.score).padStart(4,"0")+' <span class="unit">PTS</span>';
  setBar("fuelBar",state.fuel);setBar("batteryBar",state.battery);setBar("hullBar",state.hull);
  document.getElementById("scoreBar").style.width=Math.min(100,state.score/15)+"%";
  document.getElementById("stateText").textContent=state.mode;
  document.getElementById("posX").textContent=state.x.toFixed(1)+" km";
  document.getElementById("posY").textContent=state.y.toFixed(1)+" km";
  document.getElementById("speedValue").textContent=speed.toFixed(1)+" m/s";
  document.getElementById("targetText").textContent=nearest.index<0?"All complete":missions[nearest.index].name;
  const target=nearest.index>=0?missions[nearest.index]:null;
  if(target){
    const targetAngle=Math.atan2(target.y-state.y,target.x-state.x);
    const diff=Math.abs(Math.atan2(Math.sin(state.angle-targetAngle),Math.cos(state.angle-targetAngle)));
    document.getElementById("alignText").textContent=Math.round(diff*180/Math.PI)+"°";
  }else document.getElementById("alignText").textContent="COMPLETE";
  const secs=Math.floor((state.elapsed||0));
  document.getElementById("clock").textContent=String(Math.floor(secs/3600)).padStart(2,"0")+":"+
    String(Math.floor(secs/60)%60).padStart(2,"0")+":"+String(secs%60).padStart(2,"0");
  if(state.thrusting&&state.running&&!state.paused){
    state.thrusting=false;
  }
}

function frame(time){
  const dt=Math.min(.04,Math.max(0,(time-(state.lastFrame||time))/1000));
  state.lastFrame=time;
  updatePhysics(dt);
  drawBackground(time);
  drawStation(time);
  drawObjectives();
  drawShip(time);
  drawRadar();
  updateUI();
  requestAnimationFrame(frame);
}

document.addEventListener("visibilitychange",()=>{
  if(document.hidden&&state.running&&!state.paused){
    state.paused=true;
    state.mode="PAUSED";
    document.getElementById("pauseBtn").textContent="▶ RESUME";
    log("Simulation auto-paused because the tab became inactive.","warn");
  }
});

updateObjectives();
updateUI();
requestAnimationFrame(frame);
</script>
</body>
</html>
"""

@app.get("/")
def home():
    return render_template_string(PAGE)

@app.get("/health")
def health():
    return jsonify({
        "status": "ok",
        "application": "Kibo Junior Astronaut Mission Trainer"
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
```
