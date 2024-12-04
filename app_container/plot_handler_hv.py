from json import tool
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np
import holoviews as hv # type: ignore
from holoviews import opts # type: ignore
from bokeh.models import HoverTool
import panel as pn
import colorcet as cc 

def create_subplots(row):
    pressureR = row['pressure']
    pressureT = row['pressureT']
    speedR = row['speed']
    speedT = row['speedT']
    time = row['time']
    peaksP = row['peaksP']
    max_peak_timeP = row['max_peak_timeP']
    max_peak_valueP = row['max_peak_valueP']
    # rise_timeP = row['rise_timeP']
    # settling_timeP = row['settling_timeP']
    # rise_timeS = row['rise_timeS']
    # settling_timeS = row['settling_timeS']

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 6))
    
    # Plot pressure vs time
    ax1.plot(time, pressureR, label='Real Pressure', color='blue')
    ax1.plot(time, pressureT, label='Target Pressure', color='red')
    ax1.set_xlabel('Time')
    ax1.set_ylabel('Pressure')
    ax1.set_title(f"Test {row['test_id']} - Pressure vs Time")
    ax1.plot(time[peaksP], np.array(pressureR)[peaksP], 'x', label='Peaks', color='green')
    ax1.axvline(x=max_peak_timeP, color='black', linestyle='--', label='Max Peak Time (Pressure)')
    
    # if not np.isnan(rise_timeP):
    #     ax1.axvline(x=rise_timeP, color='orange', linestyle='--', label='Rise Time (Pressure)')
    # if not np.isnan(settling_timeP):
    #     ax1.axvline(x=settling_timeP, color='purple', linestyle='--', label='Settling Time (Pressure)')
    ax1.legend()

    # Plot speed vs time
    ax2.plot(time, speedR, label='Real Speed', color='blue')
    ax2.plot(time, speedT, label='Target Speed', color='red')
    ax2.set_xlabel('Time')
    ax2.set_ylabel('Speed')
    ax2.set_title(f"Test {row['test_id']} - Speed vs Time")
    ax2.axvline(x=max_peak_timeP, color='black', linestyle='--', label='Max Peak Time (Pressure)')
    
    # if not np.isnan(rise_timeS):
    #     ax2.axvline(x=rise_timeS, color='orange', linestyle='--', label='Rise Time (Speed)')
    # if not np.isnan(settling_timeS):
    #     ax2.axvline(x=settling_timeS, color='purple', linestyle='--', label='Settling Time (Speed)')
    ax2.legend()

    plt.tight_layout()

    return fig

def create_one_plot(df_plot):

    # Simulated data for pressure and speed from df_plot (replace these with your actual data)
    pressureR = df_plot['pressure']
    pressureT = df_plot['pressureT']
    time = df_plot['time']
    # pressure_fitted_values = df_plot['pressure_fittes_values']
    pressure_max_peak_time = df_plot['pressure_max_peak_time']
    pressure_max_peak_value = df_plot['pressure_max_peak_value']
    peaksP = df_plot['peaksP']
    # time_b = df_plot['time_before']

    speedR = df_plot['speed']
    speedT = df_plot['speedT']
    speed_fitted_values = df_plot['speed_fitted_values']
    # time_fitted = np.linspace(time[0], time[-1], len(pressure_fitted_values))

    # Create HoverTool for interactivity
    hover = HoverTool(tooltips=[("Time", "@x"), ("Value", "@y")])

    # Pressure plots
    pressure_raw_curve = hv.Curve((time, pressureR), label='Pressure Raw').opts(color='blue', tools=[hover], responsive=True)
    pressure_target_curve = hv.Curve((time, pressureT), label='Pressure Target').opts(color='red', tools=[hover], responsive=True)
    # pressure_fitted_curve = hv.Curve((time_b, pressure_fitted_values), label='Pressure Fitted').opts(color='pink', line_dash='dashed', tools=[hover], responsive=True)

    # Vertical lines for Pressure
    max_peak_line = hv.VLine(pressure_max_peak_time).opts(color='purple', line_dash='dashed', labelled=['x'])
    # tt_flag = df_plot['pressure_tt_flag']
    # tt_color = 'orange' if tt_flag else 'black'
    # # transient_time_line = hv.VLine(df_plot['pressure_tt']).opts(color=tt_color, line_dash='dashed', labelled=['x'])
    # rise_time_line = hv.VLine(df_plot['pressure_rise_time']).opts(color='black', line_dash='dotdash', labelled=['x'])

    # Add additional tools to restore the toolbar
    tools = ['pan', 'box_zoom', 'wheel_zoom', 'save', 'reset']

    # Combine pressure plots
    # pressure_combined = (pressure_raw_curve * pressure_target_curve * pressure_fitted_curve *
    #                      max_peak_line * transient_time_line * rise_time_line).opts(
    #     title="Pressure",
    #     xlabel='Time',
    #     ylabel='Pressure',
    #     legend_position='top_right',
    #     shared_axes=False,
    #     show_grid=True,
    #     axiswise=True,
    #     tools=tools
    # )

    pressure_combined = (pressure_raw_curve * pressure_target_curve * max_peak_line ).opts(
        title="Pressure",
        xlabel='Time',
        ylabel='Pressure',
        legend_position='top_right',
        shared_axes=False,
        show_grid=True,
        axiswise=True,
        tools=tools
    )


    # Speed plots
    speed_raw_curve = hv.Curve((time, speedR), label='Speed Raw').opts(color='blue', tools=[hover],responsive=True)
    speed_target_curve = hv.Curve((time, speedT), label='Speed Target').opts(color='green', tools=[hover], responsive=True)

    # # Vertical lines for Speed
    # speed_combined = (speed_raw_curve * speed_target_curve * max_peak_line *
    #                   transient_time_line * rise_time_line).opts(
    #     title="Speed",
    #     xlabel='Time',
    #     ylabel='Speed',
    #     legend_position='top_right',
    #     shared_axes=False,
    #     show_grid=True,
    #     axiswise=True,
    #     tools=tools
    # )

    speed_combined = (speed_raw_curve * speed_target_curve * max_peak_line).opts(
        title="Speed",
        xlabel='Time',
        ylabel='Speed',
        legend_position='top_right',
        shared_axes=False,
        show_grid=True,
        axiswise=True,
        tools=tools
    )
    # Return the plots in a Layout
    layout = hv.Layout([pressure_combined, speed_combined]).opts(shared_axes=False, merge_tools=True)

    return layout

def create_one_plot_mul(df_plot):

    # Extracting the first row of the filtered DataFrame (assuming df_plot is filtered to one test case)
    pressure_max_peak_time = df_plot['pressure_max_peak_time'].iloc[0]  # Get the scalar value
    pressure_max_peak_value = df_plot['pressure_max_peak_value'].iloc[0]  # Get the scalar value
    pressureR = df_plot['pressure'].iloc[0]
    pressureT = df_plot['pressureT'].iloc[0]
    time = df_plot['time'].iloc[0]
    # pressure_fitted_values = df_plot['pressure_fittes_values'].iloc[0]
    # time_b = df_plot['time_before'].iloc[0]
    rising_time = df_plot['RT'].iloc[0]  # Get the scalar value

    speedR = df_plot['speed'].iloc[0]
    speedT = df_plot['speedT'].iloc[0]
    
    # Create HoverTool for interactivity
    hover = HoverTool(tooltips=[("Time", "@x"), ("Value", "@y")])

    # Pressure plots
    pressure_raw_curve = hv.Curve((time, pressureR), label='Pressure Raw').opts(color='blue', tools=[hover], responsive=True)
    pressure_target_curve = hv.Curve((time, pressureT), label='Pressure Target').opts(color='red', tools=[hover], responsive=True)
    # pressure_fitted_curve = hv.Curve((time_b, pressure_fitted_values), label='Pressure Fitted').opts(color='pink', line_dash='dashed', tools=[hover], responsive=True)

    # Vertical lines for Pressure (use scalar value instead of Series)
    max_peak_line = hv.VLine(pressure_max_peak_time).opts(color='purple', line_dash='dashed', labelled=['x'])
    rising_time = hv.VLine(rising_time).opts(color='green', line_dash='dashed', labelled=['x'])

    tools = ['pan', 'box_zoom', 'wheel_zoom', 'save', 'reset']

    # Combine pressure plots
    # pressure_combined = (pressure_raw_curve * pressure_target_curve * pressure_fitted_curve * max_peak_line).opts(
    pressure_combined = (pressure_raw_curve * pressure_target_curve * max_peak_line*rising_time).opts(
        title="Pressure",
        xlabel='Time',
        ylabel='Pressure',
        legend_position='top_right',
        shared_axes=False,
        show_grid=True,
        axiswise=True,
        tools=tools,
        height=300,  # Set height
        width=700,  
    )

    # Speed plots
    speed_raw_curve = hv.Curve((time, speedR), label='Speed Raw').opts(color='blue', tools=[hover], responsive=True)
    speed_target_curve = hv.Curve((time, speedT), label='Speed Target').opts(color='red', tools=[hover], responsive=True)

    # Combine speed plots
    speed_combined = (speed_raw_curve * speed_target_curve * max_peak_line).opts(
        title="Speed",
        xlabel='Time',
        ylabel='Speed',
        legend_position='top_right',
        shared_axes=False,
        show_grid=True,
        axiswise=True,
        tools=tools,
        height=300,  # Set height
        width=700,   # Set width
    )

    # Return the plots in a Layout
    layout = hv.Layout([pressure_combined, speed_combined]).cols(1).opts(shared_axes=False, merge_tools=True)
    # layout.opts(width=600, height=900) 
    return layout

def create_one_plotBA(df_plot, df_plot_BA):

    # Simulated data for pressure and speed from df_plot (replace these with your actual data)
    pressureR = df_plot['pressure']
    pressureT = df_plot['pressureT']
    time = df_plot['time']
    # pressure_fitted_values = df_plot['pressure_fittes_values']
    pressure_max_peak_time = df_plot['pressure_max_peak_time']
    pressure_max_peak_value = df_plot['pressure_max_peak_value']
    peaksP = df_plot['peaksP']
    # time_b = df_plot['time_before']

    speedR = df_plot['speed']
    speedT = df_plot['speedT']

    ba_pressureR = df_plot_BA['pressure']
    ba_pressureT = df_plot_BA['pressureT']
    ba_time = df_plot_BA['time']
    # ba_pressure_fitted_values = df_plot_BA['pressure_fittes_values']
    ba_pressure_max_peak_time = df_plot_BA['pressure_max_peak_time']
    ba_pressure_max_peak_value = df_plot_BA['pressure_max_peak_value']
    ba_peaksP = df_plot_BA['peaksP']
    ba_time_b = df_plot_BA['time_before']

    ba_speedR = df_plot_BA['speed']
    ba_speedT = df_plot_BA['speedT']

    speed_fitted_values = df_plot['speed_fitted_values']
    # time_fitted = np.linspace(time[0], time[-1], len(pressure_fitted_values))

    # Create HoverTool for interactivity
    hover = HoverTool(tooltips=[("Time", "@x"), ("Value", "@y")])

    # Pressure plots
    pressure_raw_curve = hv.Curve((time, pressureR), label='Pressure Raw').opts(color='blue', tools=[hover], responsive=True)
    ba_pressure_raw_curve = hv.Curve((ba_time, ba_pressureR), label='ba_Pressure Raw').opts(color='green', tools=[hover], responsive=True)
    pressure_target_curve = hv.Curve((time, pressureT), label='Pressure Target').opts(color='red', tools=[hover], responsive=True)
    # pressure_fitted_curve = hv.Curve((time_b, pressure_fitted_values), label='Pressure Fitted').opts(color='pink', line_dash='dashed', tools=[hover], responsive=True)
    
    max_peak_legend = hv.Curve([(0, 0)], label='Max Peak').opts(color='yellow', line_dash='dotdash')

    # Vertical lines for Pressure
    max_peak_line = hv.VLine(pressure_max_peak_time).opts(color='yellow', line_dash='dotdash', labelled=['x'])
    max_peak_combined = max_peak_line * max_peak_legend

    # tt_flag = df_plot['pressure_tt_flag']
    # tt_color = 'orange' if tt_flag else 'black'
    # transient_time_line = hv.VLine(df_plot['pressure_tt']).opts(color=tt_color, line_dash='dashed', labelled=['x'])
    # transient_time_max_peak_legend = hv.Curve([(0, 0)], label='Max Peak').opts(color='yellow', line_dash='dotdash')
   
    rise_time_line = hv.VLine(df_plot['pressure_rise_time']).opts(color='black', line_dash='dotdash', labelled=['x'])

    # # Vertical lines for Pressure_ba
    # max_peak_line_ba = hv.VLine(ba_pressure_max_peak_time).opts(color='green', line_dash='dashed', labelled=['x'])
    # tt_flag_ba = df_plot_BA['pressure_tt_flag']
    # tt_color_ba = 'orange' if tt_flag_ba else 'green'
    # # transient_time_line_ba = hv.VLine(df_plot_BA['pressure_tt']).opts(color=tt_color_ba, line_dash='dashed', labelled=['x'])
    # rise_time_line_ba = hv.VLine(df_plot_BA['pressure_rise_time']).opts(color='green', line_dash='dotdash', labelled=['x'])


    # Add additional tools to restore the toolbar
    tools = ['pan', 'box_zoom', 'wheel_zoom', 'save', 'reset']

    # # Combine pressure plots
    # pressure_combined = (pressure_raw_curve * ba_pressure_raw_curve* pressure_target_curve * pressure_fitted_curve *
    #                      max_peak_line * transient_time_line * rise_time_line*max_peak_line_ba * transient_time_line_ba * rise_time_line_ba * max_peak_combined).opts(
    #     title="Pressure",
    #     xlabel='Time',
    #     ylabel='Pressure',
    #     legend_position='top_right',
    #     shared_axes=False,
    #     show_grid=True,
    #     axiswise=True,
    #     tools=tools
    # )

    # Combine pressure plots
    # pressure_combined = (pressure_raw_curve * ba_pressure_raw_curve* pressure_target_curve * pressure_fitted_curve *
    pressure_combined = (pressure_raw_curve * ba_pressure_raw_curve* pressure_target_curve *
                         max_peak_line *  max_peak_combined).opts(
        title="Pressure",
        xlabel='Time',
        ylabel='Pressure',
        legend_position='top_right',
        shared_axes=False,
        show_grid=True,
        axiswise=True,
        tools=tools
    )

    # Speed plots
    speed_raw_curve = hv.Curve((time, speedR), label='Speed Raw').opts(color='blue', tools=[hover],responsive=True)
    ba_speed_raw_curve = hv.Curve((ba_time, ba_speedR), label='Speed Raw BA').opts(color='green', tools=[hover],responsive=True)

    speed_target_curve = hv.Curve((time, speedT), label='Speed Target').opts(color='red', tools=[hover], responsive=True)

    # # Vertical lines for Speed
    # speed_combined = (speed_raw_curve * ba_speed_raw_curve* speed_target_curve * max_peak_line *
    #                   transient_time_line * rise_time_line).opts(
    #     title="Speed",
    #     xlabel='Time',
    #     ylabel='Speed',
    #     legend_position='top_right',
    #     shared_axes=False,
    #     show_grid=True,
    #     axiswise=True,
    #     tools=tools
    # )

    # Vertical lines for Speed
    speed_combined = (speed_raw_curve * ba_speed_raw_curve* speed_target_curve * max_peak_line ).opts(
        title="Speed",
        xlabel='Time',
        ylabel='Speed',
        legend_position='top_right',
        shared_axes=False,
        show_grid=True,
        axiswise=True,
        tools=tools
    )

    # Return the plots in a Layout
    layout = hv.Layout([pressure_combined, speed_combined]).opts(shared_axes=False, merge_tools=True)

    return layout

def create_pressure_plot(df_plot):
    pressureR = df_plot['pressure'].iloc[0]
    pressureT = df_plot['pressureT'].iloc[0]
    time = df_plot['time'].iloc[0]

    hover = HoverTool(tooltips=[("Time", "@x"), ("Value", "@y")])

    pressure_raw_curve = hv.Curve((time, pressureR), label='Pressure Raw').opts(color='blue', tools=[hover])
    pressure_target_curve = hv.Curve((time, pressureT), label='Pressure Target').opts(color='red', tools=[hover])

    return (pressure_raw_curve * pressure_target_curve).opts(title="Pressure", xlabel='Time', ylabel='Pressure')

# Function to create the speed plot
def create_speed_plot(df_plot):
    speedR = df_plot['speed'].iloc[0]
    speedT = df_plot['speedT'].iloc[0]
    time = df_plot['time'].iloc[0]

    hover = HoverTool(tooltips=[("Time", "@x"), ("Value", "@y")])

    speed_raw_curve = hv.Curve((time, speedR), label='Speed Raw').opts(color='blue', tools=[hover])
    speed_target_curve = hv.Curve((time, speedT), label='Speed Target').opts(color='red', tools=[hover])

    return (speed_raw_curve * speed_target_curve).opts(title="Speed", xlabel='Time', ylabel='Speed')

# Updated plot layout combining pressure and speed plots in a column layout
def create_plots(df_plot):
    pressure_plot = create_pressure_plot(df_plot)
    speed_plot = create_speed_plot(df_plot)

    # Combine plots in a column layout
    combined_plot = pn.Column(
        pressure_plot, 
        speed_plot
    )
    return combined_plot

def create_multiple_plots(df_plot, rising_time_toggle ):
    color_mapping = {}
    
    # Define color palette for up to 10 other signals (excluding red for the target)
    colors = ['blue', 'green', 'orange', 'purple', 'cyan', 'magenta', 'yellow', 'lime', 'teal', 'pink']
    target_color = 'red'
    
    # Data for the Target pressure and speed values
    first_row = df_plot.iloc[0]
    time = first_row['time']
    pressureT = first_row['pressureT']
    speedT = first_row['speedT']
    
    # Need to hold overlays for pressure and speed 'real/simulated' values
    pressure_overlays = []
    speed_overlays = []
    
    # ploting target values
    pressure_target_curve = hv.Curve((time, pressureT), label='Pressure Target').opts(color=target_color)
    speed_target_curve = hv.Curve((time, speedT), label='Speed Target').opts(color=target_color)
    
    # Add target signals to the overlays first (these will always be red)
    pressure_overlays.append(pressure_target_curve)
    speed_overlays.append(speed_target_curve)
    hover = HoverTool(tooltips=[("Time", "@x"), ("Value", "@y")])

    # Limit to 10 other signals and loop through the rest of the selected data
    for i, (_, row) in enumerate(df_plot.iterrows()):

        # Assign color for this test, ensuring the same test gets the same color
        if row["test_id"] not in color_mapping:  
            color_mapping[row["test_id"]] = colors[i % len(colors)]  # Ensure we don't exceed color palette
        
        color = color_mapping[row["test_id"]]
        
        time = row['time']
        pressureR = row['pressure']
        speedR = row['speed']
        rising_time = row['RT']
        
        # Plotting individual signals for pressure and speed with the assigned color
        pressure_curve = hv.Curve((time, pressureR), label=f'Pressure {row["test_id"]}').opts(color=color, tools=[hover],responsive=True)
        speed_curve = hv.Curve((time, speedR), label=f'Speed {row["test_id"]}').opts(color=color, tools=[hover],responsive=True)
               
        # Adding rising time lines based on the toggle state
        if rising_time_toggle.value:
            rising_time_line_pressure = hv.VLine(rising_time).opts(color=color, line_dash='dashed', labelled=['x'], alpha=0.5)
            rising_time_line_speed = hv.VLine(rising_time).opts(color=color, line_dash='dashed', labelled=['x'], alpha=0.5)
            pressure_overlays.append(pressure_curve * rising_time_line_pressure)
            speed_overlays.append(speed_curve * rising_time_line_speed)
        else:
            # without rising time lines
            pressure_overlays.append(pressure_curve)
            speed_overlays.append(speed_curve)

        # Stop after 10 rows + target
        if i >= 10:
            break

    # This step is super need: Combine all pressure signals into one plot and all speed signals into another
    combined_pressure = hv.Overlay(pressure_overlays).opts(
        title="Pressure", xlabel="Time", ylabel="Pressure",
        shared_axes=False, show_grid=True, axiswise=True,
        tools=['pan', 'box_zoom', 'wheel_zoom', 'save', 'reset'],
        height=350, width=700)
    
    combined_speed = hv.Overlay(speed_overlays).opts(
        title="Speed", xlabel="Time", ylabel="Speed",
        shared_axes=False, show_grid=True, axiswise=True,
        tools=['pan', 'box_zoom', 'wheel_zoom', 'save', 'reset'],
        height=350, width=700)
    
    return hv.Layout([combined_pressure, combined_speed]).cols(1).opts(shared_axes=False, merge_tools=True)

