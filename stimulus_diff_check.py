import pandas as pd
import math


def check_adjacent_differences(file_path, column_name):
    df = pd.read_csv(file_path, delimiter='\t', encoding='utf-8')
    df = df.sort_values(column_name)
    df['diff'] = df[column_name].diff().abs()
    tolerance = 1e-9

    non_matching_rows = [row_index for row_index in range(1, len(df)) if not math.isclose(df.loc[row_index, 'diff'],
                                                                                          df.loc[row_index - 1, 'diff'],
                                                                                          rel_tol=tolerance)]

    if len(non_matching_rows) == 0:
        print(f"All adjacent cells in {column_name} have the same difference.")
    else:
        for row_index in non_matching_rows:
            prev_row_index = row_index - 1
            current_value = df.loc[row_index, column_name]
            prev_value = df.loc[prev_row_index, column_name]
            diff_not_matching = df.loc[row_index, 'diff']
            print(f"Difference not equal to {df.loc[prev_row_index, 'diff']:.4f} between rows {prev_row_index} and {row_index} in {column_name}: {prev_value} and {current_value}, difference: {current_value - prev_value:.4f}")


files_and_columns = [
    (r'C:\Users\Andrea Hofmann\OneDrive\PhD\exp_jnd\jnd_task\audio\audio-FL\manipulation_FL_mimmi_ch.csv',
     'diffSyllDur'),
    (r'C:\Users\Andrea Hofmann\OneDrive\PhD\exp_jnd\jnd_task\audio\audio-pause\manipulation_pause_lilli_lisa_ch.csv',
     'p3New'),
    (r'C:\Users\Andrea Hofmann\OneDrive\PhD\exp_jnd\jnd_task\audio\audio-pitch\manipulation_pitch_nelli_ch.csv',
     'riseNew')
]

for file_path, column_name in files_and_columns:
    check_adjacent_differences(file_path, column_name)
