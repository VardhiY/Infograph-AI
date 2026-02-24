import streamlit as st
from groq import Groq
import os, io, re, json, urllib.request, base64

st.set_page_config(page_title="InfographAI", page_icon="🎨", layout="wide")

# ── API KEY ──
api_key = os.environ.get("GROQ_API_KEY")
if not api_key:
    try: api_key = st.secrets["GROQ_API_KEY"]
    except: pass
if not api_key:
    st.error("⚠️ GROQ_API_KEY missing. Add it in Render → Environment Variables.")
    st.stop()

client = Groq(api_key=api_key)

# ── GLOBAL STYLES ──
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=Epilogue:wght@300;400;500;600&family=DM+Mono:wght@400;500&display=swap');

html, body, [class*="css"] { font-family: 'Epilogue', sans-serif !important; }
.stApp { background: #07070f; color: #e8e8f0; }
.main .block-container { padding: 0 !important; max-width: 100% !important; }
#MainMenu, footer, header { display: none !important; }

/* TOP ACCENT */
.stApp::after {
  content: '';
  position: fixed; top: 0; left: 0; right: 0; height: 2px;
  background: linear-gradient(90deg, #6366f1, #a855f7, #ec4899, #f97316, #6366f1);
  background-size: 300%;
  animation: shimmer 3s linear infinite;
  z-index: 9999;
}
@keyframes shimmer { 0%{background-position:0%} 100%{background-position:300%} }

/* HEADER */
.app-header {
  padding: 3rem 4rem 2rem;
  border-bottom: 1px solid #13131f;
  display: flex; align-items: flex-end; justify-content: space-between;
}
.app-title {
  font-family: 'Syne', sans-serif;
  font-size: 2.6rem; font-weight: 800;
  background: linear-gradient(135deg, #fff 20%, #a855f7 60%, #6366f1);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
  line-height: 1;
}
.app-sub {
  font-family: 'DM Mono', monospace;
  font-size: 0.68rem; color: #333; letter-spacing: 0.15em;
  text-transform: uppercase; margin-top: 0.5rem;
}
.app-badge {
  font-family: 'DM Mono', monospace;
  font-size: 0.62rem; padding: 0.3rem 0.8rem;
  border: 1px solid #1f1f35; color: #555;
  letter-spacing: 0.1em; text-transform: uppercase;
}

/* LAYOUT */
.app-body { display: flex; min-height: calc(100vh - 120px); }
.left-panel {
  width: 380px; min-width: 380px;
  border-right: 1px solid #13131f;
  padding: 2rem;
  overflow-y: auto;
  background: #06060e;
}
.right-panel {
  flex: 1; padding: 2rem;
  overflow-y: auto;
}

/* PANEL LABELS */
.panel-label {
  font-family: 'DM Mono', monospace;
  font-size: 0.62rem; color: #6366f1;
  letter-spacing: 0.18em; text-transform: uppercase;
  margin-bottom: 0.8rem; margin-top: 1.6rem;
  display: flex; align-items: center; gap: 0.6rem;
}
.panel-label:first-child { margin-top: 0; }
.panel-label::after { content: ''; flex: 1; height: 1px; background: #13131f; }

/* INPUTS */
div[data-testid="stTextArea"] textarea {
  background: #0d0d1a !important; border: 1px solid #1a1a2e !important;
  border-radius: 8px !important; color: #e8e8f0 !important;
  font-family: 'Epilogue', sans-serif !important;
  font-size: 0.85rem !important; line-height: 1.7 !important;
  padding: 0.8rem !important;
}
div[data-testid="stTextArea"] textarea:focus {
  border-color: #6366f1 !important; box-shadow: 0 0 0 2px rgba(99,102,241,0.12) !important;
}
div[data-testid="stTextArea"] textarea::placeholder { color: #2a2a40 !important; }

.stTextInput input {
  background: #0d0d1a !important; border: 1px solid #1a1a2e !important;
  border-radius: 8px !important; color: #e8e8f0 !important;
  font-family: 'DM Mono', monospace !important; font-size: 0.8rem !important;
  padding: 0.6rem 0.9rem !important;
}
.stTextInput input:focus { border-color: #6366f1 !important; box-shadow: none !important; }
.stTextInput input::placeholder { color: #2a2a40 !important; }

/* TABS */
div[data-baseweb="tab-list"] {
  background: #0d0d1a !important; border-radius: 8px !important;
  padding: 3px !important; border: 1px solid #1a1a2e !important;
  gap: 2px !important;
}
div[data-baseweb="tab"] {
  border-radius: 6px !important; color: #333 !important;
  font-family: 'DM Mono', monospace !important;
  font-size: 0.68rem !important; padding: 0.3rem 0.7rem !important;
  letter-spacing: 0.08em;
}
div[aria-selected="true"] {
  background: #6366f1 !important; color: #fff !important;
}

/* BUTTONS */
.stButton > button {
  background: linear-gradient(135deg, #6366f1, #a855f7) !important;
  border: none !important; border-radius: 8px !important;
  color: #fff !important; font-family: 'Syne', sans-serif !important;
  font-weight: 800 !important; font-size: 0.9rem !important;
  letter-spacing: 0.08em; padding: 0.7rem 1.5rem !important;
  width: 100% !important; text-transform: uppercase;
  transition: all 0.2s !important;
}
.stButton > button:hover {
  box-shadow: 0 8px 24px rgba(99,102,241,0.4) !important;
  transform: translateY(-1px) !important;
}
.stDownloadButton > button {
  background: #0d0d1a !important; border: 1px solid #1a1a2e !important;
  border-radius: 8px !important; color: #a855f7 !important;
  font-family: 'DM Mono', monospace !important; font-size: 0.72rem !important;
  padding: 0.45rem 1rem !important; width: auto !important;
  text-transform: none !important;
}

/* SELECT BOX */
div[data-baseweb="select"] > div {
  background: #0d0d1a !important; border: 1px solid #1a1a2e !important;
  border-radius: 8px !important; color: #e8e8f0 !important;
  font-size: 0.85rem !important;
}

/* FILE UPLOADER */
[data-testid="stFileUploader"] section {
  background: #0d0d1a !important; border: 1px dashed #1a1a2e !important;
  border-radius: 8px !important;
}
[data-testid="stFileUploader"] section:hover { border-color: #6366f1 !important; }

/* STATUS CHIP */
.status-chip {
  display: inline-flex; align-items: center; gap: 0.4rem;
  font-family: 'DM Mono', monospace; font-size: 0.62rem;
  padding: 0.25rem 0.7rem; border-radius: 999px;
  letter-spacing: 0.08em;
}
.status-ok { background: rgba(52,211,153,0.1); border: 1px solid rgba(52,211,153,0.3); color: #34d399; }
.status-info { background: rgba(99,102,241,0.1); border: 1px solid rgba(99,102,241,0.3); color: #818cf8; }

/* INFOGRAPHIC TYPES */
.type-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 0.5rem; margin: 0.5rem 0; }
.type-card {
  background: #0d0d1a; border: 1px solid #1a1a2e;
  border-radius: 8px; padding: 0.7rem;
  font-size: 0.78rem; color: #555; cursor: pointer;
  transition: all 0.15s; text-align: center;
}
.type-card:hover { border-color: #6366f1; color: #818cf8; }
.type-card.selected { border-color: #6366f1; background: rgba(99,102,241,0.08); color: #818cf8; }
.type-icon { font-size: 1.2rem; display: block; margin-bottom: 0.2rem; }

/* OUTPUT AREA */
.output-placeholder {
  height: 400px; display: flex; flex-direction: column;
  align-items: center; justify-content: center; gap: 1rem;
  border: 1px dashed #13131f; border-radius: 12px;
}
.placeholder-title {
  font-family: 'Syne', sans-serif; font-size: 1.8rem;
  font-weight: 800; color: #1a1a2e; text-align: center;
}
.placeholder-sub {
  font-family: 'DM Mono', monospace; font-size: 0.65rem;
  color: #1a1a2e; letter-spacing: 0.15em; text-transform: uppercase;
}

/* INFOGRAPHIC FRAME */
.infographic-frame {
  background: #fff; border-radius: 12px;
  overflow: hidden; box-shadow: 0 0 60px rgba(99,102,241,0.15);
}

::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: #07070f; }
::-webkit-scrollbar-thumb { background: #1a1a2e; border-radius: 4px; }
</style>
""", unsafe_allow_html=True)

# ── SESSION STATE ──
for k, v in [("doc_text",""),("infographic_html",""),("infographic_type","auto"),("generated",False)]:
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
    txt = re.sub(r'<[^>]+>',' ',txt)
    return re.sub(r'\s+',' ',txt).strip()

def call_groq(system, user, max_tokens=3000, temp=0.3):
    r = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role":"system","content":system},{"role":"user","content":user}],
        temperature=temp, max_tokens=max_tokens
    )
    return r.choices[0].message.content.strip()

# ── INFOGRAPHIC GENERATOR ──
INFOGRAPHIC_TYPES = {
    "auto":      ("🤖", "AI Decides"),
    "summary":   ("📋", "Key Points"),
    "timeline":  ("⏱️", "Timeline"),
    "stats":     ("📊", "Stats & Data"),
    "comparison":("⚖️", "Comparison"),
    "process":   ("🔄", "Process Flow"),
    "report":    ("📑", "Full Report"),
}

SYSTEM_PROMPT = """You are an expert infographic designer and data visualizer. 
Your job is to analyze documents and generate stunning, complete, self-contained HTML infographics.
You must return ONLY valid HTML — no markdown, no explanation, no code fences.
The HTML must be fully self-contained with all CSS inline or in a <style> tag.
Use Google Fonts. Make it visually stunning, modern, and professional.
The infographic should be 900px wide, any height needed.
Use vibrant colors, clean typography, and creative layouts."""

def build_prompt(doc_text, inf_type, custom_title=""):
    type_instructions = {
        "auto": "Analyze the document and choose the BEST infographic format (timeline, stats cards, process flow, comparison, or key points summary). Use multiple visual elements.",
        "summary": "Create a KEY POINTS infographic with numbered cards, icons (use emoji), and a clean summary layout. Extract 5-8 main insights.",
        "timeline": "Create a TIMELINE infographic. Extract chronological events, dates, or steps. Use a vertical or horizontal timeline design.",
        "stats": "Create a STATS & DATA infographic. Extract numbers, percentages, metrics. Use large number displays, progress bars, and data visualization elements.",
        "comparison": "Create a COMPARISON infographic (vs layout / pros-cons / before-after). Extract two or more things being compared.",
        "process": "Create a PROCESS FLOW infographic. Extract steps, stages, or procedures. Use numbered steps, arrows, and flow elements.",
        "report": "Create a COMPREHENSIVE REPORT infographic. Include a title section, key stats, main points, timeline if applicable, and a summary. Multi-section layout.",
    }

    title_note = f'Use "{custom_title}" as the infographic title.' if custom_title else "Generate an appropriate title from the document content."

    return f"""Create a stunning, professional infographic from this document.

INFOGRAPHIC TYPE: {type_instructions.get(inf_type, type_instructions['auto'])}

TITLE: {title_note}

DESIGN REQUIREMENTS:
- Width: exactly 900px, centered
- Use this color palette: deep dark background (#0f0f1f) with vibrant accents (#6366f1 indigo, #a855f7 purple, #ec4899 pink, #f97316 orange, #34d399 green)
- Font: Import and use 'Syne' (700,800) for headings and 'Epilogue' (300,400,500) for body from Google Fonts
- Include: decorative geometric shapes, gradient backgrounds, glassmorphism cards
- Make it visually rich — NOT a plain list
- Use emoji as icons where appropriate
- Include a subtle footer with "Generated by InfographAI"
- Animate elements with CSS keyframes (fade in, slide up)
- Make cards have subtle borders with rgba colors
- Use CSS Grid and Flexbox for layout

DOCUMENT CONTENT:
{doc_text[:5000]}

Return ONLY the complete HTML document starting with <!DOCTYPE html>"""

def generate_infographic(doc_text, inf_type, custom_title=""):
    prompt = build_prompt(doc_text, inf_type, custom_title)
    raw = call_groq(SYSTEM_PROMPT, prompt, max_tokens=4000, temp=0.4)
    # Clean up if model adds markdown
    raw = re.sub(r'^```html\s*','', raw.strip())
    raw = re.sub(r'```$','', raw.strip())
    return raw

# ── HEADER ──
st.markdown("""
<div class="app-header">
  <div>
    <div class="app-title">InfographAI</div>
    <div class="app-sub">Document → Stunning Infographic · Powered by Groq LLaMA</div>
  </div>
  <div class="app-badge">v1.0 · Beta</div>
</div>
""", unsafe_allow_html=True)

# ── MAIN LAYOUT ──
col_left, col_right = st.columns([1.1, 2], gap="large")

with col_left:
    # ── INPUT ──
    st.markdown('<div class="panel-label">01 · Document Input</div>', unsafe_allow_html=True)
    t1, t2, t3, t4 = st.tabs(["📝 Text", "📄 PDF", "📃 DOCX", "🔗 URL"])

    with t1:
        txt = st.text_area("", height=180, placeholder="Paste your document, report, article, or any text here...", label_visibility="collapsed", key="paste_text")
        if st.button("Load Text", key="btn_text"):
            if txt.strip():
                st.session_state.doc_text = txt.strip()
                st.success(f"✅ {len(txt):,} chars loaded")
            else: st.warning("Enter some text first.")

    with t2:
        pdf_file = st.file_uploader("", type=["pdf"], label_visibility="collapsed", key="pdf_up")
        if st.button("Extract PDF", key="btn_pdf"):
            if pdf_file:
                try:
                    st.session_state.doc_text = extract_pdf(pdf_file.read())
                    st.success(f"✅ {len(st.session_state.doc_text):,} chars extracted")
                except Exception as e: st.error(f"Failed: {e}")
            else: st.warning("Upload a PDF first.")

    with t3:
        docx_file = st.file_uploader("", type=["docx"], label_visibility="collapsed", key="docx_up")
        if st.button("Extract DOCX", key="btn_docx"):
            if docx_file:
                try:
                    st.session_state.doc_text = extract_docx(docx_file.read())
                    st.success(f"✅ {len(st.session_state.doc_text):,} chars extracted")
                except Exception as e: st.error(f"Failed: {e}")
            else: st.warning("Upload a DOCX first.")

    with t4:
        url_in = st.text_input("", placeholder="https://example.com/article...", label_visibility="collapsed", key="url_in")
        if st.button("Fetch URL", key="btn_url"):
            if url_in.startswith("http"):
                with st.spinner("Fetching..."):
                    try:
                        t = fetch_url(url_in)
                        if len(t) < 100: st.error("Not enough content found. Try pasting manually.")
                        else:
                            st.session_state.doc_text = t[:6000]
                            st.success(f"✅ {len(st.session_state.doc_text):,} chars fetched")
                    except Exception as e: st.error(f"Failed: {e}")
            else: st.warning("Enter a valid URL.")

    if st.session_state.doc_text:
        st.markdown(f'<div class="status-chip status-ok">✓ Document ready — {len(st.session_state.doc_text):,} chars</div>', unsafe_allow_html=True)

    # ── INFOGRAPHIC TYPE ──
    st.markdown('<div class="panel-label">02 · Infographic Style</div>', unsafe_allow_html=True)
    inf_type = st.selectbox("", list(INFOGRAPHIC_TYPES.keys()),
        format_func=lambda k: f"{INFOGRAPHIC_TYPES[k][0]} {INFOGRAPHIC_TYPES[k][1]}",
        label_visibility="collapsed")
    st.session_state.infographic_type = inf_type

    # ── CUSTOM TITLE ──
    st.markdown('<div class="panel-label">03 · Custom Title (optional)</div>', unsafe_allow_html=True)
    custom_title = st.text_input("", placeholder="Leave blank for AI to auto-generate...", label_visibility="collapsed", key="custom_title")

    # ── COLOR THEME ──
    st.markdown('<div class="panel-label">04 · Color Theme</div>', unsafe_allow_html=True)
    theme = st.selectbox("", ["Dark · Indigo & Purple", "Dark · Teal & Emerald", "Dark · Orange & Red", "Light · Clean & Modern", "Dark · Monochrome"], label_visibility="collapsed")

    theme_map = {
        "Dark · Indigo & Purple": "Deep dark (#0f0f1f background) with indigo (#6366f1), purple (#a855f7), and pink (#ec4899) accents",
        "Dark · Teal & Emerald": "Deep dark (#071a14 background) with teal (#14b8a6), emerald (#34d399), and cyan (#22d3ee) accents",
        "Dark · Orange & Red": "Deep dark (#1a0a05 background) with orange (#f97316), red (#ef4444), and amber (#f59e0b) accents",
        "Light · Clean & Modern": "Clean white (#ffffff background) with slate (#1e293b), blue (#3b82f6), and violet (#7c3aed) accents. Light and airy.",
        "Dark · Monochrome": "Pure black (#000000 background) with white (#ffffff) and gray (#6b7280) accents. Minimal and bold.",
    }

    # ── GENERATE ──
    st.markdown("<br>", unsafe_allow_html=True)
    gen_btn = st.button("✨ Generate Infographic", use_container_width=True)

with col_right:
    if not st.session_state.generated:
        st.markdown("""
        <div class="output-placeholder">
          <div style="font-size:3rem">🎨</div>
          <div class="placeholder-title">Your Infographic<br>Appears Here</div>
          <div class="placeholder-sub">Load a document → Choose style → Generate</div>
        </div>""", unsafe_allow_html=True)
    
    if st.session_state.infographic_html and st.session_state.generated:
        # Download buttons row
        dl_col1, dl_col2, dl_col3 = st.columns([1,1,2])
        with dl_col1:
            st.download_button(
                "⬇ HTML",
                data=st.session_state.infographic_html.encode(),
                file_name="infographic.html",
                mime="text/html",
                key="dl_html"
            )
        with dl_col2:
            # Encode HTML for PNG via browser print
            b64 = base64.b64encode(st.session_state.infographic_html.encode()).decode()
            st.download_button(
                "⬇ Source",
                data=st.session_state.infographic_html.encode(),
                file_name="infographic_source.html",
                mime="text/html",
                key="dl_src"
            )
        with dl_col3:
            st.markdown(f'<div class="status-chip status-info">✓ Infographic ready · Open HTML in browser to save as PNG</div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Render infographic inside iframe-like component
        # Use components.html for proper rendering
        import streamlit.components.v1 as components
        components.html(st.session_state.infographic_html, height=900, scrolling=True)

# ── GENERATE LOGIC ──
if gen_btn:
    if not st.session_state.doc_text.strip():
        st.error("⚠️ Please load a document first.")
    else:
        theme_desc = theme_map.get(theme, theme_map["Dark · Indigo & Purple"])
        modified_prompt = build_prompt(st.session_state.doc_text, inf_type, custom_title)
        modified_prompt = modified_prompt.replace(
            "Use this color palette: deep dark background (#0f0f1f) with vibrant accents (#6366f1 indigo, #a855f7 purple, #ec4899 pink, #f97316 orange, #34d399 green)",
            f"Use this color theme: {theme_desc}"
        )

        with st.spinner("🎨 Generating your infographic... (10-20 seconds)"):
            try:
                raw = call_groq(SYSTEM_PROMPT, modified_prompt, max_tokens=4000, temp=0.4)
                raw = re.sub(r'^```html\s*','', raw.strip())
                raw = re.sub(r'```$','', raw.strip())
                # Ensure it starts with DOCTYPE
                if not raw.strip().startswith('<!'):
                    idx = raw.find('<!DOCTYPE')
                    if idx == -1: idx = raw.find('<html')
                    if idx != -1: raw = raw[idx:]
                st.session_state.infographic_html = raw
                st.session_state.generated = True
                st.rerun()
            except Exception as e:
                st.error(f"Generation failed: {e}")
