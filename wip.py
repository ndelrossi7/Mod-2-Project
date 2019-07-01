#%%
import sqlite3
conn = sqlite3.connect('database.sqlite')
c = conn.cursor()

import pandas as pd

#%%
c.execute('''SELECT * FROM Matches WHERE season = 2011;''')
df = pd.DataFrame(c.fetchall())
df.columns = [x[0] for x in c.description]
df.head()

#%%
