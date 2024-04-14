from shiny import reactive, render, req
from shiny.express import input, ui
import random
import palmerpenguins  # This package provides the Palmer Penguins dataset
from datetime import datetime
from collections import deque
import plotly.express as px
from shinywidgets import render_plotly, render_widget
from scipy import stats
import shinyswatch
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

# Use the built-in function to load the Palmer Penguins dataset.
penguins_df = palmerpenguins.load_penguins()


from faicons import icon_svg  

UPDATE_INTERVAL_SECS: int = 8

DEQUE_SIZE: int = 5
reactive_value_wrapper = reactive.value(deque(maxlen=DEQUE_SIZE))

@reactive.calc()
def reactive_calc_combined():
    # Invalidate this calculation every UPDATE_INTERVAL_SECS to trigger updates
    reactive.invalidate_later(UPDATE_INTERVAL_SECS)

    # Data generation logic
    temp = round(random.uniform(-18, -16), 1)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_dictionary_entry = {"temp":temp, "timestamp":timestamp}

    # get the deque and append the new entry
    reactive_value_wrapper.get().append(new_dictionary_entry)

    # Get a snapshot of the current deque for any further processing
    deque_snapshot = reactive_value_wrapper.get()

    # For Display: Convert deque to DataFrame for display
    df = pd.DataFrame(deque_snapshot)

    # For Display: Get the latest dictionary entry
    latest_dictionary_entry = new_dictionary_entry

    # Return a tuple with everything we need
    # Every time we call this function, we'll get all these values
    return deque_snapshot, df, latest_dictionary_entry

# Define the Shiny UI Page layout
# Call the ui.page_opts() function
# Set title to a string in quotes that will appear at the top
# Set fillable to True to use the whole page width for the UI

ui.page_opts(title="Penguins in Antarctica", fillable=True)

# Sidebar is typically used for user interaction/information
# Note the with statement to create the sidebar followed by a colon
# Everything in the sidebar is indented consistently

with ui.sidebar(open="open"):
    ui.h2("Sidebar", style="color: blue")
  
    # Use ui.input_selectize() to create a dropdown input to choose a column
    ui.input_selectize(
        "Selected_Attribute",
        "Bill Length in Millimeters",
        ["bill_length_mm", "bill_depth_mm", "flipper_length_mm", "body_mass_g"],
    )

    # Use ui.input_numeric() to create a numeric input for the number of Plotly histogram bins
    ui.input_numeric("plotly_bin_count", "Number of Plotly Bins", 20)

    # Use ui.input_slider() to create a slider input for the number of Seaborn bins
    ui.input_slider("seaborn_bin_count", "Bin Count", 1, 100, 20)


    # Use ui.input_checkbox_group() to create a checkbox group input to filter the species
    ui.input_checkbox_group(
        "selected_species_list",
        "Penguin Species",
        ["Adelie", "Gentoo", "Chinstrap"],
        selected=["Chinstrap"],
        inline=True,
    )
                            
    # Add a horizontal line to sidebar
    ui.hr()

    ui.h6("Links:")
    ui.a(
        "GitHub Source",
        href="https://github.com/14dstcyr/cintel-06-custom",
        target="_blank",
  )
    ui.a(
        "GitHub App",
        href="https://14dstcyr.github.io/cintel-06-custom/",
        target="_blank",
  )
    ui.a("PyShiny", href="https://shinylive.io/py/examples/#plotly", target="_blank")


# In Shiny Express, everything not in the sidebar is in the main panel
with ui.layout_columns():
    with ui.value_box(
        showcase=icon_svg("linux"),
        theme="bg-gradient-blue-pink",
    ):
        "Penguin Data"
        @render.text
        def display_temp():
            """Get the latest reading and return a temperature string"""
            deque_snapshot, df, latest_dictionary_entry = reactive_calc_combined()
            return f"{latest_dictionary_entry['temp']} C"
        "Imagine penguins in Antarctica"

with ui.layout_columns():
    with ui.value_box(
        showcase=icon_svg("earlybirds"),
        theme="bg-gradient-pink-blue"
    ):
        with ui.card(full_screen=True):
            ui.card_header("Current Date and Time")

        @render.text
        def display_time():
            """Get the latest reading and return a timestamp string"""
            deque_snapshot, df, latest_dictionary_entry = reactive_calc_combined()
            return f"{latest_dictionary_entry['timestamp']}"

    with ui.card(full_screen=True, min_height="50%"):
        ui.card_header("Latest Temperature Readings", style="color: purple")    
        
        @render.data_frame
        def display_df():
            """Get the latest temperature reading and return a dataframe with current readings"""
            deque_snapshot, df, latest_dictionary_entry = reactive_calc_combined()
            pd.set_option('display.width', None)  # Use maximum width
            return render.DataGrid(df,width="100%")


    with ui.card():
        ui.card_header("Current Trends")
        
        @render_plotly
        def display_plot():
            # Fetch from the reactive calc function
            deque_snapshot, df, latest_dictionary_entry = reactive_calc_combined()
            
            # Ensure the DataFrame is not empty before plotting
            if not df.empty:
                # Convert the 'timestamp' column to datetime for better plotting
                df["timestamp"] = pd.to_datetime(df["timestamp"])
                
                # Create scatter plot for readings
                # pass in the df, the name of the x column, the name of the y column,
                # and more
                
                fig = px.scatter(df,
                x="timestamp",
                y="temp",
                title="Temperature Reading with a Regression Line",
                labels={"temp": "Temperature (°C)", "timestamp": "Time"},
                color_discrete_sequence=["purple"],)
                
                fig.update_layout(
                    xaxis=dict(gridcolor='yellow'),
                    yaxis=dict(gridcolor='white'))
                fig.update_layout(
                    plot_bgcolor='violet',
                    paper_bgcolor='white'
                )
                # Linear regression - get a list of the independent
                # variable x values (time) and the dependent variable
                # y values (temp)

                # Generate a sequence of integers from 0 to len(df)
                sequence = range(len(df))
                x_vals = list(sequence)
                y_vals = df["temp"]

                slope, intercept, r_value, p_value, std_err = stats.linregress(x_vals, y_vals)
                df['best_fit_line'] = [slope * x + intercept for x in x_vals]
                
                # Add the regression line
                fig.add_scatter(x=df["timestamp"], y=df['best_fit_line'], mode='lines', name='Regression Line')

                # Update layout as needed to customize further
                fig.update_layout(xaxis_title="Time", yaxis_title="Temperature (°C)")

                return fig 

## Plotly Scatterplot
    with ui.card():
        ui.card_header()
        @render_plotly
        def plotly_scatterplot():
            return px.scatter(filtered_data(),
                          x="bill_length_mm",
                          y="body_mass_g",
                          color="species",
                          title="Scatterplot",
                          labels={"bill_length_mm": "Bill Length mm",
                                  "body_mass_g": "Body Mass g"},
                          size_max=20,
            )
            
# Create tables and plots displaying all data
## Data Table and Grid
with ui.layout_columns():                
    with ui.card():
        ui.h2("Penguins Grid")
        
        @render.data_frame
        def render_Penguin_Grid():
            return render.DataGrid(penguins_df)

# --------------------------------------------------------
# Reactive calculations and effects
# --------------------------------------------------------

# Add a reactive calculation to filter the data
# By decorating the function with @reactive, we can use the function to filter the data
# The function will be called whenever an input function used to generate that output changes.
# Any output that depends on the reactive function (e.g., filtered_data()) will be updated when the data changes.

@reactive.calc
def filtered_data():
    return penguins_df[penguins_df["species"].isin(input.selected_species_list())]
                