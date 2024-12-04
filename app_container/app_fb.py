from firebase_admin import credentials, firestore # type: ignore
from plot_handler_hv import * # type: ignore
from get_metrics_fb import getting_metrics
import holoviews as hv # type: ignore
import firebase_admin # type: ignore
from bokeh.models import HoverTool
from constants import *
from ranking_system import *
from dotenv import load_dotenv
import pandas as pd
import json
import os
# This is for loading the bokeh extension for holoviews
hv.extension('bokeh')


load_dotenv()

with open(os.getenv("FIREBASE_CREDENTIALS_PATH")) as f:
    firebase_credentials = json.load(f)
# Initialize Firebase app
cred = credentials.Certificate(firebase_credentials)

firebase_admin.initialize_app(cred)

db = firestore.client()

def get_test_id_db(test_id:str):
    id = test_id.split('_')[0]
    id = id.split('t')[-1]
    return id

def get_test_case_id(tc:str):
    return tc.split('_')[0]

def dbInit():

    db = firestore.client()
    doc_ref = db.collection('tc100_def').stream()
    mainDic = dict()

    doc_tc_def = ['tc100_def','tc104_def','tc106_def']

    for tc in doc_tc_def:
        doc_ref = db.collection(tc).stream()
        tc_id = get_test_case_id(tc)
        print('*** Conecting with DB, Processing: ', tc)
        for doc in doc_ref:  
            id = get_test_id_db(doc.id)
            finalID = tc + '_' + id
            auxDic = {finalID:{
                        'tc': tc_id,
                        'id': id,
                        'time': doc.get('time'),
                        'pressureT': doc.get('pressureT'),
                        'speedT': doc.get('speedT'),
                        'pressureR': doc.get('pressureR'),
                        'speedR': doc.get('speedR'),
                        'Kr': doc.get('Kr'),
                        'Tn': doc.get('Tn'),
                        'Tv': doc.get('Tv'),
                        'ba': doc.get('ba')
                    },}            
            mainDic.update(auxDic)
    df = pd.DataFrame.from_dict(mainDic, orient= 'index')
    df = df.reset_index().rename(columns={"index": "test_id"})

    return df

def main(dfx):
    
    ''' *** HERE START ***'''    
    print('*** Processing multiple files ***')
    global df

    df = dfx # type: ignore
    # df = df[(df['PR'] >= 0.99) & (df['PR'] <= 1.06)]

    interactive_table = pn.widgets.Tabulator(
        df,
        show_index=False,
        pagination='local',
        page_size=15,
        sizing_mode='stretch_width',  # Make sure the table stretches in width
        selectable="toggle",  # Enable multi-row selection
        frozen_columns=['tc', 'test #', 'Kr','Tn','Tv','def_GR','GR', 'def_IR', 'IR'],
        hidden_columns= notShow,
        # filters=[{"field": "tc", "type": "like", "value": ""}],
        disabled=True,  # Make the table read-only
        # header_filters = {'tc':{'type':'input'}}
    )

    weights = {
        'PR': 0.5,
        'RT': 0.6,
        'P-Eng': 1,
        'S-Eng': 1,
        'Eng_p-s':1
    }

    # Create sliders for each weight
    pr_weight_slider = pn.widgets.FloatSlider(name='PR Weight', start=0, end=1, step=0.1, value=weights['PR'])
    rt_weight_slider = pn.widgets.FloatSlider(name='RT Weight', start=0, end=1, step=0.1, value=weights['RT'])

    '''penalisation'''
    p_eng_weight_slider = pn.widgets.FloatSlider(name='P-Eng Weight', start=0, end=1, step=0.1, value=weights['P-Eng'])
    s_eng_weight_slider = pn.widgets.FloatSlider(name='S-Eng Weight', start=0, end=1, step=0.1, value=weights['S-Eng'])
    eng_p_s_weight_slider = pn.widgets.FloatSlider(name='Eng_p-s Weight', start=0, end=1, step=0.1, value=weights['Eng_p-s'])

    overshoot_allowance = pn.widgets.FloatInput(name="Overshoot Allowance", value=1.05, start=1.0, end=2.0, step=0.01)

    eng_p_s_target = pn.widgets.FloatInput(name="Eng_p-s Target", value=1)
    eng_p_target = pn.widgets.FloatInput(name="P-Eng Target", value=1)
    eng_s_target = pn.widgets.FloatInput(name="S-Eng Target", value=1)

    # Checkbox to enable or disable the use of Eng_p-s target
    use_eng_p_s = pn.widgets.Checkbox(name='Use Eng_p-s Target', value=True)
    penalty_sys = pn.widgets.Checkbox(name='Use penalty system', value=True)


    # Function to update weights dynamically
    def update_weights(event):

        current_df = filtered_df if 'filtered_df' in globals() and not filtered_df.empty else df

        if penalty_sys.value == True:
            weights['PR'] = pr_weight_slider.value # type: ignore
            weights['RT'] = rt_weight_slider.value # type: ignore
            weights['P-Eng'] = p_eng_weight_slider.value # type: ignore
            weights['S-Eng'] = s_eng_weight_slider.value # type: ignore
            weights['Eng_p-s'] = eng_p_s_weight_slider.value # type: ignore

            # Recalculate ranking based on updated weights
            global dfx
            dfx = rank_tests_p(current_df, weights,
                               overshoot_allowance=overshoot_allowance.value, # type: ignore
                               eng_p_target=eng_p_target.value, # type: ignore
                               eng_s_target=eng_s_target.value, # type: ignore
                               use_eng_p_s = use_eng_p_s.value, # type: ignore
                            #   enb_eng_p = enb_eng_p.value, # type: ignore
                            #   enb_eng_s = enb_eng_s.value, # type: ignore
                            ) # type: ignore
            interactive_table.value = dfx

        else:
            global dfxnp
            weights['PR'] = pr_weight_slider.value # type: ignore
            weights['RT'] = rt_weight_slider.value # type: ignore
            weights['P-Eng'] = p_eng_weight_slider.value # type: ignore
            weights['S-Eng'] = s_eng_weight_slider.value # type: ignore
            weights['Eng_p-s'] = eng_p_s_weight_slider.value # type: ignore

            # Recalculate ranking based on updated weights
            dfxnp = rank_tests(current_df, weights,
                                    overshoot_allowance=overshoot_allowance.value, # type: ignore
                                    ) # type: ignore
            interactive_table.value = dfxnp

    # Watch for changes in sliders and update weights accordingly
    pr_weight_slider.param.watch(update_weights, 'value')
    p_eng_weight_slider.param.watch(update_weights, 'value')
    s_eng_weight_slider.param.watch(update_weights, 'value')
    eng_p_s_weight_slider.param.watch(update_weights, 'value')
    rt_weight_slider.param.watch(update_weights, 'value')
    overshoot_allowance.param.watch(update_weights, 'value')
    eng_p_s_target.param.watch(update_weights, 'value')
    eng_p_target.param.watch(update_weights, 'value')
    eng_s_target.param.watch(update_weights, 'value')
    use_eng_p_s.param.watch(update_weights, 'value')
    penalty_sys.param.watch(update_weights, 'value')

    # Create a panel layout for the weight sliders
    weight_controls = pn.Column(
        pn.pane.Markdown("## Adjust Weights"),
        # penalty_sys,
        # pn.Row(
        #     use_eng_p_s,
        # ),
        pn.Row(
            pr_weight_slider,
            rt_weight_slider,
        ),
        pn.Row(
            overshoot_allowance,
            p_eng_weight_slider,
            s_eng_weight_slider,
            eng_p_s_weight_slider
        ),
    )

    clear_button = pn.widgets.Button(name='Clear Selection', button_type='danger')
    save_last_rank = pn.widgets.Button(name='Set new default rank', button_type='danger')

    def clear_selection(event):
        interactive_table.selection = []

    def save_new_rank_as_default(event):
        df['def_GR'] = df['GR']
        df['def_IR'] = df['IR']

    rising_time_toggle = pn.widgets.Checkbox(name="Show Rising Time", value=True)
    settlingTime_toggle = pn.widgets.Checkbox(name="Show Settling Time", value=True)
    transientTime_toggle = pn.widgets.Checkbox(name="Show Transient Time", value=True)

    search_input = pn.widgets.TextInput(name="Search by tc", placeholder="Enter test # (e.g., tc100, tc104, or tc106)")

    plot_pane = pn.pane.HoloViews(sizing_mode='fixed', height=600, width=800)  # Fixed plot size

    # NEED it to Keep track of filtered versions of the data
    # This is the function to filter both the table and plot data based on search input
    def search_and_filter_table(event):
        global filtered_df  
        search_value = search_input.value.strip()
        if search_value:
            search_terms = [term.strip() for term in search_value.replace(',', ' ').split()]
            filtered_df = df[df['tc'].isin(search_terms)]
        else:
            filtered_df = df
        
        interactive_table.value = filtered_df

    # This is the function to update the plot based on selected rows and filtered ones
    def update_plot_on_row_selection(event):
        selected_index = interactive_table.selection
        if selected_index is None or len(selected_index) == 0:# type: ignore
            return pn.pane.Markdown("### No row selected")

        # This is for getting the selected test from the corresponding df row in filtered data
        selected_tests = interactive_table.value.iloc[selected_index]['test_id'].tolist()  # type: ignore # Get real test #

        # Filter the plot dataframe to the selected tests
        selected_data = df[df['test_id'].isin(selected_tests)]

        if selected_data.empty:
            return pn.pane.Markdown("### No data available for the selected test")  # type: ignore

        # Create the plot with the filtered data
        plot = create_multiple_plots(selected_data, rising_time_toggle)
        plot_pane.object = plot  # Update the plot in the pane

    # Attach the callback to Tabulator's 'selection' event and the toggle
    search_input.param.watch(search_and_filter_table, 'value')
    search_input.param.watch(update_plot_on_row_selection, 'value')
    # search_input.param.watch(update_weights, 'value')
    interactive_table.param.watch(update_plot_on_row_selection, 'selection')
    rising_time_toggle.param.watch(update_plot_on_row_selection, 'value')
    # Watch for changes in normalization checkbox and update the data accordingly
    # normalisation_signal.param.watch(update_df, 'value')
    clear_button.param.watch(clear_selection, 'value')
    save_last_rank.param.watch(save_new_rank_as_default, 'value')

    # Description for the abbreviations in the table
    abbreviation_description = pn.pane.Markdown("""
    - **PR**: Pressure Ratio ( Pressure_peak / targetPressure_peak )
    - **P-Eng and S-Eng**: Energy of pressure and speed signals
    - **RT** : Rising Time
    - **def_GR** : Default Group Rank 
    - **def_IR** : Default Individual Rank
    - **GR** : New Group Rank 
    - **IR** : New Individual Rank   
    """)
    interactive_table.param.watch(update_plot_on_row_selection, 'selection') 

    # Create a panel layout with table next to the plot
    dashboard = pn.Column(
        pn.pane.Markdown("<h1>Metrics Dashboard</h1>"),
        search_input, 
        # normalisation_signal,
        clear_button,
        weight_controls,  # Adding weight sliders here
        pn.Row(
            pn.Column(            
                abbreviation_description,
                save_last_rank,
                interactive_table,  # Displaying the interactive table on the left
                ),
            pn.Column(
                pn.Row(
                    rising_time_toggle,
                    # settlingTime_toggle, 
                    # transientTime_toggle,
                    ),
                plot_pane),  # Displaying the plot on the right
            sizing_mode='stretch_both'  # Ensure the layout resizes appropriately
        ),
    )

    # Set the fixed size for the plot
    plot_pane.sizing_mode = 'fixed'  # Fixed size, plot will not resize with the table
    plot_pane.height = 300  # Adjust the height of the plot
    plot_pane.width = 800  # Adjust the width of the plot

    # Set the table to stretch only in width
    interactive_table.sizing_mode = 'stretch_width'

    # Serve the UI using Panel (e.g., panel serve)
    def _serve_ui():  # type: ignore
        pn.extension("tabulator") # type: ignore

        return dashboard

    ''' *** HERE ENDS ***'''
    pn.serve({'/app': lambda: _serve_ui()}, port=8080, address="0.0.0.0", show=False,  websocket_origin="*")
    
if __name__ == '__main__':

    df_data = dbInit()
    # with open('prueba.json', 'r') as file:
    #     data = json.load(file)

    # df_data = pd.DataFrame.from_dict(data, orient= 'index')
    # df_data = df_data.reset_index().rename(columns={"index": "test_id"})

    for index, row in df_data.iterrows():
        tc_id = get_test_case_id(row['test_id'])
        id = row['test_id'].split('_')[-1]
        df_data.at[index, 'tc'] = tc_id
        df_data.at[index, 'id'] = id

    df_data = getting_metrics(df_data)
    df_data = normalising_data(df_data)
    weights = {
        'PR': 0.5,
        'RT': 0.6,
        'P-Eng': 1,
        'S-Eng': 1,
        'Eng_p-s':1
    }

    df_data = rank_tests_def(df_data, weights )

    main(df_data)

