from __future__ import annotations

from pathlib import Path
import base64
import math

import streamlit as st

APP_DIR = Path(__file__).parent
ASSETS = APP_DIR / "assets"
CONTRACT_MULTIPLIER = 100

BROKERS = {
    "IBKR": {
        "name": "IBKR",
        "fee_per_side": 0.65,
        "logo": "ibkr.png",
        "note": "Default preset. IBKR can vary by plan/routing, so adjust if needed.",
    },
    "Charles Schwab": {
        "name": "Charles Schwab",
        "fee_per_side": 0.65,
        "logo": "schwab.png",
        "note": "Standard preset.",
    },
    "E*TRADE": {
        "name": "E*TRADE",
        "fee_per_side": 0.65,
        "logo": "etrade.png",
        "note": "Standard preset. Use Custom if you qualify for another rate.",
    },
    "Custom": {
        "name": "Custom",
        "fee_per_side": 0.00,
        "logo": None,
        "note": "Enter your own fee per contract, per side.",
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
            --wlf-green: #6ee75b;
            --wlf-green-soft: rgba(110, 231, 91, .16);
            --wlf-cyan: #22d3ee;
            --card: rgba(15, 23, 42, .72);
            --border: rgba(148, 163, 184, .22);
            --text-soft: rgba(226, 232, 240, .72);
        }

        .stApp {
            background:
                radial-gradient(circle at 50% 0%, rgba(34, 197, 94, .16), transparent 34%),
                radial-gradient(circle at 10% 20%, rgba(34, 211, 238, .08), transparent 26%),
                linear-gradient(135deg, #020617 0%, #07111f 45%, #020617 100%);
            color: #e5e7eb;
        }

        .block-container {
            padding-top: 1.1rem !important;
            padding-bottom: 1rem !important;
            max-width: 1120px !important;
        }

        div[data-testid="stVerticalBlock"] { gap: .7rem; }

        .wlf-header {
            text-align: center;
            padding: .25rem 0 .35rem;
        }

        .wlf-logo {
            height: 74px;
            object-fit: contain;
            margin-bottom: .2rem;
        }

        .wlf-title {
            margin: 0;
            font-size: clamp(2rem, 4vw, 3.25rem);
            font-weight: 850;
            letter-spacing: -.04em;
            color: white;
        }

        .wlf-subtitle {
            margin-top: .2rem;
            color: var(--text-soft);
            font-size: 1.05rem;
        }

        .green { color: var(--wlf-green); }
        .cyan { color: var(--wlf-cyan); }

        .section-card {
            border: 1px solid var(--border);
            background: linear-gradient(180deg, rgba(15, 23, 42, .72), rgba(2, 6, 23, .62));
            border-radius: 22px;
            padding: 1rem;
            box-shadow: 0 12px 40px rgba(0,0,0,.22);
        }

        .mini-label {
            color: var(--text-soft);
            font-size: .86rem;
            margin-bottom: .25rem;
        }

        .broker-preview {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 1rem;
            border: 1px solid rgba(110, 231, 91, .36);
            background: linear-gradient(135deg, rgba(34,197,94,.13), rgba(15,23,42,.45));
            border-radius: 18px;
            padding: .75rem .9rem;
            min-height: 86px;
        }

        .broker-left {
            display: flex;
            align-items: center;
            gap: .85rem;
        }

        .broker-logo {
            width: 58px;
            height: 58px;
            object-fit: contain;
            border-radius: 12px;
            background: rgba(255,255,255,.96);
            padding: .35rem;
        }

        .broker-name {
            color: white;
            font-weight: 800;
            font-size: 1.15rem;
        }

        .broker-note {
            color: var(--text-soft);
            font-size: .8rem;
            max-width: 420px;
            margin-top: .1rem;
        }

        .fee-pill {
            border: 1px solid rgba(110,231,91,.4);
            background: rgba(110,231,91,.12);
            border-radius: 999px;
            padding: .55rem .85rem;
            color: var(--wlf-green);
            font-weight: 800;
            white-space: nowrap;
        }

        .result-card {
            border: 1px solid rgba(110, 231, 91, .75);
            background:
                radial-gradient(circle at 15% 50%, rgba(110,231,91,.20), transparent 30%),
                linear-gradient(135deg, rgba(6, 78, 59, .42), rgba(2, 6, 23, .72));
            border-radius: 26px;
            padding: 1.25rem 1.4rem;
            box-shadow: 0 0 32px rgba(110,231,91,.16);
        }

        .result-title {
            color: var(--text-soft);
            font-size: 1.05rem;
            font-weight: 650;
        }

        .result-number {
            color: var(--wlf-green);
            font-size: clamp(3rem, 7vw, 5.4rem);
            font-weight: 900;
            letter-spacing: -.05em;
            line-height: .95;
            margin-top: .15rem;
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
            padding: .8rem .85rem;
        }

        .metric-name {
            color: var(--text-soft);
            font-size: .82rem;
            margin-bottom: .25rem;
        }

        .metric-value {
            color: white;
            font-size: 1.25rem;
            font-weight: 800;
        }

        .formula-card {
            border: 1px solid var(--border);
            background: rgba(2,6,23,.42);
            border-radius: 18px;
            padding: .85rem 1rem;
            color: #dbeafe;
            font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", monospace;
            font-size: .88rem;
        }

        .copyright {
            text-align: center;
            color: rgba(226, 232, 240, .55);
            font-size: .85rem;
            padding: .5rem 0 0;
        }

        /* Compact Streamlit controls */
        div[data-testid="stNumberInput"] input {
            background: rgba(2,6,23,.55);
            border: 1px solid rgba(148,163,184,.25);
            color: white;
            border-radius: 12px;
        }
        div[data-testid="stNumberInput"] label,
        div[data-testid="stRadio"] label,
        div[data-testid="stCheckbox"] label {
            color: rgba(226,232,240,.82) !important;
            font-weight: 600;
        }
        div[role="radiogroup"] {
            gap: .35rem;
        }
        div[role="radiogroup"] label {
            border: 1px solid rgba(148,163,184,.25);
            background: rgba(15,23,42,.55);
            border-radius: 14px;
            padding: .45rem .65rem;
            margin-right: .15rem;
        }

        @media (max-width: 760px) {
            .metric-row { grid-template-columns: 1fr 1fr; }
            .broker-preview { align-items: flex-start; flex-direction: column; }
            .fee-pill { align-self: flex-start; }
            .wlf-logo { height: 58px; }
        }
    </style>
    """,
    unsafe_allow_html=True,
)

wlf_logo_b64 = image_to_base64(ASSETS / "wlf_trading.png")
if wlf_logo_b64:
    logo_html = f'<img class="wlf-logo" src="data:image/png;base64,{wlf_logo_b64}" alt="WLF Trading logo" />'
else:
    logo_html = '<div class="wlf-title green">WLF</div>'

st.markdown(
    f"""
    <div class="wlf-header">
        {logo_html}
        <h1 class="wlf-title">Options Profit Calculator</h1>
        <div class="wlf-subtitle">Compact <span class="green">SELL TO CLOSE</span> limit-price calculator</div>
    </div>
    """,
    unsafe_allow_html=True,
)

# Defaults
if "broker" not in st.session_state:
    st.session_state.broker = "IBKR"

left, right = st.columns([1.38, 1], gap="large")

with left:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    broker = st.radio(
        "Broker fee preset",
        list(BROKERS.keys()),
        index=list(BROKERS.keys()).index(st.session_state.broker),
        horizontal=True,
        label_visibility="visible",
    )
    st.session_state.broker = broker
    broker_info = BROKERS[broker]

    logo_name = broker_info["logo"]
    logo_b64 = image_to_base64(ASSETS / logo_name) if logo_name else ""
    if logo_b64:
        broker_logo_html = f'<img class="broker-logo" src="data:image/png;base64,{logo_b64}" alt="{broker_info["name"]} logo" />'
    else:
        broker_logo_html = '<div class="broker-logo" style="display:flex;align-items:center;justify-content:center;color:#94a3b8;font-size:1.8rem;">⚙️</div>'

    if broker == "Custom":
        fee_per_side = st.number_input(
            "Custom fee per contract, per side ($)",
            min_value=0.0,
            value=0.65,
            step=0.01,
            format="%.2f",
        )
    else:
        fee_per_side = broker_info["fee_per_side"]

    st.markdown(
        f"""
        <div class="broker-preview">
            <div class="broker-left">
                {broker_logo_html}
                <div>
                    <div class="broker-name">{broker_info['name']}</div>
                    <div class="broker-note">{broker_info['note']}</div>
                </div>
            </div>
            <div class="fee-pill">${fee_per_side:.2f} / side</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    c1, c2, c3 = st.columns(3)
    with c1:
        contracts = st.number_input("Contracts", min_value=1, max_value=999, value=1, step=1)
    with c2:
        entry_premium = st.number_input("Entry premium ($)", min_value=0.01, value=2.50, step=0.01, format="%.2f")
    with c3:
        target_percent = st.number_input("Target profit (%)", min_value=0.0, max_value=10000.0, value=35.0, step=1.0, format="%.2f")

    t1, t2 = st.columns(2)
    with t1:
        include_fees = st.toggle("Include fees", value=True)
    with t2:
        round_limit = st.toggle("Round up to $0.01", value=True)
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
            <div class="result-title">SELL TO CLOSE limit price</div>
            <div class="result-number">${sell_limit:.2f}</div>
            <div class="result-sub">This is the option premium price you type into your broker.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown(
    f"""
    <div class="metric-row">
        <div class="metric-box">
            <div class="metric-name">Entry cost</div>
            <div class="metric-value">${entry_cost:,.2f}</div>
        </div>
        <div class="metric-box">
            <div class="metric-name">Total fees</div>
            <div class="metric-value">${total_fees:,.2f}</div>
        </div>
        <div class="metric-box">
            <div class="metric-name">Gross target</div>
            <div class="metric-value">${gross_profit:,.2f} <span class="green">({gross_profit_pct:.2f}%)</span></div>
        </div>
        <div class="metric-box">
            <div class="metric-name">Net target</div>
            <div class="metric-value">${net_profit:,.2f} <span class="green">({net_profit_pct:.2f}%)</span></div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    f"""
    <div class="formula-card">
        <b class="green">Formula</b><br>
        Base limit = Entry premium × (1 + Target % / 100)<br>
        Fee adjustment = Round-trip fee per contract / 100<br>
        Sell to close limit = Base limit + Fee adjustment<br><br>
        Current calculation: {entry_premium:.2f} × (1 + {target_percent:.2f}/100) + {fee_adjustment:.4f} = {raw_limit:.4f}
    </div>
    <div class="copyright">© WLF Trading</div>
    """,
    unsafe_allow_html=True,
)
