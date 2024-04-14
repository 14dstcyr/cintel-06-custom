# --------------------------------------------
# Imports at the top - PyShiny EXPRESS VERSION
# --------------------------------------------

# From shiny, import just reactive and render
from shiny import reactive, render

# From shiny.express, import just ui and inputs if needed
from shiny.express import ui


# Imports from Python Standard Library to simulate live data
import random
from datetime import datetime
from collections import deque
import plotly.express as px
from shinywidgets import render_plotly, render_widget
from scipy import stats
import shinyswatch


# Import pandas for working with data
import pandas as pd

# --------------------------------------------
# Import icons as you like
# --------------------------------------------
# add favicons to your requirements.txt 
# and install to active project virtual environment

from faicons import icon_svg  


# --------------------------------------------
# Shiny EXPRESS VERSION
# --------------------------------------------

# --------------------------------------------
# First, set a constant UPDATE INTERVAL for all live data
# Constants are usually defined in uppercase letters
# Use a type hint to make it clear that it's an integer (: int)
# --------------------------------------------

UPDATE_INTERVAL_SECS: int = 5

# --------------------------------------------
# Initialize a REACTIVE VALUE with a common data structure
# The reactive value is used to store state (information)
# Used by all the display components that show this live data.
# This reactive value is a wrapper around a DEQUE of readings
# --------------------------------------------

DEQUE_SIZE: int = 5
reactive_value_wrapper = reactive.value(deque(maxlen=DEQUE_SIZE))


# --------------------------------------------
# Initialize a REACTIVE CALC that all display components can call
# to get the latest data and display it.
# The calculation is invalidated every UPDATE_INTERVAL_SECS
# to trigger updates.
# It returns a tuple with everything needed to display the data.
# Very easy to expand or modify.
# --------------------------------------------

@reactive.calc()
def reactive_calc_combined():
    # Invalidate this calculation every UPDATE_INTERVAL_SECS to trigger updates
    reactive.invalidate_later(UPDATE_INTERVAL_SECS)

    # Data generation logic
    beak_depth = round(random.uniform(5, 15), 1)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_dictionary_entry = {"beak":beak, "timestamp":timestamp}

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

ui.page_opts(title="Darwin's Finches", fillable=True)

# Sidebar is typically used for user interaction/information
# Note the with statement to create the sidebar followed by a colon
# Everything in the sidebar is indented consistently

with ui.sidebar(open="open"):

  ui.h2("Finch Data", class_="text-center", style="color: purple")
  ui.p(
        "A look at Darwin's Finches.",
        class_="text-center",
    )
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
        showcase=icon_svg("feather"),
        theme="bg-gradient-purple-white",
    ):

        "Finch"

        @render.text
        def display_temp():
            """Get the latest reading and return a beak depth"""
            deque_snapshot, df, latest_dictionary_entry = reactive_calc_combined()
            return f"{latest_dictionary_entry['beak']} "

        "Finch Beaks"

with ui.layout_columns():
    with ui.value_box(
        showcase=icon_svg("feather"),
        theme="bg-gradient-purple-white"
    ):
        with ui.card(full_screen=True):
            ui.card_header("Beak")

        @render.text
        def display_time():
            """Get the latest reading and return """
            deque_snapshot, df, latest_dictionary_entry = reactive_calc_combined()
            return f"{latest_dictionary_entry['timestamp']}"


    with ui.card(full_screen=True, min_height="50%"):
        ui.card_header("Finch Beak Depth", style="color: purple")    
        
        @render.data_frame
        def display_df():
            """Get the data for beak depth and return a dataframe"""
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
                df["1975"] = pd.to_datetime(df["2012"])
                
                # Create scatter plot for readings
                # pass in the df, the name of the x column, the name of the y column,
                # and more
                
                fig = px.scatter(df,
                x="time",
                y="beak depth",
                title="Beak depth with a Regression Line",
                labels={"Beak": "Beak_Depth", "timestamp": "Year"},
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
                y_vals = df["beak"]

                slope, intercept, r_value, p_value, std_err = stats.linregress(x_vals, y_vals)
                df['best_fit_line'] = [slope * x + intercept for x in x_vals]
                
                # Add the regression line
                fig.add_scatter(x=df["timestamp"], y=df['best_fit_line'], mode='lines', name='Regression Line')

                # Update layout as needed to customize further
                fig.update_layout(xaxis_title="Beak Depth", yaxis_title="Year")

                return fig 
                
from ipyleaflet import Map  

ui.h2("Galapagos Islands")

@render_widget  
def map():
    return Map(center=(-0.777259, -91.142578), zoom=7) 