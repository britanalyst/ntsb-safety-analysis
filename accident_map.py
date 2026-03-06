"""
accident_map.py

Creates a state by state heatmap of US civil aviation accidents
using NTSB data with an animated year slider. Built with Plotly
for interactive visualization.

Author: Brittany Blessie
Data source: NTSB Aviation Accident Database (1982-2024)
"""

import pyodbc
import pandas as pd
import plotly.express as px

# Path to the NTSB Access database file
db_path = r"C:\Users\brittany.blessie\Downloads\avall\avall.mdb"

# Connection string for Microsoft Access driver
conn_str = (
    r"Driver={Microsoft Access Driver (*.mdb, *.accdb)};"
    r"Dbq=" + db_path + ";"
)

# Establish database connection
conn = pyodbc.connect(conn_str)

# Load state and year data from events table
df = pd.read_sql("SELECT ev_state, ev_year FROM events", conn)

# Remove missing states and incomplete year
df = df.dropna(subset=['ev_state'])
df = df[df['ev_year'] < 2025]

# Count accidents per state per year
state_year_counts = df.groupby(['ev_year', 'ev_state']).size().reset_index()
state_year_counts.columns = ['year', 'state', 'accidents']

# Convert year to string for slider display
state_year_counts['year'] = state_year_counts['year'].astype(str)

# Build animated choropleth map with year slider
fig = px.choropleth(
    state_year_counts,
    locations='state',
    locationmode='USA-states',
    color='accidents',
    scope='usa',
    color_continuous_scale='Reds',
    animation_frame='year',
    range_color=[0, 150],
    title='US Aviation Accidents by State (NTSB 1982-2024)',
    labels={'accidents': 'Number of Accidents'}
)

# Add data source annotation
fig.add_annotation(
    text="Source: NTSB Aviation Accident Database",
    xref="paper", yref="paper",
    x=0, y=-0.05,
    showarrow=False,
    font=dict(size=10, color="gray")
)

fig.update_layout(
    title_font_size=16,
    geo=dict(showlakes=True, lakecolor='lightblue')
)

# Save as interactive HTML so the slider works
fig.write_html('accident_map.html')
fig.write_image('accident_map.png', scale=2)
fig.update_traces(
    hovertemplate="<b>%{location}</b><br>Accidents: %{z}<extra></extra>"
)

fig.write_html('accident_map.html')
fig.write_image('accident_map.png', scale=2)
fig.show()