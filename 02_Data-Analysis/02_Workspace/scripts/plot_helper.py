import os
from math import pi

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import statsmodels.api as sm
from matplotlib.ticker import FormatStrFormatter

from .constants import (
    DARK_COLOR,
    LABEL_FONTSIZE,
    LIGHT_COLOR,
    MEASUREMENT_PLOT_DIRS,
    MID_COLOR,
)
from .data_helper import get_output_path, load_config

mpl.rcParams["mathtext.default"] = "regular"

_CONFIG = None

dark_color = DARK_COLOR
mid_color = MID_COLOR
light_color = LIGHT_COLOR
label_fontsize = LABEL_FONTSIZE


def set_config(config):
    """Store active pipeline config for plot output paths."""
    global _CONFIG
    _CONFIG = config


def _active_config():
    if _CONFIG is not None:
        return _CONFIG
    return load_config()


def _measurement_from_label(y_label):
    pos_marker = -2 if "^" in y_label else -1
    return "-".join(y_label.split(" ")[:pos_marker])


def _experiment_id(sub_meta):
    return sub_meta["ID"][0]


def _plot_relative_path(sub_meta, plot_category, filename):
    return os.path.join(_experiment_id(sub_meta), plot_category, filename)


def check_timepoints(timepoints, base_color=light_color):
    if timepoints > 1:
        return ["TIME", [dark_color, mid_color, light_color], None]
    return [None, None, base_color]


def format_title(plot, title):
    return plot


def format_axes(plot, show_x_label, x_labels, y_label, y_ticks, y_labelpad=None):
    plot.set_xlabel(None)
    ticks = plot.get_xticks()
    plot.set_xticks(ticks)
    if isinstance(x_labels, list) and len(x_labels) != len(ticks):
        if len(x_labels) > len(ticks):
            x_labels = x_labels[: len(ticks)]
        else:
            x_labels = list(x_labels) + [""] * (len(ticks) - len(x_labels))
    plot.set_xticklabels(
        labels=x_labels,
        fontsize=label_fontsize,
        rotation=0,
        ha="center",
        rotation_mode="anchor",
    )
    if not show_x_label:
        plot.tick_params(bottom=False)
    plot.set_ylabel(y_label, fontsize=label_fontsize, labelpad=y_labelpad)
    plot.set_yticks(np.arange(y_ticks[0], y_ticks[1], y_ticks[2]))
    plot.set_yticklabels(plot.get_yticks(), fontsize=label_fontsize)
    plot.set_ylim(y_ticks[0], y_ticks[1] - y_ticks[2])
    plot.grid(axis="y")
    return plot


def format_legend(plot, timepoints, title="time (h)", position=(1.175, 1)):
    if timepoints > 1:
        plot.legend(
            title=title,
            title_fontsize=20,
            fontsize=20,
            bbox_to_anchor=position,
            loc="upper right",
            borderaxespad=0,
            frameon=False,
        )
    return plot


def format_extratext(plot, n):
    return plot


def save_plot(plot, relative_path, config=None):
    """Save plot as SVG and TIFF under the configured output directory."""
    if config is None:
        config = _active_config()

    full_path = get_output_path(config, relative_path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)

    figure = plot if hasattr(plot, "savefig") else plot.get_figure()
    figure.savefig(full_path + ".svg", bbox_inches="tight")
    figure.savefig(full_path + ".tiff", bbox_inches="tight")
    plt.close(figure)
    return None


def visualize_boxplot(
    sub_df, sub_meta, show_x_label, y_data, y_ticks, y_label, y_labelpad=None
):
    hue_params = check_timepoints(sub_df["TIME"].nunique())
    title = sub_meta["EXP_FULL"][0]
    x_labels = sub_meta["SAMPLES_APPENDIX"][0].split(",")
    x_order = sub_meta["SAMPLES_ORDER"][0].split(",")
    n = sub_df["BIO_REP"].max()
    if not show_x_label:
        x_labels = ""

    plt.figure(figsize=(10, 7), dpi=100)
    with sns.axes_style("ticks"):
        boxplot = sns.boxplot(
            data=sub_df,
            x="SAMPLE_NAME",
            y=y_data,
            hue=hue_params[0],
            palette=hue_params[1],
            color=hue_params[2],
            linecolor="black",
            order=x_order,
        )

    format_title(boxplot, title)
    format_axes(boxplot, show_x_label, x_labels, y_label, y_ticks, y_labelpad)
    format_legend(boxplot, timepoints=sub_df["TIME"].nunique())
    format_extratext(boxplot, n)
    plt.legend([], [], frameon=False)

    measurement = _measurement_from_label(y_label)
    plot_category = MEASUREMENT_PLOT_DIRS.get(measurement, f"Boxplots_{measurement}")
    filename = f"Boxplot_{sub_meta['EXP_ABBR'][0]}_{measurement}"

    if measurement != "Zeta-Potential":
        for x in boxplot.get_xticks():
            boxplot.axvline(x + 0.5, linewidth=0.5, color="k")

    save_plot(boxplot, _plot_relative_path(sub_meta, plot_category, filename))
    return print(f'Boxplot "{sub_meta["EXP_FULL"][0]}" created and saved.')


def visualize_barplot(sub_df, sub_meta, y_data, y_label, y_ticks, y_labelpad=None):
    hue_params = check_timepoints(sub_df["TIME"].nunique(), base_color=dark_color)

    plt.figure(figsize=(10, 7), dpi=100)
    with sns.axes_style("ticks"):
        bar_plot = sns.barplot(
            data=sub_df,
            x="SAMPLE_NAME",
            y=y_data[0],
            hue=hue_params[0],
            palette=hue_params[1],
            color=hue_params[2],
            edgecolor="#262626",
            err_kws={"linewidth": 0.5, "color": "#262626"},
            capsize=0.25,
            order=sub_meta["SAMPLES_ORDER"][0].split(","),
        )

    format_axes(
        bar_plot,
        show_x_label=True,
        x_labels=sub_meta["SAMPLES_APPENDIX"][0].split(","),
        y_label=y_label,
        y_ticks=y_ticks,
        y_labelpad=y_labelpad,
    )
    format_legend(bar_plot, timepoints=sub_df["TIME"].nunique())
    format_extratext(bar_plot, n=sub_df["BIO_REP"].max())
    plt.legend([], [], frameon=False)

    prefix = "Rel-" if "%" in str(y_label) else "Abs-"
    measurement = _measurement_from_label(y_label)
    if measurement.startswith("Total-"):
        plot_category = MEASUREMENT_PLOT_DIRS["Total-Suspended-Solids"]
    else:
        plot_category = MEASUREMENT_PLOT_DIRS["Suspended-Solids"]

    filename = f"Barplot_{sub_meta['EXP_ABBR'][0]}_{prefix}{measurement}"
    save_plot(bar_plot, _plot_relative_path(sub_meta, plot_category, filename))
    return print(f'{prefix}Barplot "{sub_meta["EXP_FULL"][0]}" created and saved.')


def visualize_radarplotseries(
    sub_exp_df,
    sub_meta,
    display_title,
    toggle_type,
    alignment,
    plot_axescolor,
    plot_facecolor,
    plot_fontcolor,
):
    def _scale_data(data, ranges):
        for d, (y1, y2) in zip(data[1:], ranges[1:]):
            assert (y1 <= d <= y2) or (y2 <= d <= y1)
        x1, x2 = ranges[0]
        d = data[0]
        sdata = [d]
        for d, (y1, y2) in zip(data[1:], ranges[1:]):
            sdata.append((d - y1) / (y2 - y1) * (x2 - x1) + x1)
        return sdata

    class ComplexRadar:
        def __init__(self, fig, variables, ranges, name="undefined", rect=None, n_ordinate_levels=6):
            angles = np.arange(0, 360, 360.0 / len(variables))
            if rect is None:
                rect = [0.1, 0.1, 0.9, 0.9]
            axes = [
                fig.add_axes(rect, polar=True, label=f"axes{i}")
                for i in range(len(variables))
            ]
            _, text = axes[0].set_thetagrids(angles, labels=variables, fontsize=30)
            for txt, angle in zip(text, angles):
                txt.set_rotation(angle - 90)
            for ax in axes[1:]:
                ax.patch.set_visible(False)
                ax.grid("off")
                ax.xaxis.set_visible(False)
            for i, ax in enumerate(axes):
                grid = np.linspace(*ranges[i], num=n_ordinate_levels)
                gridlabel = [x.astype(int) for x in grid]
                if i == 1:
                    for label in gridlabel:
                        gridlabel[label] = gridlabel[label].astype(float)
                if i in (1, 2):
                    gridlabel[0] = ""
                    ha = "right"
                else:
                    ha = "left"
                ax.set_rgrids(
                    grid,
                    labels=gridlabel,
                    angle=angles[i],
                    fontsize=25,
                    ha=ha,
                    color=plot_fontcolor,
                )
                ax.set_theta_offset(pi / 2)
                ax.set_ylim(*ranges[i])
                ax.tick_params(pad=50, rotation="auto")
                ax.yaxis.grid(color=plot_axescolor)
                ax.xaxis.grid(color=plot_axescolor)
                ax.set_facecolor(plot_facecolor)
                axes[0].text(
                    0.5,
                    -0.11,
                    name,
                    transform=axes[0].transAxes,
                    fontsize=40,
                    va="center",
                    ha="center",
                )
            self.angle = np.deg2rad(np.r_[angles, angles[0]])
            self.ranges = ranges
            self.ax = axes[0]

        def plot(self, data, *args, **kw):
            for value in data:
                sdata = _scale_data(value, self.ranges)
                self.ax.plot(self.angle, np.r_[sdata, sdata[0]], *args, **kw)

        def fill(self, data, *args, **kw):
            color_palette = [dark_color, mid_color, light_color]
            sum_data = [sum(tup) for tup in data]
            if sum_data[-1] > sum_data[0]:
                data.reverse()
                color_palette.reverse()
            for i, value in enumerate(data):
                sdata = _scale_data(value, self.ranges)
                self.ax.fill(
                    self.angle, np.r_[sdata, sdata[0]], *args, **kw, color=color_palette[i]
                )

    categories = (
        "Recovery Rate [%]",
        "Sinking Velocity [m\u0020" + r"${h^{-1}}$]",
        "Particle Size [µm]",
    )
    ylim_ranges = [(0, 100), (0, 5), (0, 1000)]

    fig = plt.figure(figsize=(20, 10), dpi=200)
    rect = [0.1, 0.1, 0.35, 0.8]
    for index, sample in enumerate(sub_exp_df[toggle_type].unique()):
        print(f"Creating single radar plot for: {sample}")
        sub_sam_df = sub_exp_df[sub_exp_df[toggle_type] == sample]
        plot_sub_df = list(sub_sam_df.iloc[:, 3:].itertuples(index=False, name=None))
        sam_name = sub_meta["SAMPLES_APPENDIX"][0].split(",")[index]
        radar = ComplexRadar(fig, categories, ylim_ranges, name=sam_name, rect=rect)
        radar.plot(data=plot_sub_df, color=plot_axescolor, linewidth=1)
        radar.fill(data=plot_sub_df, alpha=1.0)
        if alignment == "Horizontal":
            rect[0] = rect[0] + 0.5
        elif alignment == "Vertical":
            rect[1] = rect[1] - 1.0

    if display_title:
        fig.text(0.125, 1, sub_meta["EXP_FULL"][0], fontsize=20, va="center", ha="center")

    plot_category = MEASUREMENT_PLOT_DIRS["Sinking-Properties"]
    filename = (
        f"Radarplot_{sub_meta['EXP_ABBR'][0]}_Sinking-Properties_{alignment}-Alignment"
    )
    save_plot(fig, _plot_relative_path(sub_meta, plot_category, filename))
    return print(f'Radar-Series "{sub_meta["EXP_ABBR"][0]}" created and saved.')


def visualize_heatmaps(df1, df2, df3, experiment_id):
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 10), dpi=200)
    sns.heatmap(
        df1.T,
        cmap="Greens",
        ax=ax1,
        cbar=True,
        vmin=0,
        vmax=100,
        cbar_kws={"label": "Relative Abundance [%]"},
    )
    sns.heatmap(
        df2.T,
        cmap="Blues",
        ax=ax2,
        cbar=True,
        vmin=0,
        vmax=100,
        cbar_kws={"label": "Relative Abundance [%]"},
    )
    sns.heatmap(
        df3.T,
        cmap="Oranges",
        ax=ax3,
        cbar=True,
        vmin=0,
        vmax=100,
        cbar_kws={"label": "Relative Abundance [%]"},
    )

    ax1.set()
    ax1.set_xticklabels(ax1.get_xticklabels(), rotation=45, ha="left", rotation_mode="anchor")
    ax1.xaxis.tick_top()
    ax2.set(xticks=[])
    ax3.set(xticks=[])
    ax1.set(xticks=[])

    for ax in (ax1, ax2, ax3):
        for _, spine in ax.spines.items():
            spine.set_visible(True)
            spine.set_linewidth(0.5)
        ax.set_aspect("equal")

    if experiment_id == "CH-Physiology":
        vline_pos = [6, 12, 18, 24]
    elif experiment_id == "CH230921":
        vline_pos = [3, 6]
    else:
        vline_pos = [6]
    for pos in vline_pos:
        for ax in (ax1, ax2, ax3):
            ax.axvline(x=pos, linewidth=0.5, color="k")

    relative_path = os.path.join(
        "Taxa-Distribution",
        f"Heatmap_{experiment_id}_Taxa-Distribution",
    )
    save_plot(fig, relative_path)
    return print(f'Heatmap "{experiment_id}" created and saved.')


def visualize_pcaplot(
    sub_df,
    experiment_id,
    phy_labels,
    pc1,
    scale_pc1,
    var_pc1,
    pc2,
    scale_pc2,
    var_pc2,
    style=None,
):
    plt.figure(figsize=(10, 10), dpi=200)
    with sns.axes_style("ticks"):
        pcaplot = sns.scatterplot(
            data=sub_df,
            x=pc1 * scale_pc1,
            y=pc2 * scale_pc2,
            color="k",
            style=style,
            s=200,
        )

    for i, label in enumerate(sub_df["SAMPLE_NAME"]):
        if experiment_id == "CH230921":
            if i % 3 == 0:
                plt.text(
                    x=pc1[i] * scale_pc1,
                    y=pc2[i] * scale_pc2 - 0.05,
                    s=str(label),
                    fontsize=15,
                    ha="center",
                )
        elif (str(label) in phy_labels) or (experiment_id != "CH-Physiology"):
            plt.text(
                x=pc1[i] * scale_pc1,
                y=pc2[i] * scale_pc2 - 0.05,
                s=str(label),
                fontsize=15,
                ha="center",
            )

    pcaplot.set_xlabel(f"PC1 - {var_pc1} % variance", fontsize=25, labelpad=15)
    pcaplot.set_xticks(pcaplot.get_xticks())
    pcaplot.set_xticklabels(pcaplot.get_xticks(), fontsize=15)
    pcaplot.xaxis.set_major_formatter(FormatStrFormatter("%.1f"))
    pcaplot.set_yticks(pcaplot.get_yticks())
    pcaplot.set_ylabel(f"PC2 - {var_pc2} % variance", fontsize=25, labelpad=15)
    pcaplot.set_yticklabels(pcaplot.get_yticks(), fontsize=15)
    pcaplot.yaxis.set_major_formatter(FormatStrFormatter("%.1f"))
    pcaplot.grid()

    format_title(pcaplot, experiment_id)
    if experiment_id != "CHcontrol":
        pcaplot.get_legend().remove()

    relative_path = os.path.join(
        "Taxa-Variance",
        f"PCA-Plot_{experiment_id}_Taxa-Variance",
    )
    save_plot(pcaplot, relative_path)
    return print(f'PCA-Plot "{experiment_id}" created and saved.')


def visualize_screeplot(experiment_id, x_axis, y_axis):
    plt.figure(figsize=(4, 2), dpi=200)
    plt.plot(x_axis, y_axis, "ro-")
    plt.title(f"{experiment_id} - Scree Plot (Elbow Method)", fontsize=10)
    plt.xlabel("Component Number", fontsize=10)
    plt.ylabel("Proportion of Variance", fontsize=10)
    plt.grid()
    relative_path = os.path.join(
        "Taxa-Variance",
        "Screeplots",
        f"Screeplot_{experiment_id}",
    )
    save_plot(plt.gcf(), relative_path)
    return print(f'Scree-Plot "{experiment_id}" created and saved.')


def visualize_qqplot(title="Unknown", data=None):
    sm.qqplot(data, line="q", fit=True)
    plt.title(title)
    relative_path = os.path.join(
        "Raw-Data",
        "Data-Statistics",
        "QQ-Plots",
        f"QQ-Plots_{title}_Normal-Distribution",
    )
    save_plot(plt.gcf(), relative_path)
    return print(f'QQ-Plot "{title}" created and saved.')
