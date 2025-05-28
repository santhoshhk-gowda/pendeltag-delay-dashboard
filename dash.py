{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "id": "4872519b-3edf-4757-8a50-eae32a8359b3",
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "2025-05-28 17:25:39.119 \n",
      "  \u001b[33m\u001b[1mWarning:\u001b[0m to view this Streamlit app on a browser, run it with the following\n",
      "  command:\n",
      "\n",
      "    streamlit run C:\\ProgramData\\anaconda3\\Lib\\site-packages\\ipykernel_launcher.py [ARGUMENTS]\n"
     ]
    }
   ],
   "source": [
    "import streamlit as st\n",
    "import pandas as pd\n",
    "import matplotlib.pyplot as plt\n",
    "\n",
    "st.set_page_config(page_title=\"Pendeltåg Delay Dashboard\", layout=\"wide\")\n",
    "\n",
    "st.title(\"🚆 Pendeltåg Delay Dashboard\")\n",
    "st.markdown(\"Analyze train delays based on historical Pendeltåg data.\")\n",
    "\n",
    "# Load CSV file\n",
    "uploaded_file = st.file_uploader(\"C:/Users/santhosh k/Desktop/Project/data/pendeltag_combined\", type=[\"csv\"])\n",
    "if uploaded_file:\n",
    "    df = pd.read_csv(uploaded_file, parse_dates=[\"scheduled\", \"expected\", \"timestamp_fetched\"])\n",
    "\n",
    "    # --- Filters ---\n",
    "    station_options = df['station_name'].dropna().unique()\n",
    "    selected_stations = st.multiselect(\"Select Station(s):\", options=station_options, default=list(station_options))\n",
    "\n",
    "    day_options = df['day_of_week'].dropna().unique()\n",
    "    selected_days = st.multiselect(\"Select Day(s) of Week (0=Mon, 6=Sun):\", options=sorted(day_options), default=sorted(day_options))\n",
    "\n",
    "    filtered_df = df[df['station_name'].isin(selected_stations) & df['day_of_week'].isin(selected_days)]\n",
    "\n",
    "    st.markdown(f\"### Filtered Data ({len(filtered_df)} rows)\")\n",
    "    st.dataframe(filtered_df[['station_name', 'scheduled', 'expected', 'delay_min', 'is_delayed', 'day_of_week', 'hour']].head(20))\n",
    "\n",
    "    # --- Delay Distribution ---\n",
    "    st.subheader(\"📊 Delay Distribution (in Minutes)\")\n",
    "    fig, ax = plt.subplots()\n",
    "    ax.hist(filtered_df['delay_min'], bins=30, edgecolor='black')\n",
    "    ax.set_xlabel(\"Delay (minutes)\")\n",
    "    ax.set_ylabel(\"Number of Trains\")\n",
    "    st.pyplot(fig)\n",
    "\n",
    "    # --- Average Delay Over Time ---\n",
    "    st.subheader(\"📈 Average Delay Over Time\")\n",
    "    filtered_df['date'] = filtered_df['scheduled'].dt.date\n",
    "    delay_trend = filtered_df.groupby('date')['delay_min'].mean()\n",
    "    st.line_chart(delay_trend)\n",
    "\n",
    "    # --- Top Delayed Stations ---\n",
    "    st.subheader(\"🏆 Top Stations by Average Delay\")\n",
    "    top_avg = filtered_df.groupby('station_name')['delay_min'].mean().sort_values(ascending=False).head(10)\n",
    "    st.bar_chart(top_avg)\n",
    "\n",
    "    # --- Delay Summary ---\n",
    "    st.subheader(\"📌 Delay Summary\")\n",
    "    delayed_pct = 100 * filtered_df['is_delayed'].sum() / len(filtered_df)\n",
    "    st.metric(\"Delayed Trains (%)\", f\"{delayed_pct:.2f}%\")\n",
    "    st.metric(\"Average Delay (min)\", f\"{filtered_df['delay_min'].mean():.2f}\")\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "3d46fc09-9f51-4864-b4ab-66661d5837d4",
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.12.7"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
