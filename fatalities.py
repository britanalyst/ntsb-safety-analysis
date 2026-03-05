import pyodbc
import pandas as pd
import matplotlib.pyplot as plt

db_path = r"C:\Users\brittany.blessie\Downloads\avall\avall.mdb"

conn_str = (
    r"Driver={Microsoft Access Driver (*.mdb, *.accdb)};"
    r"Dbq=" + db_path + ";"
)

conn = pyodbc.connect(conn_str)

injury = pd.read_sql("SELECT * FROM injury", conn)
events = pd.read_sql("SELECT ev_id, ev_year FROM events", conn)

fatalities = injury[injury['injury_level'] == 'FATL']
merged = fatalities.merge(events, on='ev_id')
merged = merged[merged['ev_year'] < 2025]

fatalities_by_year = merged.groupby('ev_year')['inj_person_count'].sum()

plt.figure(figsize=(14, 6))
plt.bar(fatalities_by_year.index, fatalities_by_year.values, color='steelblue', width=0.7)
plt.title('US Aviation Fatalities by Year', fontsize=14, pad=15)
plt.xlabel('Year', fontsize=11)
plt.ylabel('Number of Fatalities', fontsize=11)
plt.xticks(fatalities_by_year.index, rotation=45, ha='right')
plt.grid(True, alpha=0.3, axis='y')
plt.tight_layout()
plt.savefig('fatalities_by_year.png', dpi=150)
plt.show()