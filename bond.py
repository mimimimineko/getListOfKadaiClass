import pandas as pd

dfmoodle   = pd.read_csv("./test2.csv",encoding="utf-8",header=None,names=('A', 'B', 'C', 'D'))
dfsyllabus = pd.read_csv("test.csv",encoding="shift-jis", header=None,names=('A', 'B', 'C', 'D','E','F','G'))

df_merged = pd.merge(dfmoodle, dfsyllabus, on=3, how='left')
df_merged.to_csv("merged.csv", index=False)