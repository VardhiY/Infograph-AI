import streamlit as st
from groq import Groq
import os, io, re, urllib.request
import streamlit.components.v1 as components

st.set_page_config(page_title="InfographAI", page_icon="🎨", layout="wide")

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
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;600&display=swap');

/* ═══════════════════════════════════════════
   NUCLEAR OPTION — FORCE ALL TEXT VISIBLE
═══════════════════════════════════════════ */

/* Every possible Streamlit text element */
.stApp, .stApp *,
.stApp p, .stApp span, .stApp div, .stApp label,
.stApp h1, .stApp h2, .stApp h3, .stApp h4,
[data-testid="stMarkdownContainer"],
[data-testid="stMarkdownContainer"] *,
[data-testid="stText"], [data-testid="stText"] *,
.stMarkdown, .stMarkdown *,
section[data-testid="stSidebar"] *,
.element-container, .element-container *,
.stForm, .stForm *,
[class*="st-"] {
  font-family: 'Plus Jakarta Sans', sans-serif !important;
  color: #e6edf3 !important;
}

/* Tab labels — force white */
button[data-baseweb="tab"] p,
button[data-baseweb="tab"] span,
button[data-baseweb="tab"] div,
button[data-baseweb="tab"],
[role="tab"], [role="tab"] * {
  color: #e6edf3 !important;
  font-size: 1rem !important;
  font-weight: 600 !important;
}
[aria-selected="true"], [aria-selected="true"] *,
[aria-selected="true"] p, [aria-selected="true"] span {
  color: #ffffff !important;
  font-weight: 700 !important;
}

/* Select dropdown text */
[data-baseweb="select"] *,
[data-baseweb="select"] span,
[data-baseweb="select"] div,
[data-baseweb="select"] p,
[data-baseweb="menu"] *,
[data-baseweb="menu"] span,
[data-baseweb="menu"] li,
[role="option"], [role="option"] * {
  color: #e6edf3 !important;
  font-size: 1rem !important;
}

/* Input fields text */
input, input::placeholder,
textarea, textarea::placeholder,
select, select * {
  color: #e6edf3 !important;
  font-size: 1rem !important;
}
input::placeholder, textarea::placeholder {
  color: #6e7681 !important;
  opacity: 1 !important;
}

/* Upload widget text */
[data-testid="stFileUploader"] *,
[data-testid="stFileUploader"] span,
[data-testid="stFileUploader"] p,
[data-testid="stFileUploadDropzone"] * {
  color: #8b949e !important;
  font-size: 0.95rem !important;
}

/* Button text */
.stButton button, .stButton button *,
.stButton button p, .stButton button span {
  color: #ffffff !important;
  font-size: 1.05rem !important;
  font-weight: 700 !important;
}

/* Alert text */
.stSuccess, .stSuccess *, .stSuccess p,
.stError, .stError *, .stError p,
.stWarning, .stWarning *, .stWarning p,
.stInfo, .stInfo *, .stInfo p {
  font-size: 0.95rem !important;
  font-weight: 500 !important;
}
.stSuccess, .stSuccess * { color: #3fb950 !important; }
.stError, .stError * { color: #f85149 !important; }
.stWarning, .stWarning * { color: #d29922 !important; }

/* Spinner */
[data-testid="stSpinner"] *, [data-testid="stSpinner"] p {
  color: #a78bfa !important;
  font-size: 1rem !important;
}

/* ═══════════════════════════════════════════
   APP LAYOUT
═══════════════════════════════════════════ */
.stApp { background: #0d1117 !important; }

.main .block-container {
  padding: 2rem 4rem 4rem 4rem !important;
  max-width: 1440px !important;
  margin: 0 auto !important;
}
#MainMenu, footer, header, [data-testid="stToolbar"] { display: none !important; }

/* ── NAVBAR ── */
.navbar {
  display: flex; align-items: center; justify-content: space-between;
  padding: 1.2rem 2rem; background: #161b22;
  border: 1px solid #30363d; border-radius: 14px; margin-bottom: 2.5rem;
}
.nav-brand { display: flex; align-items: center; gap: 0.9rem; }
.nav-icon {
  width: 44px; height: 44px; border-radius: 10px;
  background: linear-gradient(135deg, #6366f1, #a855f7);
  display: flex; align-items: center; justify-content: center; font-size: 1.4rem;
}
.nav-title {
  font-size: 1.5rem !important; font-weight: 800 !important;
  color: #ffffff !important; letter-spacing: -0.02em;
  font-family: 'Plus Jakarta Sans', sans-serif !important;
}
.nav-title span { color: #a78bfa !important; }
.nav-pill {
  font-family: 'JetBrains Mono', monospace !important;
  font-size: 0.8rem !important; font-weight: 600 !important;
  padding: 0.38rem 1rem; border-radius: 6px;
  background: #21262d; color: #c9d1d9 !important;
  border: 1px solid #30363d; letter-spacing: 0.04em;
  display: inline-block;
}
.nav-pills { display: flex; gap: 0.5rem; flex-wrap: wrap; }
.nav-status {
  display: flex; align-items: center; gap: 0.6rem;
  font-size: 0.9rem !important; font-weight: 600 !important;
  color: #3fb950 !important;
  background: rgba(63,185,80,0.1); border: 1px solid rgba(63,185,80,0.3);
  padding: 0.5rem 1.1rem; border-radius: 20px;
}
.pulse {
  width: 8px; height: 8px; border-radius: 50%;
  background: #3fb950; flex-shrink: 0;
  animation: pulse 1.5s ease-in-out infinite;
}
@keyframes pulse { 0%,100%{opacity:1} 50%{opacity:0.2} }

/* ── SECTION HEADERS ── */
.sec-header { display: flex; align-items: center; gap: 0.8rem; margin-bottom: 1.1rem; }
.sec-icon {
  width: 36px; height: 36px; border-radius: 8px;
  background: rgba(99,102,241,0.2);
  display: flex; align-items: center; justify-content: center;
  font-size: 1.05rem; flex-shrink: 0;
}
.sec-title {
  font-size: 1.05rem !important; font-weight: 700 !important;
  color: #f0f6fc !important; font-family: 'Plus Jakarta Sans', sans-serif !important;
}
.sec-sub {
  font-size: 0.85rem !important; color: #8b949e !important;
  font-weight: 400 !important; margin-top: 0.1rem;
  font-family: 'Plus Jakarta Sans', sans-serif !important;
}

/* ── FIELD LABELS ── */
.flabel {
  display: block;
  font-family: 'JetBrains Mono', monospace !important;
  font-size: 0.82rem !important; font-weight: 600 !important;
  color: #8b949e !important; letter-spacing: 0.06em;
  text-transform: uppercase; margin-bottom: 0.45rem; margin-top: 1.2rem;
}

/* ── TABS ── */
div[data-baseweb="tab-list"] {
  background: #161b22 !important; border: 1px solid #30363d !important;
  border-radius: 10px !important; padding: 4px !important;
  gap: 3px !important; margin-bottom: 1rem;
}
div[data-baseweb="tab"] {
  background: transparent !important; border-radius: 7px !important;
  padding: 0.5rem 1.1rem !important; transition: all 0.15s !important;
  min-height: unset !important;
}
div[data-baseweb="tab"]:hover { background: #21262d !important; }
div[aria-selected="true"] { background: #21262d !important; }

/* ── TEXTAREA ── */
div[data-testid="stTextArea"] label { display: none !important; }
div[data-testid="stTextArea"] textarea {
  background: #161b22 !important; border: 1px solid #30363d !important;
  border-radius: 10px !important; color: #e6edf3 !important;
  font-size: 1rem !important; line-height: 1.8 !important;
  padding: 1rem 1.1rem !important; resize: none !important;
  caret-color: #6366f1 !important;
}
div[data-testid="stTextArea"] textarea:focus {
  border-color: #6366f1 !important;
  box-shadow: 0 0 0 3px rgba(99,102,241,0.15) !important;
  outline: none !important;
}

/* ── TEXT INPUT ── */
div[data-testid="stTextInput"] label { display: none !important; }
.stTextInput input {
  background: #161b22 !important; border: 1px solid #30363d !important;
  border-radius: 10px !important; color: #e6edf3 !important;
  font-size: 1rem !important; padding: 0.7rem 1.1rem !important;
}
.stTextInput input:focus {
  border-color: #6366f1 !important;
  box-shadow: 0 0 0 3px rgba(99,102,241,0.15) !important;
}

/* ── SELECT ── */
div[data-testid="stSelectbox"] label { display: none !important; }
div[data-baseweb="select"] > div {
  background: #161b22 !important; border: 1px solid #30363d !important;
  border-radius: 10px !important; min-height: 48px !important;
}
[data-baseweb="popover"] {
  background: #161b22 !important; border: 1px solid #30363d !important;
  border-radius: 10px !important;
}
[role="option"] { padding: 0.65rem 1.1rem !important; }
[role="option"]:hover { background: rgba(99,102,241,0.15) !important; }

/* ── FILE UPLOADER ── */
div[data-testid="stFileUploader"] label { display: none !important; }
[data-testid="stFileUploader"] section {
  background: #161b22 !important; border: 2px dashed #30363d !important;
  border-radius: 10px !important; padding: 1.5rem !important;
}
[data-testid="stFileUploader"] section:hover { border-color: #6366f1 !important; }

/* ── BUTTONS ── */
.stButton > button {
  background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
  border: none !important; border-radius: 10px !important;
  font-weight: 700 !important; font-size: 1.05rem !important;
  padding: 0.7rem 1.5rem !important; width: 100% !important;
  transition: all 0.2s !important;
  box-shadow: 0 4px 15px rgba(99,102,241,0.35) !important;
  margin-top: 0.4rem !important;
}
.stButton > button:hover {
  transform: translateY(-2px) !important;
  box-shadow: 0 8px 25px rgba(99,102,241,0.5) !important;
}
.stDownloadButton > button {
  background: rgba(63,185,80,0.12) !important;
  border: 1px solid rgba(63,185,80,0.4) !important;
  border-radius: 10px !important;
  font-weight: 700 !important; font-size: 0.95rem !important;
  padding: 0.55rem 1.3rem !important; width: auto !important;
  box-shadow: none !important; margin-top: 0 !important;
}
.stDownloadButton > button:hover {
  background: rgba(63,185,80,0.2) !important; transform: none !important;
}

/* ── ALERTS ── */
.stSuccess > div {
  background: rgba(63,185,80,0.1) !important;
  border: 1px solid rgba(63,185,80,0.3) !important;
  border-radius: 10px !important;
}
.stError > div {
  background: rgba(248,81,73,0.1) !important;
  border: 1px solid rgba(248,81,73,0.3) !important;
  border-radius: 10px !important;
}
.stWarning > div {
  background: rgba(210,153,34,0.1) !important;
  border: 1px solid rgba(210,153,34,0.3) !important;
  border-radius: 10px !important;
}

/* ── BADGES ── */
.badge {
  display: inline-flex; align-items: center; gap: 0.4rem;
  font-size: 0.85rem !important; font-weight: 600 !important;
  padding: 0.32rem 0.9rem; border-radius: 20px;
  font-family: 'Plus Jakarta Sans', sans-serif !important;
}
.badge-green { background: rgba(63,185,80,0.12); color: #3fb950 !important; border: 1px solid rgba(63,185,80,0.3); }
.badge-yellow { background: rgba(210,153,34,0.12); color: #d29922 !important; border: 1px solid rgba(210,153,34,0.3); }

/* ── DIVIDER ── */
.hr { height: 1px; background: #21262d; margin: 1.4rem 0; }

/* ── CANVAS ── */
.canvas-header {
  display: flex; align-items: center; justify-content: space-between;
  padding: 1.1rem 1.6rem; background: #161b22;
  border: 1px solid #30363d; border-radius: 14px 14px 0 0;
}
.canvas-title {
  font-size: 1.05rem !important; font-weight: 700 !important;
  color: #f0f6fc !important;
  font-family: 'Plus Jakarta Sans', sans-serif !important;
}
.canvas-body {
  border: 1px solid #30363d; border-top: none;
  border-radius: 0 0 14px 14px; overflow: hidden;
}

/* ── EMPTY STATE ── */
.empty-state {
  min-height: 580px; background: #0d1117;
  display: flex; align-items: center; justify-content: center;
  position: relative; overflow: hidden;
}
.empty-grid {
  position: absolute; inset: 0; pointer-events: none;
  background-image:
    linear-gradient(rgba(99,102,241,0.05) 1px, transparent 1px),
    linear-gradient(90deg, rgba(99,102,241,0.05) 1px, transparent 1px);
  background-size: 40px 40px;
}
.empty-inner { position: relative; z-index: 1; text-align: center; padding: 2rem; }
.empty-emoji { font-size: 4rem; display: block; margin-bottom: 1.2rem; animation: float 3s ease-in-out infinite; }
@keyframes float { 0%,100%{transform:translateY(0)} 50%{transform:translateY(-10px)} }
.empty-title {
  font-size: 1.5rem !important; font-weight: 800 !important;
  color: #21262d !important; margin-bottom: 0.5rem;
  font-family: 'Plus Jakarta Sans', sans-serif !important;
}
.empty-desc {
  font-size: 0.95rem !important; color: #161b22 !important;
  line-height: 1.7; font-family: 'Plus Jakarta Sans', sans-serif !important;
}
.steps { display: flex; gap: 1rem; margin-top: 2rem; justify-content: center; }
.step { background: #161b22; border: 1px solid #21262d; border-radius: 10px; padding: 1rem 1.4rem; text-align: center; }
.step-n {
  font-size: 0.75rem !important; color: #6366f1 !important;
  font-weight: 700 !important; font-family: 'JetBrains Mono', monospace !important;
  letter-spacing: 0.1em; margin-bottom: 0.35rem;
}
.step-t {
  font-size: 0.9rem !important; color: #21262d !important;
  font-weight: 700 !important; font-family: 'Plus Jakarta Sans', sans-serif !important;
}

/* export hint */
.export-hint {
  font-size: 0.88rem !important; color: #8b949e !important;
  line-height: 2; margin-top: 0.9rem;
  font-family: 'Plus Jakarta Sans', sans-serif !important;
}
.export-hint strong { color: #c9d1d9 !important; font-weight: 600 !important; }

::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: #0d1117; }
::-webkit-scrollbar-thumb { background: #30363d; border-radius: 4px; }
::-webkit-scrollbar-thumb:hover { background: #6366f1; }
</style>
""", unsafe_allow_html=True)

# ── SESSION ──
for k,v in [("doc_text",""),("html_out",""),("generated",False)]:
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
    return re.sub(r'\s+',' ', re.sub(r'<[^>]+>',' ',txt)).strip()

def call_groq(system, user, max_tokens=4000, temp=0.35):
    r = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role":"system","content":system},{"role":"user","content":user}],
        temperature=temp, max_tokens=max_tokens
    )
    return r.choices[0].message.content.strip()

TYPES = {
    "auto":       "🤖  AI Decides Best Format",
    "summary":    "📋  Key Points & Insights",
    "timeline":   "⏱  Timeline & Events",
    "stats":      "📊  Stats & Data Visualization",
    "comparison": "⚖  Comparison & Analysis",
    "process":    "🔄  Process Flow & Steps",
    "report":     "📑  Full Report Dashboard",
}
THEMES = {
    "Teal & Cyan":          "#0a2535 dark bg, #00bcd4 teal, #26c6da cyan, white text",
    "Dark Indigo & Purple": "#0a0f1e dark bg, #6366f1 indigo, #8b5cf6 purple, #e0e7ff text",
    "Emerald & Green":      "#071c12 dark bg, #10b981 emerald, #34d399 mint, white text",
    "Sunset Orange & Red":  "#1a0800 dark bg, #f97316 orange, #ef4444 red, #fef3c7 text",
    "Clean White & Blue":   "#f8faff white bg, #1e3a5f navy, #3b82f6 blue, #dbeafe accents",
    "Warm Cream":           "#faf7f2 cream bg, #292524 dark, #dc6e2e terracotta, #f59e0b amber",
    "Black & Gold":         "#080608 black bg, #f59e0b gold, #fbbf24 bright gold, white text",
}

SYS = """You are a world-class infographic designer. Create Canva/Piktochart quality visual infographics.
Return ONLY complete HTML starting with <!DOCTYPE html>. No markdown, no fences.
All CSS in <style>. Import Google Fonts. Width 900px centered. MUST include SVG charts."""

def build_prompt(text, itype, title, theme):
    type_map = {
        "auto":       "Choose best layout. Mix stat circles, donut charts, key insight cards.",
        "summary":    "KEY POINTS: colored header, 5-8 numbered cards in 2-col grid with emoji icons, highlight stat.",
        "timeline":   "TIMELINE: bold header, vertical alternating events, year badges, connecting dots.",
        "stats":      "STATS DASHBOARD: hero numbers row, SVG donut charts, CSS bar charts, percentage rings.",
        "comparison": "COMPARISON: two-column VS layout, checkmark rows, VS badge divider, summary banner.",
        "process":    "PROCESS FLOW: numbered steps, arrow connectors, icon per step, color progression.",
        "report":     "FULL REPORT: hero header, 4 KPI cards, 2-3 content sections with charts, footer.",
    }
    t = f'Title: "{title}"' if title.strip() else "Auto-generate a compelling title."
    return f"""Create a stunning professional infographic.
TYPE: {type_map.get(itype, type_map['auto'])}
{t}
THEME: {theme}
REQUIREMENTS:
- 900px wide, margin:0 auto
- SVG donut rings (stroke-dasharray), CSS bar charts, stat circles
- Emoji icons throughout, fadeInUp CSS animations
- Cards with box-shadow, bold numbers 2.5rem+
- Google Fonts, professional spacing
- "Generated by InfographAI" footer
SVG DONUT: <svg width="130" height="130" viewBox="0 0 130 130">
  <circle cx="65" cy="65" r="54" fill="none" stroke="rgba(255,255,255,0.1)" stroke-width="14"/>
  <circle cx="65" cy="65" r="54" fill="none" stroke="#00bcd4" stroke-width="14"
    stroke-dasharray="237 339" stroke-dashoffset="-85" stroke-linecap="round"/>
  <text x="65" y="70" text-anchor="middle" font-size="22" font-weight="800" fill="white">70%</text>
</svg>
DOCUMENT: {text[:5000]}
Return ONLY complete HTML."""

# ── NAVBAR ──
st.markdown("""
<div class="navbar">
  <div class="nav-brand">
    <div class="nav-icon">🎨</div>
    <div class="nav-title">Infograph<span>AI</span></div>
  </div>
  <div class="nav-pills">
    <div class="nav-pill">PDF</div>
    <div class="nav-pill">DOCX</div>
    <div class="nav-pill">TEXT</div>
    <div class="nav-pill">URL</div>
    <div class="nav-pill">7 FORMATS</div>
    <div class="nav-pill">7 THEMES</div>
  </div>
  <div class="nav-status"><div class="pulse"></div>System Online</div>
</div>
""", unsafe_allow_html=True)

lcol, rcol = st.columns([1, 2.2], gap="large")

with lcol:
    st.markdown("""
    <div class="sec-header">
      <div class="sec-icon">📥</div>
      <div>
        <div class="sec-title">Document Input</div>
        <div class="sec-sub">Upload or paste your content</div>
      </div>
    </div>""", unsafe_allow_html=True)

    t1,t2,t3,t4 = st.tabs(["📝 Text","📄 PDF","📃 DOCX","🔗 URL"])
    with t1:
        txt = st.text_area("input_text", height=185,
            placeholder="Paste your document, report, article or any text here...",
            label_visibility="collapsed", key="itxt")
        if st.button("Load Text →", key="btxt"):
            if txt.strip(): st.session_state.doc_text=txt.strip(); st.success(f"✅ Loaded {len(txt):,} characters")
            else: st.warning("Please enter some text first.")
    with t2:
        pf = st.file_uploader("pdf_up", type=["pdf"], label_visibility="collapsed", key="ipdf")
        if st.button("Extract PDF →", key="bpdf"):
            if pf:
                try: st.session_state.doc_text=extract_pdf(pf.read()); st.success(f"✅ Extracted {len(st.session_state.doc_text):,} chars")
                except Exception as e: st.error(f"Failed: {e}")
            else: st.warning("Upload a PDF first.")
    with t3:
        df = st.file_uploader("docx_up", type=["docx"], label_visibility="collapsed", key="idocx")
        if st.button("Extract DOCX →", key="bdocx"):
            if df:
                try: st.session_state.doc_text=extract_docx(df.read()); st.success(f"✅ Extracted {len(st.session_state.doc_text):,} chars")
                except Exception as e: st.error(f"Failed: {e}")
            else: st.warning("Upload a DOCX first.")
    with t4:
        ui = st.text_input("url_input", placeholder="https://example.com/article...", label_visibility="collapsed", key="iurl")
        if st.button("Fetch URL →", key="burl"):
            if ui.startswith("http"):
                with st.spinner("Fetching page content..."):
                    try:
                        t = fetch_url(ui)
                        if len(t)<100: st.error("Not enough content found.")
                        else: st.session_state.doc_text=t[:6000]; st.success(f"✅ Fetched {len(st.session_state.doc_text):,} chars")
                    except Exception as e: st.error(f"Failed: {e}")
            else: st.warning("Enter a valid URL starting with https://")

    if st.session_state.doc_text:
        st.markdown(f'<div class="badge badge-green" style="margin-top:0.6rem">✓ &nbsp;{len(st.session_state.doc_text):,} chars loaded</div>', unsafe_allow_html=True)

    st.markdown('<div class="hr"></div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="sec-header">
      <div class="sec-icon">⚙️</div>
      <div>
        <div class="sec-title">Configuration</div>
        <div class="sec-sub">Choose your format and style</div>
      </div>
    </div>""", unsafe_allow_html=True)

    st.markdown('<span class="flabel">Infographic Format</span>', unsafe_allow_html=True)
    itype = st.selectbox("fmt", list(TYPES.keys()), format_func=lambda k: TYPES[k], label_visibility="collapsed", key="itype")

    st.markdown('<span class="flabel">Color Theme</span>', unsafe_allow_html=True)
    theme = st.selectbox("thm", list(THEMES.keys()), label_visibility="collapsed", key="itheme")

    st.markdown('<span class="flabel">Custom Title (optional)</span>', unsafe_allow_html=True)
    ctitle = st.text_input("ttl", placeholder="Leave blank — AI will auto-generate title...", label_visibility="collapsed", key="ictitle")

    st.markdown("<br>", unsafe_allow_html=True)
    gen = st.button("✨  Generate Infographic", use_container_width=True)

    if st.session_state.generated:
        st.markdown('<div class="hr"></div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="sec-header">
          <div class="sec-icon">⬇️</div>
          <div>
            <div class="sec-title">Export</div>
            <div class="sec-sub">Download your infographic</div>
          </div>
        </div>""", unsafe_allow_html=True)
        st.download_button("⬇  Download HTML File",
            data=st.session_state.html_out.encode(),
            file_name="infographic.html", mime="text/html")
        st.markdown("""
        <div class="export-hint">
          <strong>Save as PNG:</strong><br>
          Open HTML in Chrome →<br>
          Ctrl+P → Save as PDF<br>
          or take a screenshot
        </div>""", unsafe_allow_html=True)

with rcol:
    ready = st.session_state.generated and st.session_state.html_out
    badge = '<span class="badge badge-green">✓ Infographic Ready</span>' if ready else '<span class="badge badge-yellow">⏳ Awaiting Input</span>'
    st.markdown(f"""
    <div class="canvas-header">
      <div style="display:flex;align-items:center;gap:0.7rem">
        <span style="font-size:1.2rem">🖼</span>
        <span class="canvas-title">Output Canvas</span>
      </div>
      {badge}
    </div>
    <div class="canvas-body">""", unsafe_allow_html=True)

    if not ready:
        st.markdown("""
        <div class="empty-state">
          <div class="empty-grid"></div>
          <div class="empty-inner">
            <span class="empty-emoji">🎨</span>
            <div class="empty-title">Your infographic appears here</div>
            <div class="empty-desc">Load a document, choose your format and theme,<br>then hit Generate.</div>
            <div class="steps">
              <div class="step"><div class="step-n">STEP 1</div><div class="step-t">Load Doc</div></div>
              <div class="step"><div class="step-n">STEP 2</div><div class="step-t">Configure</div></div>
              <div class="step"><div class="step-n">STEP 3</div><div class="step-t">Generate ✨</div></div>
            </div>
          </div>
        </div>""", unsafe_allow_html=True)
    else:
        components.html(st.session_state.html_out, height=980, scrolling=True)

    st.markdown('</div>', unsafe_allow_html=True)

if gen:
    if not st.session_state.doc_text.strip():
        st.error("⚠️ Please load a document first.")
    else:
        theme_desc = THEMES.get(theme, list(THEMES.values())[0])
        prompt = build_prompt(st.session_state.doc_text, itype, ctitle, theme_desc)
        with st.spinner("✨ Generating your infographic with charts and visuals..."):
            try:
                raw = call_groq(SYS, prompt, max_tokens=4000, temp=0.38)
                raw = re.sub(r'^```html\s*','',raw.strip())
                raw = re.sub(r'^```\s*','',raw.strip())
                raw = re.sub(r'```\s*$','',raw.strip())
                if not raw.strip().startswith('<!'):
                    for tag in ['<!DOCTYPE','<html']:
                        idx = raw.find(tag)
                        if idx != -1: raw = raw[idx:]; break
                st.session_state.html_out = raw
                st.session_state.generated = True
                st.rerun()
            except Exception as e:
                st.error(f"Generation failed: {e}")
