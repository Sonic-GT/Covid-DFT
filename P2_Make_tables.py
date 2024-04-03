from globals import Freq_num, Italy_freq, Year_num, New_cases, Day, Wo_z_dir, Wo_z_suff, Tables_dir, Tables_suff
import pandas as pd
import math
import os

chosen_freq = Freq_num


def calc_freq_fraction(day):
    return day * 2 * math.pi / (365 * Year_num)


for file in os.listdir(Wo_z_dir):
    Freq_num = Italy_freq if "Italy" in file else chosen_freq

    file = file.strip(Wo_z_suff + ".csv")
    df = pd.read_csv(f"{Wo_z_dir}/{file}{Wo_z_suff}.csv", sep=";", header=None)
    new_df = pd.DataFrame(columns=[Day, New_cases, 'a0'] + [ab + str(i + 1) for i in range(Freq_num) for ab in ['a', 'b']])

    for row in range(df.shape[0]):
        row_args = [df.iloc[row, 0], df.iloc[row, 1], 1]
        for i in range(Freq_num):
            freq_fraction_multiples = (i + 1) * calc_freq_fraction(df.iloc[row, 0])
            row_args += [math.cos(freq_fraction_multiples), math.sin(freq_fraction_multiples)]

        new_df.loc[row] = row_args

    new_df[Day] = new_df[Day].astype(int)
    new_df[New_cases] = new_df[New_cases].astype(int)
    new_df.to_csv(f"{Tables_dir}/{file}{Tables_suff}.csv", sep=";", index=False)
