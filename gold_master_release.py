"""Source-backed operational and portfolio summary."""

import pandas as pd
import streamlit as st


def render_gold_master_dashboard(kpis: dict, vault_data: dict, fx_rate: float = 4.0773):
    st.header("Ringkasan Data & Audit Operasi")
    st.caption(
        "Ringkasan ini melaporkan data yang diterima aplikasi; ia bukan pengesahan "
        "bank, broker, audit kewangan, pematuhan Syariah atau pensijilan keselamatan."
    )

    metadata = (vault_data or {}).get("_sync_metadata", {})
    source_tier = metadata.get("source_tier", "Sumber tidak diketahui")
    remote_data_confirmed = bool(metadata.get("remote_data_confirmed"))
    columns = st.columns(4)
    columns[0].metric("Sumber", str(source_tier))
    columns[1].metric("Tab berisi data", int(metadata.get("tabs_loaded", 0) or 0))
    columns[2].metric("Tab dari cache setempat", int(metadata.get("cached_tabs", 0) or 0))
    columns[3].metric(
        "Tarikan aplikasi terakhir",
        str(metadata.get("timestamp") or "Tidak tersedia"),
    )

    if not remote_data_confirmed:
        st.warning(
            "Tarikan jauh tidak disahkan. Nilai yang kelihatan mungkin berasal daripada "
            "snapshot sesi lama atau cache setempat."
        )
    elif metadata.get("cached_tabs"):
        st.warning("Sambungan jauh berjaya, tetapi sebahagian tab datang daripada cache.")

    data_status, statement = st.tabs(["Sumber per tab", "Metrik portfolio tersedia"])
    with data_status:
        tab_sources = metadata.get("tab_sources", {})
        cache_timestamps = metadata.get("tab_cache_timestamps", {})
        if tab_sources:
            st.dataframe(
                pd.DataFrame(
                    [
                        {
                            "Alias": alias,
                            "Sumber": source,
                            "Masa cache": cache_timestamps.get(alias, "—"),
                        }
                        for alias, source in tab_sources.items()
                    ]
                ),
                width="stretch",
                hide_index=True,
            )
        else:
            st.info("Metadata sumber tab tidak tersedia.")

    with statement:
        labels = {
            "total_deposit": "Deposit selesai (MYR)",
            "total_withdrawal": "Pengeluaran selesai (MYR)",
            "net_invested": "Modal bersih daripada rekod aliran tunai (MYR)",
            "active_portfolio_val": "Nilai pasaran pegangan (MYR)",
            "unrealized_pnl": "Untung/rugi belum realisasi (MYR)",
            "unrealized_roi_pct": "ROI pegangan belum realisasi (%)",
            "total_trades": "Rekod jurnal yang tersedia",
        }
        rows = [
            {
                "Metrik": label,
                "Nilai": kpis.get(key) if kpis.get(key) is not None else "Tidak tersedia",
            }
            for key, label in labels.items()
        ]
        st.dataframe(pd.DataFrame(rows), width="stretch", hide_index=True)
        st.caption(
            "Nilai USD dalam pegangan ditukar menggunakan kadar manual aplikasi "
            f"(USD/MYR {fx_rate:.4f}); kadar ini bukan suapan FX langsung."
        )
