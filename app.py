from flask import Flask, Response, jsonify
from datetime import datetime, timezone

app = Flask(__name__)
app.config["JSON_SORT_KEYS"] = False

PAGE = r"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="theme-color" content="#07111f">
<title>KIBO Mission Trainer</title>
<style>
:root {
  color-scheme: dark;
  --bg: #182633;
  --panel: rgba(24, 42, 56, .97);
  --panel-soft: rgba(34, 57, 72, .94);
  --line: rgba(133, 202, 230, .42);
  --cyan: #63e6ff;
  --blue: #368fff;
  --green: #82ffc1;
  --amber: #ffcb72;
  --red: #ff6f83;
  --text: #f4fbff;
  --muted: #91a9bf;
  --shadow: 0 18px 60px rgba(0, 0, 0, .38);
  --radius: 16px;
  --mono: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
  --sans: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
}
* { box-sizing: border-box; }
html { min-height: 100%; background: var(--bg); }
body {
  margin: 0;
  min-height: 100vh;
  color: var(--text);
  font-family: var(--sans);
  background: radial-gradient(ellipse at 50% -10%, #426b83 0%, #243e50 48%, #172a38 100%);
  overflow-x: hidden;
}
button, input { font: inherit; }
button { cursor: pointer; }
button:focus-visible, input:focus-visible { outline: 2px solid var(--cyan); outline-offset: 3px; }
button:disabled { cursor: not-allowed; opacity: .45; }
.app-shell { width: min(1500px, 100%); margin: 0 auto; padding: 18px; }
.topbar { display: flex; align-items: center; justify-content: space-between; gap: 16px; margin-bottom: 16px; }
.brand { display: flex; align-items: center; gap: 12px; min-width: 0; }
.brand-mark { width: 48px; height: 48px; border: 1px solid rgba(99,230,255,.55); border-radius: 14px; display: grid; place-items: center; background: linear-gradient(145deg, #163d59, #091525); box-shadow: 0 0 28px rgba(54,143,255,.16); }
.brand-mark svg { width: 29px; height: 29px; }
.brand-copy { min-width: 0; }
.brand-title { margin: 0; font-size: clamp(17px, 2.4vw, 24px); letter-spacing: .11em; font-weight: 900; }
.brand-subtitle { color: var(--muted); font-size: 11px; letter-spacing: .18em; text-transform: uppercase; margin-top: 4px; }
.top-status { display: flex; align-items: center; gap: 8px; flex-wrap: wrap; justify-content: flex-end; }
.status-pill { display: inline-flex; align-items: center; gap: 7px; border: 1px solid var(--line); border-radius: 999px; padding: 8px 11px; color: #b7d2e6; background: rgba(8,18,31,.7); font-size: 11px; letter-spacing: .06em; white-space: nowrap; }
.status-dot { width: 7px; height: 7px; border-radius: 50%; background: var(--green); box-shadow: 0 0 10px var(--green); }
.layout { display: grid; grid-template-columns: minmax(0, 1fr) 320px; gap: 16px; align-items: start; }
.main-column { min-width: 0; }
.stage-frame { position: relative; overflow: hidden; border: 1px solid rgba(99,230,255,.3); border-radius: 20px; background: #b7c9d2; box-shadow: var(--shadow); min-height: 520px; }
#gameCanvas { display: block; width: 100%; height: min(70vh, 720px); min-height: 520px; outline: none; image-rendering: auto; touch-action: none; }
.stage-vignette { pointer-events: none; position: absolute; inset: 0; background: radial-gradient(ellipse at center, transparent 72%, rgba(16,35,48,.10) 100%); }
.stage-topline { position: absolute; top: 15px; left: 16px; right: 16px; display: flex; align-items: flex-start; justify-content: space-between; gap: 12px; pointer-events: none; }
.stage-label { padding: 10px 12px; background: rgba(4,13,23,.8); border: 1px solid rgba(99,230,255,.25); border-radius: 11px; backdrop-filter: blur(12px); }
.eyebrow { color: var(--cyan); font-size: 9px; font-weight: 800; letter-spacing: .19em; text-transform: uppercase; }
.stage-location { margin-top: 4px; font-weight: 800; font-size: 13px; }
.stage-coordinates { margin-top: 4px; font-family: var(--mono); color: var(--muted); font-size: 10px; }
.stage-alert { max-width: 250px; text-align: right; color: var(--amber); font-size: 10px; line-height: 1.45; text-shadow: 0 2px 8px #000; }
.center-overlay { position: absolute; inset: 0; display: flex; align-items: center; justify-content: center; padding: 20px; background: rgba(20,38,50,.26); backdrop-filter: blur(3px); z-index: 5; }
.launch-card { width: min(560px, 100%); padding: clamp(22px, 4vw, 42px); text-align: center; border: 1px solid rgba(99,230,255,.42); border-radius: 22px; background: linear-gradient(150deg, rgba(12,32,52,.98), rgba(4,12,23,.98)); box-shadow: 0 25px 100px rgba(0,0,0,.55), 0 0 55px rgba(54,143,255,.12); }
.launch-symbol { width: 78px; height: 78px; margin: 0 auto 20px; border: 1px solid rgba(99,230,255,.6); border-radius: 50%; display: grid; place-items: center; color: var(--cyan); box-shadow: 0 0 38px rgba(99,230,255,.12), inset 0 0 22px rgba(99,230,255,.08); }
.launch-symbol svg { width: 48px; height: 48px; }
.launch-title { font-size: clamp(25px, 4.2vw, 42px); letter-spacing: .06em; line-height: 1.05; font-weight: 950; margin: 0; }
.launch-title span { color: var(--cyan); }
.launch-description { color: #a9bfd2; line-height: 1.65; max-width: 440px; margin: 16px auto 22px; font-size: 13px; }
.launch-note { padding: 12px; margin: 0 0 20px; border-radius: 10px; background: rgba(255,203,114,.08); border: 1px solid rgba(255,203,114,.2); color: #e8cb99; font-size: 11px; line-height: 1.5; text-align: left; }
.primary-button { border: 0; border-radius: 11px; padding: 13px 20px; min-height: 46px; color: #03111b; font-weight: 900; letter-spacing: .07em; text-transform: uppercase; background: linear-gradient(105deg, #7af0ff, #64b7ff); box-shadow: 0 8px 24px rgba(54,143,255,.2); transition: transform .16s ease, filter .16s ease; }
.primary-button:hover { transform: translateY(-2px); filter: brightness(1.08); }
.primary-button:active { transform: translateY(0); }
.secondary-button { border: 1px solid var(--line); border-radius: 10px; padding: 10px 13px; color: #c9e3f5; background: rgba(10,25,41,.8); transition: border-color .15s ease, background .15s ease; }
.secondary-button:hover { border-color: rgba(99,230,255,.7); background: rgba(18,43,64,.9); }
.launch-button { width: 100%; font-size: 12px; }
.launch-foot { color: #708ca4; margin-top: 14px; font-size: 10px; letter-spacing: .07em; }
.launch-count { font-family: var(--mono); color: var(--cyan); font-size: 54px; font-weight: 900; margin: 18px 0; text-shadow: 0 0 30px rgba(99,230,255,.35); }
.launch-progress { height: 5px; background: #122a3c; border-radius: 20px; overflow: hidden; margin-top: 20px; }
.launch-progress-fill { width: 0%; height: 100%; background: linear-gradient(90deg, var(--blue), var(--cyan)); transition: width .12s linear; }
.hud-bottom { position: absolute; bottom: 14px; left: 14px; right: 14px; display: flex; align-items: end; justify-content: space-between; gap: 10px; pointer-events: none; }
.hud-readout { padding: 10px 12px; border: 1px solid rgba(99,230,255,.2); border-radius: 10px; background: rgba(4,13,23,.78); backdrop-filter: blur(10px); min-width: 110px; }
.readout-label { font-size: 9px; color: var(--muted); letter-spacing: .13em; text-transform: uppercase; }
.readout-value { margin-top: 5px; font-family: var(--mono); font-weight: 800; font-size: 15px; }
.hud-readouts { display: flex; gap: 8px; }
.scan-indicator { color: var(--green); font-size: 10px; letter-spacing: .13em; text-transform: uppercase; padding: 9px 11px; border-radius: 9px; background: rgba(2,16,13,.8); border: 1px solid rgba(130,255,193,.28); }
.control-strip { display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 10px; margin-top: 12px; padding: 12px 14px; border: 1px solid var(--line); border-radius: 13px; background: rgba(8,19,32,.76); }
.control-group { display: flex; align-items: center; flex-wrap: wrap; gap: 7px; }
.keycap { display: inline-grid; place-items: center; min-width: 25px; height: 25px; padding: 0 6px; color: #d8f3ff; font-family: var(--mono); font-size: 10px; border: 1px solid #36536a; border-bottom-width: 3px; border-radius: 6px; background: linear-gradient(#142b40, #0a1727); }
.control-label { color: var(--muted); font-size: 10px; }
.side-column { display: flex; flex-direction: column; gap: 12px; min-width: 0; }
.panel { overflow: hidden; border: 1px solid var(--line); border-radius: var(--radius); background: var(--panel); box-shadow: 0 8px 28px rgba(0,0,0,.16); }
.panel-header { display: flex; align-items: center; justify-content: space-between; gap: 10px; padding: 15px 16px; border-bottom: 1px solid rgba(103,188,224,.14); }
.panel-title { margin: 0; font-size: 11px; letter-spacing: .14em; text-transform: uppercase; font-weight: 900; }
.panel-kicker { color: var(--muted); font-size: 9px; letter-spacing: .12em; text-transform: uppercase; }
.panel-body { padding: 14px 16px; }
.mission-progress { height: 5px; overflow: hidden; border-radius: 99px; background: #172b3c; margin: 8px 0 14px; }
.mission-progress-fill { width: 0; height: 100%; background: linear-gradient(90deg, #398fff, #72f4ff); transition: width .25s ease; }
.objective-list { display: flex; flex-direction: column; gap: 8px; }
.objective-item { display: grid; grid-template-columns: 27px minmax(0,1fr) auto; align-items: center; gap: 9px; padding: 10px; border: 1px solid rgba(103,188,224,.12); border-radius: 10px; background: rgba(14,31,48,.58); transition: border-color .18s ease, background .18s ease; }
.objective-item.active { border-color: rgba(99,230,255,.55); background: rgba(22,56,76,.6); }
.objective-item.complete { border-color: rgba(130,255,193,.24); background: rgba(19,55,46,.3); }
.objective-icon { display: grid; place-items: center; width: 27px; height: 27px; border-radius: 8px; color: #9eb9cf; background: #172d41; font-size: 11px; font-weight: 900; }
.objective-item.active .objective-icon { color: #03131d; background: var(--cyan); }
.objective-item.complete .objective-icon { color: #06251a; background: var(--green); }
.objective-name { font-size: 11px; line-height: 1.35; font-weight: 800; }
.objective-hint { color: var(--muted); margin-top: 4px; font-size: 9px; line-height: 1.4; }
.objective-state { color: var(--muted); font-size: 8px; text-transform: uppercase; letter-spacing: .08em; white-space: nowrap; }
.objective-item.complete .objective-state { color: var(--green); }
.objective-item.active .objective-state { color: var(--cyan); }
.stat-grid { display: grid; grid-template-columns: repeat(2, minmax(0,1fr)); gap: 8px; }
.stat-card { padding: 11px; border-radius: 10px; background: rgba(18,38,57,.72); border: 1px solid rgba(103,188,224,.12); }
.stat-label { color: var(--muted); font-size: 9px; text-transform: uppercase; letter-spacing: .11em; }
.stat-value { margin-top: 6px; font-family: var(--mono); font-size: 19px; font-weight: 900; }
.stat-unit { color: #7694aa; font-size: 9px; margin-left: 4px; }
.telemetry-row { display: flex; align-items: center; justify-content: space-between; gap: 10px; padding: 9px 0; border-bottom: 1px solid rgba(103,188,224,.1); font-size: 10px; }
.telemetry-row:last-child { border-bottom: 0; }
.telemetry-key { color: var(--muted); }
.telemetry-value { font-family: var(--mono); color: #dff7ff; text-align: right; }
.battery-track { width: 76px; height: 7px; border: 1px solid #33566a; padding: 1px; border-radius: 4px; margin-left: auto; }
.battery-fill { width: 100%; height: 100%; border-radius: 2px; background: var(--green); transition: width .2s ease; }
.battery-wrap { display: flex; align-items: center; gap: 8px; }
.mission-log { display: flex; flex-direction: column; gap: 8px; max-height: 190px; overflow-y: auto; padding-right: 3px; }
.log-entry { display: grid; grid-template-columns: 52px minmax(0,1fr); gap: 8px; font-size: 10px; line-height: 1.5; }
.log-time { color: #6489a4; font-family: var(--mono); }
.log-message { color: #bfd3e2; }
.log-entry.success .log-message { color: var(--green); }
.log-entry.warning .log-message { color: var(--amber); }
.log-entry.alert .log-message { color: var(--red); }
.route-preview { width: 100%; height: 120px; display: block; border-radius: 10px; background: #071421; border: 1px solid rgba(103,188,224,.16); }
.route-legend { display: flex; flex-wrap: wrap; gap: 12px; margin-top: 9px; }
.legend-item { display: flex; align-items: center; gap: 5px; color: var(--muted); font-size: 9px; }
.legend-dot { width: 7px; height: 7px; border-radius: 50%; }
.panel-actions { display: flex; flex-wrap: wrap; gap: 7px; }
.panel-actions button { flex: 1; min-width: 88px; font-size: 10px; }
.footer-note { color: #607b91; text-align: center; font-size: 10px; line-height: 1.6; padding: 18px 10px 4px; }
.modal-backdrop { position: fixed; inset: 0; display: none; align-items: center; justify-content: center; padding: 18px; background: rgba(1,5,10,.78); backdrop-filter: blur(8px); z-index: 20; }
.modal-backdrop.visible { display: flex; }
.modal-card { width: min(560px,100%); max-height: min(85vh,760px); overflow-y: auto; border: 1px solid rgba(99,230,255,.35); border-radius: 18px; background: #091725; box-shadow: 0 25px 90px #000; }
.modal-heading { padding: 18px 20px; border-bottom: 1px solid var(--line); display: flex; justify-content: space-between; align-items: center; gap: 12px; }
.modal-heading h2 { margin: 0; font-size: 14px; letter-spacing: .12em; text-transform: uppercase; }
.modal-content { padding: 20px; color: #bdd0df; font-size: 12px; line-height: 1.7; }
.modal-content h3 { color: var(--cyan); font-size: 11px; letter-spacing: .1em; text-transform: uppercase; margin: 18px 0 6px; }
.modal-content h3:first-child { margin-top: 0; }
.modal-content ul { padding-left: 20px; }
.modal-content li { margin: 5px 0; }
.modal-footer { padding: 0 20px 20px; display: flex; justify-content: flex-end; gap: 8px; }
.result-score { font-size: 48px; color: var(--cyan); font-weight: 950; font-family: var(--mono); text-align: center; margin: 10px 0; }
.result-caption { text-align: center; color: var(--muted); font-size: 10px; letter-spacing: .15em; text-transform: uppercase; }
.result-grid { display: grid; grid-template-columns: repeat(2,minmax(0,1fr)); gap: 8px; margin-top: 20px; }
.result-item { padding: 12px; border: 1px solid var(--line); border-radius: 10px; background: rgba(15,33,52,.7); }
.result-item span { display: block; color: var(--muted); font-size: 9px; text-transform: uppercase; letter-spacing: .1em; }
.result-item strong { display: block; margin-top: 7px; font-family: var(--mono); font-size: 17px; }
.toast-stack { position: fixed; right: 18px; bottom: 18px; display: flex; flex-direction: column; align-items: flex-end; gap: 8px; z-index: 30; pointer-events: none; }
.toast { max-width: min(360px,calc(100vw - 36px)); padding: 12px 15px; border: 1px solid rgba(99,230,255,.4); border-radius: 11px; background: rgba(7,20,33,.97); box-shadow: 0 10px 35px #0008; color: #dff8ff; font-size: 11px; line-height: 1.5; animation: toast-in .22s ease-out; }
.toast.success { border-color: rgba(130,255,193,.45); }
.toast.warning { border-color: rgba(255,203,114,.45); }
@keyframes toast-in { from { transform: translateY(8px); opacity: 0; } to { transform: translateY(0); opacity: 1; } }
@keyframes pulse { 0%,100% { opacity: .5; } 50% { opacity: 1; } }
@keyframes orbit { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }
@keyframes scanline { 0% { transform: translateY(-100%); } 100% { transform: translateY(700%); } }
.mobile-controls { display: none; grid-template-columns: repeat(3,54px); grid-template-rows: repeat(2,48px); gap: 5px; justify-content: center; padding: 10px; }
.mobile-controls button { border: 1px solid #34536a; border-radius: 10px; color: #dff8ff; background: rgba(13,34,52,.92); font-weight: 900; touch-action: none; user-select: none; }
.mobile-controls .empty { visibility: hidden; }
.mobile-actions { display: none; grid-template-columns: repeat(2,minmax(0,1fr)); gap: 7px; padding: 0 12px 12px; }
.mobile-actions button { min-height: 43px; }
.help-tip { color: #91a9bf; font-size: 10px; line-height: 1.55; margin-top: 10px; }
.meter { height: 4px; border-radius: 99px; background: #1a3347; overflow: hidden; }
.meter-fill { height: 100%; width: 50%; background: var(--cyan); transition: width .2s ease; }
.target-banner { display: none; margin-top: 12px; padding: 12px 14px; border: 1px solid rgba(99,230,255,.34); border-radius: 12px; background: rgba(13,39,56,.85); }
.target-banner.visible { display: flex; align-items: center; justify-content: space-between; gap: 10px; }
.target-banner strong { display: block; font-size: 11px; }
.target-banner span { display: block; margin-top: 4px; color: var(--muted); font-size: 10px; }
.target-banner button { white-space: nowrap; }
button:active { filter: brightness(.93); }
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: #091523; }
::-webkit-scrollbar-thumb { background: #24465e; border-radius: 9px; }
@media (max-width: 1080px) {
  .layout { grid-template-columns: minmax(0,1fr) 290px; }
  .app-shell { padding: 12px; }
  .stage-frame { min-height: 480px; }
  #gameCanvas { min-height: 480px; }
}
@media (max-width: 820px) {
  .layout { grid-template-columns: 1fr; }
  .side-column { display: grid; grid-template-columns: repeat(2,minmax(0,1fr)); align-items: start; }
  .side-column .panel:first-child { grid-column: 1 / -1; }
  .stage-frame { min-height: 430px; }
  #gameCanvas { height: 58vh; min-height: 430px; }
  .mobile-controls { display: grid; }
  .mobile-actions { display: grid; }
  .control-strip { display: none; }
}
@media (max-width: 560px) {
  .app-shell { padding: 9px; }
  .topbar { align-items: flex-start; }
  .brand-mark { width: 40px; height: 40px; }
  .brand-subtitle { font-size: 8px; letter-spacing: .12em; }
  .top-status .status-pill:nth-child(2) { display: none; }
  .status-pill { font-size: 9px; padding: 7px 8px; }
  .stage-frame { min-height: 410px; border-radius: 15px; }
  #gameCanvas { min-height: 410px; height: 55vh; }
  .stage-topline { top: 9px; left: 9px; right: 9px; }
  .stage-label { padding: 8px 9px; }
  .stage-location { font-size: 11px; }
  .stage-alert { max-width: 135px; font-size: 9px; }
  .hud-bottom { bottom: 9px; left: 9px; right: 9px; }
  .hud-readout { min-width: 0; padding: 8px; }
  .readout-value { font-size: 12px; }
  .hud-readouts { gap: 5px; }
  .scan-indicator { font-size: 8px; padding: 8px; }
  .side-column { grid-template-columns: 1fr; }
  .side-column .panel:first-child { grid-column: auto; }
  .panel-header { padding: 13px; }
  .panel-body { padding: 12px; }
  .launch-card { padding: 22px 18px; }
  .launch-description { font-size: 12px; }
  .launch-symbol { width: 62px; height: 62px; margin-bottom: 16px; }
  .launch-symbol svg { width: 38px; height: 38px; }
}

.instrument-shell { position: relative; isolation: isolate; }
.instrument-shell::before { content: ""; position: absolute; inset: 0; pointer-events: none; border: 1px solid rgba(99,230,255,.08); border-radius: inherit; }
.instrument-shell::after { content: ""; position: absolute; inset: 0; pointer-events: none; background: repeating-linear-gradient(0deg, transparent 0 5px, rgba(99,230,255,.012) 6px); }
.panel[data-state="warning"] { border-color: rgba(255,203,114,.4); }
.panel[data-state="critical"] { border-color: rgba(255,111,131,.55); }
.panel[data-state="complete"] { border-color: rgba(130,255,193,.4); }
.status-pill[data-tone="cyan"] { color: var(--cyan); }
.status-pill[data-tone="green"] { color: var(--green); }
.status-pill[data-tone="amber"] { color: var(--amber); }
.status-pill[data-tone="red"] { color: var(--red); }
.objective-item:focus-within { outline: 1px solid var(--cyan); outline-offset: 2px; }
.objective-name { overflow-wrap: anywhere; }
.objective-hint { overflow-wrap: anywhere; }
.objective-item[data-distance="near"] { box-shadow: inset 2px 0 var(--amber); }
.objective-item[data-distance="far"] { box-shadow: inset 2px 0 rgba(103,188,224,.16); }
.objective-item[data-distance="complete"] { box-shadow: inset 2px 0 var(--green); }
.telemetry-value[data-quality="excellent"] { color: var(--green); }
.telemetry-value[data-quality="good"] { color: var(--cyan); }
.telemetry-value[data-quality="adjust"] { color: var(--amber); }
.telemetry-value[data-quality="poor"] { color: var(--red); }
.stat-card[data-level="high"] { border-color: rgba(130,255,193,.3); }
.stat-card[data-level="medium"] { border-color: rgba(255,203,114,.3); }
.stat-card[data-level="low"] { border-color: rgba(255,111,131,.35); }
.readout-value { font-variant-numeric: tabular-nums; }
.telemetry-value { font-variant-numeric: tabular-nums; }
.result-item strong { font-variant-numeric: tabular-nums; }
.route-preview { image-rendering: auto; }
.route-preview:focus-visible { outline: 2px solid var(--cyan); outline-offset: 2px; }
.modal-content p { margin: 8px 0 12px; }
.modal-content strong { color: #e9f9ff; }
.modal-content code { color: var(--cyan); font-family: var(--mono); }
.modal-content .callout { padding: 11px 13px; border: 1px solid var(--line); border-radius: 9px; background: rgba(14,33,50,.7); }
.modal-card[data-tone="success"] { border-color: rgba(130,255,193,.5); }
.modal-card[data-tone="warning"] { border-color: rgba(255,203,114,.5); }
.modal-card[data-tone="danger"] { border-color: rgba(255,111,131,.5); }
.primary-button:focus-visible { outline-color: #baf7ff; }
.secondary-button:focus-visible { outline-color: var(--cyan); }
.keycap { user-select: none; }
.control-group { min-height: 26px; }
.control-strip { backdrop-filter: blur(12px); }
.footer-note a { color: var(--cyan); }
.footer-note strong { color: #bdd9e9; }
.toast { overflow-wrap: anywhere; }
.toast.success { color: #d9ffed; }
.toast.warning { color: #ffe8c0; }
.toast.error { border-color: rgba(255,111,131,.6); color: #ffdce1; }
.toast.info { border-color: rgba(99,230,255,.45); }
.battery-track { flex-shrink: 0; }
.battery-fill { min-width: 0; }
.stage-label { max-width: min(340px, 65%); }
.stage-location { overflow-wrap: anywhere; }
.stage-coordinates { font-variant-numeric: tabular-nums; }
.stage-alert { white-space: pre-line; }
.hud-bottom { z-index: 2; }
.stage-topline { z-index: 2; }
.stage-vignette { z-index: 1; }
#gameCanvas { position: relative; z-index: 0; }
#gameCanvas:focus-visible { outline: 2px solid rgba(99,230,255,.5); outline-offset: -5px; }
#launchOverlay { z-index: 6; }
#launchOverlay[hidden] { display: none; }
.launch-card { position: relative; overflow: hidden; }
.launch-card::before { content: ""; position: absolute; width: 260px; height: 260px; top: -180px; right: -100px; border: 1px solid rgba(99,230,255,.12); border-radius: 50%; pointer-events: none; }
.launch-card::after { content: ""; position: absolute; width: 170px; height: 170px; top: -135px; right: -55px; border: 1px solid rgba(99,230,255,.09); border-radius: 50%; pointer-events: none; }
.launch-note strong { color: #ffdfa8; letter-spacing: .08em; }
.launch-foot { line-height: 1.5; }
.launch-count { font-variant-numeric: tabular-nums; }
.launch-progress-fill { position: relative; }
.launch-progress-fill::after { content: ""; position: absolute; inset: 0; background: linear-gradient(90deg, transparent, rgba(255,255,255,.42), transparent); }
.mission-progress-fill { position: relative; }
.mission-progress-fill::after { content: ""; position: absolute; inset: 0; background: linear-gradient(90deg, transparent, rgba(255,255,255,.2), transparent); }
.panel-header { min-height: 48px; }
.panel-title { line-height: 1.4; }
.panel-kicker { line-height: 1.4; text-align: right; }
.panel-body > :first-child { margin-top: 0; }
.panel-body > :last-child { margin-bottom: 0; }
.objective-list:empty::after { content: "No objectives loaded"; color: var(--muted); font-size: 11px; padding: 12px 0; }
.mission-log:empty::after { content: "No events yet"; color: var(--muted); font-size: 10px; }
.log-entry { align-items: start; }
.log-time { padding-top: 1px; }
.log-message { overflow-wrap: anywhere; }
.route-legend { align-items: center; }
.legend-item { white-space: nowrap; }
.legend-dot { flex-shrink: 0; box-shadow: 0 0 8px currentColor; }
.target-banner { box-shadow: 0 10px 26px rgba(0,0,0,.14); }
.target-banner > div { min-width: 0; }
.target-banner strong { overflow-wrap: anywhere; }
.target-banner span { line-height: 1.5; }
.target-banner button { flex-shrink: 0; }
.mobile-controls button { min-width: 0; }
.mobile-controls button:active { background: #20506c; border-color: var(--cyan); }
.mobile-actions button:active { transform: translateY(1px); }
.modal-backdrop { overscroll-behavior: contain; }
.modal-card { overscroll-behavior: contain; }
.modal-heading { position: sticky; top: 0; z-index: 1; background: #091725; }
.modal-footer { position: sticky; bottom: 0; background: #091725; }
.modal-heading h2 { overflow-wrap: anywhere; }
.result-score { font-variant-numeric: tabular-nums; }
.result-caption { line-height: 1.6; }
.result-grid { align-items: stretch; }
.result-item { min-width: 0; }
.result-item strong { overflow-wrap: anywhere; }
.app-shell { isolation: isolate; }
.topbar { position: relative; z-index: 2; }
.brand-title { line-height: 1.2; }
.brand-subtitle { line-height: 1.5; }
.brand-mark { flex-shrink: 0; }
.top-status { max-width: 48%; }
.status-pill { line-height: 1.4; }
.stage-frame { isolation: isolate; }
.stage-frame::after { content: ""; position: absolute; inset: 0; border-radius: inherit; pointer-events: none; box-shadow: inset 0 0 0 1px rgba(255,255,255,.025); }
.main-column { position: relative; }
.side-column { position: relative; }
.panel { min-width: 0; }
.panel-actions button { line-height: 1.4; }
.help-tip strong { color: #cceeff; }
.eyebrow { line-height: 1.5; }
.primary-button { line-height: 1.35; }
.secondary-button { line-height: 1.35; }
button { -webkit-tap-highlight-color: transparent; }
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after { animation-duration: .01ms !important; animation-iteration-count: 1 !important; scroll-behavior: auto !important; transition-duration: .01ms !important; }
}
@media (min-width: 1200px) {
  .app-shell { padding-left: 22px; padding-right: 22px; }
  .layout { gap: 18px; }
  .side-column { gap: 14px; }
}
@media (max-width: 820px) {
  .top-status { max-width: none; }
  .target-banner.visible { align-items: flex-start; }
  .target-banner button { align-self: center; }
}
@media (max-width: 460px) {
  .top-status { gap: 5px; }
  .top-status .status-pill { letter-spacing: .025em; }
  .brand { gap: 8px; }
  .brand-title { letter-spacing: .04em; }
  .stage-label { max-width: 68%; }
  .stage-alert { max-width: 30%; font-size: 8px; }
  .target-banner.visible { flex-direction: column; }
  .target-banner button { width: 100%; }
  .result-grid { grid-template-columns: 1fr 1fr; }
}


.telemetry-row:hover { background: rgba(99,230,255,.025); }
.objective-item { position: relative; }
.objective-item::after { content: ""; position: absolute; inset: 0; border-radius: inherit; pointer-events: none; opacity: 0; transition: opacity .18s ease; box-shadow: inset 0 0 20px rgba(99,230,255,.04); }
.objective-item.active::after { opacity: 1; }
.objective-icon { flex-shrink: 0; }
.objective-state { align-self: start; padding-top: 3px; }
.stat-grid { align-items: stretch; }
.stat-card { min-width: 0; }
.stat-value { overflow-wrap: anywhere; }
.mission-log { scrollbar-gutter: stable; }
.log-entry:first-child .log-time { color: var(--cyan); }
.log-entry.alert .log-time { color: var(--red); }
.route-preview { max-width: 100%; }
.route-legend { row-gap: 7px; }
.legend-item:nth-child(1) .legend-dot { color: #63e6ff; }
.legend-item:nth-child(2) .legend-dot { color: #ffcb72; }
.legend-item:nth-child(3) .legend-dot { color: #82ffc1; }
.stage-frame canvas { max-width: 100%; }
.stage-label .eyebrow { white-space: nowrap; }
.stage-coordinates { white-space: nowrap; }
.hud-readout { backdrop-filter: blur(8px); }
.scan-indicator { backdrop-filter: blur(8px); }
.scan-indicator::first-letter { text-shadow: 0 0 8px currentColor; }
.launch-symbol { position: relative; }
.launch-symbol::before { content: ""; position: absolute; inset: -8px; border: 1px dashed rgba(99,230,255,.22); border-radius: 50%; animation: orbit 18s linear infinite; }
.launch-symbol::after { content: ""; position: absolute; inset: 7px; border: 1px solid rgba(130,255,193,.12); border-radius: 50%; }
.launch-title { text-wrap: balance; }
.launch-description { text-wrap: pretty; }
.launch-note { text-wrap: pretty; }
.launch-button { position: relative; overflow: hidden; }
.launch-button::after { content: ""; position: absolute; inset: 0; background: linear-gradient(110deg, transparent 20%, rgba(255,255,255,.28) 50%, transparent 80%); transform: translateX(-120%); transition: transform .45s ease; }
.launch-button:hover::after { transform: translateX(120%); }
.panel-actions button { white-space: normal; }
.modal-content { overflow-wrap: anywhere; }
.modal-content ul { margin-bottom: 0; }
.modal-content li::marker { color: var(--cyan); }
.modal-footer .primary-button { min-width: 120px; }
.modal-heading .secondary-button { min-width: 36px; padding: 8px; }
.toast-stack { max-height: 50vh; overflow: hidden; }
.toast { animation-fill-mode: both; }
@media (hover: hover) {
  .panel { transition: border-color .18s ease; }
  .panel:hover { border-color: rgba(103,188,224,.34); }
  .objective-item:hover { border-color: rgba(103,188,224,.3); }
  .secondary-button:hover { transform: translateY(-1px); }
}
@media (max-width: 820px) {
  .side-column .panel { width: 100%; }
  .mobile-controls { user-select: none; }
  .mobile-actions { user-select: none; }
  .mobile-controls button { font-size: 16px; }
  .mobile-actions button { font-size: 11px; }
  .panel-actions { display: grid; grid-template-columns: repeat(2,minmax(0,1fr)); }
  .panel-actions button:last-child { grid-column: 1 / -1; }
}
@media (max-width: 560px) {
  .control-strip { gap: 6px; }
  .control-group { gap: 5px; }
  .panel-actions { grid-template-columns: 1fr 1fr; }
  .panel-actions button { min-width: 0; }
  .modal-content { padding: 16px; }
  .modal-heading { padding: 14px 16px; }
  .modal-footer { padding: 0 16px 16px; }
  .toast-stack { right: 9px; bottom: 9px; }
  .toast { max-width: calc(100vw - 18px); }
}


.autonomous-console { margin-top: 0; margin-bottom: 14px; border-color: rgba(99,230,255,.48); box-shadow: 0 12px 34px rgba(0,0,0,.16); }
.how-to-play { margin: 0 0 16px; padding: 15px 17px; border: 1px solid rgba(99,230,255,.32); border-radius: 12px; background: linear-gradient(135deg, rgba(24,65,88,.9), rgba(14,35,51,.96)); color: #eaf7ff; }
.how-to-play h3 { margin: 0 0 9px; font-size: 15px; color: #8de7ff; }
.how-to-play ol { margin: 0 0 10px; padding-left: 22px; }
.how-to-play li { margin: 6px 0; color: #d5e7f4; font-size: 12px; line-height: 1.55; }
.how-to-play strong { color: #fff; }
.how-to-play p { margin: 10px 0 0; padding-top: 10px; border-top: 1px solid rgba(180,220,245,.18); color: #c5dceb; font-size: 11px; line-height: 1.65; }
.how-to-play code { color: #8de7ff; }
.program-intro { margin: 0 0 12px; color: #d1e2ef; font-size: 12px; line-height: 1.6; }
.program-label { display:block; margin-bottom:7px; color:var(--cyan); font-size:10px; font-weight:900; letter-spacing:.15em; }
#programEditor { display:block; width:100%; min-height:250px; resize:vertical; padding:14px; border:1px solid rgba(99,230,255,.25); border-radius:11px; outline:none; color:#c8f4ff; background:#050d17; font:12px/1.8 var(--mono); tab-size:2; }
#programEditor:focus { border-color:var(--cyan); box-shadow:0 0 0 2px rgba(99,230,255,.08); }
.program-toolbar { display:flex; flex-wrap:wrap; gap:8px; margin-top:10px; }
.program-toolbar .primary-button { flex:1 1 220px; }
.program-status { margin-top:11px; padding:10px 12px; border:1px solid var(--line); border-radius:9px; color:#b6d7e8; background:rgba(5,14,24,.72); font-size:11px; line-height:1.5; }
.command-reference { margin-top:10px; color:#839fb4; font-size:10px; line-height:1.8; }
.command-reference code { color:#8de7ff; white-space:normal; }
body.autonomous-mode .control-strip, body.autonomous-mode .mobile-controls, body.autonomous-mode .mobile-actions { display:none !important; }
@media(max-width:560px) { #programEditor { min-height:210px; font-size:11px; } .program-toolbar button { width:100%; } }

</style>
</head>
<body class="autonomous-mode">
<div class="app-shell">
<header class="topbar">
  <div class="brand">
    <div class="brand-mark" aria-hidden="true">
      <svg viewBox="0 0 40 40" fill="none"><circle cx="20" cy="20" r="15" stroke="#63e6ff" stroke-width="1.6"/><ellipse cx="20" cy="20" rx="7" ry="15" stroke="#63e6ff" stroke-width="1.2"/><path d="M5 20h30M8 12h24M8 28h24" stroke="#63e6ff" stroke-width="1.2"/><circle cx="20" cy="20" r="3" fill="#82ffc1"/></svg>
    </div>
    <div class="brand-copy">
      <h1 class="brand-title">KIBO <span style="color:var(--cyan)">MISSION TRAINER</span></h1>
      <div class="brand-subtitle">7th Kibo-RPC · Int-Ball2 Autonomy Practice</div>
    </div>
  </div>
  <div class="top-status">
    <div class="status-pill"><span class="status-dot"></span> SYSTEM READY</div>
    <div class="status-pill">INT-BALL2 · TRAINING MODE</div>
  </div>
</header>
<main class="layout">
  <section class="main-column">
    <section class="panel autonomous-console" id="autonomousConsole">
      <div class="panel-header"><h2 class="panel-title">Autonomous program editor</h2><span class="panel-kicker" id="programState">NOT RUNNING</span></div>
      <div class="panel-body">
        <div class="how-to-play" aria-label="How to run an autonomous mission">
          <h3>How to run your first autonomous mission</h3>
          <ol>
            <li><strong>Read the mission plan.</strong> The sample program is a browser-based practice script, not the C++/Python ROS package used for official Kibo-RPC submission.</li>
            <li><strong>Start the training run.</strong> Click “Begin launch sequence” on the Kibo scene and wait for the countdown.</li>
            <li><strong>Run autonomously.</strong> Click “Run autonomous mission”. The simulated Int-Ball2 follows the commands; do not steer it with WASD.</li>
            <li><strong>Inspect each result.</strong> Watch the current position, camera alignment, marker scan, checkpoint status, elapsed time, and event log.</li>
            <li><strong>Debug safely.</strong> Stop the run, edit the program, and retry. The sample route can be restored at any time.</li>
          </ol>
          <p><strong>Training commands:</strong> <code>MOVE_TO id</code> navigates to a practice checkpoint; <code>ALIGN</code> points the camera; <code>SCAN</code> attempts marker registration; <code>WAIT 1</code> waits for one second. In the official API workflow, a successful move alone does not prove a checkpoint passed: the robot must be stable and the checkpoint evaluation must succeed.</p>
          <p><strong>Official concepts modeled:</strong> retrieve checkpoint definitions, move to the target pose, align the camera to the AR marker, stabilize, evaluate the checkpoint, log the result, and finish the mission. The real Kibo-RPC interfaces use ROS topics, services, and actions.</p>
        </div>
        <label class="program-label" for="programEditor">MISSION SCRIPT</label>
        <textarea id="programEditor" spellcheck="false" aria-label="Autonomous mission script">MOVE_TO dock
ALIGN
WAIT 1
SCAN
MOVE_TO joint-a
ALIGN
WAIT 1
SCAN
MOVE_TO hatch
ALIGN
WAIT 1
SCAN
MOVE_TO rack
ALIGN
WAIT 1
SCAN
MOVE_TO joint-b
ALIGN
WAIT 1
SCAN
MOVE_TO panel
ALIGN
WAIT 1
SCAN
MOVE_TO sensor-bay
ALIGN
WAIT 1
SCAN
MOVE_TO rack-b
ALIGN
WAIT 1
SCAN
MOVE_TO hatch-b
ALIGN
WAIT 1
SCAN
MOVE_TO goal
ALIGN
WAIT 1
SCAN</textarea>
        <div class="program-toolbar">
          <button class="primary-button" id="runProgramButton">▶ Run autonomous mission</button>
          <button class="secondary-button" id="stopProgramButton">■ Stop</button>
          <button class="secondary-button" id="sampleProgramButton">Restore sample</button>
        </div>
        <div class="program-status" id="programStatus" role="status">Edit the script if you like. Commands are executed in order after launch.</div>
        <div class="command-reference"><strong>Practice commands:</strong> <code>MOVE_TO dock|joint-a|hatch|rack|joint-b|goal</code>, <code>ALIGN</code>, <code>SCAN</code>, <code>WAIT 1</code>. Lines starting with # are ignored. These commands are interpreted by this web trainer only; they are not the official ROS API.</div>
      </div>
    </section>
    <div class="stage-frame">
      <canvas id="gameCanvas" tabindex="0" aria-label="Kibo module mission simulator"></canvas>
      <div class="stage-vignette"></div>
      <div class="stage-topline">
        <div class="stage-label">
          <div class="eyebrow">Current location</div>
          <div class="stage-location" id="locationName">KIBO PRESSURIZED MODULE</div>
          <div class="stage-coordinates" id="coordinateReadout">X 00.0 · Y 00.0 · HDG 000°</div>
        </div>
        <div class="stage-alert" id="stageAlert">MISSION CONTROL LINK ESTABLISHED<br>AWAITING LAUNCH AUTHORIZATION</div>
      </div>
      <div class="hud-bottom">
        <div class="hud-readouts">
          <div class="hud-readout"><div class="readout-label">Mission time</div><div class="readout-value" id="timerReadout">00:00</div></div>
          <div class="hud-readout"><div class="readout-label">Velocity</div><div class="readout-value"><span id="speedReadout">0.0</span><span style="font-size:9px;color:var(--muted)"> m/s</span></div></div>
        </div>
        <div class="scan-indicator" id="scanIndicator">● SCANNER STANDBY</div>
      </div>
      <div class="center-overlay" id="launchOverlay">
        <div class="launch-card" id="launchCard">
          <div class="launch-symbol">
            <svg viewBox="0 0 64 64" fill="none"><circle cx="32" cy="32" r="23" stroke="currentColor" stroke-width="1.5"/><circle cx="32" cy="32" r="13" stroke="currentColor" stroke-width="1.5" stroke-dasharray="4 4"/><circle cx="32" cy="32" r="5" fill="#82ffc1"/><path d="M32 3v10M32 51v10M3 32h10M51 32h10" stroke="currentColor" stroke-width="2" stroke-linecap="round"/><path d="m21 21 7 7m8 8 7 7m0-22-7 7m-8 8-7 7" stroke="currentColor" stroke-width="1.3" opacity=".7"/></svg>
          </div>
          <div class="eyebrow">Mission operations · training console</div>
          <h2 class="launch-title">READY FOR<br><span>DEPLOYMENT</span></h2>
          <p class="launch-description">Program an Int-Ball2-inspired robot to autonomously travel from its starting station, align its camera with AR markers, inspect checkpoints, and reach the goal. Start the launch sequence, then run the mission script above. The robot moves by itself.</p>
          <div class="launch-note"><strong>BASED ON THE 7TH KIBO-RPC PROGRAMMING MANUAL</strong><br>This is an independent educational browser trainer. Official programs use the provided ROS environment and Kibo-RPC APIs. Exact checkpoint positions and judging are supplied by the official simulator; the positions and scoring here are illustrative.</div>
          <button class="primary-button launch-button" id="launchButton">▶ &nbsp; Begin launch sequence</button>
          <div class="launch-foot">AUTONOMOUS PROGRAMMING · NO MANUAL STEERING</div>
        </div>
      </div>
    </div>
    <div class="target-banner" id="targetBanner" style="display:none">
      <div><strong id="targetBannerTitle">Checkpoint in range</strong><span id="targetBannerText">Align the robot and scan the marker.</span></div>
      <button class="primary-button" id="targetBannerButton">SCAN TARGET</button>
    </div>
    <div class="control-strip">
      <div class="control-group"><span class="keycap">W</span><span class="keycap">A</span><span class="keycap">S</span><span class="keycap">D</span><span class="control-label">Translate</span></div>
      <div class="control-group"><span class="keycap">←</span><span class="keycap">→</span><span class="control-label">Rotate heading</span></div>
      <div class="control-group"><span class="keycap">E</span><span class="control-label">Interact</span><span class="keycap">F</span><span class="control-label">Scan marker</span></div>
      <div class="control-group"><span class="keycap">R</span><span class="control-label">Stabilize</span><span class="keycap">H</span><span class="control-label">Help</span></div>
    </div>
    <div class="mobile-controls" aria-label="Movement controls">
      <button class="empty" tabindex="-1" aria-hidden="true">·</button>
      <button data-hold="up" aria-label="Move forward">▲</button>
      <button class="empty" tabindex="-1" aria-hidden="true">·</button>
      <button data-hold="left" aria-label="Move left">◀</button>
      <button data-hold="down" aria-label="Move backward">▼</button>
      <button data-hold="right" aria-label="Move right">▶</button>
    </div>
    <div class="mobile-actions">
      <button class="secondary-button" id="mobileRotateLeft">↶ Rotate</button>
      <button class="secondary-button" id="mobileRotateRight">Rotate ↷</button>
      <button class="secondary-button" id="mobileInteract">E · Interact</button>
      <button class="primary-button" id="mobileScan">F · Scan</button>
    </div>
  </section>
  <aside class="side-column">
    <section class="panel">
      <div class="panel-header"><h2 class="panel-title">Mission objectives</h2><span class="panel-kicker" id="objectiveCounter">0 / 6</span></div>
      <div class="panel-body">
        <div style="display:flex;justify-content:space-between;align-items:center;gap:10px"><span class="panel-kicker">Route completion</span><strong id="progressPercent" style="font-family:var(--mono);font-size:12px;color:var(--cyan)">0%</strong></div>
        <div class="mission-progress"><div class="mission-progress-fill" id="missionProgressFill"></div></div>
        <div class="objective-list" id="objectiveList"></div>
        <div class="help-tip">Official scoring checks position accuracy, camera centering on the AR marker, and attitude/roll around the line of sight. The lowest condition level determines the checkpoint level. This trainer estimates those ideas; it does not reproduce the official judge.</div>
      </div>
    </section>
    <section class="panel">
      <div class="panel-header"><h2 class="panel-title">Flight telemetry</h2><span class="panel-kicker">Live</span></div>
      <div class="panel-body">
        <div class="telemetry-row"><span class="telemetry-key">Position X</span><span class="telemetry-value" id="telemetryX">0.00 m</span></div>
        <div class="telemetry-row"><span class="telemetry-key">Position Y</span><span class="telemetry-value" id="telemetryY">0.00 m</span></div>
        <div class="telemetry-row"><span class="telemetry-key">Heading</span><span class="telemetry-value" id="telemetryHeading">000.0°</span></div>
        <div class="telemetry-row"><span class="telemetry-key">Camera centering</span><span class="telemetry-value" id="telemetryAlignment">—</span></div>
        <div class="telemetry-row"><span class="telemetry-key">Training checkpoint</span><span class="telemetry-value" id="checkpointReadout">—</span></div>
        <div class="telemetry-row"><span class="telemetry-key">Battery</span><span class="battery-wrap"><span class="telemetry-value" id="batteryText">100%</span><span class="battery-track"><span class="battery-fill" id="batteryFill" style="display:block"></span></span></span></div>
        <div class="telemetry-row"><span class="telemetry-key">Scanner</span><span class="telemetry-value" id="scannerStatus">STANDBY</span></div>
      </div>
    </section>
    <section class="panel">
      <div class="panel-header"><h2 class="panel-title">Route map</h2><span class="panel-kicker">Top-down</span></div>
      <div class="panel-body">
        <canvas class="route-preview" id="routeCanvas" width="560" height="240" aria-label="Route overview"></canvas>
        <div class="route-legend">
          <div class="legend-item"><span class="legend-dot" style="background:#63e6ff"></span>Drone</div>
          <div class="legend-item"><span class="legend-dot" style="background:#ffcb72"></span>Next target</div>
          <div class="legend-item"><span class="legend-dot" style="background:#82ffc1"></span>Scanned</div>
        </div>
      </div>
    </section>
    <section class="panel">
      <div class="panel-header"><h2 class="panel-title">Mission log</h2><span class="panel-kicker" id="logCount">01 events</span></div>
      <div class="panel-body"><div class="mission-log" id="missionLog" aria-live="polite"></div></div>
    </section>
    <section class="panel">
      <div class="panel-header"><h2 class="panel-title">Mission controls</h2><span class="panel-kicker">Tools</span></div>
      <div class="panel-body">
        <div class="panel-actions">
          <button class="secondary-button" id="helpButton">Help & controls</button>
          <button class="secondary-button" id="routeButton">Route briefing</button>
          <button class="secondary-button" id="resetButton">Restart mission</button>
        </div>
      </div>
    </section>
  </aside>
</main>
<footer class="footer-note">Independent educational practice simulator inspired by the Kibo Robot Programming Challenge scenario.<br>Not affiliated with or endorsed by JAXA, NASA, or the International Space Station program.</footer>
</div>
<div class="modal-backdrop" id="modalBackdrop" role="dialog" aria-modal="true" aria-labelledby="modalTitle">
  <div class="modal-card">
    <div class="modal-heading"><h2 id="modalTitle">Mission information</h2><button class="secondary-button" id="modalClose" aria-label="Close dialog">✕</button></div>
    <div class="modal-content" id="modalContent"></div>
    <div class="modal-footer"><button class="primary-button" id="modalOkay">Understood</button></div>
  </div>
</div>
<div class="toast-stack" id="toastStack" aria-live="polite"></div>
<script>
'use strict';
const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');
const routeCanvas = document.getElementById('routeCanvas');
const routeCtx = routeCanvas.getContext('2d');
const UI = {
  overlay: document.getElementById('launchOverlay'),
  launchCard: document.getElementById('launchCard'),
  launchButton: document.getElementById('launchButton'),
  location: document.getElementById('locationName'),
  coordinates: document.getElementById('coordinateReadout'),
  alert: document.getElementById('stageAlert'),
  timer: document.getElementById('timerReadout'),
  speed: document.getElementById('speedReadout'),
  scan: document.getElementById('scanIndicator'),
  objectives: document.getElementById('objectiveList'),
  objectiveCounter: document.getElementById('objectiveCounter'),
  progress: document.getElementById('missionProgressFill'),
  progressPercent: document.getElementById('progressPercent'),
  telemetryX: document.getElementById('telemetryX'),
  telemetryY: document.getElementById('telemetryY'),
  telemetryHeading: document.getElementById('telemetryHeading'),
  telemetryAlignment: document.getElementById('telemetryAlignment'),
  batteryText: document.getElementById('batteryText'),
  batteryFill: document.getElementById('batteryFill'),
  scannerStatus: document.getElementById('scannerStatus'),
  log: document.getElementById('missionLog'),
  logCount: document.getElementById('logCount'),
  targetBanner: document.getElementById('targetBanner'),
  targetTitle: document.getElementById('targetBannerTitle'),
  targetText: document.getElementById('targetBannerText'),
  targetButton: document.getElementById('targetBannerButton'),
  modalBackdrop: document.getElementById('modalBackdrop'),
  modalTitle: document.getElementById('modalTitle'),
  modalContent: document.getElementById('modalContent'),
  toastStack: document.getElementById('toastStack')
};
const WORLD = { width: 1200, height: 720, margin: 58, grid: 40 };
const CONFIG = {
  maxSpeed: 178,
  acceleration: 650,
  friction: 0.84,
  rotationSpeed: 2.55,
  interactionRadius: 70,
  scanRadius: 90,
  scanAngle: 0.72,
  batteryDrain: 0.012,
  scanDrain: 1.7,
  missionTimeLimit: 900,
  roomPadding: 36
};
const TARGETS = [
  { id: 'dock', checkpointId: 'START', markerId: null, name: 'Starting station / release', short: 'Start station', type: 'dock', x: 125, y: 360, heading: 0, hint: 'Begin at the docking station and confirm a stable release.', description: 'Starting location for the practice mission. The official program obtains checkpoint definitions through /mission/get_checkpoints.', icon: 'S' },
  { id: 'joint-a', checkpointId: 1, markerId: 1, name: 'Checkpoint 1 · Structural joint', short: 'CP 1 · Joint', type: 'joint', x: 345, y: 170, heading: 1.2, hint: 'Approach the joint and center AR marker 1.', description: 'Illustrative checkpoint only. Official checkpoint position and attitude come from the simulator response.', icon: '1' },
  { id: 'hatch', checkpointId: 2, markerId: 2, name: 'Checkpoint 2 · Hatch area', short: 'CP 2 · Hatch', type: 'hatch', x: 575, y: 530, heading: 2.5, hint: 'Inspect the hatch area and center AR marker 2.', description: 'Illustrative checkpoint only. Stop movement before asking the judge to evaluate a pass.', icon: '2' },
  { id: 'rack', checkpointId: 3, markerId: 3, name: 'Checkpoint 3 · Experiment rack', short: 'CP 3 · Rack', type: 'rack', x: 830, y: 180, heading: 5.3, hint: 'Inspect the experiment rack and center AR marker 3.', description: 'Illustrative checkpoint only. Marker detection requires the correct 4x4 dictionary, marker ID, marker size, and camera calibration.', icon: '3' },
  { id: 'joint-b', checkpointId: 4, markerId: 4, name: 'Checkpoint 4 · Structural joint', short: 'CP 4 · Joint', type: 'joint', x: 1030, y: 470, heading: 3.4, hint: 'Inspect the second joint and center AR marker 4.', description: 'Illustrative checkpoint only. The official judge evaluates position, camera centering, and roll/attitude margins.', icon: '4' },
  { id: 'panel', checkpointId: 5, markerId: 5, name: 'Checkpoint 5 · Utility panel', short: 'CP 5 · Panel', type: 'panel', x: 210, y: 150, heading: 0.8, hint: 'Inspect the utility panel and center AR marker 5.', description: 'Illustrative training location; not an official checkpoint coordinate.', icon: '5' },
  { id: 'sensor-bay', checkpointId: 6, markerId: 6, name: 'Checkpoint 6 · Sensor bay', short: 'CP 6 · Sensor', type: 'panel', x: 1000, y: 560, heading: 4.8, hint: 'Inspect the sensor bay and center AR marker 6.', description: 'Illustrative training location; not an official checkpoint coordinate.', icon: '6' },
  { id: 'rack-b', checkpointId: 7, markerId: 7, name: 'Checkpoint 7 · Rack end', short: 'CP 7 · Rack', type: 'rack', x: 700, y: 90, heading: 1.8, hint: 'Inspect the rack end and center AR marker 7.', description: 'Illustrative training location; not an official checkpoint coordinate.', icon: '7' },
  { id: 'hatch-b', checkpointId: 8, markerId: 8, name: 'Checkpoint 8 · Hatch frame', short: 'CP 8 · Hatch', type: 'hatch', x: 90, y: 560, heading: 5.5, hint: 'Inspect the hatch frame and center AR marker 8.', description: 'Illustrative training location; the actual number and layout depend on the official course.', icon: '8' },
  { id: 'goal', checkpointId: 12, markerId: 12, name: 'Goal checkpoint · ID 12', short: 'Goal · 12', type: 'goal', x: 145, y: 360, heading: 0, hint: 'Reach the designated goal checkpoint after completing the route.', description: 'The manual example uses goalpoint_id 12. The real goal is read from the official checkpoint response, not assumed from this drawing.', icon: 'G' }
];
const ROOM_FIXTURES = [
  { type: 'rack', x: 245, y: 300, w: 104, h: 170, label: 'EXP RACK 01' },
  { type: 'rack', x: 440, y: 110, w: 84, h: 190, label: 'EXP RACK 02' },
  { type: 'rack', x: 660, y: 360, w: 116, h: 185, label: 'EXP RACK 03' },
  { type: 'rack', x: 900, y: 270, w: 82, h: 150, label: 'EXP RACK 04' },
  { type: 'cabinet', x: 520, y: 340, w: 82, h: 74, label: 'CONTROL' },
  { type: 'cabinet', x: 740, y: 120, w: 66, h: 72, label: 'UTILITY' },
  { type: 'hatch', x: 575, y: 530, w: 86, h: 22, label: 'HATCH' },
  { type: 'pipe', x: 330, y: 545, w: 170, h: 14, label: '' },
  { type: 'pipe', x: 780, y: 560, w: 140, h: 12, label: '' },
  { type: 'panel', x: 160, y: 130, w: 120, h: 42, label: 'AIR MONITOR' },
  { type: 'panel', x: 940, y: 555, w: 120, h: 40, label: 'SENSOR BAY' }
];
const state = {
  started: false,
  launching: false,
  launchStart: 0,
  completed: false,
  paused: false,
  elapsed: 0,
  lastFrame: 0,
  timeLimit: CONFIG.missionTimeLimit,
  battery: 100,
  score: 0,
  scans: 0,
  logs: [],
  targetIndex: 0,
  flash: 0,
  shake: 0,
  scanAnimation: 0,
  scanPulse: 0,
  toastId: 0,
  lastUiUpdate: 0,
  scanLock: false,
  scanFeedback: '',
  player: { x: 125, y: 360, vx: 0, vy: 0, angle: 0, radius: 15, trail: [], lastX: 125, lastY: 360 },
  keys: new Set(),
  touch: { up: false, down: false, left: false, right: false },
  particles: [],
  stars: [],
  scanResults: [],
  lastTargetId: null,
  bestAlignment: 180,
  missionStartWallTime: 0,
  autoRunning: false,
  program: [],
  programIndex: 0,
  autoPath: [],
  autoCommand: null,
  autoWait: 0,
  autoStall: 0,
  autoLastPosition: { x: 125, y: 360 }
};
let canvasWidth = 1200;
let canvasHeight = 720;
let pixelRatio = 1;
let audioContext = null;
let ambientOscillator = null;
let ambientGain = null;
let muted = true;

function clamp(value, min, max) {
  return Math.max(min, Math.min(max, value));
}

function lerp(a, b, amount) {
  return a + (b - a) * amount;
}

function distance(a, b) {
  return Math.hypot(a.x - b.x, a.y - b.y);
}

function normalizeAngle(angle) {
  let result = angle % (Math.PI * 2);
  if (result < 0) result += Math.PI * 2;
  return result;
}

function angleDifference(a, b) {
  let difference = normalizeAngle(a - b);
  if (difference > Math.PI) difference -= Math.PI * 2;
  return difference;
}

function formatTime(seconds) {
  const safe = Math.max(0, Math.floor(seconds));
  const minutes = Math.floor(safe / 60).toString().padStart(2, '0');
  const remaining = (safe % 60).toString().padStart(2, '0');
  return `${minutes}:${remaining}`;
}

function formatHeading(angle) {
  return `${Math.round(normalizeAngle(angle) * 180 / Math.PI).toString().padStart(3, '0')}°`;
}

function currentTarget() {
  if (state.completed) return null;
  return TARGETS[state.targetIndex] || null;
}

function currentTargetDistance() {
  const target = currentTarget();
  return target ? distance(state.player, target) : Infinity;
}

function currentAlignment(target = currentTarget()) {
  if (!target) return 180;
  return Math.abs(angleDifference(state.player.angle, target.heading)) * 180 / Math.PI;
}

function alignmentLabel(value) {
  if (value < 10) return 'EXCELLENT';
  if (value < 25) return 'GOOD';
  if (value < 48) return 'ADJUST';
  return 'MISALIGNED';
}

function resizeCanvas() {
  const rect = canvas.getBoundingClientRect();
  pixelRatio = Math.min(window.devicePixelRatio || 1, 1.25);
  canvasWidth = Math.max(320, rect.width);
  canvasHeight = Math.max(300, rect.height);
  canvas.width = Math.floor(canvasWidth * pixelRatio);
  canvas.height = Math.floor(canvasHeight * pixelRatio);
  ctx.setTransform(pixelRatio, 0, 0, pixelRatio, 0, 0);
  ctx.imageSmoothingEnabled = true;
  render();
}

function worldScale() {
  const horizontal = (canvasWidth - 80) / WORLD.width;
  const vertical = (canvasHeight - 100) / WORLD.height;
  return Math.max(0.35, Math.min(horizontal, vertical));
}

function worldOffset() {
  const scale = worldScale();
  return {
    x: (canvasWidth - WORLD.width * scale) / 2,
    y: (canvasHeight - WORLD.height * scale) / 2
  };
}

function toScreen(point) {
  const scale = worldScale();
  const offset = worldOffset();
  return { x: offset.x + point.x * scale, y: offset.y + point.y * scale };
}

function toWorld(point) {
  const scale = worldScale();
  const offset = worldOffset();
  return { x: (point.x - offset.x) / scale, y: (point.y - offset.y) / scale };
}

function initStars() {
  state.stars = [];
  for (let index = 0; index < 55; index += 1) {
    state.stars.push({
      x: Math.random(),
      y: Math.random(),
      size: Math.random() * 1.5 + 0.3,
      alpha: Math.random() * 0.38 + 0.08,
      phase: Math.random() * Math.PI * 2
    });
  }
}

function initParticles() {
  state.particles = [];
  for (let index = 0; index < 14; index += 1) {
    state.particles.push({
      x: Math.random() * WORLD.width,
      y: Math.random() * WORLD.height,
      radius: Math.random() * 2.2 + 0.5,
      drift: Math.random() * 10 + 2,
      phase: Math.random() * Math.PI * 2
    });
  }
}

function addLog(message, type = 'normal') {
  const stamp = state.started ? formatTime(state.elapsed) : '00:00';
  state.logs.unshift({ stamp, message, type });
  state.logs = state.logs.slice(0, 35);
  renderLog();
}

function renderLog() {
  UI.log.replaceChildren();
  state.logs.forEach(entry => {
    const row = document.createElement('div');
    row.className = `log-entry ${entry.type}`;
    const time = document.createElement('span');
    time.className = 'log-time';
    time.textContent = entry.stamp;
    const message = document.createElement('span');
    message.className = 'log-message';
    message.textContent = entry.message;
    row.append(time, message);
    UI.log.append(row);
  });
  UI.logCount.textContent = `${state.logs.length.toString().padStart(2, '0')} events`;
}

function showToast(message, type = 'normal', duration = 3000) {
  const toast = document.createElement('div');
  toast.className = `toast ${type}`;
  toast.textContent = message;
  UI.toastStack.append(toast);
  window.setTimeout(() => toast.remove(), duration);
}

function showModal(title, content) {
  UI.modalTitle.textContent = title;
  UI.modalContent.replaceChildren();
  if (typeof content === 'string') {
    const wrapper = document.createElement('div');
    wrapper.innerHTML = content;
    UI.modalContent.append(wrapper);
  } else if (content instanceof Node) {
    UI.modalContent.append(content);
  }
  UI.modalBackdrop.classList.add('visible');
  UI.modalBackdrop.dataset.open = 'true';
  UI.modalClose.focus();
}

function closeModal() {
  UI.modalBackdrop.classList.remove('visible');
  delete UI.modalBackdrop.dataset.open;
  canvas.focus({ preventScroll: true });
}

function addTextBlock(parent, heading, text) {
  const title = document.createElement('h3');
  title.textContent = heading;
  const paragraph = document.createElement('p');
  paragraph.textContent = text;
  parent.append(title, paragraph);
}

function showHelp() {
  const fragment = document.createDocumentFragment();
  addTextBlock(fragment, 'Movement', 'Write commands in the program editor and press Run autonomous mission. The robot follows its own route; no manual steering is required during the mission.');
  addTextBlock(fragment, 'Scan a checkpoint', 'The script uses MOVE_TO, ALIGN, and SCAN. The autonomous controller navigates toward the active marker, aligns the camera, stabilizes, and records the scan.');
  addTextBlock(fragment, 'Mission sequence', 'Release at the docking station, scan each highlighted AR marker in order, then return to the goal checkpoint. The objective list updates automatically after a successful scan.');
  addTextBlock(fragment, 'Recovery', 'If a command fails, stop the program, edit the script, and run it again. Restart Mission resets the simulated route.');
  showModal('Autonomous mission help', fragment);
}

function showRouteBriefing() {
  const fragment = document.createDocumentFragment();
  addTextBlock(fragment, 'Mission task', 'Inspect the illustrated Kibo module checkpoints and return to the goal. This practice route is fictionalized for gameplay; it does not represent official checkpoint coordinates.');
  const list = document.createElement('ul');
  TARGETS.forEach((target, index) => {
    const item = document.createElement('li');
    item.textContent = `${index + 1}. ${target.name} — ${target.description}`;
    list.append(item);
  });
  fragment.append(list);
  addTextBlock(fragment, 'Official scoring concepts', 'The Kibo-RPC manual describes three checkpoint conditions: position distance, camera centering toward the AR marker, and attitude/roll around the line of sight. The lowest of the condition levels becomes the checkpoint level; a condition outside its margin fails the pass. This browser trainer uses illustrative coordinates and an approximate score, not the official judge.');
  addTextBlock(fragment, 'Official workflow', 'The official program obtains checkpoint definitions, starts the mission, commands movement through the control action, waits for the robot to stabilize, requests checkpoint evaluation, logs the result, and notifies mission completion. This browser app teaches the workflow but does not connect to ROS or the JAXA simulator.');
  showModal('Route briefing', fragment);
}

function renderObjectives() {
  UI.objectives.replaceChildren();
  TARGETS.forEach((target, index) => {
    const item = document.createElement('div');
    const complete = index < state.targetIndex || state.completed;
    const active = index === state.targetIndex && !state.completed;
    item.className = `objective-item${active ? ' active' : ''}${complete ? ' complete' : ''}`;
    const icon = document.createElement('div');
    icon.className = 'objective-icon';
    icon.textContent = complete ? '✓' : target.icon;
    const copy = document.createElement('div');
    const name = document.createElement('div');
    name.className = 'objective-name';
    name.textContent = target.name;
    const hint = document.createElement('div');
    hint.className = 'objective-hint';
    hint.textContent = complete ? 'Registered · training result' : `${target.hint}${target.markerId ? ` (AR marker ${target.markerId})` : ''}`;
    copy.append(name, hint);
    const status = document.createElement('div');
    status.className = 'objective-state';
    status.textContent = complete ? 'Done' : active ? 'Current' : 'Queued';
    item.append(icon, copy, status);
    UI.objectives.append(item);
  });
  const done = state.completed ? TARGETS.length : state.targetIndex;
  const percentage = Math.round(done / TARGETS.length * 100);
  UI.objectiveCounter.textContent = `${done} / ${TARGETS.length}`;
  UI.progressPercent.textContent = `${percentage}%`;
  UI.progress.style.width = `${percentage}%`;
}

function updateTelemetry() {
  const player = state.player;
  const speed = Math.hypot(player.vx, player.vy);
  const target = currentTarget();
  const alignment = currentAlignment(target);
  UI.coordinates.textContent = `X ${player.x.toFixed(1)} · Y ${player.y.toFixed(1)} · HDG ${formatHeading(player.angle)}`;
  UI.telemetryX.textContent = `${player.x.toFixed(2)} m`;
  UI.telemetryY.textContent = `${player.y.toFixed(2)} m`;
  UI.telemetryHeading.textContent = `${(normalizeAngle(player.angle) * 180 / Math.PI).toFixed(1)}°`;
  UI.telemetryAlignment.textContent = target ? `${alignment.toFixed(1)}° · ${alignmentLabel(alignment)}` : 'COMPLETE';
  const checkpointReadout = document.getElementById('checkpointReadout');
  if (checkpointReadout) checkpointReadout.textContent = target ? `${target.checkpointId === 'START' ? 'Start station' : 'CP ' + target.checkpointId} · Marker ${target.markerId ?? '—'}` : 'Goal reached';
  UI.batteryText.textContent = `${Math.ceil(state.battery)}%`;
  UI.batteryFill.style.width = `${state.battery}%`;
  UI.batteryFill.style.background = state.battery < 20 ? 'var(--red)' : state.battery < 45 ? 'var(--amber)' : 'var(--green)';
  UI.speed.textContent = (speed / 100).toFixed(1);
  UI.timer.textContent = formatTime(state.elapsed);
  UI.scannerStatus.textContent = state.scanAnimation > 0 ? 'SCANNING' : 'STANDBY';
  UI.scan.textContent = state.scanAnimation > 0 ? '◌ SCANNING MARKER' : '● SCANNER STANDBY';
  UI.location.textContent = state.completed ? 'MISSION COMPLETE' : target ? target.name.toUpperCase() : 'KIBO PRESSURIZED MODULE';
  UI.alert.textContent = state.completed ? 'ALL CHECKPOINTS REGISTERED\nROUTE SUBMITTED' : target ? `NEXT: ${target.name.toUpperCase()}\n${currentTargetDistance() < CONFIG.scanRadius ? 'TARGET IN RANGE' : 'NAVIGATE TO HIGHLIGHTED MARKER'}` : 'AWAITING MISSION';
  updateTargetBanner();
}

function updateTargetBanner() {
  const target = currentTarget();
  if (!state.started || !target || state.completed) {
    UI.targetBanner.classList.remove('visible');
    return;
  }
  const targetDistance = currentTargetDistance();
  const alignment = currentAlignment(target);
  if (targetDistance <= CONFIG.scanRadius * 1.25) {
    UI.targetBanner.classList.add('visible');
    UI.targetTitle.textContent = targetDistance <= CONFIG.scanRadius ? `${target.name} · IN RANGE` : `${target.name} · APPROACH`;
    UI.targetText.textContent = targetDistance <= CONFIG.scanRadius ? `Distance ${targetDistance.toFixed(0)} units · Alignment ${alignment.toFixed(0)}°` : `Move ${Math.max(0, targetDistance - CONFIG.scanRadius).toFixed(0)} more units toward the marker.`;
    UI.targetButton.textContent = targetDistance <= CONFIG.scanRadius ? 'SCAN TARGET' : 'TARGET AHEAD';
    UI.targetButton.disabled = targetDistance > CONFIG.scanRadius;
  } else {
    UI.targetBanner.classList.remove('visible');
  }
}

function drawBackground(time) {
  const gradient = ctx.createLinearGradient(0, 0, canvasWidth, canvasHeight);
  gradient.addColorStop(0, '#071426');
  gradient.addColorStop(.52, '#12334b');
  gradient.addColorStop(1, '#06101e');
  ctx.fillStyle = gradient;
  ctx.fillRect(0, 0, canvasWidth, canvasHeight);
  state.stars.forEach(star => {
    const alpha = star.alpha * (.72 + Math.sin(time * .001 + star.phase) * .28);
    ctx.fillStyle = `rgba(140,214,255,${alpha})`;
    ctx.fillRect(star.x * canvasWidth, star.y * canvasHeight, star.size, star.size);
  });
  const scale = worldScale();
  const offset = worldOffset();
  ctx.save();
  ctx.translate(offset.x, offset.y);
  ctx.scale(scale, scale);
  state.particles.forEach(particle => {
    const y = (particle.y + Math.sin(time * .0002 + particle.phase) * particle.drift + WORLD.height) % WORLD.height;
    ctx.fillStyle = 'rgba(47,105,129,.18)';
    ctx.beginPath();
    ctx.arc(particle.x, y, particle.radius, 0, Math.PI * 2);
    ctx.fill();
  });
  ctx.restore();
}

function roundedRect(context, x, y, width, height, radius) {
  const r = Math.min(radius, width / 2, height / 2);
  context.beginPath();
  context.moveTo(x + r, y);
  context.arcTo(x + width, y, x + width, y + height, r);
  context.arcTo(x + width, y + height, x, y + height, r);
  context.arcTo(x, y + height, x, y, r);
  context.arcTo(x, y, x + width, y, r);
  context.closePath();
}

function drawRoom(time) {
  const scale = worldScale();
  const offset = worldOffset();
  ctx.save();
  ctx.translate(offset.x, offset.y);
  ctx.scale(scale, scale);
  const x = 0;
  const y = 0;
  const w = WORLD.width;
  const h = WORLD.height;
  const floor = ctx.createLinearGradient(0, 0, w, h);
  floor.addColorStop(0, '#d4e0e5');
  floor.addColorStop(.5, '#b8cbd4');
  floor.addColorStop(1, '#91aab8');
  ctx.fillStyle = floor;
  roundedRect(ctx, x, y, w, h, 42);
  ctx.fill();
  ctx.save();
  roundedRect(ctx, x + 2, y + 2, w - 4, h - 4, 40);
  ctx.clip();
  ctx.strokeStyle = 'rgba(35,72,91,.20)';
  ctx.lineWidth = 1;
  for (let gx = 0; gx <= w; gx += WORLD.grid) {
    ctx.beginPath();
    ctx.moveTo(gx, 0);
    ctx.lineTo(gx, h);
    ctx.stroke();
  }
  for (let gy = 0; gy <= h; gy += WORLD.grid) {
    ctx.beginPath();
    ctx.moveTo(0, gy);
    ctx.lineTo(w, gy);
    ctx.stroke();
  }
  drawFloorPanels(time);
  drawWallRibs();
  ROOM_FIXTURES.forEach(fixture => drawFixture(fixture, time));
  drawDockingArea();
  drawRouteLine();
  drawTargets(time);
  drawPlayer(time);
  drawParticlesInRoom(time);
  ctx.restore();
  drawRoomBorder();
  ctx.restore();
}

function drawFloorPanels(time) {
  ctx.save();
  ctx.lineWidth = 2;
  for (let index = 0; index < 12; index += 1) {
    const x = 25 + index * 100;
    ctx.strokeStyle = index % 2 === 0 ? 'rgba(122,197,223,.08)' : 'rgba(122,197,223,.04)';
    ctx.beginPath();
    ctx.moveTo(x, 28);
    ctx.lineTo(x, WORLD.height - 28);
    ctx.stroke();
  }
  for (let index = 0; index < 6; index += 1) {
    const y = 45 + index * 125;
    ctx.strokeStyle = 'rgba(122,197,223,.045)';
    ctx.beginPath();
    ctx.moveTo(25, y);
    ctx.lineTo(WORLD.width - 25, y);
    ctx.stroke();
  }
  const glow = ctx.createRadialGradient(580, 350, 20, 580, 350, 460);
  glow.addColorStop(0, `rgba(67,157,190,${.14 + Math.sin(time * .001) * .025})`);
  glow.addColorStop(1, 'rgba(65,100,120,0)');
  ctx.fillStyle = glow;
  ctx.fillRect(0, 0, WORLD.width, WORLD.height);
  ctx.restore();
}

function drawWallRibs() {
  ctx.save();
  for (let index = 0; index < 13; index += 1) {
    const x = 32 + index * 94;
    const gradient = ctx.createLinearGradient(x - 4, 0, x + 4, 0);
    gradient.addColorStop(0, 'rgba(4,10,17,.3)');
    gradient.addColorStop(.5, 'rgba(131,189,212,.12)');
    gradient.addColorStop(1, 'rgba(4,10,17,.35)');
    ctx.fillStyle = gradient;
    ctx.fillRect(x - 4, 8, 8, WORLD.height - 16);
  }
  for (let index = 0; index < 8; index += 1) {
    const y = 32 + index * 94;
    ctx.strokeStyle = 'rgba(42,78,97,.30)';
    ctx.lineWidth = 3;
    ctx.beginPath();
    ctx.moveTo(12, y);
    ctx.lineTo(WORLD.width - 12, y);
    ctx.stroke();
  }
  ctx.restore();
}

function drawFixture(fixture, time) {
  ctx.save();
  if (fixture.type === 'rack') {
    const gradient = ctx.createLinearGradient(fixture.x, fixture.y, fixture.x + fixture.w, fixture.y + fixture.h);
    gradient.addColorStop(0, '#8da7b4');
    gradient.addColorStop(.4, '#607f90');
    gradient.addColorStop(1, '#3d5a6b');
    ctx.fillStyle = 'rgba(25,47,60,.18)';
    roundedRect(ctx, fixture.x + 8, fixture.y + 10, fixture.w, fixture.h, 8);
    ctx.fill();
    ctx.fillStyle = gradient;
    roundedRect(ctx, fixture.x, fixture.y, fixture.w, fixture.h, 8);
    ctx.fill();
    ctx.strokeStyle = 'rgba(143,208,231,.35)';
    ctx.lineWidth = 2;
    ctx.stroke();
    ctx.fillStyle = '#344e5d';
    roundedRect(ctx, fixture.x + 9, fixture.y + 12, fixture.w - 18, fixture.h - 24, 5);
    ctx.fill();
    const count = Math.max(3, Math.floor(fixture.h / 24));
    for (let index = 0; index < count; index += 1) {
      const sy = fixture.y + 18 + index * ((fixture.h - 36) / count);
      ctx.fillStyle = index % 3 === 0 ? '#274b61' : '#18364b';
      roundedRect(ctx, fixture.x + 14, sy, fixture.w - 28, 12, 3);
      ctx.fill();
      ctx.fillStyle = index % 2 === 0 ? '#63e6ff' : '#82ffc1';
      ctx.globalAlpha = .45 + .2 * Math.sin(time * .003 + index);
      ctx.fillRect(fixture.x + fixture.w - 20, sy + 4, 4, 4);
      ctx.globalAlpha = 1;
    }
    ctx.fillStyle = '#a9c7d9';
    ctx.font = 'bold 10px ui-monospace, monospace';
    ctx.textAlign = 'center';
    ctx.fillText(fixture.label, fixture.x + fixture.w / 2, fixture.y + fixture.h + 17);
    drawFixtureBolts(fixture.x, fixture.y, fixture.w, fixture.h);
  } else if (fixture.type === 'cabinet') {
    ctx.fillStyle = '#7895a4';
    roundedRect(ctx, fixture.x, fixture.y, fixture.w, fixture.h, 7);
    ctx.fill();
    ctx.strokeStyle = '#52778c';
    ctx.lineWidth = 2;
    ctx.stroke();
    ctx.fillStyle = '#415d6d';
    roundedRect(ctx, fixture.x + 9, fixture.y + 9, fixture.w - 18, fixture.h - 18, 4);
    ctx.fill();
    ctx.fillStyle = '#63e6ff';
    ctx.fillRect(fixture.x + 16, fixture.y + 17, fixture.w - 32, 3);
    for (let index = 0; index < 3; index += 1) {
      ctx.fillStyle = index === 1 ? '#82ffc1' : '#ffcb72';
      ctx.beginPath();
      ctx.arc(fixture.x + 20 + index * 14, fixture.y + fixture.h - 19, 3, 0, Math.PI * 2);
      ctx.fill();
    }
    ctx.fillStyle = '#a9c7d9';
    ctx.font = 'bold 9px ui-monospace, monospace';
    ctx.textAlign = 'center';
    ctx.fillText(fixture.label, fixture.x + fixture.w / 2, fixture.y + fixture.h + 14);
  } else if (fixture.type === 'hatch') {
    ctx.fillStyle = '#a2b8c2';
    roundedRect(ctx, fixture.x - 6, fixture.y - 18, fixture.w + 12, fixture.h + 36, 11);
    ctx.fill();
    ctx.strokeStyle = '#7ba6bc';
    ctx.lineWidth = 4;
    ctx.stroke();
    ctx.strokeStyle = '#2e566d';
    ctx.lineWidth = 2;
    ctx.strokeRect(fixture.x + 5, fixture.y - 9, fixture.w - 10, fixture.h + 18);
    ctx.fillStyle = '#7ba6bc';
    for (let index = 0; index < 4; index += 1) {
      ctx.beginPath();
      ctx.arc(fixture.x + 9 + index * 22, fixture.y + fixture.h / 2, 3, 0, Math.PI * 2);
      ctx.fill();
    }
    ctx.fillStyle = '#c4d9e5';
    ctx.font = 'bold 10px ui-monospace, monospace';
    ctx.textAlign = 'center';
    ctx.fillText(fixture.label, fixture.x + fixture.w / 2, fixture.y + fixture.h + 32);
  } else if (fixture.type === 'pipe') {
    ctx.fillStyle = '#718f9f';
    roundedRect(ctx, fixture.x, fixture.y, fixture.w, fixture.h, fixture.h / 2);
    ctx.fill();
    ctx.strokeStyle = '#5f8499';
    ctx.lineWidth = 2;
    ctx.stroke();
    for (let index = 0; index < fixture.w; index += 38) {
      ctx.fillStyle = '#7fa3b7';
      ctx.fillRect(fixture.x + index, fixture.y - 3, 5, fixture.h + 6);
    }
  } else if (fixture.type === 'panel') {
    ctx.fillStyle = '#8aa5b3';
    roundedRect(ctx, fixture.x, fixture.y, fixture.w, fixture.h, 6);
    ctx.fill();
    ctx.strokeStyle = '#527c91';
    ctx.lineWidth = 2;
    ctx.stroke();
    ctx.fillStyle = '#0a1a28';
    roundedRect(ctx, fixture.x + 8, fixture.y + 7, fixture.w - 16, fixture.h - 14, 3);
    ctx.fill();
    ctx.fillStyle = '#63e6ff';
    ctx.fillRect(fixture.x + 15, fixture.y + 15, fixture.w * .35, 3);
    ctx.fillStyle = '#82ffc1';
    ctx.fillRect(fixture.x + fixture.w * .58, fixture.y + 15, fixture.w * .2, 3);
    ctx.fillStyle = '#b2cfdf';
    ctx.font = 'bold 8px ui-monospace, monospace';
    ctx.textAlign = 'center';
    ctx.fillText(fixture.label, fixture.x + fixture.w / 2, fixture.y + fixture.h - 8);
  }
  ctx.restore();
}

function drawFixtureBolts(x, y, w, h) {
  const points = [[x + 7, y + 7], [x + w - 7, y + 7], [x + 7, y + h - 7], [x + w - 7, y + h - 7]];
  points.forEach(point => {
    ctx.fillStyle = '#8eafc0';
    ctx.beginPath();
    ctx.arc(point[0], point[1], 2.5, 0, Math.PI * 2);
    ctx.fill();
  });
}

function drawDockingArea() {
  ctx.save();
  const dock = TARGETS[0];
  const glow = ctx.createRadialGradient(dock.x, dock.y, 8, dock.x, dock.y, 92);
  glow.addColorStop(0, 'rgba(99,230,255,.16)');
  glow.addColorStop(1, 'rgba(99,230,255,0)');
  ctx.fillStyle = glow;
  ctx.beginPath();
  ctx.arc(dock.x, dock.y, 92, 0, Math.PI * 2);
  ctx.fill();
  ctx.strokeStyle = 'rgba(99,230,255,.4)';
  ctx.lineWidth = 3;
  ctx.beginPath();
  ctx.arc(dock.x, dock.y, 38, 0, Math.PI * 2);
  ctx.stroke();
  ctx.strokeStyle = 'rgba(99,230,255,.17)';
  ctx.lineWidth = 1;
  ctx.beginPath();
  ctx.arc(dock.x, dock.y, 52, 0, Math.PI * 2);
  ctx.stroke();
  ctx.fillStyle = '#1e455b';
  roundedRect(ctx, dock.x - 31, dock.y - 24, 62, 48, 9);
  ctx.fill();
  ctx.strokeStyle = '#6ccde8';
  ctx.lineWidth = 2;
  ctx.stroke();
  ctx.fillStyle = '#a8eaff';
  ctx.fillRect(dock.x - 18, dock.y - 11, 36, 4);
  ctx.fillStyle = '#82ffc1';
  ctx.beginPath();
  ctx.arc(dock.x, dock.y + 5, 5, 0, Math.PI * 2);
  ctx.fill();
  ctx.fillStyle = '#c4e5f4';
  ctx.font = 'bold 11px ui-monospace, monospace';
  ctx.textAlign = 'center';
  ctx.fillText('DOCKING STATION', dock.x, dock.y + 52);
  ctx.restore();
}

function drawRouteLine() {
  ctx.save();
  ctx.setLineDash([9, 12]);
  ctx.lineWidth = 2;
  ctx.strokeStyle = 'rgba(99,230,255,.2)';
  ctx.beginPath();
  TARGETS.forEach((target, index) => {
    if (index === 0) ctx.moveTo(target.x, target.y);
    else ctx.lineTo(target.x, target.y);
  });
  ctx.stroke();
  ctx.setLineDash([]);
  ctx.restore();
}

function drawTargets(time) {
  TARGETS.forEach((target, index) => {
    const completed = index < state.targetIndex || state.completed;
    const active = index === state.targetIndex && !state.completed;
    if (completed) {
      drawCompletedTarget(target);
      return;
    }
    const phase = time * .002 + index;
    const pulse = 1 + (Math.sin(phase) + 1) * .11;
    const radius = active ? 26 * pulse : 15;
    ctx.save();
    ctx.globalAlpha = active ? 1 : .35;
    const color = active ? '#ffcb72' : '#7393a8';
    const glow = ctx.createRadialGradient(target.x, target.y, 2, target.x, target.y, radius * 2.8);
    glow.addColorStop(0, active ? 'rgba(255,203,114,.22)' : 'rgba(115,147,168,.08)');
    glow.addColorStop(1, 'rgba(0,0,0,0)');
    ctx.fillStyle = glow;
    ctx.beginPath();
    ctx.arc(target.x, target.y, radius * 2.8, 0, Math.PI * 2);
    ctx.fill();
    ctx.strokeStyle = color;
    ctx.lineWidth = active ? 3 : 2;
    ctx.beginPath();
    ctx.arc(target.x, target.y, radius, 0, Math.PI * 2);
    ctx.stroke();
    ctx.beginPath();
    ctx.moveTo(target.x - radius * 1.55, target.y);
    ctx.lineTo(target.x - radius * .65, target.y);
    ctx.moveTo(target.x + radius * .65, target.y);
    ctx.lineTo(target.x + radius * 1.55, target.y);
    ctx.moveTo(target.x, target.y - radius * 1.55);
    ctx.lineTo(target.x, target.y - radius * .65);
    ctx.moveTo(target.x, target.y + radius * .65);
    ctx.lineTo(target.x, target.y + radius * 1.55);
    ctx.stroke();
    ctx.fillStyle = color;
    ctx.font = 'bold 12px ui-monospace, monospace';
    ctx.textAlign = 'center';
    ctx.fillText(target.icon, target.x, target.y + 4);
    ctx.fillStyle = active ? '#ffe2ad' : '#a4bac9';
    ctx.font = active ? 'bold 13px ui-monospace, monospace' : '10px ui-monospace, monospace';
    ctx.fillText(target.short.toUpperCase(), target.x, target.y - radius - 12);
    if (active) {
      const distanceToTarget = distance(state.player, target);
      ctx.fillStyle = 'rgba(255,203,114,.9)';
      ctx.font = '10px ui-monospace, monospace';
      ctx.fillText(`${distanceToTarget.toFixed(0)} u`, target.x, target.y + radius + 17);
    }
    ctx.restore();
  });
}

function drawCompletedTarget(target) {
  ctx.save();
  ctx.globalAlpha = .85;
  ctx.fillStyle = 'rgba(130,255,193,.12)';
  ctx.beginPath();
  ctx.arc(target.x, target.y, 19, 0, Math.PI * 2);
  ctx.fill();
  ctx.strokeStyle = '#82ffc1';
  ctx.lineWidth = 2;
  ctx.beginPath();
  ctx.arc(target.x, target.y, 15, 0, Math.PI * 2);
  ctx.stroke();
  ctx.fillStyle = '#82ffc1';
  ctx.font = 'bold 15px ui-monospace, monospace';
  ctx.textAlign = 'center';
  ctx.fillText('✓', target.x, target.y + 5);
  ctx.restore();
}

function drawPlayer(time) {
  const player = state.player;
  ctx.save();
  if (state.shake > 0) {
    ctx.translate((Math.random() - .5) * state.shake, (Math.random() - .5) * state.shake);
  }
  player.trail.forEach((point, index) => {
    const alpha = (index + 1) / player.trail.length * .15;
    ctx.fillStyle = `rgba(99,230,255,${alpha})`;
    ctx.beginPath();
    ctx.arc(point.x, point.y, 3 + index * .2, 0, Math.PI * 2);
    ctx.fill();
  });
  const pulse = 1 + Math.sin(time * .005) * .04;
  const glow = ctx.createRadialGradient(player.x, player.y, 2, player.x, player.y, 48);
  glow.addColorStop(0, 'rgba(99,230,255,.22)');
  glow.addColorStop(1, 'rgba(99,230,255,0)');
  ctx.fillStyle = glow;
  ctx.beginPath();
  ctx.arc(player.x, player.y, 48, 0, Math.PI * 2);
  ctx.fill();
  ctx.translate(player.x, player.y);
  ctx.rotate(player.angle);
  ctx.scale(pulse, pulse);
  ctx.fillStyle = 'rgba(0,0,0,.3)';
  ctx.beginPath();
  ctx.ellipse(4, 6, 22, 18, 0, 0, Math.PI * 2);
  ctx.fill();
  const body = ctx.createRadialGradient(-5, -7, 1, 0, 0, 23);
  body.addColorStop(0, '#d6fbff');
  body.addColorStop(.35, '#72d7ed');
  body.addColorStop(.72, '#2d7799');
  body.addColorStop(1, '#12334b');
  ctx.fillStyle = body;
  ctx.beginPath();
  ctx.arc(0, 0, 17, 0, Math.PI * 2);
  ctx.fill();
  ctx.strokeStyle = '#b7f5ff';
  ctx.lineWidth = 1.5;
  ctx.stroke();
  ctx.fillStyle = '#102638';
  ctx.beginPath();
  ctx.ellipse(4, -1, 8, 10, 0, 0, Math.PI * 2);
  ctx.fill();
  ctx.fillStyle = '#63e6ff';
  ctx.beginPath();
  ctx.ellipse(6, -2, 4.4, 6.2, 0, 0, Math.PI * 2);
  ctx.fill();
  ctx.fillStyle = '#ffffff';
  ctx.beginPath();
  ctx.arc(7, -4, 1.4, 0, Math.PI * 2);
  ctx.fill();
  ctx.strokeStyle = '#e5fcff';
  ctx.lineWidth = 2.5;
  ctx.beginPath();
  ctx.moveTo(15, 0);
  ctx.lineTo(25, 0);
  ctx.stroke();
  ctx.fillStyle = '#82ffc1';
  ctx.beginPath();
  ctx.arc(25, 0, 3, 0, Math.PI * 2);
  ctx.fill();
  ctx.strokeStyle = 'rgba(99,230,255,.45)';
  ctx.lineWidth = 1;
  ctx.beginPath();
  ctx.arc(0, 0, 22, time * .001, time * .001 + Math.PI * 1.35);
  ctx.stroke();
  ctx.restore();
  if (state.scanAnimation > 0) drawScanEffect(player.x, player.y, time);
}

function drawScanEffect(x, y, time) {
  const progress = 1 - state.scanAnimation / 1.1;
  const radius = 18 + progress * 110;
  ctx.save();
  ctx.globalAlpha = Math.max(0, 1 - progress);
  ctx.strokeStyle = '#63e6ff';
  ctx.lineWidth = 3;
  ctx.beginPath();
  ctx.arc(x, y, radius, 0, Math.PI * 2);
  ctx.stroke();
  ctx.strokeStyle = 'rgba(99,230,255,.65)';
  ctx.lineWidth = 1;
  ctx.beginPath();
  ctx.arc(x, y, radius * .72, 0, Math.PI * 2);
  ctx.stroke();
  ctx.restore();
}

function drawParticlesInRoom(time) {
  state.particles.forEach(particle => {
    const x = (particle.x + Math.sin(time * .0003 + particle.phase) * 8 + WORLD.width) % WORLD.width;
    const y = (particle.y + Math.cos(time * .00025 + particle.phase) * 6 + WORLD.height) % WORLD.height;
    ctx.fillStyle = 'rgba(49,112,140,.20)';
    ctx.beginPath();
    ctx.arc(x, y, particle.radius, 0, Math.PI * 2);
    ctx.fill();
  });
}

function drawRoomBorder() {
  const scale = worldScale();
  const offset = worldOffset();
  ctx.save();
  ctx.translate(offset.x, offset.y);
  ctx.scale(scale, scale);
  ctx.strokeStyle = '#537e95';
  ctx.lineWidth = 7;
  roundedRect(ctx, 0, 0, WORLD.width, WORLD.height, 42);
  ctx.stroke();
  ctx.strokeStyle = 'rgba(99,230,255,.3)';
  ctx.lineWidth = 2;
  roundedRect(ctx, 9, 9, WORLD.width - 18, WORLD.height - 18, 34);
  ctx.stroke();
  const corners = [[24,24,1,1],[WORLD.width-24,24,-1,1],[24,WORLD.height-24,1,-1],[WORLD.width-24,WORLD.height-24,-1,-1]];
  corners.forEach(corner => {
    ctx.strokeStyle = '#8ddff4';
    ctx.lineWidth = 3;
    ctx.beginPath();
    ctx.moveTo(corner[0], corner[1] + 22 * corner[3]);
    ctx.lineTo(corner[0], corner[1]);
    ctx.lineTo(corner[0] + 22 * corner[2], corner[1]);
    ctx.stroke();
  });
  ctx.restore();
}

let lastRouteRender = 0;
function renderRouteMap(force = false) {
  const now = performance.now();
  if (!force && now - lastRouteRender < 180) return;
  lastRouteRender = now;
  const width = routeCanvas.width;
  const height = routeCanvas.height;
  routeCtx.clearRect(0, 0, width, height);
  routeCtx.fillStyle = '#071421';
  routeCtx.fillRect(0, 0, width, height);
  const margin = 22;
  const scaleX = (width - margin * 2) / WORLD.width;
  const scaleY = (height - margin * 2) / WORLD.height;
  const sx = x => margin + x * scaleX;
  const sy = y => margin + y * scaleY;
  routeCtx.strokeStyle = 'rgba(99,230,255,.08)';
  routeCtx.lineWidth = 1;
  for (let index = 0; index <= 12; index += 1) {
    const x = margin + index * (width - margin * 2) / 12;
    routeCtx.beginPath();
    routeCtx.moveTo(x, margin);
    routeCtx.lineTo(x, height - margin);
    routeCtx.stroke();
  }
  for (let index = 0; index <= 6; index += 1) {
    const y = margin + index * (height - margin * 2) / 6;
    routeCtx.beginPath();
    routeCtx.moveTo(margin, y);
    routeCtx.lineTo(width - margin, y);
    routeCtx.stroke();
  }
  routeCtx.strokeStyle = '#34556a';
  routeCtx.lineWidth = 2;
  roundedRect(routeCtx, margin, margin, width - margin * 2, height - margin * 2, 12);
  routeCtx.stroke();
  ROOM_FIXTURES.forEach(fixture => {
    routeCtx.fillStyle = fixture.type === 'rack' ? '#1b394e' : '#294c60';
    routeCtx.fillRect(sx(fixture.x), sy(fixture.y), Math.max(3, fixture.w * scaleX), Math.max(3, fixture.h * scaleY));
  });
  routeCtx.strokeStyle = 'rgba(99,230,255,.5)';
  routeCtx.lineWidth = 1.5;
  routeCtx.setLineDash([4, 4]);
  routeCtx.beginPath();
  TARGETS.forEach((target, index) => {
    if (index === 0) routeCtx.moveTo(sx(target.x), sy(target.y));
    else routeCtx.lineTo(sx(target.x), sy(target.y));
  });
  routeCtx.stroke();
  routeCtx.setLineDash([]);
  TARGETS.forEach((target, index) => {
    const completed = index < state.targetIndex || state.completed;
    const active = index === state.targetIndex && !state.completed;
    routeCtx.fillStyle = completed ? '#82ffc1' : active ? '#ffcb72' : '#547287';
    routeCtx.beginPath();
    routeCtx.arc(sx(target.x), sy(target.y), active ? 5 : 3.5, 0, Math.PI * 2);
    routeCtx.fill();
  });
  const player = state.player;
  routeCtx.save();
  routeCtx.translate(sx(player.x), sy(player.y));
  routeCtx.rotate(player.angle);
  routeCtx.fillStyle = '#63e6ff';
  routeCtx.beginPath();
  routeCtx.moveTo(7, 0);
  routeCtx.lineTo(-5, -4.5);
  routeCtx.lineTo(-3, 0);
  routeCtx.lineTo(-5, 4.5);
  routeCtx.closePath();
  routeCtx.fill();
  routeCtx.restore();
}

function render(time = performance.now()) {
  if (!ctx) return;
  ctx.setTransform(pixelRatio, 0, 0, pixelRatio, 0, 0);
  drawBackground(time);
  drawRoom(time);
  if (time - lastRouteRender > 180) renderRouteMap();
}

function canMoveTo(x, y) {
  const radius = state.player.radius;
  if (x < WORLD.margin + radius || x > WORLD.width - WORLD.margin - radius) return false;
  if (y < WORLD.margin + radius || y > WORLD.height - WORLD.margin - radius) return false;
  for (const fixture of ROOM_FIXTURES) {
    const padding = radius + 5;
    const insideX = x + padding > fixture.x && x - padding < fixture.x + fixture.w;
    const insideY = y + padding > fixture.y && y - padding < fixture.y + fixture.h;
    if (insideX && insideY && fixture.type !== 'pipe' && fixture.type !== 'panel') return false;
  }
  return true;
}

function stabilize() {
  state.player.vx *= .12;
  state.player.vy *= .12;
  state.player.vx = Math.abs(state.player.vx) < 3 ? 0 : state.player.vx;
  state.player.vy = Math.abs(state.player.vy) < 3 ? 0 : state.player.vy;
  addLog('Attitude hold engaged; translation damped.', 'success');
  showToast('Stabilization engaged.', 'success', 1800);
}

function updatePlayerManual(delta) {
  const player = state.player;
  const keys = state.keys;
  const touch = state.touch;
  const left = keys.has('arrowleft') || keys.has('q');
  const right = keys.has('arrowright') || keys.has('rshift');
  if (left || touch.left) player.angle -= CONFIG.rotationSpeed * delta;
  if (right || touch.right) player.angle += CONFIG.rotationSpeed * delta;
  player.angle = normalizeAngle(player.angle);
  let dx = 0;
  let dy = 0;
  if (keys.has('w') || keys.has('arrowup') || touch.up) dy -= 1;
  if (keys.has('s') || keys.has('arrowdown') || touch.down) dy += 1;
  if (keys.has('a')) dx -= 1;
  if (keys.has('d')) dx += 1;
  if (dx !== 0 && dy !== 0) {
    dx *= Math.SQRT1_2;
    dy *= Math.SQRT1_2;
  }
  const acceleration = CONFIG.acceleration * delta;
  player.vx += dx * acceleration;
  player.vy += dy * acceleration;
  player.vx *= Math.pow(CONFIG.friction, delta * 60);
  player.vy *= Math.pow(CONFIG.friction, delta * 60);
  const speed = Math.hypot(player.vx, player.vy);
  if (speed > CONFIG.maxSpeed) {
    player.vx = player.vx / speed * CONFIG.maxSpeed;
    player.vy = player.vy / speed * CONFIG.maxSpeed;
  }
  const nextX = player.x + player.vx * delta;
  const nextY = player.y + player.vy * delta;
  if (canMoveTo(nextX, player.y)) player.x = nextX;
  else player.vx *= -.12;
  if (canMoveTo(player.x, nextY)) player.y = nextY;
  else player.vy *= -.12;
  player.x = clamp(player.x, WORLD.margin + player.radius, WORLD.width - WORLD.margin - player.radius);
  player.y = clamp(player.y, WORLD.margin + player.radius, WORLD.height - WORLD.margin - player.radius);
  if (Math.hypot(player.x - player.lastX, player.y - player.lastY) > 4) {
    player.trail.push({ x: player.lastX, y: player.lastY });
    if (player.trail.length > 12) player.trail.shift();
    player.lastX = player.x;
    player.lastY = player.y;
  }
  if (state.started && !state.completed && speed > 4) state.battery = Math.max(0, state.battery - CONFIG.batteryDrain * delta * speed / 40);
  state.shake = Math.max(0, state.shake - delta * 8);
  state.scanAnimation = Math.max(0, state.scanAnimation - delta);
  state.scanPulse += delta;
}

function pointNearFixture(point, fixture, padding = 0) {
  const nearestX = clamp(point.x, fixture.x - padding, fixture.x + fixture.w + padding);
  const nearestY = clamp(point.y, fixture.y - padding, fixture.y + fixture.h + padding);
  return Math.hypot(point.x - nearestX, point.y - nearestY) < point.radius;
}

function getNearbyInteractable() {
  const target = currentTarget();
  if (!target) return null;
  return distance(state.player, target) <= CONFIG.interactionRadius ? target : null;
}

function interact() {
  if (!state.started || state.completed || state.paused) return;
  const target = getNearbyInteractable();
  if (!target) {
    const next = currentTarget();
    if (next) {
      const remaining = Math.max(0, distance(state.player, next) - CONFIG.interactionRadius);
      showToast(`Not in interaction range. Move about ${Math.ceil(remaining)} units closer to ${next.short}.`, 'warning');
      addLog(`Interaction unavailable: ${next.short} is out of range.`, 'warning');
    }
    return;
  }
  if (target.type === 'dock' && state.targetIndex === 0) {
    state.player.x = target.x + 45;
    state.player.y = target.y;
    state.player.angle = target.heading;
    state.player.vx = 0;
    state.player.vy = 0;
    showToast('Dock release confirmed. Registering docking checkpoint.', 'success');
    addLog('Docking station release confirmed.', 'success');
    scanTarget();
    return;
  }
  scanTarget();
}

function scanTarget() {
  if (!state.started || state.completed || state.paused || state.scanLock) return;
  const target = currentTarget();
  if (!target) return;
  const range = distance(state.player, target);
  if (range > CONFIG.scanRadius) {
    const remaining = Math.ceil(range - CONFIG.scanRadius);
    showToast(`Marker out of range. Move ${remaining} units closer.`, 'warning');
    addLog(`Scan rejected: ${target.short} out of range (${range.toFixed(0)} units).`, 'warning');
    state.flash = .15;
    return;
  }
  const alignment = currentAlignment(target);
  if (alignment > 100) {
    showToast(`Heading is reversed. Rotate toward ${target.short}; alignment error is ${alignment.toFixed(0)}°.`, 'warning');
    addLog(`Scan rejected: heading error ${alignment.toFixed(0)}°.`, 'warning');
    return;
  }
  state.scanLock = true;
  state.scanAnimation = 1.1;
  state.scanFeedback = target.id;
  state.scans += 1;
  const rangeScore = Math.round(clamp(100 - range * .48, 45, 100));
  const alignmentScore = Math.round(clamp(100 - alignment * 1.45, 25, 100));
  const speed = Math.hypot(state.player.vx, state.player.vy);
  const stabilityScore = Math.round(clamp(100 - speed * .32, 25, 100));
  const earned = Math.round(rangeScore * .35 + alignmentScore * .45 + stabilityScore * .2);
  state.score += earned;
  state.bestAlignment = Math.min(state.bestAlignment, alignment);
  state.battery = Math.max(0, state.battery - CONFIG.scanDrain);
  state.scanResults.push({ id: target.id, range, alignment, speed, score: earned });
  addLog(`${target.short} marker registered · ${earned}/100 scan quality.`, 'success');
  showToast(`${target.short} registered. Scan quality ${earned}/100.`, 'success', 2400);
  state.targetIndex += 1;
  renderObjectives();
  updateTelemetry();
  window.setTimeout(() => {
    state.scanLock = false;
    if (state.targetIndex >= TARGETS.length) completeMission();
  }, 520);
}

function completeMission() {
  if (state.completed) return;
  state.completed = true;
  state.player.vx = 0;
  state.player.vy = 0;
  state.score += Math.max(0, Math.round((state.timeLimit - state.elapsed) * .25));
  renderObjectives();
  updateTelemetry();
  addLog('Goal checkpoint reached. Route submitted successfully.', 'success');
  showToast('Mission complete. Route submitted.', 'success', 5000);
  window.setTimeout(showResults, 700);
}

function showResults() {
  const fragment = document.createDocumentFragment();
  const score = document.createElement('div');
  score.className = 'result-score';
  score.textContent = state.score.toLocaleString();
  const caption = document.createElement('div');
  caption.className = 'result-caption';
  caption.textContent = 'Training mission score';
  fragment.append(score, caption);
  const grid = document.createElement('div');
  grid.className = 'result-grid';
  const metrics = [
    ['Checkpoints', `${TARGETS.length}/${TARGETS.length}`],
    ['Mission time', formatTime(state.elapsed)],
    ['Markers scanned', String(state.scans)],
    ['Battery remaining', `${Math.ceil(state.battery)}%`],
    ['Best alignment', `${state.bestAlignment.toFixed(1)}°`],
    ['Scan quality avg.', `${Math.round(state.scanResults.reduce((sum, item) => sum + item.score, 0) / Math.max(1, state.scanResults.length))}/100`]
  ];
  metrics.forEach(metric => {
    const item = document.createElement('div');
    item.className = 'result-item';
    const label = document.createElement('span');
    label.textContent = metric[0];
    const value = document.createElement('strong');
    value.textContent = metric[1];
    item.append(label, value);
    grid.append(item);
  });
  fragment.append(grid);
  addTextBlock(fragment, 'Debrief', 'Mission complete. Compare your scan quality and heading alignment, then restart to practice a cleaner route. This score is illustrative and is not an official Kibo-RPC score.');
  showModal('Mission complete', fragment);
}

function resetMission(showMessage = true) {
  state.started = false;
  state.launching = false;
  state.completed = false;
  state.paused = false;
  state.elapsed = 0;
  state.battery = 100;
  state.score = 0;
  state.scans = 0;
  state.targetIndex = 0;
  state.flash = 0;
  state.shake = 0;
  state.scanAnimation = 0;
  state.scanPulse = 0;
  state.scanLock = false;
  state.scanFeedback = '';
  state.logs = [];
  state.scanResults = [];
  state.autoRunning = false;
  state.program = [];
  state.programIndex = 0;
  state.autoPath = [];
  state.autoCommand = null;
  state.autoWait = 0;
  state.autoStall = 0;
  document.body.classList.add('autonomous-mode');
  state.bestAlignment = 180;
  state.keys.clear();
  state.touch = { up: false, down: false, left: false, right: false };
  state.player = { x: 125, y: 360, vx: 0, vy: 0, angle: 0, radius: 15, trail: [], lastX: 125, lastY: 360 };
  UI.overlay.style.display = 'flex';
  UI.launchCard.innerHTML = `<div class="launch-symbol"><svg viewBox="0 0 64 64" fill="none"><circle cx="32" cy="32" r="23" stroke="currentColor" stroke-width="1.5"/><circle cx="32" cy="32" r="13" stroke="currentColor" stroke-width="1.5" stroke-dasharray="4 4"/><circle cx="32" cy="32" r="5" fill="#82ffc1"/><path d="M32 3v10M32 51v10M3 32h10M51 32h10" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg></div><div class="eyebrow">Mission operations · training console</div><h2 class="launch-title">READY FOR<br><span>DEPLOYMENT</span></h2><p class="launch-description">Program an Int-Ball2-inspired inspection robot to autonomously visit inspection checkpoints. Write the command sequence, launch the mission, and review its accuracy, heading, and route time.</p><div class="launch-note"><strong>TRAINING SIMULATOR NOTICE</strong><br>This is an independent educational practice project, not an official JAXA or NASA simulator. Locations and scoring are illustrative until official mission materials specify otherwise.</div><button class="primary-button launch-button" id="launchButton">▶ &nbsp; Begin launch sequence</button><div class="launch-foot">AUTONOMOUS PROGRAMMING · NO MANUAL STEERING</div>`;
  document.getElementById('launchButton').addEventListener('click', beginLaunch);
  UI.targetBanner.classList.remove('visible');
  renderObjectives();
  addLog('Mission console initialized. Awaiting launch authorization.');
  updateTelemetry();
  if (showMessage) showToast('Mission reset. Launch when ready.', 'success');
  render();
}

function beginLaunch() {
  if (state.launching || state.started) return;
  state.launching = true;
  state.launchStart = performance.now();
  UI.launchCard.innerHTML = `<div class="eyebrow">Flight systems check</div><h2 class="launch-title">LAUNCH<br><span>SEQUENCE</span></h2><div class="launch-count" id="launchCount">3</div><p class="launch-description" id="launchDescription">Checking attitude control, scanner, and telemetry link…</p><div class="launch-progress"><div class="launch-progress-fill" id="launchProgressFill"></div></div>`;
  addLog('Launch sequence started. Running pre-flight checks.');
  soundBeep(440, .08);
  const startedAt = performance.now();
  function step(now) {
    if (!state.launching) return;
    const elapsed = now - startedAt;
    const progress = clamp(elapsed / 3100, 0, 1);
    const count = Math.max(0, 3 - Math.floor(elapsed / 1000));
    const countElement = document.getElementById('launchCount');
    const description = document.getElementById('launchDescription');
    const progressFill = document.getElementById('launchProgressFill');
    if (countElement) countElement.textContent = count === 0 ? 'GO' : String(count);
    if (description) {
      if (elapsed < 900) description.textContent = 'Checking attitude control, scanner, and telemetry link…';
      else if (elapsed < 1900) description.textContent = 'Verifying docking release and checkpoint database…';
      else description.textContent = 'All systems nominal. Deploying into Kibo module.';
    }
    if (progressFill) progressFill.style.width = `${progress * 100}%`;
    if (elapsed < 3100) {
      if (Math.floor(elapsed / 1000) !== Math.floor((elapsed - 16) / 1000)) soundBeep(500 + count * 60, .06);
      requestAnimationFrame(step);
    } else {
      state.launching = false;
      state.started = true;
      state.elapsed = 0;
      state.missionStartWallTime = performance.now();
      UI.overlay.style.display = 'none';
      canvas.focus({ preventScroll: true });
      addLog('Launch successful. Int-Ball2 training unit deployed.', 'success');
      addLog('Autonomous console ready. Load or edit a mission script, then run it.', 'normal');
      setProgramStatus('Launch complete. Press Run autonomous mission to execute your script.', 'PROGRAM READY');
      showToast('Launch successful. Welcome aboard Kibo.', 'success');
      soundBeep(740, .18);
      updateTelemetry();
    }
  }
  requestAnimationFrame(step);
}

function soundBeep(frequency = 520, duration = .08) {
  if (muted) return;
  try {
    audioContext = audioContext || new (window.AudioContext || window.webkitAudioContext)();
    const oscillator = audioContext.createOscillator();
    const gain = audioContext.createGain();
    oscillator.type = 'sine';
    oscillator.frequency.value = frequency;
    gain.gain.setValueAtTime(.045, audioContext.currentTime);
    gain.gain.exponentialRampToValueAtTime(.001, audioContext.currentTime + duration);
    oscillator.connect(gain);
    gain.connect(audioContext.destination);
    oscillator.start();
    oscillator.stop(audioContext.currentTime + duration);
  } catch (error) {
    muted = true;
  }
}

function updatePlayer(delta) {
  if (state.autoRunning) {
    updateAutonomousPlayer(delta);
    return;
  }
  updatePlayerManual(delta);
}

function parseProgram() {
  const raw = document.getElementById('programEditor').value;
  const allowed = new Set(TARGETS.map(target => target.id));
  const commands = [];
  const lines = raw.split(/\r?\n/);
  for (let index = 0; index < lines.length; index += 1) {
    const line = lines[index].trim();
    if (!line || line.startsWith('#')) continue;
    const parts = line.split(/\s+/);
    const command = parts[0].toUpperCase();
    if (command === 'MOVE_TO' && parts.length === 2 && allowed.has(parts[1].toLowerCase())) {
      commands.push({ type: 'MOVE_TO', targetId: parts[1].toLowerCase(), line: index + 1 });
    } else if (command === 'ALIGN' && parts.length === 1) {
      commands.push({ type: 'ALIGN', line: index + 1 });
    } else if (command === 'SCAN' && parts.length === 1) {
      commands.push({ type: 'SCAN', line: index + 1 });
    } else if (command === 'WAIT' && parts.length === 2 && Number.isFinite(Number(parts[1])) && Number(parts[1]) >= 0 && Number(parts[1]) <= 10) {
      commands.push({ type: 'WAIT', seconds: Number(parts[1]), line: index + 1 });
    } else {
      throw new Error(`Line ${index + 1}: invalid command "${line}".`);
    }
  }
  if (!commands.length) throw new Error('Your program is empty. Add at least one command.');
  return commands;
}

function setProgramStatus(message, stateLabel = 'PROGRAM READY') {
  const status = document.getElementById('programStatus');
  const label = document.getElementById('programState');
  if (status) status.textContent = message;
  if (label) label.textContent = stateLabel;
}

function runAutonomousProgram() {
  if (!state.started) {
    showToast('Begin the launch sequence first.', 'warning');
    setProgramStatus('Begin the launch sequence, then run your script.', 'AWAITING LAUNCH');
    return;
  }
  if (state.completed) {
    showToast('Mission is already complete. Restart to run again.', 'warning');
    return;
  }
  try {
    state.program = parseProgram();
  } catch (error) {
    setProgramStatus(error.message, 'PROGRAM ERROR');
    addLog(error.message, 'alert');
    showToast(error.message, 'warning', 3500);
    return;
  }
  state.autoRunning = true;
  state.paused = false;
  state.programIndex = 0;
  state.autoPath = [];
  state.autoCommand = null;
  state.autoWait = 0;
  state.autoStall = 0;
  state.player.vx = 0;
  state.player.vy = 0;
  document.body.classList.add('autonomous-mode');
  setProgramStatus(`Program loaded: ${state.program.length} commands. Robot is executing autonomously.`, 'RUNNING');
  addLog(`Autonomous program started: ${state.program.length} commands loaded.`, 'success');
  showToast('Autonomous mission started.', 'success');
}

function stopAutonomousProgram() {
  state.autoRunning = false;
  state.player.vx = 0;
  state.player.vy = 0;
  document.body.classList.remove('autonomous-mode');
  setProgramStatus('Program stopped. Edit the script and run it again when ready.', 'STOPPED');
  addLog('Autonomous program stopped by operator.', 'warning');
}

function targetById(id) {
  return TARGETS.find(target => target.id === id);
}

function findApproachPoint(target) {
  const candidates = [];
  for (let radius = 34; radius <= 78; radius += 11) {
    for (let angle = 0; angle < Math.PI * 2; angle += Math.PI / 4) {
      const point = { x: target.x + Math.cos(angle) * radius, y: target.y + Math.sin(angle) * radius };
      if (canMoveTo(point.x, point.y)) candidates.push(point);
    }
    if (candidates.length) break;
  }
  candidates.sort((a, b) => distance(state.player, a) - distance(state.player, b));
  return candidates[0] || { x: target.x + 82, y: target.y };
}

function buildAutoPath(destination) {
  const step = 24;
  const cols = Math.floor(WORLD.width / step) + 1;
  const rows = Math.floor(WORLD.height / step) + 1;
  const toCell = point => ({ x: clamp(Math.round(point.x / step), 0, cols - 1), y: clamp(Math.round(point.y / step), 0, rows - 1) });
  const start = toCell(state.player);
  const goal = toCell(destination);
  const key = cell => `${cell.x},${cell.y}`;
  const queue = [start];
  const previous = new Map([[key(start), null]]);
  let found = null;
  const directions = [{ x: 1, y: 0 }, { x: -1, y: 0 }, { x: 0, y: 1 }, { x: 0, y: -1 }, { x: 1, y: 1 }, { x: -1, y: 1 }, { x: 1, y: -1 }, { x: -1, y: -1 }];
  for (let head = 0; head < queue.length && head < 6000; head += 1) {
    const cell = queue[head];
    if (Math.hypot(cell.x - goal.x, cell.y - goal.y) <= 1.5) { found = cell; break; }
    for (const direction of directions) {
      const next = { x: cell.x + direction.x, y: cell.y + direction.y };
      if (next.x < 3 || next.y < 3 || next.x > cols - 4 || next.y > rows - 4) continue;
      const nextKey = key(next);
      if (previous.has(nextKey)) continue;
      if (!canMoveTo(next.x * step, next.y * step)) continue;
      if (direction.x && direction.y && (!canMoveTo((cell.x + direction.x) * step, cell.y * step) || !canMoveTo(cell.x * step, (cell.y + direction.y) * step))) continue;
      previous.set(nextKey, key(cell));
      queue.push(next);
    }
  }
  if (!found) return [destination];
  const path = [];
  let cursor = key(found);
  while (cursor) {
    const parts = cursor.split(',').map(Number);
    path.push({ x: parts[0] * step, y: parts[1] * step });
    cursor = previous.get(cursor);
  }
  path.reverse();
  path.push(destination);
  return path;
}

function moveAutonomouslyToward(destination, delta) {
  const player = state.player;
  if (!state.autoPath.length) state.autoPath = buildAutoPath(destination);
  while (state.autoPath.length && distance(player, state.autoPath[0]) < 18) state.autoPath.shift();
  const waypoint = state.autoPath[0] || destination;
  const dx = waypoint.x - player.x;
  const dy = waypoint.y - player.y;
  const desired = Math.atan2(dy, dx);
  const turn = angleDifference(desired, player.angle);
  player.angle = normalizeAngle(player.angle + clamp(turn, -CONFIG.rotationSpeed * delta, CONFIG.rotationSpeed * delta));
  const remaining = Math.hypot(dx, dy);
  const speed = Math.min(105, Math.max(0, remaining * 2.0));
  const alignmentFactor = Math.max(.25, Math.cos(Math.min(Math.PI / 2, Math.abs(turn))));
  const travel = Math.min(remaining, speed * alignmentFactor * delta);
  const nextX = player.x + (dx / Math.max(1, remaining)) * travel;
  const nextY = player.y + (dy / Math.max(1, remaining)) * travel;
  if (canMoveTo(nextX, player.y)) player.x = nextX;
  if (canMoveTo(player.x, nextY)) player.y = nextY;
  player.vx = (player.x - player.lastX) / Math.max(delta, .001);
  player.vy = (player.y - player.lastY) / Math.max(delta, .001);
  if (Math.hypot(player.x - player.lastX, player.y - player.lastY) > 3) {
    player.trail.push({ x: player.lastX, y: player.lastY });
    if (player.trail.length > 12) player.trail.shift();
  }
  player.lastX = player.x;
  player.lastY = player.y;
  if (Math.hypot(player.x - state.autoLastPosition.x, player.y - state.autoLastPosition.y) < .7) state.autoStall += delta;
  else state.autoStall = 0;
  state.autoLastPosition = { x: player.x, y: player.y };
  if (state.autoStall > 2.2) {
    state.autoPath = [];
    state.autoStall = 0;
    if (distance(player, destination) > CONFIG.scanRadius) {
      const target = currentTarget();
      if (target) addLog(`Autopilot recalculating route near ${target.short}.`, 'warning');
    }
  }
  state.battery = Math.max(0, state.battery - .003 * delta * Math.hypot(player.vx, player.vy));
}

function updateAutonomousPlayer(delta) {
  if (!state.autoRunning || state.paused || state.completed) return;
  state.scanAnimation = Math.max(0, state.scanAnimation - delta);
  state.scanPulse += delta;
  if (state.autoWait > 0) { state.autoWait -= delta; return; }
  if (state.programIndex >= state.program.length) {
    state.autoRunning = false;
    document.body.classList.remove('autonomous-mode');
    if (!state.completed) {
      setProgramStatus('Program ended before all checkpoints were completed. Check the command sequence.', 'PROGRAM ENDED');
      addLog('Program ended before the mission route was complete.', 'alert');
    }
    return;
  }
  const command = state.program[state.programIndex];
  state.autoCommand = command;
  setProgramStatus(`Executing line ${command.line}: ${command.type}${command.targetId ? ' ' + command.targetId : ''}`, 'RUNNING');
  if (command.type === 'MOVE_TO') {
    const target = targetById(command.targetId);
    if (!target) { state.programIndex += 1; return; }
    const destination = findApproachPoint(target);
    if (distance(state.player, destination) < 19 || distance(state.player, target) <= CONFIG.scanRadius) {
      state.player.vx = 0; state.player.vy = 0; state.autoPath = [];
      state.programIndex += 1;
      addLog(`Autonomous navigation reached approach zone for ${target.short}.`, 'success');
    } else moveAutonomouslyToward(destination, delta);
  } else if (command.type === 'ALIGN') {
    const target = currentTarget() || targetById(state.program.find(item => item.type === 'MOVE_TO' && item.line > command.line)?.targetId || 'goal');
    if (!target) { state.programIndex += 1; return; }
    const difference = angleDifference(target.heading, state.player.angle);
    state.player.angle = normalizeAngle(state.player.angle + clamp(difference, -CONFIG.rotationSpeed * delta, CONFIG.rotationSpeed * delta));
    state.player.vx *= .2; state.player.vy *= .2;
    if (Math.abs(difference) < .045) { state.player.angle = target.heading; state.programIndex += 1; addLog(`Camera attitude aligned for ${target.short}.`, 'success'); }
  } else if (command.type === 'SCAN') {
    state.player.vx *= .1; state.player.vy *= .1;
    const target = currentTarget();
    if (!target) { state.programIndex += 1; return; }
    if (distance(state.player, target) <= CONFIG.scanRadius && currentAlignment(target) < 35) {
      const before = state.targetIndex;
      scanTarget();
      if (state.targetIndex > before || state.completed) { state.programIndex += 1; state.autoPath = []; }
    } else {
      const destination = findApproachPoint(target);
      moveAutonomouslyToward(destination, delta);
    }
  } else if (command.type === 'WAIT') {
    state.autoWait = command.seconds;
    state.programIndex += 1;
  }
}

function tick(delta) {
  if (!state.started || state.completed || state.paused) return;
  state.elapsed += delta;
  updatePlayer(delta);
  if (state.elapsed >= state.timeLimit) {
    state.paused = true;
    addLog('Training time limit reached. Mission paused for debrief.', 'alert');
    showModal('Training time expired', 'The practice timer reached its limit. Restart the mission to try a faster route.');
  }
  if (state.battery <= 0) {
    state.battery = 0;
    state.paused = true;
    addLog('Battery depleted. Mission paused.', 'alert');
    showModal('Battery depleted', 'The drone battery has run out in this practice run. Restart the mission to try again. Use shorter movements and avoid unnecessary scanning attempts.');
  }
  if (state.elapsed - state.lastUiUpdate > .12) {
    state.lastUiUpdate = state.elapsed;
    updateTelemetry();
  }
}

let lastRenderTime = 0;
function frame(time) {
  if (!state.lastFrame) state.lastFrame = time;
  const delta = Math.min(.033, Math.max(0, (time - state.lastFrame) / 1000));
  state.lastFrame = time;
  tick(delta);
  if (time - lastRenderTime >= 30) {
    lastRenderTime = time;
    render(time);
  }
  requestAnimationFrame(frame);
}

function handleKeyDown(event) {
  const key = event.key.toLowerCase();
  if (['arrowup','arrowdown','arrowleft','arrowright',' '].includes(key)) event.preventDefault();
  if (UI.modalBackdrop.classList.contains('visible')) {
    if (key === 'escape' || key === 'enter') closeModal();
    return;
  }
  if (key === 'h' && !event.repeat) {
    showHelp();
    return;
  }
  if (key === 'f' && !event.repeat) {
    scanTarget();
    return;
  }
  if (key === 'e' && !event.repeat) {
    interact();
    return;
  }
  if (key === ' ' && !event.repeat) {
    scanTarget();
    return;
  }
  if (key === 'r' && !event.repeat) {
    stabilize();
    return;
  }
  if (key === 'escape') {
    if (state.started) {
      state.paused = !state.paused;
      showToast(state.paused ? 'Mission paused. Press Escape to resume.' : 'Mission resumed.', 'normal');
    }
    return;
  }
  state.keys.add(key);
}

function handleKeyUp(event) {
  state.keys.delete(event.key.toLowerCase());
}

function bindHoldButton(button, direction) {
  const set = active => {
    state.touch[direction] = active;
    if (active) canvas.focus({ preventScroll: true });
  };
  button.addEventListener('pointerdown', event => {
    event.preventDefault();
    button.setPointerCapture(event.pointerId);
    set(true);
  });
  button.addEventListener('pointerup', () => set(false));
  button.addEventListener('pointercancel', () => set(false));
  button.addEventListener('lostpointercapture', () => set(false));
  button.addEventListener('contextmenu', event => event.preventDefault());
}

function bindEvents() {
  document.addEventListener('keydown', handleKeyDown);
  document.addEventListener('keyup', handleKeyUp);
  window.addEventListener('blur', () => {
    state.keys.clear();
    state.touch = { up: false, down: false, left: false, right: false };
  });
  window.addEventListener('resize', resizeCanvas);
  UI.launchButton.addEventListener('click', beginLaunch);
  document.getElementById('runProgramButton').addEventListener('click', runAutonomousProgram);
  document.getElementById('stopProgramButton').addEventListener('click', stopAutonomousProgram);
  document.getElementById('sampleProgramButton').addEventListener('click', () => { document.getElementById('programEditor').value = 'MOVE_TO dock\nALIGN\nWAIT 1\nSCAN\nMOVE_TO joint-a\nALIGN\nWAIT 1\nSCAN\nMOVE_TO hatch\nALIGN\nWAIT 1\nSCAN\nMOVE_TO rack\nALIGN\nWAIT 1\nSCAN\nMOVE_TO joint-b\nALIGN\nWAIT 1\nSCAN\nMOVE_TO panel\nALIGN\nWAIT 1\nSCAN\nMOVE_TO sensor-bay\nALIGN\nWAIT 1\nSCAN\nMOVE_TO rack-b\nALIGN\nWAIT 1\nSCAN\nMOVE_TO hatch-b\nALIGN\nWAIT 1\nSCAN\nMOVE_TO goal\nALIGN\nWAIT 1\nSCAN'; setProgramStatus('Sample route restored. This is a training script; run it after launch.', 'PROGRAM READY'); });
  UI.targetButton.addEventListener('click', scanTarget);
  document.getElementById('helpButton').addEventListener('click', showHelp);
  document.getElementById('routeButton').addEventListener('click', showRouteBriefing);
  document.getElementById('resetButton').addEventListener('click', () => {
    closeModal();
    resetMission(true);
  });
  UI.modalClose.addEventListener('click', closeModal);
  document.getElementById('modalOkay').addEventListener('click', closeModal);
  UI.modalBackdrop.addEventListener('click', event => {
    if (event.target === UI.modalBackdrop) closeModal();
  });
  document.querySelectorAll('[data-hold]').forEach(button => bindHoldButton(button, button.dataset.hold));
  document.getElementById('mobileRotateLeft').addEventListener('click', () => {
    state.player.angle = normalizeAngle(state.player.angle - Math.PI / 8);
    updateTelemetry();
  });
  document.getElementById('mobileRotateRight').addEventListener('click', () => {
    state.player.angle = normalizeAngle(state.player.angle + Math.PI / 8);
    updateTelemetry();
  });
  document.getElementById('mobileInteract').addEventListener('click', interact);
  document.getElementById('mobileScan').addEventListener('click', scanTarget);
  canvas.addEventListener('pointerdown', () => canvas.focus({ preventScroll: true }));
  canvas.addEventListener('contextmenu', event => event.preventDefault());
}

function init() {
  initStars();
  initParticles();
  bindEvents();
  resizeCanvas();
  renderObjectives();
  addLog('Mission console initialized. Awaiting launch authorization.');
  updateTelemetry();
  requestAnimationFrame(frame);
}

init();
</script>
</body>
</html>"""


@app.get("/")
def index():
    return Response(PAGE, mimetype="text/html; charset=utf-8")


@app.get("/health")
def health():
    return jsonify({
        "status": "ok",
        "application": "KIBO Mission Trainer",
        "mode": "independent educational practice simulator",
        "timestamp": datetime.now(timezone.utc).isoformat()
    })


@app.get("/favicon.ico")
def favicon():
    return Response(status=204)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port= int(__import__("os").environ.get("PORT", "5000")), debug=False)
