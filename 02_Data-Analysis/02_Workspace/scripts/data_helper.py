import os

import pandas as pd
import yaml

from .constants import SKIP_SAMPLES


def _project_root(config_path=None):
    if config_path:
        return os.path.dirname(os.path.abspath(config_path))
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.abspath(os.path.join(current_dir, "../../.."))


def load_config(config_path=None):
    """Load analysis_config.yaml and resolve all paths to absolute paths."""
    if config_path is None:
        config_path = os.path.join(_project_root(), "analysis_config.yaml")

    with open(config_path, "r", encoding="utf-8") as handle:
        config = yaml.safe_load(handle)

    mode = config["data_mode"]
    project_root = os.path.dirname(os.path.abspath(config_path))

    config["resolved_paths"] = {}
    for key, value in config["paths"][mode].items():
        if key == "experiment_ids":
            config["resolved_paths"][key] = value
        else:
            config["resolved_paths"][key] = os.path.abspath(
                os.path.join(project_root, value)
            )

    return config


def load_meta_data(config):
    """Load the full experiment metadata table."""
    return pd.read_csv(config["resolved_paths"]["meta_data"])


def get_experiment_types(meta_df, config=None):
    """Return experiment abbreviations to process in plots and exports."""
    if config is None:
        config = load_config()
    experiment_ids = config["resolved_paths"].get("experiment_ids")
    if experiment_ids:
        return meta_df[meta_df["ID"].isin(experiment_ids)]["EXP_ABBR"].unique()
    return meta_df[meta_df["SAMPLE_INFORMATION"].isna()]["EXP_ABBR"].unique()


def get_sample_columns(meta_df):
    """Return raw-data column names defined in the metadata schema rows."""
    return meta_df["SAMPLE_INFORMATION"].dropna().tolist()


def is_full_dataset(config):
    """Return True when the pipeline should process the complete dataset."""
    return config.get("data_mode") == "full"


def should_run_ngs(config):
    """NGS notebooks only run in full-dataset mode."""
    return is_full_dataset(config)


def should_run_eps(config):
    """EPS analysis requires the EPS master file (full dataset)."""
    return is_full_dataset(config)


def get_instrument_path(config, instrument_key):
    """Return absolute path to an instrument data directory."""
    rel = config["instruments"][instrument_key]
    return os.path.join(config["resolved_paths"]["input_dir"], rel)


def get_master_file_path(config, master_key):
    """Return absolute path to a master Excel file (TSS, EPS, PSA, ...)."""
    rel = config["master_files"][master_key]
    return os.path.join(config["resolved_paths"]["input_dir"], rel)


def get_output_path(config, *parts):
    """Build an absolute output path and create parent directories if needed."""
    path = os.path.join(config["resolved_paths"]["output_dir"], *parts)
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    return path


def get_experiment_output_dir(config, experiment_id, plot_category):
    """Return output directory for a specific experiment plot category."""
    return get_output_path(config, experiment_id, plot_category)


def import_raw_df_from(file_paths):
    """Import and concatenate raw data from one or more Excel master files."""
    frames = [pd.read_excel(path) for path in file_paths]
    if len(frames) == 1:
        return frames[0]
    return pd.concat(frames, ignore_index=True)


def create_filelist(files_dir, skip="", meta_path=None, config=None):
    """Collect instrument files matching metadata experiment IDs."""
    if config is None:
        config = load_config()
    if meta_path is None:
        meta_path = config["resolved_paths"]["meta_data"]

    meta_df = pd.read_csv(meta_path)
    experiment_ids = config["resolved_paths"].get("experiment_ids")
    if experiment_ids:
        df_meta_id = pd.Series(experiment_ids)
    else:
        df_meta_id = meta_df.loc[meta_df["SAMPLE_INFORMATION"].isna(), "ID"]
    filtered_files = []

    for dir_path, _, files in os.walk(files_dir):
        if not os.path.basename(dir_path).startswith("CH"):
            continue
        for file in files:
            if skip in file:
                continue
            if not file.endswith((".xlsx", ".csv")):
                continue
            file_path = os.path.join(dir_path, file)
            if any(exp_id in file_path for exp_id in df_meta_id):
                filtered_files.append(file_path)

    return filtered_files


def formatting_strings(strings):
    """Normalize column names: uppercase, replace spaces and special chars."""
    new_strings = []
    for string in strings:
        formatted = string.translate(
            str.maketrans({" ": "_", "(": "", ")": "", "°": ""})
        ).upper()
        new_strings.append(formatted)
    return new_strings


def convert_types(df):
    """Apply standard type conversions used across measurement notebooks."""
    df = df.convert_dtypes()
    df["TIME"] = (df["TIME"].str.replace("-h", "").replace("-", "0")).astype(int)
    df["BIO_REP"] = df["BIO_REP"].astype("Int64")
    df["TEC_REP"] = df["TEC_REP"].astype("Int64")
    df.fillna(0, inplace=True)
    return df


def copy_start_control(df, meta_data, skip=None):
    """Duplicate t=0 control values for each sample category (except controls)."""
    if skip is None:
        skip = SKIP_SAMPLES
    merged_df = pd.DataFrame(df)
    for exp in meta_data["EXP_ABBR"].unique():
        if exp in skip:
            continue
        sub_df = df[df["EXPERIMENT_NAME"] == exp]
        start_control = sub_df[
            (sub_df["SAMPLE_NAME"] == "Control") & (sub_df["TIME"] == 0)
        ]
        for sample_name in sub_df["SAMPLE_NAME"].unique():
            if sample_name in ("Control", "VSS-Blank"):
                continue
            sample_control = start_control.assign(SAMPLE_NAME=sample_name)
            merged_df = pd.concat([merged_df, sample_control], ignore_index=True)
    return merged_df


def filter(df, time=None):
    """Remove unwanted time points (default: drop t=12 h)."""
    if not time:
        return df
    df.drop(df[df["TIME"].isin(time)].index, inplace=True)
    return df
