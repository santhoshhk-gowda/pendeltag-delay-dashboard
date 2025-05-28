import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# App title
st.set_page_config(page_title="Pendeltåg Delay Dashboard", layout="wide")
st.title(" Pendeltåg Delay Dashboard")
st.markdown("Upload your Pendeltåg CSV file to explore delays by station and day.")

# Upload CSV
uploaded_file = st.file_uploader("C:/Users/santhosh k/Desktop/Project/data/pendetag_combined", type=["csv"])

if uploaded_file:
    # Load and parse date columns
    df = pd.read_csv(uploaded_file, parse_dates=["scheduled", "expected", "timestamp_fetched"])

    # Create 'date' column
    df['date'] = df['scheduled'].dt.date

    # --- Filters ---
    stations = df['station_name'].dropna().unique()
    selected_stations = st.multiselect("Select Station(s):", stations, default=list(stations))

    days = df['day_of_week'].dropna().unique()
    selected_days = st.multiselect("Select Day(s) of Week (0=Mon, 6=Sun):", sorted(days), default=sorted(days))

    filtered_df = df[df['station_name'].isin(selected_stations) & df['day_of_week'].isin(selected_days)]

    # Show data preview
    st.markdown(f"### Showing {len(filtered_df)} rows")
    st.dataframe(filtered_df[['station_name', 'scheduled', 'expected', 'delay_min', 'is_delayed', 'day_of_week', 'hour']].head(20))

    # --- Delay Histogram ---
    st.subheader(" Delay Distribution (in Minutes)")
    fig, ax = plt.subplots()
    ax.hist(filtered_df['delay_min'].dropna(), bins=30, edgecolor='black')
    ax.set_xlabel("Delay (minutes)")
    ax.set_ylabel("Number of Trains")
    st.pyplot(fig)

    # --- Average Delay Over Time ---
    st.subheader(" Average Delay Over Time")
    delay_trend = filtered_df.groupby('date')['delay_min'].mean()
    st.line_chart(delay_trend)

    # --- Top Delayed Stations ---
    st.subheader(" Top Stations by Average Delay")
    top_avg = filtered_df.groupby('station_name')['delay_min'].mean().sort_values(ascending=False).head(10)
    st.bar_chart(top_avg)

    # --- Delay Summary ---
    st.subheader(" Delay Summary")
    total = len(filtered_df)
    delayed = filtered_df['is_delayed'].sum()
    avg_delay = filtered_df['delay_min'].mean()

    st.metric("Delayed Trains (%)", f"{(delayed / total * 100):.2f}%")
    st.metric("Average Delay (min)", f"{avg_delay:.2f}")
