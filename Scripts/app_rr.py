import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
import numpy as np


app = dash.Dash()

colors = {
    'background': '#000000',
    'text': '#7FDBFF'
}

results = pd.read_csv('../Data_output/results_Hampton2018.csv')

available_names = np.sort(results['name'].unique())
available_sports = np.array(['time_total', 'swim', 'bike', 'run', 't1', 't2'])

def convert_min_to_time(time):
    hours = int(time/60)
    minutes = time - (hours*60)
    seconds = round((time - int(time))*60)
    #seconds_decimal = (seconds - int(seconds))*100
    if (hours > 0):
        return("%d:%02d:%02d" % (hours, minutes, seconds))
    else:
        return("%02d:%02d" % (minutes, seconds))

app.layout = html.Div([
    html.H1(children='Triathlon Comparison Tool',
            style={
                'textAlign': 'center'
    }),
    
    html.H4(children='...because analysis is the 4th sport.',
            style={'textAlign': 'center'}),
    
    html.H3(children='Hampton Ladies Triathlon 2018',
            style={'textAlign': 'left'}),
    
    html.Br(),
    
    html.Div([
        html.Div([
            html.H6('Select first athlete to compare:'),
            dcc.Dropdown(
                id='vline-name',
                options=[{'label': i, 'value': i} for i in available_names],
                value='Lindsay Brin'
            ),
            
            html.Div(id='name-1-text')
            
        ],
        style={'width': '48%', 'display': 'inline-block'}),

        html.Div([
            html.H6('Select second athlete to compare:'),
            dcc.Dropdown(
                id='vline-name-2',
                options=[{'label': i, 'value': i} for i in available_names],
                value='Rachel Kidd'
            ),
            html.Div(id='name-2-text'),
            html.Div(id = 'comparison-text')
        ],
        style={'width': '48%', 'float': 'right', 'display': 'inline-block'})
    ]),
    
    html.Br(),
    
    html.H6('Select sport to compare:'),
    dcc.RadioItems(
        id='subset-sport',
        options=[{'label': i, 'value': i} for i in available_sports],
        value='time_total',
        labelStyle={'display': 'inline-block'}
    ),


    html.Div([
        html.Div([
            dcc.Graph(
                id='indicator-graphic-hist'
            ),
            html.Div(id='comparison-text',
                     style={'textAlign': 'center'})
        ],
        style={'width': '70%', 'display': 'inline-block'})
        ],
    style = {'textAlign': 'center'}),
    
    html.Br(),
    
    html.Div([
        html.Div([
            dcc.Graph(
                id='indicator-graphic-hist-divisions'
            )
        ],
        style={'width': '70%', 'display': 'inline-block'})
        ],
    style = {'textAlign': 'center'}),    
        
    html.Br(),
    html.Hr(),
    html.Br(),
    
    html.H3('Individual sports',
            style={'textAlign': 'center'}),
    html.Br(),

    
    # Plot row 1
    html.Div([dcc.Graph(id='plot-total-time')],
        style={'width': '48%', 'display': 'inline-block'}),
    
    html.Div([dcc.Graph(id='plot-swim')],
        style={'width': '48%', 'float': 'right', 'display': 'inline-block'}),

    # Plot row 2
    html.Div([dcc.Graph(id='plot-bike')],
        style={'width': '48%', 'display': 'inline-block'}),
    
    html.Div([dcc.Graph(id='plot-run')],
        style={'width': '48%', 'float': 'right', 'display': 'inline-block'}),

    # Plot row 3
    html.Div([dcc.Graph(id='plot-t1')],
        style={'width': '48%', 'display': 'inline-block'}),
    
    html.Div([dcc.Graph(id='plot-t2')],
        style={'width': '48%', 'float': 'right', 'display': 'inline-block'})
    

    
])


# CSS from Dash tutorial
app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})


# Text for person 1
@app.callback(
    dash.dependencies.Output(component_id='name-1-text', component_property='children'),
    [dash.dependencies.Input('vline-name', 'value')]
)
def update_output_div(input_name):
    mylayout = html.Div([
                html.P("Place: {}".format( 
                    results[results['name']==input_name]['place'].values[0]
                )),
                html.P("Division: {}".format( 
                    results[results['name']==input_name]['div'].values[0]
                )),
                html.P("Division place: {}".format( 
                    results[results['name']==input_name]['div_place'].values[0]
                )),
                html.P("Total time: {}".format( 
                    convert_min_to_time(results[results['name']==input_name]['time_total'].values[0])
                )),
                html.P("Swim: {}".format(
                    convert_min_to_time(results[results['name']==input_name]['swim'].values[0])
                )),
                html.P("Bike: {}".format(
                    convert_min_to_time(results[results['name']==input_name]['bike'].values[0])
                )),
                html.P("Run: {}".format(
                    convert_min_to_time(results[results['name']==input_name]['run'].values[0])
                )),
                html.P("T1: {}".format(
                    convert_min_to_time(results[results['name']==input_name]['t1'].values[0])
                )),
                html.P("T2: {}".format(
                    convert_min_to_time(results[results['name']==input_name]['t2'].values[0])
                ))
            ])
    return mylayout

# Text for person 2
@app.callback(
    dash.dependencies.Output(component_id='name-2-text', component_property='children'),
    [dash.dependencies.Input('vline-name-2', 'value')]
)
def update_output_div(input_name):
    mylayout = html.Div([
                html.P("Place: {}".format( 
                    results[results['name']==input_name]['place'].values[0]
                )),
                html.P("Division: {}".format( 
                    results[results['name']==input_name]['div'].values[0]
                )),
                html.P("Division place: {}".format( 
                    results[results['name']==input_name]['div_place'].values[0]
                )),
                html.P("Total time: {}".format( 
                    convert_min_to_time(results[results['name']==input_name]['time_total'].values[0])
                )),
                html.P("Swim: {}".format(
                    convert_min_to_time(results[results['name']==input_name]['swim'].values[0])
                )),
                html.P("Bike: {}".format(
                    convert_min_to_time(results[results['name']==input_name]['bike'].values[0])
                )),
                html.P("Run: {}".format(
                    convert_min_to_time(results[results['name']==input_name]['run'].values[0])
                )),
                html.P("T1: {}".format(
                    convert_min_to_time(results[results['name']==input_name]['t1'].values[0])
                )),
                html.P("T2: {}".format(
                    convert_min_to_time(results[results['name']==input_name]['t2'].values[0])
                ))
            ])
    return mylayout

# Comparison text
@app.callback(
    dash.dependencies.Output(component_id='comparison-text', component_property='children'),
    [dash.dependencies.Input('vline-name', 'value'),
     dash.dependencies.Input('vline-name-2', 'value'),
     dash.dependencies.Input('subset-sport', 'value')]
)
def update_output_div(input_name, input_name_2, subset_sport_name):
    time1 = results[results['name']==input_name][subset_sport_name].values[0]
    time2 = results[results['name']==input_name_2][subset_sport_name].values[0]
    time_difference = abs(time1 - time2)
    if (time1 < time2):
        mylayout = html.Div([
            html.P("{0} was faster than {1} by: {2}".format(
                input_name,
                input_name_2,
                convert_min_to_time(time_difference)))
            ])
    elif (time1 > time2):
        mylayout = html.Div([
            html.P("{1} was faster than {0} by: {2}".format(
                input_name,
                input_name_2,
                convert_min_to_time(time_difference)))
            ])
    elif (time1 == time2):
        mylayout = html.Div([
            html.P("{0} was the same speed as {1}!".format(
                input_name,
                input_name_2,
                convert_min_to_time(time_difference)))
            ])
    else:
        mylayout = html.Div([
            html.P("I'm sorry, this is confusing.")
            ])
    
    return mylayout


#
# PLOTS 
#

# Plot 1 - radio buttons
@app.callback(
    dash.dependencies.Output('indicator-graphic-hist', 'figure'),
    [dash.dependencies.Input('vline-name', 'value'),
     dash.dependencies.Input('vline-name-2', 'value'),
     dash.dependencies.Input('subset-sport', 'value')])
def update_graph(vline_name_name, vline_name_2_name, subset_sport_name):
    vline_name_pos = results[results['name']==vline_name_name][subset_sport_name].values[0]
    vline_name_2_pos = results[results['name']==vline_name_2_name][subset_sport_name].values[0]
    times = results[subset_sport_name].dropna()
    nbins = 16
    ymax = np.histogram(times, 
                        bins = nbins)[0].max()
    return {
        'data': [go.Histogram(
                    x=times, 
                    xbins=dict(
                        start=np.min(times), 
                        size=(np.max(times)-np.min(times))/nbins, 
                        end=np.max(times)),
                    name = subset_sport_name,
                    showlegend = False,
                    opacity = 0.6,
                    marker=dict(color='rgb(12, 96, 60)')
                ),
                 go.Scatter(
                     x = [vline_name_pos, vline_name_pos],
                     y = [0, ymax],  # Draw to max y value of histogram
                     mode = 'lines',
                     name = vline_name_name,
                     line = dict(
                         color = ('rgb(22, 96, 167)'),
                         width = 2)
                 ),
                 go.Scatter(
                     x = [vline_name_2_pos, vline_name_2_pos],
                     y = [0, ymax],  # Draw to max y value of histogram
                     mode = 'lines',
                     name = vline_name_2_name,
                     line = dict(
                         color = ('rgb(205, 12, 24)'),
                         width = 2)
                 )
                ],
        'layout': go.Layout(
            xaxis={
                'title': subset_sport_name
            },
            yaxis={
                'title': 'Frequency'
            },
            title = subset_sport_name
        )
    }


# Plot 2 - radio buttons and multiple histograms
@app.callback(
    dash.dependencies.Output('indicator-graphic-hist-divisions', 'figure'),
    [dash.dependencies.Input('vline-name', 'value'),
     dash.dependencies.Input('vline-name-2', 'value'),
     dash.dependencies.Input('subset-sport', 'value')])
def update_graph(vline_name_name, vline_name_2_name, subset_sport_name):
    vline_name_pos = results[results['name']==vline_name_name][subset_sport_name].values[0]
    vline_name_2_pos = results[results['name']==vline_name_2_name][subset_sport_name].values[0]
    div_1 = results[results['name']==vline_name_name]['div'].values[0]
    div_2 = results[results['name']==vline_name_2_name]['div'].values[0]
    times_div_1 = results[results['div']==div_1][subset_sport_name].dropna()
    times_div_2 = results[results['div']==div_2][subset_sport_name].dropna()
    nbins = 16
    ymax = max(
        np.histogram(times_div_1,bins = nbins)[0].max(),
        np.histogram(times_div_2,bins = nbins)[0].max()
    )
    return {
        'data': [go.Histogram(
                    x=times_div_1, 
                    xbins=dict(
                        start=np.min(times_div_1), 
                        size=(np.max(times_div_1)-np.min(times_div_1))/nbins, 
                        end=np.max(times_div_1)),
                    name = div_1,
                    marker=dict(color='rgb(22, 96, 167)'),
                    opacity = 0.5,
                    legendgroup = 'Person1'
                ),
                 go.Histogram(
                    x=times_div_2, 
                    xbins=dict(
                        start=np.min(times_div_2), 
                        size=(np.max(times_div_2)-np.min(times_div_1))/nbins, 
                        end=np.max(times_div_2)),
                    name = div_2,
                    marker=dict(color='rgb(205, 12, 24)'),
                    opacity = 0.5,
                    legendgroup = 'Person2'
                ),
                 go.Scatter(
                     x = [vline_name_pos, vline_name_pos],
                     y = [0, ymax],  # Draw to max y value of histogram
                     mode = 'lines',
                     name = vline_name_name,
                     legendgroup = 'Person1',
                     line = dict(
                         color = ('rgb(22, 96, 167)'),
                         width = 2)
                 ),
                 go.Scatter(
                     x = [vline_name_2_pos, vline_name_2_pos],
                     y = [0, ymax],  # Draw to max y value of histogram
                     mode = 'lines',
                     name = vline_name_2_name,
                     legendgroup = 'Person2',
                     line = dict(
                         color = ('rgb(205, 12, 24)'),
                         width = 2)
                 )
                ],
        'layout': go.Layout(
            xaxis={
                'title': subset_sport_name
            },
            yaxis={
                'title': 'Frequency'
            },
            title = subset_sport_name,
            barmode = 'overlay'
        )
    }



# Plot: total time
@app.callback(
    dash.dependencies.Output('plot-total-time', 'figure'),
    [dash.dependencies.Input('vline-name', 'value'),
     dash.dependencies.Input('vline-name-2', 'value')])
def update_graph(vline_name_name, vline_name_2_name):
    subset_sport_name = 'time_total'
    vline_name_pos = results[results['name']==vline_name_name][subset_sport_name].values[0]
    vline_name_2_pos = results[results['name']==vline_name_2_name][subset_sport_name].values[0]
    times = results[subset_sport_name].dropna()
    nbins = 16
    ymax = np.histogram(times, 
                        bins = nbins)[0].max()
    return {
        'data': [go.Histogram(
                    x=times, 
                    xbins=dict(
                        start=np.min(times), 
                        size=(np.max(times)-np.min(times))/nbins, 
                        end=np.max(times)),
                    name = subset_sport_name,
                    showlegend = False
                ),
                 go.Scatter(
                     x = [vline_name_pos, vline_name_pos],
                     y = [0, ymax],  # Draw to max y value of histogram
                     mode = 'lines',
                     name = vline_name_name
                 ),
                 go.Scatter(
                     x = [vline_name_2_pos, vline_name_2_pos],
                     y = [0, ymax],  # Draw to max y value of histogram
                     mode = 'lines',
                     name = vline_name_2_name
                 )
                ],
        'layout': go.Layout(
            xaxis={
                'title': 'Total time (min)'
            },
            yaxis={
                'title': 'Frequency'
            },
            title = 'Total time',
            legend=dict(orientation="h",
                xanchor="center",
                y=1.1,
                x=0.5)
        )
    }


# Plot: swim
@app.callback(
    dash.dependencies.Output('plot-swim', 'figure'),
    [dash.dependencies.Input('vline-name', 'value'),
     dash.dependencies.Input('vline-name-2', 'value')])
def update_graph(vline_name_name, vline_name_2_name):
    subset_sport_name = 'swim'
    vline_name_pos = results[results['name']==vline_name_name][subset_sport_name].values[0]
    vline_name_2_pos = results[results['name']==vline_name_2_name][subset_sport_name].values[0]
    times = results[subset_sport_name].dropna()
    nbins = 16
    ymax = np.histogram(times, 
                        bins = nbins)[0].max()
    return {
        'data': [go.Histogram(
                    x=times, 
                    xbins=dict(
                        start=np.min(times), 
                        size=(np.max(times)-np.min(times))/nbins, 
                        end=np.max(times)),
                    name = subset_sport_name,
                    showlegend = False
                ),
                 go.Scatter(
                     x = [vline_name_pos, vline_name_pos],
                     y = [0, ymax],  # Draw to max y value of histogram
                     mode = 'lines',
                     name = vline_name_name
                 ),
                 go.Scatter(
                     x = [vline_name_2_pos, vline_name_2_pos],
                     y = [0, ymax],  # Draw to max y value of histogram
                     mode = 'lines',
                     name = vline_name_2_name
                 )
                ],
        'layout': go.Layout(
            xaxis={
                'title': 'Swim (min)'
            },
            yaxis={
                'title': 'Frequency'
            },
            title = 'Swim',
            legend=dict(orientation="h",
                xanchor="center",
                y=1.1,
                x=0.5)
        )
    }


# Plot: bike
@app.callback(
    dash.dependencies.Output('plot-bike', 'figure'),
    [dash.dependencies.Input('vline-name', 'value'),
     dash.dependencies.Input('vline-name-2', 'value')])
def update_graph(vline_name_name, vline_name_2_name):
    subset_sport_name = 'bike'
    vline_name_pos = results[results['name']==vline_name_name][subset_sport_name].values[0]
    vline_name_2_pos = results[results['name']==vline_name_2_name][subset_sport_name].values[0]
    times = results[subset_sport_name].dropna()
    nbins = 16
    ymax = np.histogram(times, 
                        bins = nbins)[0].max()
    return {
        'data': [go.Histogram(
                    x=times, 
                    xbins=dict(
                        start=np.min(times), 
                        size=(np.max(times)-np.min(times))/nbins, 
                        end=np.max(times)),
                    name = subset_sport_name,
                    showlegend = False
                ),
                 go.Scatter(
                     x = [vline_name_pos, vline_name_pos],
                     y = [0, ymax],  # Draw to max y value of histogram
                     mode = 'lines',
                     name = vline_name_name
                 ),
                 go.Scatter(
                     x = [vline_name_2_pos, vline_name_2_pos],
                     y = [0, ymax],  # Draw to max y value of histogram
                     mode = 'lines',
                     name = vline_name_2_name
                 )
                ],
        'layout': go.Layout(
            xaxis={
                'title': 'Bike (min)'
            },
            yaxis={
                'title': 'Frequency'
            },
            title = 'Bike',
            legend=dict(orientation="h",
                xanchor="center",
                y=1.1,
                x=0.5)
        )
    }


# Plot: run
@app.callback(
    dash.dependencies.Output('plot-run', 'figure'),
    [dash.dependencies.Input('vline-name', 'value'),
     dash.dependencies.Input('vline-name-2', 'value')])
def update_graph(vline_name_name, vline_name_2_name):
    subset_sport_name = 'run'
    vline_name_pos = results[results['name']==vline_name_name][subset_sport_name].values[0]
    vline_name_2_pos = results[results['name']==vline_name_2_name][subset_sport_name].values[0]
    times = results[subset_sport_name].dropna()
    nbins = 16
    ymax = np.histogram(times, 
                        bins = nbins)[0].max()
    return {
        'data': [go.Histogram(
                    x=times, 
                    xbins=dict(
                        start=np.min(times), 
                        size=(np.max(times)-np.min(times))/nbins, 
                        end=np.max(times)),
                    name = subset_sport_name,
                    showlegend = False
                ),
                 go.Scatter(
                     x = [vline_name_pos, vline_name_pos],
                     y = [0, ymax],  # Draw to max y value of histogram
                     mode = 'lines',
                     name = vline_name_name
                 ),
                 go.Scatter(
                     x = [vline_name_2_pos, vline_name_2_pos],
                     y = [0, ymax],  # Draw to max y value of histogram
                     mode = 'lines',
                     name = vline_name_2_name
                 )
                ],
        'layout': go.Layout(
            xaxis={
                'title': 'Run (min)'
            },
            yaxis={
                'title': 'Frequency'
            },
            title = 'Run',
            legend=dict(orientation="h",
                xanchor="center",
                y=1.1,
                x=0.5)
        )
    }


# Plot: t1
@app.callback(
    dash.dependencies.Output('plot-t1', 'figure'),
    [dash.dependencies.Input('vline-name', 'value'),
     dash.dependencies.Input('vline-name-2', 'value')])
def update_graph(vline_name_name, vline_name_2_name):
    subset_sport_name = 't1'
    vline_name_pos = results[results['name']==vline_name_name][subset_sport_name].values[0]
    vline_name_2_pos = results[results['name']==vline_name_2_name][subset_sport_name].values[0]
    times = results[subset_sport_name].dropna()
    nbins = 16
    ymax = np.histogram(times, 
                        bins = nbins)[0].max()
    return {
        'data': [go.Histogram(
                    x=times, 
                    xbins=dict(
                        start=np.min(times), 
                        size=(np.max(times)-np.min(times))/nbins, 
                        end=np.max(times)),
                    name = subset_sport_name,
                    showlegend = False
                ),
                 go.Scatter(
                     x = [vline_name_pos, vline_name_pos],
                     y = [0, ymax],  # Draw to max y value of histogram
                     mode = 'lines',
                     name = vline_name_name
                 ),
                 go.Scatter(
                     x = [vline_name_2_pos, vline_name_2_pos],
                     y = [0, ymax],  # Draw to max y value of histogram
                     mode = 'lines',
                     name = vline_name_2_name
                 )
                ],
        'layout': go.Layout(
            xaxis={
                'title': 'T1 (min)'
            },
            yaxis={
                'title': 'Frequency'
            },
            title = 'T1',
            legend=dict(orientation="h",
                xanchor="center",
                y=1.1,
                x=0.5)
        )
    }




# Plot: t2
@app.callback(
    dash.dependencies.Output('plot-t2', 'figure'),
    [dash.dependencies.Input('vline-name', 'value'),
     dash.dependencies.Input('vline-name-2', 'value')])
def update_graph(vline_name_name, vline_name_2_name):
    subset_sport_name = 'swim'
    vline_name_pos = results[results['name']==vline_name_name][subset_sport_name].values[0]
    vline_name_2_pos = results[results['name']==vline_name_2_name][subset_sport_name].values[0]
    times = results[subset_sport_name].dropna()
    nbins = 16
    ymax = np.histogram(times, 
                        bins = nbins)[0].max()
    return {
        'data': [go.Histogram(
                    x=times, 
                    xbins=dict(
                        start=np.min(times), 
                        size=(np.max(times)-np.min(times))/nbins, 
                        end=np.max(times)),
                    name = subset_sport_name,
                    showlegend = False
                ),
                 go.Scatter(
                     x = [vline_name_pos, vline_name_pos],
                     y = [0, ymax],  # Draw to max y value of histogram
                     mode = 'lines',
                     name = vline_name_name
                 ),
                 go.Scatter(
                     x = [vline_name_2_pos, vline_name_2_pos],
                     y = [0, ymax],  # Draw to max y value of histogram
                     mode = 'lines',
                     name = vline_name_2_name
                 )
                ],
        'layout': go.Layout(
            xaxis={
                'title': 'T2 (min)'
            },
            yaxis={
                'title': 'Frequency'
            },
            title = 'T2',
            legend=dict(orientation="h",
                xanchor="center",
                y=1.1,
                x=0.5)
        )
    }











if __name__ == '__main__':
    app.run_server()