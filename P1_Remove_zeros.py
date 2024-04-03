from globals import First_dir, Wo_z_suff, Wo_z_dir
import pandas as pd
import os

for file in os.listdir(First_dir):
    file = file.strip(".csv")
    df = pd.read_csv(f"{First_dir}/{file}.csv")

    new_df = df[df.index % 7 == 5]
    new_df.index += 2

    new_df.to_csv(f"{Wo_z_dir}/{file}{Wo_z_suff}.csv", sep=";", header=None)
