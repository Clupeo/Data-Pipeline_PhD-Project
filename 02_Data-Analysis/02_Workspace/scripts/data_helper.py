import os
import yaml
import pandas as pd

def load_config(config_path=None):
    """
    Loads the configuration from a YAML file.
    Automatically finds the project root if config_path is not provided.
    """
    if config_path is None:
        # Assuming we are in 02_Data-Analysis/02_Workspace/scripts
        # Project root is 3 levels up
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.abspath(os.path.join(current_dir, "../../.."))
        config_path = os.path.join(project_root, "analysis_config.yaml")
    
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    
    # Resolve relative paths to absolute paths
    mode = config['data_mode']
    project_root = os.path.dirname(os.path.abspath(config_path))
    
    config['resolved_paths'] = {}
    for key, val in config['paths'][mode].items():
        config['resolved_paths'][key] = os.path.abspath(os.path.join(project_root, val))
        
    return config

def create_filelist(files_dir, skip, meta_path):
    df_meta_id = pd.read_csv(meta_path).ID

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