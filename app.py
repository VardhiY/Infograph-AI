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
    st.error("⚠️ GROQ_API_KEY missing.")
    st.stop()

client = Groq(api_key=api_key)

# ══════════════════════════════════════════════════════════
# CSS — Light green (#e8f5e9) + Thick dark green (#1b5e20)
# ══════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=DM+Sans:wght@300;400;500;600&family=DM+Mono:wght@400;500&display=swap');

*, *::before, *::after { box-sizing: border-box; }

/* ═══ BASE ═══ */
.stApp {
    background: #e8f5e9 !important;
    color: #1b5e20 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 15px !important;
}
.stApp::before {
    content: '';
    position: fixed; inset: 0; z-index: 0; pointer-events: none;
    background:
        radial-gradient(ellipse 1100px 780px at   0%   0%, rgba(165,214,167,0.65) 0%, transparent 55%),
        radial-gradient(ellipse  900px 700px at 100%   5%, rgba(200,230,201,0.52) 0%, transparent 55%),
        radial-gradient(ellipse  800px 650px at   0% 100%, rgba(165,214,167,0.45) 0%, transparent 55%),
        radial-gradient(ellipse  950px 580px at 100% 100%, rgba(129,199,132,0.38) 0%, transparent 55%);
}
.block-container {
    padding-top: 0 !important;
    padding-bottom: 3rem !important;
    max-width: 1260px !important;
    position: relative; z-index: 1;
}
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #c8e6c9; }
::-webkit-scrollbar-thumb { background: #2e7d32; border-radius: 10px; }

/* ═══ NAV — thick dark green ═══ */
.ig-nav {
    display: flex; align-items: center; justify-content: space-between;
    padding: 0.88rem 1.7rem;
    background: #1b5e20;
    border-radius: 0 0 22px 22px;
    box-shadow: 0 6px 26px rgba(27,94,32,0.42);
    margin-bottom: 0;
}
.ig-logo-wrap { display: flex; align-items: center; gap: 0.65rem; }
.ig-logo-icon {
    width: 38px; height: 38px;
    background: linear-gradient(135deg, #4caf50, #a5d6a7);
    border-radius: 11px;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.05rem;
    box-shadow: 0 3px 10px rgba(0,0,0,0.28);
}
.ig-logo-text {
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 1.2rem; font-weight: 800; color: #ffffff; letter-spacing: -0.3px;
}
.ig-logo-text span { color: #a5d6a7; }
.ig-nav-pills { display: flex; align-items: center; gap: 0.4rem; flex-wrap: wrap; }
.ig-pill {
    font-family: 'DM Mono', monospace; font-size: 0.6rem;
    letter-spacing: 0.1em; text-transform: uppercase;
    color: #c8e6c9; border: 1.5px solid rgba(165,214,167,0.35);
    background: rgba(255,255,255,0.12);
    padding: 0.24rem 0.72rem; border-radius: 100px; font-weight: 600;
}
.ig-status {
    display: flex; align-items: center; gap: 0.45rem;
    font-size: 0.8rem; font-weight: 700; color: #a5d6a7;
    background: rgba(255,255,255,0.1);
    border: 1.5px solid rgba(165,214,167,0.3);
    padding: 0.32rem 0.9rem; border-radius: 100px;
}
.ig-status-dot {
    width: 8px; height: 8px; background: #69f0ae; border-radius: 50%;
    box-shadow: 0 0 10px rgba(105,240,174,0.9);
    animation: sDot 2.4s ease-in-out infinite; flex-shrink: 0;
}
@keyframes sDot { 0%,100%{opacity:1;} 50%{opacity:0.22;} }

/* ═══ HERO ═══ */
.ig-hero { text-align: center; padding: 2.8rem 0 2.2rem; }
.ig-hero-tag {
    display: inline-flex; align-items: center; gap: 0.45rem;
    background: #ffffff; border: 2.5px solid #43a047;
    border-radius: 100px; padding: 0.35rem 1.1rem;
    font-size: 0.77rem; font-weight: 700; color: #2e7d32;
    margin-bottom: 1.3rem;
    box-shadow: 0 3px 14px rgba(67,160,71,0.22);
}
.ig-hero-tag::before {
    content:''; width:8px; height:8px; background:#43a047; border-radius:50%;
    flex-shrink:0; box-shadow:0 0 8px rgba(67,160,71,0.7);
    animation: tagPulse 2s ease-in-out infinite;
}
@keyframes tagPulse { 0%,100%{opacity:1;transform:scale(1);} 50%{opacity:0.3;transform:scale(0.7);} }
.ig-h1 {
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: clamp(2.2rem, 4.5vw, 3.5rem); font-weight: 800;
    line-height: 1.1; letter-spacing: -1px; color: #1b5e20; margin: 0;
}
.ig-h1-accent {
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: clamp(2.2rem, 4.5vw, 3.5rem); font-weight: 800;
    line-height: 1.1; letter-spacing: -1px;
    background: linear-gradient(90deg, #2e7d32, #388e3c, #66bb6a);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-clip: text; display: block; margin-bottom: 1rem;
}
.ig-hero-sub {
    font-size: 1rem; color: #2e7d32; font-weight: 500;
    max-width: 480px; margin: 0 auto; line-height: 1.75;
}

/* ═══ CARD — white, thick left green border ═══ */
.ig-card {
    background: #ffffff;
    border: 2px solid #c8e6c9;
    border-left: 6px solid #388e3c;
    border-radius: 14px;
    padding: 1.5rem 1.5rem 1.1rem;
    margin-bottom: 1rem;
    box-shadow: 0 4px 20px rgba(56,142,60,0.14), 0 1px 4px rgba(0,0,0,0.05);
}

/* ═══ SECTION LABEL ═══ */
.ig-sec-label {
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 0.68rem; font-weight: 800; letter-spacing: 0.13em;
    text-transform: uppercase; color: #2e7d32;
    margin-bottom: 0.95rem; display: flex; align-items: center; gap: 0.5rem;
}
.ig-sec-label::after {
    content:''; flex:1; height:2.5px;
    background: linear-gradient(90deg, #a5d6a7, transparent);
    border-radius: 2px;
}

/* ═══ TABS ═══ */
div[data-baseweb="tab-list"] {
    background: #e8f5e9 !important; border-radius: 10px !important;
    padding: 4px !important; border: 2px solid #a5d6a7 !important;
    gap: 3px !important; margin-bottom: 1rem !important; width: fit-content !important;
}
div[data-baseweb="tab"] {
    border-radius: 7px !important; color: #2e7d32 !important;
    font-weight: 700 !important; font-family: 'DM Sans', sans-serif !important;
    font-size: 0.88rem !important; padding: 0.42rem 1.05rem !important;
    transition: all 0.18s !important; min-height: unset !important;
}
div[data-baseweb="tab"]:hover { background: #c8e6c9 !important; }
div[aria-selected="true"] {
    background: #1b5e20 !important; color: #ffffff !important;
    box-shadow: 0 3px 12px rgba(27,94,32,0.42) !important;
}
div[data-baseweb="tab-panel"] { background: transparent !important; padding: 0 !important; }

/* ═══ INPUTS ═══ */
div[data-testid="stTextArea"] label,
div[data-testid="stTextInput"] label,
div[data-testid="stSelectbox"] label,
div[data-testid="stFileUploader"] label { display: none !important; }

textarea {
    background: #f1f8e9 !important; border: 2px solid #a5d6a7 !important;
    border-radius: 11px !important; color: #1b5e20 !important;
    font-family: 'DM Sans', sans-serif !important; font-size: 0.95rem !important;
    padding: 0.85rem 1rem !important; line-height: 1.65 !important;
    transition: all 0.2s !important; resize: none !important;
}
textarea:focus {
    border-color: #2e7d32 !important;
    box-shadow: 0 0 0 3px rgba(46,125,50,0.18) !important;
    outline: none !important; background: #ffffff !important;
}
textarea::placeholder { color: #81c784 !important; }

.stTextInput input {
    background: #f1f8e9 !important; border: 2px solid #a5d6a7 !important;
    border-radius: 11px !important; color: #1b5e20 !important;
    font-family: 'DM Sans', sans-serif !important; font-size: 0.95rem !important;
    padding: 0.75rem 1rem !important; transition: all 0.2s !important;
}
.stTextInput input:focus {
    border-color: #2e7d32 !important;
    box-shadow: 0 0 0 3px rgba(46,125,50,0.18) !important;
    outline: none !important; background: #ffffff !important;
}
.stTextInput input::placeholder { color: #81c784 !important; }

/* ═══ SELECT ═══ */
div[data-baseweb="select"] > div {
    background: #f1f8e9 !important; border: 2px solid #a5d6a7 !important;
    border-radius: 11px !important; color: #1b5e20 !important;
    font-family: 'DM Sans', sans-serif !important;
}
div[data-baseweb="select"] > div:focus-within {
    border-color: #2e7d32 !important;
    box-shadow: 0 0 0 3px rgba(46,125,50,0.18) !important;
}
div[data-baseweb="select"] span { color: #1b5e20 !important; font-weight: 600 !important; }
[data-baseweb="popover"] > div {
    background: #ffffff !important; border: 2px solid #a5d6a7 !important;
    border-radius: 11px !important; box-shadow: 0 8px 24px rgba(27,94,32,0.2) !important;
}
[role="option"] { color: #1b5e20 !important; font-family: 'DM Sans', sans-serif !important; padding: 0.65rem 1rem !important; }
[role="option"]:hover { background: #e8f5e9 !important; }

/* ═══ FILE UPLOADER ═══ */
[data-testid="stFileUploader"] section {
    background: #f1f8e9 !important; border: 2.5px dashed #66bb6a !important;
    border-radius: 13px !important; padding: 1.4rem 1rem !important; transition: all 0.2s !important;
}
[data-testid="stFileUploader"] section:hover {
    border-color: #1b5e20 !important; background: #e8f5e9 !important;
}
[data-testid="stFileUploader"] section p,
[data-testid="stFileUploader"] section span {
    color: #388e3c !important; font-weight: 500 !important;
}
[data-testid="stFileUploader"] button {
    background: #2e7d32 !important; color: #ffffff !important;
    border-radius: 8px !important; border: none !important; font-weight: 700 !important;
}

/* ═══ PRIMARY BUTTON — thick dark green ═══ */
.stButton > button {
    width: 100% !important; background: #2e7d32 !important;
    border: none !important; border-bottom: 4px solid #1b5e20 !important;
    border-radius: 12px !important; color: #ffffff !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important; font-weight: 800 !important;
    font-size: 1rem !important; padding: 0.88rem 1.5rem !important;
    margin-top: 0.55rem !important; transition: all 0.18s !important;
    box-shadow: 0 4px 16px rgba(46,125,50,0.38) !important; letter-spacing: 0.01em !important;
}
.stButton > button:hover {
    background: #1b5e20 !important; transform: translateY(-2px) !important;
    box-shadow: 0 8px 24px rgba(27,94,32,0.45) !important;
}
.stButton > button:active { transform: translateY(1px) !important; border-bottom-width: 2px !important; }

/* ═══ DOWNLOAD BUTTON ═══ */
.stDownloadButton > button {
    background: #e8f5e9 !important; border: 2px solid #66bb6a !important;
    border-bottom: 3px solid #388e3c !important; color: #1b5e20 !important;
    font-family: 'DM Sans', sans-serif !important; font-weight: 700 !important;
    border-radius: 10px !important; padding: 0.5rem 1.1rem !important;
    font-size: 0.88rem !important; transition: all 0.18s !important;
}
.stDownloadButton > button:hover {
    background: #c8e6c9 !important; border-color: #2e7d32 !important;
}

/* ═══ SECURITY ROWS ═══ */
.sec-row {
    display: flex; align-items: center; justify-content: space-between;
    background: #f1f8e9; border: 1.5px solid #c8e6c9;
    border-left: 5px solid #4caf50;
    border-radius: 10px; padding: 0.62rem 1rem; margin-bottom: 0.42rem; transition: all 0.15s;
}
.sec-row:hover { background: #e8f5e9; border-left-color: #1b5e20; }
.sec-row-label { font-size: 0.88rem; font-weight: 700; color: #1b5e20; }
.badge-pass {
    font-size: 0.74rem; font-weight: 800; color: #1b5e20;
    background: #c8e6c9; border: 2px solid #66bb6a;
    border-radius: 6px; padding: 0.14rem 0.52rem;
}
.badge-fail {
    font-size: 0.74rem; font-weight: 800; color: #b71c1c;
    background: #ffebee; border: 2px solid #ef9a9a;
    border-radius: 6px; padding: 0.14rem 0.52rem;
}
.badge-info {
    font-size: 0.74rem; font-weight: 800; color: #e65100;
    background: #fff8e1; border: 2px solid #ffe082;
    border-radius: 6px; padding: 0.14rem 0.52rem;
}

/* ═══ SCORE ROW ═══ */
.score-row {
    display: flex; align-items: center; gap: 1.4rem;
    background: #e8f5e9; border: 2.5px solid #a5d6a7;
    border-radius: 13px; padding: 0.95rem 1.2rem; margin-top: 0.55rem;
}
.score-num { font-family:'Plus Jakarta Sans',sans-serif; font-size:2.2rem; font-weight:800; line-height:1; }
.score-lbl { font-family:'DM Mono',monospace; font-size:0.58rem; font-weight:700; letter-spacing:0.12em; text-transform:uppercase; color:#388e3c; margin-bottom:0.14rem; }
.score-bar-bg { height:10px; background:#c8e6c9; border-radius:100px; overflow:hidden; flex:1; border:1px solid #a5d6a7; }
.score-bar-fill { height:100%; border-radius:100px; }

/* ═══ CANVAS ═══ */
.canvas-header {
    display: flex; align-items: center; justify-content: space-between;
    padding: 1rem 1.5rem; background: #2e7d32;
    border-radius: 16px 16px 0 0; box-shadow: 0 4px 18px rgba(46,125,50,0.35);
}
.canvas-title {
    font-family: 'Plus Jakarta Sans', sans-serif; font-size: 0.98rem;
    font-weight: 800; color: #ffffff; display: flex; align-items: center; gap: 0.5rem;
}
.canvas-body {
    border: 2.5px solid #a5d6a7; border-top: none;
    border-radius: 0 0 16px 16px; overflow: hidden;
    box-shadow: 0 6px 24px rgba(56,142,60,0.14);
}
.cbadge-ready {
    display: inline-flex; align-items: center; gap: 0.38rem;
    font-size: 0.76rem; font-weight: 800; color: #1b5e20;
    background: #a5d6a7; border: 2px solid #66bb6a;
    border-radius: 100px; padding: 0.26rem 0.85rem;
}
.cbadge-wait {
    display: inline-flex; align-items: center; gap: 0.38rem;
    font-size: 0.76rem; font-weight: 800; color: #e65100;
    background: #fff8e1; border: 2px solid #ffe082;
    border-radius: 100px; padding: 0.26rem 0.85rem;
}
.cbadge-dot { width: 7px; height: 7px; border-radius: 50%; flex-shrink: 0; }

/* ═══ EMPTY STATE ═══ */
.empty-wrap {
    min-height: 560px; background: #f1f8e9;
    display: flex; align-items: center; justify-content: center;
    position: relative; overflow: hidden;
}
.empty-grid {
    position: absolute; inset: 0; pointer-events: none;
    background-image:
        linear-gradient(rgba(56,142,60,0.12) 1px, transparent 1px),
        linear-gradient(90deg, rgba(56,142,60,0.12) 1px, transparent 1px);
    background-size: 36px 36px;
}
.empty-inner { position: relative; z-index: 1; text-align: center; padding: 2rem; }
.empty-emoji { font-size:4rem; display:block; margin-bottom:1.1rem; animation:float 3.2s ease-in-out infinite; }
@keyframes float { 0%,100%{transform:translateY(0)} 50%{transform:translateY(-12px)} }
.empty-h { font-family:'Plus Jakarta Sans',sans-serif; font-size:1.5rem; font-weight:800; color:#a5d6a7; margin-bottom:0.45rem; }
.empty-p { font-size:0.92rem; color:#81c784; line-height:1.7; }
.steps { display:flex; gap:0.85rem; margin-top:1.9rem; justify-content:center; flex-wrap:wrap; }
.step {
    background: #ffffff; border: 2px solid #a5d6a7; border-top: 5px solid #2e7d32;
    border-radius: 12px; padding: 0.9rem 1.2rem; text-align: center;
    box-shadow: 0 3px 12px rgba(56,142,60,0.14); min-width: 90px;
}
.step-n { font-family:'DM Mono',monospace; font-size:0.65rem; color:#2e7d32; font-weight:800; letter-spacing:0.1em; text-transform:uppercase; margin-bottom:0.28rem; }
.step-t { font-family:'Plus Jakarta Sans',sans-serif; font-size:0.88rem; color:#1b5e20; font-weight:800; }

/* ═══ CHARS BADGE ═══ */
.chars-badge {
    display: inline-flex; align-items: center; gap: 0.38rem;
    font-family: 'DM Mono', monospace; font-size: 0.73rem; font-weight: 700;
    color: #1b5e20; background: #c8e6c9; border: 2px solid #66bb6a;
    border-radius: 8px; padding: 0.26rem 0.75rem; margin-top: 0.55rem;
}

/* ═══ ALERTS ═══ */
div[data-testid="stAlert"],
.stSuccess > div { background: #e8f5e9 !important; border: 2px solid #a5d6a7 !important; border-left: 5px solid #2e7d32 !important; border-radius: 11px !important; color: #1b5e20 !important; }
.stError > div   { background: #ffebee !important; border: 2px solid #ef9a9a !important; border-left: 5px solid #c62828 !important; border-radius: 11px !important; }
.stWarning > div { background: #fff8e1 !important; border: 2px solid #ffe082 !important; border-left: 5px solid #f57f17 !important; border-radius: 11px !important; }
.stSpinner > div { border-top-color: #1b5e20 !important; }

/* ═══ EXPORT HINT ═══ */
.export-hint {
    font-size: 0.85rem; color: #388e3c; line-height: 2;
    margin-top: 0.8rem; font-family: 'DM Sans', sans-serif;
    background: #f1f8e9; border: 1.5px solid #c8e6c9;
    border-radius: 10px; padding: 0.75rem 1rem;
}
.export-hint strong { color: #1b5e20; font-weight: 800; }
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════
# SECURITY
# ══════════════════════════════════════════════════════════
MALWARE_SIGS = [b"cmd.exe", b"powershell", b"eval(", b"WScript", b"<script", b"javascript:"]

def check_malware(fb):
    fl = fb.lower()
    return not any(s.lower() in fl for s in MALWARE_SIGS)

def check_integrity(fb, ext):
    try:
        if ext == "pdf":
            import pypdf; pypdf.PdfReader(io.BytesIO(fb))
        elif ext == "docx":
            import docx; docx.Document(io.BytesIO(fb))
        return True
    except: return False

def fmt_size(b):
    if b < 1024: return f"{b} B"
    elif b < 1_048_576: return f"{b/1024:.1f} KB"
    else: return f"{b/1_048_576:.1f} MB"

def security_scan(fb, ext):
    m_ok = check_malware(fb)
    i_ok = check_integrity(fb, ext)
    sz   = fmt_size(len(fb))
    score = 100 - (0 if m_ok else 40) - (0 if i_ok else 30)
    clr   = "#1b5e20" if score == 100 else ("#e65100" if score >= 60 else "#b71c1c")
    bar   = ("linear-gradient(90deg,#2e7d32,#66bb6a)" if score == 100 else
             "linear-gradient(90deg,#ef6c00,#ffa726)" if score >= 60 else
             "linear-gradient(90deg,#c62828,#ef5350)")
    bp    = lambda ok: '<span class="badge-pass">✓ Pass</span>' if ok else '<span class="badge-fail">✗ Fail</span>'
    html  = f"""
<div class="ig-sec-label" style="margin-top:1.1rem;">Security Scan</div>
<div class="sec-row"><span class="sec-row-label">🛡️ Malware Signature Scan</span>{bp(m_ok)}</div>
<div class="sec-row"><span class="sec-row-label">✅ File Integrity Check</span>{bp(i_ok)}</div>
<div class="sec-row"><span class="sec-row-label">📦 File Size</span><span class="badge-info">{sz} · No limit</span></div>
<div class="score-row">
  <div><div class="score-lbl">Security</div>
       <div class="score-num" style="color:{clr};">{score}</div>
       <div style="font-size:0.6rem;color:#66bb6a;font-family:'DM Mono',monospace;">/100</div></div>
  <div style="flex:1;"><div class="score-lbl" style="margin-bottom:.3rem;">Confidence</div>
    <div class="score-bar-bg"><div class="score-bar-fill" style="width:{score}%;background:{bar};"></div></div>
    <div style="font-size:.7rem;color:{clr};font-family:'DM Mono',monospace;margin-top:.28rem;font-weight:800;">{score}% clean</div>
  </div>
</div>"""
    return html, m_ok, i_ok


# ══════════════════════════════════════════════════════════
# EXTRACTION
# ══════════════════════════════════════════════════════════
def extract_pdf(fb):
    import pypdf
    return "\n".join(p.extract_text() or "" for p in pypdf.PdfReader(io.BytesIO(fb)).pages).strip()

def extract_docx(fb):
    import docx
    return "\n".join(p.text for p in docx.Document(io.BytesIO(fb)).paragraphs).strip()

def fetch_url(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=15) as r:
        html = r.read().decode('utf-8', errors='ignore')
    txt = re.sub(r'<style[^>]*>.*?</style>', '', html, flags=re.DOTALL)
    txt = re.sub(r'<script[^>]*>.*?</script>', '', txt, flags=re.DOTALL)
    return re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', txt)).strip()

def call_groq(system, user, max_tokens=4000, temp=0.35):
    r = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "system", "content": system}, {"role": "user", "content": user}],
        temperature=temp, max_tokens=max_tokens)
    return r.choices[0].message.content.strip()


# ══════════════════════════════════════════════════════════
# INFOGRAPHIC CONFIG
# ══════════════════════════════════════════════════════════
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
    "Emerald & Green":      "#071c12 dark bg, #10b981 emerald, #34d399 mint, white text",
    "Teal & Cyan":          "#0a2535 dark bg, #00bcd4 teal, #26c6da cyan, white text",
    "Dark Indigo & Purple": "#0a0f1e dark bg, #6366f1 indigo, #8b5cf6 purple, #e0e7ff text",
    "Sunset Orange & Red":  "#1a0800 dark bg, #f97316 orange, #ef4444 red, #fef3c7 text",
    "Clean White & Blue":   "#f8faff white bg, #1e3a5f navy, #3b82f6 blue, #dbeafe accents",
    "Warm Cream":           "#faf7f2 cream bg, #292524 dark, #dc6e2e terracotta, #f59e0b amber",
    "Black & Gold":         "#080608 black bg, #f59e0b gold, #fbbf24 bright gold, white text",
}

SYS = """You are a world-class infographic designer. Create Canva/Piktochart quality visual infographics.
Return ONLY complete HTML starting with <!DOCTYPE html>. No markdown, no fences.
All CSS in <style>. Import Google Fonts. Width 900px centered. MUST include SVG charts."""

def build_prompt(text, itype, title, theme):
    tmap = {
        "auto":       "Choose best layout. Mix stat circles, donut charts, key insight cards.",
        "summary":    "KEY POINTS: colored header, 5-8 numbered cards in 2-col grid with emoji icons.",
        "timeline":   "TIMELINE: bold header, vertical alternating events, year badges, connecting dots.",
        "stats":      "STATS DASHBOARD: hero numbers row, SVG donut charts, CSS bar charts.",
        "comparison": "COMPARISON: two-column VS layout, checkmark rows, VS badge, summary banner.",
        "process":    "PROCESS FLOW: numbered steps, arrow connectors, icon per step, color progression.",
        "report":     "FULL REPORT: hero header, 4 KPI cards, 2-3 content sections with charts, footer.",
    }
    t = f'Title: "{title}"' if title.strip() else "Auto-generate a compelling title."
    return f"""Create a stunning professional infographic.
TYPE: {tmap.get(itype, tmap['auto'])}
{t}
THEME: {theme}
REQUIREMENTS: 900px wide, margin:0 auto, SVG donut rings (stroke-dasharray), CSS bar charts,
emoji icons throughout, fadeInUp animations, cards with box-shadow, bold numbers 2.5rem+,
Google Fonts, "Generated by InfographAI" footer.
DOCUMENT: {text[:5000]}
Return ONLY complete HTML."""


# ══════════════════════════════════════════════════════════
# SESSION
# ══════════════════════════════════════════════════════════
for k, v in [("doc_text", ""), ("html_out", ""), ("generated", False)]:
    if k not in st.session_state: st.session_state[k] = v


# ══════════════════════════════════════════════════════════
# NAV
# ══════════════════════════════════════════════════════════
st.markdown("""
<div class="ig-nav">
  <div class="ig-logo-wrap">
    <div class="ig-logo-icon">🎨</div>
    <div class="ig-logo-text">Infograph<span>AI</span></div>
  </div>
  <div class="ig-nav-pills">
    <span class="ig-pill">PDF</span>
    <span class="ig-pill">DOCX</span>
    <span class="ig-pill">TEXT</span>
    <span class="ig-pill">URL</span>
    <span class="ig-pill">7 FORMATS</span>
    <span class="ig-pill">7 THEMES</span>
  </div>
  <div class="ig-status"><div class="ig-status-dot"></div>AI Online</div>
</div>
""", unsafe_allow_html=True)

# HERO
st.markdown("""
<div class="ig-hero">
  <div class="ig-hero-tag">AI-Powered Infographic Generator</div>
  <h1 class="ig-h1">Transform Documents</h1>
  <span class="ig-h1-accent">into Visual Infographics</span>
  <p class="ig-hero-sub">Paste text, upload PDF or DOCX, or drop a URL — InfographAI turns your content into stunning shareable visuals.</p>
</div>
""", unsafe_allow_html=True)

lcol, rcol = st.columns([1, 2.2], gap="large")

# ══════════════════════════════════════════════════════════
# LEFT
# ══════════════════════════════════════════════════════════
with lcol:

    st.markdown('<div class="ig-card">', unsafe_allow_html=True)
    st.markdown('<div class="ig-sec-label">Document Input</div>', unsafe_allow_html=True)

    t1, t2, t3, t4 = st.tabs(["📝 Text", "📄 PDF", "📃 DOCX", "🔗 URL"])

    with t1:
        txt = st.text_area("", height=180,
            placeholder="Paste your document, report, article or any text here…",
            label_visibility="collapsed", key="itxt")
        if st.button("Load Text →", key="btxt"):
            if txt.strip():
                st.session_state.doc_text = txt.strip()
                st.success(f"✅ Loaded {len(txt):,} characters")
            else:
                st.warning("Please enter some text first.")

    with t2:
        pf = st.file_uploader("", type=["pdf"], label_visibility="collapsed", key="ipdf")
        if st.button("Extract & Scan PDF →", key="bpdf"):
            if pf:
                fb = pf.read()
                sh, m_ok, i_ok = security_scan(fb, "pdf")
                st.markdown(sh, unsafe_allow_html=True)
                if m_ok and i_ok:
                    try:
                        st.session_state.doc_text = extract_pdf(fb)
                        st.success(f"✅ Extracted {len(st.session_state.doc_text):,} chars")
                    except Exception as e: st.error(f"Failed: {e}")
                else: st.error("🚫 File blocked by security scan.")
            else: st.warning("Upload a PDF first.")

    with t3:
        df = st.file_uploader("", type=["docx"], label_visibility="collapsed", key="idocx")
        if st.button("Extract & Scan DOCX →", key="bdocx"):
            if df:
                fb = df.read()
                sh, m_ok, i_ok = security_scan(fb, "docx")
                st.markdown(sh, unsafe_allow_html=True)
                if m_ok and i_ok:
                    try:
                        st.session_state.doc_text = extract_docx(fb)
                        st.success(f"✅ Extracted {len(st.session_state.doc_text):,} chars")
                    except Exception as e: st.error(f"Failed: {e}")
                else: st.error("🚫 File blocked by security scan.")
            else: st.warning("Upload a DOCX first.")

    with t4:
        ui = st.text_input("", placeholder="https://example.com/article…",
                           label_visibility="collapsed", key="iurl")
        if st.button("Fetch URL →", key="burl"):
            if ui.startswith("http"):
                with st.spinner("Fetching…"):
                    try:
                        t = fetch_url(ui)
                        if len(t) < 100: st.error("Not enough content found.")
                        else:
                            st.session_state.doc_text = t[:8000]
                            st.success(f"✅ Fetched {len(st.session_state.doc_text):,} chars")
                    except Exception as e: st.error(f"Failed: {e}")
            else: st.warning("Enter a valid URL starting with https://")

    if st.session_state.doc_text:
        st.markdown(f'<div class="chars-badge">✓ &nbsp;{len(st.session_state.doc_text):,} chars loaded</div>',
                    unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # CONFIG
    st.markdown('<div class="ig-card">', unsafe_allow_html=True)
    st.markdown('<div class="ig-sec-label">Configuration</div>', unsafe_allow_html=True)

    st.markdown('<p style="font-family:\'DM Mono\',monospace;font-size:0.68rem;font-weight:800;letter-spacing:0.12em;text-transform:uppercase;color:#2e7d32;margin:0 0 0.4rem;">Infographic Format</p>', unsafe_allow_html=True)
    itype = st.selectbox("fmt", list(TYPES.keys()), format_func=lambda k: TYPES[k],
                         label_visibility="collapsed", key="itype")

    st.markdown('<p style="font-family:\'DM Mono\',monospace;font-size:0.68rem;font-weight:800;letter-spacing:0.12em;text-transform:uppercase;color:#2e7d32;margin:0.8rem 0 0.4rem;">Color Theme</p>', unsafe_allow_html=True)
    theme = st.selectbox("thm", list(THEMES.keys()), label_visibility="collapsed", key="itheme")

    st.markdown('<p style="font-family:\'DM Mono\',monospace;font-size:0.68rem;font-weight:800;letter-spacing:0.12em;text-transform:uppercase;color:#2e7d32;margin:0.8rem 0 0.4rem;">Custom Title (optional)</p>', unsafe_allow_html=True)
    ctitle = st.text_input("", placeholder="Leave blank — AI will auto-generate…",
                           label_visibility="collapsed", key="ictitle")

    st.markdown("<div style='height:.2rem'></div>", unsafe_allow_html=True)
    gen = st.button("✨  Generate Infographic", key="bgen")
    st.markdown('</div>', unsafe_allow_html=True)

    if st.session_state.generated:
        st.markdown('<div class="ig-card">', unsafe_allow_html=True)
        st.markdown('<div class="ig-sec-label">Export</div>', unsafe_allow_html=True)
        st.download_button("⬇  Download HTML File",
                           data=st.session_state.html_out.encode(),
                           file_name="infographic.html", mime="text/html")
        st.markdown("""
<div class="export-hint">
  <strong>Save as PNG/PDF:</strong><br>
  Open in Chrome → Ctrl+P<br>
  → Save as PDF or screenshot
</div>""", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════
# RIGHT — Canvas
# ══════════════════════════════════════════════════════════
with rcol:
    ready = st.session_state.generated and st.session_state.html_out
    badge = (
        '<span class="cbadge-ready"><span class="cbadge-dot" style="background:#1b5e20;box-shadow:0 0 7px rgba(27,94,32,0.7);"></span>Infographic Ready</span>'
        if ready else
        '<span class="cbadge-wait"><span class="cbadge-dot" style="background:#fb8c00;box-shadow:0 0 7px rgba(251,140,0,0.7);"></span>Awaiting Input</span>'
    )
    st.markdown(f"""
<div class="canvas-header">
  <div class="canvas-title">🖼 Output Canvas</div>
  {badge}
</div>
<div class="canvas-body">""", unsafe_allow_html=True)

    if not ready:
        st.markdown("""
<div class="empty-wrap">
  <div class="empty-grid"></div>
  <div class="empty-inner">
    <span class="empty-emoji">🎨</span>
    <div class="empty-h">Your infographic appears here</div>
    <div class="empty-p">Load a document, choose format and theme,<br>then hit Generate.</div>
    <div class="steps">
      <div class="step"><div class="step-n">Step 01</div><div class="step-t">Load Doc</div></div>
      <div class="step"><div class="step-n">Step 02</div><div class="step-t">Configure</div></div>
      <div class="step"><div class="step-n">Step 03</div><div class="step-t">Generate ✨</div></div>
    </div>
  </div>
</div>""", unsafe_allow_html=True)
    else:
        components.html(st.session_state.html_out, height=980, scrolling=True)

    st.markdown('</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════
# GENERATE
# ══════════════════════════════════════════════════════════
if gen:
    if not st.session_state.doc_text.strip():
        st.error("⚠️ Please load a document first — Text, PDF, DOCX or URL.")
    else:
        theme_desc = THEMES.get(theme, list(THEMES.values())[0])
        prompt = build_prompt(st.session_state.doc_text, itype, ctitle, theme_desc)
        with st.spinner("✨ Generating your infographic…"):
            try:
                raw = call_groq(SYS, prompt, max_tokens=4000, temp=0.38)
                raw = re.sub(r'^```html\s*', '', raw.strip())
                raw = re.sub(r'^```\s*',     '', raw.strip())
                raw = re.sub(r'```\s*$',     '', raw.strip())
                if not raw.strip().startswith('<!'):
                    for tag in ['<!DOCTYPE', '<html']:
                        idx = raw.find(tag)
                        if idx != -1: raw = raw[idx:]; break
                st.session_state.html_out  = raw
                st.session_state.generated = True
                st.rerun()
            except Exception as e:
                st.error(f"Generation failed: {e}")
