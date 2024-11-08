import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import gate_class as gc
import numpy as np
from scipy.optimize import minimize
import qutip as qt

#%%
# Initialize the main window
GUItest = tk.Tk()
GUItest.title("xyGate")
GUItest.geometry("2500x1000")

GUItest.rowconfigure(0, weight=1)
GUItest.columnconfigure(1, weight=1)
GUItest.columnconfigure(3, weight=3)

# Font settings for labels and entries
font_settings = ("Arial", 16)
# LabelFrame to group input fields
input_frame = tk.LabelFrame(GUItest, text="Parameters", font=("Arial", 14, "bold"))
input_frame.grid(row=0, column=0, rowspan=10, columnspan=2, padx=10, pady=10, sticky="nsew")


for i in range(10):  
    input_frame.rowconfigure(i, weight=1)
input_frame.columnconfigure(0, weight=1)
input_frame.columnconfigure(1, weight=2)

# width for entries
entry_width = 30

#%%
# Entry and label
lb_W = tk.Label(input_frame, text='Base Energy(W)', font=font_settings, width=entry_width)
lb_W.grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
en_W = tk.Entry(input_frame, font=font_settings)
en_W.grid(row=0, column=1, sticky="nsew", padx=5, pady=3)
en_W.insert(0, str(4.5))

lb_W_d = tk.Label(input_frame, text='Energy Offset(W_d)', font=font_settings, width=entry_width)
lb_W_d.grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
en_W_d = tk.Entry(input_frame, font=font_settings)
en_W_d.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)
en_W_d.insert(0, str(4.5))

lb_A = tk.Label(input_frame, text='Amplitude(A)', font=font_settings, width=entry_width)
lb_A.grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
en_A = tk.Entry(input_frame, font=font_settings)
en_A.grid(row=2, column=1, sticky="nsew", padx=5, pady=5)
en_A.insert(0, str(0.04))

lb_b = tk.Label(input_frame, text='Derivative Intensity(b)', font=font_settings, width=entry_width)
lb_b.grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
en_b = tk.Entry(input_frame, font=font_settings)
en_b.grid(row=3, column=1, sticky="nsew", padx=5, pady=5)
en_b.insert(0, str(0.4))

lb_sigma = tk.Label(input_frame, text='Gaussian Width(sigma)', font=font_settings, width=entry_width)
lb_sigma.grid(row=4, column=0, sticky=tk.W, padx=5, pady=5)
en_sigma = tk.Entry(input_frame, font=font_settings)
en_sigma.grid(row=4, column=1, sticky="nsew", padx=5, pady=5)
en_sigma.insert(0, str(90))

lb_t_0 = tk.Label(input_frame, text='Gaussian Center Time(t_0)', font=font_settings, width=entry_width)
lb_t_0.grid(row=5, column=0, sticky=tk.W, padx=5, pady=5)
en_t_0 = tk.Entry(input_frame, font=font_settings)
en_t_0.grid(row=5, column=1, sticky="nsew", padx=5, pady=5)
en_t_0.insert(0, str(500))

lb_alpha = tk.Label(input_frame, text='Control Strength Coefficient(alpha)', font=font_settings, width=entry_width)
lb_alpha.grid(row=6, column=0, sticky=tk.W, padx=5, pady=5)
en_alpha = tk.Entry(input_frame, font=font_settings)
en_alpha.grid(row=6, column=1, sticky="nsew", padx=5, pady=5)
en_alpha.insert(0, str(-0.2))

GUItest.option_add("*TCombobox*Listbox.font","Arial 16")
lb_gate = tk.Label(input_frame, text='Gate Type(gate)', font=font_settings, width=entry_width)
lb_gate.grid(row=7, column=0, sticky=tk.W, padx=5, pady=5)
values_gate = ("X" , "x" , "Y" , "y")
en_gate = ttk.Combobox(input_frame, values=values_gate, font=font_settings,height=5)
en_gate.grid(row=7, column=1, sticky="nsew", padx=5, pady=5)
en_gate.set("x") 


lb_q = tk.Label(input_frame, text='System Dimension(q)', font=font_settings, width=entry_width)
lb_q.grid(row=8, column=0, sticky=tk.W, padx=5, pady=5)
en_q = tk.Entry(input_frame, font=font_settings)
en_q.grid(row=8, column=1, sticky="nsew", padx=5, pady=5)
en_q.insert(0, str(4))

lb_t_r = tk.Label(input_frame, text='Time Range (start, end, num)', font=font_settings, width=entry_width)
lb_t_r.grid(row=9, column=0, sticky=tk.W, padx=5, pady=5)

frame_t_r = tk.Frame(input_frame)
frame_t_r.grid(row=9, column=1, sticky="nsew", padx=5, pady=5)
frame_t_r.columnconfigure(0, weight=1)
frame_t_r.columnconfigure(1, weight=1)
frame_t_r.columnconfigure(2, weight=1)

en_t_r_start = tk.Entry(frame_t_r, font=font_settings)
en_t_r_start.grid(row=0, column=0, sticky="nsew", padx=2, pady=5)
en_t_r_start.insert(0, str(0))

en_t_r_end = tk.Entry(frame_t_r, font=font_settings)
en_t_r_end.grid(row=0, column=1, sticky="nsew", padx=2, pady=5)
en_t_r_end.insert(0, str(2000))

en_t_r_num = tk.Entry(frame_t_r, font=font_settings)
en_t_r_num.grid(row=0, column=2, sticky="nsew", padx=2, pady=5)
en_t_r_num.insert(0, str(300))


# Matplotlib figure and canvas for plot
fig, ax = plt.subplots()
canvas = FigureCanvasTkAgg(fig, master=GUItest)
canvas.get_tk_widget().grid(row=0, column=3, rowspan=10, sticky="nsew", padx=10, pady=10)

# solution Label
solution_frame = tk.LabelFrame(GUItest, text="result", font=("Arial", 14, "bold"))
solution_frame.grid(row=2, column=3, rowspan=10, columnspan=2, padx=10, pady=10, sticky="nsew")
minimize_stste = tk.Label(solution_frame, text="minisize_state", font=("Arial", 14))
minimize_stste.grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)

# Make the canvas resizable
GUItest.rowconfigure(0, weight=10)
GUItest.columnconfigure(3, weight=10)
#%% 
# get function
def get():
    # gate_coeff = {'X':[1,1], 'x':[0.5,0.5], 'Y':[-1,1], 'y':[-0.5,0.5]}
    args = {
        'W': float(en_W.get()),
        'W_d': float(en_W_d.get()),
        'A': float(en_A.get()),
        'b': float(en_b.get()),
        'sigma': float(en_sigma.get()),
        't_0': float(en_t_0.get()),
        'alpha': float(en_alpha.get()),
        'gate': en_gate.get(),
        'q': int(en_q.get())
    }
    return args

def linspace():
    start = int(en_t_r_start.get())
    end = int(en_t_r_end.get())
    num = int(en_t_r_num.get())
    time_range = np.linspace(start,end,num)
    return time_range

#%%
# function about make gate
def update_plot():
    args = get()
    time_range = linspace()

    gate_evo = gc.GateEvo(time_range, args)
    result = gate_evo.make_result()
        
    P0, P1, P2, P3 = [qt.basis(args['q'], i) * qt.basis(args['q'], i).dag() for i in range(4)]
        
        # Calculate probabilities over time for each state
    m = [np.absolute((i * P0).tr()) ** 2 for i in result.states]
    n = [np.absolute((i * P1).tr()) ** 2 for i in result.states]
    l = [np.absolute((i * P2).tr()) ** 2 for i in result.states]
    p = [np.absolute((i * P3).tr()) ** 2 for i in result.states]
        
        # Plot the probabilities
    ax.clear()
    ax.plot(time_range, m, label='ground state')
    ax.plot(time_range, n, label='1st excited')
    ax.plot(time_range, l, label='2nd excited')
    ax.plot(time_range, p, label='2nd excited')
    ax.set_xlabel("Time")
    ax.set_ylabel("Probability")
    ax.set_title("State Probabilities Over Time")
    ax.legend()
        
        # Refresh the canvas
    canvas.draw()



bt_plot = tk.Button(GUItest, text="Plot",command=update_plot, font=("Arial", 14)) 
bt_plot.grid(row=10, column=1, padx=5, pady=10, sticky="ew")


GUItest.mainloop()

