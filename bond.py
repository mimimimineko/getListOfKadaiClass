import pandas as pd

dfmoodle   = pd.read_csv("./moodle.csv",encoding="cp932",header=None,names=('A', 'C', 'B', 'D'))
dfsyllabus = pd.read_csv("./syllabus.csv",encoding="cp932", header=None,names=('A', 'B', 'C', 'D','E','F','G'))

df_merged = pd.merge(dfsyllabus,dfmoodle, on="C", how='left')
df_merged.to_csv("merged.csv", index=False)
