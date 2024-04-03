from globals import Freq_num, Italy_freq, Tables_dir, Tables_suff, New_cases, Fourier_magnitudes_dir, Fourier_magnitudes_suff, \
    Fourier_magnitudes_suff_2, Calculated_coefficients
import numpy as np
import pandas as pd
import math
import os

chosen_freq = Freq_num


for file in os.listdir(Tables_dir):
    Freq_num = Italy_freq if "Italy" in file else chosen_freq

    file = file.strip(Tables_suff + ".csv")
    data = pd.read_csv(f"{Tables_dir}/{file}{Tables_suff}.csv", sep=";")
    A = data[['a0'] + [ab + str(i + 1) for i in range(Freq_num) for ab in ['a', 'b']]].to_numpy()
    b = data[[New_cases]].to_numpy()
    AN = A.transpose() @ A
    bn = A.transpose() @ b
    x = np.linalg.solve(AN, bn)
    np.set_printoptions(precision=2)
    print(x)

    out_df = pd.DataFrame([e[0] for e in x], columns=[Calculated_coefficients])
    out_df.to_csv(f'{Fourier_magnitudes_dir}/{file}{Fourier_magnitudes_suff}.csv', sep=';', index=False)

    x0 = np.nan
    x1 = np.array([1.0, 1.0])
    y1 = np.array([pow(x1[0], 2) + np.sin(math.pi * x1[0] * x1[1]) - 1, x1[0] + pow(x1[1], 2)
                   + np.exp(x1[0] + x1[1]) - 3])
    while np.linalg.norm(y1) > 0.1:
        x0 = x1 - np.linalg.inv(np.array([[2 * x1[0] + np.cos(math.pi * x1[0] * x1[1]) * math.pi * x1[1],
                                           np.cos(math.pi * x1[0] * x1[1]) * math.pi * x1[0]],
                                          [1 + np.exp(x1[0] + x1[1]), 2 * x1[1] + np.exp(x1[0] + x1[1])]])) @ y1
        x1 = x0
        y1 = np.array(
            [pow(x1[0], 2) + np.sin(math.pi * x1[0] * x1[1]) - 1, x1[0] + pow(x1[1], 2) + np.exp(x1[0] + x1[1]) - 3])
    print('lo zero è =', x0, ', la tolleranza è=', y1)

    data_list = [[round(float(x0[i]), 4), round(float(y1[i]), 4)] for i in range(2)]
    out = pd.DataFrame(data_list, columns=['zero', 'tolerance'])
    out.to_csv(f'{Fourier_magnitudes_dir}/{file}{Fourier_magnitudes_suff}{Fourier_magnitudes_suff_2}.csv', sep=';', index=False)
