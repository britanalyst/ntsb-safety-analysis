import pyodbc
import pandas as pd
import matplotlib.pyplot as plt

db_path = r"C:\Users\brittany.blessie\Downloads\avall\avall.mdb"

conn_str = (
    r"Driver={Microsoft Access Driver (*.mdb, *.accdb)};"
    r"Dbq=" + db_path + ";"
)

conn = pyodbc.connect(conn_str)

aircraft = pd.read_sql("SELECT ev_id, acft_category FROM aircraft", conn)
events_seq = pd.read_sql("SELECT ev_id, Occurrence_Description FROM Events_Sequence", conn)
events = pd.read_sql("SELECT ev_id, ev_year FROM events", conn)

# Filter to helicopters only
heli = aircraft[aircraft['acft_category'] == 'HELI']

# Merge with events sequence
merged = heli.merge(events_seq, on='ev_id')
merged = merged.merge(events, on='ev_id')

# Filter out incomplete year
merged = merged[merged['ev_year'] < 2025]

# Top 10 accident types
top_types = merged['Occurrence_Description'].value_counts().head(10)

plt.figure(figsize=(12, 7))
top_types.plot(kind='barh', color='steelblue')
plt.title('Top 10 Helicopter Accident Types (NTSB 1982-2024)', fontsize=14, pad=15)
plt.xlabel('Number of Accidents', fontsize=11)
plt.gca().invert_yaxis()
plt.grid(True, alpha=0.3, axis='x')
plt.tight_layout()
plt.savefig('helicopter_accident_types.png', dpi=150)
plt.show()

# Helicopter accidents by year
heli_by_year = merged.groupby('ev_year').size()

plt.figure(figsize=(12, 6))
plt.plot(heli_by_year.index, heli_by_year.values, color='steelblue', linewidth=2)
plt.title('Helicopter Accidents by Year (NTSB 1982-2024)', fontsize=14, pad=15)
plt.xlabel('Year', fontsize=11)
plt.ylabel('Number of Accidents', fontsize=11)
plt.xticks(heli_by_year.index[::2], rotation=45, ha='right')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('helicopter_accidents_by_year.png', dpi=150)
plt.show()