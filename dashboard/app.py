from shiny import App, reactive, render, ui
from shiny.express import ui
from faicons import icon_svg
import pandas as pd
import random
from datetime import datetime
from collections import deque
import plotly.express as px
from scipy import stats
from shinywidgets import render_plotly, output_widget, render_widget
from ipyleaflet import Map

# Load CSV files with correct paths
data1 = pd.read_csv(r'C:\Users\debcy\OneDrive\Documents\NWMSU\Continuous_Intelligence\Cintel\cintel-06-custom\dashboard\finch_beaks_1975.csv')
data2 = pd.read_csv(r'C:\Users\debcy\OneDrive\Documents\NWMSU\Continuous_Intelligence\Cintel\cintel-06-custom\dashboard\finch_beaks_2012.csv')
data3 = pd.read_csv(r'C:\Users\debcy\OneDrive\Documents\NWMSU\Continuous_Intelligence\Cintel\cintel-06-custom\dashboard\fortis_beak_depth_heredity.csv')
data4 = pd.read_csv(r'C:\Users\debcy\OneDrive\Documents\NWMSU\Continuous_Intelligence\Cintel\cintel-06-custom\dashboard\scandens_beak_depth_heredity.csv')

UPDATE_INTERVAL_SECS: int = 5
DEQUE_SIZE: int = 5
reactive_value_wrapper = reactive.value(deque(maxlen=DEQUE_SIZE))

@reactive.calc()
def reactive_calc_combined():
    reactive.invalidate_later(UPDATE_INTERVAL_SECS)
    beak_depth = round(random.uniform(5, 15), 1)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_dictionary_entry = {"beak_depth": beak_depth, "timestamp": timestamp}
    reactive_value_wrapper.get().append(new_dictionary_entry)
    deque_snapshot = reactive_value_wrapper.get()
    df = pd.DataFrame(deque_snapshot)
    latest_dictionary_entry = new_dictionary_entry
    return deque_snapshot, df, latest_dictionary_entry

ui.page_opts(title="Darwin's Finches", fillable=True)

with express_ui.sidebar(open="open"):
    express_ui.h2("Finch Data", class_="text-center", style="color: purple")
    express_ui.p("A look at Darwin's Finches.", class_="text-center")
    express_ui.hr()
    express_ui.h6("Links:")
    express_ui.a("GitHub Source", href="https://github.com/14dstcyr/cintel-06-custom", target="_blank")
    express_ui.a("GitHub App", href="https://14dstcyr.github.io/cintel-06-custom/", target="_blank")
    express_ui.a("PyShiny", href="https://shinylive.io/py/examples/#plotly", target="_blank")

app_ui = express_ui.page_fluid(
    express_ui.input_select(
        id="dataset",
        label="data1:",
        choices=["data1", "data2"]
    ),
    express_ui.output_table("data_table")
)

def server(input, output, session):
    @reactive.calc
    def selected_data():
        if input.dataset() == "data1":
            return data1
        else:
            return data2

    @output
    @render.table
    def render_data_table():
        return selected_data()

with express_ui.layout_columns():
    with express_ui.value_box(showcase=icon_svg("feather"), theme="bg-gradient-purple-white"):
        @render.text
        def display_temp():
            deque_snapshot, df, latest_dictionary_entry = reactive_calc_combined()
            return f"{latest_dictionary_entry['beak_depth']}"

        "Finch Beaks"

with express_ui.layout_columns():
    with express_ui.value_box(showcase=icon_svg("feather"), theme="bg-gradient-purple-white"):
        with express_ui.card(full_screen=True):
            express_ui.card_header("Beak")

        @render.text
        def display_time():
            deque_snapshot, df, latest_dictionary_entry = reactive_calc_combined()
            return f"{latest_dictionary_entry['timestamp']}"

    with express_ui.card(full_screen=True, min_height="50%"):
        express_ui.card_header("Finch Beak Depth", style="color: purple")

        @render.data_frame
        def display_df():
            deque_snapshot, df, latest_dictionary_entry = reactive_calc_combined()
            pd.set_option('display.width', None)
            return render.DataGrid(df, width="100%")

    with express_ui.card():
        express_ui.card_header("Current Trends")

        @render_plotly
        def display_plot():
            deque_snapshot, df, latest_dictionary_entry = reactive_calc_combined()
            if not df.empty:
                fig = px.scatter(df, x="timestamp", y="beak_depth", title="Beak depth with a Regression Line", labels={"beak_depth": "Beak_Depth", "timestamp": "Timestamp"}, color_discrete_sequence=["purple"])
                fig.update_layout(xaxis=dict(gridcolor='yellow'), yaxis=dict(gridcolor='white'))
                fig.update_layout(plot_bgcolor='violet', paper_bgcolor='white')
                sequence = range(len(df))
                x_vals = list(sequence)
                y_vals = df["beak_depth"]
                slope, intercept, r_value, p_value, std_err = stats.linregress(x_vals, y_vals)
                df['best_fit_line'] = [slope * x + intercept for x in x_vals]
                fig.add_scatter(x=df["timestamp"], y=df['best_fit_line'], mode='lines', name="Regression Line")
                fig.update_layout(xaxis_title="Timestamp", yaxis_title="Beak Depth")
                return fig

ui.h2("Galapagos Islands")

@render_widget
def map():
    return Map(center=(-0.777259, -91.142578), zoom=7)
