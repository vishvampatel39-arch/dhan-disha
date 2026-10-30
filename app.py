import os
import io
import base64
import json
import time
import xml.etree.ElementTree as ET
from email.utils import parsedate_to_datetime
import streamlit as st
try:
    import streamlit.components.v1 as components  # older Streamlit versions
except Exception:
    components = None
import requests
import pandas as pd
import altair as alt
import html

try:
    from packaging.version import Version as _V
    _too_old = _V(st.__version__) < _V("1.40")
except Exception:
    _too_old = False
if _too_old:
    st.set_page_config(page_title="Dhan Disha")
    st.error("Your copy of Streamlit is too old for this app. In the black window type: "
             "py -m pip install --upgrade streamlit   then start the app again.")
    st.stop()

st.set_page_config(page_title="Dhan Disha", page_icon=":material/account_balance:", layout="wide", initial_sidebar_state="auto")
home = st.container(key="home")
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap');
html, body, [class*="css"], .stApp { font-family: 'Poppins', sans-serif; }
.stApp { background: #f8faff; }
.stApp, .stApp p, .stApp label, .stApp li, .stApp h1, .stApp h2, .stApp h3,
.stApp h4, .stMarkdown, [data-testid="stCaptionContainer"] { color: #1f2937; }
#MainMenu, footer, [data-testid="stAppDeployButton"], [data-testid="stToolbarActions"], [data-testid="stMainMenu"], [data-testid="stDecoration"] { display: none; }
[data-testid="stExpandSidebarButton"] { background: #14306b !important; border-radius: 50% !important; width: 40px; height: 40px; box-shadow: 0 4px 14px rgba(20,48,107,.35); transition: transform .2s; }
[data-testid="stExpandSidebarButton"]:hover { transform: scale(1.1); }
[data-testid="stExpandSidebarButton"] * { color: #ffffff !important; }
header { background: transparent !important; }
.block-container { padding-top: 1.5rem; max-width: 1100px; }

.hero { background: linear-gradient(120deg, #14306b 0%, #0d9488 100%);
        border-radius: 22px; padding: 34px 38px; margin-bottom: 22px;
        box-shadow: 0 12px 30px rgba(20,48,107,.30); }
.hero, .hero * { color: #ffffff !important; }
.hero { display: flex; align-items: center; justify-content: space-between; gap: 20px; }
.herotext { flex: 1; } .heroart { flex: 0 0 250px; }
@media (max-width: 760px) { .heroart { display: none; } }
.fgrid { display: grid; grid-template-columns: repeat(auto-fit, minmax(210px, 1fr)); gap: 14px; margin: 6px 0 22px 0; }
.fcard { background: #ffffff; border-radius: 18px; padding: 18px 20px; box-shadow: 0 4px 16px rgba(0,0,0,.07); border-top: 4px solid #14306b; }
.fcard:nth-child(even) { border-top-color: #0d9488; }
.fcard .ic { font-size: 1.8rem; } .fcard b { display: block; margin-top: 6px; color: #1f2937; }
.fcard span { color: #6b7280; font-size: .88rem; }
.score { background: #ffffff; border-radius: 18px; padding: 20px 24px; box-shadow: 0 4px 16px rgba(0,0,0,.08); margin: 12px 0; }
.bar { height: 14px; border-radius: 999px; background: #e5e7eb; overflow: hidden; margin-top: 10px; }
.bar > div { height: 100%; border-radius: 999px; }
.hero { position: relative; overflow: hidden; animation: fadeup .6s ease both; }
.hero::after { content: ''; position: absolute; right: -70px; top: -70px; width: 240px; height: 240px; border-radius: 50%; background: rgba(255,255,255,.08); }
.hero::before { content: ''; position: absolute; left: 35%; bottom: -90px; width: 200px; height: 200px; border-radius: 50%; background: rgba(245,179,1,.12); }
.herotext, .heroart { position: relative; z-index: 1; }
@keyframes fadeup { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: none; } }
.fcard { transition: transform .2s, box-shadow .2s; animation: fadeup .6s ease both; }
.fcard:hover { transform: translateY(-5px); box-shadow: 0 12px 26px rgba(20,48,107,.18); }
.stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 14px; margin: 4px 0 18px 0; }
.stats > div { background: #14306b; border-radius: 16px; padding: 14px 18px; text-align: center; }
.stats b { display: block; font-size: 1.7rem; color: #f5b301 !important; }
.stats span { color: #dbe4ff !important; font-size: .85rem; }
.steps { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 14px; margin: 0 0 22px 0; }
.steps > div { background: #ffffff; border-radius: 16px; padding: 14px 18px; box-shadow: 0 3px 12px rgba(0,0,0,.06); }
.steps i { display: inline-block; width: 28px; height: 28px; line-height: 28px; text-align: center; border-radius: 50%; background: #f5b301; color: #14306b; font-style: normal; font-weight: 700; margin-right: 8px; }
.steps b { color: #1f2937; } .steps span { display: block; color: #6b7280; font-size: .85rem; margin-top: 4px; }
[data-testid="stSidebar"] { background: linear-gradient(180deg, #14306b 0%, #0d4a6b 100%); }
[data-testid="stSidebar"] * { color: #ffffff !important; }
.sb { text-align: center; } .sb h2 { margin: 8px 0 0 0; font-size: 1.5rem; }
.sb p, .sb li { font-size: .85rem; opacity: .92; } .sb ul { text-align: left; padding-left: 20px; }
.sb hr { border-color: rgba(255,255,255,.25); margin: 14px 0; }
.stTabs h3 { border-left: 5px solid #f5b301; padding-left: 12px; color: #14306b !important; margin-top: 8px; }
[data-baseweb="input"], [data-baseweb="select"] > div, [data-baseweb="textarea"] { border-radius: 12px !important; }
[data-testid="stDataFrame"], [data-testid="stDataEditor"] { border-radius: 14px; overflow: hidden; box-shadow: 0 3px 12px rgba(0,0,0,.07); }
[data-testid="stVegaLiteChart"], [data-testid="stArrowVegaLiteChart"] { background: #ffffff; border-radius: 16px; padding: 10px; box-shadow: 0 3px 12px rgba(0,0,0,.07); }
.trust { display: flex; flex-wrap: wrap; gap: 8px 22px; margin: -6px 0 20px 0; }
.trust span { color: #14306b !important; font-weight: 500; font-size: .9rem; }
[data-testid="stSidebar"] [data-testid="stRadioGroup"], [data-testid="stSidebar"] [role="radiogroup"] { gap: 4px; }
[data-testid="stSidebar"] [data-testid="stRadioGroup"], [data-testid="stSidebar"] [data-testid="stRadio"] > div { width: 100%; align-items: stretch !important; }
[data-testid="stSidebar"] [data-testid="stRadioGroup"] > div { width: 100%; }
[data-testid="stSidebar"] [data-testid="stRadio"] label:not([data-testid="stWidgetLabel"]) { display: flex; width: 100%; padding: 10px 14px; border-radius: 12px; cursor: pointer; transition: background .25s, transform .25s, box-shadow .25s; animation: slidein .5s ease both; }
[data-testid="stSidebar"] [data-testid="stRadio"] label:not([data-testid="stWidgetLabel"]) > div:first-child:not([data-testid]), [data-testid="stSidebar"] [data-testid="stRadio"] label:not([data-testid="stWidgetLabel"]) > div > div:first-child:not([data-testid]) { display: none; }
[data-testid="stSidebar"] [data-testid="stRadio"] label:not([data-testid="stWidgetLabel"]):hover { background: rgba(255,255,255,.16); transform: translateX(6px); }
[data-testid="stSidebar"] [data-testid="stRadio"] label:not([data-testid="stWidgetLabel"]):has(input:checked) { background: #f5b301; animation: glow 2.5s ease-in-out infinite; }
[data-testid="stSidebar"] [data-testid="stRadio"] label:not([data-testid="stWidgetLabel"]):has(input:checked) * { color: #14306b !important; font-weight: 600; }
[data-testid="stSidebar"] [data-testid="stRadioGroup"] > div:nth-child(1) label { animation-delay: 0.05s; }
[data-testid="stSidebar"] [data-testid="stRadioGroup"] > div:nth-child(2) label { animation-delay: 0.10s; }
[data-testid="stSidebar"] [data-testid="stRadioGroup"] > div:nth-child(3) label { animation-delay: 0.15s; }
[data-testid="stSidebar"] [data-testid="stRadioGroup"] > div:nth-child(4) label { animation-delay: 0.20s; }
[data-testid="stSidebar"] [data-testid="stRadioGroup"] > div:nth-child(5) label { animation-delay: 0.25s; }
[data-testid="stSidebar"] [data-testid="stRadioGroup"] > div:nth-child(6) label { animation-delay: 0.30s; }
[data-testid="stSidebar"] [data-testid="stRadioGroup"] > div:nth-child(7) label { animation-delay: 0.35s; }
[data-testid="stSidebar"] [data-testid="stRadioGroup"] > div:nth-child(8) label { animation-delay: 0.40s; }
[data-testid="stSidebar"] [data-testid="stRadioGroup"] > div:nth-child(9) label { animation-delay: 0.45s; }
[data-testid="stSidebar"] [data-testid="stRadioGroup"] > div:nth-child(10) label { animation-delay: 0.50s; }
@keyframes shift { 0% { background-position: 0% 50%; } 50% { background-position: 100% 50%; } 100% { background-position: 0% 50%; } }
@keyframes floaty { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-10px); } }
@keyframes grow { from { transform: scaleY(0); } to { transform: scaleY(1); } }
@keyframes fillbar { from { width: 0; } }
@keyframes pop { from { opacity: 0; transform: scale(.92); } to { opacity: 1; transform: none; } }
.hero { background-size: 200% 200%; animation: fadeup .6s ease both, shift 14s ease infinite; }
.heroart svg { animation: floaty 5s ease-in-out infinite; }
.heroart rect { transform-box: fill-box; transform-origin: bottom; animation: grow 1s ease both; }
.heroart rect:nth-of-type(2) { animation-delay: .15s; } .heroart rect:nth-of-type(3) { animation-delay: .3s; } .heroart rect:nth-of-type(4) { animation-delay: .45s; }
.bar > div { animation: fillbar 1.3s ease-out both; }
.score { animation: pop .5s ease both; }
.stats > div { animation: pop .5s ease both; }
.stats > div:nth-child(2) { animation-delay: .1s; } .stats > div:nth-child(3) { animation-delay: .2s; } .stats > div:nth-child(4) { animation-delay: .3s; }
.fcard:nth-child(2) { animation-delay: .05s; } .fcard:nth-child(3) { animation-delay: .1s; } .fcard:nth-child(4) { animation-delay: .15s; }
.fcard:nth-child(5) { animation-delay: .2s; } .fcard:nth-child(6) { animation-delay: .25s; } .fcard:nth-child(7) { animation-delay: .3s; } .fcard:nth-child(8) { animation-delay: .35s; }
[data-testid="stMetric"] { transition: transform .2s, box-shadow .2s; }
[data-testid="stMetric"]:hover { transform: translateY(-3px); box-shadow: 0 10px 22px rgba(20,48,107,.16); }
[class*="st-key-page_"] { animation: fadeup .45s ease both; }
@keyframes slidein { from { opacity: 0; transform: translateX(-22px); } to { opacity: 1; transform: none; } }
@keyframes glow { 0%, 100% { box-shadow: 0 4px 14px rgba(245,179,1,.35); } 50% { box-shadow: 0 4px 24px rgba(245,179,1,.85); } }
@keyframes pulse { 0%, 100% { transform: scale(1); } 50% { transform: scale(1.12); } }
@keyframes drift { 0%, 100% { transform: translate(0, 0); } 50% { transform: translate(-30px, 24px); } }
@keyframes drift2 { 0%, 100% { transform: translate(0, 0); } 50% { transform: translate(34px, -20px); } }
@keyframes draw { from { stroke-dashoffset: 200; } to { stroke-dashoffset: 0; } }
@keyframes bounce { 0%, 100% { transform: translateY(0); } 40% { transform: translateY(-9px); } }
@keyframes sweep { from { left: -40%; } to { left: 110%; } }
@keyframes glowtext { 0%, 100% { text-shadow: 0 0 0 rgba(245,179,1,0); } 50% { text-shadow: 0 0 14px rgba(245,179,1,.9); } }
.hero::after { animation: drift 9s ease-in-out infinite; }
.hero::before { animation: drift2 11s ease-in-out infinite; }
.heroart circle { transform-box: fill-box; transform-origin: center; animation: pulse 2.4s ease-in-out infinite; }
.heroart circle:nth-of-type(2) { animation-delay: .3s; } .heroart circle:nth-of-type(3) { animation-delay: .6s; }
.heroart circle:nth-of-type(4) { animation-delay: .9s; } .heroart circle:nth-of-type(5) { animation-delay: 1.2s; }
.heroart polyline { stroke-dasharray: 200; stroke-dashoffset: 200; animation: draw 1.8s .5s ease forwards; }
.sb svg { animation: floaty 4s ease-in-out infinite; }
.fcard .ic { display: inline-block; }
.fcard:hover .ic { animation: bounce .6s ease; }
.stats b { animation: glowtext 3s ease-in-out infinite; }
.steps i { animation: pulse 2.6s ease-in-out infinite; }
.steps > div:nth-child(2) i { animation-delay: .4s; } .steps > div:nth-child(3) i { animation-delay: .8s; }
.bar > div { position: relative; overflow: hidden; }
.bar > div::after { content: ""; position: absolute; top: 0; bottom: 0; width: 40%; background: linear-gradient(90deg, transparent, rgba(255,255,255,.6), transparent); animation: sweep 2.2s linear infinite; }
[data-testid="stMetric"] { animation: pop .5s ease both; }
[data-testid="stAlert"] { animation: fadeup .5s ease both; }
.stButton > button:active { transform: scale(.96); }
@media (prefers-reduced-motion: reduce) { * { animation-iteration-count: 1 !important; } }
.hero h1 { margin: 0; font-size: 2.3rem; font-weight: 700; }
.hero p { margin: 8px 0 0 0; font-size: 1.05rem; opacity: .95; }
.badges span { display: inline-block; background: rgba(255,255,255,.2);
        border-radius: 999px; padding: 4px 14px; margin: 14px 8px 0 0; font-size: .85rem; }

[data-testid="stMetric"] { background: #ffffff; border-radius: 16px; padding: 16px 20px;
        border-left: 6px solid #f5b301; box-shadow: 0 4px 14px rgba(0,0,0,.07); }
[data-testid="stMetricValue"] { color: #14306b; font-weight: 700; }

.stTabs [data-baseweb="tab-list"] { gap: 8px; flex-wrap: wrap; }
.stTabs [data-baseweb="tab"] { background: #ffffff; border-radius: 999px; padding: 8px 18px;
        box-shadow: 0 2px 8px rgba(0,0,0,.06); height: auto; }
.stTabs [aria-selected="true"] { background: linear-gradient(120deg, #14306b, #0d9488); }
.stTabs [aria-selected="true"] p { color: #ffffff !important; font-weight: 600; }
.stTabs [data-baseweb="tab-highlight"], .stTabs [data-baseweb="tab-border"] { display: none; }

.stButton > button { background: linear-gradient(120deg, #f5b301, #fbbf24); color: #14306b;
        border: none; border-radius: 12px; padding: 10px 26px; font-weight: 600; }
.stButton > button:hover { transform: translateY(-1px); box-shadow: 0 6px 16px rgba(245,179,1,.45); }
[data-testid="stAlert"] { border-radius: 14px; }

.st-key-herobox { background: linear-gradient(120deg, #1747c4 0%, #2f6bff 60%, #4d8bff 100%); background-size: 200% 200%; border-radius: 24px; padding: 34px 38px; margin-bottom: 20px; overflow: hidden; position: relative; box-shadow: 0 14px 34px rgba(23,71,196,.32); animation: fadeup .6s ease both, shift 14s ease infinite; }
.st-key-herobox::after { content: ''; position: absolute; right: -80px; top: -80px; width: 260px; height: 260px; border-radius: 50%; background: rgba(255,255,255,.09); animation: drift 9s ease-in-out infinite; pointer-events: none; }
.st-key-herobox, .st-key-herobox p, .st-key-herobox h1, .st-key-herobox span { color: #ffffff !important; }
.st-key-herobox h1 { font-size: 2.7rem; font-weight: 700; line-height: 1.15; margin: 12px 0 8px 0; padding: 0; }
.st-key-herobox .pill { background: rgba(255,255,255,.18); border-radius: 999px; padding: 5px 14px; font-size: .85rem; display: inline-block; }
.st-key-herobox p.lead { font-size: 1.05rem; opacity: .95; max-width: 520px; }
.badges span { display: inline-block; background: rgba(255,255,255,.18); border-radius: 999px; padding: 4px 14px; margin: 10px 8px 0 0; font-size: .82rem; }
.st-key-cta1 button { background: linear-gradient(120deg, #f5b301, #fbbf24) !important; border: none !important; border-radius: 12px !important; }
.st-key-cta1 button p { color: #14306b !important; font-weight: 600; }
.st-key-cta2 button { background: #ffffff !important; border: none !important; border-radius: 12px !important; }
.st-key-cta2 button p { color: #1747c4 !important; font-weight: 600; }
.mock { position: relative; height: 280px; margin-top: 4px; }
.mmain { position: absolute; inset: 14px 24px 14px 34px; background: #ffffff; border-radius: 18px; padding: 14px 18px; box-shadow: 0 18px 40px rgba(0,0,0,.28); animation: floaty 6s ease-in-out infinite; }
.st-key-herobox .mmain, .st-key-herobox .mmain * { color: #1f2937 !important; }
.mtop i { display: inline-block; width: 9px; height: 9px; border-radius: 50%; background: #d1d5db; margin-right: 5px; }
.mtop i:first-child { background: #f87171; } .mtop i:nth-child(2) { background: #fbbf24; } .mtop i:nth-child(3) { background: #34d399; }
.mmain small { display: block; margin-top: 12px; font-size: .78rem; opacity: .7; }
.mmain .big { font-size: 2.2rem; font-weight: 700; line-height: 1.1; } .mmain .big em { font-size: 1rem; font-style: normal; opacity: .6; }
.mmain svg { width: 100%; height: 80px; margin-top: 10px; }
.mmain rect { transform-box: fill-box; transform-origin: bottom; animation: grow 1s ease both; }
.mmain rect:nth-of-type(2) { animation-delay: .1s; } .mmain rect:nth-of-type(3) { animation-delay: .2s; } .mmain rect:nth-of-type(4) { animation-delay: .3s; } .mmain rect:nth-of-type(5) { animation-delay: .4s; } .mmain rect:nth-of-type(6) { animation-delay: .5s; }
.mchip { position: absolute; background: #ffffff; border-radius: 14px; padding: 8px 14px; font-size: .8rem; box-shadow: 0 10px 24px rgba(0,0,0,.25); animation: floaty 5s ease-in-out infinite; }
.st-key-herobox .mchip, .st-key-herobox .mchip * { color: #14306b !important; }
.mchip.c1 { top: 0; right: 0; } .mchip.c2 { bottom: 34px; left: 0; animation-delay: .8s; } .mchip.c3 { bottom: 0; right: 6px; animation-delay: 1.6s; }
.st-key-herobox .sample { font-size: .7rem; opacity: .7; text-align: center; margin-top: -4px; }
.sec { text-align: center; margin: 28px 0 14px 0; }
.sec > span { color: #2f6bff; font-weight: 600; letter-spacing: .14em; font-size: .78rem; }
.sec h2 { color: #14306b !important; font-size: 1.9rem; font-weight: 700; margin: 4px 0 2px 0; padding: 0; }
.sec > p { color: #6b7280; margin: 0; }
[class*="st-key-tile_"] button { width: 100%; min-height: 112px; background: #ffffff !important; border: 1px solid #e3e9f7 !important; border-radius: 18px !important; box-shadow: 0 4px 16px rgba(20,48,107,.08); transition: transform .2s, box-shadow .2s; animation: pop .5s ease both; }
[class*="st-key-tile_"] button p { color: #14306b !important; font-weight: 600; text-align: center; font-size: .95rem; }
[class*="st-key-tile_"] button:hover { transform: translateY(-5px); box-shadow: 0 14px 28px rgba(47,107,255,.25); border-color: #2f6bff !important; }
.st-key-featband { background: linear-gradient(120deg, #1747c4, #2f6bff); border-radius: 24px; padding: 6px 28px 28px 28px; margin: 24px 0; box-shadow: 0 14px 34px rgba(23,71,196,.25); }
.st-key-featband .sec h2, .st-key-featband .sec h2 *, .st-key-featband .sec > span, .st-key-featband .sec > p { color: #ffffff !important; }
.fc2 { background: #ffffff; border-radius: 16px; overflow: hidden; box-shadow: 0 10px 24px rgba(0,0,0,.2); margin-bottom: 10px; }
.fc2 .top { height: 130px; overflow: hidden; display: flex; align-items: center; justify-content: center; font-size: 3rem; background: linear-gradient(135deg, #e8efff, #fdf3d6); }
.fc2 .body { padding: 14px 16px; } .fc2 b { color: #14306b; display: block; } .fc2 span { color: #6b7280; font-size: .87rem; display: block; margin-top: 4px; }
[class*="st-key-feat_"] button { background: #f5b301 !important; border: none !important; border-radius: 12px !important; }
[class*="st-key-feat_"] button p { color: #14306b !important; font-weight: 600; }
.st-key-lightband { background: #e8f0ff; border-radius: 24px; padding: 4px 28px 26px 28px; margin: 24px 0; }
.t3 { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 14px; }
.t3 > div { background: #ffffff; border-radius: 16px; padding: 18px 20px; box-shadow: 0 3px 12px rgba(0,0,0,.06); animation: pop .5s ease both; }
.t3 .ic { font-size: 1.8rem; } .t3 b { display: block; color: #14306b; margin-top: 6px; } .t3 span { color: #6b7280; font-size: .88rem; }
.st-key-ctaband { background: linear-gradient(120deg, #0b1f4d, #14306b); border-radius: 24px; padding: 30px 34px 22px 34px; margin: 24px 0 8px 0; text-align: center; }
.st-key-ctaband, .st-key-ctaband p, .st-key-ctaband h2, .st-key-ctaband span { color: #ffffff !important; }
.st-key-ctaband h2 { font-size: 1.8rem; margin: 0 0 4px 0; padding: 0; }
.st-key-ctaband small { color: #b8c6ea !important; }
.st-key-cta3 button { background: linear-gradient(120deg, #f5b301, #fbbf24) !important; border: none !important; border-radius: 12px !important; }
.st-key-cta3 button p { color: #14306b !important; font-weight: 700; }
.mmain.mphoto { padding: 0; overflow: hidden; inset: 4px 14px 4px 14px; }
.mmain.mphoto img { width: 100%; height: 100%; object-fit: cover; display: block; }
.fc2 .top img { width: 100%; height: 100%; object-fit: cover; display: block; }
[class*="st-key-tile_"], [class*="st-key-feat_"], [class*="st-key-cta"] { width: 100% !important; }
[class*="st-key-tile_"] button [data-testid="stMarkdownContainer"] { display: flex; flex-direction: column; align-items: center; gap: 4px; width: 100%; }
[class*="st-key-tile_"] button p { white-space: normal !important; overflow: visible !important; text-overflow: clip !important; margin: 0; line-height: 1.25; }
[class*="st-key-tile_"] button [data-testid="stMarkdownContainer"] p:first-child { font-size: 1.8rem; }
.st-key-cta1, .st-key-cta2, .st-key-cta3 { width: auto !important; }
.pbanner { height: 150px; border-radius: 20px; background-size: cover; background-position: center; display: flex; align-items: center; padding: 0 30px; margin-bottom: 16px; box-shadow: 0 10px 26px rgba(20,48,107,.22); animation: fadeup .5s ease both; }
.pbanner h2, .pbanner h2 * { color: #ffffff !important; margin: 0; padding: 0; font-size: 1.9rem; font-weight: 700; text-shadow: 0 2px 10px rgba(0,0,0,.35); }
.gal { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 14px; margin-bottom: 8px; }
.gcard { height: 230px; border-radius: 18px; background-size: cover; background-position: center; position: relative; overflow: hidden; box-shadow: 0 8px 22px rgba(20,48,107,.18); transition: transform .25s, box-shadow .25s; animation: pop .5s ease both; }
.gcard::after { content: ""; position: absolute; inset: 0; background: linear-gradient(180deg, transparent 45%, rgba(11,31,77,.88)); }
.gcard span { position: absolute; left: 16px; right: 12px; bottom: 14px; color: #ffffff !important; font-weight: 600; z-index: 1; }
.gcard:hover { transform: translateY(-6px); box-shadow: 0 16px 32px rgba(47,107,255,.3); }
[data-testid="stMainBlockContainer"] { position: relative; z-index: 1; }
[data-testid="stLayoutWrapper"]:has(> .st-key-bgdots) { position: absolute; width: 0; height: 0; overflow: visible; }
.st-key-bgdots { position: fixed; inset: 0; width: 100vw; height: 100vh; z-index: -1; pointer-events: none; }
.st-key-bgdots, .st-key-bgdots * { pointer-events: none !important; }
.st-key-bgdots [data-testid="stElementContainer"], .st-key-bgdots iframe { width: 100vw !important; height: 100vh !important; border: 0; display: block; }
.st-key-flowband { background: #ffffff; border-radius: 24px; box-shadow: 0 8px 26px rgba(20,48,107,.12); padding: 8px 12px 4px 12px; margin-bottom: 18px; overflow: hidden; animation: fadeup .6s ease both; }
.st-key-flowband iframe { border: 0; border-radius: 18px; display: block; }
.st-key-flowband [data-testid="stCaptionContainer"] { text-align: center; }
@property --a { syntax: '<angle>'; inherits: false; initial-value: 0deg; }
@keyframes hbg { to { --a: 360deg; } }
.st-key-cta1 button, .st-key-cta2 button, .st-key-cta3 button { position: relative; isolation: isolate; background: transparent !important; border: none !important; border-radius: 999px !important; padding: .55rem 1.25rem !important; overflow: visible !important; }
.st-key-cta1 button::before, .st-key-cta2 button::before, .st-key-cta3 button::before { content: ""; position: absolute; inset: -2px; border-radius: inherit; z-index: -2; background: conic-gradient(from var(--a), rgba(255,255,255,0) 0%, rgba(255,255,255,0) 58%, #ffffff 80%, #3275f8 94%, rgba(255,255,255,0) 100%), linear-gradient(rgba(255,255,255,.32), rgba(255,255,255,.32)); filter: blur(1.5px); animation: hbg 2.6s linear infinite; transition: filter .4s; }
.st-key-cta1 button::after, .st-key-cta2 button::after, .st-key-cta3 button::after { content: ""; position: absolute; inset: 2px; border-radius: inherit; background: #0a1a3f; z-index: -1; }
.st-key-cta1 button:hover::before, .st-key-cta2 button:hover::before, .st-key-cta3 button:hover::before { background: radial-gradient(75% 180% at 50% 50%, #3275f8 0%, rgba(255,255,255,.2) 100%); animation: none; filter: blur(4px); }
.st-key-cta1 button p, .st-key-cta2 button p, .st-key-cta3 button p { color: #ffffff !important; font-weight: 600; font-size: .95rem; white-space: nowrap !important; overflow: visible !important; text-overflow: clip !important; }

/* Dhan Disha redesign: clean fintech dashboard */
:root { --navy:#102b52; --orange:#ff6b16; --blue:#2f6bff; --ink:#10264d; --muted:#60799e; }
.stApp { background:linear-gradient(135deg,#f7faff 0%,#f2f7ff 100%) !important; }
.block-container { max-width:1600px !important; padding-top:1rem !important; padding-bottom:2rem !important; }
[data-testid="stSidebar"] { background:linear-gradient(180deg,#ffffff 0%,#f3f7fd 100%) !important; border-right:1px solid #dce8f8; min-width:270px; }
[data-testid="stSidebar"] > div:first-child { padding:1.2rem .9rem; }
.sb { padding:14px 12px 22px !important; margin-bottom:14px !important; border-bottom:1px solid #d9e6f7; text-align:left !important; }
.sb svg { width:46px !important;height:46px !important;display:inline-block;vertical-align:middle;margin-right:8px; }
.sb h2 { display:inline-block !important;vertical-align:middle;font-size:1.45rem !important;color:#102b52 !important;margin:0 !important; }
.sb h2::first-letter { color:#102b52; }
.sb p { color:#7187a8 !important;margin:4px 0 0 54px !important; }
[data-testid="stSidebar"] [role="radiogroup"] { gap:7px !important; }
[data-testid="stSidebar"] [role="radiogroup"] label { border-radius:12px !important;padding:10px 12px !important;border:1px solid transparent !important;transition:all .18s ease; }
[data-testid="stSidebar"] [role="radiogroup"] label:hover { background:#eaf2ff !important;border-color:#d8e7ff !important;transform:translateX(2px); }
[data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked) { background:linear-gradient(90deg,#fff0e5,#eaf2ff) !important;border-color:#ffd7bb !important;box-shadow:inset 3px 0 #ff6b16; }
[data-testid="stSidebar"] [role="radiogroup"] label p { color:#183861 !important;font-weight:500 !important;font-size:.91rem !important; }
[data-testid="stHeader"] { background:transparent !important; }
.st-key-herobox { background:linear-gradient(105deg,#f0f7ff 0%,#ebf4ff 50%,rgba(235,244,255,0) 80%),url(data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAQDAwQDAwQEBAQFBQQFBwsHBwYGBw4KCggLEA4RERAOEA8SFBoWEhMYEw8QFh8XGBsbHR0dERYgIh8cIhocHRz/2wBDAQUFBQcGBw0HBw0cEhASHBwcHBwcHBwcHBwcHBwcHBwcHBwcHBwcHBwcHBwcHBwcHBwcHBwcHBwcHBwcHBwcHBz/wAARCAEmAeIDASIAAhEBAxEB/8QAHwAAAQUBAQEBAQEAAAAAAAAAAAECAwQFBgcICQoL/8QAtRAAAgEDAwIEAwUFBAQAAAF9AQIDAAQRBRIhMUEGE1FhByJxFDKBkaEII0KxwRVS0fAkM2JyggkKFhcYGRolJicoKSo0NTY3ODk6Q0RFRkdISUpTVFVWV1hZWmNkZWZnaGlqc3R1dnd4eXqDhIWGh4iJipKTlJWWl5iZmqKjpKWmp6ipqrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uHi4+Tl5ufo6erx8vP09fb3+Pn6/8QAHwEAAwEBAQEBAQEBAQAAAAAAAAECAwQFBgcICQoL/8QAtREAAgECBAQDBAcFBAQAAQJ3AAECAxEEBSExBhJBUQdhcRMiMoEIFEKRobHBCSMzUvAVYnLRChYkNOEl8RcYGRomJygpKjU2Nzg5OkNERUZHSElKU1RVVldYWVpjZGVmZ2hpanN0dXZ3eHl6goOEhYaHiImKkpOUlZaXmJmaoqOkpaanqKmqsrO0tba3uLm6wsPExcbHyMnK0tPU1dbX2Nna4uPk5ebn6Onq8vP09fb3+Pn6/9oADAMBAAIRAxEAPwD7iy3qfzoy3qfzp+3ik24rrOYYc+p/OjJ9T+dONGOKAG7m/vH86Qlv7x/OnUmKAE3N/eP50mW/vH86WigBCzf3j+dIWb+8350tIaYhA7/3m/Ok8x/7zfnSkd6aaYAZH/vt+dNMjj+NvzpTimEUaC1FMsn99vzphlk/56N+ZpcU0/lTFdjTNL/z0f8A76NIZpcY8x/++jS9qYRVKwtRDNN/z0f/AL6NNM8o/wCWr/8AfRoIphqkkS7i+fN/z1k/76NNNxN/z1k/76NIRSEetVoK7D7RN/z2k/76NBuJj/y1k/76NNIpMYp2QrsU3E+f9dJ/30ab9on/AOe0n/fRpp60hBNOyFdjjcTc/vpP++jTDPNn/Wyf99Ggg03ZTVhXYGWb/nrJ/wB9GmmWXvI//fRpdtKVz1p6AR+bJ/ff/vo0nmPn77fmacU5oK09BWGF3P8AE3500s/95vzqQjFNIp3ERln/ALzfmaaS/wDeb86lNNIzTuKxHvb+8350hdv7zfnTytIVzTuIZuf+835mkLv/AHm/M04qaaVqhEZZ/wC+350wyP8A32/OpGGKjPNMTG72/vt+dIWY/wATfmaXbS4pkkJL5+8350m5/wC+35mp9hboM0xkweRzTugsxm5sfeb86aWY9Wb86fg001QtSPLD+NvzNIXf+8351JtzTSuKdwItzZ++351IrsR95sfWkEZJFKV2nFDYJCNI3Zm/OlDuByzfnRwKRqBXGyOx7n86hO7rub86m4pMVa0J3GbmA+8fzpjOx/ib86kIpPLzzRcQxZJEYEO4I6EMeK6vw54mmFxHaXjmSOQ7UkY8qewJ7iuY2U9RsIYcEHIrOrCNSNmjSnOUHdHrlFOjXdGjHqQCaK8C57RR20hFSU01qZWG7aNtO/GjFAhmKTFPpMUwGYpCKfikIzQAwikxmpCKTFFxEeKQipMU00wGEYphHpUpFNIpiIyKaR+dSkCmkGmmKxCRTSKlIpCvFUKxARTSKlINMK1SZJERSGpSOKbtp3FYixRt96kxSEU7isRFaQipSKbincViMjmkwKk20BeaLhYiI5pNuamK0YouFiHbRtqYrSEU7isQFKb5ftU+2kZafMFiuVxSYqUrzSbaaYrEJXmmkVOUxTSlPmFYhIpCuRU2ynRQtPIsUYy7UOaSuxKN9ioydai2itk6Syoxkfa+eAOarvp2B8rc+9SsRB7Mt0J9jPZPWr9rpm6PzJlOD0HTioFhkZygRiw6gDNdJKc2qsRtZgOD2NY4mu4pKPU1w9FSbcuhiTlFURoMAegqnJEGIOKuSIdxzULL1xTpzstCpxvuUJITklenpUHBrRZapvEVc56GuqnUvoctSnbVEXH4UAZNSFO1KI8DmtHKxmokR+WoSCxNWmAxTPpRGQOJX24NBFSkU3FXchoj20u2pNtG2ncLEeygJUoXvShaXMFiLZSFetT4pGXANHMOx6pD/qo/90UU2E/uo/8AdFFeC9z2EV6Q0tH1rQgSilooENIoIpeaKAsIFpMU4iigLDSKQinY60EUXEREUhGKlxSYp3AjIphFTFaaR1p3CxFimmpCKaR+VMkj70EU/ApMc07gRMKYVqcimladxWICKbipiKTaKdybEJWgrUlFO4WISlJtqakK0cwWIduKMYqQrmjbRcViPFBFSYpNtHMFiMLSFamxSEUXCxDtpu2pitG2nzCsVyvNAWpytNIp8wWIttJ5dS4pRRzBYr+UWbCgkngCuktrcW1vGoUAgc+ue9ZVqywzxyEZCmtwTRypuRgwrgxs5NJLY68LFJt9TOuhubOc1UdcdqvSK0jdOarzIVOOtY06iSSOicL6lRJGhZmQgFuvvUs0pmweenSg25K5JAHvRtESHJpyqRbutwjB2s9inJGevSqrrg1dmYE47VVcc100pt7mM4ogPJ6VE8ZZ8Yqxgim4Oa6Y1LO5hKnfQgMIGMN9ahkBBIPNXCtMkTKmtIVNdTOdPTQospNJtqzsoKV08xyWKpQ0COrOw0m3FPmDlINmKAgqYrQsbNyOg7mk523BRu9BgSgpUmB9fen7MjnijmHylYLQVyDUrAZ4FN2GmmKx6XCP3Mf+6P5UURY8tOeworxnueqitil6daKU9a0IExmilopXASkp1J1oCwlFLijFFwsJjNKRRilouOw3bSYp+KQ0XCwwjNNKmpKM0XCxDt9aaUqfAP1pcCjmFylQijbVhkFRsuOlVzEuJCRTalwCaQqKdxWIitNIqXFJtzTuKxDjNGMVKVpNtLmCxHSEZqXyycdvc0m3Bpcw+Ui20Y9al20m2nzBYjxRtp+KcADS5g5SErRtFSlRQRijmDlINlAXAqYjNNxT5gsREDGKAtSEcU0LRzCsLFbtO+1Me59KuLp8USHeSx9elTaeirEXH3icGpJ27CuCviJc3LFnXRox3aM6OzUzEMx8vt61dijit0bYTg9STUW0npUbk5wTkCueVadTRs6I0Yx1SJvMBzg1AzBmPFJ0pjSAtgVFrGq1I5WFV5CSKlkYA1AzZ4reDM5IruTTMZqUjJph4zXRGZk4iYGKYQKUtk0ZzWiZm0MxTHPUCpCDUZWt6TV9TCre3uke00qxs5wqkn0AzU3kuqByp2noa3NOhWC2DFSsjctnrV18XGlDmWplRwzqSs9DANtIqbipA9+tQlcVtXA3uzM2BnpVSRIiRlSSPfGamli3LdF1MKlsylDA8hJVcgflVl4x5YEhANOedgu1AEA7CqxyxyeprRqVR3ehmnGmrLUY7Kv3Vz7mo+Sc1P5eaettkbifwrbmjBGVnNlcLntT/KJHSp9uOAKfgkc8VPtR+zO0iz5afQUUsX+rT6CiuFs7ERYxQRS0lMQlGKdSHmi4CYoxS4oouAuKTGKWikMSjHrTqBSuAmKQ06kJoGNI9aNopaTvRcBCPSkIx3p2c0baLhYbmjaCaCuDTCSKXoANGO1QlTUu45zQSTQnJA7Mi2UbKmJXuMfSkxnpRzi5SArRtqbB9KQrT5hcpFtpcAdRT8U0ilcdrDCFx3zTdtSbSe1KVxwaSklpcdmRBKUJngCpMUdKbkJIYUx1pjLzxU3vTW59KXMwsiAg1MtqxwWIA/WpreNSxJ7dBTp5SvC/nWFau0+WJtSpJ6sqGIAkA/nUbLjihnOakjdCPnBJ9qI1mviKlQT+EdbyPEcENsPtVuTnmlWQMoIGB6VE0wyQpBrkq1FN3sa04OOgyV8L7VRkkw3Bq3JIGB3CqMgBY4NTFo2sKJ85BqNn/OmEU0itLIWojyEim596CpPem+XVJpBZgWqN+afgk460CMscDrVKokQ4EOKeIyqhiOD0qwINvBIzUpWIjlycDtT9q+guRdSkVqe0s/tEwDZ2DlqlSSEA/L+Bq7YzAs6hQBjPFXOc1BtIzXLzJCzKsSgenSqTXEgJwxxVu6LOMms985rKhFNamlRtbEUjEnPrURJJ5qWmkCvRhZbHHK7G43UghZjgDNWIVAycZqYk9uPpV+0aVkYygm9SFIFRgSen86VsZwAAPapGjYYJHWk2DvUJ82rdynpolYrsD2FMK+tWyoxUbR1qppGTi2dbEf3Sf7oopsX+qT/dFFYm42ilxSYoELRQDQaBhRS0lILCUtLikoGJS0Yo6UgCkxTqPalcdhvQ0UpGKQ0XHYM0mRSGmkGoY0POGFN8vI5NIu6nhmrNylHQ05U9SLbg0mPSp/qOaQqPSn7Yn2ZARQKkK80YxVc9yeWw3rSge2aSnqcCs5zsioxuyJhTVUZ56VMcH60hQ4qfaXRXJqNPI44NIO+ea4r4mfFXw18JNIh1DxJdSxC58xbWCGJne4dV3FRgYHbk4HNfHOuft0eMrjXBcaRo+kWejxvxaTo00ki+jyZGD/ugVpSozqK8VoTUqxg7M++itIV6V84/Bn9rTSfiLcRaTrtimlaw5wskMm6CTPfnlew7jmvpAY7ms3WSk4S0aL9jKyktnsRkZOKUwkDORTy6jqKZ54Jx0qHXe8Rqj3FjQhg3ao5y2Sc5FEk4UYB5qv5rc88elZSk5u7NoQ5UNbmhSF7ZppJqNiaq62HZk73DMMdPpUW854PNMAJNTIkQHLE/SobS0KSGM5Y802rLIrD5RhfrR5MY+8/JrPnsVbuVduaX7Ox6DOasiFAf9YPyqZREg65PrSc5MLxRSNk4GcAn0FNltmjXLEfhV15WY4BIFRowBIYZBo5Zb3Ep+RmFSDxTtzYx0+laRSIn7n60xlXPCAH3q031QNoz8cUiwsx4q6I13ZI5qZY8qTwB71uqltzFq+xSS2CHPU1ZFlJxJuCfzqWNR5i8ginXMp+6KJV3ookxpXd5CZUptL5PcmqFxKu4qgBHrQ7sCfeqz/WnShrdlzelkRuTTQTigntRnjFd8XocjRZF4I1UIgPHJNTfaFaMtgbvSs/FKQQOKh0o7rcak+pK8rk/eNSQuzA57d6q5NSLu245xVpJIiV5MnkuEQYHJpgud3UcU37M7LuAyDUiWbEc8VK5Vu7jd+isdbEo8pP90UURH90n+6KKogZQaKQ0wDpRRS0hiZpc0lFIBc80YoooAKKKQmkMWlpuaUVLKA0mKWjNQykNC5NLtFKaMcVDZVhMDtSHIpxwDyaQEdjUOQ7CUhpcZpp4p3QrMM00tS59KaQT6VDkilFhuApvmAk80jo7dOlM8tvSsXuapaDs5bhuKkRwWC56nFVzG/SoZEkXkA8VPNyl8tz8rfjt8Rbz4gfEzxJqFxPM1pHeS29pDIxxDDGxRVC9Bnbk47k15c+1umd2M8HvXsH7Uvw/uPAnxh1qRYGj0vXXOp2b4+U7+ZVHusm7j0Irx5F7mvo6U1OCcdjxpw5ZNM674aWl7qHjTRbSwXffXFysUKbsb3bgLnPAOcV+uemWNzZaZZW93MJruGCOOaQZw7hQGP4kGvzj+BPgWzu/EXhHUJgzrLcyxXW18MN6hECjsRuLZ9SPSv0niiFtbw26vI6wosYaRizMAMZLHqeOTXh4qpTq1210VvxZ7EKVWhQjGfV3/BDCpppQH1qUim49Kxshc7ITDz1oEQqfBpu2ly+Y+caI09abJCmOM/hUg4pKjlt1KUiqwA6KR9aZmruMio2iB7CjmsUncqhzyO1SImTwak8gVIAEUZIFS5pjvbYYFwOetLt5xTlw+dpBx6UkkgiO3GTjk5qXUsieW7I3cR5HO79KiWbn5unrTGOSaYaz9p1N1TViyJ1DY7etOEivnB6VR71LFE7SheVNJVWDpRRZ25NLcMV+UfdqKW5aM7UIKr39aimu/MAAGPWr1kQo2dxBKiuPmI9xSyXKyAnPI9aqHk5oMZxnHFdUYwXUl81xzy5qMmgISaftA6mumM0jCUGyHZk0vln0qdSuQCv45rTiijVflHB705Yjl6E+yMdI9xxU4t8DkE1oN5MPJUDPtSCRZFyD+FJ1ZPXoJRSKcdoC2WGBVgQqBwoAp7MqdSBUAuyH5Hy/ypKTkDTRNtxS4zmoftSliOg7GnCTIODmhya6E+zT6nQR/wCrT6CimR58tPoKK7zlDpSUUmaAHdKSk/Gl6UgQd6KKKQxaKQHJpaTGHakBpe1JUsaDNKKbx6UvFTcoXOKQnNFJkVLY0g3Y600y+lLTSoPes3bqWkMZs9+aNxHelKUhWndDsOWXs1PyDnBqEqPSjBHTis2uxRLmkqIbgetSB6zbsOwuaTNHXpXJ/EP4g6R8MvDFx4h1szmyhkjh2W6b5Hd2wAB+Z59KSvJ2igbUVdnWCl8vd1rM0LxFpniLQbPXdOvI59Ku4RcR3GdqlMdTnpjBznpg14On7TFx4o8cy6R4T061OhWKNJcahdhmknAO0eWgICgseC2TgdBW1HC1KzskZVK8Kau2Vf2xvhjpvi3wZp+uSXU1vrWlzC2s1+9FMJWBdWHXICbgR6Ec5r4isPhpcrqKLfXEDWiHLrETuf25HA9a+zvFGvyXf2rUdU1SWOFSZJJJJtkcQ/kor5+8S/F3T57z7NpWijU4i237ReyOjyn/AKZqvzD2LHJ9BXpLB14Q5YSX9eZhDF4dyTqQb87/AKHsHwM8IX//AAm+h3X9n3H9mqPtZlWBhBGQhC/P90nhehr7B28V8+/Bf4ra9caTY6Trngi50mztoxHBcLexudg6bo2Kv+QJ9q91ttTtrtykM6NIF3FM/MB7jqK8D2NSi37Vas9fEYqOJknT2WxbIox7Um/IpGGe9PmRhYXFIcetNJPrmo33HocVLqFKI8mjJBpmWx2zSbmHf9KhyKUSc5IPO0U3Of8AGoGkJ9aaGDdU/WsnOw1EladFOCcn1FUppGkJOfoKnwh6oPzpNqZ+4MemajnNIpIrozA8Eg085B5BB96kO3PEagelSpLtBAXr6nNZuoNy7IrYzgDrSNH+FXEdwcgKPwqYuxBBVT9RU8yZPtGikkezGwF3PcL0pzR3bA9ce+KsFpAc7qryySfe3GnzpApNsgNpNjlf1pv2YHguob0od2Ykkkk0zNCrdjVXe4ogUE5cfgKUQjOQxxSA4pwfitFWYuUeI0APr61DtjU8mnE7gRnFJ5QPet6Va25MoXGK0e7o1TNMzcKSFHSm+Uo71KqLjpW6rxvdmTpshd3k5PamBfrV5VXsKzf7e0k3jWY1C3FyvBQtjn0z0zWsarlpBGcoRj8TLJUv2OfU0v2fI5IFT7BRtAqFXaK9miv9lXGSxxUqRqg4zT80o6UnVcuocluhtRf6pOewop0ePLT6CivZseUR0hpcikJpgGaM0maD1oGhc0lFJSGKKWm5p2aljQuaKTNL+NSykJQaWkqGykgpMUuaTNZtlKIlFLmmkVDkWoi00mkNMWZXJUMCRWd32Ksh2cUbjiik6VDkVYXr2pMCgmmFsVLkVyj922vH/wBobxb4Tsfh7rmha/dw/a9Us5EtbQLvlMmPkkC/whWAO446V2fxF8cWvw+8Gat4huQj/Y4/3MLNjzpm4RPxYj8M1+bPiPxFqPijWLzWNWuXub+8cySyMe/YAdlA4A7AV6WXYN13zt2ijz8divY2jFas9n8SftFRz/DoeB/C+jHSrEWSWIu57gbwgADEIgwC2DnJP3jXhWkamNGkvVl+03QmQBGtL6S2CuCSGO0ZbGeAelVmmj24EMQPdgCWP5msu+1BI8LEymRu/ZfevehQp048qWh5DrTqS5nubWveKPE/i+TS9Mu7v7WAVhggBCB36B3/ALzf7R/Cvdvhh8N7HwkqahdlLzWmHM5Hyw+0YPT/AHup9q+bNKyNRsyjEym4iw+ec7xX2PpkjSWobjIJGamWjNIK6OkjuwpXyiBKxwp9Peuu8La82k3SqWBhc/MW6g+uf515KdTZrvbHJsKqR7g5rUtNSvAf3cqSAdmGf5c1y1qUK0HCWzOilOVKSkj6nt5o7mBJUPDdvQ9xUhryjwB4snNwtrdtgOMYDZz7jvkd89vpXqVvPFd28dxBKk0Eo3JJGwZWHqCOtfL1acqU3CS1X4+Z7cZRnFSjsxxphOKkIphrnZohhNJye9KRTCKybZSAg00ggc07HtTSKhspDN2e9LupTx0pN7ev5ispSsUKMGpUT0qNSc9B+VWYWxxgY+lKLTdmRJtD0jJICjJqwLQ45bn2FWIECxg45bmpMcV6dLBx5VKWtzjlVd9DPlhaMZPK+oqqwzxjithgCCKy5cxSMoJAHSuXFUlS1WxrSm3oUZIiGIwcfSo/JcjIU4FWpJGz941AzNg5YgfWuO6OuMmQvFIBjhfrUex84LDFTYzzSEU1KxomMEXPLE1KAAMCkBxSFwOtaKbE9R/Q0jyrEjO7KqKMlmOABXHeLfGo0SRLazWOW6zly/3UHp9a5i78ZX+r2MiTeTFCSFKxggsc55yelehTwVWUFUeiZzPEQ53DqjovEviz7UotdOmZYv45V4Lew9BXmd1cCS5kYHIJwPers0hWGRd+HflmP8K/4muekuRvOz7o6E9cV9DldGMG2jy8xm3GKOv0Hx3f6HLHG7tc2IODCx5A/wBknp/KvXNH1+x1yBZbO4WTPVCcOp9CvWvnVJA/Xr61YhdoXV1Yq6nIZTgj8a2xeW0q75l7rOfD42pS0eqPobUNe0zTARc3cayDrGvzP+Qqe3vLe9gE1tMk0LdGQ9/Q+hrwJL3jk/Meee9XdP8AEd7o8rS2ku0t95CMq31Fck8mXJ7kve/A6IZk+b3lofSMX+qT/dFFNtfntoWJ5KA/pRV7E2EzQDRmkqhC5oJphOKQuKLAPoNR76TcR3osFySlqLzPamG4CnFLlY7osZNKpqsZtw6jFM3EHg4qeRj5i6SFGSahNwAemRVcsT1NMLHNCpLqPn7FpbgM2CMVJkHkVQ3c07zSpJU4zWVSj2NIVO5cJxSGVVUksMVQYserE596hYkVKw992U6tuhPPcmQELwv6mqqtsYH0pGYgGoy9dMYKKsjFybdy+t2VOGO4HoalF1GSPm5NZmVPGTtP6UYK9fzrkeHjJ66HR7Ro0HuVB+UZ96kVxJ2NZy3O3qMmuC+Nd74pf4eX9v4OHl6rcSJHLcrMITbW3LSyByePlXGRyN2RzSjhk2ojlVsuY+dv20vHJm8RaJ4WtryM2dhCbu5jjkB/0hiVVXAPBVATg/36+aYdU02HSLmW63y3jv5VuBLtVOMlz69celLJf+epdnf5/myyMc55zn/GqMksTk7pEz719BHD+zpqlGVrHgSr89R1JR3KNxqUcikGZCPZqoJmUvK3HYD0FW75AzKoX5Tk5IxnHpUUYUQqGYKuMsT6VU21qyoJbI2/Btu0+v6PGRndcq5HsCT/AEr660sldNUFmUnPKnBFfKHgCVf+EqscnJAkcZ9kOK+lrW9NxbQKjNtmGCFOCGHBrKpK0bm1NXlYz9ZeWCe4vxKGt7VczyMQi4JwFJzyxJAHck11l5pk/h2/uLPVojay2ieZMJGyqJjO7cDgrjv9fSvNoftPxQ+I3gvRtLiJ8C2muJHPdIfl1C5iUzSY9Y0RdoPq+e4r7V8Q+FdD8TyLcalp9vNdohSOaQE7QckBlzhwCc4YEV5McTUU27advyPRlRpuKXXufINx47m1S626c72mlxnIK/K9wfVvRP8AZ79/Svp34T/EbRda0G10qNLXTruyXYLWMBIyvXKDsPaviHXrXXvAuv3Gj+JbRrS5WRtsmzZDMMn542+6UPUY6dOOlbunahNC6TQStG68hlOCK8+vfEPmbtL+tD2IYeNKHJvHe6/M/Q7cD1qCa6SMHnc3oK+cPAXxgnihjtNTnYBON7ZZCPcdV+oz9K9z069g1awgvbaRJIJlyrIwYe4yK5qFPmnyVNH+fz/pmdek6aUou6f9bGvFdrIcN8p/SrHWsjO2pY7l0/i49DWtbCLeBjGd9DQNNNU1vWUkN84oN1vPB2+1ccsLO5rHUtMyqcE0u0dapZ5JpyzMvAP4Gs5YfQ15dNC+vHSplkKjt+VZ63DjsDUb6k6n5QprL2UkQ6TkdFbzBo8kgbeuakjuYpiQjqxHoa46W5lmJLOceg6VJ5zRkFWIYdwa6FjJ00o2uS8F5nXkisu7dQ7OSAvTJrJGpzyja0zfSopJsrgkt9TU1qrrpJIKeFcHqy5PMick5PoKzLq5MiMCcL6UyR8dT+AqjPISemB6U8PhfeTZu+WC8yaG+kt+nzJ/dNWotXhYHzAUPbHOa53+0baWRo1uIt6nBXcMiqV9q9vZpneJG/uxkE/jXrPBU6u61OB1nHqdpHqlq45k2n0YVzWreMGguGSyhjlhXjzHJ+Y+3tXMSa5NfEqF8u36kA8sPc+lY19qe2NnXgtlVHpWcMvpe0cYq5TryUeZ6GdeTvqN+8kjnDEszH9TUsJEzBgNttF0B7/WssSPM5RASW6gd6ub3aExREBF+8/bNepiYqCUb2t+Hn/kcOHk5Nyt/wAHyFvJfNjMKMGkkOWx2rClKxzMqvuUcbsYqzeXJgBjhYjByzd2Pv8A4Vmljksc5PPNdeDi0rrZnLjJpu3UupIPXirUToUI3Hf29BWVHIUYMADjselWJ50cK0Q2H+JR0H0rrkr6HHGSWpaacbTz92nCXeCQcj2rJd3kYgmnqJEUkZH41exF+x9l2cP+iW/P/LNf5UVLZ/8AHpb/APXNf5UV4bep7CWhTzTSaaWppat7GNxSabRv9qRn4p2AXtTGbb3qNmPY1EzGmkJsc855HSmbgw60xuBk8VC0igZ3DFUkK5Y4o80r0rPl1Dbwoz7mqc93JIMFiB6Diq5Gxc6RtG9hUgO6qx7E1NkEZyCPauQd8c96tw6g23KnJHVTUVI8uvQunLm0N2SdE4zk+1QfawW54FZf9qwlnDEIB3J61KkqyAFTkHuKEkNtmkLj+6c07zQR71ky3EcTBWkVWPQE4NUJNet4SQJC59F/xpeyvsJVLbnRH5qZgDrXNHxLMCSsCbe3JzWV/b19BJLL5wZpOoYZH4DtSdCp0LVaHU7nj1qG5vI7YYZuf7o61xv/AAlU8vyviP3QdaQa1a7WaSVhjklgaaw8vtideP2Dpn1a325y4P8AdxzXD/FPxA1t8NvF8sUbo66VchWJ6ExkZ/Wtg3sKEBgQD34Ncv8AElINf8AeJ9LhuRHNdafMiNtJ+YKWA/Hbj8auFGKdyJ1pNH5/q4hQDPCiopJ1JzWe2oJLjkDcAcZ9aC54IPAr1XPseUodxt1J5lwf9le9UQgdIySSABx2qabJnUD+NcZ9MVCkiiMKQeOOBnNZN3eprFWRveCZ0h8WWJdgqssi5JwOUP8AhXfXXiG58cagPC2g3Dx2BP8AxMtRi/hjzyiH1bpnv24zXkthpb6zqdrZBxF9pk2b2GQg7kj6V9GeGPDdj4W0lbW0iOCMttIMkz49f736AVhLXR7G8e6Pof4X+HPDOk6V4XhtJLW3vdHhupre1E6h1SXCNIyk56AfN711fiX4g6D4YtXudS12yt41zx5wdj7BVyTX5+fFDxhDqHitJtMlU3MNkltezWshMczKei88hVwuejEVxk2oT3ir5s8kigcbmJAHtXm0cHUS1aO+riad9E2fVXxG/ay0q6tptN0TQYdWjOQZdVQNB9RFzn8SK+cx8Q9YbUbm6K2Kxztu+yx24jhi9kVcbR9K5ggGoJZVjzz06n0rpWEpJe8rmSxdVfA7eh6bo/jzWNUu1tLW3thOysyqGbL7VLbVz/EQDgdzX1h+y5r93qmi68s8zPCssLoCflBZWyRz3AFfDXge8ki8V6LMDiQXsBXB/wCmi8V97/Cm3tPAHhqXSp2D3El1LO8kS5GC2EX8FA/WuCrh066jTVklf81/kejTxb+rydV3b0/JnthY9aYT71xkvimwRDKl8iAcEbsH8utWbDxGLth5N1DMPTIJ/wAauVGSMY1os6nkd6fvIHzdKyX1l1HEaZ/GqM2rXEhPz4U9h0rF0WbxqnRmTaMg7R79Kab3aOm4+vauXW7k7saf9qcEEMR+Nc86Fzqp1UdC11I/U4HoKQOT0rGTUmH38Ee1DasobCglfWuaVJ7WOpTj3NwyBV5NMec5+Ubh61ki8EnI+b6HmlkvSB8mVYdjWLw93qVzovNPjqrA+oo/tRU4aRCPQ1iXF7JIpBY4rOkcry7bVP51vChGCuzKVVy0R0d1rdnCpJfn0UZNYWqa8Htm8jcgPBY8EewrKkdHl+b5UqpeF7jgYCDp6CunkTaWy6nL7S13v2MmaUNOSB8vQCkFrl98i5PZOgH1/wAKs7I4SSCDJjOT1/AVly6tHvaITIrA4IJxmvQU5VI8lLRHnNKEuapuaEl6sSFAef4iP5Vlusl452DCLxk9AKVtmN8r7I/X1pl1ra2HyDbHCB8p61MZQpP2dHWTHLmmuerpFEsqx2alCSEIyVH3pD7nsPaqC3xEZDfw5KqOlUrvVI2zI8owf4iaovfxCMy7wY84yPX0rphhYcv7x3ZzTxM+b92rItNlicnOeaZdSLbW5uJyVhXC7scD0FEdxAr7ZXIfbu2+g9SfSub8Vau1zp8caTAW+/KRDv7mksZGpVjSo666vp8u7/AiWGcKcqlXTTbqdIlxbzIhimjfeMqAwyfwp4QkjHWvJUmIkBBIPqDgiuxsvGNxa2scZijkmVhmZj95fTHr716cqcl8Op5kakW/e0Om1ORrDTL26wQ0MLOMDJBA64q80ieQpf5SVBP5V5t468XNf6DeW6wPEJF+R0fkMDnBHpjNP8MeJraLw9ZpdXbyTRrh1JZ3U5PBPrWCc+d3XY0coWVmfoPZSf6Hb8/8s1/lRUVgCbG2PrEv8hRXlvc9dFYmmk4pc0xiK6DEGNRtJt702Qbe9Vm681SRLdiVpVJxn8ajeXB45qJuKieTiqUSeYfLKWGCfwqlM+eBSyS1C8uBweapRsJu5E+QCTVd3wCM1I7c9etU536+1aJENjJZM96qmYh+WIHqO1EknHFVJnBxjrjmqtfQSlbUkuJ8jzA2H6MPX3qq2pOsZRXZM9wagmlA6sB9aoTu2wEEFexpeyj1H7WXQu/bASdxOT3JprTBhWJNcMnU8VE19sQndgDnJrRQkZuaNw3hiXl8Aep4rmrfxdFqWuXFkpkjSFCpWVAoDA9c55B7VjXnijRtdsJ7U6hCI5l2MS20rnocH3FcrGn/AAiniaO1k1XzYDF5srSKMDOTsxk4z2NceO51TvB2fcKdZKavqj1XztxyCCPUGo7i9CbIzn94cFhghcev17VzsXi63dftU80dvbFiqROR2zx1+9ntXPaj8Q9LtQyrPLcuM5MaYyefU471wUs0niFGnSTck7Npaeeux2PDxh77ej2PRbnUUbiNm9yT1qi1xIzbg5yK8X1P4oX80yfYIY7aNGy3mtvLj0PoPpzVHV/irqTQRm1n+zybiHQBSPwbr+FelerSUYRi5N9br8f+GMbQneUpW8rMxviF+zzqMupXWpeFhbT2czGQ2DyiN4ieSELcMuegyCOnNeM+I/C+r+EpooNa0260+WZS0YnGBIoOCVIOCM+lepap8UfENwGVtUkRfSMhB+leZ+LtWu9faKS5uZLiWHIUu2cA9QPyFawddfxEkvJtv8kRKNL7Lb+Vv1ZzaXSRPuBG7pyacb6FmGGC56jPArPmt36mNvyqFP3Z5Uj8KPaMPZpnqngzVPDfh6X7fe6h597tKokMTMIweuOOSfWneM/iXLrVnLp+kQNZWUgKyzMQJpV7qMcIp79Seme1eaxzqBwRT2uAcDPFNtPcFG2wyOPynJ9BgD0A/wDr1KJ/KRQetM5k4XJJ9Kt6RZwXWtWFteF2inuI4nWJgDhmAPzHp1rGpVjTV2bU6UqjSRb8P6NqvivU4tN0mzlu7uXpHGOg9WJ4Vfc4FSeL/DVz4W8R32hXU1vNc2DhJGt2LR7yoJAJAzjOM+1fZHh/RtI8HWTWOjWMVpAD8xTlpD6sx5Y/Wvk34pysvxM8Sls/PdF+fRlU/wBacG370tmRzxbcI9CL4d2Ak8b+Hkf5i19CP/HxX2Q0z72O85JJ618lfCYrc/ETw6hHCXPmH6KrN/Svqln3YwefrWdNr6xPyivzkaVv4EPNy/KJZ3FiSxyfU1atLv7PKrbcqDyO9c4bmeKaTc+0pzz0xVwaunXygRjs3euuUeZWtdM4Y1FF3vZndQeJ5beQK8u+2xnD9QPY1qW3iS0nUvIzRAd2GR+leZJq6SxrBMNpyfnXt6VHHfvErLG5Bz19K4ng5pWT2O6OOV1fY9d/4SKwRoUS5R2mbaiqc5P9KsjVoCeVx9K8VW6ke5jl3BGVshgOnvW3Z6qbK8DuCpf7+05Rx7j+tZVsK4va+hvRx1/I9WW7tpwA0hUfSrkUUEyfJNG3/AsH9a4ca3axhWfPlkgHawBGfTPWux0uXwzMGMl/KXRSxSQbCcenHNeTOrTUbptfI9SM5N62ZbGnOT8nP0YGlNvdoMMo2DrvIwKyZPGel25xaWkMZ/haT5mqheeJW1JgXvcKOgxgCsJyqvZfh/kaxqQXU2bq4jiGEMbP3ZRwPpnrWXLIjEs8gz6k1mSBbtwqXbsT1A4qJraNN0TbWz3M2GohdLV6+n+Yp1LvbT1G3+sW9sfk2tjqTz+QqvLqy3dvmAMxbjpjFOOmxuTl4kX0BLH86Y+mxIcmclB/CnGK356Fldu6ME6t3orHL6mtwsy8ESnP3Tk/iazn02XfvupPLX+6OWNdXdOkeY7YIjev3mNZE9qTkySAZ7k5J/AV6lLFScVFPlX4/wBfeeVVpwUm3735FGS7jtoQkKFQP77bifwrDvruSfCs5KqSQPTNbr6cJOfMPpjHSqlzpsMX3ySc4AJA5q4zw2H957/iZSlXradPwMcefNb7cnyEOPbP9TVuFRb5jjJkZvmdz90H2HrSTSpbJggkLnagrMmnv7hWCq0aHjAGBXJPnxsWtIwv950UqkcPJPdk17dwhfncmPcR5UXJkPPU1zupXcd7M7SRsjgbUUNwo9K0J4l0+2wzuhf70mPmY+gHYVz23dcAAkqW7nnFduBpU6XNO+i2ZzY3ESqWj33GMu0Egg46j0pouTHx2psEkd6pljysbMcAnkckYNPltsISvJ969hVE0n3PJ5NWjM8Q3rHT2Tahik+UsZNrD2x3pugPC+mukPmFo8l92AATngVi+JZ2XbG8DRyrwCWDAjnoRVnwveGMm3kvT5bozLbhSRn1J7GsMNUU3KoupVeHLaHY/UzTMnTbM4/5Yp/6CKKm0sf8Syy/64p/6CKK8Z7n0C2MzdmopX7CkbPrUTMR1rrSOZscHzwajdM5xTGNNaYhjkjaKLO+grq2o1+ODxVZzjrSzzgsCO1VpZQzcHgDvWkbkMbI4yQD0qpLKF96aznceetQykDknitUiGyGW4Y9OKpSSkZ561YkHXBqlMrGqJuCyAKflJ9xVGX5sksQ38qfIpzgOR9KhlmXkMcn+8Kl3T0E7NGVcrJvYk7j61Ta6MY2tkD3q/cseWEi5z9wjt9awdX161025tLW4DGS6JCFRwMHHNXz9GjNpx1OU8Ta1dw6kkV+qppBmRo5VOG455Gc1t22q2+sQTSRAiIllKkjp6n0FeYeL57S+up5LaDyVEh3XHmk+Yee2eBVOx0zUNW0e7s11WC2RZfO8iVyvmAA/MSOi8f/AFq5pzcKqlzaChLmTVri+JvCtxpt1JPDHZwWbZSKP7RjjB6lu9ZE/iKG+je9vJGa/Eyxm3UbUeMLjdnt0xWfMJruISX63M+l2J8pmVvu5Jwik8An+Wax1gkgcqQGhbkFmxxzxnsaquo2bSMYeY7xPrsep3kRto5YYoowNjvuwxJJwfTn61lJq80IZpGEiKOjHn86rX0xklllChQTwAcgD61QVJJup6881rQjGnTjTh0OrWTuzfTXoZSqCKYyN0XI/nRdJ5gwyKB1wRnFc5cIInRd3XINZUksrZHmPsHbccVpKfLuOMEzo5rJpSQuAPZRVdtHT+M/yqhaK8katLHJMo+6C5AAroLO4towCbVkPqAD+tEdVdoJaPRmb/YUUny7OvcmhvD8BUjav4iuogv9PZcvN5fruRuPyrVjg0B0D3WsqIiM5tYWc/8Aj2BU1KtOmryX3Jv8h06c6jtH80jzOTwpbOTmIH6cUyHwdZvPHEFl8yRgqjzMDJ7ZNeinXdF0Tetna22sIz8fbrXZIB/vKx49sVW1TWNO1OyeeHw9b2Dq6q81rM2EBPUoeCO2eOa5HXbf8N276fk7M6lRSWs1ftr+exWHwuv9DCz3FibWFjsaab5lXP8AeIJIFeh6D8LNAs4o7/UZ7KZoiJB9ki3eWQcg5U5zx0xVbwnFq91aT6Z5k02n3UTQ7mORESDtYEnpuxkdK4gNcbi0Bkh1G3J5jYqz46jj+IHP15ry6lKtiVKEqii1/Kuj/FHpUqtHDuMo027931X4PyPbbTxpoOsajHYWk909zKH2ySxBEZlBOAM5yRmvm/41WS2/xCvZP4bmCCUH1+QKf/Qa3NNupbbWbC8RiWFwjOR67uT+OTR8b/B+sTazp2sRKk1td2626Isnzq8ed3y+nI5rbDL6tV9jKbaaurvqnr+Bz1oe3h7eEEnezsu+xh/BfYvxBs2JwVgnKHsDsx/ImvqPakkbGKVZFHXaeR9RXzV8LfBmvWupyay0xsoLPakqAhnmV8jaQDwpx1+nFeww3UsEgaNyGHcGt4c0qk6lNrovu/4c4sXJQjCnNNPV/e/+AdXcWrIASDis+0uhc3N1Zsg3RE7CuAVx296ZqHiXdZumxXcodzhtpXr0A61znhy4kiv4tsyxIxwzScjb3q6dWpOHtKkeXlOWUYQnyRd7nYDTJnOVKgjnlsVdj0x/lkdlYA8qp5q4rBFDkHb2bHB/Gqz6s6TuFO1FXgCrWLqVVeDQexjB+8WWsrZyCN0JPbqPyqOSxkGQjq69iDUDapdTx4Vd4J67actxcpKWMiBD0RucVl7WpF25jS0HrYbNDcpHtKEqOc9anTVblBGC24RjAB9PSo0M0k7+U8xLclY1yB+dW7fQ9QuD5cFjcyOx7sB/KplOMl78V/XqaQU0/cbLVl4jaCRisceH+8JollB/A9Pwro7fVNJv71JbqxiSDy9jx2hMPzf3/wD61VNI+HHiDUHGbNbZQfvTN/QV22n/AAWmzuu9VVBjpDESfzJrzp/V4ybpvXy/4B3w9u0lNaeZTtPCek+Ion/sTVniu1J/0W7xux6gr1H51l6h4M8Q6WctaieMd4m3D/Gu50vSPCPg+GDWV1FJzuMSXUsoYAnIO0Dv2pNW+K2j28N2llDNeXUWBGNu2KX5gDh/pk1zPHShLlTuvP8A4Bv7CM1d6PyPMS1/aK4uLSXf/eZSAPbFZ1xrsiKxYogjGSey12Xif4pKCV0+zEUXIMlzgsevRQcAfU14x448Vz6hGyyyK80h2ghQAqZzwB2rTD16Veoowp3b630MK8JUoNupojqW1e4uF3ookVuQwUEGlbUbeMRC7dElkGQq46epNedaJe6pcWs1vC+beIb2diFEec9/6UzVdQgK5mme6nxj5DtQD69a6Z4evKs6MLK38u/lfojmhiKUaSqyu799v+Cd5deI7aLJt1X5DyxbJH+H/wCqvMtd8QTyyPFvJVJWZHz8wz2p0+pIkECoyQxFfM8qL5mLZ4yTWHcxxS7WDyGViS27GPwrbLcvdKq6lS7b7+X9dDLG432kFCFl6Fu28R3ttvInZi4x8/zY9xmt3T/FMszRBoAzKDuk9f8ACuLZ0zwMY71OL2QRLHGSgHUg9a9ithKdRW5Vc8ynXnDXmOn1XVoLgM87szjoB1rEa+gKGVHEUq8gSdDWfJI8zbnbJ96W5gdNLuCLG4mncBoWUEIo5yxOeo7VxY2nHD4Vq9r6dOvqdOEnKtXTa21M7wprUUkJhkuRLOzMwiCHKckkFu5zXWPNL5EkkEas6DoT09/evOvDtwy3U2yBjvb95KXwB17V2FxfS21q8kUrLIOhzwa6ZJwoLl1em5krSrNPRM5nxLdpMFWKIRjrJhsl29T/AIVT0m5uFSU2sKMoU/PMRhDg5K8gf1qDVr2W9eSSaRXkB2nCgHv6VmMTApRpd0UiluDwD+dbUIKnFRtYirLndz9gNLfGmWX/AFxT/wBBFFRaTzpVj/1wT/0EUV5LWp7q2MwmoHNTE1A45rsRyshdsVXkep396qyHBNWiSKQntVaR8VM7enWqkx65q7ENkDyDP1qpcSgjAOBTpyc1TfnqcCqSJbFW4Vc5PJqN7kdiGOM/WqdxIRkDG71rOuLhlO4seO9Jxb2YuZIsXF0ZCcYHstZ0V0t2G8pwwGcEd8da57VdXkhlNzFcgRjgxjrmm2GtyN9ouFjAUqcnoAfUVy4vESoxTi7aodFKcrM2pXLcZri/FHiSayllt47HzreJczs6E4U91PQdetdWbmCSJXhl8zIGSBXF+KdaspoGhmtpJ4Qx5LmNSwz0I64rop4qnWhzQZlWpypO0jlNZ1mxXSp30mBYpUcO32jDSBSSPlB4x/8AXqh/Y9zcww3EjW8byAMQDyuckH9elYGpyrCA3mfOegzz9awp9RuWlRDcSbM8gMeB9KzrUK1ZxdOSj30uFKUFfmVz0vXPFWirpq6XHZl2tlwiKB5ayYPzE55POe9eW6hcyMhVVG7GNxb86tPMpQhQRjpkYrKurlV4knjQ/SjD5fDDxacnK+urLq1PatOyVjHniutjKFDL6bulZ8skqMPMRo88D0rcnu404Ul3PHpWVdyzPGUdQEJ6e/tXRaENUEblO5ki8nmUibqABkD8azQxk68IOv8AhWn/AGXJONzHYPQ8mq8ujuv3ZSB9P/r1lyyWr1LUkTw6mY+CBsxgAdqtx6mGHy5Zz0HSsR7Wa3cBjvB4+Xr+VNab7O8iyMY3HRSOTV+2tuHKmak7M2fMkLf7CHAqe3vZ5Lc2rzubdG8xIt3yqehwO1YqXj4yFOOmT0q/bS7ArkZPUijmTNErGhgqQRyD+lFxI4tJ1RiMryAeuOf6UjTK8f7s5560qziJ1ZkVwOquMg+xpyejFHc09I8S6jpxja0vp4l4barnb+XStXxP4iXUtYj1e2RbeW4jSSXZwPPXh2H1IB/GuJtLpHiAXgqSpUHpyastOxRF/hDE/TI/+tWTpU3NVLa/5lqrNRdO+h6npM2n3XiOax12wFtaarGj2cwXY1vLjhgR2Y5z2yRR8aNam0GXww0sHnWjwTKxBwRIGXOPwxWNpxl1/wAIXFrJukm04+fayZyygffQ+gxyPwqz8SJn8XfCyxviQ15pt1G7n/ZdSjN+eM+4r5yUOXFU3LZPla9Vo166X80fQKs/q8+XdrmT9Hqn6a28mcYfiLdeWLXR5biyjnkja6kJA8yNG3bMemfz6V62l3DeWaX9owks5SQsi8hT/dPoR6GvmxLW5tYwytAx67RKM/ka6Hw54u1fw+0xgLIkoxIu5Sjj/aU8Gva9k6D56Cv3T6/PueJUqQxq5a7s+jXTyt1TPYpZ9zn5s5681HFIIZgnmDbkfOvpXN+HvHOp69dfZX0+BrBY3Msoh3eWQCQdwwFyeK15Sc8V34apKsmqkeVrzuePi8OsNKKhLmT8rHf6T4he3huIIZop1ZSDFIOO/IrL0bV5Jtbnjul81QpQIGwBg8EGubWKW1uljZgkg5DK27GR6iozezQ3xnWUu4P3+m6uBZbDmqOD+Jb7P8P+HOhY2SUVJfC9tz1hhbEYN9NGG6o2FwOeh71s/Du00/xRILaSWO3ZI2fzJCCZMHH545rzGfxSnkXKTRq5Qrs/HrVmyvIAoltx+7OeM9PUe1cUaFejTk22302/r7zq9vSlUWit1PqTTfBeh2pt2eeOUztthJcYkOCcL6nAP5V3NhpVrZoFghRB/sivknT/ABRLZPpc0V1IrabKZrWOQ7o42Ocnb75r0C3+M2tDVNIuJ/IawtmkNxFbkqblWUgZzkfKeRXkVXVk/wB438z1qeIopWppfI941bV4PD9mbqa2vJ41BJFtCZCMDPOOgr511j4s6xqC3An1OaKCZmYwwYVVU5woI5xj3ruF+Punj+xElsXhku7jyr0uf3drHz84b+LnH61d1f4ZeDfEsFzdWt3FbmSTBlguFKI7HgYzgEk9KVFUVeNZNJ9iakpy1pNHz2niZJZGXYscSZK7j39hWbqviuaWB4bclAWGXB5wDnivSvEH7Pt9p7ySW140kS9zHn+RrzTWfBWqaXIQ211B+8Af5V7uDwuBnPmi7+TPIxVXF042lHTuU7/xFJdh5pXLTuuxVH3UHc/U1gySS3BjUlnKjCjrVqWzljfMwwAeeCPw6VrWt3DGo2RKDjHykZ/xr0owhh4pUoHmzqyqv35GW1reW8bRBXzwWRT1PaoZ7aOHatxMfNbkxp/CPc1sT6mFyq4Ue+RVFNLS6WS4lmwCfug5JrNV5r3qmnp1K5Iy0jqc9PgysY8hM8A9ajd3LA5Oelbd3ZwRovkLIW/iL1XFkDAZDkNuAA9vWu1V4cik/Qx5JOTS9TGYbA7tkKozxT4yGxg5zUmswyW9gZRGzK77AQcDPXrSaHbTXVmspjKIo27mPDEZ6VDxMYuUpPRW+809k3GKS1ZatrfzZUjGN7nAyaj8R2Vxp1lM99PMbaP92tuWOxic9CG7elRwXcE/nebN5W0ZUf3utc74kur17mKFWdLV4tyxyzZHGckn1ry8xqurVjRUkktXdfk/Tt9534KlyQdS3ktfzRzlnPDDc5mLeSuSQoyT7e1de+sQT2EUo+VT/wAs2ODgdjz3riYpCs8bwDzJOSUVMhef1rWhjl1AzCRXEyrkDb9456YrtmnUirSsZLlhK8lch1HUEuG2RRRwxAkhIx3+p5NNiZfs77mBDKTsKEjoec0+70hreORpG2yrgmPqRzjk9j7U86fJHaK4YOjrnK9q2pqMY2TuYVJXdz9dNJQDSrH/AK4J/wCgiil0o40yyHpCn/oIoryXue8tjDJGKidhTjUT13JHHcikbriqkjdanlOO3FVJWGDzzVpEMhcjqKrysCDRI+3vVOScZPvVksbK4XPFUJ5RyOMVLPMBnJ4qkl6xfayK8KZJOM7fxrOtV9lHm3CEeeVipcSooJJAA71i3V1HMZY2KtEUPIb8xWleW5QeXMuFkXOD3U1xV+0j3rw2ybRnaq5wPqSaKj9pBOmzO7hK0kUdYhhW3M0DFYlbYySMN2fasuVbpbcP8xtwufvDAU+2aivIi7SCWTbICdqkZDde9VmurV4Wgmd0lCkIQ2VLc4zXHiFK0dL28vxHStzN3sbj3cUbwXcbyQ6dbRfvNh3N7g+vvXDePdbEsVsllqwutOJJS3AwYSPUd+vU13cNqdP08ta/6TLJBl4ZmAVnxnAP9K8mbSLrUXa8+xg2gm/eJGcYXPzBRnOAK8jAeynXdepLSnor21vfvrfs767HpYjmVP2cVrLff+reRyVxLLIJJSrsoPzPg4B9zVVJhHmRhlz0HoK9gi0W2t9L1zQ7SUyWl+FuLb+NlORx74wK5fxZqHh6z0ePRNK0YCeJh5uo3S4mYg84HYE+vavUwucrE1fZUoN6/dGyd3fz0tq9DCpgfZQ55S/4fsjgmeWUvJ5hGPyrMeFbhG3yFdxyTnmtC4vCgAwAo7CqcirMm/cCc8r6V7jVzhTsQTWdn5R2yhWXkNu/nT7FLdCXMpLMNu8gk/gOw96ypFa4ufLRsRr941u21+trDsVMIozxxWKpRlLmG3ZlwxwIu3B+mDmqc1srONkhSPvjkk/0FUbvXI3XMYck9m4x/jVe1ur26mDI6+UOu5Rt+gpys2UloaqxWsAYIihh95jyfxNUplV2ZtqsfcA1I9pM24pKFJ6jbxWTdJc2ilZDlM/KwqLPXmWhSS6kd1bEOhxm1UljGvGCe/0pkqsZR5OAh/hJqWG43Rk7skdQazJptkhjVjnPy/SsOVRd4lrc1FnNsRuUxse/Y06SYMSc5J5JqGE+dCVkw475pJ7cxpuhXIA5QHp7irtZ3LtdEWn+U8OTEjNk5JHNdbb31gdOtIU0SxE6OTLPIWcyjPAwT8vccVx2l5VHXPIJrchbyvlJwpP5VXsYVLOS2EqkoN2PRb3TtAlj0m9sEutIF6rIZbeUuscgOCCpOSOex6VLb6Pe6JeTaDqCrLBqKNHHt+5KGzgrnuGCnHUGuCN45iVRI2xCSozwD6iu00nUZte0O8t/MZr20xdw7myVlXncD23qCpHrg15GMwroUtZXXn010d99D1cJXjXqq0bPy66aq22pr6d8JdNvNKS01jSXsLgR830ExaQPz1Qkgj2/WvOvFXwxufCV2n2pIZrCVsRXsefKc/3W/uN7H8M13fg74sX7XskOrX8v2SQ/u5uAYM5xn1Feux+ILK8gk03VZLW+SeIu0bxAiaLnk84NeR9Yx2X1X7X3ovW12/ub2t228up6McJgsZTToe7JadPxS/M81+GVnBYoYdP1Z7WaYYltJQssUvXtnn+dd54j8D2J0ee9toUg1CFTIywEiOQDqNh+6cc8V418Q/Cdv4P1GC70mR20a+BeD5stEw6pnvwcqeuPpXT+EvFN1LoVjNJPLM1vO6SF2JzHkAgnPTD/AKVdWnVpyjmGFqaSe1rfJ99ra7BBUq0ZYHFU9Yrf9V276FO2RHvI1dWMOfmKnHGD3qtewRRTkQzCZOu7BGPatGaxe2vZIeWWNiAPVe36VMNCvZLOW/S2b7HG21n9Pw64r6d4unGarTmlFpWV1rf9T4j2M0pUVG8k3f5FPSNBn1qaREOxUQndjJJ7DHX8afEX0W5kguAModrqrZGfrXTaZPp3m2rR2bRThgokjlICnkevX2rE8VabFarBDZWU7SDLS3HLb89uMjIrxsJnn1jHSw9VWi1onbpe7vc7a2XcuGVWDvJevlpawlrrNs4xdqQWbaChxtHvTH8RqJLuNPkjT/U47jPP+NcupkbhQce9TJaSSN8zov45r3Z4CjJts86niakEkjZl16Y37bJM268L9Mdfzq/B4jnW2khhLx+c6vIqthGKtuU49QeaxbfTt9xb2o+aa4JKMG7D+Hb613Gj/DXVr2a1T7PJGtzJ5SO6kDPfP0rH2GHh8Stb9Opsp15/A73/AKse6/Bz4s/2/bSaV4k1INqslxttXkTBlVh90kcZByBn1r1PUvDtlfria2jbBznHQ15/8LPhNbeGI2vtVtoJ9Tjm3QSBywRR0IHTryDXo+r30Gn2k91cylLaCNpZG/uqoJJ/IV8tjnSjWbw/4fpbofTYFVfZJVt/63OL174e6fdWcvlRKk+MqR615fqnw0SaAtLbBXXIPygH68V75b3Fvd2kV1CytbyxiVXPGVIyDz04rI1DWdNh1u00SSTGoXlu9zCmOHRCA3Przn6A1pg8wr07xepWJwNCqry0PlnV/A01k5MDuCP4WG4Vz0ltd2MgFxbgA9GXoa9A+NvxDsIrWztdEvA7Gd/tDRAr9zoAfTOenXFcNqPxAm1GG1+xoFmKCRjGgJZuefpXsvFRqU1Nx3v+B4FTDRp1HCEtFYaY2/tCO1aAJIyGVllO07cZznNQXmoaPHcxxOjy24b968MuM9cBfRaxdevJp43uLi4jkvJ4thVGz5aDoM+prm9PkDAq7DC/MAen0rmWGniYus5NJK1lffvf8vvL9rGi1BJNvv8AkS+LNeOozxxfZY4YrYssZXPKk+/8xVTSNXkgSSFSWL/KiZ4BPes7U2kmunaRwx/2TkAegqCEFCCDzXs0MJGOGVFr/h9/zOOrXcqzqI6H+w55Jp7eb9y0aFtx+Zc9hkHvWDq2lwQxyvqFy01zsIihibcQecFj2Ax0rXXXHt4VCKAVHzY/i69vrzmuPnlupL10ifzptpYtEc5GDnNcE44qdR+3kopJbfjr0R2U/YQgvZJtvuUYLd3O5JNuzqQ2MV1mma1bW0DG4kWWbaVUZIJ/LtXHxhpslOVHXmnrDI86xqCWYgDHc16E6cakeWWxzczUrmxeahLMrJkLCTnYnT/69MGoPDbsgb5dp4qSe0aK1maeVDNtOI0OcfU1XkEH2BD5oE2zBQj2POacakErRWhlKEnqz9fdJk3aXYn1gT/0EUVHoyn+x9P/AOveP/0EUV5j3PeT0MFmwKicnHtSnnPtTS37vb1OeK7m7bHFYgc1VlGM56+1TykoSD1qpJJitVqQ9Cnc1lTSBWwTyea0LpiVYqMnsKw7kysyqy4Y9AO9OT5UZtjbplcEPgp7+tY/72MkuoCv8uC1Wrm8UoV2lWB7msO8lY7Wcna3Q57e1c1Vc7sVCXLqbhmh8yczR5Lr99m+5gVw+uX0IneGFw6dS4/iroJ44ri2kgiuGmicYYHiRR/hXL6noaWd1bP9pU2jH595wwA9PUV5uExFOlN+0k/Ja9F+D8jqxMJVIrkS9TFlN9f/AOhWvmyqxLeSp4J9a5HVwbJZYpY3iuUf5t3GB6EV65pgsbW9muLLhJI9rRg52kHt7GvNPHWpza/I9xHbxxWdo+3LEea5ORk98cdKqhmP1mvyQjaOmr0dzOeEVKnzuV3+Bharr1zcTqTLIIo8BIw2MADH5+9Lb61KlksVp+6VCzEsdxGc9Pasi+uoVMDsCx2/cB+8e49hVuw1zQhBLbamjpKwaTzUB27gDtQY5A96yxdCPskvZt26JX/DqFCcvaN8yV+4niC31GHSYta0jU7qS2ZjHI1tHs2nkktjlRnHbH0rI8S6toGsaBBfo08XiQFI5o925ZsfekbjHvkfQjvSeHPH2qeGpx5Tia0YkyWsh+RsjnHofp6VyOqSm+vri52RxmeRpPLjGFXJzgD0rfCZZVp171NFF3Uk0m0/syVlf/hrFzxcZwsuu6fTzRVL7yWYfL9eRVC5cJkhwT6DrWxqfh3U7DSdP1KWFfseoEiBkkBJOcYI7H61f1HwDrGm3kVmsC3Vy9v9odYOfKAzuDE+mK9SePw8bJ1Er369t/uMFhqstVF9Px2OSjnKptUgHqcjnNQTTOQxZ2I9zxUsskbjduAI6NUcctsjEvlnP8TDIH4VrOXJG61MvOxTV/MYLnlj+VdBZNEGVRnbjaowSKwx5L3btGMRjjj9TWmt8qOsaPiMDqtOk7rmZTOhjQOCpIU9jn9KqXgTy5QuJCFJ9jVOG+WViu47h0J/iqySApOMk9TV66tML6WZzM8OVZ4FCy91HRvp71m3HzRrJj5lNdNdWioTKn3e49Pf6Vn3VqkqNtGHPB9DWc6ety4tEdkybOHyxGSPSrXmYbg1iW7+W2N2Gzg+1acLls7jkL3rJbGkSC4mWPUAVULvT5vQkd60UmMijPpVO8RSonCgNG27Ht0NWbaVJmI37Wxx71rBNGcy1bs3lsD2Nb/h3VG0jWbaQ5RC4WQMMfKfX+dZMKxj5RlR35z+Ndxb61purXNta3WjLPbRwCJmUk3LBRy+8dwO3TFc+NUvZuPLdNO50YSSVRTUrNNWOBvAum6/f2gIMayOEPtnI/Q11Oiard2mli/SQmPTLpBsJz+7k+8OvTI6e9Yvjfw3JoWpwXEc32jT7sb7a5H/AC0X0P8AtDgGpfDkFzfNNYwpJKlwjb4kPoCQ34YrnnyVsMp3utNfz/C5vBzo4lxas3fT129Vex6l4iii8Q+Er2xiLSzWy/arfA/u8gZ9SpYceleeeBr1rbWrO3eVhaXDmNkz8p3jH9B+Vdb4S8RGB9LHAkw0R3H5SV5Axnvkj8cVzHi/SDomuPJbqyWVw3nWzjpg84B9Qa8vAxUfaYOfW7X5P/M9bGzv7PGw6WT/ADX+R6olybhIHlnhhYBoZmYfxx8H36cig69i9cWF+jyTRFN8gwm8eg9+3FcNDqt1f2N4nlOj3apcwu4KK0o4dATgZYZIHfFY091e2YIltp4mjGctGy7evJ/xryZZd7aTTltpbT1/B6fI5sVX9nLnhF2et9f68/mdPFrE1jqDASfvlJDMQMA889cV2FpZa1cWSyWDvPHOzFpsDcnXrk8flXk2j3lxcapAISrzs+VEjABj7k8V3ul+IdQuLwySEkI20RhsKCCeOvJpY7BSpzjKKi7K7v1+X/BOTCYmMotO6vtY2IPhtOwJlLBupTv/ADrptI+HcSBd4284LEdK6XQNXttL0uS61HULeWa6fzJFi+ZkbH3TznP6Vn618TLS2S6tpLZPs9xDJFHIHDOrFWADqe3+Ne/hMxxNakpTjZ+X6GFTA4am9/vPIdW1saT8S7WKaC/tBY3KJ5cRjlkKZODHjg7gQce9fcmnxQXdpZTtbvGQBNGkqhWjJHcDo2DzX5o30XlajKy26W+0j9ymcIQMY5Of1r6G8EfGK+0uOxtbCGNLax0iO0WCS5MgaUOWaXb2/u47U80w9TkjUj21Jy3FU4SnGXVn2ChIXAfHtivG/jF8SdKg8E69b2WoRXF20n9muikhkZs7jg4yAoIyO9eVan8T/Euqzb31SeLGdogPl7evp9a8s8W6uqQPA4ldpH8zzSxwG5zn1NeThcMp1Y37o7MRj3yvkXzPT7n43yXXwtsvDUUEv297f7JdXTkKvlA4ATBySVAUn61wEni+9vNQsbi91KYSWMIghdpDmKNQcKCD7mua8PTQ3omhnDlEGVZCRj2JrVm0bTJMk+eB7SA4/MV7SpUqMpQ5bXv+J41SvUqpNy2/Q5vXdXOrXDMBtiTiMe3PNLa37x2DQRsEJ+8e7D0z6e1XL/SNPhRjD9qZ+gzjGapR2kCxYLTCX/d4r0YRoygopaI45TmpN33I7u5SRm8vIUcL7CqiXDxxsqtgPwfXFWpLT/b49xVOW3Knhga6o8kY8qMryk7kTHIq/aGC5jihlghiSMczbmBAzksfU46CtLWNEsrXQrC5s7gTymVo5pVyA5xkYB5wKy7eMowzxg964pVqeNot021Zu26aa0/q52wjPCVLSSe3mrPUfe3OmfaIIVRorcOXkfaQ5HYYJziuVv8AUJo5XW0YR24JG0KMsMn73r1rpNV0y4urgSu8kl1dP8oPJI/vE9hWLLp6W006XvBRHwiuMlsHHP15riw9Gmvjlzu2zd/n+h2TrSfwx5V9xz0QRNxIIHt2rQg1n7OFJghk2AhS45HXvT7XTpbq1uHRk8uLBcFgO1Z7QqrgMTsPcV6jUZ3i+hyX1uaFncma3nMiHy8HLjsSKkFp59m0r5CpGcEdzg8VWMkUMEkcUhw6kEc80xb1ltmi3NjaQBniny3Whi2fsVo+V0iwHpBH/wCgiijSGH9k2HT/AFEf/oIorynue8tjkpDtJ/u01Jtq8nA7VGxZsoD+tVTKQwzyRwK75Q5lY4FPldye4kDcgYPc561SkJILdh1p8kxRTvUg/wA6cjAx74z97jn+VRKp7KGiKUfaSM6Vjg881k3UD5yGyT1JOOa1LyQtIxYYPpXPahqSwSFCGOOpHauhJTimzCfusyNRkjXO3duz97PB/CuY1C+ZTy7YXoPSujurm3ukeJCFJ/iYYB9q5rV4obe4iUSByOXIPAOaTgkzK7I4dSlEiyygoV6FeCay9YvJLyZJGO5h2JwAPT2p11Ny5XLlOWC9RXLXuoNP+8Y4jBwq57+9cqoqc72G5zSt0OgspN9y0sNy1sY+mOSevHPGPrVjUDpltYyTXlibuN2LSyn5n56t9PpWEuv21lplxaXEazb8uir98PjHXsO9cOnia+0ecv5nmxP9+GTlX/wrxq+WV61SU4Nq22trr1Wv36HqUcXTpRSet9/L5Fm+0m0vvEN1BYXKLZRACOWQ5GSM7ffk/pXM+JdGfR5lBnhnD5w0TZ5HXI7U9NXW2hGUVmnZpSgOFUdBVq20XUdeKSm3k+zOwDSqB8ik8nGegFerTlOi1KrO0Era2u2lvfvc4Z2nJqEdX26HHsFeQANtXHJbsa7DQL/Rl0eTS7+283zJC4nWP5s4wNp6jH5c1uaj8L4odOuILafz9RMyvFcMdqCHnIIBPPf8K4GbR76z8SSaPBdKJYTlpwdqqoGS3XpiuapjcJmVOVOFRrl17PTr6a/8A0eHr4aSbje+n/APRJNb0iDRdP0i6tTc2GnzpJ5hYhgQxIyB9eaxdY8S6f4s1O/0ybX30nTygQTxRfu7rBJKlzyo56Hg1wNx4jjsTexwM15JOWheaf8A1bx5zkL/AHs85zXX3ev+Fdb8BQ2V1M1jdWwLQW0CF2EgGMnjlW75P8q8etlnsZxqcknzPda8rerlytPr5bdnY9CliW048y0Wz626XPOfFlppGm6sbbRL+W/tI0AaaRQBv5yFI6r05rGecGM8AVO8e5WOOQO1UlhedQiDLE4r6+FN0qahKXNZbvd/cec5qcnK1i3bWolhDeaVZuenFMliltJAGIPcEdCK0DB9ljiy4bjHHbFMu2WW1OfvJyD/ADqouMo80TJTuxkNwNuSME+hrWiv45sRlMccZOcmuWSRvNTYNxz09RV470lGcjjIrSMrFOKOh8wEeq+9Yl1IFZlQE4JAqdbzgHt3FUJH3TZxgFulObvsEEZNwpju2P8Aew1akEqlQFyPY9agv4C3lFQSSSKaIZQvAyV4ODXNKyldl3RonDRsp6EEYqja3ZiWIYH7sk57mmpcHPXkVWXh3U9QTitLjep0ltdJLhlbP481dEzb8ISODyDXN2oiYqzvtcNwPX8a2/PaMh1OCOv0rRO6ItZnSXGqz6v4Xu9MuTEwsVFzbO3DAqfmUeuVJrnNL1mbT7mC5t3KSxMGUg/zpRdqrjd0PBH1rKtE+fax+6cdfSuZUIQ5opaPW35/ebTrSlytvVaX/L7j0Dwj4gtE1yb7ZawvNcyF7eSQDbE5zkY6DOf0r1jVbrT/AB14Vn09iiyTIWt3AA8qdc4x6AkEe4rzHw/4UtNfslmm024soZSVS8t5S6A89VbPHvWk9nqvhG2uLFJkuZYmFzauOPMT+JcZ6j0r5rG0qdSrzQfLNNfh969T6PBVakaPLNXg7/1/kZ/hzx1Y6vNBpviuJJYYyAskgyisowCwFesMjabC91oV4kllLG2+wuG863nXklUzyp9hxXzHqrD+3Lx0XbHK/mqvoG5x+ZNd/wCA/Es2lBrSRt1pcOAAT/qnzw4+vQjvWuKyeHJ7fD6dXHo+9l0f9IyweayU/Y1/RS6rtr1RseNvD+mx6bp+uaRZtZRXTETQebuWNjkjHpnB/SsXTtZmtY40t3VLjeWMjHgADgY967FdSsvEGgXujxsQykxozn/lopypHtnivH/Nka7WEy+S5bY5fohz3q8LBVacqVbeL666dDhzKkqVWFaja0100V1ueyWnihbJIpnVIrh1/eypjOOevYk+tcBr/il9SbyyqgLIWEp++w5xmr8elXlisH9ox+bpzsN01u+8Y+vb8a9B8P6Z4ZTTr2OMLJFO4ZvPXc2RypHGcZFcNPF0Msj7VRdS70tstf60M54OtinySfL6/wBfieNPIxfLlt/fd1rf0PUYreWEHeJWJG/ICqO31rT+Iq2lxNbXovVuNUlytyqKVVQoAHXnNcVbefJKBDxtP3ycBT9a+ooYhYzCKpNct9/600/M8Svhnh67hF3sd9/a80V2HjkDOp+6x4Psa4/xJqMeqXstwqyxMT9zdlCfX2Nblw32C3t5xIrXAyHYHKt9Aa5jUpZJ281ppJVY9XGMGuXBUYTqqpBabX+ZpVqShDkk/kP0q/FmzOIlklIwrFiNn0A6/jXbvuMakyEsRk8Y5rzXcyn5Tiuj0rUmWaUyyOU2DljnmuvF0ZNqUTmg4/aJtbvyHiiSQhkYM2O1dHploL6SBEKgykKC5wAT6muKv7g3Fy0jHI7ewr03wqlla6P5GsQLHeTTKkCu+2RgwwMEHoPeuTMKv1PDqdrvy39fl1NcLReJq8i0X9fmaWseDZbTQY7ZdNMuordM0lxFhwYwpAAIPc89O1cTZ6BLqc8iRPHGsf3nkOAD6fWum1rxJbXusjSLdZ1c5torlFLRiQdRnODj1rHa2u/Ds8du12JvPPOxcDqQO/f1rwcBmNeFGUKsvfl7yun136tWXRHrYzA03UUqa92Oj+Wxta/AkOl2witEnurIq6gTeWmR3IPUcdOK8+g8X2zalcXF/p4+2b2kclsqDz/B+WK9HfR57z/Rp5EhypbAYOe/A561xXiDwvCJ1iikBsQ5JjXAZ3BOSx/IVw4LEUE5U6k7t31Tez1flr2OudKpZSUfvtuc7f8AjS6uI5IlvJAjOZTlQGcn3HTjt9a5c3CzO5lL7SCflPOe3WpNR06W1nnyMRo5AJP/ANeltprSGyuIZrbzJZeVnDYaPAOAPYnrX2WHpUaFPmoK9+1jxa051Z2qPYqJcNGhXseo9aj84SsAzbRnrjOKlsNksV2skkaEgbS+eoz0qtJgHAABHXnrXcpJtow5bFhUhbeDISf4W7H8KmZIksW43SlTx6VTjXO1iflJqWZSI3w+BtNXZPdmcrH7GaQn/EpsOP8AlhH/AOgiipdH/wCQRYf9cI//AEEUV4j3PeS0OGlwVwgYgdWNUZW5xWhNcFztjX5cc9qzbluQRtA6YFelCT2Z58l1QkLDdIXxsVCeelUJ9SeKBxtUBuMrxiknfOfmAA6+tZN42c4J2+/aplTUpai53FaDk1TymcO2I8Zx1OfasO9uRcGRm4ZjnPpSzZJwOv8AKqNyODuY4HpRyRUnJbmbnJrlZUuSIkk24JZcciuV1Gf3reuJUU5Zd6c5UtjP41i6hHC0URibcxB3rzwc8c01LlevUh7GA907zrtlaOTG3ep6/WsTVllgh4IeIHdnHIrR1BWiO/dgg8VRu7pbi2fHVlIx6GnJtNSWxHM9jPS0SNPMuZMMeQi/1Nc/rEL3W4IuSp4b0Fakk5dAxOTt61iTXbi7RVJ2AHcvrURdTmbbE3roMSztoAufmdf4mHf/AAro7HxXFpcIeLzGu1bGz+Ap7muduZmkBH3R+v8A9aseZnW4WBCFBI3N7n+lcWJwkcSv3mtiqNeUHoexaVr1hql0ssEctvcsMSRZ/duDnn0z3ry7xLbal4s1+7u9F0q9MWDA8kYOJMZBJJwBkAcVs6Pr9to2mm3Dxu4kLllGSyjPXtkY6+9ZGk/EC+06/uJ3a4u7afJki6svXBUdFNeBg8NWoVK1fD07tKy5m9dfx8rntVK0Jwp06st9XYkm+Eyahoti9rLNZ6tu23CXuQpPcBQCeD0IzkGvLtRt5dL1G6sJmRpbaVomaNsqSDg4PpXqGoeNdV1o6lbWkjW8dyAlnBcw7JHz94LJ0z/jTPC/wqtWt73UPFN0tpBEjbYPN2sT0Ds4zxnsOSRXXhMzq4NTnj6l77RWstdbLvbbsu5VXDU67isPH1ey0/q55davIZxsGePmHtV63hgVxJGSJVYkqehp9xaQafezRwXYuYEJVJ/LKeYPXaeRVT7Qo81lUqccse9fR1JOaTjs/wCtTwpN8zRZnkMw2RKMA8u3QewqhKwDNHIenXB60TSz+UGGFGOOeTVSJwWyTg9eaVBNXV9C46LQcgjguC3zKpHBbtV4z7QNpBzxz0qqZppomKQnb3LDIqsN6IUI4JyPauiL0si467mliFuRuVj1weKjaNfNO2QMF9u9R25LjHcVMVVFOBg+nrVWK1RDMxMZ2nkcimCXIA+7jripJVBjDDjPBxVIloiwIyQOPf3rKaV7sHa5JPEzHzQuB3bPBquIZXkLIMkDkE1oQL58JRzwf0NPkQRFGGAuNuc85qYp7MpPoUraby3ZHHB4INaplwxTt61nXgUqJejDgn2quNQkMucggcAY7Vraw9zSXnIeTLgkbcdvXNOurhVnjKRpHG3B2jnPvVe1kaSSQlepzmr81l9ot2A64yPrWcoXdxLfUvaZrM+m3MFxbysGicOBuODj1FelL4hHifSzIyfZXjuAIpA27y3IyBn0PIPvivFbZmVmy3GOldVpOvy2Wl3VogUw3DKzbhypHQiuTGYSNZKaXvLqehg8VKi3Bv3X0/I0/GekWSWkd7bRGK7jkKTgH74OcE+4PFc3DIpEZSdUY8HfkBT65rYv9Rl16WW3ixGJ23nceFGBnP4gVyAWWKaSCQbWRirD0OanDQnCHs29f0Fi5RnUc4rQ7rSri8027Hn/ALsTAssgIKt15Bz9DW1feEze2dtrtrNGGuJNk0bkDbJ0z+PXFc94O2XF/FHcsjQQAt5cj4BycYH4mu9i+zC1utEuYlhlkJ2S7sgsfun/AOvXnYxTjNOD97S9luuun3M7qEI16HK9tbX7/wDBKVqNT0L90BELeT5HJ+aMZz1HataOe58MWC3FvcxXloj7ZMDmMn0Pp/KvLmuJorkxzs7eW+10LHsTmtvT9ZlhhvHEgED/ACTRcHfGc84zyR61yYzLqnKm7NO19N/zdznw+Lu+R3uttdj0C+Np4x04xbYlmmP7uYgBo398Hniuav7HRLLTEjtGaW8ico0rZUsRnJx0xXO2+p/2VdyokruFXEcinGcjg11ejeMC1uLfUfJuLY8AyRK20+p9RWuCwVajF8km6aaaV7f8P6aGdadKu+Wdozel7X/r1OVumMg2ucIo4H92qLOhjePcdp5/Gu61bSdLvTvijayduQ0RLRH/AICeR+Fchd6Nc2cu2VOD9xxyrD1Br6LDVqVVJR08jxsXg62G96Wq7r+tCjb2D3UiRxIzyudoRRksfQCvR9H+Gsi297aassllq00Ky2O5xsOD8wbHfpx2rH8M+G7yeNNRtdSsraeGUiNJJSsm4DIIwDXpen6zfy6YX1kReapIVIhuk75LAdM/yr53P85qUv3eFmtHZ78yd9LdGu53ZXgYVHzV4tp7drdfO/Y8F1SM2l9PbiZJhE5TzE+62O49q7nwFb6JILJ3WRtahkMy7pCq/LnB9CPr3rotSsdO1LRrrRtIsLeGR9reZIwBGHyWyfmPHFUYfDlv4dgR0v3FyEKvIVDQnOc8HkD9a48fnNPG4T2MnKE29O7Vt3bZO+x04TL54av7SKUo9fLXpfqu5sLdW+n6c2n6U5haKaSZhI24uSSW5J79qxLjWLO8kW5liinKhgIpuUJ564PauauLk3mqx2v2lYUl3L5qHjv0zVS8e2s1jhtJ2efzDvYgt8vPYfy5rzaWAjCaTbcpa31673Z2yxLnG62Wn9IaNev/AA9qMs6eUYJGJCxcKBnIUZ5HrWdqPiiS8glSIyieRj82eFU9QPUmteTTHmtJYr+SOISHMZB+Y4J5I/SsXU7izhjKxW5t54yAAMFSBnknrmvocEsPWmvcvJdVtpt6/wBXPNxEqsFvZGLrOlXemrA10yCSUZ8vfudPTcOx56VQEUqIHZDsbo2aW4uJLx5d7lmJLknufWkikby/KkBA7E9q96lGcYpNps82o4t3itCnExXcAOSamVAJMyjjHH1pbSMDexHOcD2qWQjO09O/tXT1M29bIZ5iIDtAz71UuZWEb5P8J5/CrgSMngZrpPAvw/vfiF4t0rw7pkDyTX0yrIwHEUQP7yRj2Crk5+g70NK1xR1dj9ZNGkJ0fTz/ANO8f/oIoqSBFtoY4IlAjiUIv0AwKK8do925iN4YLdLrH/AP/r1Wk8I7xg3h/wC/f/16KK39pLuY+zj2IW8DBwR9uIz/ANMv/r1Wf4cI/XUW/wC/Q/xoope1n3D2MOxBL8MI5Bzqkg+kI/xqhN8JIpDzrEv/AH4H+NFFJVJdxOjDsVH+B8NwSW12YegFsvH/AI9ULfAe1xj+3p//AAGX/wCKoopOpLuP6vT7GbP+zda3LMzeJbnJ4H+iJx/49WaP2XbJSdvim8wTnBtE/wDiqKKPbTas2H1en2I0/ZSsFXB8VXh/7c0/+Kqo/wCyLpvnSS/8JZf5cYx9jj4/Wiil7Wd9w+rUuxGP2RdJzz4q1HP/AF6x/wCNRn9jfRHyx8Wapubqfs0VFFHtZrZiWGpfyleX9jLRXVk/4S7VVVuDttYqv6H+yDo2izPNb+K9VZpF2MHt4sEUUVnV/eQdOeqe5UKEISUorVE/iL9kbRtfs7e3l8T6jCsEjSK0dtHnJ/GtfTv2bLGx0oWNx4mv75VPD3NrExwOgI6HHvRRXHLBYedNUpQVk7ryfrudEZyjLnT1OT8R/sY+H9evzdxeJLywDKA0VtZRhWP97GetYMv7CuhspX/hNtXAPXFpDRRXfTk4QVOL0RhOnGcnOS1ZKn7CuhlgW8bauf8At0hqRv2EvDrjB8Zax1zxaw0UUe0ktmKNCn2LifsSaBGc/wDCX6vjsPs0P+FVZP2FfDssjP8A8JlrKljnAtocfyooojVnHZgqFNbIYv7Cfh9GBHjTWc/9esNWJP2HfDzLz4w1j8LaH/CiirWIqdyvZQ7Fc/sNeHsFf+Ex1gA/9O0P+FI37CXhyQL/AMVlrQI/6dof8KKKHXn3EqUL7EkP7C3h+EsV8Z6zg9jaw/4U6b9hrw9IgU+MNYxnP/HtD/hRRS9vU7jdGHYrP+wl4ckUj/hMtaGf+neH/Cq8X7AnhxOT411s/wDbtB/hRRQ69TuCpx7GlbfsL+GbdSB4w1ts+tvB/hUw/Yj8PIfl8Ya1/wCA8P8AhRRS9vU7j9lDsZ4/YS8OmQsPGmtjJzj7PD/hVpP2GfDyKVHjLW8HqPs8P+FFFHtp9xqnHsaVl+xd4ds3Zl8U6ud0YjP7iHt36deKrar+xH4b1K/lux4s1iJ5cblW3hIyBjPT2ooqFJqXOty3rHlexXh/Yf0G1benjLWCcEc20Nbx/ZK0ee2gil8U6q8sI2rMYItxHYH6UUUSfPrLoEJOnpHqUdR/Yu0G/vJbr/hLdWjeUgsBbREZxgn8etUG/Yf0Nuf+Ez1Yf9ukVFFUqs0uVPQzlTjKXM1qydv2KNEMMcbeMNVbywQpNrFkCmD9i7RkwB4w1XHp9lioopwqSjsyZU4voa1j+yNp1qAqeMdU8sfwNaxEVtR/st6L9ne3n8QahNA/VTbxDB9QccH3oorOb5ndm0G4qyI3/ZX0OG2MVp4g1C26/vlgiMuD23kdKoWv7Kum2MdwIPFmqrLPgNKYIy2MnP5560UVzywtGopKcb338+ok3Bpx0sE37J2lXF0s8firUoCgAQR20Xy47/1qfU/2U9P1O2WGTxbqS85ZltYvm+tFFT9ToJx91e7t5D5m7677mFN+xXo0xQnxjqo2HIxaxVfg/Y+0i2lEsPivUUkxgn7JEciiitKlKFRWmroUFyaxKd5+xnpM80ko8aatHvOdq2sXH0rNf9h7QpSd3jTWTn/p2hoorak/ZxtDQidOM3eWpGn7Cfh9GJHjPWOf+naGpx+w14eAwfGGsH/t2hoorX29RdSPq9N9Bsf7DHh6MsV8Zazyf+faGmH9hnw5k58YaySf+neH/Ciij6xU7h9WpfyjoP2GPDSzo0ni7W3iB+ZVhhUkexxx+Ve/fDb4TeE/hXYyW/hzTvLmnAE95O3mXE2OgZz2/wBkYHtRRSdWclZscaMIu6Wp25oooqSz/9k=) right center/auto 100% no-repeat,#eaf3ff !important; border:1px solid #dce9fb !important;border-radius:22px !important;padding:32px 34px !important;margin-bottom:18px !important;box-shadow:0 10px 28px rgba(34,77,133,.09) !important;min-height:290px; }
.st-key-herobox h1 { color:#102b52 !important;font-size:clamp(2rem,3vw,3rem) !important;line-height:1.12 !important;max-width:620px; }
.st-key-herobox p,.st-key-herobox span { color:#365b8b !important; }
.st-key-herobox .pill { background:#ffffffc9 !important;color:#5579a7 !important;border:1px solid #dce9fb; }
.st-key-herobox .stButton button { background:linear-gradient(100deg,#f45c0a,#ff8527) !important;color:white !important;border:0 !important;border-radius:999px !important;padding:.65rem 1.2rem !important;box-shadow:0 6px 14px #ff6b1629; }
.st-key-herobox .stButton button:hover { transform:translateY(-2px);box-shadow:0 10px 18px #ff6b1638; }
.st-key-herobox .mock { background:rgba(255,255,255,.78) !important;backdrop-filter:blur(8px);border:1px solid #d9e7fa !important;box-shadow:0 12px 28px #17365b15 !important; }
.st-key-herobox .mmain,.st-key-herobox .mmain * { color:#17345d !important; }
.st-key-herobox .mchip { background:#fff !important;border:1px solid #deebfb;box-shadow:0 8px 18px #17365b14; }
.st-key-herobox .mchip,.st-key-herobox .mchip * { color:#17345d !important; }
.st-key-herobox .badges span { background:#ffffffc9 !important;color:#365b8b !important;border:1px solid #dce9fb; }
.st-key-home .sec h2,.st-key-home h2,.st-key-home h3 { color:#102b52 !important; }
.st-key-home .stats > div,.st-key-home .card,.st-key-home .tile,.st-key-home .tool-card { background:#fff !important;border:1px solid #e0ebfa !important;border-radius:16px !important;box-shadow:0 6px 18px rgba(33,74,125,.055) !important; }
.pbanner { border-radius:17px !important;box-shadow:0 8px 22px #183d6b18 !important; }
div[data-testid="stMetric"] { background:#fff;border:1px solid #e0ebfa;border-radius:15px;padding:15px 17px;box-shadow:0 5px 18px rgba(33,74,125,.055); }
div[data-testid="stMetricLabel"] p { color:#60799e !important; }
div[data-testid="stMetricValue"] { color:#102b52 !important; }
.stButton button,.stDownloadButton button { border-radius:12px;transition:transform .18s,box-shadow .18s; }
.stButton button:hover,.stDownloadButton button:hover { transform:translateY(-1px);box-shadow:0 6px 16px #102b521c; }
[data-testid="stDataFrame"],.stAlert { border-radius:14px !important; }
@media(max-width:850px){.st-key-herobox{padding:22px !important;background-position:65% center !important}.st-key-herobox h1{font-size:2rem !important}}

</style>
""", unsafe_allow_html=True)

BG_HTML = r"""<!doctype html><html><head><meta charset="utf-8"><style>html,body{margin:0;height:100%;background:transparent;overflow:hidden}
canvas{position:absolute;inset:0;width:100%;height:100%;display:block;opacity:0;transition:opacity 1.4s}canvas.on{opacity:1}
.g1,.g2{position:absolute;border-radius:50%;pointer-events:none}
.g1{top:-20%;left:-10%;width:55%;height:55%;background:radial-gradient(circle,rgba(203,213,225,.65),rgba(203,213,225,0) 70%)}
.g2{bottom:-20%;right:-10%;width:45%;height:45%;background:radial-gradient(circle,rgba(203,213,225,.65),rgba(203,213,225,0) 70%)}
.big{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;font-family:"Space Grotesk","Segoe UI",system-ui,sans-serif;font-weight:900;font-size:62vh;line-height:1;color:#000;opacity:.03;user-select:none;pointer-events:none}</style></head>
<body><canvas id="c"></canvas><div class="g1"></div><div class="g2"></div><div class="big">&#8377;</div><script>
(function(){
var SPACING=30,BASE_R=1.5,HOVER_R=100,SCAN_DUR=2500,SCAN_PAUSE=4000,DEFAULT="rgba(148,163,184,0.4)",ACTIVE="#ff5500",TAU=Math.PI*2;
var cv=document.getElementById("c"),ctx=cv.getContext("2d"),W=1,H=1,mx=-1000,my=-1000,mobile=false,parts=[];
var P=null;try{P=window.parent;P.document}catch(e){P=null}
var reduce=window.matchMedia&&matchMedia("(prefers-reduced-motion: reduce)").matches;
function Pt(){this.reset()}
Pt.prototype.reset=function(){this.x=Math.random()*W;this.y=Math.random()*H;this.vx=(Math.random()-0.5)*0.5;this.vy=(Math.random()-0.5)*0.5;this.size=Math.random()*2};
Pt.prototype.update=function(){this.x+=this.vx;this.y+=this.vy;if(this.x<0||this.x>W)this.vx*=-1;if(this.y<0||this.y>H)this.vy*=-1};
function build(){var r=cv.getBoundingClientRect(),dpr=Math.min(window.devicePixelRatio||1,2);W=Math.max(1,r.width);H=Math.max(1,r.height);
cv.width=Math.round(W*dpr);cv.height=Math.round(H*dpr);ctx.setTransform(dpr,0,0,dpr,0,0);mobile=W<768;parts=[];
var n=mobile?12:40;for(var i=0;i<n;i++)parts.push(new Pt())}
function draw(now,still){ctx.clearRect(0,0,W,H);ctx.shadowBlur=0;ctx.shadowColor="transparent";
ctx.fillStyle="rgba(249,115,22,0.15)";for(var k=0;k<parts.length;k++){var q=parts[k];if(!still)q.update();ctx.beginPath();ctx.arc(q.x,q.y,q.size,0,TAU);ctx.fill()}
var loop=now%(SCAN_DUR+SCAN_PAUSE),scanY=mobile?Math.min(loop/SCAN_DUR,1)*(H+HOVER_R*2)-HOVER_R:0,hot=[];
ctx.fillStyle=DEFAULT;ctx.beginPath();
for(var x=0;x<W;x+=SPACING){for(var y=0;y<H;y+=SPACING){var dx=x-mx,dy=y-my,dist=mobile?Math.abs(y-scanY):Math.sqrt(dx*dx+dy*dy);
if(!still&&dist<HOVER_R){hot.push(x,y,1-dist/HOVER_R)}else{ctx.moveTo(x+BASE_R,y);ctx.arc(x,y,BASE_R,0,TAU)}}}
ctx.fill();
ctx.fillStyle=ACTIVE;ctx.shadowBlur=mobile?0:15;ctx.shadowColor=mobile?"transparent":"rgba(255,85,0,0.4)";
for(var h=0;h<hot.length;h+=3){ctx.beginPath();ctx.arc(hot[h],hot[h+1],BASE_R+hot[h+2]*(mobile?2:3),0,TAU);ctx.fill()}
ctx.shadowBlur=0}
function loop(now){if(!(P&&P.document.hidden))draw(now,false);requestAnimationFrame(loop)}
if(P){P.addEventListener("mousemove",function(e){if(!mobile){mx=e.clientX;my=e.clientY}},{passive:true});
P.document.addEventListener("mouseleave",function(){mx=-1000;my=-1000})}
new ResizeObserver(function(){build();if(reduce)draw(performance.now(),true)}).observe(cv);
build();cv.classList.add("on");if(reduce){draw(performance.now(),true)}else{requestAnimationFrame(loop)}
})();
</script></body></html>"""

with st.container(key="bgdots"):
    if hasattr(st, "iframe"):
        st.iframe(BG_HTML, height=600)
    elif components is not None:
        components.html(BG_HTML, height=600)
IMG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "images")


@st.cache_data(show_spinner=False)
def _encode_img(path, mtime, max_w):
    from PIL import Image
    im = Image.open(path).convert("RGB")
    im.thumbnail((max_w, max_w))
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=82)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()


def img_uri(name, max_w=900):
    """Looks for images/<name>.jpg/.jpeg/.png/.webp. Returns an embeddable data URI, or None if there is no such file."""
    for ext in ("jpg", "jpeg", "png", "webp"):
        path = os.path.join(IMG_DIR, f"{name}.{ext}")
        if os.path.exists(path):
            try:
                return _encode_img(path, os.path.getmtime(path), max_w)
            except Exception:
                return None
    return None


FLOW_HTML = r"""<!doctype html><html><head><meta charset="utf-8"><style>html,body{margin:0;height:100%;background:transparent;overflow:hidden}canvas{width:100%;height:100%;display:block;cursor:pointer}</style></head><body><canvas id="c"></canvas><script>
(function(){
var TEXT="Dhan Disha",CELL=8,GAP=3,SPEED=1,RADIUS=130,STRENGTH=1;
var COLORS=[[190,205,240,1],[47,107,255,1],[20,48,107,1]];
var TAU=Math.PI*2,clamp=function(v,a,b){return Math.max(a,Math.min(b,v))},sm=function(v){return v*v*(3-2*v)};
var hash=function(x,y){var v=Math.sin(x*127.1+y*311.7+74.7)*43758.5453123;return v-Math.floor(v)};
var vnoise=function(x,y){var ix=Math.floor(x),iy=Math.floor(y),fx=x-ix,fy=y-iy,ux=sm(fx),uy=sm(fy);
var a=hash(ix,iy),b=hash(ix+1,iy),c=hash(ix,iy+1),d=hash(ix+1,iy+1);var t=a+(b-a)*ux,bt=c+(d-c)*ux;return t+(bt-t)*uy};
var cv=document.getElementById("c"),ctx=cv.getContext("2d");
var W=1,H=1,cols=1,rows=1,n=1,step=11,cellPx=8,seed=0;
var mask,amp,sizeB,hx,hy,sx,sy,wx,wy,dly,tiers=[],tcss=[];
var px=0,py=0,pact=false,t0=performance.now(),last=t0,scat=t0;
var reduce=window.matchMedia&&matchMedia("(prefers-reduced-motion: reduce)").matches;
function mix(a,b,t){return Math.round(a+(b-a)*t)}
function ramp(c){var low=c<=0.6,f=low?COLORS[0]:COLORS[1],t=low?COLORS[1]:COLORS[2],k=low?c/0.6:(c-0.6)/0.4,fa=low?0.24:0.92,ta=low?0.92:1;
return "rgba("+mix(f[0],t[0],k)+","+mix(f[1],t[1],k)+","+mix(f[2],t[2],k)+","+(fa+(ta-fa)*k).toFixed(3)+")"}
function sample(){var o=document.createElement("canvas");o.width=cols;o.height=rows;var c=o.getContext("2d",{willReadFrequently:true});
var fs=Math.max(rows*0.68,1),fam='"Segoe UI",system-ui,Arial,sans-serif';c.font="800 "+fs+"px "+fam;var w=c.measureText(TEXT).width,mx=cols*0.86;
if(w>mx){fs=Math.max(fs*mx/w,1);c.font="800 "+fs+"px "+fam}
c.fillStyle="#fff";c.textAlign="center";c.textBaseline="middle";c.fillText(TEXT,cols/2,rows/2);
var d=c.getImageData(0,0,cols,rows).data;mask=new Float32Array(n);
for(var i=0;i<n;i++){var p=i*4,l=(d[p]*0.2126+d[p+1]*0.7152+d[p+2]*0.0722)/255,cov=l*d[p+3]/255;mask[i]=sm(clamp((cov-0.08)/0.78,0,1))}}
function scatter(){for(var i=0;i<n;i++){sx[i]=(hash(i+1,seed*1.7+3.1)*1.25-0.125)*W;sy[i]=(hash(seed*2.3+7.7,i+1)*1.25-0.125)*H}}
function build(){var r=cv.getBoundingClientRect(),dpr=Math.min(window.devicePixelRatio||1,2);W=Math.max(1,r.width);H=Math.max(1,r.height);
cv.width=Math.round(W*dpr);cv.height=Math.round(H*dpr);ctx.setTransform(dpr,0,0,dpr,0,0);
step=CELL+GAP;cellPx=CELL;cols=Math.ceil(W/step);rows=Math.ceil(H/step);
var ls=Math.max(W/44,3);if(W>=44&&ls<step){cellPx*=ls/step;step=ls;cols=Math.ceil(W/step);rows=Math.ceil(H/step)}
if(cols*rows>14000){var k=Math.sqrt(cols*rows/14000);step*=k;cellPx*=k;cols=Math.ceil(W/step);rows=Math.ceil(H/step)}
n=cols*rows;amp=new Float32Array(n);sizeB=new Float32Array(n);hx=new Float32Array(n);hy=new Float32Array(n);sx=new Float32Array(n);sy=new Float32Array(n);wx=new Float32Array(n);wy=new Float32Array(n);dly=new Float32Array(n);
sample();
for(var row=0;row<rows;row++){var ny=rows>1?row/(rows-1):0;for(var col=0;col<cols;col++){var i=row*cols+col,nx=cols>1?col/(cols-1):0,m=mask[i];
hx[i]=(col+0.5)*step;hy[i]=(row+0.5)*step;amp[i]=1-m*0.84;sizeB[i]=0.3+0.64*m;dly[i]=clamp(nx*0.55+ny*0.3+hash(col,row)*0.15-m*0.16,0,1)}}
scatter();var b=[[],[],[],[],[],[],[]];for(var j=0;j<n;j++){b[Math.min(6,Math.floor(mask[j]*7))].push(j)}
tiers=b.map(function(a){return Int32Array.from(a)});tcss=b.map(function(a,t){return ramp((t+0.5)/7)})}
function stamp(dt){var rad=RADIUS,lim=rad*rad,ceil=step*2.4,c0=clamp(Math.floor((px-rad)/step),0,cols-1),c1=clamp(Math.ceil((px+rad)/step),0,cols-1),r0=clamp(Math.floor((py-rad)/step),0,rows-1),r1=clamp(Math.ceil((py+rad)/step),0,rows-1);
for(var r=r0;r<=r1;r++){for(var c=c0;c<=c1;c++){var i=r*cols+c,dx=hx[i]-px,dy=hy[i]-py,sq=dx*dx+dy*dy;if(sq>=lim||sq===0)continue;
var dist=Math.sqrt(sq),fo=1-dist/rad,push=fo*fo*STRENGTH*rad*3.4*dt;wx[i]=clamp(wx[i]+dx/dist*push,-ceil,ceil);wy[i]=clamp(wy[i]+dy/dist*push,-ceil,ceil)}}}
function draw(now,still){var dt=clamp((now-last)/1000,0,0.05);last=now;var time=still?0:(now-t0)/1000*SPEED*0.14;
ctx.clearRect(0,0,W,H);if(!still&&pact)stamp(dt);
var reform=still?1:clamp((now-scat)/1750,0,1),settled=reform>=1,decay=Math.exp(-dt/0.42),drift=step*0.95,rest=1/0.55;
for(var k=0;k<tiers.length;k++){var bk=tiers[k];if(!bk.length)continue;ctx.fillStyle=tcss[k];ctx.beginPath();
for(var q=0;q<bk.length;q++){var i=bk[q],col=i%cols,row=(i/cols)|0,gx=col*0.19,gy=row*0.19;
var ang=vnoise(gx,gy+time)*TAU*1.35,mag=0.35+0.65*vnoise(gx+37.2,gy-time*0.8+11.5),u=Math.cos(ang)*mag,v=Math.sin(ang)*mag;
wx[i]*=decay;wy[i]*=decay;var a=drift*amp[i],rx=hx[i]+u*a+wx[i],ry=hy[i]+v*a+wy[i],x=rx,y=ry,sc=1;
if(!settled){var loc=clamp((reform-dly[i]*0.45)*rest,0,1),inv=1-loc,e=1-inv*inv*inv;x=sx[i]+(rx-sx[i])*e;y=sy[i]+(ry-sy[i])*e;sc=0.5+0.5*e}
var size=cellPx*(sizeB[i]+0.2*(Math.abs(u)+Math.abs(v)))*sc;if(size<=0.35)continue;if(x<-size||x>W+size||y<-size||y>H+size)continue;
ctx.rect(x-size/2,y-size/2,size,size)}ctx.fill()}}
function loop(now){draw(now,false);requestAnimationFrame(loop)}
cv.addEventListener("pointermove",function(e){var r=cv.getBoundingClientRect();px=e.clientX-r.left;py=e.clientY-r.top;pact=true},{passive:true});
cv.addEventListener("pointerleave",function(){pact=false});
cv.addEventListener("click",function(){seed++;scatter();scat=performance.now();wx.fill(0);wy.fill(0)});
new ResizeObserver(function(){build();if(reduce)draw(performance.now(),true)}).observe(cv);
build();if(reduce){draw(performance.now(),true)}else{requestAnimationFrame(loop)}
})();
</script></body></html>"""
CHART_DOC = r'''<!doctype html><html><head><meta charset="utf-8"><style>
html,body{margin:0;height:100%;background:transparent;font-family:Poppins,"Segoe UI",system-ui,sans-serif;color:#4c6489;overflow:hidden}
#w{position:relative;width:100%;height:100%}
svg{display:block;width:100%;height:100%;overflow:visible}
.ttl{position:absolute;top:10px;left:16px;font-size:13px;font-weight:600;color:#102b52;z-index:2}
.leg{position:absolute;top:10px;right:16px;display:flex;gap:16px;font-size:12px;color:#33507a;z-index:2}
.leg i{display:inline-block;width:10px;height:10px;border-radius:3px;margin-right:6px;vertical-align:-1px}
.tip{position:absolute;pointer-events:none;background:#fff;border:1px solid #dfe9f7;border-radius:10px;padding:8px 12px;box-shadow:0 10px 24px rgba(24,56,107,.16);font-size:12px;opacity:0;transition:opacity .15s;min-width:130px;z-index:3}
.tip b{display:block;color:#102b52;margin-bottom:5px}
.tip div{display:flex;justify-content:space-between;gap:16px;margin-top:2px}
.tip em{font-style:normal;font-weight:600;color:#102b52}
.brow{display:flex;align-items:center;gap:12px;margin:16px 16px}
.blab{width:150px;font-size:13px;color:#33507a;flex:none}
.btrack{flex:1;height:26px;background:#edf2fb;border-radius:8px;overflow:hidden}
.bfill{height:100%;width:0;border-radius:8px}
.bval{width:96px;text-align:right;font-weight:600;color:#102b52;font-size:13px;flex:none}
.dwrap{display:flex;align-items:center;justify-content:center;gap:34px;height:100%}
.dleg div{display:flex;align-items:center;gap:10px;font-size:13px;margin:9px 0;color:#33507a;transition:opacity .2s;cursor:default}
.dleg i{width:11px;height:11px;border-radius:3px;display:inline-block}
.dleg em{font-style:normal;font-weight:600;color:#102b52;margin-left:auto;padding-left:18px}
</style></head><body><div id="w"></div><script>
var S=__SPEC__;
(function(){
var W=document.getElementById("w"),NS="http://www.w3.org/2000/svg";
var reduce=window.matchMedia&&matchMedia("(prefers-reduced-motion: reduce)").matches;
var KEY="dd_chart_"+S.id,raf=0,played=false,prev=null,svg=null;
try{prev=JSON.parse(sessionStorage.getItem(KEY)||"null")}catch(e){prev=null}
function el(n,a,p){var e=document.createElementNS(NS,n);for(var k in a)e.setAttribute(k,a[k]);if(p)p.appendChild(e);return e}
function fIN(v){return Math.round(v).toLocaleString("en-IN")}
function fShort(v){var a=Math.abs(v),s=v<0?"-":"";if(a>=1e7)return s+"₹"+(a/1e7).toFixed(a>=1e8?0:1).replace(/\.0$/,"")+" Cr";if(a>=1e5)return s+"₹"+(a/1e5).toFixed(1).replace(/\.0$/,"")+" L";if(a>=1e3)return s+"₹"+(a/1e3).toFixed(0)+"K";return s+"₹"+Math.round(a)}
function fVal(v){return S.fmt==="pct0"?Math.round(v)+"%":S.fmt==="pct"?v.toFixed(1)+"%":S.fmt==="num"?"₹"+v.toFixed(2):"₹"+fIN(v)}
function fAx(v){return S.fmt==="pct"?v.toFixed(0)+"%":S.fmt==="num"?"₹"+v.toFixed(0):fShort(v)}
function ease(t){return 1-Math.pow(1-t,3)}
function clamp(v,a,b){return Math.max(a,Math.min(b,v))}
function mono(p){var n=p.length;if(n<2)return"";var dx=[],m=[],t=[],i;
for(i=0;i<n-1;i++){dx[i]=p[i+1][0]-p[i][0]||1;m[i]=(p[i+1][1]-p[i][1])/dx[i]}
t[0]=m[0];t[n-1]=m[n-2];for(i=1;i<n-1;i++)t[i]=(m[i-1]*m[i]<=0)?0:(m[i-1]+m[i])/2;
for(i=0;i<n-1;i++){if(m[i]===0){t[i]=0;t[i+1]=0}else{var a=t[i]/m[i],b=t[i+1]/m[i],h=a*a+b*b;if(h>9){var s=3/Math.sqrt(h);t[i]=s*a*m[i];t[i+1]=s*b*m[i]}}}
var d="M"+p[0][0].toFixed(1)+","+p[0][1].toFixed(1);
for(i=0;i<n-1;i++){var h2=dx[i]/3;d+=" C"+(p[i][0]+h2).toFixed(1)+","+(p[i][1]+t[i]*h2).toFixed(1)+" "+(p[i+1][0]-h2).toFixed(1)+","+(p[i+1][1]-t[i+1]*h2).toFixed(1)+" "+p[i+1][0].toFixed(1)+","+p[i+1][1].toFixed(1)}
return d}
function niceStep(r){var e=Math.pow(10,Math.floor(Math.log(r)/Math.LN10)),f=r/e;return(f<=1?1:f<=2?2:f<=2.5?2.5:f<=5?5:10)*e}
/* ---------------- LINE ---------------- */
var L=null;
function buildLine(){
W.innerHTML="";var w=W.clientWidth||620,h=W.clientHeight||340,m={t:48,r:26,b:36,l:64},iw=w-m.l-m.r,ih=h-m.t-m.b,X=S.x,n=X.length,ser=S.series;
var all=[];ser.forEach(function(s){all=all.concat(s.y)});if(S.ref)all.push(S.ref.value);
var lo=Math.min(0,Math.min.apply(null,all)),hi=Math.max.apply(null,all);if(hi<=lo)hi=lo+1;
var step=niceStep((hi-lo)/4);hi=Math.ceil(hi/step)*step;lo=Math.floor(lo/step)*step;
var sx=function(i){return m.l+(n>1?iw*i/(n-1):iw/2)},sy=function(v){return m.t+ih*(1-(v-lo)/(hi-lo))};
if(S.title){var t=document.createElement("div");t.className="ttl";t.textContent=S.title;W.appendChild(t)}
var lg=document.createElement("div");lg.className="leg";ser.forEach(function(s){var d=document.createElement("span");d.innerHTML='<i style="background:'+s.color+'"></i>'+s.name;lg.appendChild(d)});W.appendChild(lg);
svg=el("svg",{viewBox:"0 0 "+w+" "+h,preserveAspectRatio:"none"},null);W.appendChild(svg);
var defs=el("defs",{},svg);
var pat=el("pattern",{id:"dg",x:0,y:0,width:20,height:20,patternUnits:"userSpaceOnUse"},defs);el("circle",{cx:10,cy:10,r:1,fill:"#9fb3d1","fill-opacity":.35},pat);
var shadow=el("filter",{id:"ds",x:"-50%",y:"-50%",width:"200%",height:"200%"},defs);el("feDropShadow",{dx:1,dy:2,stdDeviation:2.5,"flood-color":"rgba(16,43,82,.45)"},shadow);
ser.forEach(function(s,k){var g=el("linearGradient",{id:"ag"+k,x1:0,y1:0,x2:0,y2:1},defs);el("stop",{offset:"0%","stop-color":s.color,"stop-opacity":.16},g);el("stop",{offset:"100%","stop-color":s.color,"stop-opacity":0},g);
var f=el("filter",{id:"gl"+k,x:"-30%",y:"-60%",width:"160%",height:"220%"},defs);el("feDropShadow",{dx:0,dy:5,stdDeviation:6,"flood-color":s.color,"flood-opacity":.45},f)});
el("rect",{x:m.l,y:m.t,width:iw,height:ih,fill:"url(#dg)","pointer-events":"none"},svg);
for(var v=lo;v<=hi+1e-9;v+=step){var y=sy(v);el("line",{x1:m.l,x2:m.l+iw,y1:y,y2:y,stroke:"#d6e1f2","stroke-dasharray":"4 8"},svg);var tx=el("text",{x:m.l-10,y:y+4,"text-anchor":"end","font-size":11,fill:"#4f678d"},svg);tx.textContent=fAx(v)}
var cnt=Math.min(6,n),used={};for(var q=0;q<cnt;q++){var ix=cnt>1?Math.round(q*(n-1)/(cnt-1)):0;if(used[ix])continue;used[ix]=1;var t2=el("text",{x:sx(ix),y:h-10,"text-anchor":q===0?"start":q===cnt-1?"end":"middle","font-size":11,fill:"#4f678d"},svg);t2.textContent=X[ix]}
if(S.ref){var ry=sy(S.ref.value);el("line",{x1:m.l,x2:m.l+iw,y1:ry,y2:ry,stroke:"#ff6b16","stroke-dasharray":"5 5","stroke-width":1.2},svg);
var lab=el("text",{x:m.l+8,y:ry-7,"text-anchor":"start","font-size":11,"font-weight":600,fill:"#e0580b"},svg);lab.textContent=S.ref.label}
L={w:w,h:h,m:m,iw:iw,ih:ih,sx:sx,sy:sy,n:n,paths:[],areas:[],dots:[],tags:[],cur:null,curDots:[]};
ser.forEach(function(s,k){var a=el("path",{fill:"url(#ag"+k+")",stroke:"none"},svg),p=el("path",{fill:"none",stroke:s.color,"stroke-width":2.4,"stroke-linecap":"round","stroke-linejoin":"round",filter:"url(#gl"+k+")"},svg);
if(s.dash)p.setAttribute("stroke-dasharray","6 6");
L.areas.push(a);L.paths.push(p);
var d=el("circle",{r:6,fill:s.color,stroke:"#fff","stroke-width":2,filter:"url(#ds)"},svg);L.dots.push(d);
var tg=el("g",{},svg),rc=el("rect",{rx:8,height:20,fill:s.color},tg),tt=el("text",{"font-size":11,"font-weight":600,fill:"#fff","text-anchor":"middle"},tg);L.tags.push({g:tg,r:rc,t:tt})});
L.cur=el("line",{y1:m.t,y2:m.t+ih,stroke:"#7b8fb0","stroke-dasharray":"3 3","stroke-width":1,opacity:0},svg);
ser.forEach(function(s){L.curDots.push(el("circle",{r:6,fill:s.color,stroke:"#fff","stroke-width":2,filter:"url(#ds)",opacity:0},svg))});
var tip=document.createElement("div");tip.className="tip";W.appendChild(tip);
svg.addEventListener("pointermove",function(e){var r=svg.getBoundingClientRect(),mx=(e.clientX-r.left)*(w/r.width);if(mx<m.l||mx>m.l+iw){leave();return}
var i=clamp(Math.round((mx-m.l)/iw*(n-1)),0,n-1);L.cur.setAttribute("x1",sx(i));L.cur.setAttribute("x2",sx(i));L.cur.setAttribute("opacity",1);
var html="<b>"+X[i]+"</b>";ser.forEach(function(s,k){L.curDots[k].setAttribute("cx",sx(i));L.curDots[k].setAttribute("cy",sy(L.vals?L.vals[k][i]:s.y[i]));L.curDots[k].setAttribute("opacity",1);html+='<div><span><i style="display:inline-block;width:8px;height:8px;border-radius:2px;margin-right:6px;background:'+s.color+'"></i>'+s.name+"</span><em>"+fVal(s.y[i])+"</em></div>"});
tip.innerHTML=html;tip.style.opacity=1;var tw=tip.offsetWidth,left=sx(i)*(r.width/w)+14;if(left+tw>r.width)left=sx(i)*(r.width/w)-tw-14;tip.style.left=left+"px";tip.style.top=(m.t+6)+"px"});
function leave(){tip.style.opacity=0;L.cur.setAttribute("opacity",0);L.curDots.forEach(function(d){d.setAttribute("opacity",0)})}
svg.addEventListener("pointerleave",leave)}
function setLine(t,mode){var n=L.n,ser=S.series,vals=[];
ser.forEach(function(s,k){var ys=s.y.slice();if(mode==="morph"&&prev&&prev[k]){var pv=prev[k],pn=pv.length;ys=ys.map(function(v,i){var f=n>1?i/(n-1)*(pn-1):0,i0=Math.floor(f),i1=Math.min(pn-1,i0+1),old=pv[i0]+(pv[i1]-pv[i0])*(f-i0);return old+(v-old)*ease(t)})}
vals.push(ys)});L.vals=vals;
ser.forEach(function(s,k){var pts=vals[k].map(function(v,i){return[L.sx(i),L.sy(v)]}),d=mono(pts),p=L.paths[k];p.setAttribute("d",d);
L.areas[k].setAttribute("d",d+" L"+L.sx(n-1)+","+(L.m.t+L.ih)+" L"+L.sx(0)+","+(L.m.t+L.ih)+" Z");
var last=pts[n-1],dot=L.dots[k],tg=L.tags[k];dot.setAttribute("cx",last[0]);dot.setAttribute("cy",last[1]);
var txt=fAx(vals[k][n-1]);tg.t.textContent=txt;var tw=txt.length*6.6+16,ends=vals.map(function(v){return v[n-1]}),up=(ser.length===1)||(ends[k]>=Math.max.apply(null,ends));var ty=clamp(last[1]+(up?-30:12),L.m.t-8,L.m.t+L.ih-24);
tg.r.setAttribute("width",tw);tg.r.setAttribute("x",-tw/2);tg.r.setAttribute("y",0);tg.t.setAttribute("y",14);tg.g.setAttribute("transform","translate("+clamp(last[0],L.m.l+tw/2,L.w-tw/2-2)+","+ty+")");
if(mode==="draw"){var len=p.getTotalLength(),pr=ease(clamp(t,0,1));p.setAttribute("stroke-dasharray",s.dash?"6 6":len+" "+len);if(!s.dash)p.setAttribute("stroke-dashoffset",len*(1-pr));
L.areas[k].setAttribute("opacity",clamp((t-.45)/.55,0,1));var show=clamp((t-.85)/.15,0,1);dot.setAttribute("r",6*show);tg.g.setAttribute("opacity",show)}
else{L.areas[k].setAttribute("opacity",1);dot.setAttribute("r",6);tg.g.setAttribute("opacity",1);if(!s.dash)p.removeAttribute("stroke-dashoffset")}})}
/* ---------------- BARS ---------------- */
function buildBars(){W.innerHTML="";if(S.title){var t=document.createElement("div");t.className="ttl";t.textContent=S.title;W.appendChild(t)}
var box=document.createElement("div");box.style.cssText="position:absolute;left:0;right:0;top:44px";W.appendChild(box);var mx=Math.max.apply(null,S.items.map(function(i){return i.v}))||1;
S.items.forEach(function(it){var r=document.createElement("div");r.className="brow";r.innerHTML='<div class="blab">'+it.l+'</div><div class="btrack"><div class="bfill" style="background:'+it.c+'"></div></div><div class="bval">0</div>';box.appendChild(r);it.fill=r.querySelector(".bfill");it.val=r.querySelector(".bval");it.pc=it.v/mx*100})}
function setBars(t){S.items.forEach(function(it,i){var p=ease(clamp(t*1.25-i*0.12,0,1));it.fill.style.width=(it.pc*p)+"%";it.val.textContent=fVal(it.v*p)})}
/* ---------------- DONUT ---------------- */
function buildDonut(){W.innerHTML="";var tot=S.parts.reduce(function(a,p){return a+p.v},0)||1,R=70,C=2*Math.PI*R,wrap=document.createElement("div");wrap.className="dwrap";
var sv=el("svg",{viewBox:"0 0 200 200",width:200,height:200,style:"flex:none;width:200px;height:200px"},null);el("circle",{cx:100,cy:100,r:R,fill:"none",stroke:"#edf2fb","stroke-width":26},sv);
var off=0;S.parts.forEach(function(p){p.len=p.v/tot*C;p.off=off;off+=p.len;p.c=el("circle",{cx:100,cy:100,r:R,fill:"none",stroke:p.c0||p.color,"stroke-width":26,transform:"rotate(-90 100 100)","stroke-dasharray":"0 "+C,"stroke-dashoffset":-p.off},sv)});
var c1=el("text",{x:100,y:94,"text-anchor":"middle","font-size":11,fill:"#4f678d"},sv);c1.textContent=S.cl||"";S.cv=el("text",{x:100,y:116,"text-anchor":"middle","font-size":19,"font-weight":700,fill:"#102b52"},sv);
wrap.appendChild(sv);var lg=document.createElement("div");lg.className="dleg";
S.parts.forEach(function(p){var d=document.createElement("div");d.innerHTML='<i style="background:'+p.color+'"></i>'+p.name+"<em>"+fVal(p.v)+" · "+Math.round(p.v/tot*100)+"%</em>";lg.appendChild(d);
d.addEventListener("pointerenter",function(){S.parts.forEach(function(q){q.c.style.opacity=q===p?1:.25;q.c.setAttribute("stroke-width",q===p?32:26)})});d.addEventListener("pointerleave",function(){S.parts.forEach(function(q){q.c.style.opacity=1;q.c.setAttribute("stroke-width",26)})})});
wrap.appendChild(lg);W.appendChild(wrap);S.C=C}
function setDonut(t){var C=S.C,ang=ease(t)*C;S.parts.forEach(function(p){var l=clamp(ang-p.off,0,p.len);p.c.setAttribute("stroke-dasharray",l+" "+(C-l))});S.cv.textContent=S.cvf?fVal(S.cvn*ease(t)):S.cvt}
/* ---------------- driver ---------------- */
function build(){if(S.kind==="line")buildLine();else if(S.kind==="bars")buildBars();else buildDonut()}
function frame(t,mode){if(S.kind==="line")setLine(t,mode);else if(S.kind==="bars")setBars(t);else setDonut(t)}
function save(){if(S.kind==="line"){try{sessionStorage.setItem(KEY,JSON.stringify(S.series.map(function(s){return s.y})))}catch(e){}}}
function play(){cancelAnimationFrame(raf);build();var mode=(!played&&prev&&S.kind==="line")?"morph":"draw";played=true;
if(reduce){frame(1,"static");save();return}
var dur=S.kind==="line"?(mode==="morph"?650:1500):1300,t0=null;
function step(ts){if(t0===null)t0=ts;var t=clamp((ts-t0)/dur,0,1);frame(t,mode);if(t<1)raf=requestAnimationFrame(step);else{frame(1,mode==="morph"?"static":"static");save()}}
frame(0,mode);raf=requestAnimationFrame(step)}
function settle(){cancelAnimationFrame(raf);build();frame(1,"static")}
var vis=false;new IntersectionObserver(function(es){var v=es[0].isIntersecting;if(v&&!vis){vis=true;play()}else if(!v&&vis){vis=false;cancelAnimationFrame(raf)}},{threshold:.05}).observe(W);
var rz=null;new ResizeObserver(function(){if(!vis)return;clearTimeout(rz);rz=setTimeout(settle,120)}).observe(W);
})();
</script></body></html>'''


def _show_chart(spec, height):
    doc = CHART_DOC.replace("__SPEC__", json.dumps(spec, ensure_ascii=False).replace("<", "\\u003c"))
    if hasattr(st, "iframe"):
        st.iframe(doc, height=height)
    elif components is not None:
        components.html(doc, height=height)


def chart_line(cid, x, series, fmt="inr", ref=None, title=None, height=360):
    """Animated line chart. series is a list of (name, colour, values, dashed)."""
    n = len(x)
    idx = list(range(n)) if n <= 140 else [round(i * (n - 1) / 139) for i in range(140)]
    spec = {"kind": "line", "id": cid, "title": title, "fmt": fmt, "x": [str(x[i]) for i in idx], "ref": ref,
            "series": [{"name": html.escape(nm), "color": c, "dash": bool(d), "y": [round(float(v[i]), 2) for i in idx]}
                       for nm, c, v, d in series]}
    _show_chart(spec, height)


def chart_bars(cid, items, fmt="inr", title=None):
    spec = {"kind": "bars", "id": cid, "title": title, "fmt": fmt,
            "items": [{"l": html.escape(str(l)), "v": round(float(v), 2), "c": c} for l, v, c in items]}
    _show_chart(spec, 70 + 46 * len(items))


def chart_donut(cid, parts, center_label, center_text, fmt="inr", height=250):
    parts = [(nm, v, c) for nm, v, c in parts if v > 0]
    if not parts:
        return
    spec = {"kind": "donut", "id": cid, "fmt": fmt, "cl": center_label, "cvt": center_text,
            "parts": [{"name": html.escape(str(nm)), "v": round(float(v), 2), "color": c} for nm, v, c in parts]}
    _show_chart(spec, height)


PALETTE = ["#14306b", "#2f6bff", "#ff6b16", "#f5b301", "#0d9488", "#7b8fb0", "#9333ea", "#e11d48"]


def page_banner(name, title):
    """Shows a wide photo strip at the top of a page if images/<name>.jpg (or png/webp) exists."""
    u = img_uri(name, 1400)
    if u:
        st.markdown('<div class="pbanner" style="background-image:linear-gradient(90deg,rgba(11,31,77,.80),rgba(11,31,77,.12)),url(\'' + u + '\')"><h2>' + title + '</h2></div>',
                    unsafe_allow_html=True)


def go(label):
    st.session_state["nav"] = label


with home:
    with st.container(key="herobox"):
        hl, hr = st.columns([3, 2])
        with hl:
            st.markdown("""
<span class="pill">Free · No sign-up · Nothing is saved</span>
<h1>A clearer plan<br>for your money.</h1>
<p class="lead">Work out your SIP, your EMIs, your tax and your retirement number in a few minutes. Built around how Indian households actually save.</p>
""", unsafe_allow_html=True)
            b1, b2, _sp = st.columns([1.5, 2.0, 0.4])
            b1.button("Start planning", key="cta1", on_click=go, args=("Financial Health",))
            b2.button("Investment ideas", key="cta2", on_click=go, args=("Investment Ideas",))
            st.markdown('<div class="badges"><span>Formulas shown</span><span>FY 2026-27 tax rules</span><span>No ads, no products</span></div>',
                        unsafe_allow_html=True)
        with hr:
            hero_img = img_uri("hero", 1000)
            _mock = '<div class="mock"><div class="mmain"><div class="mtop"><i></i><i></i><i></i></div><small>Money health score</small><div class="big">78<em> / 100</em></div><div class="bar"><div style="width:78%;background:#16a34a"></div></div><svg viewBox="0 0 220 80"><rect x="6" y="52" width="26" height="28" rx="5" fill="#cfe0ff"/><rect x="42" y="42" width="26" height="38" rx="5" fill="#a9c6ff"/><rect x="78" y="32" width="26" height="48" rx="5" fill="#7fa8ff"/><rect x="114" y="22" width="26" height="58" rx="5" fill="#4d8bff"/><rect x="150" y="12" width="26" height="68" rx="5" fill="#2f6bff"/><rect x="186" y="2" width="26" height="78" rx="5" fill="#1747c4"/></svg></div><div class="mchip c1">Goal progress <b>72%</b></div><div class="mchip c2">Debt-free in <b>18 months</b></div><div class="mchip c3">Retire at <b>55</b></div></div><div class="sample">Example</div>'
            if hero_img:
                _i = _mock.index('<div class="mmain">')
                _j = _mock.index('<div class="mchip c1">')
                _mock = _mock[:_i] + f'<div class="mmain mphoto"><img src="{hero_img}"></div>' + _mock[_j:]
                _mock = _mock.replace('<div class="sample">Example</div>', '<div class="sample">AI-generated image</div>')
            st.markdown(_mock, unsafe_allow_html=True)

    with st.container(key="flowband"):
        if hasattr(st, "iframe"):
            st.iframe(FLOW_HTML, height=200)
        elif components is not None:
            components.html(FLOW_HTML, height=200)
        st.caption("Move your mouse over the word, or click it. The dots across the page follow your mouse too.")

    st.markdown("""
<div class="stats"><div><b>12</b><span>Tools</span></div><div><b>₹0</b><span>To use</span></div><div><b>0</b><span>Personal data stored</span></div><div><b>FY 26-27</b><span>Tax rules used</span></div></div>
<div class="sec"><h2>Pick what you want to work out</h2><p>Each tool opens on its own page.</p></div>
""", unsafe_allow_html=True)
    TILES = [("Financial Health", "monitor_heart"), ("Goal Planner", "flag"), ("Investment Ideas", "trending_up"),
             ("Child Education", "school"), ("Retirement", "beach_access"), ("Tax Saver", "receipt_long"),
             ("Calculators", "calculate"), ("EMI Manager", "credit_card"), ("Teen Savers", "savings"),
             ("Mutual Fund Lookup", "query_stats"), ("News", "newspaper"), ("AI Advisor", "forum")]
    for r in range(3):
        cols = st.columns(4)
        for c in range(4):
            name, icon = TILES[r * 4 + c]
            try:
                cols[c].button(name, icon=f":material/{icon}:", key=f"tile_{r * 4 + c}", on_click=go, args=(name,))
            except TypeError:      # older Streamlit without button icons
                cols[c].button(name, key=f"tile_{r * 4 + c}", on_click=go, args=(name,))

    _ICON = {
        "invest": '<svg viewBox="0 0 24 24"><polyline points="22 7 13.5 15.5 8.5 10.5 2 17"/><polyline points="16 7 22 7 22 13"/></svg>',
        "emi": '<svg viewBox="0 0 24 24"><rect width="20" height="14" x="2" y="5" rx="2"/><line x1="2" x2="22" y1="10" y2="10"/></svg>',
        "goal": '<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/></svg>',
        "lock": '<svg viewBox="0 0 24 24"><rect width="18" height="11" x="3" y="11" rx="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>',
        "sum": '<svg viewBox="0 0 24 24"><rect width="16" height="20" x="4" y="2" rx="2"/><line x1="8" x2="16" y1="6" y2="6"/><path d="M16 14v4"/><path d="M16 10h.01"/><path d="M12 10h.01"/><path d="M8 10h.01"/><path d="M12 14h.01"/><path d="M8 14h.01"/><path d="M12 18h.01"/><path d="M8 18h.01"/></svg>',
        "tag": '<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><path d="m4.9 4.9 14.2 14.2"/></svg>',
    }
    with st.container(key="featband"):
        st.markdown('<div class="sec"><h2>Where most people start</h2><p>Three tools that answer the questions people ask first.</p></div>', unsafe_allow_html=True)
        fcols = st.columns(3)
        FEAT = [("invest", "Investment Ideas", "A suggested split between equity, debt and gold, based on your age, how long you can wait, and how you handle a bad year.", "Investment Ideas"),
                ("emi", "EMI Manager", "List every loan you have. See which one to pay off first and how much interest that saves.", "EMI Manager"),
                ("goal", "Goal Planner", "Put a price and a date on a goal. See the monthly SIP, and what waiting a year would cost.", "Goal Planner")]
        for i, (ic, nm, ds, lb) in enumerate(FEAT):
            with fcols[i]:
                _pic = img_uri(["tool_invest", "tool_emi", "tool_goal"][i], 700)
                _top = (f'<div class="top" style="padding:0"><img src="{_pic}"></div>' if _pic else f'<div class="top">{_ICON[ic]}</div>')
                st.markdown(f'<div class="fc2">{_top}<div class="body"><b>{nm}</b><span>{ds}</span></div></div>', unsafe_allow_html=True)
                st.button("Open " + nm, key=f"feat_{i}", on_click=go, args=(lb,))

    _stories = [("story_1", "Your first savings goal"), ("story_2", "Becoming debt-free"),
                ("story_3", "Your child's future"), ("story_4", "Retiring on your terms")]
    _got = [(img_uri(k, 600), t) for k, t in _stories]
    _got = [(u, t) for u, t in _got if u]
    if _got:
        st.markdown('<div class="sec"><span>REAL GOALS</span><h2>Money plans for every stage of life</h2></div>', unsafe_allow_html=True)
        st.markdown('<div class="gal">' + "".join('<div class="gcard" style="background-image:url(\'' + u + '\')"><span>' + t + '</span></div>'
                                                 for u, t in _got) + "</div>", unsafe_allow_html=True)

    with st.container(key="lightband"):
        st.markdown(f"""
<div class="sec"><h2>How it works</h2></div>
<div class="steps"><div><i>1</i><b>Put in your numbers</b><span>A minute or less per tool.</span></div><div><i>2</i><b>Read the plan</b><span>Monthly amounts, scores and charts.</span></div><div><i>3</i><b>Ask if something is unclear</b><span>The AI page explains it in plain words.</span></div></div>
<div class="sec"><h2>What the app does, and what it does not</h2></div>
<div class="t3"><div><div class="ic">{_ICON["lock"]}</div><b>Saves nothing</b><span>What you type is not stored. Please keep PAN, Aadhaar and bank details out of the AI box.</span></div><div><div class="ic">{_ICON["sum"]}</div><b>Shows its sums</b><span>The formulas are listed at the bottom of every page, so you can check the working.</span></div><div><div class="ic">{_ICON["tag"]}</div><b>Sells nothing</b><span>No products, ads or commissions here. Suggestions are about types of investments, not brands.</span></div></div>
""", unsafe_allow_html=True)

    with st.container(key="ctaband"):
        _cta = img_uri("cta", 1400)
        if _cta:
            st.markdown("<style>.st-key-ctaband { background-image: linear-gradient(120deg, rgba(11,31,77,.90), rgba(20,48,107,.78)), url('" + _cta + "'); background-size: cover; background-position: center; }</style>", unsafe_allow_html=True)
        st.markdown("<h2>Start with your money health check</h2><p>It takes about a minute, and nothing is saved.</p>", unsafe_allow_html=True)
        _l, _m, _r = st.columns([2, 1.3, 2])
        _m.button("Begin", key="cta3", on_click=go, args=("Financial Health",))
        _ai_note = " Images on this page are AI-generated." if any(img_uri(k, 300) for k in ["hero", "tool_invest", "tool_emi", "tool_goal", "cta", "story_1", "story_2", "story_3", "story_4", "banner_health", "banner_goal", "banner_invest", "banner_education", "banner_retirement", "banner_tax", "banner_emi", "banner_teen", "banner_funds", "banner_ai"]) else ""
        st.markdown(f"<small>Educational tool for India. Not SEBI-registered investment advice.{_ai_note}</small>", unsafe_allow_html=True)



# ---------- helper maths ----------
def sip_factor(annual_return, years):
    r = annual_return / 12 / 100
    n = years * 12
    if r == 0:
        return n
    return (((1 + r) ** n - 1) / r) * (1 + r)


def sip_needed(target, annual_return, years, existing=0):
    grown = existing * (1 + annual_return / 100) ** years
    gap = max(target - grown, 0)
    return gap / sip_factor(annual_return, years)


def money(x):
    n = int(round(x))
    sign = "-" if n < 0 else ""
    d = str(abs(n))
    if len(d) > 3:
        head, tail, parts = d[:-3], d[-3:], []
        while len(head) > 2:
            parts.insert(0, head[-2:])
            head = head[:-2]
        if head:
            parts.insert(0, head)
        d = ",".join(parts) + "," + tail
    return f"{sign}₹{d}"


def short(x):
    if x >= 1e7:
        return f"₹{x / 1e7:.2f} Crore"
    if x >= 1e5:
        return f"₹{x / 1e5:.2f} Lakh"
    return money(x)


# ---------- TAX (EDIT THESE EACH FINANCIAL YEAR) ----------
# FY 2026-27 (AY 2027-28). Budget 2026 left the slabs, standard deduction, rebate and cess unchanged.
NEW_SLABS = [(400000, 0), (800000, 5), (1200000, 10), (1600000, 15),
             (2000000, 20), (2400000, 25), (float("inf"), 30)]
OLD_SLABS = {   # old regime, by age band: below 60, 60 to 79, 80 and above
    "below 60": [(250000, 0), (500000, 5), (1000000, 20), (float("inf"), 30)],
    "60 to 79": [(300000, 0), (500000, 5), (1000000, 20), (float("inf"), 30)],
    "80 and above": [(500000, 0), (1000000, 20), (float("inf"), 30)],
}
NEW_STD_DED, OLD_STD_DED = 75000, 50000
NEW_REBATE_LIMIT, NEW_REBATE_MAX = 1200000, 60000      # section 87A, new regime
OLD_REBATE_LIMIT, OLD_REBATE_MAX = 500000, 12500       # section 87A, old regime
SURCHARGE = [(5_000_000, 0.10), (10_000_000, 0.15), (20_000_000, 0.25), (50_000_000, 0.37)]
CESS = 0.04
CAPS = {"80c": 150000, "80d": 100000, "nps": 50000, "home_loan": 200000}


def slab_tax(income, slabs):
    tax, prev = 0.0, 0
    for upper, rate in slabs:
        if income > prev:
            tax += (min(income, upper) - prev) * rate / 100
        prev = upper
    return tax


def _surcharge_rate(income, new):
    rate = 0.0
    for limit, r in SURCHARGE:
        if income > limit:
            rate = min(r, 0.25) if new else r       # the new regime caps surcharge at 25%
    return rate


def _with_surcharge(income, base, new, tax_at):
    """Surcharge on top of the slab tax, with marginal relief just above each threshold."""
    rate = _surcharge_rate(income, new)
    if rate == 0:
        return 0.0
    total = base * (1 + rate)
    limit = max(l for l, _ in SURCHARGE if income > l)
    at_limit = tax_at(limit)
    cap = at_limit * (1 + _surcharge_rate(limit, new)) + (income - limit)
    return max(min(total, cap) - base, 0.0)


def new_regime(gross, salaried=True):
    std = NEW_STD_DED if salaried else 0
    taxable = max(gross - std, 0)
    slab = slab_tax(taxable, NEW_SLABS)
    rebate = relief = 0.0
    if taxable <= NEW_REBATE_LIMIT:
        rebate = min(slab, NEW_REBATE_MAX)
    elif slab > taxable - NEW_REBATE_LIMIT:           # marginal relief just above the rebate limit
        relief = slab - (taxable - NEW_REBATE_LIMIT)
    base = slab - rebate - relief
    sur = _with_surcharge(taxable, base, True, lambda t: max(slab_tax(t, NEW_SLABS) - (NEW_REBATE_MAX if t <= NEW_REBATE_LIMIT else 0), 0))
    cess = (base + sur) * CESS
    return dict(gross=gross, std=std, deductions=0, taxable=taxable, slab=slab, rebate=rebate, relief=relief,
                surcharge=sur, cess=cess, total=base + sur + cess)


def old_regime(gross, age_band="below 60", d80c=0, d80d=0, nps=0, home_loan=0, hra=0, salaried=True):
    std = OLD_STD_DED if salaried else 0
    ded = (min(d80c, CAPS["80c"]) + min(d80d, CAPS["80d"]) + min(nps, CAPS["nps"])
           + min(home_loan, CAPS["home_loan"]) + hra)
    taxable = max(gross - std - ded, 0)
    slabs = OLD_SLABS[age_band]
    slab = slab_tax(taxable, slabs)
    rebate = min(slab, OLD_REBATE_MAX) if taxable <= OLD_REBATE_LIMIT else 0.0
    base = slab - rebate
    sur = _with_surcharge(taxable, base, False, lambda t: slab_tax(t, slabs))
    cess = (base + sur) * CESS
    return dict(gross=gross, std=std, deductions=ded, taxable=taxable, slab=slab, rebate=rebate, relief=0.0,
                surcharge=sur, cess=cess, total=base + sur + cess)


def new_regime_tax(gross):
    return new_regime(gross)["total"]


# ---------- AI helper (Google Gemini free tier) ----------
def ask_ai(prompt):
    """Uses NVIDIA (free) if NVIDIA_API_KEY is set, otherwise Google Gemini if GEMINI_API_KEY is set."""
    # A public link means anyone can press the AI buttons, so each visit gets a fair share of your free quota.
    used = st.session_state.get("ai_calls", 0)
    if used >= 25:
        return "You have used all the AI answers for this visit. Reload the page to start a fresh visit."
    st.session_state["ai_calls"] = used + 1
    prompt = str(prompt)[:3000]
    def secret(name):
        try:
            return st.secrets.get(name, "")
        except Exception:
            return ""

    system = ("You are a careful Indian personal-finance educator. Explain options simply, "
              "mention risks, only suggest LEGAL tax-saving methods, and remind the user to "
              "verify with a SEBI-registered advisor or CA. Never ask for PAN, Aadhaar or bank details.")

    nv_key = secret("NVIDIA_API_KEY")
    if nv_key:
        model = secret("NVIDIA_MODEL") or "meta/llama-3.1-70b-instruct"  # change in secrets.toml if NVIDIA retires it
        try:
            r = requests.post(
                "https://integrate.api.nvidia.com/v1/chat/completions",
                headers={"Authorization": f"Bearer {nv_key}", "Accept": "application/json"},
                json={"model": model, "temperature": 0.5, "max_tokens": 1024, "stream": False,
                      "messages": [{"role": "system", "content": system},
                                   {"role": "user", "content": prompt}]},
                timeout=90)
            data = r.json()
            if "choices" in data:
                msg = data["choices"][0]["message"]
                return msg.get("content") or msg.get("reasoning_content") or "The AI sent an empty answer. Try again."
            err = data.get("detail") or data.get("error") or data.get("message") or str(data)
            return f"The NVIDIA service replied with a problem: {err}"
        except Exception as e:
            return f"Could not reach the NVIDIA service: {e}"

    gem_key = secret("GEMINI_API_KEY")
    if gem_key:
        model = "gemini-3.8-flash"  # Google renames models often
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
        body = {"contents": [{"parts": [{"text": system + "\n\n" + prompt}]}]}
        try:
            r = requests.post(url, headers={"x-goog-api-key": gem_key}, json=body, timeout=40)
            data = r.json()
            if "candidates" in data:
                return data["candidates"][0]["content"]["parts"][0]["text"]
            err = data.get("error", {}).get("message", str(data))
            return f"The AI service replied with a problem: {err}"
        except Exception as e:
            return f"Could not reach the AI service: {e}"

    return ("AI key not found. Create the file .streamlit/secrets.toml in your project folder "
            "with the line: NVIDIA_API_KEY = \"your-key\", then restart the app.")


_LOGO = '<svg width="72" height="72" viewBox="0 0 72 72" xmlns="http://www.w3.org/2000/svg"><circle cx="36" cy="36" r="33" fill="none" stroke="#f5b301" stroke-width="3"/><circle cx="36" cy="36" r="24" fill="#f5b301"/><text x="36" y="46" font-size="28" font-weight="700" text-anchor="middle" fill="#14306b">₹</text><polygon points="36,3 41,16 31,16" fill="#ffffff"/></svg>'
PAGES = ["Home", "Financial Health", "Goal Planner", "Investment Ideas", "Child Education", "Retirement",
         "Tax Saver", "Calculators", "EMI Manager", "Teen Savers", "Mutual Fund Lookup", "News", "AI Advisor"]
PAGE_KEY = [None, 0, 1, 9, 2, 3, 4, 11, 8, 7, 5, 10, 6]   # which content block each menu item opens
with st.sidebar:
    st.markdown(f'<div class="sb">{_LOGO}<h2>Dhan Disha</h2><p>Your direction for wealth</p><p style="font-size:.7rem;opacity:.55;margin-top:-6px">Version 14</p></div>',
                unsafe_allow_html=True)
    page = st.radio("Menu", PAGES, label_visibility="collapsed", key="nav")
_sel = PAGES.index(page)
_hide = "" if _sel == 0 else '[data-testid="stLayoutWrapper"]:has(> .st-key-home), .st-key-home{display:none;}'
for _i, _k in enumerate(PAGE_KEY):
    if _k is not None and _i != _sel:
        _hide += f'[data-testid="stLayoutWrapper"]:has(> .st-key-page_{_k}), .st-key-page_{_k}{{display:none;}}'
st.markdown(f"<style>{_hide}</style>", unsafe_allow_html=True)
# Shared visual system for the non-home pages. The Home page's layout remains untouched.
st.markdown(r"""
<style>
/* Dhan Disha interior pages: high-contrast, airy fintech dashboard */
.st-key-page_0, .st-key-page_1, .st-key-page_2, .st-key-page_3, .st-key-page_4,
.st-key-page_5, .st-key-page_6, .st-key-page_7, .st-key-page_8, .st-key-page_9, .st-key-page_10, .st-key-page_11 {
  background: transparent; color:#142746; padding: 0 2px 20px 2px;
}
.st-key-page_0 h1, .st-key-page_1 h1, .st-key-page_2 h1, .st-key-page_3 h1,
.st-key-page_4 h1, .st-key-page_5 h1, .st-key-page_6 h1, .st-key-page_7 h1,
.st-key-page_8 h1, .st-key-page_9 h1,
.st-key-page_0 h2, .st-key-page_1 h2, .st-key-page_2 h2, .st-key-page_3 h2,
.st-key-page_4 h2, .st-key-page_5 h2, .st-key-page_6 h2, .st-key-page_7 h2,
.st-key-page_8 h2, .st-key-page_9 h2,
.st-key-page_0 h3, .st-key-page_1 h3, .st-key-page_2 h3, .st-key-page_3 h3,
.st-key-page_4 h3, .st-key-page_5 h3, .st-key-page_6 h3, .st-key-page_7 h3,
.st-key-page_8 h3, .st-key-page_9 h3 { color:#102a56 !important; letter-spacing:-.02em; font-weight:700; }
.st-key-page_0 p, .st-key-page_1 p, .st-key-page_2 p, .st-key-page_3 p,
.st-key-page_4 p, .st-key-page_5 p, .st-key-page_6 p, .st-key-page_7 p,
.st-key-page_8 p, .st-key-page_9 p,
.st-key-page_0 label, .st-key-page_1 label, .st-key-page_2 label, .st-key-page_3 label,
.st-key-page_4 label, .st-key-page_5 label, .st-key-page_6 label, .st-key-page_7 label,
.st-key-page_8 label, .st-key-page_9 label,
.st-key-page_0 [data-testid="stMarkdownContainer"], .st-key-page_1 [data-testid="stMarkdownContainer"],
.st-key-page_2 [data-testid="stMarkdownContainer"], .st-key-page_3 [data-testid="stMarkdownContainer"],
.st-key-page_4 [data-testid="stMarkdownContainer"], .st-key-page_5 [data-testid="stMarkdownContainer"],
.st-key-page_6 [data-testid="stMarkdownContainer"], .st-key-page_7 [data-testid="stMarkdownContainer"],
.st-key-page_8 [data-testid="stMarkdownContainer"], .st-key-page_9 [data-testid="stMarkdownContainer"] { color:#243b5a; }
.st-key-page_0 [data-testid="stCaptionContainer"], .st-key-page_1 [data-testid="stCaptionContainer"],
.st-key-page_2 [data-testid="stCaptionContainer"], .st-key-page_3 [data-testid="stCaptionContainer"],
.st-key-page_4 [data-testid="stCaptionContainer"], .st-key-page_5 [data-testid="stCaptionContainer"],
.st-key-page_6 [data-testid="stCaptionContainer"], .st-key-page_7 [data-testid="stCaptionContainer"],
.st-key-page_8 [data-testid="stCaptionContainer"], .st-key-page_9 [data-testid="stCaptionContainer"] { color:#526782 !important; }
.st-key-page_0 [data-baseweb="input"] > div, .st-key-page_1 [data-baseweb="input"] > div,
.st-key-page_2 [data-baseweb="input"] > div, .st-key-page_3 [data-baseweb="input"] > div,
.st-key-page_4 [data-baseweb="input"] > div, .st-key-page_5 [data-baseweb="input"] > div,
.st-key-page_6 [data-baseweb="input"] > div, .st-key-page_7 [data-baseweb="input"] > div,
.st-key-page_8 [data-baseweb="input"] > div, .st-key-page_9 [data-baseweb="input"] > div,
.st-key-page_0 [data-baseweb="select"] > div, .st-key-page_1 [data-baseweb="select"] > div,
.st-key-page_2 [data-baseweb="select"] > div, .st-key-page_3 [data-baseweb="select"] > div,
.st-key-page_4 [data-baseweb="select"] > div, .st-key-page_5 [data-baseweb="select"] > div,
.st-key-page_6 [data-baseweb="select"] > div, .st-key-page_7 [data-baseweb="select"] > div,
.st-key-page_8 [data-baseweb="select"] > div, .st-key-page_9 [data-baseweb="select"] > div,
.st-key-page_0 [data-baseweb="textarea"] > div, .st-key-page_1 [data-baseweb="textarea"] > div,
.st-key-page_2 [data-baseweb="textarea"] > div, .st-key-page_3 [data-baseweb="textarea"] > div,
.st-key-page_4 [data-baseweb="textarea"] > div, .st-key-page_5 [data-baseweb="textarea"] > div,
.st-key-page_6 [data-baseweb="textarea"] > div, .st-key-page_7 [data-baseweb="textarea"] > div,
.st-key-page_8 [data-baseweb="textarea"] > div, .st-key-page_9 [data-baseweb="textarea"] > div { background:#fff !important; border:1px solid #d8e4f2 !important; border-radius:12px !important; }
.st-key-page_0 input, .st-key-page_1 input, .st-key-page_2 input, .st-key-page_3 input,
.st-key-page_4 input, .st-key-page_5 input, .st-key-page_6 input, .st-key-page_7 input,
.st-key-page_8 input, .st-key-page_9 input,
.st-key-page_0 textarea, .st-key-page_1 textarea, .st-key-page_2 textarea, .st-key-page_3 textarea,
.st-key-page_4 textarea, .st-key-page_5 textarea, .st-key-page_6 textarea, .st-key-page_7 textarea,
.st-key-page_8 textarea, .st-key-page_9 textarea { color:#172b4d !important; -webkit-text-fill-color:#172b4d !important; }
.st-key-page_0 [data-testid="stMetric"], .st-key-page_1 [data-testid="stMetric"],
.st-key-page_2 [data-testid="stMetric"], .st-key-page_3 [data-testid="stMetric"],
.st-key-page_4 [data-testid="stMetric"], .st-key-page_5 [data-testid="stMetric"],
.st-key-page_6 [data-testid="stMetric"], .st-key-page_7 [data-testid="stMetric"],
.st-key-page_8 [data-testid="stMetric"], .st-key-page_9 [data-testid="stMetric"] { background:#fff; border:1px solid #e0eaf6; border-radius:16px; padding:16px 18px; box-shadow:0 5px 18px rgba(25,64,112,.07); }
.st-key-page_0 [data-testid="stMetricLabel"], .st-key-page_1 [data-testid="stMetricLabel"],
.st-key-page_2 [data-testid="stMetricLabel"], .st-key-page_3 [data-testid="stMetricLabel"],
.st-key-page_4 [data-testid="stMetricLabel"], .st-key-page_5 [data-testid="stMetricLabel"],
.st-key-page_6 [data-testid="stMetricLabel"], .st-key-page_7 [data-testid="stMetricLabel"],
.st-key-page_8 [data-testid="stMetricLabel"], .st-key-page_9 [data-testid="stMetricLabel"] { color:#526782 !important; }
.st-key-page_0 [data-testid="stMetricValue"], .st-key-page_1 [data-testid="stMetricValue"],
.st-key-page_2 [data-testid="stMetricValue"], .st-key-page_3 [data-testid="stMetricValue"],
.st-key-page_4 [data-testid="stMetricValue"], .st-key-page_5 [data-testid="stMetricValue"],
.st-key-page_6 [data-testid="stMetricValue"], .st-key-page_7 [data-testid="stMetricValue"],
.st-key-page_8 [data-testid="stMetricValue"], .st-key-page_9 [data-testid="stMetricValue"] { color:#102a56 !important; font-weight:750; }
.st-key-page_0 [data-testid="stAlert"], .st-key-page_1 [data-testid="stAlert"],
.st-key-page_2 [data-testid="stAlert"], .st-key-page_3 [data-testid="stAlert"],
.st-key-page_4 [data-testid="stAlert"], .st-key-page_5 [data-testid="stAlert"],
.st-key-page_6 [data-testid="stAlert"], .st-key-page_7 [data-testid="stAlert"],
.st-key-page_8 [data-testid="stAlert"], .st-key-page_9 [data-testid="stAlert"] { border-radius:14px; border:1px solid #dce8f5; }
.st-key-page_0 button[kind="primary"], .st-key-page_1 button[kind="primary"],
.st-key-page_2 button[kind="primary"], .st-key-page_3 button[kind="primary"],
.st-key-page_4 button[kind="primary"], .st-key-page_5 button[kind="primary"],
.st-key-page_6 button[kind="primary"], .st-key-page_7 button[kind="primary"],
.st-key-page_8 button[kind="primary"], .st-key-page_9 button[kind="primary"] { background:linear-gradient(100deg,#f47721,#ff9d32) !important; border:0 !important; color:white !important; border-radius:12px !important; font-weight:650; }
.st-key-page_0 button, .st-key-page_1 button, .st-key-page_2 button, .st-key-page_3 button,
.st-key-page_4 button, .st-key-page_5 button, .st-key-page_6 button, .st-key-page_7 button,
.st-key-page_8 button, .st-key-page_9 button { border-radius:12px; }
.st-key-page_0 [data-testid="stVegaLiteChart"], .st-key-page_1 [data-testid="stVegaLiteChart"],
.st-key-page_2 [data-testid="stVegaLiteChart"], .st-key-page_3 [data-testid="stVegaLiteChart"],
.st-key-page_4 [data-testid="stVegaLiteChart"], .st-key-page_5 [data-testid="stVegaLiteChart"],
.st-key-page_6 [data-testid="stVegaLiteChart"], .st-key-page_7 [data-testid="stVegaLiteChart"],
.st-key-page_8 [data-testid="stVegaLiteChart"], .st-key-page_9 [data-testid="stVegaLiteChart"] { background:#fff; border:1px solid #e3ebf5; border-radius:16px; padding:10px; }
.st-key-page_0 .pbanner, .st-key-page_1 .pbanner, .st-key-page_2 .pbanner, .st-key-page_3 .pbanner,
.st-key-page_4 .pbanner, .st-key-page_5 .pbanner, .st-key-page_6 .pbanner, .st-key-page_7 .pbanner,
.st-key-page_8 .pbanner, .st-key-page_9 .pbanner { border-radius:18px; box-shadow:0 7px 22px rgba(23,57,99,.12); overflow:hidden; }
.st-key-page_0 .score, .st-key-page_1 .score, .st-key-page_2 .score, .st-key-page_3 .score,
.st-key-page_4 .score, .st-key-page_5 .score, .st-key-page_6 .score, .st-key-page_7 .score,
.st-key-page_8 .score, .st-key-page_9 .score { background:#fff; border:1px solid #e1eaf5; border-radius:16px; box-shadow:0 5px 18px rgba(25,64,112,.06); color:#243b5a; }
</style>
""", unsafe_allow_html=True)

# Readability fixes: solid panels behind page content, dark text on light surfaces.
st.markdown(r"""
<style>
.st-key-page_0, .st-key-page_1, .st-key-page_2, .st-key-page_3, .st-key-page_4,
.st-key-page_5, .st-key-page_6, .st-key-page_7, .st-key-page_8, .st-key-page_9, .st-key-page_10, .st-key-page_11 {
  background: rgba(255,255,255,.95) !important; border: 1px solid #dfe9f7; border-radius: 22px;
  padding: 26px 30px 30px 30px !important; box-shadow: 0 10px 30px rgba(24,56,107,.08);
}
[data-testid="stSidebar"] .sb, [data-testid="stSidebar"] .sb * { color: #2a4468 !important; }
[data-testid="stSidebar"] .sb h2, [data-testid="stSidebar"] .sb h2 * { color: #102b52 !important; }
[data-testid="stSidebar"] .sb p { color: #6b82a6 !important; }
[data-testid="stSidebar"] .sb b { color: #102b52 !important; }
[data-testid="stSidebar"] .sb hr { border-color: #d9e6f7 !important; }
.st-key-home .stats b { color: #102b52 !important; text-shadow: none !important; }
.st-key-home .stats span { color: #4c6489 !important; }
.st-key-home .sec { background: rgba(248,250,252,.94); border-radius: 16px; padding: 10px 20px; max-width: 560px; margin: 30px auto 14px auto; }
.st-key-home .steps > div, .st-key-home .t3 > div { border: 1px solid #e0ebfa; }
[data-testid="stExpander"] { background: #ffffff; border-radius: 14px; border: 1px solid #dfe9f7; }
[data-testid="stCaptionContainer"] p, [data-testid="stCaptionContainer"] { color: #4c6489 !important; }
</style>
""", unsafe_allow_html=True)


# Motion for the inner pages: cascade-in, animated headings, chart reveal, hover and focus effects.
st.markdown(r"""
<style>
@keyframes cascade { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: none; } }
@keyframes underline { from { transform: scaleX(0); } to { transform: scaleX(1); } }
@keyframes popin { 0% { opacity: 0; transform: scale(.88) translateY(10px); } 70% { transform: scale(1.03); } 100% { opacity: 1; transform: none; } }
@keyframes reveal { from { clip-path: inset(0 100% 0 0 round 16px); opacity: .2; } to { clip-path: inset(0 0 0 0 round 16px); opacity: 1; } }
@keyframes sheen { from { left: -60%; } to { left: 130%; } }
@keyframes barflow { from { background-position: 0% 0; } to { background-position: 200% 0; } }
@keyframes kenburns { from { background-size: 100% auto; background-position: 50% 40%; } to { background-size: 112% auto; background-position: 50% 60%; } }
@keyframes stripes { from { background-position: 0 0; } to { background-position: 40px 0; } }
@keyframes emojiwave { 0%, 100% { transform: rotate(0); } 25% { transform: rotate(-10deg) scale(1.1); } 75% { transform: rotate(10deg) scale(1.1); } }
[class*="st-key-page_"] { position: relative; }
[class*="st-key-page_"]::before { content: ""; position: absolute; top: 0; left: 26px; right: 26px; height: 4px; border-radius: 0 0 8px 8px; background: linear-gradient(90deg, #2f6bff, #ff6b16, #f5b301, #2f6bff); background-size: 200% 100%; animation: barflow 5s linear infinite; pointer-events: none; }
[class*="st-key-page_"] > * { animation: cascade .6s cubic-bezier(.2,.8,.2,1) backwards; }
[class*="st-key-page_"] > *:nth-child(1) { animation-delay: 0.06s; }
[class*="st-key-page_"] > *:nth-child(2) { animation-delay: 0.12s; }
[class*="st-key-page_"] > *:nth-child(3) { animation-delay: 0.18s; }
[class*="st-key-page_"] > *:nth-child(4) { animation-delay: 0.24s; }
[class*="st-key-page_"] > *:nth-child(5) { animation-delay: 0.30s; }
[class*="st-key-page_"] > *:nth-child(6) { animation-delay: 0.36s; }
[class*="st-key-page_"] > *:nth-child(7) { animation-delay: 0.42s; }
[class*="st-key-page_"] > *:nth-child(8) { animation-delay: 0.48s; }
[class*="st-key-page_"] > *:nth-child(9) { animation-delay: 0.54s; }
[class*="st-key-page_"] > *:nth-child(10) { animation-delay: 0.60s; }
[class*="st-key-page_"] > *:nth-child(11) { animation-delay: 0.66s; }
[class*="st-key-page_"] > *:nth-child(12) { animation-delay: 0.70s; }
[class*="st-key-page_"] > *:nth-child(13) { animation-delay: 0.70s; }
[class*="st-key-page_"] > *:nth-child(14) { animation-delay: 0.70s; }
[class*="st-key-page_"] h3 { position: relative; display: inline-block; margin-bottom: 12px; }
[class*="st-key-page_"] h3::after { content: ""; position: absolute; left: 0; bottom: -5px; width: 100%; height: 3px; border-radius: 3px; background: linear-gradient(90deg, #ff6b16, #2f6bff); transform-origin: left; animation: underline .9s .35s cubic-bezier(.2,.8,.2,1) backwards; }
[class*="st-key-page_"] div[data-testid="stMetric"] { position: relative; overflow: hidden; animation: popin .65s cubic-bezier(.2,.9,.3,1.1) backwards; transition: transform .25s, box-shadow .25s, border-color .25s; }
[class*="st-key-page_"] [data-testid="stColumn"]:nth-child(2) div[data-testid="stMetric"] { animation-delay: .12s; }
[class*="st-key-page_"] [data-testid="stColumn"]:nth-child(3) div[data-testid="stMetric"] { animation-delay: .24s; }
[class*="st-key-page_"] div[data-testid="stMetric"]:hover { transform: translateY(-5px); border-color: #2f6bff; box-shadow: 0 14px 28px rgba(47,107,255,.18); }
[class*="st-key-page_"] div[data-testid="stMetric"]::after { content: ""; position: absolute; top: 0; left: -60%; width: 40%; height: 100%; background: linear-gradient(100deg, transparent, rgba(255,255,255,.75), transparent); transform: skewX(-20deg); pointer-events: none; }
[class*="st-key-page_"] div[data-testid="stMetric"]:hover::after { animation: sheen .9s ease; }
[class*="st-key-page_"] [data-testid="stVegaLiteChart"], [class*="st-key-page_"] [data-testid="stArrowVegaLiteChart"], [class*="st-key-page_"] [data-testid="stDataFrame"], [class*="st-key-page_"] [data-testid="stDataEditor"] { animation: reveal 1.1s .15s cubic-bezier(.2,.8,.2,1) backwards; }
[class*="st-key-page_"] [data-testid="stAlert"] { animation: slidein .6s cubic-bezier(.2,.9,.3,1.1) backwards; transition: transform .25s, box-shadow .25s; }
[class*="st-key-page_"] [data-testid="stAlert"]:hover { transform: translateX(4px); box-shadow: 0 8px 20px rgba(24,56,107,.10); }
[class*="st-key-page_"] .score { transition: transform .25s, box-shadow .25s; }
[class*="st-key-page_"] .score:hover { transform: translateY(-4px); box-shadow: 0 14px 28px rgba(24,56,107,.14); }
[class*="st-key-page_"] .bar > div { background-image: repeating-linear-gradient(135deg, rgba(255,255,255,.28) 0 10px, transparent 10px 20px); background-size: 40px 40px; animation: fillbar 1.3s ease-out both, stripes 1.2s linear infinite; }
[class*="st-key-page_"] [data-baseweb="input"], [class*="st-key-page_"] [data-baseweb="select"] > div, [class*="st-key-page_"] [data-baseweb="textarea"] { transition: box-shadow .25s, transform .25s, border-color .25s; }
[class*="st-key-page_"] [data-baseweb="input"]:hover, [class*="st-key-page_"] [data-baseweb="select"] > div:hover { box-shadow: 0 4px 14px rgba(24,56,107,.10); }
[class*="st-key-page_"] [data-baseweb="input"]:focus-within, [class*="st-key-page_"] [data-baseweb="select"] > div:focus-within, [class*="st-key-page_"] [data-baseweb="textarea"]:focus-within { box-shadow: 0 0 0 3px rgba(47,107,255,.25), 0 8px 18px rgba(47,107,255,.14); transform: translateY(-1px); }
[class*="st-key-page_"] [role="slider"] { transition: box-shadow .25s; }
[class*="st-key-page_"] [role="slider"]:hover, [class*="st-key-page_"] [role="slider"]:focus { box-shadow: 0 0 0 9px rgba(47,107,255,.18); }
[class*="st-key-page_"] [data-testid="stRadio"] label, [class*="st-key-page_"] [data-testid="stCheckbox"] label { transition: transform .2s, color .2s; }
[class*="st-key-page_"] [data-testid="stRadio"] label:hover, [class*="st-key-page_"] [data-testid="stCheckbox"] label:hover { transform: translateX(4px); }
[class*="st-key-page_"] .stButton > button { background: linear-gradient(100deg, #2f6bff, #14306b, #2f6bff) !important; background-size: 200% 100% !important; border: none !important; border-radius: 12px !important; transition: background-position .6s, transform .18s, box-shadow .18s; }
[class*="st-key-page_"] .stButton > button p { color: #ffffff !important; font-weight: 600; }
[class*="st-key-page_"] .stButton > button:hover { background-position: 100% 0 !important; transform: translateY(-2px); box-shadow: 0 10px 22px rgba(47,107,255,.32); }
[class*="st-key-page_"] .stButton > button:active { transform: scale(.97); }
[class*="st-key-page_"] .pbanner { animation: fadeup .5s ease both, kenburns 16s ease-in-out infinite alternate; }
[class*="st-key-page_"] .pbanner h2 { animation: cascade .8s .2s backwards; }
[class*="st-key-page_"] [data-testid="stExpander"] details[open] > div:last-child { animation: cascade .45s ease backwards; }
[class*="st-key-page_"] .fc2, [class*="st-key-page_"] .t3 > div { transition: transform .25s, box-shadow .25s; }
@media (prefers-reduced-motion: reduce) { [class*="st-key-page_"], [class*="st-key-page_"] * { animation: none !important; transition: none !important; } }
</style>
""", unsafe_allow_html=True)


# Calmer styling: fewer gradients and bounces, left-aligned headings, real icons, solid buttons.
st.markdown(r"""
<style>
[class*="st-key-page_"]::before { display: none !important; }
[class*="st-key-page_"] h3::after { width: 44px !important; height: 3px !important; background: #ff6b16 !important; }
[class*="st-key-page_"] div[data-testid="stMetric"] { animation: cascade .5s ease backwards !important; }
[class*="st-key-page_"] div[data-testid="stMetric"]::after { display: none !important; }
[class*="st-key-page_"] .bar > div { background-image: none !important; animation: fillbar 1.3s ease-out both !important; }
[class*="st-key-page_"] .stButton > button { background: #14306b !important; background-size: auto !important; }
[class*="st-key-page_"] .stButton > button:hover { background: #2f6bff !important; transform: none; box-shadow: 0 6px 16px rgba(47,107,255,.25); }
[class*="st-key-page_"] iframe { border: 1px solid #e4ecf8 !important; border-radius: 14px; background: #ffffff; }
.taxcard { background: #fff; border: 1px solid #e0ebfa; border-radius: 14px; padding: 16px 20px 12px 20px; box-shadow: 0 4px 14px rgba(24,56,107,.06); margin-bottom: 12px; }
.taxcard .tt { font-weight: 600; color: #102b52; display: flex; align-items: center; }
.taxcard .tv { font-size: 2rem; font-weight: 700; color: #102b52; margin: 4px 0 8px 0; }
.taxcard .trow { display: flex; justify-content: space-between; font-size: .9rem; padding: 6px 0; border-top: 1px solid #edf2fb; color: #33507a; }
.taxcard .trow b { color: #102b52; font-weight: 600; }
.tag { background: #e6f6ec; color: #15803d; border-radius: 999px; padding: 2px 10px; font-size: .72rem; font-weight: 600; margin-left: 10px; }
.st-key-home .sec { text-align: left !important; background: transparent !important; max-width: none !important; padding: 0 !important; margin: 38px 0 14px 0 !important; }
.st-key-home .sec > span { display: none !important; }
.st-key-home .sec h2 { font-size: 1.5rem !important; }
.st-key-home .sec > p { margin-top: 2px !important; }
[class*="st-key-tile_"] button > div { justify-content: center; width: 100%; }
[class*="st-key-tile_"] button > div > span { display: flex !important; flex-direction: column !important; align-items: center; gap: 8px; }
[class*="st-key-tile_"] button [data-testid="stMarkdownContainer"] p, [class*="st-key-tile_"] button [data-testid="stMarkdownContainer"] p:first-child { font-size: .95rem !important; font-weight: 600; line-height: 1.25; text-align: center; }
[class*="st-key-tile_"] button [data-testid="stIconMaterial"] { font-size: 1.9rem !important; color: #2f6bff !important; }
.fc2 .top svg { width: 44px; height: 44px; stroke: #2f6bff; fill: none; stroke-width: 1.7; stroke-linecap: round; stroke-linejoin: round; }
.ngrid { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 14px; margin-top: 10px; }
.ncard { display: flex; flex-direction: column; gap: 8px; padding: 16px 18px; background: #fff; border: 1px solid #e0ebfa; border-radius: 14px; text-decoration: none !important; transition: transform .2s, box-shadow .2s, border-color .2s; animation: cascade .5s ease backwards; }
.ncard:hover { transform: translateY(-4px); border-color: #2f6bff; box-shadow: 0 12px 24px rgba(47,107,255,.14); }
.ncard b { color: #102b52 !important; font-size: .98rem; line-height: 1.35; font-weight: 600; }
.ncard .nsrc { font-size: .75rem; color: #2f6bff !important; font-weight: 600; }
.ncard .nago { font-size: .75rem; color: #6b82a6 !important; margin-top: auto; }
.ncard:nth-child(2) { animation-delay: .05s; } .ncard:nth-child(3) { animation-delay: .1s; } .ncard:nth-child(4) { animation-delay: .15s; } .ncard:nth-child(5) { animation-delay: .2s; } .ncard:nth-child(6) { animation-delay: .25s; }
.t3 .ic svg { width: 26px; height: 26px; stroke: #2f6bff; fill: none; stroke-width: 1.8; stroke-linecap: round; stroke-linejoin: round; }
</style>
""", unsafe_allow_html=True)


# Version 14 polish: pill selectors, tighter menu, readable labels and focus outlines.
st.markdown(r"""
<style>
.st-key-calc_kind [data-testid="stRadioGroup"], .st-key-news_topic [data-testid="stRadioGroup"], .st-key-gst_mode [data-testid="stRadioGroup"] { gap: 8px; flex-wrap: wrap; }
.st-key-calc_kind label[data-testid="stRadioOption"], .st-key-news_topic label[data-testid="stRadioOption"], .st-key-gst_mode label[data-testid="stRadioOption"] {
  background: #eef3fb; border: 1px solid #dbe5f5; border-radius: 999px; padding: 7px 16px; margin: 0 !important; cursor: pointer; transition: background .2s, border-color .2s, transform .2s; }
.st-key-calc_kind label[data-testid="stRadioOption"] > div > div:first-child, .st-key-news_topic label[data-testid="stRadioOption"] > div > div:first-child, .st-key-gst_mode label[data-testid="stRadioOption"] > div > div:first-child { display: none !important; }
.st-key-calc_kind label[data-testid="stRadioOption"]:hover, .st-key-news_topic label[data-testid="stRadioOption"]:hover, .st-key-gst_mode label[data-testid="stRadioOption"]:hover { border-color: #2f6bff; transform: none; }
.st-key-calc_kind label[data-selected="true"], .st-key-news_topic label[data-selected="true"], .st-key-gst_mode label[data-selected="true"] { background: #14306b; border-color: #14306b; }
.st-key-calc_kind label[data-selected="true"] p, .st-key-news_topic label[data-selected="true"] p, .st-key-gst_mode label[data-selected="true"] p { color: #ffffff !important; font-weight: 600; }
[data-testid="stSidebar"] [role="radiogroup"] { gap: 1px !important; }
[data-testid="stSidebar"] [data-testid="stRadio"] label[data-testid="stRadioOption"] { padding-top: 7px !important; padding-bottom: 7px !important; }
[data-testid="stMetricLabel"] p, [data-testid="stMetricLabel"] div { white-space: normal !important; overflow: visible !important; text-overflow: clip !important; }
.st-key-herobox .sample { background: rgba(255,255,255,.85); color: #33507a !important; border-radius: 999px; padding: 2px 10px; display: inline-block; opacity: 1 !important; }
[data-testid="stMain"] button:focus-visible { outline: 2px solid #2f6bff; outline-offset: 2px; }
[data-testid="stMetricValue"], [data-testid="stMetricValue"] > div { white-space: normal !important; overflow: visible !important; text-overflow: clip !important; font-size: clamp(1.3rem, 2vw, 2rem) !important; line-height: 1.15; }
</style>
""", unsafe_allow_html=True)

tabs = [st.container(key=f"page_{i}") for i in range(12)]

# ---------- 1. Financial health ----------
with tabs[0]:
    page_banner("banner_health", "Financial Health")
    st.subheader("Monthly financial health check")
    left, right = st.columns([5, 7], gap="large")
    with left:
        income = st.number_input("Monthly income (₹)", 0, value=80000, step=5000)
        expenses = st.number_input("Monthly expenses (₹)", 0, value=45000, step=5000)
        emi = st.number_input("Monthly loan EMIs (₹)", 0, value=10000, step=1000)
        savings = st.number_input("Emergency savings now (₹)", 0, value=100000, step=10000)
    with right:
        if income <= 0:
            st.info("Enter your monthly income to see your score.")
        else:
            invest = income - expenses - emi
            months = savings / max(expenses + emi, 1)
            m1, m2, m3 = st.columns(3)
            m1.metric("Left to save", money(invest), help="Income minus expenses and EMIs, every month.")
            m2.metric("EMIs vs income", f"{emi / income * 100:.0f}%", help="Aim to keep this below 40%.")
            m3.metric("Safety net", f"{months:.1f} mo", help="How many months of expenses your emergency savings cover. Aim for 6.")
            st.caption(f"A common split of your income: needs {money(income * .5)}, wants {money(income * .3)}, savings {money(income * .2)}.")
            if months < 6:
                st.warning("Build your emergency fund first (liquid fund or savings account) before risky investing.")
            if emi / income > 0.4:
                st.warning("High EMI burden. Consider prepaying the costliest loan first.")
            s_save = min(max(invest, 0) / income / 0.2, 1) * 40
            s_emi = max(0, 1 - max(emi / income - 0.2, 0) / 0.3) * 30
            s_fund = min(months / 6, 1) * 30
            total = round(s_save + s_emi + s_fund)
            col = "#16a34a" if total >= 70 else "#f59e0b" if total >= 40 else "#dc2626"
            label = "Strong" if total >= 70 else "Fair" if total >= 40 else "Needs attention"
            st.markdown(f'<div class="score"><b>Your money health score</b><br>'
                        f'<span style="font-size:2.4rem;font-weight:700;color:{col}">{total}/100</span> '
                        f'<span style="color:{col};font-weight:600">{label}</span>'
                        f'<div class="bar"><div style="width:{total}%;background:{col}"></div></div></div>',
                        unsafe_allow_html=True)
            chart_donut("health", [("Living expenses", expenses, "#14306b"), ("EMIs", emi, "#ff6b16"),
                                   ("Left to save", max(invest, 0), "#2f6bff")], "Left to save", money(max(invest, 0)))
            if months < 3:
                step = "Build your emergency fund first: aim for 3 to 6 months of expenses in a savings account or liquid fund."
            elif emi / income > 0.4:
                step = "Reduce your EMI burden: put extra money on the costliest loan (see the EMI Manager tab)."
            elif invest / income < 0.2:
                step = "Raise your savings towards 20% of income. Even a small SIP increase helps."
            else:
                step = "You are in good shape. Start a goal-based SIP for your biggest goal (see the Goal Planner tab)."
            st.markdown(f'<div class="score" style="border-left:6px solid #f5b301"><b>Next step</b><br>{step}</div>',
                        unsafe_allow_html=True)

# ---------- 2. Goal planner ----------
with tabs[1]:
    page_banner("banner_goal", "Goal Planner")
    st.subheader("Plan any goal (house, car, wedding, travel)")
    left, right = st.columns([5, 7], gap="large")
    with left:
        goal = st.text_input("Goal name", "Buy a car")
        cost = st.number_input("Cost today (₹)", 0, value=1000000, step=50000, key="g1")
        yrs = st.slider("Years to goal", 1, 30, 5, key="g2")
        infl = st.slider("Expected inflation %", 0.0, 12.0, 6.0, key="g3")
        ret = st.slider("Expected return %", 4.0, 15.0, 10.0, key="g4")
        have = st.number_input("Already saved for this (₹)", 0, value=0, step=10000, key="g5")
    future = cost * (1 + infl / 100) ** yrs
    sip = sip_needed(future, ret, yrs, have)
    with right:
        m1, m2 = st.columns(2)
        m1.metric("Cost in future", money(future))
        m2.metric("Monthly SIP needed", money(sip))
        pct_done = min(have / future * 100, 100) if future else 0
        st.markdown(f'<div class="score"><b>Your goal: {html.escape(goal)}</b><br>Saved so far vs future cost: <b>{pct_done:.0f}%</b>'
                    f'<div class="bar"><div style="width:{pct_done}%;background:#f5b301"></div></div></div>',
                    unsafe_allow_html=True)
        if yrs > 1:
            delay = sip_needed(future, ret, yrs - 1, have) - sip
            st.info(f"Starting one year later would raise your monthly SIP by about {money(delay)}. "
                    "Starting early is the cheapest way to reach your goal.")
        yl = list(range(0, yrs + 1))
        chart_line("goal", [f"Year {k}" for k in yl],
                   [("Total you put in", "#7b8fb0", [have + sip * 12 * k for k in yl], True),
                    ("Projected value", "#14306b", [have * (1 + ret / 100) ** k + sip * sip_factor(ret, k) for k in yl], False)],
                   ref={"value": future, "label": "Goal: " + short(future)}, title="How the money builds up")
        st.caption("Rule of thumb: goals under 3 years suit debt or liquid funds, 3 to 7 years suit hybrid funds, and 7 years or more suit equity index funds.")

# ---------- 3. Child education ----------
with tabs[2]:
    page_banner("banner_education", "Child Education")
    st.subheader("Child education planner")
    left, right = st.columns([5, 7], gap="large")
    with left:
        age = st.number_input("Child's age now", 0, 17, 3)
        college_age = st.number_input("Age when college starts", 15, 25, 18)
        edu_cost = st.number_input("Course cost today (₹)", 0, value=2500000, step=100000)
        edu_infl = st.slider("Education inflation %", 4.0, 12.0, 9.0)
        r2 = st.slider("Expected return %", 4.0, 15.0, 11.0, key="e1")
    y = max(college_age - age, 1)
    fut = edu_cost * (1 + edu_infl / 100) ** y
    _se = sip_needed(fut, r2, y)
    with right:
        m1, m2 = st.columns(2)
        m1.metric("Cost when child is ready", money(fut))
        m2.metric("Monthly SIP needed", money(_se))
        yl = list(range(0, y + 1))
        chart_line("edu", [f"Age {age + k}" for k in yl],
                   [("Course cost", "#ff6b16", [edu_cost * (1 + edu_infl / 100) ** k for k in yl], True),
                    ("Your SIP savings", "#14306b", [_se * sip_factor(r2, k) for k in yl], False)],
                   title="Course cost against your savings")
        st.caption("Ideas to explore: Sukanya Samriddhi Yojana (girl child), PPF, equity index fund SIP, child insurance only if you need cover.")

# ---------- 4. Retirement ----------
with tabs[3]:
    page_banner("banner_retirement", "Retirement")
    st.subheader("Retirement planner")
    left, right = st.columns([5, 7], gap="large")
    with left:
        a = st.number_input("Your age", 18, 70, 28)
        ra = st.number_input("Retire at", 40, 75, 55)
        mexp = st.number_input("Current monthly expenses (₹)", 0, value=40000, step=5000, key="r1")
        inf3 = st.slider("Inflation %", 3.0, 10.0, 6.0, key="r2")
        swr = st.slider("Safe withdrawal rate % per year", 2.5, 5.0, 3.5)
        r3 = st.slider("Return before retirement %", 5.0, 14.0, 10.0, key="r3")
        cur = st.number_input("Retirement savings now (₹)", 0, value=200000, step=50000)
    yrs_left = max(ra - a, 1)
    exp_then = mexp * 12 * (1 + inf3 / 100) ** yrs_left
    corpus = exp_then / (swr / 100)
    _s = sip_needed(corpus, r3, yrs_left, cur)
    with right:
        m1, m2 = st.columns(2)
        m1.metric("Corpus needed", money(corpus))
        m2.metric("Monthly SIP needed", money(_s))
        st.caption(f"At {ra} your yearly spending would be about {money(exp_then)}, so you need roughly {short(corpus)} to cover it.")
        yl = list(range(0, yrs_left + 1))
        chart_line("retire", [f"Age {a + k}" for k in yl],
                   [("Your savings", "#14306b", [cur * (1 + r3 / 100) ** k + _s * sip_factor(r3, k) for k in yl], False)],
                   ref={"value": corpus, "label": "Needed: " + short(corpus)}, title="Savings against the corpus you need")
        st.caption("Explore: EPF, PPF, NPS (extra ₹50,000 tax deduction in the old regime), equity index funds.")

# ---------- 5. Tax saver ----------
def _tax_card(title, r, accent, cheaper):
    rows = [("Taxable income", r["taxable"], False), ("Tax on slabs", r["slab"], False)]
    if r["rebate"]:
        rows.append(("Rebate under 87A", r["rebate"], True))
    if r["relief"]:
        rows.append(("Marginal relief", r["relief"], True))
    if r["surcharge"]:
        rows.append(("Surcharge", r["surcharge"], False))
    rows.append(("Health and education cess (4%)", r["cess"], False))
    body = "".join(f'<div class="trow"><span>{l}</span><b>{"-" if neg else ""}{money(v)}</b></div>' for l, v, neg in rows)
    tag = '<span class="tag">Lower tax</span>' if cheaper else ""
    return (f'<div class="taxcard" style="border-top:4px solid {accent}"><div class="tt">{title}{tag}</div>'
            f'<div class="tv">{money(r["total"])}</div>{body}</div>')


with tabs[4]:
    page_banner("banner_tax", "Tax Saver")
    st.subheader("Old regime or new regime?")
    st.caption("FY 2026-27 (assessment year 2027-28). Budget 2026 left the slabs unchanged. These are estimates, "
               "so check incometax.gov.in before you file.")
    top1, top2, top3 = st.columns([2, 1, 1])
    gross = top1.number_input("Annual salary or income (₹)", 0, value=1500000, step=50000)
    age_band = top2.selectbox("Your age", list(OLD_SLABS))
    salaried = top3.checkbox("Salaried", value=True, help="The standard deduction applies to salary and pension income.")
    c1, c2 = st.columns(2)
    with c1:
        d80c = st.number_input("80C (EPF, PPF, ELSS, LIC) ₹", 0, value=150000, step=10000)
        d80d = st.number_input("80D health insurance ₹", 0, value=25000, step=5000)
        nps = st.number_input("NPS extra (80CCD 1B) ₹", 0, value=50000, step=10000)
    with c2:
        hl = st.number_input("Home loan interest ₹", 0, value=0, step=10000)
        hra = st.number_input("HRA exemption ₹", 0, value=0, step=10000)
    nr = new_regime(gross, salaried)
    orr = old_regime(gross, age_band, d80c, d80d, nps, hl, hra, salaried)
    cheaper_new = nr["total"] <= orr["total"]
    ca, cb = st.columns(2)
    ca.markdown(_tax_card("New regime", nr, "#2f6bff", cheaper_new), unsafe_allow_html=True)
    cb.markdown(_tax_card("Old regime", orr, "#ff6b16", not cheaper_new), unsafe_allow_html=True)
    diff = abs(nr["total"] - orr["total"])
    if diff >= 1:
        st.success(f"The {'new' if cheaper_new else 'old'} regime costs you {money(diff)} less.")
    else:
        st.info("Both regimes give the same tax.")
    if nr["relief"] > 0:
        st.info(f"Your income is just above ₹12 lakh, so marginal relief takes {money(nr['relief'])} off the new-regime tax.")
    for nm, val, cap, txt in [("80C", d80c, CAPS["80c"], "₹1.5 lakh"),
                              ("80D", d80d, CAPS["80d"], "₹1 lakh here (self, family and senior-citizen parents)"),
                              ("NPS extra", nps, CAPS["nps"], "₹50,000"),
                              ("Home loan interest", hl, CAPS["home_loan"], "₹2 lakh")]:
        if val > cap:
            st.caption(f"{nm} is capped at {txt}, so the extra {money(val - cap)} is ignored in the old regime.")
    chart_bars("taxcmp", [("New regime", nr["total"], "#2f6bff"), ("Old regime", orr["total"], "#ff6b16")],
               title="Tax you would pay")
    with st.expander("See the working"):
        st.markdown("""
**New regime.** Standard deduction of ₹75,000 for salaried income, and no other deductions. Slabs: nil up to ₹4 lakh, then 5% to ₹8 lakh, 10% to ₹12 lakh, 15% to ₹16 lakh, 20% to ₹20 lakh, 25% to ₹24 lakh and 30% above that. Taxable income up to ₹12 lakh pays no tax (rebate under 87A, up to ₹60,000). Just above ₹12 lakh, marginal relief stops the tax from exceeding the income over ₹12 lakh.

**Old regime.** Standard deduction of ₹50,000 plus the deductions you enter, within their caps. Slabs depend on age. Below 60: nil to ₹2.5 lakh, 5% to ₹5 lakh, 20% to ₹10 lakh, 30% above. Ages 60 to 79: nil to ₹3 lakh. Age 80 and above: nil to ₹5 lakh, then 20% to ₹10 lakh. Taxable income up to ₹5 lakh gets a rebate of up to ₹12,500.

**Both.** Surcharge is 10% above ₹50 lakh, 15% above ₹1 crore and 25% above ₹2 crore. The old regime adds 37% above ₹5 crore, while the new regime stays at 25%. Marginal relief applies just above each threshold. Cess is 4% of tax plus surcharge.

**Not covered.** Capital gains and other special-rate income, employer NPS contributions, and tax paid abroad.
""")
    st.markdown("**Legal ways to lower your tax:** ELSS, PPF and EPF (80C), health insurance (80D), "
                "the extra NPS deduction, HRA, home-loan interest, planning when you book capital gains, and donations (80G). "
                "Anything that promises to hide income is evasion, and it is illegal.")

# ---------- 6. Mutual fund lookup (free API: mfapi.in) ----------
with tabs[5]:
    page_banner("banner_funds", "Mutual Fund Lookup")
    st.subheader("Look up an Indian mutual fund")
    q = st.text_input("Fund name (e.g. Nifty 50 index)")
    if q:
        try:
            res = requests.get("https://api.mfapi.in/mf/search", params={"q": q}, timeout=20).json()
            names = {f"{x['schemeName']}": x["schemeCode"] for x in res[:20]}
            if names:
                pick = st.selectbox("Select fund", list(names))
                data = requests.get(f"https://api.mfapi.in/mf/{names[pick]}", timeout=20).json()
                st.write("Latest NAV:", data["data"][0]["nav"], "on", data["data"][0]["date"])
                rows_nav = data["data"][:365][::-1]
                chart_line("mf", [d["date"] for d in rows_nav], [("NAV", "#14306b", [float(d["nav"]) for d in rows_nav], False)],
                           fmt="num", title="NAV over the last year")
            else:
                st.write("No funds found.")
        except Exception:
            st.error("Could not reach the fund data service.")

# ---------- 7. AI advisor ----------
with tabs[6]:
    page_banner("banner_ai", "AI Advisor")
    st.subheader("Ask the AI (do not enter PAN, Aadhaar or bank details)")
    question = st.text_area("Your question", "I am 28, earn ₹15 lakh. How should I split savings across goals?")
    if st.button("Get suggestions"):
        with st.spinner("Thinking..."):
            st.write(ask_ai(question))


# ---------- 8. Teen savers ----------
import pandas as pd

with tabs[7]:
    page_banner("banner_teen", "Teen Savers")
    st.subheader("Saving for something big")
    left, right = st.columns([5, 7], gap="large")
    with left:
        goal_t = st.text_input("What are you saving for?", "Laptop for video editing", key="t1")
        cost_t = st.number_input("Cost (₹)", 0, value=60000, step=1000, key="t2")
        saved_t = st.number_input("Already saved (₹)", 0, value=2000, step=500, key="t3")
        months_t = st.slider("Months you have", 3, 60, 12, key="t4")
        pocket = st.number_input("Pocket money per month (₹)", 0, value=2000, step=500, key="t5")
        side = st.number_input("Side income per month (₹)", 0, value=1000, step=500, key="t6")
    need = max(cost_t - saved_t, 0)
    per_month = need / months_t
    with right:
        c1, c2 = st.columns(2)
        c1.metric("Save per month", money(per_month))
        c2.metric("Save per week", money(per_month * 12 / 52))
        st.caption(f"Goal: {goal_t}")
        income_t = pocket + side
        if income_t > 0:
            pct = per_month / income_t * 100
            st.write(f"That is **{pct:.0f}%** of your monthly money.")
            if pct > 70:
                st.warning("Tough target. Give yourself more months, earn a bit more, or pick a cheaper version.")
            elif pct > 40:
                st.info("Doable, but you will need discipline. Pay yourself first, the day money arrives.")
            else:
                st.success("Very doable. You are on track.")
        pig, rd, b0, b1 = [saved_t], [saved_t], saved_t, saved_t
        for m in range(1, months_t + 1):
            b0 += per_month
            b1 = (b1 + per_month) * (1 + 0.065 / 12)
            pig.append(b0)
            rd.append(b1)
        chart_line("teen", [f"Month {m}" for m in range(0, months_t + 1)],
                   [("Cash in a piggy bank", "#7b8fb0", pig, True), ("Recurring deposit (about 6.5%)", "#14306b", rd, False)],
                   ref={"value": cost_t, "label": "Your goal: " + short(cost_t)}, title="Your savings, month by month")
        st.caption("Interest rates change. Check your bank's current RD rate.")

    st.markdown("### 52-week challenge")
    base = st.number_input("Week 1 amount (₹)", 1, value=10, key="t7")
    st.write(f"Save ₹{base} in week 1, ₹{base*2} in week 2, and so on. "
             f"After 52 weeks you will have **{money(base * 52 * 53 / 2)}**.")

    st.markdown("""### 6 money habits for teens
1. **Pay yourself first:** move savings away the day money arrives, then spend what is left.
2. **Split it:** try 50% spend, 20% save for big goals, 20% short-term goals, 10% give or invest.
3. **Wait 48 hours** before any non-essential purchase.
4. **Earn more:** tutoring juniors, design or video editing, freelancing, selling things you make.
5. **Save safely:** with a parent or guardian, open a minor savings account, recurring deposit, or a guardian-operated mutual fund SIP. Girls under 10 can have a Sukanya Samriddhi account.
6. **Learn early:** a small SIP started at 16 grows far bigger than the same SIP started at 26, because of compounding.

**Watch out:** "double your money" schemes, betting or fantasy-game apps, risky crypto tips on social media, and anyone asking for your OTP. If it sounds too good to be true, it is.""")

# ---------- 9. EMI manager ----------
def simulate_payoff(loans, extra=0.0, strategy="avalanche", rollover=True, track=False):
    bal = [l["bal"] for l in loans]
    rate = [l["rate"] for l in loans]
    emi = [l["emi"] for l in loans]
    total_interest, months = 0.0, 0
    hist = [sum(bal)]
    while any(b > 0.5 for b in bal) and months < 600:
        months += 1
        pool = extra
        for i in range(len(bal)):
            if bal[i] <= 0.5:
                if rollover:
                    pool += emi[i]
                continue
            interest = bal[i] * rate[i] / 1200
            bal[i] += interest
            total_interest += interest
            pay = min(emi[i], bal[i])
            bal[i] -= pay
            if rollover:
                pool += emi[i] - pay
        open_loans = [i for i in range(len(bal)) if bal[i] > 0.5]
        if strategy == "avalanche":
            open_loans.sort(key=lambda i: -rate[i])
        else:
            open_loans.sort(key=lambda i: bal[i])
        for i in open_loans:
            if pool <= 0:
                break
            pay = min(pool, bal[i])
            bal[i] -= pay
            pool -= pay
        hist.append(sum(b for b in bal if b > 0))
    stuck = any(b > 0.5 for b in bal)
    return (months, total_interest, stuck, hist) if track else (months, total_interest, stuck)


with tabs[8]:
    page_banner("banner_emi", "EMI Manager")
    st.subheader("Several EMIs, one plan")
    st.write("Edit the table below. Click the empty last row to add a loan (phone, bike, credit card, education...).")
    default = pd.DataFrame({
        "Loan": ["Phone EMI", "Bike loan", "Credit card"],
        "Outstanding (₹)": [30000, 150000, 40000],
        "Interest % per year": [0.0, 11.0, 36.0],
        "Monthly EMI (₹)": [3000, 6000, 3000],
    })
    df = st.data_editor(default, num_rows="dynamic", key="emi_table")
    inc = st.number_input("Your monthly income (₹)", 0, value=80000, step=5000, key="emi_inc")
    extra = st.number_input("Extra money you can add each month (₹)", 0, value=2000, step=500, key="emi_extra")

    try:
        d = df.dropna()
        loans = [{"name": str(r.iloc[0]), "bal": float(r.iloc[1]), "rate": float(r.iloc[2]), "emi": float(r.iloc[3])}
                 for _, r in d.iterrows() if float(r.iloc[1]) > 0 and float(r.iloc[3]) > 0]
    except Exception:
        loans = []
        st.error("Please fill numbers only in the number columns.")

    if loans:
        total_emi = sum(l["emi"] for l in loans)
        st.metric("Total EMIs per month", money(total_emi))
        if inc > 0:
            ratio = total_emi / inc * 100
            st.write(f"**EMI-to-income:** {ratio:.0f}% (healthy is under 40%, ideal under 30%)")
            if ratio > 40:
                st.error("Too much of your income goes to EMIs. Avoid new loans and use the plan below.")

        base_m, base_i, base_stuck, base_h = simulate_payoff(loans, 0, rollover=False, track=True)
        av_m, av_i, av_stuck, av_h = simulate_payoff(loans, extra, "avalanche", track=True)
        sn_m, sn_i, sn_stuck = simulate_payoff(loans, extra, "snowball")
        if base_stuck or av_stuck:
            st.error("At least one EMI is too small to cover its interest. That loan will never finish! Raise its EMI.")
        else:
            st.markdown("### Payoff plans")
            plans = pd.DataFrame({
                "Plan": ["Just pay EMIs as they are", "Avalanche (highest interest first)", "Snowball (smallest loan first)"],
                "Debt-free in (months)": [base_m, av_m, sn_m],
                "Total interest (₹)": [round(base_i), round(av_i), round(sn_i)],
            })
            st.dataframe(plans, hide_index=True)
            span = max(len(base_h), len(av_h))
            pad = lambda h: [float(v) for v in h] + [0.0] * (span - len(h))
            chart_line("emi_debt", [f"Month {k}" for k in range(span)],
                       [("Paying EMIs as they are", "#7b8fb0", pad(base_h), True), ("With your extra amount", "#14306b", pad(av_h), False)],
                       title="Debt left, month by month")
            chart_bars("emi_interest", [("Just the EMIs", base_i, "#7b8fb0"), ("Avalanche", av_i, "#2f6bff"), ("Snowball", sn_i, "#ff6b16")],
                       title="Total interest you would pay")
            chart_donut("emi_mix", [(l["name"], l["bal"], c) for l, c in zip(loans, PALETTE * 3)], "Owed today",
                        money(sum(l["bal"] for l in loans)))
            st.success(f"Avalanche saves you about {money(base_i - av_i)} in interest "
                       f"and {base_m - av_m} months vs doing nothing extra.")
            st.write("**Pay-first order (avalanche):** " +
                     " → ".join(l["name"] for l in sorted(loans, key=lambda x: -x["rate"])))
            st.caption("How it works: pay the minimum EMI on every loan, put all extra money on the loan with "
                       "the highest interest, and when a loan ends, roll its EMI onto the next one.")

    st.markdown("""**Quick rules**
- Credit card debt (30-42% a year) is the most expensive. Clear it first.
- "No-cost EMI" is rarely free: look for processing fees, GST on interest, and lost discounts.
- Floating-rate loans for individuals generally have no prepayment penalty. Check your loan terms before prepaying.
- Never pay one EMI with another loan.""")

    st.markdown("### Can I afford a new EMI?")
    p = st.number_input("Loan amount (₹)", 0, value=500000, step=10000, key="n1")
    nr = st.slider("Interest % per year", 0.0, 24.0, 10.0, key="n2")
    nm = st.slider("Tenure (months)", 6, 360, 60, key="n3")
    if p > 0:
        r = nr / 1200
        new_emi = p / nm if r == 0 else p * r * (1 + r) ** nm / ((1 + r) ** nm - 1)
        st.metric("New EMI", money(new_emi))
        st.write(f"Total interest you will pay: **{money(new_emi * nm - p)}**")
        chart_donut("emi_new", [("Principal", p, "#14306b"), ("Interest", new_emi * nm - p, "#ff6b16")], "Monthly EMI", money(new_emi))
        if inc > 0:
            old = sum(l["emi"] for l in loans) if loans else 0
            after = (old + new_emi) / inc * 100
            st.write(f"EMI-to-income after this loan: **{after:.0f}%**")
            if after > 40:
                st.warning("This would push you above 40%. Think twice or choose a longer tenure or a smaller loan.")


# ---------- 10. Investment ideas ----------
with tabs[9]:
    page_banner("banner_invest", "Investment Ideas")
    st.subheader("Investment ideas for your situation")
    st.caption("Answer a few questions. You get a suggested mix and the TYPES of investments that fit you, not tips on specific funds or stocks.")
    c1, c2 = st.columns(2)
    with c1:
        iv_age = st.number_input("Your age", 14, 80, 28, key="iv_age")
        iv_amt = st.number_input("Monthly amount you can invest (₹)", 0, value=10000, step=1000, key="iv_amt")
        iv_years = st.slider("How long can you stay invested? (years)", 1, 30, 10, key="iv_years")
        iv_goal = st.selectbox("Main purpose", ["Build long-term wealth", "Retirement", "Child's education",
                                                "Buy a house or car", "Short-term goal (under 3 years)", "Save tax"], key="iv_goal")
    with c2:
        R1 = ["Sell to avoid more loss", "Wait and hold", "Invest more"]
        R2 = ["Uncertain", "Fairly stable", "Very stable"]
        R3 = ["New to it", "Some experience", "Experienced"]
        iv_react = st.radio("If your investments fell 20% in a month, you would...", R1, key="iv_react")
        iv_income = st.radio("Your income is...", R2, key="iv_income")
        iv_exp = st.radio("Investing experience", R3, key="iv_exp")
        iv_fund = st.radio("Do you have an emergency fund (3-6 months of expenses)?", ["Not yet", "Partly", "Yes, fully"], key="iv_fund")
    c3, c4, c5 = st.columns(3)
    iv_debt = c3.checkbox("I have loans or card dues above 12% interest", key="iv_debt")
    iv_regime = c4.selectbox("Tax regime", ["New regime", "Old regime"], key="iv_reg")
    iv_girl = c5.checkbox("Saving for a daughter under 10", key="iv_girl")

    pts = R1.index(iv_react) + R2.index(iv_income) + R3.index(iv_exp)      # risk comfort, 0 to 6
    cap = 10 if iv_years <= 3 else 35 if iv_years <= 5 else 55 if iv_years <= 7 else 80
    if iv_goal.startswith("Short-term"):
        cap = min(cap, 10)
    eq = int(max(0, min((100 - iv_age) + (pts - 3) * 5, cap, 80)) // 5 * 5)
    gold = 10 if (iv_years > 3 and eq <= 70 and not iv_goal.startswith("Short-term")) else 0
    debt = 100 - eq - gold

    st.markdown("### Do these first")
    first = []
    if iv_debt:
        first.append("**Clear expensive debt first.** Loans or card dues above 12% cost more than most investments earn.")
    if iv_fund != "Yes, fully":
        first.append("**Build your emergency fund.** Keep 3-6 months of expenses in a savings account or liquid fund before taking market risk.")
    if iv_age < 18:
        first.append("**You are under 18.** Investments must be opened by a parent or guardian, so involve them from the start.")
    if first:
        for f in first:
            st.warning(f)
    else:
        st.success("You are ready to invest. Nothing needs to come first.")

    if iv_amt <= 0:
        st.info("Enter a monthly amount above to see your plan.")
    else:
        st.markdown("### Your suggested mix")
        m1, m2, m3 = st.columns(3)
        m1.metric("Equity (growth)", f"{eq}%")
        m2.metric("Debt (stability)", f"{debt}%")
        m3.metric("Gold (cushion)", f"{gold}%")
        chart_donut("mix", [("Equity", eq, "#14306b"), ("Debt", debt, "#2f6bff"), ("Gold", gold, "#f5b301")],
                    "Equity / Debt / Gold", f"{eq} / {debt} / {gold}", fmt="pct0")

        def card(name, why, amt):
            return (f'<div class="score" style="margin:8px 0"><b>{name}</b>'
                    f'<span style="float:right;font-weight:700;color:#14306b">{money(amt)} / month</span><br>'
                    f'<span style="color:#6b7280;font-size:.9rem">{why}</span></div>')

        def show(title, share, items):
            if share <= 0:
                return
            st.markdown(f"#### {title}: {money(iv_amt * share / 100)} a month")
            st.markdown("".join(card(n, w, iv_amt * share / 100 * pct / 100) for n, w, pct in items if pct > 0),
                        unsafe_allow_html=True)

        elss = 20 if (iv_regime == "Old regime" and iv_years >= 3) else 0
        flexi = 25 if (pts >= 4 and iv_years >= 7) else 0
        show("Equity", eq, [
            ("Index funds (Nifty 50 or Sensex)", "Low-cost and diversified. The simplest base for long-term money.", 100 - elss - flexi),
            ("Flexi-cap funds", "A fund manager picks across company sizes. Adds some variety if you are comfortable with risk.", flexi),
            ("ELSS tax-saving funds", "Equity funds with a 3-year lock-in. Counts under Section 80C in the old regime only.", elss)])

        if iv_age >= 60:
            debt_items = [("Senior Citizens' Savings Scheme", "Government-backed, for people aged 60+, regular interest.", 50),
                          ("Bank fixed deposits (senior rates)", "Predictable returns with a fixed term.", 50)]
        elif iv_years <= 3:
            debt_items = [("Liquid or ultra-short-term debt funds", "Stable and easy to withdraw for near-term needs.", 50),
                          ("Recurring or fixed deposits", "Guaranteed returns for a fixed period.", 50)]
        else:
            debt_items = [("PPF (Public Provident Fund)", "Government-backed, tax-free interest, 15-year lock-in with partial withdrawals later.", 40),
                          ("Short-duration or corporate bond funds", "Higher potential than deposits, with some interest-rate risk.", 40),
                          ("Fixed deposits", "Simple and predictable. Good for part of your safe money.", 20)]
        show("Debt", debt, debt_items)
        show("Gold", gold, [("Gold ETFs or gold funds", "Often holds up when markets fall. Keep it small. Sovereign Gold Bonds can still be bought from the stock market.", 100)])

        extras = []
        if iv_goal == "Retirement":
            extras.append("**NPS (National Pension System):** built for retirement and partly locked until 60. Under the old regime it gives an extra ₹50,000 deduction (Section 80CCD(1B)).")
        if iv_girl:
            extras.append("**Sukanya Samriddhi Yojana:** a government scheme for a girl child under 10, with tax benefits and a high fixed rate. Opened by a parent or guardian.")
        if iv_goal == "Child's education":
            extras.append("**Long-term SIP:** for goals 10+ years away, a monthly SIP in the equity part above usually does the heavy lifting.")
        if iv_regime == "New regime":
            extras.append("**Tax note:** the new regime gives no 80C benefit, so pick investments for their returns and safety, not the tax deduction.")
        if extras:
            st.markdown("#### Also worth knowing")
            for e in extras:
                st.info(e)

        blended = (eq * 10 + debt * 6.5 + gold * 7) / 100
        put_in = iv_amt * 12 * iv_years
        grown = iv_amt * sip_factor(blended, iv_years)
        st.markdown("### What this could look like")
        p1, p2, p3 = st.columns(3)
        p1.metric("You invest", money(put_in))
        p2.metric("Illustrative value", money(grown))
        p3.metric("Bad-year risk", f"about -{eq * 0.35:.0f}%")
        yl = list(range(0, iv_years + 1))
        chart_line("invest", [f"Year {k}" for k in yl],
                   [("You put in", "#7b8fb0", [iv_amt * 12 * k for k in yl], True),
                    ("Illustrative value", "#14306b", [iv_amt * sip_factor(blended, k) for k in yl], False)],
                   title="An illustration, not a forecast")
        st.caption(f"Assumes about {blended:.1f}% a year (equity 10%, debt 6.5%, gold 7%). These are illustrations, not promises. "
                   "In a very bad year the equity part can fall 30-40%, which is why the mix matters.")

        if st.button("Explain this plan in simple words", key="iv_ai"):
            with st.spinner("Thinking..."):
                st.write(ask_ai(f"Explain this investment mix to an Indian beginner in simple words, with the main risks, "
                                f"and do NOT name specific funds or stocks. Equity {eq}%, debt {debt}%, gold {gold}%, "
                                f"time horizon {iv_years} years, age {iv_age}, goal: {iv_goal}, tax regime: {iv_regime}, "
                                f"monthly investment {iv_amt} rupees."))
        st.caption("Educational only. Not SEBI-registered advice. Talk to a SEBI-registered advisor before investing.")

# ---------- 11. News ----------
NEWS_URL = os.environ.get("DD_NEWS_URL", "https://news.google.com/rss/search")
NEWS_TOPICS = {
    "Markets": 'Sensex OR Nifty OR "stock market" India',
    "Economy and RBI": 'RBI OR "repo rate" OR inflation India economy',
    "Tax": '"income tax" OR ITR OR GST India',
    "Mutual funds": '"mutual fund" OR SIP India',
    "Gold and savings": '"gold price" OR "fixed deposit" OR PPF India',
    "Personal finance": '"personal finance" OR "home loan" OR insurance India',
}


@st.cache_data(ttl=900, show_spinner=False)
def fetch_news(query, limit=14):
    r = requests.get(NEWS_URL, params={"q": query + " when:7d", "hl": "en-IN", "gl": "IN", "ceid": "IN:en"},
                     headers={"User-Agent": "Mozilla/5.0"}, timeout=12)
    r.raise_for_status()
    out = []
    for it in ET.fromstring(r.content).iter("item"):
        title = (it.findtext("title") or "").strip()
        link = (it.findtext("link") or "").strip()
        src_el = it.find("source")
        src = (src_el.text or "").strip() if src_el is not None else ""
        if src and title.endswith(" - " + src):
            title = title[: -(len(src) + 3)]
        try:
            when = parsedate_to_datetime(it.findtext("pubDate") or "").timestamp()
        except Exception:
            when = None
        if title and link.startswith(("http://", "https://")):
            out.append({"title": title, "link": link, "source": src, "when": when})
    return out[:limit]


def _ago(ts):
    if not ts:
        return ""
    secs = max(0, time.time() - ts)
    if secs < 3600:
        return f"{int(secs // 60) or 1} min ago"
    if secs < 86400:
        return f"{int(secs // 3600)} h ago"
    return f"{int(secs // 86400)} d ago"


def _news_cards(items):
    cards = []
    for it in items:
        cards.append(f'<a class="ncard" href="{html.escape(it["link"], quote=True)}" target="_blank" rel="noopener noreferrer">'
                     f'<span class="nsrc">{html.escape(it["source"] or "News")}</span><b>{html.escape(it["title"])}</b>'
                     f'<span class="nago">{_ago(it["when"])}</span></a>')
    return '<div class="ngrid">' + "".join(cards) + "</div>"


with tabs[10]:
    page_banner("banner_news", "News")
    st.subheader("Money news from India")
    st.caption("Headlines from the past week, gathered from Google News. We show the headline and a link. "
               "The article opens on the publisher's own site.")
    topic = st.radio("Topic", list(NEWS_TOPICS), horizontal=True, label_visibility="collapsed", key="news_topic")
    if page == "News":      # only go online when this page is open
        if st.button("Refresh", key="news_refresh"):
            fetch_news.clear()
        try:
            news_items = fetch_news(NEWS_TOPICS[topic])
        except Exception:
            news_items = None
        if news_items is None:
            st.warning("Could not load the news just now. Check your internet connection, then press Refresh.")
        elif not news_items:
            st.info("No headlines found for this topic right now. Try another topic.")
        else:
            st.markdown(_news_cards(news_items), unsafe_allow_html=True)
            st.caption("Headlines are general information, not investment advice.")

# ---------- 12. Calculators ----------
with tabs[11]:
    page_banner("banner_calc", "Calculators")
    st.subheader("Everyday calculators")
    kind = st.radio("Calculator", ["GST", "Gratuity", "Capital gains"], horizontal=True, label_visibility="collapsed", key="calc_kind")

    if kind == "GST":
        g1, g2, g3 = st.columns(3)
        mode = g1.radio("What do you have?", ["Price without GST", "Price with GST"], key="gst_mode")
        amount = g2.number_input("Amount (₹)", 0.0, value=10000.0, step=100.0, key="gst_amt")
        pick = g3.selectbox("GST rate", ["18%", "5%", "40%", "3% (gold)", "0%", "Other"], key="gst_rate")
        rate = {"18%": 18.0, "5%": 5.0, "40%": 40.0, "3% (gold)": 3.0, "0%": 0.0}.get(pick)
        if rate is None:
            rate = g3.number_input("Rate (%)", 0.0, 100.0, value=12.0, step=0.5, key="gst_other")
        if mode == "Price without GST":
            base, total = amount, amount * (1 + rate / 100)
        else:
            base, total = amount / (1 + rate / 100), amount
        gst_amt = total - base
        m1, m2, m3 = st.columns(3)
        m1.metric("Price before GST", money(base))
        m2.metric("GST", money(gst_amt))
        m3.metric("Total price", money(total))
        st.caption(f"Within one state, the GST splits into CGST {money(gst_amt / 2)} and SGST {money(gst_amt / 2)}. "
                   f"Between states it is a single IGST of {money(gst_amt)}.")
        chart_donut("gst", [("Price before GST", base, "#14306b"), ("GST", gst_amt, "#ff6b16")], "Total", money(total))
        st.caption("Since 22 September 2025 most goods and services are taxed at 5% or 18%, with 40% on a few luxury and "
                   "sin goods, and 3% on gold. Check the rate for your own item before you rely on this.")

    elif kind == "Gratuity":
        a1, a2 = st.columns(2)
        pay = a1.number_input("Last drawn monthly basic + DA (₹)", 0, value=50000, step=1000, key="gr_pay")
        covered = a2.radio("Is your employer covered by the Payment of Gratuity Act?", ["Yes", "No, it has its own scheme"], key="gr_cov")
        b1, b2 = st.columns(2)
        yrs_s = b1.number_input("Years of service", 0, 50, value=8, key="gr_y")
        mon_s = b2.number_input("Extra months", 0, 11, value=3, key="gr_m")
        counted = int(yrs_s) + (1 if mon_s > 6 else 0)      # more than 6 months counts as a full year
        factor = 15 / 26 if covered == "Yes" else 15 / 30
        grat = pay * factor * counted
        limit = 2000000
        m1, m2, m3 = st.columns(3)
        m1.metric("Gratuity", money(grat))
        m2.metric("Years counted", f"{counted}")
        m3.metric("Taxable part", money(max(grat - limit, 0)))
        if yrs_s < 5:
            st.warning("Gratuity is normally paid only after 5 years of continuous service, except on death or disability. "
                       "Fixed-term contracts can differ, so check yours.")
        if counted >= 1:
            ks = list(range(0, counted + 1))
            chart_line("grat", [f"{k} yr" for k in ks], [("Gratuity", "#14306b", [pay * factor * k for k in ks], False)],
                       ref={"value": limit, "label": "Tax-free limit: ₹20 lakh"}, title="Gratuity by years of service")
        st.caption("Formula: last monthly pay × 15 ÷ 26 × years of service (÷ 30 instead of 26 if your employer is not covered by the Act). "
                   "More than 6 months of extra service counts as a full year. Up to ₹20 lakh is tax-free for private-sector employees, "
                   "and government employees are fully exempt. Limits can change, so confirm with your HR team.")

    else:
        k1, k2 = st.columns(2)
        buy = k1.number_input("Total buy cost (₹)", 0, value=500000, step=10000, key="cg_buy")
        sell = k2.number_input("Total sale value (₹)", 0, value=800000, step=10000, key="cg_sell")
        k3, k4 = st.columns(2)
        months = k3.number_input("Months you held it", 0, 600, value=18, key="cg_m")
        other = k4.number_input("Other long-term equity gains this year (₹)", 0, value=0, step=10000, key="cg_other")
        gain = sell - buy
        if gain <= 0:
            st.info(f"This is a loss of {money(-gain)}. Short-term losses can be set against any capital gain, and long-term "
                    "losses against long-term gains, and unused losses carry forward for 8 years.")
        else:
            if months > 12:
                lt_total = gain + other
                taxable, rate, kind_txt = max(lt_total - 125000, 0) - max(other - 125000, 0), 12.5, "long-term"
            else:
                taxable, rate, kind_txt = gain, 20.0, "short-term"
            tax = taxable * rate / 100 * 1.04
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("Gain", money(gain))
            m2.metric("Taxable gain", money(taxable))
            m3.metric(f"Tax at {rate:g}% + cess", money(tax))
            m4.metric("You keep", money(gain - tax))
            st.caption(f"This is a {kind_txt} gain. " + ("The first ₹1.25 lakh of long-term equity gains in a year is tax-free." if months > 12 else
                                                          "Equity gains held for 12 months or less are taxed at a flat 20%."))
            chart_donut("cg", [("You keep", gain - tax, "#14306b"), ("Tax", tax, "#ff6b16")], "Tax", money(tax))
        st.caption("For listed shares and equity mutual funds (STT paid). Held 12 months or less: 20%. Held longer: 12.5% on gains "
                   "above ₹1.25 lakh a year. Budget 2026 did not change these. Not included: surcharge, brokerage and STT, "
                   "gold, property and debt funds (taxed differently), and the 31 January 2018 grandfathering rule.")

with st.expander("How the numbers are worked out"):
    st.markdown("""
- **Future cost:** today's cost × (1 + inflation) ^ years.
- **SIP needed:** the monthly amount that grows to your target, using the standard future-value formula for monthly investing at the return you choose.
- **Retirement corpus:** yearly expenses at retirement ÷ safe withdrawal rate.
- **Investment mix:** starts from 100 minus your age as the share in equity, adjusted by your risk answers, then capped for short time horizons. The rest goes to debt and gold. Return figures are illustrative assumptions, not promises.
- **Tax:** slabs, rebate and 4% cess are set in the code for one financial year and must be updated every year.
- **EMI payoff:** a month-by-month simulation. Avalanche means highest interest first.
- **Reminder:** returns are not guaranteed. Investments are subject to market risks.
""")

st.markdown('<hr><p style="text-align:center;color:#6b7280;font-size:.85rem">'
            '<b>Dhan Disha</b> · Built for the AI Conclave · Educational use only, not financial advice · '
            'Your inputs are never stored</p>', unsafe_allow_html=True)


with st.sidebar:
    st.markdown("""
<div class="sb"><hr>
<b>Quick guide</b><ul><li>Pick a section from the menu above</li><li>Enter your numbers</li><li>Read your score and plan</li><li>Ask the AI to explain</li></ul><hr>
<b>Privacy</b><p>This app saves nothing you type. Never enter PAN, Aadhaar or bank details.</p><hr>
<b>Note</b><p>Educational tool, not SEBI-registered advice. Check tax rules on incometax.gov.in.</p></div>
""", unsafe_allow_html=True)
