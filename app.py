import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
import numpy as np


app = dash.Dash()
server = app.server

# CSS from Dash tutorial
app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})

colors = {
    'background': '#000000',
    'text': '#7FDBFF'
}

hampton17sprint = pd.read_csv('Data_output/results_hampton17sprint.csv')
hampton18sprint = pd.read_csv('Data_output/results_hampton18sprint.csv')
rockwood17sprint = pd.read_csv('Data_output/results_rockwood17sprint.csv')
rockwood18sprint = pd.read_csv('Data_output/results_rockwood18sprint.csv')

available_sports = np.array(['finish', 'swim', 'bike', 'run', 't1', 't2'])
available_distributions = np.array(['All', 'Gender', 'Division'])

# Set up dictionary to access df names based on race and year selections
race_options = {
    'Rockwood': {
        '2017': ["rockwood17sprint"],
        '2018': ["rockwood18sprint"]
    },
    'Hampton': {
        '2017': ["hampton17sprint"],
        '2018': ["hampton18sprint"]
    }
}

# eval(race_dataframes['Rockwood']['2018'][0])
# gives the dataframe `rockwood18sprint`

def convert_min_to_time(time):
    """
    Convert a numeric representing decimal minutes to a character string
    in mm:ss or hh:mm:ss format as appropriate.
    """
    hours = int(time/60)
    minutes = time - (hours*60)
    seconds = round((time - int(time))*60)
    #seconds_decimal = (seconds - int(seconds))*100
    if (hours > 0):
        return("%d:%02d:%02d" % (hours, minutes, seconds))
    else:
        return("%02d:%02d" % (minutes, seconds))

def convert_numeric_to_ordinal(value):
    """
    Convert a number into a string that has the appropriate suffix
    for an ordinal number (e.g., 1 -> 1st, 2 -> 2nd, etc.).
    """
    lastchar = int('{0}'.format(value)[-1])
    if (lastchar == 1):
        suffix = 'st'
    elif (lastchar == 2):
        suffix = 'nd'
    elif (lastchar == 3):
        suffix = 'rd'
    else:
        suffix = 'th'
    word = '{0}{1}'.format(value, suffix)
    return(word)

#---------#
# Layout
#---------#

app.layout = html.Div([

    html.Br(),

    # Header

    html.H1(children='Triathlon Stats Comparison Tool',
            style={
                'textAlign': 'center'
    }),

    html.H4(children='...because analysis is the 4th sport.',
            style={'textAlign': 'center'}),

    html.Br(),
    html.Hr(),


    # Top text container
    html.Div([
        html.Div([

            html.H2('What is this?'),

            html.P(['A ',
            html.A('triathlon', href='https://en.wikipedia.org/wiki/Triathlon'),
            ' is a race that includes swimming, biking, and running components, as well as transitions in between sports.  Triathletes tend to be an obsessive bunch who get very involved in analyzing and comparing race times - which, in my personal experience, usually involves a browser with multiple open tabs, a calculator (or Spotlight), and frustration that I don\'t have a histogram of all participants\' times. This tool was developed to address that. (Note that many triathletes also claim to do triathlons to eat and drink more, so the motivations are broad and wide-ranging.)']),

            html.P('You can use this tool to compare triathlon race times between two athletes (or the same athlete between two different races or race years). Use the dropdown menus to select each race, year, and athlete. The athletes\' time will appear on the plots below, along with the times for other athletes in the same race. Data associated with the athlete on the left will be shown in red, and data associated with the athlete on the right will be shown in blue.'),

            html.P('Scroll down for more info (or just start playing around to figure out how it works).'),],

            style = {'width': '85%', 'textAlign': 'center', 'display': 'inline-block'})

    # Wrap up for top text container
    ],
    style={'width': '100%', 'textAlign': 'center', 'display': 'inline-block'}),


    html.Br(),
    html.Hr(),


    # Athlete selection container
    html.Div([

        # Left side
        html.Div([
            html.Div([
                html.H6('Select first race, year, and athlete:', style={'color': 'rgb(22, 96, 167)'}),
                dcc.Dropdown(
                    id='race-dropdown-left',
                    options=[{'label': i, 'value': i} for i in race_options.keys()],
                    value='Rockwood'
                ),

                dcc.Dropdown(id='year-dropdown-left'),

                dcc.Dropdown(id='athlete-dropdown-left')
            ],
            style={'width': '75%', 'display': 'inline-block'}),
        ],
        style={'width': '45%', 'textAlign': 'center', 'display': 'inline-block'}),

        # Right side
        html.Div([
            html.Div([
                html.H6('Select second race, year, and athlete:', style={'color': 'rgb(205, 12, 24)'}),
                dcc.Dropdown(
                    id='race-dropdown-right',
                    options=[{'label': i, 'value': i} for i in race_options.keys()],
                    value='Rockwood'
                ),

                dcc.Dropdown(id='year-dropdown-right'),

                dcc.Dropdown(id='athlete-dropdown-right')
            ],
            style={'width': '75%', 'display': 'inline-block'}),
        ],
        style={'width': '45%', 'textAlign': 'center', 'display': 'inline-block'}),


        html.Br(),
        html.Hr(),

    # Wrap up for athlete selection container
    ],
    style={'width': '90%', 'textAlign': 'center', 'display': 'inline-block'}),


    # Outer plot container (for all plots)
    html.Div([

        # Distribution container
        html.Div([
            # (left)
            html.Div([
                html.Div([
                    html.H6('Select first distribution:', style={'color': 'rgb(22, 96, 167)'}),
                    dcc.RadioItems(
                        id='dist-radio-left',
                        options=[{'label': i, 'value': i} for i in available_distributions],
                        value='All'
                    ),

                    dcc.Dropdown(id='dist-details-dropdown-left')
                ],
                    style={'width': '75%', 'display': 'inline-block'}),
            ],
                style={'width': '50%', 'textAlign': 'center', 'display': 'inline-block'}),

            # Select distribution
            # (right)
            html.Div([
                html.Div([
                    html.H6('Select second distribution:', style={'color': 'rgb(205, 12, 24)'}),
                    dcc.RadioItems(
                        id='dist-radio-right',
                        options=[{'label': i, 'value': i} for i in ['All', 'Gender', 'Division']],
                        value='All'
                    ),

                    dcc.Dropdown(id='dist-details-dropdown-right')
                ],
                    style={'width': '75%', 'display': 'inline-block'}),
            ],
                style={'width': '50%', 'textAlign': 'center', 'display': 'inline-block'})
        ],
            style={'width': '80%', 'textAlign': 'center', 'display': 'inline-block'}),

        html.Br(),
        html.Hr(),

        # Radio buttons to select sport
        html.Div([
            html.Div([
                html.H6('Select sport to compare:'),
                dcc.RadioItems(
                    id='subset-sport',
                    options=[{'label': '{0}{1}'.format(i, '    '), 'value': i} for i in available_sports],
                    value='finish',
                    labelStyle={'display': 'inline-block'}
                )
            ],
                style={'width': '80%', 'textAlign': 'left', 'display': 'inline-block'})
        ],
            style = {'width': '100%', 'textAlign': 'center', 'display': 'inline-block'}),

        html.Br(), html.Br(),

        # Text comparing speeds
        html.Div(id='comparison-text'),

        # Boxplot container
        html.Div([
            dcc.Graph(id='boxplot-1')
        ],
            style={'width': '80%', 'textAlign': 'center', 'display': 'inline-block'}),

        html.Br(),

        # Narrower <hr>
        html.Div([
            html.Hr()
        ],
            style = {'width': '60%', 'textAlign': 'center', 'display': 'inline-block'}),

        # Histogram container
        html.Div([
            dcc.Graph(id='histogram-main')
        ],
            style={'width': '80%', 'textAlign': 'center', 'display': 'inline-block'}),


    # Wrap up for outer plot container
    ],
        style={'width': '90%', 'textAlign': 'center', 'display': 'inline-block'}
    ),

    html.Br(),
    html.Hr(),

    # More info text container
    html.Div([
        html.Div([

            html.H2('More Info'),

            html.P('Select a sport to explore using the radio buttons above the first plot. `finish` is the overall race time.  Individual sport times come directly from the available results data, so some races may have separate transition times (`t1` and `t2`), whereas others may have transition time as part of `swim`, `bike`, or `run` times.'),

            html.P('You can also select a subset of race data to compare each athlete\'s times against. The default selection is `All`, which is the full race data. `Gender` lets you compare the athlete\'s times to just women\'s or men\'s times, and `Division` lets you compare the athlete\'s times to those from a single division (e.g., `F30-39` is females age 30-39). For each subset, the default selection is the group that the selected athlete is in.'),

            html.P('The boxplots and histograms can help give you a sense of where an athlete\'s times fell in the overall distribution of other athletes in the race. Different races or race courses may be generally faster or slower, depending on factors like weather or hills. Also, different races attract participants with different levels of experience and ability. For example, the Hampton Ladies\' Triathlon attracts both experienced triathletes and complete beginners, whereas participants in the Rockwood By the Bay triathlon are on average faster and more experienced.'),

            # Narrower <hr>
            html.Div([
                html.Hr()
            ],
                style = {'width': '60%', 'textAlign': 'center', 'display': 'inline-block'}),


            html.H2('Races'),

            html.P('The following races are currently available in this tool:'),

            html.H4('Rockwood By the Bay'),

            html.P([ 'The ', html.A('Rockwood by the Bay Triathlon', href = 'https://www.facebook.com/RockwoodbytheBayTriathlon/'), ' is the home race for the Fundy Extreme Triathlon Club, based in Saint John, NB, held in and around Saint John\'s beautiful Rockwood Park.',
            html.Br(),
            html.A('2017 Sprint Triathlon results', href = 'https://results.raceroster.com/results/7uqq4njwwzqnbn6q'),
            html.Br(),
            html.A('2018 Sprint Triathlon results', href = 'https://results.raceroster.com/results/syf4m4gy6sknmzc3?sub_event=13620&query_string=&gender_code=&per_page=500&division=&page=1'),
            ]
            ),

            html.H4('Hampton Ladies\' Triathlon'),

            html.P([ 'The ', html.A('Hampton Ladies\' Triathlon', href = 'https://fundysportstourism.com/hampton-ladies-triathlon/'), ' is an extremely welcoming, supportive, and fun triathlon held in Hampton, NB.',
            html.Br(),
            html.A('2017 Sprint Triathlon results', href = 'https://results.raceroster.com/results/sj47pnd6egmunhjt'),
            html.Br(),
            html.A('2018 Sprint Triathlon results', href = 'https://results.raceroster.com/results/wjvz7sruf3ngamgq'),
            ]
            ),

            # Narrower <hr>
            html.Div([
                html.Hr()
            ],
                style = {'width': '60%', 'textAlign': 'center', 'display': 'inline-block'}),


            html.H2('About me'),

            html.P('My name is Lindsay Brin, and I am a data scientist with a background in biogeochemistry. I help businesses use their data to answer questions and find actionable insights.  For more info about my work, check out my website:'),

            html.A('lindsaydbrin.com', href = 'http://www.lindsaydbrin.com'),

            ],
            style = {'width': '85%', 'textAlign': 'center', 'display': 'inline-block'})

    # Wrap up for top text container
    ],
    style={'width': '100%', 'textAlign': 'center', 'display': 'inline-block'}),


    html.Br(),
    html.Hr(),

    html.Div([
        html.P('© Copyright Lindsay D Brin 2018')
    ],
        style = {'width': '90%', 'textAlign': 'left', 'display': 'inline-block'}),

    html.Br(),
    html.Br()

# Wrap up for full page container
],
    style = {'width': '100%', 'textAlign': 'center', 'display': 'inline-block'})

#------------#
# Callbacks
#------------#

# Set race year options based on selected race
#   (left)
@app.callback(
    dash.dependencies.Output('year-dropdown-left', 'options'),
    [dash.dependencies.Input('race-dropdown-left', 'value')])
def set_year_options(selected_race):
    return [{'label': i, 'value': i} for i in sorted(list(race_options[selected_race].keys()), reverse=True)]

#   (right)
@app.callback(
    dash.dependencies.Output('year-dropdown-right', 'options'),
    [dash.dependencies.Input('race-dropdown-right', 'value')])
def set_year_options(selected_race):
    # return [{'label': i, 'value': i} for i in race_options[selected_race]]
    return [{'label': i, 'value': i} for i in sorted(list(race_options[selected_race].keys()), reverse=True)]

# Set race year initial value based on selected race and above options
#   (left)
@app.callback(
    dash.dependencies.Output('year-dropdown-left', 'value'),
    [dash.dependencies.Input('year-dropdown-left', 'options')])
def set_year_value(year_options):
    return year_options[0]['value']

#   (right)
@app.callback(
    dash.dependencies.Output('year-dropdown-right', 'value'),
    [dash.dependencies.Input('year-dropdown-right', 'options')])
def set_year_value(year_options):
    return year_options[0]['value']

# Set athlete options based on selected race and year
#   (left)
@app.callback(
    dash.dependencies.Output('athlete-dropdown-left', 'options'),
    [dash.dependencies.Input('race-dropdown-left', 'value'),
    dash.dependencies.Input('year-dropdown-left', 'value')])
def set_athlete_options(selected_race, selected_year):
    return [{'label': i, 'value': i} for i in sorted(list(eval(race_options[selected_race][selected_year][0])["name"]))]

#   (right)
@app.callback(
    dash.dependencies.Output('athlete-dropdown-right', 'options'),
    [dash.dependencies.Input('race-dropdown-right', 'value'),
    dash.dependencies.Input('year-dropdown-right', 'value')])
def set_athlete_options(selected_race, selected_year):
    return [{'label': i, 'value': i} for i in sorted(list(eval(race_options[selected_race][selected_year][0])["name"]))]

# Set athlete initial value based on selected race and year and above options
#   (left)
@app.callback(
    dash.dependencies.Output('athlete-dropdown-left', 'value'),
    [dash.dependencies.Input('athlete-dropdown-left', 'options')])
def set_year_value(athlete_options):
    return athlete_options[0]['value']

#   (right)
@app.callback(
    dash.dependencies.Output('athlete-dropdown-right', 'value'),
    [dash.dependencies.Input('athlete-dropdown-right', 'options')])
def set_year_value(athlete_options):
    return athlete_options[0]['value']

# Set distribution dropdown options based on selection of All, Gender, or Division
#   (left)
@app.callback(
    dash.dependencies.Output('dist-details-dropdown-left', 'options'),
    [dash.dependencies.Input('dist-radio-left', 'value'),
    dash.dependencies.Input('race-dropdown-left', 'value'),
    dash.dependencies.Input('year-dropdown-left', 'value')])
def set_dist_options_left(selected_dist_type, selected_race, selected_year):
    if selected_dist_type == 'All':
        return [{'label': 'All', 'value': 'All'}]
    elif selected_dist_type == 'Gender':
        return [{'label': i, 'value': i} for i in list(np.unique(eval(race_options[selected_race][selected_year][0])["gender"]))]
    elif selected_dist_type == 'Division':
        return [{'label': i, 'value': i} for i in list(np.unique(eval(race_options[selected_race][selected_year][0])["division"]))]
    else:
        return [{'label': 'CONFUZZLED', 'value': 'CONFUZZLED'}]

#   (right)
@app.callback(
    dash.dependencies.Output('dist-details-dropdown-right', 'options'),
    [dash.dependencies.Input('dist-radio-right', 'value'),
    dash.dependencies.Input('race-dropdown-right', 'value'),
    dash.dependencies.Input('year-dropdown-right', 'value')])
def set_dist_options_right(selected_dist_type, selected_race, selected_year):
    if selected_dist_type == 'All':
        return [{'label': 'All', 'value': 'All'}]
    elif selected_dist_type == 'Gender':
        return [{'label': i, 'value': i} for i in list(np.unique(eval(race_options[selected_race][selected_year][0])["gender"]))]
    elif selected_dist_type == 'Division':
        return [{'label': i, 'value': i} for i in list(np.unique(eval(race_options[selected_race][selected_year][0])["division"]))]
    else:
        return [{'label': 'CONFUZZLED', 'value': 'CONFUZZLED'}]


# Set distribution dropdown initial value based on dropdown options and corresponding to selected athlete and dist type
#   (left)
@app.callback(
    dash.dependencies.Output('dist-details-dropdown-left', 'value'),
    [dash.dependencies.Input('race-dropdown-left', 'value'),
     dash.dependencies.Input('year-dropdown-left', 'value'),
     dash.dependencies.Input('athlete-dropdown-left', 'value'),
     dash.dependencies.Input('dist-radio-left', 'value')])
def set_dist_value(selected_race, selected_year, selected_athlete,
                   selected_dist_type):
    df = eval(race_options[selected_race][selected_year][0])
    athlete_row = df[df['name'] == selected_athlete]
    if selected_dist_type == 'All':
        return 'All'
    else:
        return list(athlete_row[selected_dist_type.lower()])[0]

#   (right)
@app.callback(
    dash.dependencies.Output('dist-details-dropdown-right', 'value'),
    [dash.dependencies.Input('race-dropdown-right', 'value'),
     dash.dependencies.Input('year-dropdown-right', 'value'),
     dash.dependencies.Input('athlete-dropdown-right', 'value'),
     dash.dependencies.Input('dist-radio-right', 'value')])
def set_dist_value(selected_race, selected_year, selected_athlete,
                   selected_dist_type):
    df = eval(race_options[selected_race][selected_year][0])
    athlete_row = df[df['name'] == selected_athlete]
    if selected_dist_type == 'All':
        return 'All'
    else:
        return list(athlete_row[selected_dist_type.lower()])[0]


# Comparison text
@app.callback(
    dash.dependencies.Output(component_id='comparison-text', component_property='children'),
    [dash.dependencies.Input('race-dropdown-left', 'value'),
     dash.dependencies.Input('year-dropdown-left', 'value'),
     dash.dependencies.Input('athlete-dropdown-left', 'value'),
     dash.dependencies.Input('race-dropdown-right', 'value'),
     dash.dependencies.Input('year-dropdown-right', 'value'),
     dash.dependencies.Input('athlete-dropdown-right', 'value'),
     dash.dependencies.Input('subset-sport', 'value')]
)
def update_output_div(selected_race_left, selected_year_left, selected_athlete_left,
                      selected_race_right, selected_year_right, selected_athlete_right,
                      selected_sport):
    # Get dataframes
    df_left = eval(race_options[selected_race_left][selected_year_left][0])
    df_right = eval(race_options[selected_race_right][selected_year_right][0])
    # Get specific athlete times for selected sport
    athlete_time_left = df_left[df_left['name']==selected_athlete_left][selected_sport].values[0]
    athlete_time_right = df_right[df_right['name']==selected_athlete_right][selected_sport].values[0]
    time_difference = abs(athlete_time_left - athlete_time_right)
    if (athlete_time_left < athlete_time_right):
        mylayout = html.Div([
            html.P("{0} ({1} {2}) was faster than {3} ({4} {5}) by: {6}".format(
                selected_athlete_left,
                selected_race_left,
                selected_year_left,
                selected_athlete_right,
                selected_race_right,
                selected_year_right,
                convert_min_to_time(time_difference)))
            ])
    elif (athlete_time_left > athlete_time_right):
        mylayout = html.Div([
            html.P("{3} ({4} {5}) was faster than {0} ({1} {2}) by: {6}".format(
                selected_athlete_left,
                selected_race_left,
                selected_year_left,
                selected_athlete_right,
                selected_race_right,
                selected_year_right,
                convert_min_to_time(time_difference)))
            ])
    elif (athlete_time_left == athlete_time_right):
        mylayout = html.Div([
            html.P("{0} ({1} {2}) was the same speed as {3} ({4} {5})!".format(
                selected_athlete_left,
                selected_race_left,
                selected_year_left,
                selected_athlete_right,
                selected_race_right,
                selected_year_right,
                convert_min_to_time(time_difference)))
            ])
    else:
        mylayout = html.Div([
            html.P("I'm sorry, this is confusing.")
            ])

    return mylayout
    # return html.Div([html.P("There be words here!")])


# Boxplot
@app.callback(
    dash.dependencies.Output('boxplot-1', 'figure'),
    [dash.dependencies.Input('race-dropdown-left', 'value'),
     dash.dependencies.Input('year-dropdown-left', 'value'),
     dash.dependencies.Input('athlete-dropdown-left', 'value'),
     dash.dependencies.Input('dist-radio-left', 'value'),
     dash.dependencies.Input('dist-details-dropdown-left', 'value'),
     dash.dependencies.Input('race-dropdown-right', 'value'),
     dash.dependencies.Input('year-dropdown-right', 'value'),
     dash.dependencies.Input('athlete-dropdown-right', 'value'),
     dash.dependencies.Input('dist-radio-right', 'value'),
     dash.dependencies.Input('dist-details-dropdown-right', 'value'),
     dash.dependencies.Input('subset-sport', 'value')])
def update_boxplot_1(selected_race_left, selected_year_left, selected_athlete_left,
                     selected_dist_type_left, selected_dist_value_left,
                     selected_race_right, selected_year_right, selected_athlete_right,
                          selected_dist_type_right, selected_dist_value_right,
                          selected_sport):
    # Pull selected race/year dataframe
    df_left = eval(race_options[selected_race_left][selected_year_left][0])
    df_right = eval(race_options[selected_race_right][selected_year_right][0])
    # Get specific athlete times for selected sport
    athlete_time_left = df_left[df_left['name']==selected_athlete_left][selected_sport].values[0]
    athlete_time_right = df_right[df_right['name']==selected_athlete_right][selected_sport].values[0]
    # Get all times for selected sport and subset, using selected_dist_type to filter (for each histogram)
    if (selected_dist_type_left == 'All'):
        all_times_left = df_left[selected_sport].dropna()
    else:
        all_times_left = df_left[df_left[selected_dist_type_left.lower()]==selected_dist_value_left.lower()][selected_sport].dropna()
    if (selected_dist_type_right == 'All'):
        all_times_right = df_right[selected_sport].dropna()
    else:
        all_times_right = df_right[df_right[selected_dist_type_right.lower()]==selected_dist_value_right.lower()][selected_sport].dropna()
    # Set bins and find maximum value for y axis
    nbins = 12
    ymax = max(
        np.histogram(all_times_left, bins = nbins)[0].max(),
        np.histogram(all_times_right, bins = nbins)[0].max()
    )
    # Calculate athletes' rank and percentile
    athlete_rank_left = (all_times_left < athlete_time_left).values.sum() + 1
    athlete_percentile_left = int(round((athlete_rank_left/len(all_times_left))*100))
    athlete_rank_right = (all_times_right < athlete_time_right).values.sum() + 1
    athlete_percentile_right = int(round((athlete_rank_right/len(all_times_right))*100))
    # Create plot
    trace0 = go.Box(
        x = all_times_left,
        jitter = 0.4,
        pointpos = 0,
        boxpoints = 'all',
        name = selected_race_left + ' ' + selected_year_left + ': ' + selected_dist_value_left + ' ',
        marker = dict(color = 'rgb(22, 96, 167)'),
        line = dict(color = 'rgb(22, 96, 167)'),
        legendgroup = "athlete_left"
                 )
    trace1 = go.Box(
        x = all_times_right,
        jitter = 0.4,
        pointpos = 0,
        boxpoints = 'all',
        name = selected_race_right + ' ' + selected_year_right + ': ' + selected_dist_value_right,
        marker = dict(color = 'rgb(205, 12, 24)'),
        line = dict(color = 'rgb(205, 12, 24)'),
        legendgroup = 'athlete_right'
    )
    trace2 = go.Scatter(
         x = [athlete_time_left],
         y = [selected_athlete_left],
         mode = 'markers',
         marker = dict(size = 12,
                       color = 'rgb(115, 157, 198)',
                       line = dict(color = 'rgb(22, 96, 167)',
                                   width = 2)),
         name = selected_athlete_left + '<br>' +
         "{0} percentile ({1} out of {2})".format(
             convert_numeric_to_ordinal(athlete_percentile_left),
             athlete_rank_left,
             len(all_times_left)),
         legendgroup = 'athlete_left'
         )
    trace3 = go.Scatter(
         x = [athlete_time_right],
         y = [selected_athlete_right + ' '],
         mode = 'markers',
         marker = dict(size = 12,
                       color = 'rgb(246, 141, 141)',
                       line = dict(color = 'rgb(205, 12, 24)',
                                   width = 2)),
         name = selected_athlete_right + '<br>' +
         "{0} percentile ({1} out of {2})".format(
             convert_numeric_to_ordinal(athlete_percentile_right),
             athlete_rank_right,
             len(all_times_right)),
         legendgroup = 'athlete_right'
         )
    trace_blank = go.Scatter(
         x = [athlete_time_right],
         y = [' '],
         mode = 'markers',
         marker = dict(size = 0, color = 'rgb(255, 255, 255)'),
         name = ' ',
         legendgroup = 'blank'
         )
    return {
        'data': [trace2, trace0, trace_blank, trace3, trace1],
        'layout': go.Layout(
            xaxis = {
                'title': selected_sport + " (min)"
            },
            yaxis = {
                'autorange': 'reversed'
            },
            legend = {
                'traceorder': 'grouped+reversed'
            },
            margin = {
                'l': 160
            },
            title = selected_sport
            #,
            # yaxis = {
            #     'overlaying': 'y'
            # }
        )
    }


# Histogram plot
@app.callback(
    dash.dependencies.Output('histogram-main', 'figure'),
    [dash.dependencies.Input('race-dropdown-left', 'value'),
     dash.dependencies.Input('year-dropdown-left', 'value'),
     dash.dependencies.Input('athlete-dropdown-left', 'value'),
     dash.dependencies.Input('dist-radio-left', 'value'),
     dash.dependencies.Input('dist-details-dropdown-left', 'value'),
     dash.dependencies.Input('race-dropdown-right', 'value'),
     dash.dependencies.Input('year-dropdown-right', 'value'),
     dash.dependencies.Input('athlete-dropdown-right', 'value'),
     dash.dependencies.Input('dist-radio-right', 'value'),
     dash.dependencies.Input('dist-details-dropdown-right', 'value'),
     dash.dependencies.Input('subset-sport', 'value')])
def update_histogram_main(selected_race_left, selected_year_left, selected_athlete_left,
                          selected_dist_type_left, selected_dist_value_left,
                          selected_race_right, selected_year_right, selected_athlete_right,
                          selected_dist_type_right, selected_dist_value_right,
                          selected_sport):
    # Pull selected race/year dataframe
    df_left = eval(race_options[selected_race_left][selected_year_left][0])
    df_right = eval(race_options[selected_race_right][selected_year_right][0])
    # Get specific athlete times for selected sport
    athlete_time_left = df_left[df_left['name']==selected_athlete_left][selected_sport].values[0]
    athlete_time_right = df_right[df_right['name']==selected_athlete_right][selected_sport].values[0]
    # Get all times for selected sport and subset (for each histogram)
    if (selected_dist_type_left == 'All'):
        all_times_left = df_left[selected_sport].dropna()
    else:
        all_times_left = df_left[df_left[selected_dist_type_left.lower()]==selected_dist_value_left.lower()][selected_sport].dropna()
    if (selected_dist_type_right == 'All'):
        all_times_right = df_right[selected_sport].dropna()
    else:
        all_times_right = df_right[df_right[selected_dist_type_right.lower()]==selected_dist_value_right.lower()][selected_sport].dropna()
    # Set bins and find maximum value for y axis
    nbins = 12
    ymax = max(
        np.histogram(all_times_left, bins = nbins)[0].max(),
        np.histogram(all_times_right, bins = nbins)[0].max()
    )
    # Calculate athletes' rank and percentile
    athlete_rank_left = (all_times_left < athlete_time_left).values.sum() + 1
    athlete_percentile_left = int(round((athlete_rank_left/len(all_times_left))*100))
    athlete_rank_right = (all_times_right < athlete_time_right).values.sum() + 1
    athlete_percentile_right = int(round((athlete_rank_right/len(all_times_right))*100))
    # Create plot
    return {
        'data': [go.Histogram(
                    x=all_times_left,
                    xbins=dict(
                        start=np.min(all_times_left),
                        size=(np.max(all_times_left)-np.min(all_times_left))/nbins,
                        end=np.max(all_times_left)),
                    name = selected_race_left + ' ' + selected_year_left + ': ' + selected_dist_value_left,
                    marker=dict(color='rgb(22, 96, 167)'),
                    opacity = 0.5,
                    legendgroup = 'Person1'
                ),
                 go.Histogram(
                    x=all_times_right,
                    xbins=dict(
                        start=np.min(all_times_right),
                        size=(np.max(all_times_right)-np.min(all_times_right))/nbins,
                        end=np.max(all_times_right)),
                    name = selected_race_right + ' ' + selected_year_right + ': ' + selected_dist_value_right,
                    marker=dict(color='rgb(205, 12, 24)'),
                    opacity = 0.5,
                    legendgroup = 'Person2'
                ),
                 go.Scatter(
                     x = [athlete_time_left, athlete_time_left],
                     y = [0, ymax],  # Draw to max y value of histogram
                     mode = 'lines',
                     name = selected_athlete_left + '<br>' +
                     "{0} percentile ({1} out of {2})".format(
                         convert_numeric_to_ordinal(athlete_percentile_left),
                         athlete_rank_left,
                         len(all_times_left)),
                     legendgroup = 'Person1',
                     line = dict(
                         color = ('rgb(22, 96, 167)'),
                         width = 2)
                 ),
                 go.Scatter(
                     x = [athlete_time_right, athlete_time_right],
                     y = [0, ymax],  # Draw to max y value of histogram
                     mode = 'lines',
                     name = selected_athlete_right + '<br>' +
                     "{0} percentile ({1} out of {2})".format(
                         convert_numeric_to_ordinal(athlete_percentile_right),
                         athlete_rank_right,
                         len(all_times_right)),
                     legendgroup = 'Person2',
                     line = dict(
                         color = ('rgb(205, 12, 24)'),
                         width = 2)
                 )
                ],
        'layout': go.Layout(
            xaxis={
                'title': selected_sport + " (min)"
            },
            yaxis={
                'title': 'Frequency'
            },
            title = selected_sport,
            barmode = 'overlay'
        )
    }


if __name__ == '__main__':
    app.run_server(debug=True)
