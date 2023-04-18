# Imports
#____________________________________________________________
from fredapi import Fred
import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import messagebox
from processing import resample_fred_data, train_model
from multiprocessing import cpu_count

if __name__ == '__main__':
    #Data Unifier program, on the left of the screen
    # Constants
    #____________________________________________________________
    output_path = "/Users/yourusername/Desktop/Market Analysis/resampled_data.csv"

    available_indicators = [
        "A191RL1Q225SBEA",  # Real Gross Domestic Product
        "CPIAUCSL",  # Consumer Price Index for All Urban Consumers
        "CPILFESL",  # Consumer Price Index for All Urban Consumers: All Items Less Food & Energy
        "DEXCAUS",  # Canada / U.S. Foreign Exchange Rate
        "DTB3",  # 3-Month Treasury Bill: Secondary Market Rate
        "DTB6",  # 6-Month Treasury Bill: Secondary Market Rate
        "DGS10",  # 10-Year Treasury Constant Maturity Rate
        "DGS2",  # 2-Year Treasury Constant Maturity Rate
        "FEDFUNDS",  # Effective Federal Funds Rate
        "ICSA",  # Initial Claims
        "M1SL",  # M1 Money Stock
        "M2SL",  # M2 Money Stock
        "PAYEMS",  # Total Nonfarm Payrolls
        "PCEPI",  # Personal Consumption Expenditures: Chain-type Price Index
        "RECPROUSM156N",  # Recession Indicators Series
        "T10Y2Y",  # 10-Year Treasury Constant Maturity Minus 2-Year Treasury Constant Maturity
        "T5YIFR",  # 5-Year Forward Inflation Expectation Rate
        "UNRATE",  # Unemployment Rate
        "WM2NS",  # Monetary Base; Total
        "W875RX1",  # Real Personal Income
        "USSTHPI",  # All-Transactions House Price Index for the United States
        "HOUST",  # Housing Starts: Total: New Privately Owned Housing Units Started
        "RSXFS",  # Real Retail Sales
        "BAMLH0A0HYM2",  # ICE BofA US High Yield Index Option-Adjusted Spread
        "GS10",  # 10-Year Government Bond Yield
        "BAA",  # Moody's Seasoned Baa Corporate Bond Yield
        "GS1",  # 1-Year Treasury Constant Maturity Rate
        "GS5",  # 5-Year Treasury Constant Maturity Rate
    ]




    default_indicators = ["UNRATE", "CPIAUCSL", "GDP", "FEDFUNDS", "PAYEMS"]

    start_date = '2000-01-01'
    end_date = '2021-01-01'
    time_interval = 'M'


    # Initialize frames
    #____________________________________________________________
    main_frame = tk.Tk()
    main_frame.title("FRED Data Resampler & Data Processor")

    main_frame.columnconfigure(0, weight=1)  # Add this line
    main_frame.rowconfigure(0, weight=1)     # Add this line

    left_frame = tk.Frame(main_frame)
    left_frame.grid(row=0, column=0, sticky="nsew")
    left_frame.columnconfigure(0, weight=1)  # Add this line
    left_frame.rowconfigure(0, weight=0)     # Add this line
    left_frame.rowconfigure(1, weight=1)     # Add this line

    right_frame = tk.Frame(main_frame)       # Add this line
    right_frame.grid(row=0, column=1, sticky="nsew")  # Add this line
    right_frame.columnconfigure(0, weight=1)  # Add this line
    right_frame.rowconfigure(0, weight=3)     # Add this line
    right_frame.rowconfigure(1, weight=1)     # Add this line

    top_frame = tk.Frame(left_frame)
    top_frame.grid(row=0, column=0, columnspan=3, sticky="new")
    top_frame.columnconfigure(0, weight=0)
    top_frame.columnconfigure(1, weight=1)

    bottom_frame = tk.Frame(left_frame)
    bottom_frame.grid(row=1, column=0, sticky="nsew")  # Add pady=(5, 5)
    bottom_frame.columnconfigure(0, weight=1)
    bottom_frame.rowconfigure(1, weight=1)
    bottom_frame.rowconfigure(3, weight=1)




    train_model_frame = tk.Frame(right_frame)  # Update this line
    train_model_frame.grid(row=0, column=0, padx=(10, 10), pady=(10, 10), sticky="nsew")  # Update this line
    for i in range(15):
        train_model_frame.rowconfigure(i, minsize=30, weight=1)

    graphing_frame = tk.Frame(right_frame)  # Update this line
    graphing_frame.grid(row=1, column=0, padx=(10, 10), pady=(10, 10), sticky="nsew")  # Update this line
    for i in range(3):
        graphing_frame.rowconfigure(i, minsize=30, weight=1)

    # Configure input fields
    #____________________________________________________________
    # Add input fields for API key, start date, end date, time interval, and output path
    api_key_var = tk.StringVar(value='6fcfd7e4aa7dc78d6e9635ed058d3fc4')
    start_date_var = tk.StringVar(value=start_date)
    end_date_var = tk.StringVar(value=end_date)
    time_interval_var = tk.StringVar(value=time_interval)

    api_key_label = tk.Label(top_frame, text="API Key:")
    api_key_entry = tk.Entry(top_frame, textvariable=api_key_var)
    start_date_label = tk.Label(top_frame, text="Start Date:")
    start_date_entry = tk.Entry(top_frame, textvariable=start_date_var)
    end_date_label = tk.Label(top_frame, text="End Date:")
    end_date_entry = tk.Entry(top_frame, textvariable=end_date_var)
    time_interval_label = tk.Label(top_frame, text="Time Interval:")
    time_interval_combobox = ttk.Combobox(top_frame, textvariable=time_interval_var, values=['W', 'M', 'Q'])
    output_path_var = tk.StringVar(value=output_path)

    output_path_label = tk.Label(top_frame, text="Output Path:")
    output_path_entry = tk.Entry(top_frame, textvariable=output_path_var)


    output_path_label.grid(row=4, column=0, padx=(10, 5), pady=(5, 5), sticky="w")
    output_path_entry.grid(row=4, column=1, padx=(0, 10), pady=(5, 5), sticky="ew")

    api_key_label.grid(row=0, column=0, padx=(10, 5), pady=(10, 5), sticky="w")
    api_key_entry.grid(row=0, column=1, padx=(0, 10), pady=(10, 5), sticky="ew")
    start_date_label.grid(row=1, column=0, padx=(10, 5), pady=(5, 5), sticky="w")
    start_date_entry.grid(row=1, column=1, padx=(0, 10), pady=(5, 5), sticky="ew")
    end_date_label.grid(row=2, column=0, padx=(10, 5), pady=(5, 5), sticky="w")
    end_date_entry.grid(row=2, column=1, padx=(0, 10), pady=(5, 5), sticky="ew")
    time_interval_label.grid(row=3, column=0, padx=(10, 5), pady=(5, 5), sticky="w")
    time_interval_combobox.grid(row=3, column=1, padx=(0, 10), pady=(5, 5), sticky="ew")


    # Configure indicator treeviews
    #____________________________________________________________
    # Add treeviews for available and selected indicators
    available_label = tk.Label(bottom_frame, text="Available Indicators:")
    available_label.grid(row=0, column=0, padx=(10, 10), pady=(5, 0), sticky="w")

    selected_treeview = ttk.Treeview(bottom_frame, selectmode=tk.EXTENDED)

    selected_label = tk.Label(bottom_frame, text=f"Selected Indicators: {len(selected_treeview.get_children())}")
    selected_label.grid(row=2, column=0, padx=(10, 10), pady=(5, 0), sticky="w")

    selected_treeview["columns"] = ("code", "desc")
    selected_treeview["show"] = "headings"
    selected_treeview.column("code", width=100, anchor="w")
    selected_treeview.column("desc", width=400, anchor="w")
    selected_treeview.heading("code", text="Code")
    selected_treeview.heading("desc", text="Description")

    selected_treeview.grid(row=3, column=0, padx=(10, 10), pady=(5, 5), sticky="nsew")

    indicator_treeview = ttk.Treeview(bottom_frame, selectmode=tk.EXTENDED)
    indicator_treeview["columns"] = ("code", "desc")
    indicator_treeview["show"] = "headings"
    indicator_treeview.column("code", width=100, anchor="w")
    indicator_treeview.column("desc", width=400, anchor="w")
    indicator_treeview.heading("code", text="Code")
    indicator_treeview.heading("desc", text="Description")

    fred = Fred(api_key=api_key_var.get())

    sorted_indicators = []

    for code in available_indicators:
        try:
            series_info = fred.get_series_info(code)
            title = series_info.title
            sorted_indicators.append((code, title))
        except Exception as e:
            print(f"Failed to get series info for code {code}: {e}")

    sorted_indicators = sorted(sorted_indicators, key=lambda x: x[1])

    for code, title in sorted_indicators:
        indicator_treeview.insert("", tk.END, values=(code, title))




    indicator_treeview.grid(row=1, column=0, padx=(10, 10), pady=(5, 5), sticky="nsew")


    # Functions
    #____________________________________________________________
    # Define functions for adding manual indicator and handling double-click events

    def on_add_manual_indicator():
        new_code = manual_code_var.get()
        if not new_code:
            messagebox.showerror("Error", "Please enter an indicator code.")
            return

        # Check if the input is alphanumeric and not longer than 25 characters
        if not new_code.isalnum() or len(new_code) > 25:
            messagebox.showerror("Error", "Invalid series_id. Series IDs should be 25 or less alphanumeric characters.")
            return

        try:
            # Check if the indicator already exists in the indicator_treeview
            for child in indicator_treeview.get_children():
                if indicator_treeview.item(child)['values'][0] == new_code:
                    new_item = indicator_treeview.item(child, "values")
                    selected_treeview.insert("", tk.END, values=new_item)
                    indicator_treeview.delete(child)
                    return
                
            for child in selected_treeview.get_children():
                if selected_treeview.item(child)['values'][0] == new_code:
                    messagebox.showwarning("Warning", "The indicator already exists.")
                    return

            series_info = fred.get_series_info(new_code)
            new_item = (new_code, series_info.title)
            selected_treeview.insert("", tk.END, values=new_item)

            selected_label.config(text=f"Selected Indicators: {len(selected_treeview.get_children())}")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to add the indicator: {e}")



    def on_double_click(event, source_treeview, target_treeview):
        item_id = source_treeview.identify_row(event.y)
        if item_id:
            item_values = source_treeview.item(item_id, "values")
            target_treeview.insert("", "end", values=item_values)
            source_treeview.delete(item_id)

            # Sort items in target_treeview alphabetically based on the second column
            items = [(target_treeview.set(child, 1), child) for child in target_treeview.get_children()]
            items.sort()
            for index, (value, child) in enumerate(items):
                target_treeview.move(child, "", index)

        selected_label.config(text=f"Selected Indicators: {len(selected_treeview.get_children())}")





    def on_submit():
        api_key = api_key_var.get()
        start_date = start_date_var.get()
        end_date = end_date_var.get()
        time_interval = time_interval_var.get()
        output_path = output_path_var.get()

        selected_indicators = [indicator_treeview.item(i)["values"][0] for i in indicator_treeview.selection()] + \
                            [selected_treeview.item(i)["values"][0] for i in selected_treeview.get_children()]

        if not api_key or not start_date or not end_date or not time_interval or not selected_indicators:
            messagebox.showerror("Error", "Please fill in all fields and select at least one indicator.")
            return

        try:
            resample_fred_data(api_key, selected_indicators, start_date, end_date, time_interval, output_path)
            messagebox.showinfo("Success", f"Data saved at {output_path_var.get()} ")
        except Exception as e:
            messagebox.showerror("Error", str(e))




    # Bind double-click events
    #____________________________________________________________
    indicator_treeview.bind("<Double-1>", lambda event: on_double_click(event, indicator_treeview, selected_treeview))
    selected_treeview.bind("<Double-1>", lambda event: on_double_click(event, selected_treeview, indicator_treeview))


    # Configure manual code input and button
    #____________________________________________________________
    manual_code_label = tk.Label(top_frame, text="Manual Code:")
    manual_code_var = tk.StringVar()
    manual_code_entry = tk.Entry(top_frame, textvariable=manual_code_var)
    manual_code_button = tk.Button(top_frame, text="Add", command=on_add_manual_indicator)

    manual_code_label.grid(row=8, column=0, padx=(10, 5), pady=(10, 5), sticky="w")
    manual_code_entry.grid(row=8, column=1, padx=(0, 5), pady=(10, 5), sticky="ew")
    manual_code_button.grid(row=8, column=2, padx=(5, 10), pady=(10, 5), sticky="ew")


    # Configure submit button
    #____________________________________________________________
    submit_button = tk.Button(bottom_frame, text="Submit", command=on_submit)
    submit_button.grid(row=4, column=0, columnspan=2, padx=(10, 10), pady=(10, 10), sticky="sew")





    #Data Processor program, on the right of the screen
    # Constants
    #____________________________________________________________


    # Initialize frames
    #____________________________________________________________

    # Add input fields for the train_model function parameters
    market_data_path_var = tk.StringVar(value='/Users/yourusername/Desktop/Market Analysis/NASDAQCOM.csv')
    n_processes_var = tk.IntVar(value=int(cpu_count() / 2))
    population_size_var = tk.IntVar(value=1000)
    generations_var = tk.IntVar(value=20)
    p_crossover_var = tk.DoubleVar(value=0.7)
    p_subtree_mutation_var = tk.DoubleVar(value=0.1)
    p_hoist_mutation_var = tk.DoubleVar(value=0.05)
    p_point_mutation_var = tk.DoubleVar(value=0.1)
    max_samples_var = tk.DoubleVar(value=0.9)
    tournament_size_var = tk.IntVar(value=20)
    parsimony_coefficient_var = tk.DoubleVar(value=0.001)
    t_offset_var = tk.IntVar(value=1)
    t_frame_var = tk.StringVar(value='M')
    start_training_var = tk.StringVar(value='2010-01-01')
    end_training_var = tk.StringVar(value='2020-01-01')

    # Define layout for the train_model function parameters
    train_model_label = tk.Label(train_model_frame, text="Train Model Parameters", font=("Helvetica", 16, "bold"))
    train_model_label.grid(row=0, column=0, pady=(10, 10), sticky="ew")

    market_data_path_label = tk.Label(train_model_frame, text="Market Data Path:")
    market_data_path_entry = tk.Entry(train_model_frame, textvariable=market_data_path_var)
    n_processes_label = tk.Label(train_model_frame, text="Number of Processes:")
    n_processes_entry = tk.Entry(train_model_frame, textvariable=n_processes_var)
    population_size_label = tk.Label(train_model_frame, text="Population Size:")
    population_size_entry = tk.Entry(train_model_frame, textvariable=population_size_var)
    generations_label = tk.Label(train_model_frame, text="Generations:")
    generations_entry = tk.Entry(train_model_frame, textvariable=generations_var)
    p_crossover_label = tk.Label(train_model_frame, text="P Crossover:")
    p_crossover_entry = tk.Entry(train_model_frame, textvariable=p_crossover_var)
    p_subtree_mutation_label = tk.Label(train_model_frame, text="P Subtree Mutation:")
    p_subtree_mutation_entry = tk.Entry(train_model_frame, textvariable=p_subtree_mutation_var)
    p_hoist_mutation_label = tk.Label(train_model_frame, text="P Hoist Mutation:")
    p_hoist_mutation_entry = tk.Entry(train_model_frame, textvariable=p_hoist_mutation_var)
    p_point_mutation_label = tk.Label(train_model_frame, text="P Point Mutation:")
    p_point_mutation_entry = tk.Entry(train_model_frame, textvariable=p_point_mutation_var)
    max_samples_label = tk.Label(train_model_frame, text="Max Samples:")
    max_samples_entry = tk.Entry(train_model_frame, textvariable=max_samples_var)
    tournament_size_label = tk.Label(train_model_frame, text="Tournament Size:")
    tournament_size_entry = tk.Entry(train_model_frame, textvariable=tournament_size_var)
    parsimony_coefficient_label = tk.Label(train_model_frame, text="Parsimony Coefficient:")
    parsimony_coefficient_entry = tk.Entry(train_model_frame, textvariable=parsimony_coefficient_var)
    t_offset_label = tk.Label(train_model_frame, text="T Offset:")
    t_offset_entry = tk.Entry(train_model_frame, textvariable=t_offset_var)
    t_frame_label = tk.Label(train_model_frame, text="T Frame:")
    t_frame_combobox = ttk.Combobox(train_model_frame, textvariable=time_interval_var, values=['W', 'M', 'Q'])
    start_training_label = tk.Label(train_model_frame, text="Start Training:")
    start_training_entry = tk.Entry(train_model_frame, textvariable=start_training_var)
    end_training_label = tk.Label(train_model_frame, text="End Training:")
    end_training_entry = tk.Entry(train_model_frame, textvariable=end_training_var)



    # Place train_model parameter input fields in the grid layout
    market_data_path_label.grid(row=1, column=0, sticky="w", pady=(5, 5))
    market_data_path_entry.grid(row=1, column=1, sticky="w", pady=(5, 5))
    n_processes_label.grid(row=2, column=0, sticky="w", pady=(5, 5))
    n_processes_entry.grid(row=2, column=1, sticky="w", pady=(5, 5))
    population_size_label.grid(row=3, column=0, sticky="w", pady=(5, 5))
    population_size_entry.grid(row=3, column=1, sticky="w", pady=(5, 5))
    generations_label.grid(row=4, column=0, sticky="w", pady=(5, 5))
    generations_entry.grid(row=4, column=1, sticky="w", pady=(5, 5))
    p_crossover_label.grid(row=5, column=0, sticky="w", pady=(5, 5))
    p_crossover_entry.grid(row=5, column=1, sticky="w", pady=(5, 5))
    p_subtree_mutation_label.grid(row=6, column=0, sticky="w", pady=(5, 5))
    p_subtree_mutation_entry.grid(row=6, column=1, sticky="w", pady=(5, 5))
    p_hoist_mutation_label.grid(row=7, column=0, sticky="w", pady=(5, 5))
    p_hoist_mutation_entry.grid(row=7, column=1, sticky="w", pady=(5, 5))
    p_point_mutation_label.grid(row=8, column=0, sticky="w", pady=(5, 5))
    p_point_mutation_entry.grid(row=8, column=1, sticky="w", pady=(5, 5))
    max_samples_label.grid(row=9, column=0, sticky="w", pady=(5, 5))
    max_samples_entry.grid(row=9, column=1, sticky="w", pady=(5, 5))
    tournament_size_label.grid(row=10, column=0, sticky="w", pady=(5, 5))
    tournament_size_entry.grid(row=10, column=1, sticky="w", pady=(5, 5))
    parsimony_coefficient_label.grid(row=11, column=0, sticky="w", pady=(5, 5))
    parsimony_coefficient_entry.grid(row=11, column=1, sticky="w", pady=(5, 5))
    t_offset_label.grid(row=12, column=0, sticky="w", pady=(5, 5))
    t_offset_entry.grid(row=12, column=1, sticky="w", pady=(5, 5))
    t_frame_label.grid(row=13, column=0, sticky="w", pady=(5, 5))
    t_frame_combobox.grid(row=13, column=1, sticky="w", pady=(5, 5))
    start_training_label.grid(row=14, column=0, sticky="w", pady=(5, 5))
    start_training_entry.grid(row=14, column=1, sticky="w", pady=(5, 5))
    end_training_label.grid(row=15, column=0, sticky="w", pady=(5, 5))
    end_training_entry.grid(row=15, column=1, sticky="w", pady=(5, 5))



    # Graphing Parameters
    #____________________________________________________________
    output_label = tk.Label(graphing_frame, text="Output Parameters", font=("Helvetica", 16, "bold"))
    output_label.grid(row=0, column=0, pady=(10, 10), sticky="ew")

    start_graphing_var = tk.StringVar(value='2000-01-01')
    end_graphing_var = tk.StringVar(value='2021-01-01')
    result_output_path_var = tk.StringVar(value='/Users/yourusername/Desktop/Market Analysis/output.txt')

    start_graphing_label = tk.Label(graphing_frame, text="Start Graphing:")
    start_graphing_entry = tk.Entry(graphing_frame, textvariable=start_graphing_var)
    end_graphing_label = tk.Label(graphing_frame, text="End Graphing:")
    end_graphing_entry = tk.Entry(graphing_frame, textvariable=end_graphing_var)
    result_output_path_label = tk.Label(graphing_frame, text="Output Path:")
    result_output_path_entry = tk.Entry(graphing_frame, textvariable=result_output_path_var)

    start_graphing_label.grid(row=1, column=0, sticky="w", pady=(5, 5))
    start_graphing_entry.grid(row=1, column=1, sticky="w", pady=(5, 5))
    end_graphing_label.grid(row=2, column=0, sticky="w", pady=(5, 5))
    end_graphing_entry.grid(row=2, column=1, sticky="w", pady=(5, 5))
    result_output_path_label.grid(row=3, column=0, sticky="w", pady=(5, 5))
    result_output_path_entry.grid(row=3, column=1, sticky="w", pady=(5, 5))







    # Create a function to execute the train_model with the given parameters
    def execute_train_model():
        train_model(
            population_size=population_size_var.get(),
            generations=generations_var.get(),
            p_crossover=p_crossover_var.get(),
            p_subtree_mutation=p_subtree_mutation_var.get(),
            p_hoist_mutation=p_hoist_mutation_var.get(),
            p_point_mutation=p_point_mutation_var.get(),
            max_samples=max_samples_var.get(),
            tournament_size=tournament_size_var.get(),
            parsimony_coefficient=parsimony_coefficient_var.get(),
            t_offset=t_offset_var.get(),
            t_frame=t_frame_var.get(),
            start_training=start_training_var.get(),
            end_training=end_training_var.get(),
            start_graphing=start_graphing_var.get(),
            end_graphing=end_graphing_var.get(),
            market_data_path=market_data_path_var.get(),
            resampled_data_path=output_path_var.get(),
            output_path=result_output_path_var.get(),
            n_processes=n_processes_var.get()
        )

    # Add a button to execute the train_model function with the input parameters
    execute_button = tk.Button(graphing_frame, text="Execute", command=execute_train_model)

    execute_button.grid(row=4, column=0, columnspan=2, sticky="we")




    main_frame.mainloop()
