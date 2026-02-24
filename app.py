import streamlit as st
from groq import Groq
import os, io, re, base64, urllib.request
import streamlit.components.v1 as components

st.set_page_config(page_title="INFOGRAPH.AI", page_icon="⬡", layout="wide")

api_key = os.environ.get("GROQ_API_KEY")
if not api_key:
    try: api_key = st.secrets["GROQ_API_KEY"]
    except: pass
if not api_key:
    st.error("GROQ_API_KEY not found.")
    st.stop()

client = Groq(api_key=api_key)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Chakra+Petch:wght@300;400;600;700&family=Orbitron:wght@700;900&display=swap');

:root {
  --bg: #050508;
  --surface: #0a0a10;
  --border: #1c1c2e;
  --amber: #ffb700;
  --amber-dim: rgba(255,183,0,0.12);
  --green: #00ff88;
  --green-dim: rgba(0,255,136,0.08);
  --red: #ff3c5a;
  --text: #c8c8d8;
  --text-dim: #3a3a50;
}

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
html, body, [class*="css"] { font-family: 'Chakra Petch', sans-serif !important; font-size: 14px; }

.stApp { background: var(--bg); color: var(--text); min-height: 100vh; position: relative; }

/* SCANLINES */
.stApp::before {
  content: ''; position: fixed; inset: 0;
  background: repeating-linear-gradient(0deg, transparent, transparent 2px, rgba(0,0,0,0.15) 2px, rgba(0,0,0,0.15) 4px);
  pointer-events: none; z-index: 9997;
}

/* GRID BG */
.stApp::after {
  content: ''; position: fixed; inset: 0;
  background-image: linear-gradient(rgba(255,183,0,0.025) 1px, transparent 1px), linear-gradient(90deg, rgba(255,183,0,0.025) 1px, transparent 1px);
  background-size: 40px 40px; pointer-events: none; z-index: 0;
}

.main .block-container { padding: 0 !important; max-width: 100% !important; position: relative; z-index: 1; }
#MainMenu, footer, header { display: none !important; }

/* MASTHEAD */
.masthead {
  border-bottom: 1px solid var(--amber); display: grid;
  grid-template-columns: auto 1fr auto; align-items: stretch;
}
.mast-logo-wrap {
  padding: 1.2rem 2rem; border-right: 1px solid var(--amber);
  display: flex; flex-direction: column; justify-content: center;
}
.mast-logo {
  font-family: 'Orbitron', monospace; font-size: 1.6rem; font-weight: 900;
  color: var(--amber); letter-spacing: 0.1em;
  text-shadow: 0 0 20px rgba(255,183,0,0.5); line-height: 1;
}
.mast-tagline { font-family: 'Share Tech Mono', monospace; font-size: 0.6rem; color: var(--text-dim); letter-spacing: 0.2em; margin-top: 0.3rem; }
.mast-center { padding: 1rem 2rem; display: flex; align-items: center; }
.mast-ticker { font-family: 'Share Tech Mono', monospace; font-size: 0.65rem; color: var(--text-dim); letter-spacing: 0.1em; display: flex; gap: 2rem; }
.ticker-item span { color: var(--amber); }
.mast-right { padding: 1rem 2rem; border-left: 1px solid var(--amber); display: flex; flex-direction: column; align-items: flex-end; justify-content: center; gap: 0.3rem; }
.status-dot { display: flex; align-items: center; gap: 0.5rem; font-family: 'Share Tech Mono', monospace; font-size: 0.62rem; color: var(--green); letter-spacing: 0.12em; }
.dot { width: 6px; height: 6px; background: var(--green); border-radius: 50%; animation: blink 1.5s ease-in-out infinite; }
@keyframes blink { 0%,100%{opacity:1} 50%{opacity:0.2} }

/* SEC HEADERS */
.sec-head { padding: 0.8rem 1.2rem; border-bottom: 1px solid var(--border); display: flex; align-items: center; gap: 0.8rem; background: rgba(255,183,0,0.02); }
.sec-num { font-family: 'Orbitron', monospace; font-size: 0.6rem; color: var(--amber); letter-spacing: 0.15em; background: var(--amber-dim); padding: 0.15rem 0.5rem; border: 1px solid rgba(255,183,0,0.3); }
.sec-title { font-family: 'Share Tech Mono', monospace; font-size: 0.65rem; color: var(--text-dim); letter-spacing: 0.2em; text-transform: uppercase; }

/* FIELD LABEL */
.field-label { font-family: 'Share Tech Mono', monospace; font-size: 0.6rem; color: var(--text-dim); letter-spacing: 0.18em; text-transform: uppercase; margin-bottom: 0.3rem; margin-top: 0.8rem; }
.field-label:first-child { margin-top: 0; }

/* INPUTS */
div[data-testid="stTextArea"] label, div[data-testid="stTextInput"] label, div[data-testid="stFileUploader"] label { display: none !important; }

div[data-testid="stTextArea"] textarea {
  background: var(--bg) !important; border: 1px solid var(--border) !important; border-radius: 0 !important;
  color: var(--amber) !important; font-family: 'Share Tech Mono', monospace !important;
  font-size: 0.78rem !important; line-height: 1.8 !important; padding: 0.8rem !important; resize: none !important;
}
div[data-testid="stTextArea"] textarea:focus { border-color: var(--amber) !important; box-shadow: 0 0 12px rgba(255,183,0,0.15) !important; outline: none !important; }
div[data-testid="stTextArea"] textarea::placeholder { color: var(--text-dim) !important; font-family: 'Share Tech Mono', monospace !important; }

.stTextInput input {
  background: var(--bg) !important; border: 1px solid var(--border) !important; border-radius: 0 !important;
  color: var(--amber) !important; font-family: 'Share Tech Mono', monospace !important;
  font-size: 0.75rem !important; padding: 0.6rem 0.8rem !important;
}
.stTextInput input:focus { border-color: var(--amber) !important; box-shadow: 0 0 8px rgba(255,183,0,0.12) !important; }
.stTextInput input::placeholder { color: var(--text-dim) !important; }

/* TABS */
div[data-baseweb="tab-list"] {
  background: transparent !important; border: none !important;
  border-bottom: 1px solid var(--border) !important; border-radius: 0 !important;
  padding: 0 !important; gap: 0 !important; margin-bottom: 0.8rem;
}
div[data-baseweb="tab"] {
  background: transparent !important; border-radius: 0 !important; color: var(--text-dim) !important;
  font-family: 'Share Tech Mono', monospace !important; font-size: 0.63rem !important;
  padding: 0.45rem 0.8rem !important; letter-spacing: 0.1em;
  border-bottom: 2px solid transparent !important; margin-bottom: -1px;
}
div[aria-selected="true"] { background: var(--amber-dim) !important; color: var(--amber) !important; border-bottom: 2px solid var(--amber) !important; }

/* BUTTONS */
.stButton > button {
  background: transparent !important; border: 1px solid var(--amber) !important; border-radius: 0 !important;
  color: var(--amber) !important; font-family: 'Orbitron', monospace !important; font-weight: 700 !important;
  font-size: 0.68rem !important; letter-spacing: 0.15em !important; padding: 0.55rem 1rem !important;
  text-transform: uppercase !important; transition: all 0.15s !important;
}
.stButton > button:hover { background: var(--amber) !important; color: var(--bg) !important; box-shadow: 0 0 20px rgba(255,183,0,0.4) !important; }

.stDownloadButton > button {
  background: transparent !important; border: 1px solid var(--green) !important; border-radius: 0 !important;
  color: var(--green) !important; font-family: 'Share Tech Mono', monospace !important;
  font-size: 0.65rem !important; padding: 0.4rem 0.9rem !important; letter-spacing: 0.1em; text-transform: none !important;
}
.stDownloadButton > button:hover { background: var(--green-dim) !important; }

/* SELECT */
div[data-baseweb="select"] > div {
  background: var(--bg) !important; border: 1px solid var(--border) !important; border-radius: 0 !important;
  color: var(--amber) !important; font-family: 'Share Tech Mono', monospace !important; font-size: 0.73rem !important;
}

/* FILE UPLOADER */
[data-testid="stFileUploader"] section {
  background: var(--bg) !important; border: 1px dashed var(--border) !important; border-radius: 0 !important; padding: 1rem !important;
}
[data-testid="stFileUploader"] section:hover { border-color: var(--amber) !important; }

/* CANVAS */
.canvas-header {
  padding: 0.8rem 2rem; border-bottom: 1px solid var(--border);
  display: flex; align-items: center; justify-content: space-between;
}
.canvas-title { font-family: 'Share Tech Mono', monospace; font-size: 0.62rem; color: var(--text-dim); letter-spacing: 0.2em; text-transform: uppercase; }

/* CHIPS */
.chip { display: inline-flex; align-items: center; gap: 0.4rem; font-family: 'Share Tech Mono', monospace; font-size: 0.6rem; padding: 0.2rem 0.6rem; letter-spacing: 0.1em; border: 1px solid; }
.chip-ok { border-color: rgba(0,255,136,0.4); color: var(--green); background: var(--green-dim); }
.chip-warn { border-color: rgba(255,183,0,0.4); color: var(--amber); background: var(--amber-dim); }

/* EMPTY STATE */
.empty-state { height: 600px; border: 1px solid var(--border); display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 1.5rem; position: relative; overflow: hidden; }
.corner-tl { position: absolute; top: 0; left: 0; width: 16px; height: 16px; border-top: 2px solid var(--amber); border-left: 2px solid var(--amber); }
.corner-br { position: absolute; bottom: 0; right: 0; width: 16px; height: 16px; border-bottom: 2px solid var(--amber); border-right: 2px solid var(--amber); }
.empty-hex { font-family: 'Share Tech Mono', monospace; font-size: 0.6rem; color: var(--border); position: absolute; inset: 0; display: flex; align-items: center; justify-content: center; word-break: break-all; padding: 3rem; line-height: 2.2; opacity: 0.6; }
.empty-content { position: relative; z-index: 1; text-align: center; }
.empty-icon { font-family: 'Orbitron', monospace; font-size: 2.5rem; color: #1c1c2e; display: block; margin-bottom: 1rem; animation: pulse 3s ease-in-out infinite; }
@keyframes pulse { 0%,100%{opacity:0.4} 50%{opacity:0.8} }
.empty-label { font-family: 'Orbitron', monospace; font-size: 0.75rem; color: #1c1c2e; letter-spacing: 0.2em; }
.empty-sub { font-family: 'Share Tech Mono', monospace; font-size: 0.58rem; color: #16162a; letter-spacing: 0.12em; margin-top: 0.5rem; }

::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--border); }
::-webkit-scrollbar-thumb:hover { background: var(--amber); }

.stSuccess > div, .stError > div, .stWarning > div { font-family: 'Share Tech Mono', monospace !important; font-size: 0.72rem !important; border-radius: 0 !important; }
</style>
""", unsafe_allow_html=True)

for k, v in [("doc_text",""),("infographic_html",""),("generated",False)]:
    if k not in st.session_state: st.session_state[k] = v

def extract_pdf(fb):
    import pypdf
    return "\n".join(p.extract_text() or "" for p in pypdf.PdfReader(io.BytesIO(fb)).pages).strip()

def extract_docx(fb):
    import docx
    return "\n".join(p.text for p in docx.Document(io.BytesIO(fb)).paragraphs).strip()

def fetch_url(url):
    req = urllib.request.Request(url, headers={'User-Agent':'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=15) as r:
        html = r.read().decode('utf-8', errors='ignore')
    txt = re.sub(r'<style[^>]*>.*?</style>','',html,flags=re.DOTALL)
    txt = re.sub(r'<script[^>]*>.*?</script>','',txt,flags=re.DOTALL)
    txt = re.sub(r'<[^>]+>',' ',txt)
    return re.sub(r'\s+',' ',txt).strip()

def call_groq(system, user, max_tokens=4000, temp=0.35):
    r = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role":"system","content":system},{"role":"user","content":user}],
        temperature=temp, max_tokens=max_tokens
    )
    return r.choices[0].message.content.strip()

INFOGRAPHIC_TYPES = {
    "auto": "🤖  AI DECIDES", "summary": "📋  KEY POINTS", "timeline": "⏱   TIMELINE",
    "stats": "📊  STATS / DATA", "comparison": "⚖   COMPARISON",
    "process": "🔄  PROCESS FLOW", "report": "📑  FULL REPORT",
}
THEMES = {
    "DARK — CYBER": "dark #0a0a14 bg, neon cyan #00e5ff + electric purple #9f00ff, glassmorphism cards",
    "DARK — AMBER": "deep black #050505 bg, amber #ffb700 + orange #ff6b00, terminal aesthetic",
    "DARK — EMERALD": "dark #071a12 bg, emerald #00ff88 + teal #00d4aa, bioluminescent",
    "LIGHT — CLEAN": "white #ffffff bg, deep navy #0f172a text, electric blue #2563eb accents",
    "LIGHT — WARM": "cream #faf8f4 bg, charcoal #1c1917 text, terracotta #dc6e2e accents",
    "DARK — CRIMSON": "black #080508 bg, crimson #ff2d55 + gold #ffd700, dramatic luxury",
}

SYSTEM_PROMPT = "You are a world-class infographic designer. Generate a COMPLETE SELF-CONTAINED HTML infographic. Return ONLY HTML — no markdown, no fences. All CSS in <style>. Use Google Fonts. Width 900px. Visually stunning with animations."

def build_prompt(doc_text, inf_type, title, theme_desc):
    type_map = {
        "auto": "Choose BEST format, mix stats + points + visuals",
        "summary": "KEY POINTS: numbered cards, emoji icons, 5-8 insights",
        "timeline": "TIMELINE: vertical/horizontal with dates, milestones, connectors",
        "stats": "STATS: large numbers, progress bars, percentage rings",
        "comparison": "COMPARISON: vs layout, pros/cons, feature table",
        "process": "PROCESS FLOW: numbered steps, arrows, flow connectors",
        "report": "FULL REPORT: hero title, stats row, content, timeline, summary footer",
    }
    t = f'Title: "{title}"' if title else "Generate compelling title from content."
    return f"""Create a stunning infographic.
TYPE: {type_map.get(inf_type,'choose best')}
{t}
THEME: {theme_desc}
RULES: 900px wide, rich visual hierarchy, CSS animations, emoji icons, decorative shapes, glassmorphism cards, bold typography, section dividers. Footer: "Generated by InfographAI".

DOCUMENT:
{doc_text[:5000]}

Return ONLY complete HTML starting with <!DOCTYPE html>"""

# MASTHEAD
st.markdown("""
<div class="masthead">
  <div class="mast-logo-wrap">
    <div class="mast-logo">INFOGRAPH.AI</div>
    <div class="mast-tagline">DOCUMENT → VISUAL INTELLIGENCE</div>
  </div>
  <div class="mast-center">
    <div class="mast-ticker">
      <span class="ticker-item">INPUT: <span>PDF · DOCX · TEXT · URL</span></span>
      <span class="ticker-item">OUTPUT: <span>HTML · PNG</span></span>
      <span class="ticker-item">ENGINE: <span>GROQ LLAMA 3.1</span></span>
      <span class="ticker-item">FORMATS: <span>7 STYLES</span></span>
    </div>
  </div>
  <div class="mast-right">
    <div class="status-dot"><div class="dot"></div>SYSTEM ONLINE</div>
    <div style="font-family:'Share Tech Mono',monospace;font-size:0.55rem;color:#1c1c2e;letter-spacing:0.1em">API CONNECTED</div>
  </div>
</div>""", unsafe_allow_html=True)

left_col, right_col = st.columns([0.9, 2.4], gap="small")

with left_col:
    st.markdown('<div class="sec-head"><span class="sec-num">SYS.01</span><span class="sec-title">DOCUMENT INPUT</span></div>', unsafe_allow_html=True)

    t1, t2, t3, t4 = st.tabs(["TEXT", "PDF", "DOCX", "URL"])
    with t1:
        txt = st.text_area("", height=150, placeholder="> PASTE TEXT, REPORTS, ARTICLES...", label_visibility="collapsed", key="k_txt")
        if st.button("▶ LOAD TEXT", key="btn_txt"):
            if txt.strip(): st.session_state.doc_text = txt.strip(); st.success(f"LOADED — {len(txt):,} CHARS")
            else: st.warning("NO INPUT")
    with t2:
        pdf_f = st.file_uploader("", type=["pdf"], label_visibility="collapsed", key="k_pdf")
        if st.button("▶ EXTRACT PDF", key="btn_pdf"):
            if pdf_f:
                try: st.session_state.doc_text = extract_pdf(pdf_f.read()); st.success(f"EXTRACTED — {len(st.session_state.doc_text):,} CHARS")
                except Exception as e: st.error(f"ERR: {e}")
            else: st.warning("UPLOAD FIRST")
    with t3:
        docx_f = st.file_uploader("", type=["docx"], label_visibility="collapsed", key="k_docx")
        if st.button("▶ EXTRACT DOCX", key="btn_docx"):
            if docx_f:
                try: st.session_state.doc_text = extract_docx(docx_f.read()); st.success(f"EXTRACTED — {len(st.session_state.doc_text):,} CHARS")
                except Exception as e: st.error(f"ERR: {e}")
            else: st.warning("UPLOAD FIRST")
    with t4:
        url_i = st.text_input("", placeholder="https://...", label_visibility="collapsed", key="k_url")
        if st.button("▶ FETCH URL", key="btn_url"):
            if url_i.startswith("http"):
                with st.spinner("FETCHING..."):
                    try:
                        t = fetch_url(url_i)
                        if len(t) < 100: st.error("INSUFFICIENT CONTENT")
                        else: st.session_state.doc_text = t[:6000]; st.success(f"FETCHED — {len(st.session_state.doc_text):,} CHARS")
                    except Exception as e: st.error(f"ERR: {e}")
            else: st.warning("INVALID URL")

    if st.session_state.doc_text:
        st.markdown(f'<div class="chip chip-ok" style="margin:0.5rem 0">✓ {len(st.session_state.doc_text):,} CHARS READY</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="sec-head"><span class="sec-num">SYS.02</span><span class="sec-title">CONFIGURATION</span></div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown('<div class="field-label">FORMAT TYPE</div>', unsafe_allow_html=True)
    inf_type = st.selectbox("", list(INFOGRAPHIC_TYPES.keys()), format_func=lambda k: INFOGRAPHIC_TYPES[k], label_visibility="collapsed")

    st.markdown('<div class="field-label">COLOR THEME</div>', unsafe_allow_html=True)
    theme = st.selectbox("", list(THEMES.keys()), label_visibility="collapsed", key="k_theme")

    st.markdown('<div class="field-label">TITLE (OPTIONAL)</div>', unsafe_allow_html=True)
    custom_title = st.text_input("", placeholder="> AUTO-GENERATED IF BLANK", label_visibility="collapsed", key="k_title")

    st.markdown("<br>", unsafe_allow_html=True)
    gen_btn = st.button("⬡  EXECUTE GENERATION", use_container_width=True)

    if st.session_state.generated:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="sec-head"><span class="sec-num">SYS.03</span><span class="sec-title">EXPORT</span></div>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        st.download_button("↓ DOWNLOAD HTML", data=st.session_state.infographic_html.encode(), file_name="infographic.html", mime="text/html")
        st.markdown("""<div style="font-family:'Share Tech Mono',monospace;font-size:0.58rem;color:#2a2a40;letter-spacing:0.08em;margin-top:0.8rem;line-height:1.9">
PNG EXPORT:<br>OPEN HTML IN BROWSER<br>CTRL+P → SAVE AS PDF<br>OR SCREENSHOT
</div>""", unsafe_allow_html=True)

with right_col:
    ready_chip = "<div class='chip chip-ok'>✓ INFOGRAPHIC RENDERED</div>" if st.session_state.generated else "<div class='chip chip-warn'>⬡ AWAITING INPUT</div>"
    st.markdown(f'<div class="canvas-header"><span class="canvas-title">// OUTPUT CANVAS</span><div>{ready_chip}</div></div>', unsafe_allow_html=True)

    st.markdown('<div style="padding:1.5rem">', unsafe_allow_html=True)
    if not st.session_state.generated or not st.session_state.infographic_html:
        hex_str = ("DEADBEEF 0A1B2C3D FF00AA 12345678 ABCDEF90 " * 60)[:600]
        st.markdown(f"""
        <div class="empty-state">
          <div class="corner-tl"></div><div class="corner-br"></div>
          <div class="empty-hex">{hex_str}</div>
          <div class="empty-content">
            <span class="empty-icon">⬡</span>
            <div class="empty-label">CANVAS EMPTY</div>
            <div class="empty-sub">LOAD DOC → CONFIG → EXECUTE GENERATION</div>
          </div>
        </div>""", unsafe_allow_html=True)
    else:
        components.html(st.session_state.infographic_html, height=960, scrolling=True)
    st.markdown('</div>', unsafe_allow_html=True)

if gen_btn:
    if not st.session_state.doc_text.strip():
        st.error("⚠ NO DOCUMENT LOADED")
    else:
        theme_desc = THEMES.get(theme, THEMES["DARK — CYBER"])
        prompt = build_prompt(st.session_state.doc_text, inf_type, custom_title, theme_desc)
        with st.spinner("⬡ PROCESSING — GENERATING INFOGRAPHIC..."):
            try:
                raw = call_groq(SYSTEM_PROMPT, prompt, max_tokens=4000, temp=0.38)
                raw = re.sub(r'^```html\s*','',raw.strip())
                raw = re.sub(r'^```\s*','',raw.strip())
                raw = re.sub(r'```$','',raw.strip())
                if not raw.strip().startswith('<!'):
                    for tag in ['<!DOCTYPE','<html']:
                        idx = raw.find(tag)
                        if idx != -1: raw = raw[idx:]; break
                st.session_state.infographic_html = raw
                st.session_state.generated = True
                st.rerun()
            except Exception as e:
                st.error(f"GENERATION FAILED: {e}")
