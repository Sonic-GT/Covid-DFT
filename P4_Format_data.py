from globals import Tables_dir, Tables_suff, Fourier_magnitudes_dir, Fourier_magnitudes_suff, Formatted_dir, Formatted_suff, Graph_cases_suff, Graph_cases_dir, Graph_freq_suff, Graph_freq_dir, Freq_num, Italy_freq, Year_num, Day, Phase, \
    New_cases, Calculated_coefficients, Theoretical_cases
from P2_Make_tables import calc_freq_fraction
import pandas as pd
import os
import math
import matplotlib.pyplot as plt


def calc_theoretical_value(coefficients, freq_fraction):
    res = coefficients[0]
    for i in range(chosen_freq):
        freq_fraction_multiples = (i+1) * freq_fraction
        res += coefficients[2*i+1] * math.cos(freq_fraction_multiples) + coefficients[2*(i+1)] * math.sin(freq_fraction_multiples)
    return res


for file in os.listdir(Tables_dir):
    chosen_freq = Italy_freq if "Italy" in file else Freq_num

    file = file.strip(Tables_suff + ".csv")
    df_tables = pd.read_csv(f"{Tables_dir}/{file}{Tables_suff}.csv", sep=";")
    df_dft = pd.read_csv(f"{Fourier_magnitudes_dir}/{file}{Fourier_magnitudes_suff}.csv", sep=";")
    df_out = pd.DataFrame(columns=[Day, Phase, New_cases, Theoretical_cases, '', 'a0'] + [ab + str(i + 1) for i in range(chosen_freq) for ab in ['a', 'b']])
    for row in range(df_tables.shape[0]):
        row_args = [df_tables[Day][row], df_tables[New_cases][row], '', df_tables['a0'][row]] + [df_tables[col][row] for col in [ab + str(i + 1) for i in range(chosen_freq) for ab in ['a', 'b']]]
        row_args.insert(1, calc_freq_fraction(df_tables[Day][row]))
        # I coefficienti del software sono già riportati nei file DFT_magnitudes
        row_args.insert(3, calc_theoretical_value(df_dft[Calculated_coefficients].tolist(),
                                                  calc_freq_fraction(df_tables[Day][row])))
        df_out.loc[row] = row_args

    df_out.to_csv(f'{Formatted_dir}/{file}{Formatted_suff}.csv', sep=';', index=False)

    # New cases graph
    plt.scatter(df_out[Day], df_out[New_cases], label='Casi registrati')
    plt.scatter(df_out[Day], df_out[Theoretical_cases], label='Casi teorici')

    plt.xlabel('Giorni')
    plt.ylabel('Nuovi casi')
    plt.subplots_adjust(left=0.15)
    plt.title(f'Casi SARS-COV2 — {file}')
    plt.legend()
    plt.grid(True)

    plt.savefig(f'{Graph_cases_dir}/{file}{Graph_cases_suff}.png')
    plt.clf()

    # Frequency graph
    x_val = [0]+[(n+1) for n in range(chosen_freq)]
    y_val = [df_dft.iloc[0, 0]/2] + [pow((pow(df_dft.iloc[2*n+1, 0], 2) + pow(df_dft.iloc[2*(n+1), 0], 2)), 0.5)/2 for n in range(chosen_freq)]
    plt.plot(x_val, y_val)

    plt.xlabel('Frequenza')
    plt.ylabel('Intensità')
    plt.subplots_adjust(left=0.15)
    plt.xscale('log', base=2)
    plt.title(f'Frequenze FT — {file}')
    plt.grid(True)

    plt.savefig(f'{Graph_freq_dir}/{file}{Graph_freq_suff}.png')
    plt.clf()
