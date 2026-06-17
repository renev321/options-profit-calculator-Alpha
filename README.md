# WLF Options Profit Calculator

A compact Streamlit app for calculating the **SELL TO CLOSE** limit price for options.

## Main idea

The limit order price is the option premium price you type into the broker, not the x100 contract value.

```text
Base limit = Entry premium × (1 + Target % / 100)
Round-trip fee = Fee per side × 2
Fee adjustment = Round-trip fee / 100
Sell to close limit = Base limit + Fee adjustment
```

The `/100` converts contract-level dollar fees into option premium units.

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Default settings

- Broker: IBKR
- Contracts: 1
- Target: 35%
- Fee presets can be edited directly in `app.py`.
