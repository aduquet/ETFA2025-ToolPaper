from scipy.stats import pearsonr
import pandas as pd
import numpy as np

def normalize_column(column):
    return round((column - column.min()) / (column.max() - column.min()),3)

def get_max(column):
    return column.max()

def calculate_penalty(row, overshoot_allowance=1.05, eng_p_s_target=1, eng_p_target=1, eng_s_target=1, 
                      pEngP = 1, 
                      pEngs = 1,
                      pEngSP = 1):
    """Calculate penalty for deviation from ideal PR and balance."""
    pr_value = row['PR']
    nobp_s = row['nobp_s'] 

    # Check if PR is within the acceptable range [1, overshoot_allowance]
    if 1 <= pr_value <= float(overshoot_allowance): # type: ignore
        pr_penalty = 0  # No penalty if within the range
    else:
        # Penalize based on the distance from the nearest boundary
        if pr_value < 1:
            pr_penalty = abs(pr_value - 1) * 100
        else:
            pr_penalty = abs(pr_value - overshoot_allowance) * 100  # Penalize deviation from ideal PR

    if nobp_s == 1: # type: ignore
        nobp_penalty = 0  
    else:
        nobp_penalty = nobp_s / 10


    # Penalize imbalance in energy ratios
    if eng_p_s_target != None:
        eng_p_s_penalty = abs(row['Eng_p-s'] - eng_p_s_target)

    else:
        eng_p_s_penalty = 0

    if eng_p_target != None:
        # eng_p_penalty = abs(row['P-Eng'] - float(eng_p_target))
        eng_p_penalty = abs(row['P-Eng'] - eng_p_target)

    else:
        eng_p_penalty = 0

    if eng_s_target != None:
        # eng_s_penalty = abs(row['S-Eng'] - float(eng_s_target))
        eng_s_penalty = abs(row['S-Eng'] - eng_s_target)

    else:
        eng_s_penalty = 0
    
    # Calculate the total penalty
    total_penalty = pr_penalty + (pEngSP * eng_p_s_penalty) + (pEngP *eng_p_penalty) + (pEngs*eng_s_penalty) + nobp_penalty

    return total_penalty

def rank_tests_p(df, weights, 
               overshoot_allowance=1.05,
               eng_p_s_target=1, 
               eng_p_target=1, 
               eng_s_target=1, 
               use_eng_p_s = True):
    """Rank the test cases based on weighted scores and penalties."""

    # Step 1: Normalize the metrics
    # df['norm_PR'] = (df['PR'])
    # df['norm_RT'] = normalize_column(df['RT'])

    # RT_max = get_max(df['RT'])

    # df['PR_aux'] = normalize_column(overshoot_allowance - df['norm_PR']) 
    # df['RT_aux'] = normalize_column(abs(df['norm_RT']-RT_max) )

    # Group by 'tc' and apply normalization within each group
    df['norm_PR'] = df.groupby('tc')['PR'].transform(lambda x: normalize_column(x))
    df['norm_RT'] = df.groupby('tc')['RT'].transform(lambda x: normalize_column(x))

    # Calculate the maximum RT per test case group
    df['RT_max'] = df.groupby('tc')['RT'].transform('max')

    # Adjust PR and RT auxiliary calculations to work per test case
    df['PR_aux'] = df.groupby('tc')['norm_PR'].transform(lambda x: normalize_column(overshoot_allowance - x))
    df['RT_aux'] = df.groupby('tc')['norm_RT'].transform(lambda x: normalize_column(abs(x - df['RT_max'])))


    df['weighted_score'] = (
        (weights['PR'] * df['PR_aux'] ) +
        (weights['RT'] * df['RT_aux'])
    )

    pEngP = weights['P-Eng'] 
    pEngs = weights['S-Eng']
    pEngSP = weights['Eng_p-s']

    if use_eng_p_s:
        # Directly assign the penalty to the DataFrame
        df['penalty'] = df.apply(
            lambda row: calculate_penalty(
                row,
                overshoot_allowance=overshoot_allowance,
                eng_p_s_target=eng_p_s_target,
                eng_p_target=eng_p_target,
                eng_s_target=eng_s_target,
                pEngP = pEngP, 
                pEngs = pEngs,
                pEngSP = pEngSP
            ),
            axis=1
            )

    else:
        # Ignore Eng_p-s target in the penalty calculation
        df['penalty'] = df.apply(
            lambda row: calculate_penalty(
                row,
            overshoot_allowance=overshoot_allowance,
            eng_p_s_target=None,  # Set to None or some default value # type: ignore
            eng_p_target=eng_p_target,
            eng_s_target=eng_s_target,
            pEngP = pEngP, 
            pEngs = pEngs,
            pEngSP = pEngSP
            ),
            axis=1
            )
    df['final_score'] = df['weighted_score'] - df['penalty']
    df['GR'] = df['final_score'].rank(ascending=False)
    df = df.dropna(subset=['GR'])
    # Sort by rank for final output
    df = df.sort_values(by='GR')
    df = df.dropna(subset=['GR'])

    df['IR'] = df.groupby(df['test_id'].str.extract(r'(tc\d+)', expand=False))['final_score'].rank(ascending=False)
    
    return df

def rank_tests(df, weights, 
               overshoot_allowance=1.05):
    """Rank the test cases based on weighted scores and penalties."""

    df['norm_RT'] = normalize_column(df['RT'])

    RT_max = get_max(df['RT'])

    df['PR_aux'] = normalize_column(overshoot_allowance - df['norm_PR']) 
    df['RT_aux'] = normalize_column(abs(df['norm_RT']-RT_max) )


    df['weighted_score'] = (
        (weights['PR'] * df['PR_aux'] ) +
        (weights['RT'] * df['RT_aux'])
    )

    df['penalty'] = df.apply(
            lambda row: calculate_penalty(
                row,
            overshoot_allowance=overshoot_allowance,
            eng_p_s_target=None,  # Set to None or some default value # type: ignore
            eng_p_target=None, # type: ignore
            eng_s_target=None, # type: ignore
            pEngP = 0, 
            pEngs = 0,
            pEngSP = 0
            ),
            axis=1
            )

    df['final_score'] = df['weighted_score'] - df['penalty']
    
    df['GR'] = df['final_score'].rank(ascending=False)
    df = df.dropna(subset=['GR'])
    # Sort by rank for final output
    df = df.sort_values(by='GR')

    df['IR'] = df.groupby(df['test_id'].str.extract(r'(tc\d+)', expand=False))['final_score'].rank(ascending=False)
    
    return df


def rank_tests_def(df, weights, 
                   overshoot_allowance=1.05, 
               eng_p_s_target=1, 
               eng_p_target=1, 
               eng_s_target=1,

            #    eng_p_s_target=0.099079, 
            #    eng_p_target=0.055461, 
            #    eng_s_target=0.007009, 
                   ):
    use_eng_p_s = True

    # df['norm_PR'] = (df['PR'])
    # df['norm_RT'] = normalize_column(df['RT'])

    # RT_max = get_max(df['RT'])

    # df['PR_aux'] = normalize_column(overshoot_allowance - df['norm_PR']) 
    # df['RT_aux'] = normalize_column(abs(df['norm_RT']-RT_max) )

    df['norm_PR'] = df.groupby('tc')['PR'].transform(lambda x: normalize_column(x))
    df['norm_RT'] = df.groupby('tc')['RT'].transform(lambda x: normalize_column(x))

    # Calculate the maximum RT per test case group
    df['RT_max'] = df.groupby('tc')['RT'].transform('max')

    # Adjust PR and RT auxiliary calculations to work per test case
    df['PR_aux'] = df.groupby('tc')['norm_PR'].transform(lambda x: normalize_column(overshoot_allowance - x))
    df['RT_aux'] = df.groupby('tc')['norm_RT'].transform(lambda x: normalize_column(abs(x - df['RT_max'])))


    df['weighted_score'] = (
        (weights['PR'] * df['PR_aux'] ) +
        (weights['RT'] * df['RT_aux'])
    )

    pEngP = weights['P-Eng'] 
    pEngs = weights['S-Eng']
    pEngSP = weights['Eng_p-s']

    if use_eng_p_s:
        # Directly assign the penalty to the DataFrame
        df['penalty'] = df.apply(
            lambda row: calculate_penalty(
                row,
                overshoot_allowance=overshoot_allowance,
                eng_p_s_target=eng_p_s_target,
                eng_p_target=eng_p_target,
                eng_s_target=eng_s_target,
                pEngP = pEngP, 
                pEngs = pEngs,
                pEngSP = pEngSP
            ),
            axis=1
            )

    else:
        # Ignore Eng_p-s target in the penalty calculation
        df['penalty'] = df.apply(
            lambda row: calculate_penalty(
                row,
            overshoot_allowance=overshoot_allowance,
            eng_p_s_target=None,  # Set to None or some default value # type: ignore
            eng_p_target=eng_p_target,
            eng_s_target=eng_s_target,
            pEngP = pEngP, 
            pEngs = pEngs,
            pEngSP = pEngSP
            ),
            axis=1
            )

    df['final_score'] = df['weighted_score'] - df['penalty']
        
    # Step 5: Rank based on the final score
    df['def_GR'] = df['final_score'].rank(ascending=False)
    df = df.dropna(subset=['def_GR'])
        # Sort by rank for final output
    df = df.sort_values(by='def_GR')

    df['def_IR'] = df.groupby(df['test_id'].str.extract(r'(tc\d+)', expand=False))['final_score'].rank(ascending=False)


    return df

def normalising_data(df):
    df_aux = df.copy()

    # Create a dictionary mapping test_id prefixes to their respective t0 rows
    t0_rows = {
        'tc100': df_aux[df_aux['test_id'] == 'tc100_def_0'].iloc[0],
        'tc104': df_aux[df_aux['test_id'] == 'tc104_def_0'].iloc[0],
        'tc106': df_aux[df_aux['test_id'] == 'tc106_def_0'].iloc[0]
    }

    # Normalize the relevant columns based on the appropriate t0 row
    for index, row in df_aux.iterrows():
        for prefix, t0_row in t0_rows.items():
            if row['test_id'].startswith(prefix):
                for col in ['P-Eng', 'S-Eng', 'Eng_p-s', 'gr_s', 'gr_ratio']:
                    df_aux.at[index, col] = round((row[col] / t0_row[col]), 3) # type: ignore
                break  # Exit loop once the correct t0_row is found

    return df_aux
