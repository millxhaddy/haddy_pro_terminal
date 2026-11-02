"""Threshold-based portfolio monitoring alerts."""

import math

import pandas as pd
import streamlit as st


def evaluate_holding_risks(
    holdings: pd.DataFrame,
    drawdown_threshold_pct: float = 10.0,
    concentration_threshold_pct: float = 30.0,
) -> list[dict]:
    """Return drawdown and equity-position concentration alerts."""
    if not isinstance(holdings, pd.DataFrame):
        raise TypeError("holdings mesti berupa pandas DataFrame.")

    required_columns = {"Ticker", "Nilai_Semasa_MYR", "ROI_Pct"}
    missing_columns = required_columns.difference(holdings.columns)
    if missing_columns:
        raise ValueError(f"Lajur pegangan tiada: {', '.join(sorted(missing_columns))}")
    if holdings.empty:
        return []

    if not math.isfinite(drawdown_threshold_pct) or not 0 < drawdown_threshold_pct <= 100:
        raise ValueError("Ambang kerugian mesti antara 0 dan 100 peratus.")
    if not math.isfinite(concentration_threshold_pct) or not 0 < concentration_threshold_pct <= 100:
        raise ValueError("Ambang kepekatan mesti antara 0 dan 100 peratus.")

    values = pd.to_numeric(holdings["Nilai_Semasa_MYR"], errors="coerce")
    returns = pd.to_numeric(holdings["ROI_Pct"], errors="coerce")
    valid_rows = []
    for (index, row), value, return_pct in zip(
        holdings.iterrows(), values.tolist(), returns.tolist()
    ):
        if (
            pd.notna(value)
            and pd.notna(return_pct)
            and math.isfinite(float(value))
            and math.isfinite(float(return_pct))
            and float(value) > 0
        ):
            valid_rows.append((index, row, float(value), float(return_pct)))
    if not valid_rows:
        raise ValueError("Tiada pegangan dengan nilai pasaran dan ROI yang sah untuk dinilai.")

    total_equity_value = sum(value for _, _, value, _ in valid_rows)
    alerts = []
    for _, row, market_value, roi_pct in valid_rows:
        ticker = str(row["Ticker"]).strip() or "Pegangan tanpa ticker"
        concentration_pct = market_value / total_equity_value * 100

        if roi_pct <= -drawdown_threshold_pct:
            severity = "Tinggi" if roi_pct <= -(drawdown_threshold_pct * 1.5) else "Perhatian"
            alerts.append(
                {
                    "severity": severity,
                    "ticker": ticker,
                    "type": "Kerugian berbanding kos",
                    "message": (
                        f"ROI {roi_pct:.2f}% telah melepasi ambang "
                        f"-{drawdown_threshold_pct:.1f}%."
                    ),
                }
            )

        if concentration_pct >= concentration_threshold_pct:
            alerts.append(
                {
                    "severity": "Perhatian",
                    "ticker": ticker,
                    "type": "Kepekatan pegangan",
                    "message": (
                        f"{concentration_pct:.1f}% daripada nilai semua pegangan saham "
                        f"berbanding ambang {concentration_threshold_pct:.1f}%."
                    ),
                }
            )

    severity_order = {"Tinggi": 0, "Perhatian": 1}
    alerts.sort(key=lambda alert: severity_order[alert["severity"]])
    return alerts


def render_holding_risk_alerts(
    holdings: pd.DataFrame,
    drawdown_threshold_pct: float,
    concentration_threshold_pct: float,
) -> None:
    """Render portfolio monitoring alerts without suggesting trades."""
    if not isinstance(holdings, pd.DataFrame) or holdings.empty:
        with st.expander("Amaran risiko pegangan", expanded=True):
            st.warning("Data pegangan yang sah belum tersedia; amaran risiko tidak dapat dikira.")
        return

    try:
        alerts = evaluate_holding_risks(
            holdings,
            drawdown_threshold_pct=drawdown_threshold_pct,
            concentration_threshold_pct=concentration_threshold_pct,
        )
    except ValueError as exc:
        with st.expander("Amaran risiko pegangan", expanded=True):
            st.error(f"Amaran tidak dapat dikira: {exc}")
        return

    with st.expander("Amaran risiko pegangan", expanded=bool(alerts)):
        st.caption(
            "Petunjuk pemantauan sahaja, bukan arahan beli/jual. "
            "Kepekatan dikira daripada nilai pegangan saham yang tersedia, "
            "bukan jumlah portfolio termasuk tunai."
        )
        st.caption(
            "Harga dan ROI bergantung pada snapshot pegangan aplikasi; "
            "amaran ini tidak mengesahkan sebut harga masa nyata."
        )
        if not alerts:
            st.success("Tiada ambang kerugian atau kepekatan yang dicetuskan.")
            return

        for alert in alerts:
            with st.container(border=True):
                if alert["severity"] == "Tinggi":
                    st.error("Risiko tinggi", icon="🚨")
                else:
                    st.warning("Perhatian", icon="⚠️")
                st.text(f"{alert['ticker']} · {alert['type']}: {alert['message']}")
