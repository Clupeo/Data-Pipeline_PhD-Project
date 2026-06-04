import os
import pandas as pd


def create_filelist(files_dir, skip):
    df_meta_id = pd.read_csv("../data/meta_data.csv").ID

    filtered_files = []   
    # walk over every file in instrument directory 
    for dir_path, dirs, files in os.walk(files_dir):
        # filter for only "CHYYMMDD" experiments
        if os.path.basename(dir_path).startswith("CH"):
            for file in files:
                if skip in file: 
                    continue                     
                # filter for data files
                if file.endswith('.xlsx') or file.endswith('.csv'):
                    # don't get file if custom argument(s) prevent it                      
                    file_path = os.path.join(dir_path, file)
                    # search current id in meta information
                    for id in df_meta_id:
                        if id in file_path:
                            filtered_files.append(file_path)
    return filtered_files


def formatting_strings(strings):
    new_strings = []
    for string in strings:
        formatted_string = string.translate(str.maketrans({" ": "_", "(": "", ")": "", "°": ""})).upper()
        new_strings.append(formatted_string)
    return new_strings


def convert_types(df):
    # Automatic data conversion by pandas
    df = df.convert_dtypes()
    # Custom data conversion
    df["TIME"] = (df["TIME"].str.replace("-h", "").replace("-", "0")).astype(int)
    df["BIO_REP"] = df["BIO_REP"].astype("Int64")
    df["TEC_REP"] = df["TEC_REP"].astype("Int64")
    # Fill NaN values with 0 for samples with no data
    df.fillna(0, inplace = True)
    return df


def copy_start_control(df, META_DATA):
    skip = ["SC", "CC", "RM", "BM"] # Custom skip filter
    merged_df = pd.DataFrame(df)
    for exp in META_DATA["EXP_ABBR"].unique():
        if exp in skip: continue
        # Subset data frame and filter for start control
        sub_df = df[df["EXPERIMENT_NAME"] == exp]
        start_control = sub_df[(sub_df["SAMPLE_NAME"] == "Control") & (sub_df["TIME"] == 0)]
        # Append to each sample categorie start control values
        for sample_name in sub_df["SAMPLE_NAME"].unique():
            if (sample_name == "Control") | (sample_name == "VSS-Blank"): continue
            sample_control = start_control.assign(SAMPLE_NAME = sample_name)
            merged_df = pd.concat([merged_df, sample_control], ignore_index = True)
    return merged_df


def filter(df, time = []):
    # Break out if list is empty
    if not time: return df
    # Filter time list out of data frame
    df.drop(df[df["TIME"].isin([12])].index, inplace = True)
    return df