import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
from math import pi
from matplotlib.ticker import FormatStrFormatter
import statsmodels.api as sm

# Show regular expression in non-italic format - TODO Not working yet!
mpl.rcParams['mathtext.default'] = 'regular'

# Change font to Arial
# from matplotlib import rc
# font = {'size'   : 16}
# mpl.rc('font', **font)
# mpl.rcParams['font.sans-serif'] = "Comic Sans MS"
# mpl.rcParams['font.family'] = "sans-serif"

dark_color = "#464646"
mid_color = "#969696"
light_color = "#DCDCDC"

label_fontsize = 20 # 20 default for thesis - disputation: 25?

def check_timepoints(timepoints, base_color = light_color):
    # Change layout, if experiment is time-driven
    if timepoints > 1:
        return ["TIME", [dark_color, mid_color, light_color], None]
    else:
        return [None, None, base_color]   
def format_title(plot, title):
    #plot.text(0, 1.1, title, transform = plot.transAxes, fontsize = 15, va="center", ha="left")
    return plot
def format_axes(plot, show_x_label, x_labels, y_label, y_ticks, y_labelpad = None):
    # Formatting x axis
    plot.set_xlabel(None)
    plot.set_xticks(plot.get_xticks())
    plot.set_xticklabels(labels = x_labels, fontsize = label_fontsize, rotation = 0, ha = 'center', rotation_mode = 'anchor') # Optional for SC/BM: rotation -20, ha='left', rotation_mode='anchor'
    if not show_x_label: plot.tick_params(bottom=False)
    # Formatting y axis 
    plot.set_ylabel(y_label, fontsize = label_fontsize, labelpad = y_labelpad)
    plot.set_yticks(np.arange(y_ticks[0],y_ticks[1],y_ticks[2])) # y_ticks = y_min, y_max, y_step 
    plot.set_yticklabels(plot.get_yticks(), fontsize = label_fontsize)
    plot.set_ylim(y_ticks[0], y_ticks[1]- y_ticks[2]) # y_lim = y_max - y_step
    plot.grid(axis = "y")
    return plot
def format_legend(plot, timepoints, title = "time (h)", position = (1.175, 1)):
    if timepoints > 1:
        plot.legend(title = title, title_fontsize = 20, fontsize = 20, bbox_to_anchor = position, loc = "upper right", borderaxespad = 0, frameon = False)
        return plot
    else:
        #plot.get_legend().remove() # TODO Bug with boxplots / bar plots
        return plot
def format_extratext(plot, n):
    # Insert n = n right top of the plot
    #plot.text(0.895, 1.01 , "n = " + str(n), transform = plot.transAxes, fontsize = 20)
    return plot
def save_plot(plot, file_name):
    # Export each file to tiff and svg image
    plot.get_figure().savefig("../exports/" + file_name + ".svg", bbox_inches = "tight")
    plot.get_figure().savefig("../exports/" + file_name + ".tiff", bbox_inches = "tight")
    return plt.close()


# Boxplots
def visualize_boxplot(sub_df, sub_meta, show_x_label, y_data, y_ticks, y_label, y_labelpad = None):
    # Get layout information for current subset
    hue_params = check_timepoints(sub_df["TIME"].nunique(), )
    title = sub_meta["EXP_FULL"][0]
    x_labels = sub_meta["SAMPLES_APPENDIX"][0].split(",")
    x_order = sub_meta["SAMPLES_ORDER"][0].split(",")
    n = sub_df["BIO_REP"].max()
    if not show_x_label: x_labels = "" # Optional: for RR and SV graphs

    # Create subset plot
    plt.figure(figsize = (10, 7), dpi = 100) # Plot dimensions # Optional 7 for sinking properties / 10 as default
    with sns.axes_style("ticks"):
        boxplot = sns.boxplot(data = sub_df,
                                x = "SAMPLE_NAME", # x-axis data
                                y = y_data, # y-axis data
                                hue = hue_params[0], # group by time conditionally
                                palette = hue_params[1], # color palette
                                color = hue_params[2], # color for non time plots
                                linecolor = "black", # framecolor of boxes
                                order = x_order, # sample order
        )
    
    format_title(boxplot, title)
    format_axes(boxplot, show_x_label, x_labels, y_label, y_ticks, y_labelpad)
    format_legend(boxplot, timepoints = sub_df["TIME"].nunique())
    format_extratext(boxplot, n)

    plt.legend([],[], frameon=False)
    
    # Export and close
    pos_marker = -1
    if "^" in y_label:
        pos_marker = -2
    measurement = "-".join(y_label.split(" ")[:pos_marker])
    file_name = "Disputation-Plots" + "/Boxplot_" + sub_meta["EXP_ABBR"][0] + "_" + measurement # <- for disputation
    #file_name = "Boxplots" + measurement + "/Boxplot_" + sub_meta["EXP_ABBR"][0] + "_" + measurement # <- for thesis
     
    
    if measurement != "Zeta-Potential":
        [boxplot.axvline(x + 0.5,linewidth = 0.5, color = 'k') for x in boxplot.get_xticks()]
    
    save_plot(boxplot, file_name)
    
    return print(f"Boxplot \"{sub_meta['EXP_FULL'][0]}\" created and saved.")
    

# Barplots
def visualize_barplot(sub_df, sub_meta, y_data, y_label, y_ticks, y_labelpad = None):
    # Get group information for current subset
    hue_params = check_timepoints(sub_df["TIME"].nunique(), base_color = dark_color)

    plt.figure(figsize = (10, 7), dpi = 100) # Plot dimensions
    with sns.axes_style("ticks"):
        barTSS = sns.barplot(data = sub_df,
                    x = "SAMPLE_NAME",
                    y = y_data[0], # TSS Data
                    hue = hue_params[0], palette = hue_params[1], color = hue_params[2], edgecolor = "#262626", # Grouping
                    err_kws= {"linewidth": 0.5, "color": "#262626"}, capsize = 0.25, # Error bars
                    order = sub_meta["SAMPLES_ORDER"][0].split(","),) # Ordering
        #barVSS = sns.barplot(data = sub_df,
        #            x = "SAMPLE_NAME",
        #            y = y_data[1], # VSS Data
        #            hue = hue_params[0], palette = hue_params[1], color = hue_params[2], edgecolor = "#C8C8C8", # Grouping
        #            err_kws= {"linewidth": 0.5, "color": "#C8C8C8"}, capsize = 0.25, hatch = "////", # Error bars
        #            legend = False,) # Delete 2. legend
        
    #format_title(barTSS, sub_meta["EXP_FULL"][0])
    format_axes(barTSS, show_x_label = True, x_labels = sub_meta["SAMPLES_APPENDIX"][0].split(","), y_label = y_label, y_ticks = y_ticks, y_labelpad = y_labelpad)
    format_legend(barTSS, timepoints = sub_df["TIME"].nunique())
    format_extratext(barTSS, n = sub_df["BIO_REP"].max())
    
    plt.legend([],[], frameon=False)
    
    # Export and close
    prefix = "Abs-" # Choose between relative and absolute naming
    if "%" in str(y_label): prefix = "Rel-"
    
    pos_marker = -1
    if "^" in y_label:
        pos_marker = -2
    
    measurement = "-".join(y_label.split(" ")[:pos_marker])
    file_name = "Disputation-Plots" + "/Barplot_" + sub_meta["EXP_ABBR"][0] + "_" + prefix + measurement
    #file_name = "Barplots_" + measurement + "/Barplot_" + sub_meta["EXP_ABBR"][0] + "_" + prefix + measurement
    save_plot(barTSS, file_name)
    
    return print(f"{prefix}Barplot \"{sub_meta['EXP_FULL'][0]}\" created and saved.")


# Radarplots
def visualize_radarplotseries(sub_exp_df, sub_meta,
                              DISPLAY_TITLE, 
                              TOGGLE_TYPE, ALIGNMENT,
                              PLOT_AXESCOLOR, PLOT_FACECOLOR, PLOT_FONTCOLOR):
    # Normalizes data to make it suitable to one plot
    def _scale_data(data, ranges):
        """scales data[1:] to ranges[0]"""
        for d, (y1, y2) in zip(data[1:], ranges[1:]):
            assert (y1 <= d <= y2) or (y2 <= d <= y1)
        x1, x2 = ranges[0]
        d = data[0]
        sdata = [d]
        for d, (y1, y2) in zip(data[1:], ranges[1:]):
            sdata.append((d-y1) / (y2-y1) 
                        * (x2 - x1) + x1)
        return sdata

    # Masterclass for single radar plot
    class ComplexRadar():
        def __init__(self, fig, variables, ranges, name="undefined", rect=None, n_ordinate_levels=6):
            angles = np.arange(0, 360, 360./len(variables))
            if rect is None:
                rect = [0.1, 0.1, 0.9, 0.9]
            # Add axes to polar plot
            #self.axes = [fig.add_axes(rect, projection="polar", label="axes%d" % i) for i in range(self.n)]
            axes = [fig.add_axes(rect,polar=True,
                    label = "axes{}".format(i)) 
                    for i in range(len(variables))]
            # axes = [fig.add_axes([0.1,0.1,0.9,0.9],polar=True,
            #         label = "axes{}".format(i)) 
            #         for i in range(len(variables))]
            # Handle for ylabels (Categories)
            l, text = axes[0].set_thetagrids(angles, 
                                            labels=variables,
                                            fontsize = 30)
            [txt.set_rotation(angle-90) for txt, angle 
                in zip(text, angles)]
            # Make delete multiple grids
            for ax in axes[1:]:
                ax.patch.set_visible(False)
                ax.grid("off")
                ax.xaxis.set_visible(False)
            # Create y axes
            for i, ax in enumerate(axes):
                grid = np.linspace(*ranges[i], num=n_ordinate_levels)
                gridlabel = [x.astype(int) for x in grid]
                # Convert sinking velocity to float values
                if i == 1:
                    for label in gridlabel:
                        gridlabel[label] = gridlabel[label].astype(float)
                # Get rid of multiple 0s
                if i == 1 or i == 2:
                    gridlabel[0] = "" # clean up origin
                    ax.set_rgrids(grid, 
                            labels=gridlabel,
                            angle=angles[i],
                            fontsize = 25,
                            ha = "right",
                            color = PLOT_FONTCOLOR)
                else:
                    ax.set_rgrids(grid, 
                            labels=gridlabel,
                            angle=angles[i],
                            fontsize = 25,
                            ha = "left",
                            color = PLOT_FONTCOLOR)
                # Turn first axis is to top
                ax.set_theta_offset(pi / 2) 
                # Set specified y limitations
                ax.set_ylim(*ranges[i])
                # Padding for categories and rotate labels and ticks accordingly
                ax.tick_params(pad=50,rotation='auto')
                # Color grids
                ax.yaxis.grid(color=PLOT_AXESCOLOR)
                ax.xaxis.grid(color=PLOT_AXESCOLOR)
                ax.set_facecolor(PLOT_FACECOLOR)
                
                axes[0].text(0.5, -0.11, name, transform = axes[0].transAxes, fontsize = 40, va="center", ha="center") # TODO Make generic
                
            # Variables for plotting
            self.angle = np.deg2rad(np.r_[angles, angles[0]])
            self.ranges = ranges
            self.ax = axes[0]
        # Plot data to radar spine
        def plot(self, data, *args, **kw):
            for value in data:
                sdata = _scale_data(value, self.ranges)
                self.ax.plot(self.angle, np.r_[sdata, sdata[0]], *args, **kw)
        # Fill triangles with color
        def fill(self, data, *args, **kw):
            #color_palette = ["#5C5C5C", "#939393", "#C9C9C9"] # for time
            color_palette = [dark_color, mid_color, light_color]
            #color_palette = ["#262626", "#4A4A4A", "#6F6F6F", "#939393", "#B7B7B7", "#DBDBDB", "#FFFFFF"] # for samples
            # Inverts data if samples are gaining sinking properties by sum of all three categories for aesthetical reasons
            sum_data = [sum(tup) for tup in data]
            if sum_data[len(sum_data)-1] > sum_data[0]:
                data.reverse()
                color_palette.reverse()
            for i, value in enumerate(data):
                sdata = _scale_data(value, self.ranges)
                self.ax.fill(self.angle, np.r_[sdata, sdata[0]], *args, **kw, color=color_palette[i])

    # Constant categories and ylim ranges
    categories = ("Recovery Rate [%]", "Sinking Velocity [m\u0020" + r"${h^{-1}}$]", "Particle Size [µm]")
    ylim_ranges = [(0, 100), (0, 5), (0, 1000)] # Recovery Rate, Sinking Velocity, Particle Size

    # Create single radar plot with one experiment line
    fig = plt.figure(figsize=(20, 10), dpi=200)
    rect=[0.1,0.1, 0.35,0.8] # starting rectangle position
    for index, sample in enumerate(sub_exp_df[TOGGLE_TYPE].unique()):
        print(f"Creating single radar plot for: {sample}")
        # Single sample data subset
        sub_sam_df = sub_exp_df[sub_exp_df[TOGGLE_TYPE] == sample]
        # Convert into readable tuples for radar class
        plot_sub_df = list(sub_sam_df.iloc[:,3:].itertuples(index=False, name=None)) 
        # Extract fully formatted sample name from meta data
        print(sub_meta["SAMPLES_APPENDIX"][0].split(",")[index])
        sam_name = sub_meta["SAMPLES_APPENDIX"][0].split(",")[index]
        # Create radar plot
        radar = ComplexRadar(fig, categories, ylim_ranges, name=sam_name, rect=rect)
        # Plot data into current radar plot
        radar.plot(data = plot_sub_df, color = PLOT_AXESCOLOR, linewidth=1)
        radar.fill(data = plot_sub_df, alpha=1.0)
        # Move rectangle to next plot position in figure depending on desired alignment
        if ALIGNMENT == "Horizontal":
            rect[0] = rect[0] + 0.5
        elif ALIGNMENT == "Vertical":
            rect[1] = rect[1] - 1.0
    
    # Title for current experiment
    if DISPLAY_TITLE:
        exp_name = sub_meta["EXP_FULL"][0]
        fig.text(0.125, 1, exp_name, fontsize = 20, va="center", ha="center")
    
    # Replicates   
    #n = 3
    #if "CC" in sub_exp_df["EXPERIMENT_NAME"].values:
    #    n = 5
    #fig.text(3.46, 0.9, "n = " + str(n), fontsize = 35, va="center", ha="center")
        
    # Get correct file ending
    if TOGGLE_TYPE == "SAMPLE_NAME": appendix = "By-Samples"
    if TOGGLE_TYPE == "TIME": appendix = "By-Time"
    # Export
    file_name = "Radarplots_Sinking-Properties/" + ALIGNMENT + "_" + appendix + "/Radarplot_" + sub_meta["EXP_ABBR"][0] + "_Sinking-Properties-" + ALIGNMENT + "-" + appendix
    save_plot(fig, file_name)
    
    return print(f"Radar-Series \"{sub_meta['EXP_ABBR'][0]}\" created and saved.")


# Heatmaps
def visualize_heatmaps(df1, df2, df3, id):    
    # Base plot
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize = (10,10), dpi = 200) # Optional: only with HA-Plots tweak to 3 instead of 10 and 1,3 instead 3,1
    # Create each plot
    sns.heatmap(df1.T, cmap = "Greens", ax = ax1, cbar = True, vmin = 0, vmax = 100, cbar_kws = {"label": "Relative Abundance [%]"},) # Microalgae
    sns.heatmap(df2.T, cmap = "Blues", ax = ax2, cbar = True, vmin = 0, vmax = 100, cbar_kws = {"label": "Relative Abundance [%]"},) # Cyanobacteria
    sns.heatmap(df3.T, cmap = "Oranges", ax = ax3, cbar = True, vmin = 0, vmax = 100, cbar_kws = {"label": "Relative Abundance [%]"},) # Bacteria
    
    ax1.set()
    
    # hide axes of ax2 and ax3 and move ax1 to top with rotation
    ax1.set_xticklabels(ax1.get_xticklabels(), rotation = 45, ha = "left", rotation_mode='anchor')
    ax1.xaxis.tick_top()
    #ax1.set(xticks=[]) # Optional: only with HA-Plots
    ax2.set(xticks=[])
    ax3.set(xticks=[])
    ax1.set(xticks=[]) # <- only relevant for CH230117
    
    # drawing the frames 
    for _, spine in ax1.spines.items(): 
        spine.set_visible(True) 
        spine.set_linewidth(0.5) 
    for _, spine in ax2.spines.items(): 
        spine.set_visible(True) 
        spine.set_linewidth(0.5) 
    for _, spine in ax3.spines.items(): 
        spine.set_visible(True) 
        spine.set_linewidth(0.5) 

    # aspect ratio set to equal
    ax1.set_aspect("equal")
    ax2.set_aspect("equal")
    ax3.set_aspect("equal")
    
    # custom text to define which taxa group is shown
    #ax1.text(-0.11, 1.05, "Microalgae", weight = "bold", transform = ax1.transAxes, fontsize = 10, va="center", ha="center")
    #ax2.text(-0.11, 1.05, "Cyanobacteria", weight = "bold", transform = ax2.transAxes, fontsize = 10, va="center", ha="center")
    #ax3.text(-0.11, 1.05, "other Bacteria", weight = "bold", transform = ax3.transAxes, fontsize = 10, va="center", ha="center")
    
    # Toggle off, if not title is needed
    #ax1.text(-1.5, -4, id, fontsize = 10, va="center", ha="right")

    if id == "CH-Physiology":
        vline_pos = [6, 12, 18, 24]
    elif id == "CH230921":
        vline_pos = [3, 6]
    else: 
        vline_pos = [6]
    for pos in vline_pos:
        ax1.axvline(x=pos, linewidth=0.5, color="k")
        ax2.axvline(x=pos, linewidth=0.5, color="k")
        ax3.axvline(x=pos, linewidth=0.5, color="k")

    # Optional: only with HA-Plots
    #plt.subplots_adjust(left=0.1, bottom=0.1, right=0.9, top=0.9, wspace=0.5, hspace=0.4)
    
    # Export and close
    file_name = "Heatmaps_Taxa-Distribution/Heatmap_" + id + "_Taxa-Distribution-VA"
    save_plot(fig, file_name)
 
    return print(f"Heatmap \"" + id + "\" created and saved.")


# PCA-Plots
def visualize_pcaplot(sub_df, id, PHY_LABELS, PC1, scale_PC1, var_PC1, PC2, scale_PC2, var_PC2, style = None): 
    plt.figure(figsize = (10, 10), dpi = 200) # pcaplot dimensions
    with sns.axes_style("ticks"):
        pcaplot = sns.scatterplot(data = sub_df,
                    x = PC1 * scale_PC1,
                    y = PC2 * scale_PC2,
                    color = "k",
                    style = style,
                    s = 200,
                    )

    for i, label in enumerate(sub_df["SAMPLE_NAME"]):
        if id == "CH230921":
            if i % 3 == 0:
                plt.text(x = PC1[i] * scale_PC1,
                       y = PC2[i] * scale_PC2 - 0.05,
                       s = str(label),
                       fontsize = 15, ha = "center")
        elif (str(label) in PHY_LABELS) | (id != "CH-Physiology"):
            plt.text(x = PC1[i] * scale_PC1,
                    y = PC2[i] * scale_PC2 - 0.05,
                    s = str(label),
                    fontsize = 15, ha = "center")

    # Formatting x axis
    pcaplot.set_xlabel(f"PC1 - {var_PC1} % variance", fontsize = 25, labelpad = 15)
    pcaplot.set_xticks(pcaplot.get_xticks())
    pcaplot.set_xticklabels(pcaplot.get_xticks(), fontsize = 15)
    pcaplot.xaxis.set_major_formatter(FormatStrFormatter('%.1f'))
    # Formatting y axis 
    pcaplot.set_yticks(pcaplot.get_yticks())
    pcaplot.set_ylabel(f"PC2 - {var_PC2} % variance", fontsize = 25, labelpad = 15)
    pcaplot.set_yticklabels(pcaplot.get_yticks(), fontsize = 15)
    pcaplot.yaxis.set_major_formatter(FormatStrFormatter('%.1f'))
    pcaplot.grid()

    # Standard title
    format_title(pcaplot, id)
    # Change legend position depending on experiment id
    if id == "CH-Physiology":
       leg_pos = (1.54, 1)
    else:
       leg_pos = (1.38, 1)
    #format_legend(pcaplot, timepoints = sub_df["TIME"].nunique(), title = None, position = leg_pos)
    if id != "CHcontrol":
        pcaplot.get_legend().remove()

    # Export
    file_name = "PCA-Plots_Taxa-Variance/PCA-Plot_" + id + "_Taxa-Variance"
    save_plot(pcaplot, file_name)
    
    return print(f"PCA-Plot \"{id}\" created and saved.")
    

# Screeplots
def visualize_screeplot(id, x_axis, y_axis):
    plt.figure(figsize = (4, 2), dpi = 200)
    plt.plot(x_axis, y_axis, "ro-")
    plt.title(f"{id} - Scree Plot (Elbow Method)", fontsize = 10)
    plt.xlabel("Component Number", fontsize = 10)
    plt.ylabel("Proportion of Variance", fontsize = 10)
    plt.grid()
    # Export as .png
    png_file = "../exports/PCA-plots_Next-Generation-Sequencing/Screeplots/Screeplot_" + id + ".png"
    plt.savefig(png_file, bbox_inches = "tight")
    plt.close()
    
    return print(f"Scree-Plot \"{id}\" created and saved.")


# QQ-Plot
def visualize_qqplot(title = "Unknown", data = None):
    sm.qqplot(data, line = "q", fit = "True")
    plt.title(title)
    
    # Export
    png_file = "../exports/Raw-Data/Data-Statistics/QQ-Plots/QQ-Plots_" + title + "_Normal-Distribution"
    plt.savefig(png_file, bbox_inches = "tight")
    plt.close()
    #file_name = "Raw-Data/Data-Statistics/QQ-Plots" + id + "_Normal-Distribution"
    #save_plot(pcaplot, file_name)
    
    return print(f"QQ-Plot \"{title}\" created and saved.")