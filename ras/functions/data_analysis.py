import pandas as pd
import csv
import numpy as np
from tabulate import tabulate
from run import app
from flask import session


def statastics(filename):
    df = pd.read_csv(f"{app.config['CSV_DIRECTORY']}/{filename[:-4]}.csv")
    student_count = df.groupby('SEM')['NAME OF STUDENT'].nunique().reset_index()
    student_count.rename(columns={'NAME OF STUDENT': 'STUDENT COUNT'}, inplace=True)

    count_f = df[df['GRADE POINT'] == 'F'].groupby(['SEM', 'SUBJECT CODE']).size().reset_index(name='FAILED STUDENT COUNT')
    count_aa_ex = df[df['EXTERNAL'] == 'AA'].groupby(['SEM', 'SUBJECT CODE']).size().reset_index(name='ABSENT STUDENT IN EXTERNAL COUNT')
    count_aa_in = df[df['INTERNAL'] == 'AA'].groupby(['SEM', 'SUBJECT CODE']).size().reset_index(name='ABSENT STUDENT IN INTERNAL COUNT')


    merged_df = pd.merge(count_f, count_aa_ex, on=['SEM', 'SUBJECT CODE'], how='outer', suffixes=('_failed', '_external_absent'))
    merged_df = pd.merge(merged_df, count_aa_in, on=['SEM', 'SUBJECT CODE'], how='outer', suffixes=('_failed', '_internal_absent'))
    merged_df.fillna(0, inplace=True)
    merged_df['ABSENT STUDENT IN EXTERNAL COUNT'] = merged_df['ABSENT STUDENT IN EXTERNAL COUNT'].astype(int)
    merged_df['ABSENT STUDENT IN INTERNAL COUNT'] = merged_df['ABSENT STUDENT IN INTERNAL COUNT'].astype(int)
    merged_df.to_excel(f"{app.config['CSV_DIRECTORY']}/{session['iname']}_failed_absent_count.xlsx",index=False)



    df['INTERNAL'] = pd.to_numeric(df['INTERNAL'], errors='coerce')
    df['EXTERNAL'] = pd.to_numeric(df['EXTERNAL'], errors='coerce')
    statistics = df.groupby(['SEM','SUBJECT CODE']).agg({
        'INTERNAL': ['max', 'min', lambda x: round(x.mean(), 2)],
        'EXTERNAL': ['max', 'min', lambda x: round(x.mean(), 2)]
    })
    statistics.columns = ['MAX_IN', 'MIN_IN', 'AVG_IN', 'MAX_EX', 'MIN_EX', 'AVG_EX']
    statistics.to_excel(f"{app.config['CSV_DIRECTORY']}/{session['iname']}_statistics.xlsx")

