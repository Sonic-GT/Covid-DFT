from globals import Tables_dir, Tables_suff, Fourier_magnitudes_dir, Fourier_magnitudes_suff, Formatted_dir, Formatted_suff, Graph_suff, Graph_dir,  Freq_num, Italy_freq, Day, Phase, \
    New_cases, Calculated_coefficients, Theoretical_cases
from P2_Make_tables import calc_freq_fraction
import pandas as pd
import os
import math
import matplotlib.pyplot as plt

chosen_freq = Freq_num


def calc_theoretical_value(coefficients, freq_fraction):
    res = coefficients[0]
    for i in range(Freq_num):
        freq_fraction_multiples = (i+1) * freq_fraction
        res += coefficients[2*i+1] * math.cos(freq_fraction_multiples) + coefficients[2*(i+1)] * math.sin(freq_fraction_multiples)
    return res


for file in os.listdir(Tables_dir):
    Freq_num = Italy_freq if "Italy" in file else chosen_freq

    file = file.strip(Tables_suff + ".csv")
    df_tables = pd.read_csv(f"{Tables_dir}/{file}{Tables_suff}.csv", sep=";")
    df_dft = pd.read_csv(f"{Fourier_magnitudes_dir}/{file}{Fourier_magnitudes_suff}.csv", sep=";")
    df_out = pd.DataFrame(columns=[Day, Phase, New_cases, Theoretical_cases, '', 'a0'] + [ab + str(i + 1) for i in range(Freq_num) for ab in ['a', 'b']])
    for row in range(df_tables.shape[0]):
        row_args = [df_tables[Day][row], df_tables[New_cases][row], '', df_tables['a0'][row]] + [df_tables[col][row] for col in [ab + str(i + 1) for i in range(Freq_num) for ab in ['a', 'b']]]
        row_args.insert(1, calc_freq_fraction(df_tables[Day][row]))
        # I coefficienti del software sono già riportati nei file DFT_magnitudes
        row_args.insert(3, calc_theoretical_value(df_dft[Calculated_coefficients].tolist(),
                                                  calc_freq_fraction(df_tables[Day][row])))
        df_out.loc[row] = row_args

    df_out.to_csv(f'{Formatted_dir}/{file}{Formatted_suff}.csv', sep=';', index=False)

    plt.scatter(df_out[Day], df_out[New_cases], label='Casi registrati')
    plt.scatter(df_out[Day], df_out[Theoretical_cases], label='Casi teorici')

    plt.xlabel('Giorni')
    plt.ylabel('Nuovi casi')
    plt.subplots_adjust(left=0.15)
    plt.title(f'Casi SARS-COV2 — {file}')
    plt.legend()
    plt.grid(True)

    plt.savefig(f'{Graph_dir}/{file}{Graph_suff}.png')
    plt.clf()
