import pyodbc
import pandas as pd
import matplotlib.pyplot as plt

db_path = r"C:\Users\brittany.blessie\Downloads\avall\avall.mdb"

conn_str = (
    r"Driver={Microsoft Access Driver (*.mdb, *.accdb)};"
    r"Dbq=" + db_path + ";"
)

conn = pyodbc.connect(conn_str)

df = pd.read_sql("SELECT * FROM events", conn)

# Filter out incomplete current year
df = df[df['ev_year'] < 2025]

accidents_by_year = df.groupby('ev_year').size()

plt.figure(figsize=(12, 6))
plt.plot(accidents_by_year.index, accidents_by_year.values, color='steelblue', linewidth=2)
plt.title('US Aviation Accidents by Year')
plt.xlabel('Year')
plt.ylabel('Number of Accidents')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('accidents_by_year.png', dpi=150)
plt.show()

