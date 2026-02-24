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
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

html, body, [class*="css"] {
  font-family: 'Plus Jakarta Sans', sans-serif !important;
  background: #0c0e14 !important;
  color: #e8eaf0 !important;
  font-size: 15px !important;
}
.stApp { background: #0c0e14 !important; }

.main .block-container {
  padding: 2.5rem 4rem 4rem 4rem !important;
  max-width: 1440px !important;
  margin: 0 auto !important;
}

#MainMenu, footer, header, [data-testid="stToolbar"] { display: none !important; }

/* ── NAVBAR ── */
.navbar {
  display: flex; align-items: center; justify-content: space-between;
  padding: 1.2rem 2rem;
  background: #13151e;
  border: 1px solid #1e2130;
  border-radius: 14px;
  margin-bottom: 2.5rem;
}
.nav-brand { display: flex; align-items: center; gap: 0.8rem; }
.nav-icon {
  width: 38px; height: 38px; border-radius: 10px;
  background: linear-gradient(135deg, #6366f1, #a855f7);
  display: flex; align-items: center; justify-content: center;
  font-size: 1.1rem;
}
.nav-title {
  font-size: 1.25rem; font-weight: 800; color: #ffffff;
  letter-spacing: -0.02em;
}
.nav-title span { color: #818cf8; }
.nav-pills { display: flex; gap: 0.5rem; }
.nav-pill {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.72rem; font-weight: 500;
  padding: 0.35rem 0.9rem;
  border-radius: 6px;
  background: #1e2130; color: #94a3b8;
  border: 1px solid #2a2e40;
  letter-spacing: 0.04em;
}
.nav-pill.active {
  background: rgba(99,102,241,0.15);
  color: #818cf8; border-color: rgba(99,102,241,0.4);
}
.nav-status {
  display: flex; align-items: center; gap: 0.5rem;
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.75rem; color: #4ade80;
  background: rgba(74,222,128,0.08);
  border: 1px solid rgba(74,222,128,0.2);
  padding: 0.4rem 0.9rem; border-radius: 20px;
}
.pulse { width: 7px; height: 7px; border-radius: 50%; background: #4ade80; animation: pulse 1.5s ease-in-out infinite; }
@keyframes pulse { 0%,100%{opacity:1;transform:scale(1)} 50%{opacity:0.4;transform:scale(0.8)} }

/* ── CARDS ── */
.card {
  background: #13151e;
  border: 1px solid #1e2130;
  border-radius: 14px;
  padding: 1.5rem;
  margin-bottom: 1.2rem;
}
.card-header {
  display: flex; align-items: center; gap: 0.7rem;
  margin-bottom: 1.2rem;
}
.card-icon {
  width: 30px; height: 30px; border-radius: 8px;
  background: rgba(99,102,241,0.15);
  display: flex; align-items: center; justify-content: center;
  font-size: 0.9rem; flex-shrink: 0;
}
.card-title {
  font-size: 0.88rem; font-weight: 700;
  color: #e2e8f0; letter-spacing: 0.01em;
}
.card-sub {
  font-size: 0.72rem; color: #64748b;
  font-weight: 400; margin-top: 0.1rem;
}

/* ── SECTION LABELS ── */
.field-label {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.72rem; font-weight: 500;
  color: #64748b; letter-spacing: 0.08em;
  text-transform: uppercase;
  margin-bottom: 0.45rem; margin-top: 1rem;
}
.field-label:first-child { margin-top: 0; }

/* ── TABS ── */
div[data-baseweb="tab-list"] {
  background: #1a1d28 !important;
  border: 1px solid #252836 !important;
  border-radius: 10px !important;
  padding: 4px !important; gap: 3px !important;
  margin-bottom: 1rem;
}
div[data-baseweb="tab"] {
  background: transparent !important; border-radius: 7px !important;
  color: #64748b !important;
  font-family: 'JetBrains Mono', monospace !important;
  font-size: 0.72rem !important; font-weight: 500 !important;
  padding: 0.42rem 0.9rem !important; letter-spacing: 0.05em;
  transition: all 0.15s !important;
}
div[data-baseweb="tab"]:hover { color: #94a3b8 !important; }
div[aria-selected="true"] {
  background: #252836 !important; color: #c7d2fe !important;
}

/* ── TEXTAREA ── */
div[data-testid="stTextArea"] label { display: none !important; }
div[data-testid="stTextArea"] textarea {
  background: #1a1d28 !important; border: 1px solid #252836 !important;
  border-radius: 10px !important; color: #e2e8f0 !important;
  font-family: 'JetBrains Mono', monospace !important;
  font-size: 0.85rem !important; line-height: 1.8 !important;
  padding: 0.9rem 1rem !important; resize: none !important;
  transition: border-color 0.2s !important;
}
div[data-testid="stTextArea"] textarea:focus {
  border-color: #6366f1 !important;
  box-shadow: 0 0 0 3px rgba(99,102,241,0.1) !important;
  outline: none !important;
}
div[data-testid="stTextArea"] textarea::placeholder {
  color: #334155 !important;
}

/* ── TEXT INPUT ── */
div[data-testid="stTextInput"] label { display: none !important; }
.stTextInput input {
  background: #1a1d28 !important; border: 1px solid #252836 !important;
  border-radius: 10px !important; color: #e2e8f0 !important;
  font-family: 'JetBrains Mono', monospace !important;
  font-size: 0.82rem !important; padding: 0.65rem 1rem !important;
  transition: border-color 0.2s !important;
}
.stTextInput input:focus { border-color: #6366f1 !important; box-shadow: 0 0 0 3px rgba(99,102,241,0.1) !important; }
.stTextInput input::placeholder { color: #334155 !important; }

/* ── SELECT ── */
div[data-testid="stSelectbox"] label { display: none !important; }
div[data-baseweb="select"] > div {
  background: #1a1d28 !important; border: 1px solid #252836 !important;
  border-radius: 10px !important; color: #e2e8f0 !important;
  font-family: 'Plus Jakarta Sans', sans-serif !important;
  font-size: 0.85rem !important; font-weight: 500 !important;
  min-height: 44px !important;
}
div[data-baseweb="select"] > div:focus-within { border-color: #6366f1 !important; }
[data-baseweb="popover"] { background: #1a1d28 !important; border: 1px solid #252836 !important; border-radius: 10px !important; }
[role="option"] { font-size: 0.85rem !important; color: #e2e8f0 !important; padding: 0.6rem 1rem !important; }
[role="option"]:hover { background: rgba(99,102,241,0.1) !important; }

/* ── FILE UPLOADER ── */
div[data-testid="stFileUploader"] label { display: none !important; }
[data-testid="stFileUploader"] section {
  background: #1a1d28 !important; border: 2px dashed #252836 !important;
  border-radius: 10px !important; padding: 1.5rem !important;
  transition: border-color 0.2s !important;
}
[data-testid="stFileUploader"] section:hover { border-color: #6366f1 !important; }
[data-testid="stFileUploader"] span {
  font-size: 0.82rem !important; color: #64748b !important;
  font-family: 'Plus Jakarta Sans', sans-serif !important;
}
[data-testid="stFileUploader"] button {
  background: rgba(99,102,241,0.15) !important;
  color: #818cf8 !important; border-radius: 8px !important;
  font-size: 0.8rem !important; border: 1px solid rgba(99,102,241,0.3) !important;
}

/* ── BUTTONS ── */
.stButton > button {
  background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
  border: none !important; border-radius: 10px !important;
  color: #ffffff !important;
  font-family: 'Plus Jakarta Sans', sans-serif !important;
  font-weight: 700 !important; font-size: 0.88rem !important;
  letter-spacing: 0.02em !important; padding: 0.65rem 1.4rem !important;
  width: 100% !important; transition: all 0.2s !important;
  box-shadow: 0 4px 14px rgba(99,102,241,0.3) !important;
  margin-top: 0.3rem !important;
}
.stButton > button:hover {
  transform: translateY(-2px) !important;
  box-shadow: 0 8px 24px rgba(99,102,241,0.45) !important;
}
.stButton > button:active { transform: translateY(0) !important; }

.stDownloadButton > button {
  background: rgba(74,222,128,0.1) !important;
  border: 1px solid rgba(74,222,128,0.35) !important;
  border-radius: 10px !important; color: #4ade80 !important;
  font-family: 'Plus Jakarta Sans', sans-serif !important;
  font-weight: 600 !important; font-size: 0.82rem !important;
  padding: 0.5rem 1.2rem !important; width: auto !important;
  box-shadow: none !important; margin-top: 0 !important;
}
.stDownloadButton > button:hover { background: rgba(74,222,128,0.18) !important; transform: none !important; }

/* ── STATUS BADGES ── */
.badge {
  display: inline-flex; align-items: center; gap: 0.4rem;
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.72rem; font-weight: 500;
  padding: 0.28rem 0.75rem; border-radius: 20px;
  letter-spacing: 0.05em;
}
.badge-green { background: rgba(74,222,128,0.1); color: #4ade80; border: 1px solid rgba(74,222,128,0.25); }
.badge-blue { background: rgba(99,102,241,0.12); color: #818cf8; border: 1px solid rgba(99,102,241,0.25); }
.badge-yellow { background: rgba(251,191,36,0.12); color: #fbbf24; border: 1px solid rgba(251,191,36,0.25); }

/* ── CANVAS ── */
.canvas-header {
  display: flex; align-items: center; justify-content: space-between;
  padding: 1rem 1.5rem;
  background: #13151e; border: 1px solid #1e2130;
  border-radius: 14px 14px 0 0;
}
.canvas-title { font-size: 0.88rem; font-weight: 700; color: #e2e8f0; }
.canvas-body {
  border: 1px solid #1e2130; border-top: none;
  border-radius: 0 0 14px 14px; overflow: hidden;
}

/* ── EMPTY STATE ── */
.empty-state {
  min-height: 580px; background: #0f1118;
  display: flex; flex-direction: column;
  align-items: center; justify-content: center; gap: 1rem;
  position: relative;
}
.empty-grid {
  position: absolute; inset: 0;
  background-image:
    linear-gradient(rgba(99,102,241,0.04) 1px, transparent 1px),
    linear-gradient(90deg, rgba(99,102,241,0.04) 1px, transparent 1px);
  background-size: 36px 36px;
  pointer-events: none;
}
.empty-content { position: relative; z-index: 1; text-align: center; padding: 2rem; }
.empty-emoji { font-size: 3.5rem; display: block; margin-bottom: 1.2rem; animation: float 3s ease-in-out infinite; }
@keyframes float { 0%,100%{transform:translateY(0)} 50%{transform:translateY(-8px)} }
.empty-title { font-size: 1.3rem; font-weight: 800; color: #1e2436; margin-bottom: 0.5rem; }
.empty-desc { font-size: 0.85rem; color: #1a1f2e; font-weight: 400; line-height: 1.6; }
.steps-row {
  display: flex; gap: 1rem; margin-top: 2rem;
}
.step-item {
  background: #13151e; border: 1px solid #1e2130;
  border-radius: 10px; padding: 0.9rem 1.2rem;
  text-align: center; min-width: 120px;
}
.step-num { font-family: 'JetBrains Mono', monospace; font-size: 0.65rem; color: #6366f1; font-weight: 600; letter-spacing: 0.1em; margin-bottom: 0.3rem; }
.step-txt { font-size: 0.78rem; color: #1e2436; font-weight: 600; }

/* ── ALERTS ── */
.stSuccess > div { background: rgba(74,222,128,0.08) !important; border: 1px solid rgba(74,222,128,0.2) !important; border-radius: 10px !important; color: #4ade80 !important; font-size: 0.82rem !important; }
.stError > div { background: rgba(248,113,113,0.08) !important; border: 1px solid rgba(248,113,113,0.2) !important; border-radius: 10px !important; color: #f87171 !important; font-size: 0.82rem !important; }
.stWarning > div { background: rgba(251,191,36,0.08) !important; border: 1px solid rgba(251,191,36,0.2) !important; border-radius: 10px !important; color: #fbbf24 !important; font-size: 0.82rem !important; }
div[data-testid="stSpinner"] p { color: #818cf8 !important; font-size: 0.85rem !important; }

/* DIVIDER */
.divider { height: 1px; background: #1e2130; margin: 1.2rem 0; }

::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: #0c0e14; }
::-webkit-scrollbar-thumb { background: #1e2130; border-radius: 4px; }
::-webkit-scrollbar-thumb:hover { background: #6366f1; }
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
    "auto":"🤖  AI Decides Best Format",
    "summary":"📋  Key Points & Insights",
    "timeline":"⏱  Timeline & Events",
    "stats":"📊  Stats & Data Visualization",
    "comparison":"⚖  Comparison & Analysis",
    "process":"🔄  Process Flow & Steps",
    "report":"📑  Full Report Dashboard",
}
THEMES = {
    "Teal & Cyan (Professional)": "#0a2535 dark bg, #00bcd4 teal, #26c6da cyan, #80deea light cyan, white text — clean professional style",
    "Dark Navy & Indigo": "#0a0f1e dark bg, #6366f1 indigo, #8b5cf6 purple, #e0e7ff light, modern tech style",
    "Emerald & Green": "#071c12 dark bg, #10b981 emerald, #34d399 mint, #d1fae5 light, fresh data style",
    "Sunset Orange & Red": "#1a0800 dark bg, #f97316 orange, #ef4444 red, #fef3c7 warm light, energetic style",
    "White & Blue (Light)": "#f8faff white bg, #1e3a5f dark navy text, #3b82f6 blue, #dbeafe light blue, minimal clean",
    "Warm Cream & Terracotta": "#faf7f2 cream bg, #292524 dark text, #dc6e2e terracotta, #f59e0b amber, editorial warm",
    "Black & Gold (Luxury)": "#080608 black bg, #f59e0b gold, #fbbf24 bright gold, #fef3c7 pale, premium luxury style",
}

SYS = """You are a world-class infographic designer. Create stunning visual infographics like those from Canva, Piktochart, or Venngage.
Return ONLY complete valid HTML starting with <!DOCTYPE html>. No markdown, no code fences, no explanation.
All CSS in <style> tag. Import Google Fonts. Width exactly 900px centered. Use any height needed.
MUST include real SVG charts: donut rings, bar charts, stat circles, line charts."""

def build_prompt(text, itype, title, theme):
    type_map = {
        "auto": "Analyze and pick the BEST layout. Mix stat circles, donut charts, key insight cards, and visual elements.",
        "summary": "KEY POINTS layout: colored header, 5-8 numbered cards in 2-col grid with emoji icons, central highlight stat, visual accents.",
        "timeline": "TIMELINE: bold header, vertical alternating timeline, year badges, connecting line with dots, color-coded phases.",
        "stats": "STATS DASHBOARD: hero numbers row, SVG donut charts, CSS bar charts, percentage rings, SVG line chart.",
        "comparison": "COMPARISON: two-column VS layout, colored headers, feature rows with checkmarks, VS badge divider, summary banner.",
        "process": "PROCESS FLOW: numbered steps 1→N, arrow connectors, icon per step, color progression, notes sidebar.",
        "report": "FULL REPORT: hero header, 4 KPI metric cards top row, 2-3 content sections with charts, timeline, callout box, footer.",
    }
    t = f'Title: "{title}"' if title.strip() else "Auto-generate a compelling specific title."
    return f"""Create a stunning professional infographic (like Canva/Piktochart quality).

TYPE: {type_map.get(itype, type_map['auto'])}
{t}
THEME: {theme}

MUST HAVE:
- 900px width, margin:0 auto
- At least 2 SVG charts (donut rings using stroke-dasharray, bar charts, stat circles)
- Emoji icons used as visual accents throughout
- CSS fadeInUp animations with staggered delays
- Cards with box-shadow: 0 4px 20px rgba(0,0,0,0.2)
- Bold number typography (2.5rem+ for stats)
- Color-coded sections using theme colors
- Google Fonts (2 fonts: display + body)
- Professional layout with proper spacing
- "Generated by InfographAI" footer

SVG DONUT CHART PATTERN:
<svg width="130" height="130" viewBox="0 0 130 130">
  <circle cx="65" cy="65" r="54" fill="none" stroke="rgba(255,255,255,0.1)" stroke-width="14"/>
  <circle cx="65" cy="65" r="54" fill="none" stroke="#00bcd4" stroke-width="14"
    stroke-dasharray="237 339" stroke-dashoffset="-85" stroke-linecap="round"
    style="animation: spin 0.8s ease-out"/>
  <text x="65" y="70" text-anchor="middle" font-size="22" font-weight="800" fill="white">70%</text>
</svg>

DOCUMENT:
{text[:5000]}

Return ONLY the complete HTML document."""

# ── NAVBAR ──
st.markdown("""
<div class="navbar">
  <div class="nav-brand">
    <div class="nav-icon">🎨</div>
    <div>
      <div class="nav-title">Infograph<span>AI</span></div>
    </div>
  </div>
  <div class="nav-pills">
    <div class="nav-pill active">PDF</div>
    <div class="nav-pill active">DOCX</div>
    <div class="nav-pill active">TEXT</div>
    <div class="nav-pill active">URL</div>
    <div class="nav-pill">7 FORMATS</div>
    <div class="nav-pill">7 THEMES</div>
  </div>
  <div class="nav-status">
    <div class="pulse"></div>
    System Online
  </div>
</div>
""", unsafe_allow_html=True)

# ── LAYOUT ──
lcol, rcol = st.columns([1, 2.2], gap="large")

with lcol:
    # INPUT CARD
    st.markdown("""
    <div class="card-header" style="margin-bottom:0.8rem">
      <div class="card-icon">📥</div>
      <div>
        <div class="card-title">Document Input</div>
        <div class="card-sub">Upload or paste your content</div>
      </div>
    </div>""", unsafe_allow_html=True)

    t1,t2,t3,t4 = st.tabs(["📝 Text","📄 PDF","📃 DOCX","🔗 URL"])

    with t1:
        txt = st.text_area("", height=180,
            placeholder="Paste your document, report, article, or any text here...",
            label_visibility="collapsed", key="itxt")
        if st.button("Load Text →", key="btxt"):
            if txt.strip():
                st.session_state.doc_text = txt.strip()
                st.success(f"✅ Loaded — {len(txt):,} characters")
            else: st.warning("Please enter some text first.")

    with t2:
        pf = st.file_uploader("", type=["pdf"], label_visibility="collapsed", key="ipdf")
        if st.button("Extract PDF →", key="bpdf"):
            if pf:
                try:
                    st.session_state.doc_text = extract_pdf(pf.read())
                    st.success(f"✅ Extracted — {len(st.session_state.doc_text):,} chars")
                except Exception as e: st.error(f"Failed: {e}")
            else: st.warning("Upload a PDF first.")

    with t3:
        df = st.file_uploader("", type=["docx"], label_visibility="collapsed", key="idocx")
        if st.button("Extract DOCX →", key="bdocx"):
            if df:
                try:
                    st.session_state.doc_text = extract_docx(df.read())
                    st.success(f"✅ Extracted — {len(st.session_state.doc_text):,} chars")
                except Exception as e: st.error(f"Failed: {e}")
            else: st.warning("Upload a DOCX first.")

    with t4:
        ui = st.text_input("", placeholder="https://example.com/article...", label_visibility="collapsed", key="iurl")
        if st.button("Fetch URL →", key="burl"):
            if ui.startswith("http"):
                with st.spinner("Fetching page content..."):
                    try:
                        t = fetch_url(ui)
                        if len(t) < 100: st.error("Not enough content found.")
                        else:
                            st.session_state.doc_text = t[:6000]
                            st.success(f"✅ Fetched — {len(st.session_state.doc_text):,} chars")
                    except Exception as e: st.error(f"Failed: {e}")
            else: st.warning("Enter a valid URL.")

    if st.session_state.doc_text:
        st.markdown(f'<div class="badge badge-green" style="margin-top:0.6rem">✓ &nbsp;{len(st.session_state.doc_text):,} chars ready</div>', unsafe_allow_html=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # CONFIG
    st.markdown("""
    <div class="card-header" style="margin-bottom:0.8rem">
      <div class="card-icon">⚙️</div>
      <div>
        <div class="card-title">Configuration</div>
        <div class="card-sub">Choose format and style</div>
      </div>
    </div>""", unsafe_allow_html=True)

    st.markdown('<div class="field-label">Infographic Format</div>', unsafe_allow_html=True)
    itype = st.selectbox("", list(TYPES.keys()), format_func=lambda k: TYPES[k], label_visibility="collapsed", key="itype")

    st.markdown('<div class="field-label">Color Theme</div>', unsafe_allow_html=True)
    theme = st.selectbox("", list(THEMES.keys()), label_visibility="collapsed", key="itheme")

    st.markdown('<div class="field-label">Custom Title (optional)</div>', unsafe_allow_html=True)
    ctitle = st.text_input("", placeholder="Leave blank — AI will auto-generate...", label_visibility="collapsed", key="ictitle")

    st.markdown("<br>", unsafe_allow_html=True)
    gen = st.button("✨  Generate Infographic", use_container_width=True)

    if st.session_state.generated:
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="card-header" style="margin-bottom:0.8rem">
          <div class="card-icon">⬇️</div>
          <div>
            <div class="card-title">Export</div>
            <div class="card-sub">Download your infographic</div>
          </div>
        </div>""", unsafe_allow_html=True)
        st.download_button(
            "⬇  Download HTML File",
            data=st.session_state.html_out.encode(),
            file_name="infographic.html", mime="text/html"
        )
        st.markdown("""
        <div style="font-size:0.76rem;color:#475569;line-height:1.8;margin-top:0.8rem">
          <strong style="color:#64748b">Save as PNG:</strong><br>
          Open HTML in Chrome →<br>
          Right-click → Print →<br>
          Save as PDF / Screenshot
        </div>""", unsafe_allow_html=True)

with rcol:
    ready = st.session_state.generated and st.session_state.html_out
    badge = '<span class="badge badge-green">✓ Infographic Ready</span>' if ready else '<span class="badge badge-yellow">⏳ Awaiting Input</span>'

    st.markdown(f"""
    <div class="canvas-header">
      <div style="display:flex;align-items:center;gap:0.6rem">
        <span style="font-size:1rem">🖼</span>
        <div class="canvas-title">Output Canvas</div>
      </div>
      {badge}
    </div>
    <div class="canvas-body">""", unsafe_allow_html=True)

    if not ready:
        st.markdown("""
        <div class="empty-state">
          <div class="empty-grid"></div>
          <div class="empty-content">
            <span class="empty-emoji">🎨</span>
            <div class="empty-title">Your infographic appears here</div>
            <div class="empty-desc">Load a document, choose a format and theme,<br>then click Generate.</div>
            <div class="steps-row">
              <div class="step-item"><div class="step-num">STEP 1</div><div class="step-txt">Load Document</div></div>
              <div class="step-item"><div class="step-num">STEP 2</div><div class="step-txt">Pick Format</div></div>
              <div class="step-item"><div class="step-num">STEP 3</div><div class="step-txt">Generate ✨</div></div>
            </div>
          </div>
        </div>""", unsafe_allow_html=True)
    else:
        components.html(st.session_state.html_out, height=980, scrolling=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ── GENERATE ──
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
