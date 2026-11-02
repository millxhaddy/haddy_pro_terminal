"""Google Sheets-backed decision tables and risk/reward comparison."""

import pandas as pd
import plotly.graph_objects as go

from pipeline_cleaner import clean_currency, clean_ratio


DECISION_COLUMNS = ["Ticker", "Harga_Rujukan", "SL", "TP", "RR", "Status"]
TICKER_TERMS = ("ticker", "simbol", "kod", "kaunter", "saham", "stock", "symbol")
INVALID_TICKERS = {
    "", "nan", "none", "-", "n/a", "#n/a", "#ref!", "#error!", "#value!",
    "ticker", "simbol", "kod", "kaunter", "jumlah", "total", "purata",
}


def _find_column(
    dataframe: pd.DataFrame,
    terms: tuple[str, ...],
    exclude: tuple[str, ...] = (),
    occurrence: int = 0,
):
    matches = [
        column
        for column in dataframe.columns
        if any(
            term in str(column).strip().lower().replace("_", " ")
            for term in terms
        )
        and not any(
            term in str(column).strip().lower().replace("_", " ")
            for term in exclude
        )
    ]
    if not matches:
        return None
    return matches[min(occurrence, len(matches) - 1)]


def _extract_subtable_from_raw_rows(raw_rows: list, market: str = "bursa") -> pd.DataFrame:
    """Fallback terus daripada _raw_rows_meja_keputusan jika top10_bursa/top10_us kosong."""
    if not isinstance(raw_rows, list) or not raw_rows:
        return pd.DataFrame()

    header_rows = []
    for idx, row in enumerate(raw_rows):
        cells_lower = [str(c).strip().lower() for c in row]
        ticker_positions = [
            col_idx
            for col_idx, cell in enumerate(cells_lower)
            if any(
                cell == term or cell.startswith(f"{term} ") or f" {term}" in cell
                for term in TICKER_TERMS
            )
        ]
        if ticker_positions:
            header_rows.append((idx, ticker_positions, row))

    if not header_rows:
        return pd.DataFrame()

    # Kes 1: Jadual Bursa & US bersebelahan pada baris pengepala yang sama (>= 2 lajur Ticker)
    first_hdr_idx, ticker_pos, hdr_row = header_rows[0]
    if len(ticker_pos) >= 2 and len(header_rows) == 1:
        split_col = ticker_pos[1]
        if market == "bursa":
            sub_headers = [str(c).strip() or f"Col_{i}" for i, c in enumerate(hdr_row[:split_col])]
            sub_data = [
                r[:split_col] + [""] * max(0, split_col - len(r))
                for r in raw_rows[first_hdr_idx + 1 : first_hdr_idx + 16]
            ]
        else:
            start_col = max(0, split_col - 1)
            sub_headers = [str(c).strip() or f"Col_{i}" for i, c in enumerate(hdr_row[start_col:])]
            sub_data = [
                r[start_col:] + [""] * max(0, len(sub_headers) - len(r[start_col:]))
                for r in raw_rows[first_hdr_idx + 1 : first_hdr_idx + 16]
            ]
        return pd.DataFrame(sub_data, columns=sub_headers)

    # Kes 2: Jadual Bursa & US bertindih secara menegak (Stacked)
    target_hdr_idx = None
    for idx, _, row in header_rows:
        joined_lower = " ".join(str(c).lower() for c in row)
        if market == "bursa" and ("rm" in joined_lower or "bursa" in joined_lower or "myr" in joined_lower):
            target_hdr_idx = idx
            break
        if market == "us" and ("usd" in joined_lower or "us" in joined_lower or "$" in joined_lower):
            target_hdr_idx = idx
            break

    if target_hdr_idx is None:
        if market == "bursa":
            target_hdr_idx = header_rows[0][0]
        elif len(header_rows) > 1:
            target_hdr_idx = header_rows[1][0]
        else:
            return pd.DataFrame()

    raw_hdr = raw_rows[target_hdr_idx]
    headers = []
    seen = {}
    for i, h in enumerate(raw_hdr):
        clean_h = str(h).strip() or f"Col_{i+1}"
        if clean_h in seen:
            seen[clean_h] += 1
            clean_h = f"{clean_h}_{seen[clean_h]}"
        else:
            seen[clean_h] = 1
        headers.append(clean_h)

    data_rows = []
    for r in raw_rows[target_hdr_idx + 1 : target_hdr_idx + 16]:
        if not any(str(c).strip() for c in r):
            if data_rows:
                break
            continue
        joined_r = " ".join(str(c).lower() for c in r)
        if any(str(c).strip().lower() in {"ticker", "simbol"} for c in r) and ("usd" in joined_r or "rm" in joined_r):
            break
        padded = list(r[: len(headers)]) + [""] * max(0, len(headers) - len(r))
        data_rows.append(padded)

    return pd.DataFrame(data_rows, columns=headers) if data_rows else pd.DataFrame()


def _parse_candidate_dataframe(source: pd.DataFrame, ticker_index: int = 0) -> pd.DataFrame:
    if source is None or not isinstance(source, pd.DataFrame) or source.empty:
        return pd.DataFrame(columns=DECISION_COLUMNS)

    ticker_columns = [
        column
        for column in source.columns
        if any(term in str(column).lower() for term in TICKER_TERMS)
    ]
    if not ticker_columns:
        return pd.DataFrame(columns=DECISION_COLUMNS)

    occ = min(ticker_index, len(ticker_columns) - 1)
    ticker_col = ticker_columns[occ]
    price_col = _find_column(
        source,
        ("harga rujukan", "harga semasa", "harga live", "harga", "price", "entry"),
        ("stop", "sasaran", "target", "sl", "tp"),
        occurrence=occ,
    )
    stop_col = _find_column(
        source,
        ("stop loss", "stop-loss", " sl", "henti rugi", "sl", "cut loss"),
        occurrence=occ,
    )
    target_col = _find_column(
        source,
        ("sasaran", "take profit", "target", " tp", "tp"),
        occurrence=occ,
    )
    rr_col = _find_column(
        source,
        ("nisbah r:r", "r:r", "risk reward", "rr"),
        occurrence=occ,
    )
    status_col = _find_column(
        source,
        ("keputusan akhir", "keputusan", "status", "tindakan", "signal", "isyarat"),
        occurrence=occ,
    )

    normalized = pd.DataFrame()
    normalized["Ticker"] = source[ticker_col].astype(str).str.strip()
    normalized["Harga_Rujukan"] = (
        source[price_col].map(clean_currency) if price_col else pd.NA
    )
    normalized["SL"] = source[stop_col].map(clean_currency) if stop_col else pd.NA
    normalized["TP"] = source[target_col].map(clean_currency) if target_col else pd.NA
    normalized["RR"] = source[rr_col].map(clean_ratio) if rr_col else pd.NA
    normalized["Status"] = (
        source[status_col].astype(str).str.strip() if status_col else "Tidak dinyatakan"
    )

    normalized = normalized[
        ~normalized["Ticker"].str.lower().isin(INVALID_TICKERS)
        & ~normalized["Ticker"].str.lower().str.startswith(("jadual", "meja", "nota", "top "))
    ]
    return normalized[DECISION_COLUMNS].head(10).reset_index(drop=True)


def _normalize_decision_table(
    vault_data: dict,
    keys: tuple[str, ...],
    ticker_index: int = 0,
    market: str = "bursa",
):
    if not isinstance(vault_data, dict):
        return pd.DataFrame(columns=DECISION_COLUMNS)

    candidates = []
    for key in keys:
        df_cand = vault_data.get(key)
        if isinstance(df_cand, pd.DataFrame) and not df_cand.empty:
            candidates.append((df_cand, 0))

    raw_rows = vault_data.get("_raw_rows_meja_keputusan", [])
    raw_extracted = _extract_subtable_from_raw_rows(raw_rows, market=market)
    if not raw_extracted.empty:
        candidates.append((raw_extracted, 0))

    for fallback_key in ("meja_keputusan", "01_Meja Keputusan", "top10_bursa"):
        fb_df = vault_data.get(fallback_key)
        if isinstance(fb_df, pd.DataFrame) and not fb_df.empty:
            candidates.append((fb_df, ticker_index))

    for cand_df, idx_to_use in candidates:
        result = _parse_candidate_dataframe(cand_df, ticker_index=idx_to_use)
        if not result.empty:
            return result

    return pd.DataFrame(columns=DECISION_COLUMNS)


def get_top10_bursa(vault_data: dict) -> pd.DataFrame:
    """Return Bursa decisions only when an actual decision table is present in Sheets."""
    return _normalize_decision_table(
        vault_data,
        ("top10_bursa", "bursa_top10"),
        ticker_index=0,
        market="bursa",
    )


def get_top10_us(vault_data: dict) -> pd.DataFrame:
    """Return US decisions only when an actual decision table is present in Sheets."""
    return _normalize_decision_table(
        vault_data,
        ("top10_us", "us_top10"),
        ticker_index=1,
        market="us",
    )


def render_rr_comparison_chart(df_bursa: pd.DataFrame, df_us: pd.DataFrame):
    """Plot risk/reward values supplied by the decision-sheet snapshot."""
    fig = go.Figure()
    for dataframe, name, color in (
        (df_bursa, "Bursa Malaysia", "#00E676"),
        (df_us, "Wall Street US", "#29B6F6"),
    ):
        if dataframe is None or dataframe.empty or not {"Ticker", "RR"}.issubset(dataframe.columns):
            continue
        values = pd.to_numeric(dataframe["RR"], errors="coerce")
        valid = values.notna()
        if valid.any():
            fig.add_trace(
                go.Bar(
                    y=dataframe.loc[valid, "Ticker"].astype(str),
                    x=values[valid],
                    name=name,
                    orientation="h",
                    marker_color=color,
                )
            )

    if not fig.data:
        fig.add_annotation(
            text="Tiada nisbah risiko/ganjaran sah daripada tab keputusan Google Sheets.",
            x=0.5,
            y=0.5,
            xref="paper",
            yref="paper",
            showarrow=False,
        )
    else:
        fig.add_vline(
            x=2.5,
            line_dash="dash",
            line_color="#FFBB28",
            annotation_text="Rujukan 2.50x",
            annotation_position="top right",
        )
    fig.update_layout(
        title="Nisbah Risiko/Ganjaran daripada snapshot Sheets",
        template="plotly_dark",
        paper_bgcolor="#141824",
        plot_bgcolor="#141824",
        height=420,
        barmode="group",
        xaxis_title="Nisbah R:R",
    )
    return fig