import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import gate_class
import numpy as np
from scipy.optimize import minimize
import qutip as qt


#%%
# Initialize the main window
GUItest = tk.Tk()
GUItest.title("xyGate")
GUItest.geometry("2500x1000")

GUItest.rowconfigure(0, weight=2)
GUItest.columnconfigure(1, weight=1)
GUItest.columnconfigure(3, weight=3)

# Font settings for labels and entries
font_settings = ("Arial", 24)
# LabelFrame to group input fields
input_frame = tk.LabelFrame(GUItest, text="Parameters", font=("Arial", 24, "bold"))
input_frame.grid(row=0, column=0, rowspan=10, columnspan=2, padx=10, pady=10, sticky="nsew")


for i in range(10):  
    input_frame.rowconfigure(i, weight=1)
input_frame.columnconfigure(0, weight=1)
input_frame.columnconfigure(1, weight=2)

# width for entries
entry_width = 30

#%%
# Entry and label
# lb = Label
# en = Entry


lb_W = tk.Label(input_frame, text='Transmon Frequency(W)', font=font_settings, width=entry_width)
lb_W.grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
en_W = tk.Entry(input_frame, font=font_settings)
en_W.grid(row=0, column=1, sticky="nsew", padx=5, pady=3)
en_W.insert(0, str(4.5))

lb_W_d = tk.Label(input_frame, text='Driving Frequency(W_d)', font=font_settings, width=entry_width)
lb_W_d.grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
en_W_d = tk.Entry(input_frame, font=font_settings)
en_W_d.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)
en_W_d.insert(0, str(4.5))

lb_A = tk.Label(input_frame, text='diving amplitude(A)', font=font_settings, width=entry_width)
lb_A.grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
en_A = tk.Entry(input_frame, font=font_settings)
en_A.grid(row=2, column=1, sticky="nsew", padx=5, pady=5)
en_A.insert(0, str(0.068))

lb_b = tk.Label(input_frame, text='DRAG factor(b)', font=font_settings, width=entry_width)
lb_b.grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
en_b = tk.Entry(input_frame, font=font_settings)
en_b.grid(row=3, column=1, sticky="nsew", padx=5, pady=5)
en_b.insert(0, str(0.4))

lb_sigma = tk.Label(input_frame, text='gate length(sigma)', font=font_settings, width=entry_width)
lb_sigma.grid(row=4, column=0, sticky=tk.W, padx=5, pady=5)
en_sigma = tk.Entry(input_frame, font=font_settings)
en_sigma.grid(row=4, column=1, sticky="nsew", padx=5, pady=5)
en_sigma.insert(0, str(130))

lb_t_0 = tk.Label(input_frame, text='gating time(t_0)', font=font_settings, width=entry_width)
lb_t_0.grid(row=5, column=0, sticky=tk.W, padx=5, pady=5)
en_t_0 = tk.Entry(input_frame, font=font_settings)
en_t_0.grid(row=5, column=1, sticky="nsew", padx=5, pady=5)
en_t_0.insert(0, str(500))

lb_alpha = tk.Label(input_frame, text='anharmonicity(alpha)', font=font_settings, width=entry_width)
lb_alpha.grid(row=6, column=0, sticky=tk.W, padx=5, pady=5)
en_alpha = tk.Entry(input_frame, font=font_settings)
en_alpha.grid(row=6, column=1, sticky="nsew", padx=5, pady=5)
en_alpha.insert(0, str(-0.2))

GUItest.option_add("*TCombobox*Listbox.font","Arial 24")
lb_gate = tk.Label(input_frame, text='Gate Type(gate)', font=font_settings, width=entry_width)
lb_gate.grid(row=7, column=0, sticky=tk.W, padx=5, pady=5)
values_gate = ("X" , "x" , "Y" , "y")
en_gate = ttk.Combobox(input_frame, values=values_gate, font=font_settings,height=5)
en_gate.grid(row=7, column=1, sticky="nsew", padx=5, pady=5)
en_gate.set("x") 


lb_q = tk.Label(input_frame, text='number of levels(q)', font=font_settings, width=entry_width)
lb_q.grid(row=8, column=0, sticky=tk.W, padx=5, pady=5)
en_q = tk.Entry(input_frame, font=font_settings)
en_q.grid(row=8, column=1, sticky="nsew", padx=5, pady=5)
en_q.insert(0, str(4))

check_btn_gausswave_var = tk.IntVar()
check_btn_gausswave = tk.Checkbutton(input_frame,text='gauss wave',variable = check_btn_gausswave_var,font=font_settings, width=entry_width)
check_btn_gausswave.grid(row=9, column=0, sticky=tk.W, padx=5, pady=5)
check_btn_gausswave.pack

# lb_t_r = tk.Label(input_frame, text='Time Range (start, end, num)', font=font_settings, width=entry_width)
# lb_t_r.grid(row=9, column=0, sticky=tk.W, padx=5, pady=5)

# frame_t_r = tk.Frame(input_frame)
# frame_t_r.grid(row=9, column=1, sticky="nsew", padx=5, pady=5)
# frame_t_r.columnconfigure(0, weight=1)
# frame_t_r.columnconfigure(1, weight=1)
# frame_t_r.columnconfigure(2, weight=1)

# en_t_r_start = tk.Entry(frame_t_r, font=font_settings)
# en_t_r_start.grid(row=0, column=0, sticky="nsew", padx=2, pady=5)
# en_t_r_start.insert(0, str(0))

# en_t_r_end = tk.Entry(frame_t_r, font=font_settings)
# en_t_r_end.grid(row=0, column=1, sticky="nsew", padx=2, pady=5)
# en_t_r_end.insert(0, str(2000))

# en_t_r_num = tk.Entry(frame_t_r, font=font_settings)
# en_t_r_num.grid(row=0, column=2, sticky="nsew", padx=2, pady=5)
# en_t_r_num.insert(0, str(300))


# Matplotlib figure and canvas for plot
fig, ax = plt.subplots()
canvas = FigureCanvasTkAgg(fig, master=GUItest)
canvas.get_tk_widget().grid(row=0, column=3, rowspan=5, sticky="nsew", padx=10, pady=10)

# solution Label
solution_frame = tk.LabelFrame(GUItest, text="result", font=("Arial", 24, "bold"))
solution_frame.grid(row=2, column=3, rowspan=10, columnspan=2, padx=10, pady=10, sticky="nsew")

for i in range(4):  
    solution_frame.columnconfigure(i, weight=1)

State_0 = tk.Label(solution_frame, text="P0 :", font=("Arial", 18))
State_0.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

State_1 = tk.Label(solution_frame, text="P1 :", font=("Arial", 18))
State_1.grid(row=0, column=2, sticky="nsew", padx=5, pady=5)

State_2 = tk.Label(solution_frame, text="P2 :", font=("Arial", 18))
State_2.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)

State_3 = tk.Label(solution_frame, text="P3 :", font=("Arial", 18))
State_3.grid(row=1, column=2, sticky="nsew", padx=5, pady=5)




# Make the canvas resizable
GUItest.rowconfigure(0, weight=10)
GUItest.columnconfigure(3, weight=10)
#%% 
# get function
def get():
    # gate_coeff = {'X':[1,1], 'x':[0.5,0.5], 'Y':[-1,1], 'y':[-0.5,0.5]}
    if int(en_q.get())<2:
        error_signal = tk.messagebox.showerror('errer','dimension must be greater or equal to 2')
        return error_signal
    else :
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
    time_range = np.linspace(0,2*float(en_t_0.get()),200)
    return time_range

#%%
# function about make gate
def update_plot():
    args = get()
    time_range = linspace()
    qpsi0 = qt.basis(args['q'],0)

    
    my_GateEvo = gate_class.GateEvo(time_range,qpsi0,args)
    result = my_GateEvo.make_result()
    
    plt.rcParams.update({'font.size': 16})
    global ax,ax2,fig
    if fig is None or ax is None:
        fig, ax = plt.subplots()  
    else:
        fig.clear()  
        ax = fig.add_subplot(111) 
    ax.clear()
    ax.plot(time_range, result.expect[0], color='#1f77b4', label="P0")
    ax.plot(time_range, result.expect[1], color='#ff7f0e', label="P1")
    ax.plot(time_range, result.expect[2], color='#2ca02c', label="P2")
    ax.plot(time_range, result.expect[3], color='#d62728', label="P3")
    ax.set_xlabel("Time")
    ax.set_ylabel("Probability")
    ax.set_title("State Probabilities Over Time")
    ax.legend()
    ax2 = ax.twinx()
    check = check_btn_gausswave_var.get()
    if check == 1:
        # gauss_deriv = my_GateEvo.gauss_deriv(time_range)
        gauss_wave = my_GateEvo.gauss_wave(time_range)
        # ax2.plot(time_range,gauss_deriv, color='#e377c2')
        ax2.plot(time_range,gauss_wave, color='#e377c2')
    fig.tight_layout()
    


    # Refresh the canvas
    canvas.draw()
    state_probs = [result.expect[i][-1] for i in range(4)]  
    State_0.config(text=f"P0: {state_probs[0]*100:.2f}%")
    State_1.config(text=f"P1: {state_probs[1]*100:.2f}%")
    State_2.config(text=f"P2: {state_probs[2]*100:.2f}%")
    State_3.config(text=f"P3: {state_probs[3]*100:.2f}%")

    
# def const(x):
#     return x[0]
# def minimize_func(x):
#     args = get()
#     time_range = linspace()
#     qpsi0 = qt.basis(args['q'],0)
#     constraints = {'type':'ineq', 'fun':const}
#     args['A'] = x[0]
#     args['sigma'] = x[1]
#     obj = gate_class.GateEvo(time_range, qpsi0, args).make_result().expect[1][-1]
#     res = minimize(np.abs(0.5-obj), x0=[0.07,130], constraints=constraints)
#     return(res.x[0],res.x[1])       
        

# bt_minimize = tk.Button(solution_frame, text="最小化", command=minimize_func(), font=("Arial", 14))
# bt_minimize.grid(row=0, column=1, padx=5, pady=10, sticky="ew")

bt_plot = tk.Button(GUItest, text="Plot",command=update_plot, font=("Arial", 24, "bold")) 
bt_plot.grid(row=10, column=1, padx=5, pady=20, sticky="ew")


GUItest.mainloop()