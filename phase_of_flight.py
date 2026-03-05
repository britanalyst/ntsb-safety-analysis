import pyodbc
import pandas as pd
import matplotlib.pyplot as plt

db_path = r"C:\Users\brittany.blessie\Downloads\avall\avall.mdb"

conn_str = (
    r"Driver={Microsoft Access Driver (*.mdb, *.accdb)};"
    r"Dbq=" + db_path + ";"
)

conn = pyodbc.connect(conn_str)

df = pd.read_sql("SELECT * FROM Events_Sequence", conn)

phase_counts = df['Occurrence_Description'].value_counts().head(10)

plt.figure(figsize=(12, 7))
bars = plt.barh(range(len(phase_counts)), phase_counts.values, color='steelblue')
plt.yticks(range(len(phase_counts)), phase_counts.index, fontsize=9)
plt.title('Top 10 Accident Types by Occurrence', fontsize=14, pad=15)
plt.xlabel('Number of Accidents', fontsize=11)
plt.gca().invert_yaxis()
plt.grid(True, alpha=0.3, axis='x')
plt.tight_layout()
plt.savefig('phase_of_flight.png', dpi=150)
plt.show()