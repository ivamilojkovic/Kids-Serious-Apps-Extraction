#%% importing required libraries
import dash
import dash_table
import dash_bootstrap_components as dbc
import dash_core_components as dcc    
import dash_html_components as html
from dash.dependencies import Input, Output, State, ALL 
import plotly
import random
import plotly.graph_objs as go
from collections import deque
import plotly.express as px
from dash.exceptions import PreventUpdate
import pickle

import pandas as pd
import json


#%% Import our DataBases

# New database
with open('Ourdatabase.json') as f:
  data = json.load(f)

data = data['_default']
df = pd.DataFrame()
df = pd.DataFrame(data).transpose()

df['score'] = df['score'].apply(lambda x: round(x, 0))
num_rows = len(df['title'])
num_col = len(df.columns)
num_categories_after = len(list(set(df['genre'])))

# Old database
data2 = pd.read_csv('Google-Playstore.csv')
data2 = data2.rename({'App Name': 'title',
			   'Category': 'genre',
			   'Rating': 'score',
			   'Installs': 'installs'}, axis=1)
data2['score'] = data2['score'].apply(lambda x: round(x, 0))

num_rows_before = len(data2['title'])
num_col_before = len(data2.columns)
num_categories_before = len(list(set(data2['genre'])))

# Aggregation between apps and publications
with open('pubs_per_game.pickle', 'rb') as f:
    data_file = pickle.load(f)

with open('dict_game_scores.pickle', 'rb') as f:
    pub_scores_file = pickle.load(f)

with open('number_pubs_per_game.pickle', 'rb') as f:
    num_pub_per_game = pickle.load(f)

#%%

df['Study type'] = ''
df['Number of publications'] = 0

study_types_all = []
for game_name, pubs in pub_scores_file.items():
	study_types = []
	for pub in pubs:
		study_types.append(max(pub, key=pub.get))
		study_types_all.append(max(pub, key=pub.get))
	data_file[game_name]['Study Type']=study_types

	idx = list(df['title']).index(game_name)
	if game_name in list(df['title']):		
		df['Study type'][idx] = study_types
		df['Number of publications'][idx] = int(num_pub_per_game[game_name])
	else:
		df['Study type'][idx] = []
		df['Number of publications'][idx] = 0

# All publications for all games
df_list = pd.DataFrame(study_types_all, columns=['Study Type'])

# Sort df according to the number of publications
df.sort_values(
	by=['Number of publications'], 
	ascending=False, 
	ignore_index=False,
	inplace=True
	)

#%%

################################### Create App #################################
app = dash.Dash(__name__)

PAGE_STYLE = {
    'top': 0,
	'background': 'white',
	'margin-left': "1%", 
	'margin-right': "1%",
}

TEXT_STYLE = {
	'font_family': 'times',
	'font_size': '22px',
    'textAlign': 'center',
    'color': '#d7d8da',
	'margin-bottom': '20px'
}

HIGHLIGHT_STYLE = {
	'font_family': 'times',
	'font_size': '28px',
    'textAlign': 'center',
    'color': '#339966',
	'fontWeight': 'bold',
	'margin-bottom': '20px'
}

HIGHLIGHT_STYLE_2 = {
	'font_family': 'times',
	'font_size': '20px',
    'textAlign': 'left',
    'color': 'white',
	'fontWeight': 'bold',
	'margin-bottom': '10px',
	'margin-right': '10px',
	'margin-left': '10px',
	'margin-top': '10px',
}



CARD_TEXT_STYLE = {
	'font_family': 'times',
    'font_size': '14px',
    'textAlign': 'center',
    'color': '#009933'
}				

button_style = {
	'font_family': 'times',
	'font-size': '10px',
	'width': '200px', 
	'display': 'block', 
	'margin-bottom': '4px', 
	'height':'35px',
	'textAlign': 'center',
	'background-color': '#339966',
	'color':'white',
	'align-items': 'center',
	'border-radius': '15px',
	'borderBottom': '1px solid #d6d6d6',
	'padding': '6px',
	'float': 'left',
}

clicked_button_style = {
	'font_family': 'times',
	'font-size': '10px',
	'width': '200px', 
	'display': 'block', 
	'margin-bottom': '4px', 
	'height':'35px',
	'textAlign': 'center',
	'background-color': '#133926',
	'color':'white',
	'align-items': 'center',
	'border-radius': '15px',
	'borderBottom': '1px solid #d6d6d6',
	'padding': '6px',
	'float': 'left',
}

button_style_2 = {
	'font_family': 'times',
	'fontSize': '10px',
	'width': '280px', 
	'display': 'block', 
	'margin-bottom': '4px', 
	'height':'60px',
	'textAlign': 'center',
	'background-color': '#339966',
	'color':'white',
	'align-items': 'center',
	'border-radius': '15px',
	'borderBottom': '1px solid #d6d6d6',
	'padding': '6px',
	'float': 'left',
}

tabs_styles = {
	'font_family': 'times',
    'height': '50px',
    'align-items': 'center'
}

tab_style = {
	'font_family': 'times',
    'borderBottom': '1px solid #d6d6d6',
    'padding': '6px',
    'fontWeight': 'bold',
    'border-radius': '15px',
    'background-color': '#F2F2F2',
    'box-shadow': '4px 4px 4px 4px lightgrey',
}

card_style = {
	'font_family': 'times',
    'borderBottom': '1px solid #d6d6d6',
    'padding': '6px',
    'fontWeight': 'bold',
    'border-radius': '15px',
    'background-color': '#2d3035',
	'width':"50%",
	'align-items': 'center',
	'margin-left':'30px',
	'margin-right': '5px',
	'display': 'inline-block',
	'float': 'left',
	'height':'560px',
}
 
card_style_2 = {
	'top': '0',
	'font_family': 'times',
    'borderBottom': '1px solid #d6d6d6',
    'padding': '6px',
    'fontWeight': 'bold',
    'border-radius': '15px',
    'background-color': '#2d3035',
	'display': 'inline-block',
	'width': '21%',
	'align-items': 'center',
	'margin-right': '5px',
	'margin-left': '0px',
	'height':'560px',
	'float': 'left',
}

card_style_3 = {
	'top': 0,
	'font_family': 'times',
    'borderBottom': '1px solid #d6d6d6',
    'padding': '6px',
    'fontWeight': 'bold',
    'border-radius': '15px',
    'background-color': '#2d3035',
	'width':"40%",
	'align-items': 'center',
	'margin-left':'5px',
	'margin-right': '5px',
	'display': 'inline-block',
	'height':'560px',
	'float': 'center',
}


card_style_4 = {
	'top': 0,
	'font_family': 'times',
    'borderBottom': '1px solid #d6d6d6',
    'padding': '6px',
    'fontWeight': 'bold',
    'border-radius': '15px',
    'background-color': '#2d3035',
	'width':"25%",
	'align-items': 'center',
	'margin-left':'5px',
	'margin-right': '5px',
	'display': 'inline-block',
	'height':'560px',
	'float': 'center',
}

card_style_5 = {
	'top': 0,
	'font_family': 'times',
    'borderBottom': '1px solid #d6d6d6',
    'padding': '6px',
    'fontWeight': 'bold',
    'border-radius': '15px',
    'background-color': '#2d3035',
	'align-items': 'center',
	'margin-left':'1px',
	'margin-right': '1px',
	'margin-bottom': '1px',
	'display': 'block',
	'height':'45%',
	'width':'70%',
	'float': 'center',
}

card_small = {
	'background-color': '#2f3237',
    "margin": "1px",
	'border-radius': '5px',
	'font_family': 'times',
    'padding': '6px',
	'width':'72%',
	'height':'20%',
	"border":"1px solid #464a53",
	'display': 'inline-block',
	'box-shadow': '1px 1px 2px 2px #17191c',
	'fontSize': '16px',
	'textAlign': 'right',
	'color': '#339966',
	'margin-right': '10px'
}
card_small_url = {
	'background-color': '#2f3237',
    "color": "white",
    "fontSize": '10px',
    "margin": "1px",
	'border-radius': '5px',
	'font_family': 'times',
    'padding': '6px',
	'width':'72%',
	'height':'20%',
	"border":"1px solid #464a53",
	'display': 'inline-block',
	'box-shadow': '1px 1px 2px 2px #17191c',
	'textAlign': 'left',
	'margin-right': '10px'
}

tab_selected_style = {
	'font_family': 'times',
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': '#339966',
    'color': 'white',
    'padding': '6px',
    'border-radius': '15px',
}

style_label_number = {
	'font_family': 'times',
	'color': 'white',
	'fontWeight': 'bold',
	'align-items': 'center',
	'font_size': '54px',
	"display": "block",
	"margin-bottom":"30px",
}




HEADER = html.Div([
			html.Div([
				html.Div([
					html.H3('CHARACTERIZATION OF RELEVANT SERIOUS GAMES', 
					style = {'margin-bottom': '0px', 'color': 'black', 'font_family': 'times'}),
				])
			], className = "create_container1 four columns", id = "title"),
	
		], id = "header", className = "row flex-display", style = {"margin-bottom": "20px", 'textAlign': 'center', 'font_family': 'times'})

TABS = html.Div([
		html.Div([
			dcc.Tabs(id = "tabs-styled-with-inline", value = 'tab-1', children = [
				dcc.Tab(label = 'App Databases', value = 'tab-1', style = tab_style, selected_style = tab_selected_style),
				dcc.Tab(label = 'Application', value = 'tab-2', style = tab_style, selected_style = tab_selected_style),
				dcc.Tab(label = 'PubMed Publication', value = 'tab-3', style = tab_style, selected_style = tab_selected_style),
				dcc.Tab(label = 'Publication', value = 'tab-4', style = tab_style, selected_style = tab_selected_style),
			], style = tabs_styles),
			html.Div(id = 'tabs-content-inline')
		], className = "create_container3 eight columns", ),
		], className = "row flex-display")

btnlst_1 = [html.Button(name, id={'type' : 'mybuttons','index' : i}, n_clicks=0, style=button_style) for i, name in enumerate(df['title'])]

content_page_1 = \
	html.Div([
		html.Div([
			dbc.Row([							
				dbc.Col([ # select app column
				html.Div([
					html.H2(
						'SELECT APP FEATURE', 
						className = 'fix_label', 
						style = HIGHLIGHT_STYLE
						),
					dcc.RadioItems(
						id = 'radio_items',
						labelStyle = {"display": "inline-block"},
						options = [
							{'label': 'App Category', 'value': 'genre'},
							{'label': 'App Rating', 'value': 'score'},
							{'label': 'Number of installations:', 'value': 'installs'},
							],
						value = 'genre',
						inputStyle={"margin-left": "30px"},
						style = TEXT_STYLE, 
						className = 'dcc_compon'
						),
					dcc.Loading(
						id="loading-1",
						children = [
							dcc.Graph(
								id='the_graph_1', 
								style={
									'width': '50%', 
									'height': '90%', 
									'display': 'inline-block',
									'textAlign': 'center'
									}
								),
							dcc.Graph(
								id='the_graph_2', 
								style={
									'width': '50%', 
									'height': '90%', 
									'display': 'inline-block',
									'textAlign': 'center'
									}
								)
							],
						type="circle", 
						color = 'white',
						),
					]),
					],
					style = card_style
					),

				dbc.Col([ # number of apps and categories column
					html.Div([
						html.H2('AFTER FILTERING', className = 'fix_label', style = HIGHLIGHT_STYLE),
						html.Label(
							id='label_tot_num_after',
							children=["Number of applications: "],  
							style = {
								'font_family': 'times',
								'font_size': '22px',
								'textAlign': 'center',
								'color': '#d7d8da',
								'margin-bottom': '30px',
								"display": "block"
							}),
						html.H2(children= str(num_rows), style=style_label_number),
						html.Label(
							id='label_categ_num_after',
							children="Number of learning categories: ", 
							style = {
								'font_family': 'times',
								'font_size': '22px',
								'textAlign': 'center',
								'color': '#d7d8da',
								'margin-bottom': '30px',
								"display": "block"
							}),
						html.H2(children= str(num_categories_after), style=style_label_number),
						html.Label(
							id='label_categ_num_after_val', 
							style = {
								'font_family': 'times',
								'font_size': '22px',
								'textAlign': 'center',
								'color': '#d7d8da',
								'margin-bottom': '50px',
								"display": "block"
							}),
						html.H2('BEFORE FILTERING', className = 'fix_label', style = HIGHLIGHT_STYLE),	
						html.Label(
							id='label_tot_num_before',
							children="Number of applications: ", 
							style = {
								'font_family': 'times',
								'font_size': '22px',
								'textAlign': 'center',
								'color': '#d7d8da',
								'margin-bottom': '30px',
								"display": "block"
							}),
						html.H2(children= str(num_rows_before), style=style_label_number),	
						html.Label(
							id='label_categ_num_before',
							children="Number of learning categories: ", 
							style = {
								'font_family': 'times',
								'font_size': '22px',
								'textAlign': 'center',
								'color': '#d7d8da',
								'margin-bottom': '30px',
								"display": "block"
							}),
						html.H2(children= str(num_categories_before), style=style_label_number),
						],
						style={'top': '0'},
						)
					],
					style = card_style_2
					),
				dbc.Col([ # number of apps and categories column
					html.Div([
						html.H2('LIST OF APPS', className = 'fix_label', style = HIGHLIGHT_STYLE),
						html.Div(btnlst_1, 
						style={
							"height":"470px", 
							"overflowY": "auto", 
							"color":"white",
							'align-items': 'center',
							'margin-right': '5px',
							'margin-left': '50px',
							'background-color': '#2d3035',
							'font-family':'times',
							'list-style': 'None',
							'float':'left',
							'flush':'False',
							'scrollbar-width':'none',
							'-ms-overflow-style':'none'
						}						
						),
					], style = {
						'align-items': 'center',
						'margin-right': '0px',
						'margin-left': '0px',
						
					}),
				],
				style = card_style_2
				),
				]),
			], 
			className = "create_container3 four columns", 
			style={'textAlign': 'center',  'align-items': 'center'}
			),
		], 
		className = "row flex-display", 
		style={'textAlign': 'center',  'align-items': 'center'}
		)
		
##################################################### PAGE 2 ###############################################################


def make_small_cards(header, idd, is_url = False):

	if is_url==False:
		card = dbc.Card(
				dbc.CardBody([
					html.H2(header, className="card-title", style= HIGHLIGHT_STYLE_2),
					html.H2(id = idd, 
						style={
							'font_family': 'times',
							'font_size': '20px',
							'textAlign': 'right',
							'color': '#339966',
							'margin-right': '1px'
						}
					),
				], style = card_small)
			)
		return card
	else:
		card = dbc.Card(
				dbc.CardBody([
					html.H2(header, className="card-title", style= HIGHLIGHT_STYLE_2),
					html.A(id=idd,target="_blank", 
						style={
							'font_family': 'times',
							'fontSize': '10',
							'textAlign': 'right',
							'color': '#339966',
						}
					),
				], style = card_small_url)
			)
		return card


content_page_2 = \
	html.Div([
		html.Div([
			dbc.Row([	

				dbc.Col([ # select app column
					html.Div([
						html.H2(
							[html.Div(id = 'btn-out-container')],
							id='app-name',
							style = HIGHLIGHT_STYLE,
							),
						make_small_cards('Learning Category', 'btn-genre'),
						make_small_cards('Rating', 'btn-score'),
						make_small_cards('Number of publications', 'btn-num-papers'),
						make_small_cards('URL', 'btn-url', True),
					]),
				],  style=card_style_4),

				dbc.Col([ # List of publications
					html.Div([
						html.H2('LIST OF PUBLICATIONS', className = 'fix_label', style = HIGHLIGHT_STYLE),
						html.Div(id = 'btn-list-2',
							style={
								"height":"470px", 
								"overflowY": "auto", 
								"color":"white",
								'align-items': 'center',
								'margin-right': '5px',
								'margin-left': '20px',
								'background-color': '#2d3035',
								'font-family':'times',
								'list-style': 'None',
								'float':'left',
								'flush':'False',
								'scrollbar-width':'none',
								'-ms-overflow-style':'none'
							}
						)],
						style = {
							'align-items': 'center',
							'margin-right': '0px',
							'margin-left': '1px',
						}
					)],
					style = card_style_4
					),

				dbc.Col([ # Publication statistics
					dbc.Row([
						html.Div([	
							dcc.Loading(
							id="loading-3",
							children = [
								dcc.Graph(
									id='the_graph_bar_1',
									),
								],
							type="circle", 
							color = 'white',
							),
						],
						style =
						{
							'align-items': 'center',
							'margin-right': '0px',
							'margin-left': '1px',
							'textAlign': 'center',
						}
					)],
					style = card_style_5
					),
					dbc.Row([
						html.Div([
							dcc.Loading(
							id="loading-4",
							children = [
								dcc.Graph(
									id='the_graph_bar_2',
									),
								],
							type="circle", 
							color = 'white',
							),		
						],
						style = {
							'align-items': 'center',
							'margin-right': '0px',
							'margin-left': '1px',
							
						}
					)],
					style = card_style_5
					),
				], style = {
					'top': 0,
					'align-items': 'center',
					'margin-left':'5px',
					'margin-right': '5px',
					'display': 'inline-block',
					'height':'605px',
					'width':'45%',
					'float': 'left',
					'margin-bottom': '3px',
					'margin-top': '1px',
					'background-color':'white',
				}),
			]),
			], 
			className = "create_container3 four columns", 
			style={'textAlign': 'center',  'align-items': 'center', 'float':'center'}
			),
		], 
		className = "row flex-display", 
		style={'textAlign': 'center',  'align-items': 'center', 'float':'center', 'margin-left':'150px'}
		)


################################################# CALLBACKS ##################################################################

@app.callback(
    Output(component_id='the_graph_1', component_property='figure'),
    [Input(component_id='radio_items', component_property='value')]
)

def update_graph(radio_items):
    
	dff = df
	if radio_items=='genre':
		colors = color_discrete_sequence=px.colors.qualitative.T10
	if radio_items=='score':
		colors = color_discrete_sequence=px.colors.qualitative.Dark24
	if radio_items=='installs':
		colors = color_discrete_sequence=px.colors.qualitative.Vivid

	piechart = px.pie(
		data_frame=dff,
		names=radio_items,
		hole=.4,
		color_discrete_sequence=colors,
		title = "Results after filtering",
		)
	
	piechart.update_traces(textposition ='inside')
	piechart.update_layout(
		autosize = True, #width = 250, height = 300,
		margin=dict(t=40, b=10, l=40, r=20),
		plot_bgcolor='#2d3035', paper_bgcolor='#2d3035',
		title_font=dict(size=20, color='#d7d8da', family="times"),
		title_x=0.5,
		font=dict(color='#8a8d93', size = 12, family='times'),
		legend=dict(orientation="h", yanchor="bottom", y=0, xanchor="right", x=0)
		)
	piechart.update_layout(showlegend=False)
	
	piechart.update_xaxes(showticklabels=False)  
	piechart.update_yaxes(showticklabels=False)

	return piechart

@app.callback(
	Output(component_id='the_graph_2', component_property='figure'),
    [Input(component_id='radio_items', component_property='value')]
)

def update_graph(radio_items):
    
	dff = df
	if radio_items=='genre':
		colors = color_discrete_sequence=px.colors.qualitative.T10
	if radio_items=='score':
		colors = color_discrete_sequence=px.colors.qualitative.Dark24
	if radio_items=='installs':
		colors = color_discrete_sequence=px.colors.qualitative.Vivid


	piechart = px.pie(
		data_frame=data2,
		names=radio_items,
		hole=.4,
		color_discrete_sequence=colors,
		title = "Results before filtering",
		)
	
	piechart.update_traces(textposition ='inside')
	piechart.update_layout(
		autosize = True, #width = 250, height = 300,
		margin=dict(t=40, b=10, l=20, r=40),
		plot_bgcolor='#2d3035', paper_bgcolor='#2d3035',
		title_font=dict(size=20, color='#d7d8da', family="times"),
		title_x=0.5,
		font=dict(color='#8a8d93', size = 12, family='times'),
		legend=dict(orientation="h", yanchor="bottom", y=0, xanchor="right", x=0)
		)
	piechart.update_layout(showlegend=False)
	
	piechart.update_xaxes(showticklabels=False)  
	piechart.update_yaxes(showticklabels=False)

	return piechart


@app.callback(Output('tabs-content-inline', 'children'),
              [Input('tabs-styled-with-inline', 'value')])

def render_content(tab):
	if tab == 'tab-1':
		return content_page_1
	elif tab=='tab-2':
		return content_page_2

@app.callback(
    Output('local-store-2', 'data'),
	[Input({'type':'mybuttons', 'index':ALL}, 'n_clicks')],
)

def change_app_info(n_clicks):
	
	changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
	if changed_id == '.':
		msg = 'None of the buttons have been clicked yet'
	else:
        # do additional parsing of changed_id here as necessary
		msg = 'Changed property: {}'.format(changed_id)
		ind = changed_id.split(',')[0]
		ind = ind[ind.find(':')+1:]

	return ind

@app.callback(
	[Output('btn-out-container', 'children'), 
	Output('btn-genre', 'children'),
	Output('btn-score', 'children'),
	Output('btn-num-papers', 'children'),
	Output('btn-url', 'href'),
	Output('btn-url', 'children'),
	Output('btn-list-2', 'children'),
	],
    Input('local-store-2', 'data'),
)

def update_second_page(ind):
	
	dff = df
	btnlst_2 = [html.Button(name, id={'type' : 'mybuttons2','index' : i}, n_clicks=0, style=button_style_2) for i, name in enumerate(data_file[dff['title'][int(ind)]]['Title'])]
	return dff['title'][int(ind)], dff['genre'][int(ind)], dff['score'][int(ind)], len(data_file[dff['title'][int(ind)]]['ID']), dff['url'][int(ind)], dff['url'][int(ind)], btnlst_2

@app.callback(
	[
	Output('the_graph_bar_1', 'figure'),
	Output('the_graph_bar_2', 'figure'),
	],
    Input('local-store-2', 'data'),
)

def figures_second_page(ind):
	print(ind)
	fig1 = px.pie(
		data_frame=data_file[df['title'][int(ind)]],
		names='Study Type',
		hole=.4,
		color_discrete_sequence=px.colors.qualitative.T10,
		title = "Game's publications study types",
		)
	fig1.update_traces(textposition ='inside')
	fig1.update_layout(
		autosize = True, height = 270, width = 360,
		margin=dict(t=30, b=0, l=30, r=0),
		title_font=dict(color='#8a8d93', size = 16, family='times'),
		plot_bgcolor='#2d3035', paper_bgcolor='#2d3035',
		font=dict(color='#8a8d93', size = 12, family='times'),
		)

	fig2 = px.pie(
		data_frame=df_list,
		names='Study Type',
		hole=.4,
		color_discrete_sequence=px.colors.qualitative.T10,
		title = "General statistics about study types",
		)
	fig2.update_traces(textposition ='inside')
	fig2.update_layout(
		autosize = True, height = 270, width = 360,
		margin=dict(t=30, b=0, l=30, r=0),
		title_font=dict(color='#8a8d93', size = 16, family='times'),
		plot_bgcolor='#2d3035', paper_bgcolor='#2d3035',
		font=dict(color='#8a8d93', size = 12, family='times'),
		)

	return fig1, fig2


#['Meta Analysis','Observational Study', 'RCT', 'Systematic Review', 'Other']
######################################################### APP MAIN #############################################################
 
app.layout = html.Div([
	dcc.Store(id='local-store-2', storage_type='memory'),
	HEADER, 
	TABS, 
	], 
	style=PAGE_STYLE)

if __name__ == '__main__':
    app.run_server()