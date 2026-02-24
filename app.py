import streamlit as st
from groq import Groq
import os, io, re, urllib.request
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
@import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Orbitron:wght@700;900&family=Chakra+Petch:wght@300;400;500;600&display=swap');

html, body, [class*="css"] {
  font-family: 'Chakra Petch', sans-serif !important;
  background: #05050a !important;
  color: #d0d0e0 !important;
}
.stApp { background: #05050a !important; }

/* GRID BACKGROUND */
.stApp > div:first-child::before {
  content: ''; position: fixed; inset: 0; z-index: 0; pointer-events: none;
  background-image:
    linear-gradient(rgba(255,183,0,0.018) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255,183,0,0.018) 1px, transparent 1px);
  background-size: 48px 48px;
}
/* SCANLINES */
.stApp > div:first-child::after {
  content: ''; position: fixed; inset: 0; z-index: 1; pointer-events: none;
  background: repeating-linear-gradient(0deg, transparent, transparent 3px, rgba(0,0,0,0.07) 3px, rgba(0,0,0,0.07) 4px);
}

.main .block-container {
  padding: 2rem 5rem 3rem 5rem !important;
  max-width: 1500px !important;
  margin: 0 auto !important;
  position: relative; z-index: 2;
}
#MainMenu, footer, header, [data-testid="stToolbar"] { display: none !important; }

/* ── TOP BAR ── */
.topbar {
  display: flex; align-items: stretch;
  border: 1px solid #ffb700; margin-bottom: 2.5rem;
  box-shadow: 0 0 40px rgba(255,183,0,0.05);
}
.topbar-logo {
  padding: 1.1rem 2rem; border-right: 1px solid rgba(255,183,0,0.35);
  display: flex; flex-direction: column; justify-content: center;
  background: rgba(255,183,0,0.03); min-width: 200px;
}
.logo-text {
  font-family: 'Orbitron', monospace; font-size: 1.4rem; font-weight: 900;
  color: #ffb700; text-shadow: 0 0 20px rgba(255,183,0,0.5);
  letter-spacing: 0.08em; line-height: 1;
}
.logo-sub { font-family: 'Share Tech Mono', monospace; font-size: 0.55rem; color: #2a2a40; letter-spacing: 0.2em; margin-top: 0.35rem; }
.topbar-info { flex: 1; padding: 1rem 2rem; display: flex; align-items: center; gap: 3rem; }
.info-item { display: flex; flex-direction: column; gap: 0.2rem; }
.info-label { font-family: 'Share Tech Mono', monospace; font-size: 0.52rem; color: #1e1e38; letter-spacing: 0.2em; text-transform: uppercase; }
.info-val { font-family: 'Share Tech Mono', monospace; font-size: 0.68rem; color: #ffb700; letter-spacing: 0.1em; }
.topbar-status {
  padding: 1rem 1.8rem; border-left: 1px solid rgba(255,183,0,0.35);
  display: flex; flex-direction: column; align-items: flex-end; justify-content: center; gap: 0.35rem;
}
.status-row { display: flex; align-items: center; gap: 0.5rem; font-family: 'Share Tech Mono', monospace; font-size: 0.6rem; color: #00ff88; letter-spacing: 0.12em; }
.blink-dot { width: 5px; height: 5px; border-radius: 50%; background: #00ff88; animation: blink 1.4s ease-in-out infinite; flex-shrink: 0; }
@keyframes blink { 0%,100%{opacity:1} 50%{opacity:0.1} }

/* ── PANEL HEADERS ── */
.panel-hdr {
  display: flex; align-items: center; gap: 0.8rem;
  padding: 0.6rem 1rem; border: 1px solid #141420;
  background: rgba(255,183,0,0.015); margin-bottom: 1rem;
}
.panel-num { font-family: 'Orbitron', monospace; font-size: 0.52rem; color: #ffb700; letter-spacing: 0.18em; background: rgba(255,183,0,0.08); padding: 0.12rem 0.45rem; border: 1px solid rgba(255,183,0,0.2); }
.panel-name { font-family: 'Share Tech Mono', monospace; font-size: 0.6rem; color: #2a2a45; letter-spacing: 0.22em; text-transform: uppercase; }

/* ── FIELD LABELS ── */
.flabel { font-family: 'Share Tech Mono', monospace; font-size: 0.56rem; color: #252540; letter-spacing: 0.2em; text-transform: uppercase; margin-top: 0.9rem; margin-bottom: 0.3rem; }
.flabel:first-child { margin-top: 0; }

/* ── TABS ── */
div[data-baseweb="tab-list"] {
  background: #080810 !important; border: 1px solid #141420 !important;
  border-bottom: 1px solid #ffb700 !important; border-radius: 0 !important;
  padding: 0 !important; gap: 0 !important; margin-bottom: 0.8rem;
}
div[data-baseweb="tab"] {
  background: transparent !important; border-radius: 0 !important; color: #252540 !important;
  font-family: 'Share Tech Mono', monospace !important; font-size: 0.6rem !important;
  padding: 0.5rem 1rem !important; letter-spacing: 0.12em; text-transform: uppercase;
  border-bottom: 2px solid transparent !important; margin-bottom: -1px; transition: color 0.15s !important;
}
div[data-baseweb="tab"]:hover { color: #ffb700 !important; }
div[aria-selected="true"] { background: rgba(255,183,0,0.05) !important; color: #ffb700 !important; border-bottom: 2px solid #ffb700 !important; }

/* ── TEXTAREA ── */
div[data-testid="stTextArea"] label { display: none !important; }
div[data-testid="stTextArea"] textarea {
  background: #08080f !important; border: 1px solid #141420 !important; border-radius: 0 !important;
  color: #ffb700 !important; font-family: 'Share Tech Mono', monospace !important;
  font-size: 0.76rem !important; line-height: 1.85 !important; padding: 0.85rem 1rem !important;
  caret-color: #ffb700 !important; resize: none !important; transition: border-color 0.2s !important;
}
div[data-testid="stTextArea"] textarea:focus { border-color: #ffb700 !important; box-shadow: 0 0 14px rgba(255,183,0,0.08) !important; outline: none !important; }
div[data-testid="stTextArea"] textarea::placeholder { color: #1a1a30 !important; font-family: 'Share Tech Mono', monospace !important; }

/* ── TEXT INPUT ── */
div[data-testid="stTextInput"] label { display: none !important; }
.stTextInput input {
  background: #08080f !important; border: 1px solid #141420 !important; border-radius: 0 !important;
  color: #ffb700 !important; font-family: 'Share Tech Mono', monospace !important;
  font-size: 0.73rem !important; padding: 0.62rem 0.9rem !important; transition: border-color 0.2s !important;
}
.stTextInput input:focus { border-color: #ffb700 !important; box-shadow: 0 0 10px rgba(255,183,0,0.08) !important; }
.stTextInput input::placeholder { color: #1a1a30 !important; }

/* ── SELECT ── */
div[data-testid="stSelectbox"] label { display: none !important; }
div[data-baseweb="select"] > div {
  background: #08080f !important; border: 1px solid #141420 !important; border-radius: 0 !important;
  color: #ffb700 !important; font-family: 'Share Tech Mono', monospace !important; font-size: 0.73rem !important;
}
div[data-baseweb="select"] > div:focus-within { border-color: #ffb700 !important; }

/* ── FILE UPLOADER ── */
div[data-testid="stFileUploader"] label { display: none !important; }
[data-testid="stFileUploader"] section { background: #08080f !important; border: 1px dashed #141420 !important; border-radius: 0 !important; padding: 1rem !important; }
[data-testid="stFileUploader"] section:hover { border-color: #ffb700 !important; }
[data-testid="stFileUploader"] span { font-family: 'Share Tech Mono', monospace !important; font-size: 0.65rem !important; color: #252540 !important; }

/* ── BUTTONS ── */
.stButton > button {
  background: transparent !important; border: 1px solid #ffb700 !important; border-radius: 0 !important;
  color: #ffb700 !important; font-family: 'Orbitron', monospace !important; font-weight: 700 !important;
  font-size: 0.65rem !important; letter-spacing: 0.18em !important; padding: 0.58rem 1rem !important;
  text-transform: uppercase !important; width: 100% !important; transition: all 0.15s !important; margin-top: 0.25rem !important;
}
.stButton > button:hover { background: #ffb700 !important; color: #05050a !important; box-shadow: 0 0 22px rgba(255,183,0,0.3) !important; }

.stDownloadButton > button {
  background: transparent !important; border: 1px solid #00ff88 !important; border-radius: 0 !important;
  color: #00ff88 !important; font-family: 'Share Tech Mono', monospace !important; font-size: 0.62rem !important;
  padding: 0.42rem 0.9rem !important; letter-spacing: 0.1em; width: auto !important; text-transform: none !important; margin-top: 0 !important;
}
.stDownloadButton > button:hover { background: rgba(0,255,136,0.06) !important; }

/* ── CHIPS ── */
.chip { display: inline-flex; align-items: center; gap: 0.35rem; font-family: 'Share Tech Mono', monospace; font-size: 0.58rem; padding: 0.2rem 0.65rem; letter-spacing: 0.1em; border: 1px solid; margin: 0.35rem 0; }
.chip-ok { border-color: rgba(0,255,136,0.3); color: #00ff88; background: rgba(0,255,136,0.05); }
.chip-wait { border-color: rgba(255,183,0,0.3); color: #ffb700; background: rgba(255,183,0,0.04); }

/* ── CANVAS ── */
.canvas-topbar { display: flex; align-items: center; justify-content: space-between; padding: 0.62rem 1.2rem; border: 1px solid #141420; border-bottom: none; background: rgba(255,183,0,0.015); }
.canvas-label { font-family: 'Share Tech Mono', monospace; font-size: 0.58rem; color: #252540; letter-spacing: 0.22em; text-transform: uppercase; }

/* ── EMPTY STATE ── */
.empty-canvas { min-height: 580px; border: 1px solid #141420; display: flex; align-items: center; justify-content: center; position: relative; overflow: hidden; }
.empty-bg { position: absolute; inset: 0; display: flex; align-items: center; justify-content: center; font-family: 'Share Tech Mono', monospace; font-size: 0.58rem; color: #0c0c1a; letter-spacing: 0.05em; line-height: 2.2; word-break: break-all; padding: 2.5rem; pointer-events: none; }
.empty-center { position: relative; z-index: 1; text-align: center; }
.empty-icon { font-family: 'Orbitron', monospace; font-size: 2.5rem; color: #111128; display: block; margin-bottom: 1.2rem; animation: pulse 2.5s ease-in-out infinite; }
@keyframes pulse { 0%,100%{opacity:0.35;transform:scale(1)} 50%{opacity:0.65;transform:scale(1.04)} }
.empty-main { font-family: 'Orbitron', monospace; font-size: 0.75rem; color: #111128; letter-spacing: 0.25em; line-height: 1.9; }
.empty-sub { font-family: 'Share Tech Mono', monospace; font-size: 0.55rem; color: #0c0c1a; letter-spacing: 0.15em; margin-top: 0.6rem; }
.corner { position: absolute; width: 14px; height: 14px; }
.c-tl { top:0;left:0; border-top:1px solid rgba(255,183,0,0.4); border-left:1px solid rgba(255,183,0,0.4); }
.c-tr { top:0;right:0; border-top:1px solid rgba(255,183,0,0.4); border-right:1px solid rgba(255,183,0,0.4); }
.c-bl { bottom:0;left:0; border-bottom:1px solid rgba(255,183,0,0.4); border-left:1px solid rgba(255,183,0,0.4); }
.c-br { bottom:0;right:0; border-bottom:1px solid rgba(255,183,0,0.4); border-right:1px solid rgba(255,183,0,0.4); }

/* ALERTS */
.stSuccess > div { font-family:'Share Tech Mono',monospace !important; font-size:0.7rem !important; border-radius:0 !important; background:rgba(0,255,136,0.05) !important; border:1px solid rgba(0,255,136,0.2) !important; color:#00ff88 !important; }
.stError > div { font-family:'Share Tech Mono',monospace !important; font-size:0.7rem !important; border-radius:0 !important; background:rgba(255,60,90,0.05) !important; border:1px solid rgba(255,60,90,0.2) !important; color:#ff3c5a !important; }
.stWarning > div { font-family:'Share Tech Mono',monospace !important; font-size:0.7rem !important; border-radius:0 !important; }

::-webkit-scrollbar { width:3px; height:3px; }
::-webkit-scrollbar-track { background:#05050a; }
::-webkit-scrollbar-thumb { background:#1a1a2e; }
::-webkit-scrollbar-thumb:hover { background:rgba(255,183,0,0.4); }
</style>
""", unsafe_allow_html=True)

# ── SESSION ──
for k,v in [("doc_text",""),("html_out",""),("generated",False)]:
    if k not in st.session_state: st.session_state[k] = v

# ── HELPERS ──
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
    return re.sub(r'\s+',' ', re.sub(r'<[^>]+>',' ',txt)).strip()

def call_groq(system, user, max_tokens=4000, temp=0.35):
    r = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role":"system","content":system},{"role":"user","content":user}],
        temperature=temp, max_tokens=max_tokens
    )
    return r.choices[0].message.content.strip()

TYPES = {
    "auto":"🤖  AI DECIDES", "summary":"📋  KEY POINTS",
    "timeline":"⏱   TIMELINE", "stats":"📊  STATS / DATA",
    "comparison":"⚖   COMPARISON", "process":"🔄  PROCESS FLOW", "report":"📑  FULL REPORT",
}
THEMES = {
    "TEAL & CYAN (like sample)": "#0a2a35 bg, #00bcd4 teal, #26c6da cyan, #80deea light cyan, white text — like a professional graphic design infographic",
    "DARK CYBER — Neon Blue": "#090914 bg, #00e5ff cyan, #3b82f6 blue, #9f00ff purple, glassmorphism",
    "TERMINAL — Amber/Black": "#050505 bg, #ffb700 amber, #ff6b00 orange, monochrome terminal",
    "BIO — Emerald/Teal": "#071a12 bg, #00ff88 emerald, #00d4aa teal, bioluminescent",
    "EDITORIAL — White/Navy": "#ffffff bg, #0f172a navy, #2563eb blue, clean magazine",
    "WARM — Cream/Terracotta": "#faf8f4 bg, #1c1917 charcoal, #dc6e2e terracotta, #f59e0b gold",
    "LUXURY — Black/Gold": "#080508 bg, #ffd700 gold, #ff2d55 crimson, dramatic luxury",
}

SYS = """You are a world-class infographic designer who creates stunning visual infographics like those made in professional design tools (Canva, Adobe, Piktochart).
Generate a COMPLETE SELF-CONTAINED HTML infographic.
Return ONLY valid HTML starting with <!DOCTYPE html> — absolutely no markdown, no code fences, no explanations.
All CSS inside <style> tag. Import Google Fonts in HTML head.
Width: exactly 900px centered. Use any height needed.
CRITICAL: Create REAL visual charts and graphs using pure CSS and SVG — donut charts, bar charts, progress rings, line charts, stat circles. NO plain text lists."""

def build_prompt(text, itype, title, theme):
    type_instructions = {
        "auto": """Analyze the content and choose the BEST layout. 
Mix multiple visual elements: stat circles with big numbers, donut/pie charts using SVG, 
bar chart comparisons, timeline with icons, key insight cards with icons.""",

        "summary": """KEY POINTS infographic layout:
- Header section with title and subtitle on colored background
- 4-6 numbered insight cards in 2-column grid, each with an emoji icon, bold heading, description
- One large pull-quote or highlight stat in the center  
- Visual icons and decorative shapes throughout
- Footer with source/summary""",

        "timeline": """TIMELINE infographic layout:
- Bold header section
- Vertical timeline with alternating left/right content cards
- Each event: year/date badge, title, description, icon
- Connecting line with dot markers
- Color-coded by era or phase""",

        "stats": """STATS & DATA infographic layout — make it look like the reference image:
- Header bar with title
- Row of 3-4 large stat circles (SVG circles with percentage fill animation)
- CSS bar charts comparing multiple metrics
- SVG donut charts for proportional data
- Large hero numbers with labels
- Mini line chart using SVG polyline
- Data source footer""",

        "comparison": """COMPARISON infographic layout:
- Bold title header
- Two-column VS layout with colored headers per side
- Feature comparison rows with ✓ and ✗ marks
- Central divider with VS badge
- Pros/cons cards
- Summary recommendation banner""",

        "process": """PROCESS FLOW infographic layout:
- Title header
- Numbered steps 1-N in cards connected by arrows
- Each step: number badge, icon emoji, title, description
- Arrow connectors between steps
- Color progression from start to end
- Tips or notes sidebar""",

        "report": """COMPREHENSIVE REPORT infographic layout — like a full dashboard:
- Hero header with title, subtitle, date
- Top row: 4 key metric cards with big numbers and icons
- Middle: 2-3 content sections with charts and text
- SVG bar charts and donut charts
- Timeline section if applicable  
- Highlighted callout box
- Summary footer""",
    }

    t = f'Use this exact title: "{title}"' if title.strip() else "Generate a compelling specific title from the document."

    return f"""Create a stunning, visually rich professional infographic — like those made in Canva or Piktochart.

INFOGRAPHIC TYPE: {type_instructions.get(itype, type_instructions['auto'])}

TITLE: {t}

COLOR THEME: {theme}

CRITICAL DESIGN REQUIREMENTS:
1. Width: 900px exactly, margin: 0 auto, centered
2. MUST include SVG-based visual charts — at least one of:
   - SVG donut/pie chart (use <circle> stroke-dasharray for ring charts)
   - CSS bar chart (divs with percentage widths and labels)  
   - SVG circle stat (stroke-dasharray ring showing percentage)
   - SVG line/area chart (polyline or path)
3. Use emoji icons as visual accents throughout (📊 📈 🎯 ⭐ 💡 🔑 etc.)
4. Color-coded sections — each major section uses theme accent color variations
5. Cards with subtle shadows: box-shadow: 0 4px 20px rgba(0,0,0,0.15)
6. Bold typography contrast: 2.5rem+ for numbers, 0.8rem for body
7. CSS entrance animations: @keyframes fadeInUp with animation-delay staggering
8. Decorative geometric shapes (circles, lines, dots) as background accents
9. Import Google Fonts — use 2 complementary fonts (one display, one body)
10. Professional layout: proper padding, visual hierarchy, breathing space

EXAMPLE SVG DONUT CHART (use this pattern for circular charts):
<svg width="120" height="120" viewBox="0 0 120 120">
  <circle cx="60" cy="60" r="50" fill="none" stroke="#1a1a2e" stroke-width="12"/>
  <circle cx="60" cy="60" r="50" fill="none" stroke="#00bcd4" stroke-width="12"
    stroke-dasharray="220 314" stroke-dashoffset="-78" stroke-linecap="round"/>
  <text x="60" y="65" text-anchor="middle" font-size="18" font-weight="bold" fill="white">70%</text>
</svg>

DOCUMENT CONTENT TO VISUALIZE:
{text[:5000]}

Return ONLY the complete HTML. Start with <!DOCTYPE html>. Make it beautiful."""

# ─── TOP BAR ───
st.markdown("""
<div class="topbar">
  <div class="topbar-logo">
    <div class="logo-text">INFOGRAPH.AI</div>
    <div class="logo-sub">Document → Visual Intelligence</div>
  </div>
  <div class="topbar-info">
    <div class="info-item"><div class="info-label">Input</div><div class="info-val">PDF · DOCX · TEXT · URL</div></div>
    <div class="info-item"><div class="info-label">Output</div><div class="info-val">HTML + PNG</div></div>
    <div class="info-item"><div class="info-label">Engine</div><div class="info-val">GROQ LLAMA 3.1</div></div>
    <div class="info-item"><div class="info-label">Visual</div><div class="info-val">CHARTS · GRAPHS · RINGS</div></div>
  </div>
  <div class="topbar-status">
    <div class="status-row"><div class="blink-dot"></div>SYSTEM ONLINE</div>
    <div style="font-family:'Share Tech Mono',monospace;font-size:0.52rem;color:#151528;letter-spacing:0.1em">API CONNECTED</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ─── COLUMNS ───
lcol, rcol = st.columns([1, 2.4], gap="large")

with lcol:
    st.markdown('<div class="panel-hdr"><span class="panel-num">SYS.01</span><span class="panel-name">Document Input</span></div>', unsafe_allow_html=True)
    t1,t2,t3,t4 = st.tabs(["TEXT","PDF","DOCX","URL"])

    with t1:
        txt = st.text_area("", height=175,
            placeholder="> PASTE DOCUMENT, REPORT\n> ARTICLE OR ANY TEXT...",
            label_visibility="collapsed", key="itxt")
        if st.button("LOAD TEXT", key="btxt"):
            if txt.strip(): st.session_state.doc_text=txt.strip(); st.success(f"✓ LOADED — {len(txt):,} CHARS")
            else: st.warning("NO INPUT DETECTED")
    with t2:
        pf = st.file_uploader("", type=["pdf"], label_visibility="collapsed", key="ipdf")
        if st.button("EXTRACT PDF", key="bpdf"):
            if pf:
                try: st.session_state.doc_text=extract_pdf(pf.read()); st.success(f"✓ EXTRACTED — {len(st.session_state.doc_text):,} CHARS")
                except Exception as e: st.error(f"FAILED: {e}")
            else: st.warning("UPLOAD FILE FIRST")
    with t3:
        df = st.file_uploader("", type=["docx"], label_visibility="collapsed", key="idocx")
        if st.button("EXTRACT DOCX", key="bdocx"):
            if df:
                try: st.session_state.doc_text=extract_docx(df.read()); st.success(f"✓ EXTRACTED — {len(st.session_state.doc_text):,} CHARS")
                except Exception as e: st.error(f"FAILED: {e}")
            else: st.warning("UPLOAD FILE FIRST")
    with t4:
        ui = st.text_input("", placeholder="> https://...", label_visibility="collapsed", key="iurl")
        if st.button("FETCH URL", key="burl"):
            if ui.startswith("http"):
                with st.spinner("FETCHING..."):
                    try:
                        t = fetch_url(ui)
                        if len(t)<100: st.error("INSUFFICIENT CONTENT")
                        else: st.session_state.doc_text=t[:6000]; st.success(f"✓ FETCHED — {len(st.session_state.doc_text):,} CHARS")
                    except Exception as e: st.error(f"FAILED: {e}")
            else: st.warning("INVALID URL")

    if st.session_state.doc_text:
        st.markdown(f'<div class="chip chip-ok">✓ {len(st.session_state.doc_text):,} CHARS READY</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="panel-hdr"><span class="panel-num">SYS.02</span><span class="panel-name">Configuration</span></div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown('<div class="flabel">Infographic Format</div>', unsafe_allow_html=True)
    itype = st.selectbox("", list(TYPES.keys()), format_func=lambda k: TYPES[k], label_visibility="collapsed", key="itype")

    st.markdown('<div class="flabel">Color Theme</div>', unsafe_allow_html=True)
    theme = st.selectbox("", list(THEMES.keys()), label_visibility="collapsed", key="itheme")

    st.markdown('<div class="flabel">Custom Title (optional)</div>', unsafe_allow_html=True)
    ctitle = st.text_input("", placeholder="> Leave blank for AI auto-title...", label_visibility="collapsed", key="ictitle")

    st.markdown("<br>", unsafe_allow_html=True)
    gen = st.button("⬡  EXECUTE GENERATION", use_container_width=True)

    if st.session_state.generated:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="panel-hdr"><span class="panel-num">SYS.03</span><span class="panel-name">Export</span></div>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        st.download_button("↓  DOWNLOAD HTML", data=st.session_state.html_out.encode(), file_name="infographic.html", mime="text/html")
        st.markdown("""<div style="font-family:'Share Tech Mono',monospace;font-size:0.54rem;color:#1a1a35;letter-spacing:0.1em;line-height:2;margin-top:0.8rem">
PNG: OPEN HTML IN CHROME<br>CTRL+SHIFT+P → SCREENSHOT<br>OR CTRL+P → SAVE AS PDF</div>""", unsafe_allow_html=True)

with rcol:
    ready = st.session_state.generated and st.session_state.html_out
    chip = '<span class="chip chip-ok">✓ INFOGRAPHIC RENDERED</span>' if ready else '<span class="chip chip-wait">⬡ AWAITING INPUT</span>'
    st.markdown(f'<div class="canvas-topbar"><span class="canvas-label">// OUTPUT CANVAS</span>{chip}</div>', unsafe_allow_html=True)

    if not ready:
        hex_fill = "FF A0 B1 C2 D3 E4 00 1A 2B 3C 4D 5E 6F 7A 8B DEAD BEEF CAFE BABE F00D " * 25
        st.markdown(f"""
        <div class="empty-canvas">
          <div class="corner c-tl"></div><div class="corner c-tr"></div>
          <div class="corner c-bl"></div><div class="corner c-br"></div>
          <div class="empty-bg">{hex_fill[:480]}</div>
          <div class="empty-center">
            <span class="empty-icon">⬡</span>
            <div class="empty-main">CANVAS EMPTY<br>AWAITING DOCUMENT</div>
            <div class="empty-sub">LOAD INPUT → CONFIGURE → EXECUTE</div>
          </div>
        </div>""", unsafe_allow_html=True)
    else:
        components.html(st.session_state.html_out, height=980, scrolling=True)

# ─── GENERATE ───
if gen:
    if not st.session_state.doc_text.strip():
        st.error("⚠ NO DOCUMENT LOADED")
    else:
        theme_desc = THEMES.get(theme, list(THEMES.values())[0])
        prompt = build_prompt(st.session_state.doc_text, itype, ctitle, theme_desc)
        with st.spinner("⬡  GENERATING INFOGRAPHIC WITH CHARTS & VISUALIZATIONS..."):
            try:
                raw = call_groq(SYS, prompt, max_tokens=4000, temp=0.38)
                raw = re.sub(r'^```html\s*','',raw.strip())
                raw = re.sub(r'^```\s*','',raw.strip())
                raw = re.sub(r'```\s*$','',raw.strip())
                if not raw.strip().startswith('<!'):
                    for tag in ['<!DOCTYPE','<html','<HTML']:
                        idx = raw.find(tag)
                        if idx != -1: raw = raw[idx:]; break
                st.session_state.html_out = raw
                st.session_state.generated = True
                st.rerun()
            except Exception as e:
                st.error(f"GENERATION FAILED: {e}")
