from __future__ import annotations

from pathlib import Path
import base64
import math

import streamlit as st

APP_DIR = Path(__file__).parent
ASSETS = APP_DIR / "assets"
CONTRACT_MULTIPLIER = 100

BROKERS = {
    "IBKR": {"fee_per_side": 0.65, "logo": "ibkr.png"},
    "Charles Schwab": {"fee_per_side": 0.65, "logo": "schwab.png"},
    "E*TRADE": {"fee_per_side": 0.65, "logo": "etrade.png"},
    "Custom": {"fee_per_side": 0.00, "logo": None},
}

TXT = {
    "ES": {
        "app_title": "Calculadora de Ganancia en Opciones",
        "subtitle": "Calcula el precio límite para cerrar una operación con ganancia",
        "lang": "Idioma",
        "broker": "Broker",
        "fee": "Comisión",
        "fee_help": "Comisión por contrato, por lado. La app usa ida y vuelta: abrir + cerrar.",
        "custom_fee": "Comisión personalizada / lado ($)",
        "contracts": "Contratos",
        "entry": "Prima de entrada ($)",
        "target": "Objetivo (%)",
        "include_fees": "Incluir comisiones",
        "include_fees_help": "Suma la comisión de abrir + cerrar al precio límite de salida.",
        "round_tick": "Redondear a $0.01",
        "round_tick_help": "Redondea hacia arriba al centavo más cercano para que el objetivo cubra el cálculo.",
        "result_title": "Precio límite SELL TO CLOSE",
        "result_hint": "Este es el precio de prima que escribes en el broker.",
        "entry_cost": "Costo de entrada",
        "total_fees": "Comisiones totales",
        "gross": "Objetivo bruto",
        "net": "Objetivo neto",
        "formula": "Fórmula",
        "base": "Base = prima × (1 + objetivo / 100)",
        "fee_adj": "Ajuste comisión = comisión ida y vuelta / 100",
        "final": "Límite de salida = Base + Ajuste comisión",
        "calc": "Cálculo actual",
        "custom": "Personalizado",
        "side": "lado",
        "open_close": "abrir + cerrar",
    },
    "EN": {
        "app_title": "Options Profit Calculator",
        "subtitle": "Calculate the limit price to close an options trade in profit",
        "lang": "Language",
        "broker": "Broker",
        "fee": "Fee",
        "fee_help": "Fee per contract, per side. The app uses round trip: open + close.",
        "custom_fee": "Custom fee / side ($)",
        "contracts": "Contracts",
        "entry": "Entry premium ($)",
        "target": "Target (%)",
        "include_fees": "Include fees",
        "include_fees_help": "Adds the open + close fee to the exit limit price.",
        "round_tick": "Round to $0.01",
        "round_tick_help": "Rounds up to the nearest cent so the target covers the calculation.",
        "result_title": "SELL TO CLOSE limit price",
        "result_hint": "This is the premium price you type into your broker.",
        "entry_cost": "Entry cost",
        "total_fees": "Total fees",
        "gross": "Gross target",
        "net": "Net target",
        "formula": "Formula",
        "base": "Base = premium × (1 + target / 100)",
        "fee_adj": "Fee adjustment = round-trip fee / 100",
        "final": "Exit limit = Base + Fee adjustment",
        "calc": "Current calculation",
        "custom": "Custom",
        "side": "side",
        "open_close": "open + close",
    },
}


def image_to_base64(path: Path) -> str:
    if not path.exists():
        return ""
    return base64.b64encode(path.read_bytes()).decode("utf-8")


def round_to_tick(value: float, tick: float) -> float:
    if tick <= 0:
        return value
    return math.ceil(value / tick) * tick


st.set_page_config(
    page_title="WLF Options Profit Calculator",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
    <style>
        :root {
            --wlf-green: #78f25f;
            --wlf-cyan: #22d3ee;
            --bg-card: rgba(15, 23, 42, .64);
            --border: rgba(148, 163, 184, .24);
            --text-soft: rgba(226, 232, 240, .76);
        }

        .stApp {
            background:
                radial-gradient(circle at 50% 0%, rgba(34,197,94,.14), transparent 28%),
                radial-gradient(circle at 8% 25%, rgba(34,211,238,.08), transparent 26%),
                linear-gradient(135deg, #020617 0%, #07111f 45%, #020617 100%);
            color: #e5e7eb;
        }

        .block-container {
            padding-top: 2.1rem !important;
            padding-bottom: 1rem !important;
            max-width: 1120px !important;
        }

        div[data-testid="stVerticalBlock"] { gap: .55rem; }
        .green { color: var(--wlf-green); }
        .cyan { color: var(--wlf-cyan); }

        .topbar {
            display: flex;
            justify-content: center;
            align-items: center;
            margin-bottom: .15rem;
        }

        .wlf-logo {
            width: 116px;
            height: auto;
            display: block;
            filter: drop-shadow(0 0 14px rgba(120,242,95,.22));
        }

        .wlf-header {
            text-align: center;
            padding: .2rem 0 .45rem;
        }

        .wlf-title {
            margin: 0;
            font-size: clamp(2rem, 4vw, 3.15rem);
            font-weight: 850;
            letter-spacing: -.045em;
            color: white;
        }

        .wlf-subtitle {
            margin-top: .25rem;
            color: var(--text-soft);
            font-size: 1.05rem;
        }

        .section-card {
            border: 1px solid var(--border);
            background: linear-gradient(180deg, rgba(15, 23, 42, .70), rgba(2, 6, 23, .58));
            border-radius: 22px;
            padding: .9rem 1rem;
            box-shadow: 0 12px 40px rgba(0,0,0,.20);
        }

        .row-title {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: .8rem;
            margin-bottom: .45rem;
        }

        .row-title strong {
            color: #f8fafc;
            font-size: 1.05rem;
        }

        .fee-small {
            border: 1px solid rgba(120,242,95,.40);
            background: rgba(120,242,95,.11);
            border-radius: 999px;
            padding: .32rem .65rem;
            color: var(--wlf-green);
            font-weight: 800;
            font-size: .86rem;
            white-space: nowrap;
        }

        .broker-strip {
            display: flex;
            align-items: center;
            gap: .7rem;
            margin: .3rem 0 .7rem;
            color: var(--text-soft);
        }

        .broker-strip img {
            width: 34px;
            height: 34px;
            object-fit: contain;
            border-radius: 8px;
            background: rgba(255,255,255,.96);
            padding: .18rem;
        }

        .broker-selected-name {
            color: #ffffff;
            font-weight: 850;
            font-size: 1.08rem;
        }

        .input-caption {
            color: var(--text-soft);
            font-size: .85rem;
        }

        .result-card {
            border: 1px solid rgba(120,242,95,.76);
            background:
                radial-gradient(circle at 15% 50%, rgba(120,242,95,.20), transparent 30%),
                linear-gradient(135deg, rgba(6, 78, 59, .42), rgba(2, 6, 23, .72));
            border-radius: 26px;
            padding: 1.15rem 1.35rem;
            box-shadow: 0 0 32px rgba(120,242,95,.15);
            min-height: 218px;
            display: flex;
            flex-direction: column;
            justify-content: center;
        }

        .result-title {
            color: var(--text-soft);
            font-size: 1.08rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: .02em;
        }

        .result-number {
            color: var(--wlf-green);
            font-size: clamp(3rem, 7vw, 5.2rem);
            font-weight: 950;
            letter-spacing: -.05em;
            line-height: .95;
            margin-top: .18rem;
        }

        .result-sub {
            color: var(--text-soft);
            margin-top: .45rem;
            font-size: .95rem;
        }

        .metric-row {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: .7rem;
            margin-top: .7rem;
        }

        .metric-box {
            border: 1px solid var(--border);
            background: rgba(2, 6, 23, .38);
            border-radius: 16px;
            padding: .75rem .85rem;
        }

        .metric-name {
            color: var(--text-soft);
            font-size: .83rem;
            margin-bottom: .25rem;
        }

        .metric-value {
            color: white;
            font-size: 1.22rem;
            font-weight: 850;
        }

        .formula-card {
            border: 1px solid var(--border);
            background: rgba(2,6,23,.42);
            border-radius: 18px;
            padding: .85rem 1rem;
            color: #dbeafe;
            font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", monospace;
            font-size: .88rem;
            line-height: 1.55;
        }

        .copyright {
            text-align: center;
            color: rgba(226,232,240,.58);
            font-size: .86rem;
            padding: .5rem 0 0;
        }

        /* Make radio options look like clear toggle buttons */
        div[role="radiogroup"] {
            gap: .35rem !important;
        }
        div[role="radiogroup"] label {
            border: 1px solid rgba(148,163,184,.32) !important;
            background: rgba(15,23,42,.72) !important;
            border-radius: 14px !important;
            padding: .45rem .70rem !important;
            margin-right: .15rem !important;
            color: #f8fafc !important;
            min-height: 42px;
        }
        div[role="radiogroup"] label p {
            color: #f8fafc !important;
            font-weight: 800 !important;
            font-size: .96rem !important;
        }
        div[role="radiogroup"] input:checked + div p,
        div[role="radiogroup"] label:has(input:checked) p {
            color: var(--wlf-green) !important;
        }
        div[data-testid="stNumberInput"] input {
            background: rgba(2,6,23,.55);
            border: 1px solid rgba(148,163,184,.32);
            color: white;
            border-radius: 12px;
            font-weight: 700;
        }
        div[data-testid="stNumberInput"] label,
        div[data-testid="stRadio"] label,
        div[data-testid="stCheckbox"] label,
        div[data-testid="stToggle"] label {
            color: rgba(226,232,240,.90) !important;
            font-weight: 700 !important;
        }
        .st-emotion-cache-1gwvy71, .st-emotion-cache-16txtl3 { color: #f8fafc !important; }

        @media (max-width: 760px) {
            .metric-row { grid-template-columns: 1fr 1fr; }
            .result-card { min-height: 180px; }
            .wlf-logo { width: 92px; }
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Defaults
if "broker" not in st.session_state:
    st.session_state.broker = "IBKR"
if "language" not in st.session_state:
    st.session_state.language = "ES"

lang_col1, lang_col2, lang_col3 = st.columns([1, 1.2, 1])
with lang_col3:
    language_display = st.radio(
        "🌐 Language / Idioma",
        ["Español", "English"],
        index=0 if st.session_state.language == "ES" else 1,
        horizontal=True,
        label_visibility="collapsed",
    )
st.session_state.language = "ES" if language_display == "Español" else "EN"
t = TXT[st.session_state.language]

wlf_logo_b64 = image_to_base64(ASSETS / "wlf_trading_cropped.png") or image_to_base64(ASSETS / "wlf_trading.png")
if wlf_logo_b64:
    logo_html = f'<img class="wlf-logo" src="data:image/png;base64,{wlf_logo_b64}" alt="WLF Trading logo" />'
else:
    logo_html = '<div class="wlf-title green">WLF</div>'

st.markdown(
    f"""
    <div class="topbar">{logo_html}</div>
    <div class="wlf-header">
        <h1 class="wlf-title">{t['app_title']}</h1>
        <div class="wlf-subtitle">{t['subtitle']} · <span class="green">SELL TO CLOSE</span></div>
    </div>
    """,
    unsafe_allow_html=True,
)

left, right = st.columns([1.45, 1], gap="large")

with left:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)

    broker_options = list(BROKERS.keys())
    broker = st.radio(
        t["broker"],
        broker_options,
        index=broker_options.index(st.session_state.broker),
        horizontal=True,
        label_visibility="visible",
    )
    st.session_state.broker = broker
    broker_info = BROKERS[broker]

    if broker == "Custom":
        fee_per_side = st.number_input(
            t["custom_fee"],
            min_value=0.0,
            value=0.65,
            step=0.01,
            format="%.2f",
            help=t["fee_help"],
        )
    else:
        fee_per_side = broker_info["fee_per_side"]

    logo_name = broker_info["logo"]
    logo_b64 = image_to_base64(ASSETS / logo_name) if logo_name else ""
    logo_html = (
        f'<img src="data:image/png;base64,{logo_b64}" alt="{broker} logo" />'
        if logo_b64
        else '<span style="font-size:1.6rem">⚙️</span>'
    )

    st.markdown(
        f"""
        <div class="broker-strip">
            {logo_html}
            <div class="broker-selected-name">{broker if broker != 'Custom' else t['custom']}</div>
            <div class="fee-small">{t['fee']}: ${fee_per_side:.2f} / {t['side']}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    c1, c2, c3 = st.columns(3)
    with c1:
        contracts = st.number_input(t["contracts"], min_value=1, max_value=999, value=1, step=1)
    with c2:
        entry_premium = st.number_input(t["entry"], min_value=0.01, value=2.50, step=0.01, format="%.2f")
    with c3:
        target_percent = st.number_input(t["target"], min_value=0.0, max_value=10000.0, value=35.0, step=1.0, format="%.2f")

    t1, t2 = st.columns(2)
    with t1:
        include_fees = st.toggle(t["include_fees"], value=True, help=t["include_fees_help"])
    with t2:
        round_limit = st.toggle(t["round_tick"], value=True, help=t["round_tick_help"])

    st.markdown('</div>', unsafe_allow_html=True)

# Calculations
base_limit = entry_premium * (1 + target_percent / 100)
round_trip_fee_per_contract = fee_per_side * 2
fee_adjustment = (round_trip_fee_per_contract / CONTRACT_MULTIPLIER) if include_fees else 0.0
raw_limit = base_limit + fee_adjustment
sell_limit = round_to_tick(raw_limit, 0.01) if round_limit else raw_limit

entry_cost = entry_premium * CONTRACT_MULTIPLIER * contracts
sell_value = sell_limit * CONTRACT_MULTIPLIER * contracts
total_fees = round_trip_fee_per_contract * contracts if include_fees else 0.0
gross_profit = sell_value - entry_cost
net_profit = gross_profit - total_fees
net_profit_pct = (net_profit / entry_cost) * 100 if entry_cost else 0.0
gross_profit_pct = (gross_profit / entry_cost) * 100 if entry_cost else 0.0

with right:
    st.markdown(
        f"""
        <div class="result-card">
            <div class="result-title">{t['result_title']}</div>
            <div class="result-number">${sell_limit:.2f}</div>
            <div class="result-sub">{t['result_hint']}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown(
    f"""
    <div class="metric-row">
        <div class="metric-box">
            <div class="metric-name">{t['entry_cost']}</div>
            <div class="metric-value">${entry_cost:,.2f}</div>
        </div>
        <div class="metric-box">
            <div class="metric-name">{t['total_fees']}</div>
            <div class="metric-value">${total_fees:,.2f}</div>
        </div>
        <div class="metric-box">
            <div class="metric-name">{t['gross']}</div>
            <div class="metric-value">${gross_profit:,.2f} <span class="green">({gross_profit_pct:.2f}%)</span></div>
        </div>
        <div class="metric-box">
            <div class="metric-name">{t['net']}</div>
            <div class="metric-value">${net_profit:,.2f} <span class="green">({net_profit_pct:.2f}%)</span></div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    f"""
    <div class="formula-card">
        <b class="green">{t['formula']}</b><br>
        {t['base']}<br>
        {t['fee_adj']} <span style="color:rgba(226,232,240,.62)">({t['open_close']})</span><br>
        {t['final']}<br><br>
        {t['calc']}: {entry_premium:.2f} × (1 + {target_percent:.2f}/100) + {fee_adjustment:.4f} = {raw_limit:.4f}
    </div>
    <div class="copyright">© WLF Trading</div>
    """,
    unsafe_allow_html=True,
)
