import base64
from pathlib import Path
import streamlit as st
import streamlit.components.v1 as components

VERSION = "v14"
st.set_page_config(page_title="WLF Options Profit Calculator", page_icon="WLF", layout="wide")

ASSET_DIR = Path(__file__).parent / "assets"

def img_b64(name: str) -> str:
    p = ASSET_DIR / name
    if not p.exists():
        return ""
    return base64.b64encode(p.read_bytes()).decode()

LOGOS = {
    "IBKR": "ibkr.png",
    "Charles Schwab": "schwab.png",
    "E*TRADE": "etrade.png",
    "Custom": "",
}
BROKERS = {
    "IBKR": 0.65,
    "Charles Schwab": 0.65,
    "E*TRADE": 0.65,
    "Custom": 0.65,
}

TEXT = {
    "ES": {
        "title": "Calculadora de Ganancia en Opciones",
        "subtitle": "Calcula el precio límite para cerrar una operación con ganancia - <span>SELL TO CLOSE</span>",
        "broker": "Broker",
        "contracts": "Contratos",
        "premium": "Prima de entrada ($)",
        "target": "Objetivo (%)",
        "include_fees": "Incluir comisiones",
        "round": "Redondear a $0.01",
        "fee": "Comision",
        "per_side": "/ lado",
        "custom_fee": "Comisión por lado ($)",
        "result_title": "PRECIO LIMITE SELL TO CLOSE",
        "result_help": "Precio premium para pegar en el broker.",
        "copy_title": "Copiar precio al broker",
        "copy_button": "Copiar",
        "copy_hint": "Si el botón no copia, selecciona el número y usa Ctrl+C.",
        "copied": "Copiado",
        "entry_cost": "Costo de entrada",
        "fees_total": "Comisiones totales",
        "gross": "Objetivo bruto",
        "net": "Objetivo neto",
        "formula": "Formula",
        "base": "Base = prima x (1 + objetivo / 100)",
        "fee_adj": "Ajuste comision = comision ida y vuelta / 100",
        "exit": "Limite de salida = Base + Ajuste comision",
        "calc": "Calculo actual",
    },
    "EN": {
        "title": "Options Profit Calculator",
        "subtitle": "Calculate the limit price to close an options trade in profit - <span>SELL TO CLOSE</span>",
        "broker": "Broker",
        "contracts": "Contracts",
        "premium": "Entry premium ($)",
        "target": "Target (%)",
        "include_fees": "Include fees",
        "round": "Round to $0.01",
        "fee": "Fee",
        "per_side": "/ side",
        "custom_fee": "Fee per side ($)",
        "result_title": "SELL TO CLOSE LIMIT PRICE",
        "result_help": "This is the option premium price you type into your broker.",
        "copy_title": "Copy price to broker",
        "copy_button": "Copy",
        "copy_hint": "If the button does not copy, select the number and press Ctrl+C.",
        "copied": "Copied",
        "entry_cost": "Entry cost",
        "fees_total": "Total fees",
        "gross": "Gross target",
        "net": "Net target",
        "formula": "Formula",
        "base": "Base = premium × (1 + target / 100)",
        "fee_adj": "Fee adjustment = round-trip fee / 100",
        "exit": "Exit limit = Base + Fee adjustment",
        "calc": "Current calculation",
    },
}

st.markdown(
    """
<style>
[data-testid="stHeader"] {background: rgba(6, 10, 22, 0.86);} 
.block-container {padding-top: .75rem; max-width: 1180px;}
html, body, [class*="css"] {font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;}
.stApp {background: radial-gradient(circle at top, #0a2324 0, #071223 34%, #050914 100%); color: #f8fbff;}
.logo-wrap {text-align:center; margin-top: .15rem; margin-bottom: .45rem;}
.logo-wrap img {height: 58px; object-fit: contain;}
.main-title {font-size: 3.0rem; font-weight: 900; text-align:center; margin: .05rem 0 .25rem; letter-spacing:-1.5px;}
.subtitle {text-align:center; color:#d5dfef; font-size: 1.08rem; margin-bottom: 1rem;}
.subtitle span {color:#74ff66; font-weight:800;}
.lang-select-wrap {max-width: 92px; margin-left:auto; margin-top:.15rem; margin-bottom:.25rem;}
.broker-row {display:flex; gap:.7rem; flex-wrap:wrap; margin:.35rem 0 .65rem;}
.broker-chip {border:1px solid #34415b; border-radius:14px; padding:.55rem .85rem; font-weight:900; color:#ffffff; background:#101827; display:flex; gap:.5rem; align-items:center;}
.broker-chip.active {border-color:#72ff66; box-shadow:0 0 0 1px #72ff66 inset; color:#72ff66;}
.broker-detail {display:flex; align-items:center; gap:.75rem; margin:.4rem 0 .8rem;}
.broker-detail img {width:42px; height:42px; border-radius:8px; object-fit:contain; background:#fff; padding:4px;}
.broker-detail .name {font-weight:900; font-size:1.15rem;}
.fee-pill {display:inline-block; padding:.42rem .8rem; border-radius:999px; border:1px solid #55d65c; background:rgba(50,150,70,.16); color:#78ff74; font-weight:900; font-size:.9rem;}
.result-card {border:1px solid #58e85b; border-radius:26px; padding:1.55rem 1.7rem; background:linear-gradient(135deg, rgba(14,50,50,.78), rgba(7,14,30,.92)); min-height: 220px; box-shadow:0 0 26px rgba(64,255,70,.12);}
.result-title {font-size:1.12rem; color:#c4d1dc; font-weight:900; letter-spacing:.3px;}
.big-price {font-size:5.7rem; line-height:1; color:#80ff67; font-weight:950; letter-spacing:-3px; margin:.5rem 0;}
.result-help {font-size:1.05rem; color:#d9e6ea; max-width: 410px;}
.copy-card {border:1px solid #3f9cff; border-radius:16px; background:rgba(33,91,150,.11); padding:.85rem 1rem; margin-top:.9rem;}
.copy-title {font-weight:900; color:#8fd2ff; margin-bottom:.45rem;}
.metric-card {border:1px solid #29344a; border-radius:16px; padding:1rem 1.1rem; background:rgba(6,10,25,.52); min-height:95px;}
.metric-label {color:#b7c6d7; font-size:.9rem; margin-bottom:.35rem;}
.metric-value {font-size:1.45rem; font-weight:950; color:#fff;}
.formula-card {border:1px solid #26344a; border-radius:18px; padding:1.05rem 1.2rem; background:#070b19; margin-top:.75rem;}
.formula-card pre {white-space:pre-wrap; color:#f5f7ff; font-size:.92rem; line-height:1.8; margin:0;}
.footer {text-align:center; color:#9badc3; margin:1.1rem 0 .2rem; font-size:.85rem;}
button[kind="secondary"] {font-weight:900 !important;}
.stNumberInput label, .stSelectbox label {font-weight:800 !important; color:#dfe8f7 !important;}
</style>
""",
    unsafe_allow_html=True,
)

# State defaults
if "broker" not in st.session_state:
    st.session_state.broker = "IBKR"
if "lang" not in st.session_state:
    st.session_state.lang = "ES"

# Language selector: top-right inside the app content, visible but not stuck to the browser toolbar
top_left, top_right = st.columns([8, 1.25])
with top_right:
    st.markdown('<div class="lang-select-wrap">', unsafe_allow_html=True)
    lang_label = st.selectbox("", ["ES", "EN"], index=0 if st.session_state.lang == "ES" else 1, key="lang_select", label_visibility="collapsed")
    st.markdown('</div>', unsafe_allow_html=True)
if lang_label != st.session_state.lang:
    st.session_state.lang = lang_label
    st.rerun()

# Initial language setup
t = TEXT[st.session_state.lang]

logo = img_b64("wlf_trading_cropped.png") or img_b64("wlf_trading.png")
if logo:
    st.markdown(f'<div class="logo-wrap"><img src="data:image/png;base64,{logo}" /></div>', unsafe_allow_html=True)
st.markdown(f'<div class="main-title">{t["title"]}</div>', unsafe_allow_html=True)
st.markdown(f'<div class="subtitle">{t["subtitle"]}</div>', unsafe_allow_html=True)

left, right = st.columns([1.38, 1.0], gap="large")

with left:
    st.markdown(f"**{t['broker']}**")
    broker_cols = st.columns(4)
    for i, b in enumerate(LOGOS.keys()):
        with broker_cols[i]:
            active = st.session_state.broker == b
            label = b
            if st.button(label, key=f"broker_{b}", use_container_width=True):
                st.session_state.broker = b
                st.rerun()

    broker = st.session_state.broker
    broker_logo = img_b64(LOGOS.get(broker, "")) if LOGOS.get(broker) else ""
    img_html = f'<img src="data:image/png;base64,{broker_logo}" />' if broker_logo else '<div style="width:42px;height:42px;border-radius:8px;border:1px solid #445;display:flex;align-items:center;justify-content:center;color:#fff;font-weight:900;">C</div>'
    fee_default = BROKERS.get(broker, 0.65)
    st.markdown(
        f"""
        <div class="broker-detail">
            {img_html}
            <div class="name">{broker}</div>
            <div class="fee-pill">{t['fee']}: ${fee_default:.2f} {t['per_side']}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    c1, c2, c3 = st.columns(3)
    with c1:
        contracts = st.number_input(t["contracts"], min_value=1, max_value=200, value=1, step=1)
    with c2:
        premium = st.number_input(t["premium"], min_value=0.01, max_value=999.99, value=2.50, step=0.01, format="%.2f")
    with c3:
        target_pct = st.number_input(t["target"], min_value=0.0, max_value=1000.0, value=35.0, step=1.0, format="%.2f")

    f1, f2, f3 = st.columns([1, 1, 1])
    with f1:
        include_fees = st.toggle(t["include_fees"], value=True)
    with f2:
        round_tick = st.toggle(t["round"], value=True)
    with f3:
        if broker == "Custom":
            fee_per_side = st.number_input(t["custom_fee"], min_value=0.0, max_value=99.0, value=0.65, step=0.01, format="%.2f")
        else:
            fee_per_side = fee_default

base_limit = premium * (1 + target_pct / 100)
round_trip_fee_per_contract = fee_per_side * 2 if include_fees else 0.0
fee_adjustment = round_trip_fee_per_contract / 100
limit_price_raw = base_limit + fee_adjustment
limit_price = round(limit_price_raw + 1e-9, 2) if round_tick else limit_price_raw
copy_value = f"{limit_price:.2f}"

entry_cost = premium * contracts * 100
total_fees = round_trip_fee_per_contract * contracts
gross_target = (base_limit - premium) * contracts * 100
net_target = (limit_price * contracts * 100) - entry_cost - total_fees
net_pct = (net_target / entry_cost * 100) if entry_cost else 0
gross_pct = (gross_target / entry_cost * 100) if entry_cost else 0

with right:
    # One compact custom result card. The copy control lives inside the card, not below it.
    components.html(
        f"""
        <div style="font-family:Inter,Arial,sans-serif;box-sizing:border-box;padding-bottom:10px;">
          <div style="border:1px solid #58e85b;border-radius:26px;padding:24px 28px;
                      background:linear-gradient(135deg, rgba(14,50,50,.78), rgba(7,14,30,.94));
                      min-height:250px;box-shadow:0 0 26px rgba(64,255,70,.12);color:#f8fbff;">
            <div style="font-size:18px;color:#c4d1dc;font-weight:900;letter-spacing:.3px;">
              {t['result_title']}
            </div>
            <div style="display:flex;align-items:center;gap:14px;flex-wrap:wrap;margin:12px 0 10px;">
              <div id="priceText" style="font-size:78px;line-height:1;color:#80ff67;font-weight:950;letter-spacing:-3px;">
                ${copy_value}
              </div>
              <button onclick="copyPrice()" title="{t['copy_button']}"
                style="cursor:pointer;border:1px solid #63ff62;background:rgba(33,95,42,.55);
                       color:#7fff6c;border-radius:14px;padding:9px 14px;font-size:15px;font-weight:900;
                       box-shadow:0 0 12px rgba(99,255,98,.18);">
                {t['copy_button']}
              </button>
            </div>
            <div style="font-size:17px;color:#d9e6ea;max-width:420px;line-height:1.55;">
              {t['result_help']}
            </div>
            <div id="copyMsg" style="margin-top:8px;color:#7fff6c;font-weight:900;font-size:14px;min-height:18px;"></div>
          </div>
        </div>
        <script>
        function copyPrice() {{
          const val = "{copy_value}";
          const msg = document.getElementById('copyMsg');
          if (navigator.clipboard && window.isSecureContext) {{
            navigator.clipboard.writeText(val).then(function() {{
              msg.innerText = '{t['copied']}: ' + val;
            }}).catch(function() {{
              fallbackCopy(val, msg);
            }});
          }} else {{
            fallbackCopy(val, msg);
          }}
        }}
        function fallbackCopy(val, msg) {{
          const temp = document.createElement('input');
          temp.value = val;
          document.body.appendChild(temp);
          temp.focus();
          temp.select();
          try {{
            document.execCommand('copy');
            msg.innerText = '{t['copied']}: ' + val;
          }} catch(e) {{
            msg.innerText = 'Selecciona el precio y usa Ctrl+C';
          }}
          document.body.removeChild(temp);
        }}
        </script>
        """,
        height=315,
    )

m1, m2, m3, m4 = st.columns(4)
metrics = [
    (t["entry_cost"], f"${entry_cost:,.2f}"),
    (t["fees_total"], f"${total_fees:,.2f}"),
    (t["gross"], f"${gross_target:,.2f} ({gross_pct:.2f}%)"),
    (t["net"], f"${net_target:,.2f} ({net_pct:.2f}%)"),
]
for col, (label, val) in zip([m1, m2, m3, m4], metrics):
    with col:
        st.markdown(f'<div class="metric-card"><div class="metric-label">{label}</div><div class="metric-value">{val}</div></div>', unsafe_allow_html=True)

formula_text = (
    f"{t['base']}\n"
    f"{t['fee_adj']}\n"
    f"{t['exit']}\n\n"
    f"{t['calc']}: {premium:.2f} x (1 + {target_pct:.2f}/100) + {fee_adjustment:.4f} = {limit_price_raw:.4f}"
)
st.markdown(f'<div class="formula-card"><pre><b style="color:#6fff68">{t["formula"]}</b>\n{formula_text}</pre></div>', unsafe_allow_html=True)
st.markdown(f'<div class="footer">&copy; WLF Trading - {VERSION}</div>', unsafe_allow_html=True)
