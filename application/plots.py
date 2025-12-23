import numpy as np
import matplotlib
import matplotlib.dates as mdates
import matplotlib.ticker as ticker
import platform
import mplcyberpunk
import matplotlib.pyplot as plt

if platform.system() == 'Darwin': # Use TkAgg backend on macOS
    matplotlib.use('TkAgg')

plt.style.use("cyberpunk")

def create_surface_plot():
    fig, ax = plt.subplots()
    fig.patch.set_facecolor('#FFFFFF')
    fig.tight_layout(pad=2.5)

    ax.patch.set_facecolor('#FFFFFF')
    ax.set_aspect('equal')
    ax.set_xlim(-2.5, 2.5)
    ax.set_ylim(-2.5, 2.5)
    ax.set_xlabel("X Axis", color="black")
    ax.set_ylabel("Y Axis", color="black")
    ax.tick_params(axis='x', colors='black')
    ax.tick_params(axis='y', colors='black')
    ax.axhline(0, color='gray', linewidth=0.8)
    ax.axvline(0, color='gray', linewidth=0.8)
    ax.grid(True, color='lightgray', linestyle='--')
    
    return fig, ax

def update_surface_plot(ax, new_data):
    None

def seconds_to_hhmmss(x, pos):
    hours = int(x // 3600)
    minutes = int((x % 3600) // 60)
    seconds = int(x % 60)
    return f'{hours:02d}:{minutes:02d}:{seconds:02d}'

def create_pid_plot():
    fig, ax = plt.subplots()
    fig.patch.set_facecolor('#FFFFFF')
    fig.tight_layout()
    fig.subplots_adjust(bottom=0.15)
    
    ax.patch.set_facecolor('#FFFFFF')
    ax.set_xlim(left=0)
    ax.set_ylim(bottom=0) 
    ax.set_xlabel("")
    ax.set_ylabel("Load (lbf)", color="black")

    ax.xaxis.set_major_formatter(ticker.FuncFormatter(seconds_to_hhmmss))

    ax.tick_params(axis='x', colors='black')
    ax.tick_params(axis='y', colors='black')
    ax.axhline(0, color='gray', linewidth=0.8)
    ax.axvline(0, color='gray', linewidth=0.8)
    ax.grid(True, color='lightgray', linestyle='--')
    ax.text(0.5, 0.015, "Time (hh:mm:ss)", ha="center", va="bottom", transform=ax.transAxes, color="black")
    ax.pid_tuning_mode = ax.text(0.95, 0.95, "", ha='right', va='top',transform=ax.transAxes, color='black')

    (load,) = ax.plot([], [], linestyle='-', color='#242424')
    (target,) = ax.plot([], [], linestyle='-', color='red')

    ax.load = load
    ax.target = target

    return fig, ax

def update_pid_plot(ax, new_data, target, pid_tuning_mode):
    time, load = new_data

    ax.load.set_data(time, load)

    xmin, xmax = time[0], max(time)

    ax.target.set_data([xmin, xmax], [target, target])
    
    ax.relim(visible_only=True)
    ax.autoscale_view(scalex=True, scaley=True)

    ax.set_xlim(xmin, xmax)
    ax.set_ylim(0, max(load))

    ax.pid_tuning_mode.set_text(pid_tuning_mode)