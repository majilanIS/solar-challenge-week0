import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Try to import load_country_data safely
try:
    from app.utils import load_country_data
except Exception:
    try:
        from utils import load_country_data
    except Exception as e:
        st.error(f"Could not import load_country_data from utils: {e}")
        raise

# --- PAGE CONFIG ---
st.set_page_config(page_title="Solar Dashboard", layout="wide", page_icon="☀️")
st.title("☀️ Solar Energy Interactive Dashboard")

# --- SIDEBAR ---
st.sidebar.header("🌍 Data Filters")

country_list = ["benin", "sierraleone", "togo"]
selected_country = st.sidebar.selectbox("Select Country", country_list)

# Define region options per country (fallback list for UI only)
region_options = {
    "benin": ["Cotonou", "Porto-Novo", "Parakou", "Abomey"],
    "sierraleone": ["Freetown", "Bo", "Kenema", "Makeni"],
    "togo": ["Lomé", "Sokodé", "Kara", "Atakpamé"]
}

# Regions update dynamically based on selected country
available_regions = region_options.get(selected_country, [])
selected_regions = st.sidebar.multiselect(
    "🏙️ Select Regions (optional)",
    options=available_regions,
    default=available_regions[:1],
)

# UI options: prefer attractive area charts; allow per-region small multiples
per_region = st.sidebar.checkbox("Show area chart per region (small multiples)", value=False)
downsample_limit = st.sidebar.slider("Max points to plot (approx)", 1000, 50000, 20000, step=1000)
# Option to show a comparative overview across all countries
show_compare = st.sidebar.checkbox("Show comparative overview across all countries", value=False)

# --- LOAD DATA ---
df = load_country_data(selected_country)
if df is None or (hasattr(df, 'empty') and df.empty):
    attempted = f"data/{selected_country.lower().replace(' ', '')}_clean.csv"
    st.error(f"No data found for {selected_country}. Tried: {attempted}")
else:
    # --- CLEAN AND PREP DATA ---
    df.columns = df.columns.str.strip().str.lower()
    column_map = {"timestamp": "date", "tamb": "temperature"}
    df.rename(columns={k: v for k, v in column_map.items() if k in df.columns}, inplace=True)

    ghi_col = next((c for c in df.columns if "ghi" in c), None)
    temp_col = "temperature" if "temperature" in df.columns else None
    date_col = "date" if "date" in df.columns else None
    region_col = next((c for c in df.columns if "region" in c), None)

    if date_col:
        df[date_col] = pd.to_datetime(df[date_col], errors="coerce")

    if ghi_col:
        df[ghi_col] = pd.to_numeric(df[ghi_col], errors="coerce")

    if temp_col:
        df[temp_col] = pd.to_numeric(df[temp_col], errors="coerce")

    # Filter by selected regions (if the dataset has a region column)
    if region_col and selected_regions:
        df = df[df[region_col].isin(selected_regions)]

    # Drop rows missing required plotting columns
    required = [date_col, ghi_col]
    plot_df = df.dropna(subset=[c for c in required if c is not None])

    if plot_df.empty:
        st.warning("No valid data available for the selected filters.")
    else:
        # Header with selected regions if any
        region_label = f" ({', '.join(selected_regions)})" if selected_regions else ""
        st.markdown(f"### 📊 Solar Metrics for **{selected_country.title()}**{region_label}")

        # --- SUMMARY METRICS ---
        if ghi_col:
            max_val = plot_df[ghi_col].max()
            avg_val = plot_df[ghi_col].mean()
            min_val = plot_df[ghi_col].min()

            # larger metric cards with spacing
            col1, col2, col3 = st.columns([1, 1, 1])
            col1.metric("🌞 Max GHI", f"{max_val:.2f}")
            col2.metric("🌑 Min GHI", f"{min_val:.2f}")
            col3.metric("📈 Avg GHI", f"{avg_val:.2f}")

        # Downsample for performance
        if len(plot_df) > downsample_limit:
            step = max(1, len(plot_df) // downsample_limit)
            plot_sample = plot_df.iloc[::step].copy()
            st.info(f"Data downsampled for plotting: showing ~{len(plot_sample)} points")
        else:
            plot_sample = plot_df

        # --- Chart selection built from available data ---
        chart_options = ["GHI Area"]
        if temp_col:
            chart_options.append("Temperature Area")
            chart_options.append("Bubble: GHI vs Temp")
        if date_col:
            chart_options.append("Line: GHI over Time")
        chart_options.append("All")

        # Dropdown removed — show all charts by default
        selected_chart = "All"

        # --- Render charts according to selection ---
        def show_area(df_source, y_col, title_suffix=""):
            if per_region and region_col:
                fig = px.area(
                    df_source,
                    x=date_col,
                    y=y_col,
                    facet_col=region_col,
                    facet_col_wrap=2,
                    title=f"{y_col.upper()} Area Chart Over Time{title_suffix}",
                    labels={date_col: "Date", y_col: y_col}
                )
                fig.update_layout(showlegend=False)
                st.plotly_chart(fig, width='stretch')
            else:
                fig = px.area(
                    df_source,
                    x=date_col,
                    y=y_col,
                    color=region_col if region_col else None,
                    title=f"{y_col.upper()} Area Chart Over Time{title_suffix}",
                    labels={date_col: "Date", y_col: y_col}
                )
                st.plotly_chart(fig, width='stretch')

        # Show GHI as a plain line chart with 'x' markers (replace area chart to match requested style)
        if selected_chart == "GHI Area" or selected_chart == "All":
            st.subheader("🗺️ GHI Over Time — Line Plot")
            fig_ghi = go.Figure()

            if region_col and region_col in plot_sample.columns:
                for r in plot_sample[region_col].dropna().unique():
                    df_r = plot_sample[plot_sample[region_col] == r]
                    fig_ghi.add_trace(go.Scatter(
                        x=df_r[date_col],
                        y=df_r[ghi_col],
                        mode='lines+markers',
                        name=str(r),
                        marker=dict(symbol='x', size=6),
                        line=dict(shape='linear', width=1)
                    ))
            else:
                fig_ghi.add_trace(go.Scatter(
                    x=plot_sample[date_col],
                    y=plot_sample[ghi_col],
                    mode='lines+markers',
                    name='GHI',
                    marker=dict(symbol='x', size=6),
                    line=dict(shape='linear', width=1)
                ))

            fig_ghi.update_layout(
                title="GHI Over Time",
                xaxis_title="Date",
                yaxis_title=ghi_col,
                showlegend=True
            )
            st.plotly_chart(fig_ghi, width='stretch')

        if temp_col and (selected_chart == "Temperature Area" or selected_chart == "All"):
            st.subheader("🌡️ Area Chart: Temperature Over Time")
            show_area(plot_sample, temp_col, title_suffix=" (Temperature)")

        if temp_col and (selected_chart == "Bubble: GHI vs Temp" or selected_chart == "All"):
            st.subheader("🫧 Bubble Chart: GHI vs Temperature")
            fig_bubble = px.scatter(
                plot_sample,
                x=temp_col,
                y=ghi_col,
                size=ghi_col,
                color=region_col if region_col else ghi_col,
                color_continuous_scale="Viridis",
                title="GHI vs Temperature (Size = GHI)",
                hover_data=[region_col] if region_col else None
            )
            st.plotly_chart(fig_bubble, width='stretch')

        if date_col and (selected_chart == "Line: GHI over Time" or selected_chart == "All"):
            st.subheader("📈 GHI Trend Over Time")
            # Build a plain line chart with 'x' markers (straight lines, discrete points)
            fig_line = go.Figure()

            # If the dataset contains regions, add one trace per region for clarity
            if region_col and region_col in plot_sample.columns:
                for r in plot_sample[region_col].dropna().unique():
                    df_r = plot_sample[plot_sample[region_col] == r]
                    fig_line.add_trace(go.Scatter(
                        x=df_r[date_col],
                        y=df_r[ghi_col],
                        mode='lines+markers',
                        name=str(r),
                        marker=dict(symbol='x', size=6),
                        line=dict(shape='linear')
                    ))
            else:
                fig_line.add_trace(go.Scatter(
                    x=plot_sample[date_col],
                    y=plot_sample[ghi_col],
                    mode='lines+markers',
                    name='GHI',
                    marker=dict(symbol='x', size=6),
                    line=dict(shape='linear')
                ))

            fig_line.update_layout(
                title="GHI Over Time",
                xaxis_title="Date",
                yaxis_title=ghi_col,
                legend_title_text="Region"
            )
            st.plotly_chart(fig_line, width='stretch')

        # --- Comparative overview across all countries ---
        if show_compare:
            st.markdown("## 🌐 Comparative Overview — All Countries")
            all_country_dfs = []
            for c in country_list:
                df_c = load_country_data(c)
                if df_c is None:
                    continue
                # normalize
                df_c.columns = df_c.columns.str.strip().str.lower()
                df_c.rename(columns={"timestamp": "date", "tamb": "temperature"}, inplace=True)
                ghi_c = next((col for col in df_c.columns if "ghi" in col), None)
                if "date" in df_c.columns:
                    df_c["date"] = pd.to_datetime(df_c["date"], errors="coerce")
                if ghi_c:
                    df_c[ghi_c] = pd.to_numeric(df_c[ghi_c], errors="coerce")
                    # unify ghi column name
                    df_c = df_c.rename(columns={ghi_c: "ghi"})
                else:
                    continue
                # keep minimal columns
                tmp = df_c[["date", "ghi"]].dropna()
                if tmp.empty:
                    continue
                tmp["country"] = c
                all_country_dfs.append(tmp)

            if not all_country_dfs:
                st.info("No comparative data available for the countries.")
            else:
                df_all = pd.concat(all_country_dfs, ignore_index=True)
                # aggregate to daily mean to keep visuals light
                df_daily = (
                    df_all
                    .groupby([pd.Grouper(key="date", freq="D"), "country"])["ghi"]
                    .mean()
                    .reset_index()
                )

                # summary table per country
                summary = (
                    df_all.groupby("country")["ghi"]
                    .agg(["max", "min", "mean"])
                    .rename(columns={"mean": "avg"})
                    .reset_index()
                )
                st.subheader("Summary Metrics by Country")
                st.table(summary)

                st.subheader("Combined Area: Daily Mean GHI by Country")
                fig_cmp = px.area(
                    df_daily,
                    x="date",
                    y="ghi",
                    color="country",
                    title="Daily Mean GHI — Countries Comparison",
                    labels={"date": "Date", "ghi": "Daily Mean GHI"}
                )
                st.plotly_chart(fig_cmp, width='stretch')

                st.subheader("Small Multiples: Daily GHI per Country")
                fig_facet = px.area(
                    df_daily,
                    x="date",
                    y="ghi",
                    facet_col="country",
                    facet_col_wrap=3,
                    title="Daily Mean GHI — Small Multiples by Country",
                )
                fig_facet.update_layout(showlegend=False)
                st.plotly_chart(fig_facet, width='stretch')
