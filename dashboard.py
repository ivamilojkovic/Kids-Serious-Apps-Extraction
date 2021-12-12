# importing required libraries
import dash
import dash_table
import dash_bootstrap_components as dbc
import dash_core_components as dcc    
import dash_html_components as html
from dash.dependencies import Input, Output, State 
import plotly
import random
import plotly.graph_objs as go
from collections import deque
import plotly.express as px

import pandas as pd
import json


# Import our DataBase

with open('Ourdatabase.json') as f:
  data = json.load(f)

data = data['_default']
df = pd.DataFrame()
df = pd.DataFrame(data).transpose()

df['score'] = df['score'].apply(lambda x: round(x, 0))

# Create App
app = dash.Dash(__name__)

CONTENT_STYLE = {
    'margin-left': '1%',
    'margin-right': '1%',
    'top': 0,
    'padding': '5px 5px'
}

TEXT_STYLE = {
	'font_family': 'times',
	'font_size': '22px',
    'textAlign': 'center',
    'color': '#d7d8da',
	'margin-bottom': '20px'
}

HIGHLIGHT_STYLE = {'font_family': 'times',
	'font_size': '28px',
    'textAlign': 'center',
    'color': '#339966',
	'fontWeight': 'bold',
	'margin-bottom': '20px'

}


CARD_TEXT_STYLE = {
	'font_family': 'times',
    'font_size': '14px',
    'textAlign': 'center',
    'color': '#009933'
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
	'width':"70%",
	'align-items': 'center',
	'margin-left':'30px',
	'margin-right': '0px',
	'display': 'inline-block',
	'float': 'left'
}
 

card_style_2 = {
	'top': '0',
	'font_family': 'times',
    'borderBottom': '1px solid #d6d6d6',
    'padding': '6px',
    'fontWeight': 'bold',
    'border-radius': '15px',
    'background-color': '#62656a',
	'display': 'inline-block',
	'width': '21%',
	'align-items': 'center',
	'margin-right': '30px',
	'height':'550px'
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
				dcc.Tab(label = 'Applications', value = 'tab-1', style = tab_style, selected_style = tab_selected_style),
				dcc.Tab(label = 'Application', value = 'tab-2', style = tab_style, selected_style = tab_selected_style),
				dcc.Tab(label = 'PubMed Publications', value = 'tab-3', style = tab_style, selected_style = tab_selected_style),
				dcc.Tab(label = 'Publication', value = 'tab-4', style = tab_style, selected_style = tab_selected_style),
			], style = tabs_styles),
			html.Div(id = 'tabs-content-inline')
		], className = "create_container3 eight columns", ),
		], className = "row flex-display")

# General_stat_after = html.Div([
# 				html.Div([					
# 					html.Label(id='label_tot_num_after',children="Number of applications:", style = TEXT_STYLE),
# 					html.Label(id='label_categ_num_after',children="Number of learning categories:", style = TEXT_STYLE),
# 				])
# 	], style={'height':'100%'})

# General_stat_before = html.Div([
# 				html.Div([					
# 					html.Label(id='label_tot_num_before',children="Number of applications:", style = TEXT_STYLE),
# 					html.Label(id='label_categ_num_before',children="Number of learning categories:", style = TEXT_STYLE),
# 				])
# 	])

# Piechart_1 = html.Div([
#         html.Div([
# 			dcc.Loading(
# 					id="loading-1",
# 					children = [dcc.Graph(id='the_graph', style={
# 														'width': '50%', 
# 														'height': '90%', 
# 														'display': 'inline-block',
# 														'textAlign': 'center'}),
# 								dcc.Graph(id='the_graph_2', style={
# 														'width': '50%', 
# 														'height': '90%', 
# 														'display': 'inline-block',
# 														'textAlign': 'center'})],
# 					type="circle",
# 					), 
#         ], className = "create_container3 four columns", style={'textAlign': 'center'}),
#     ], className = "row flex-display", style={'textAlign': 'center', 'height':'100%'})

	

# radio_buttons_1 = html.Div([
# 					html.Div([
# 						html.P('Select App Feature', 
# 							className = 'fix_label', 
# 							style = TEXT_STYLE),
# 						dcc.RadioItems(
# 							id = 'radio_items',
# 							labelStyle = {"display": "inline-block"},
# 							options = [
# 								{'label': 'App Category', 'value': 'genre'},
# 								{'label': 'App Rating', 'value': 'score'},
# 								{'label': 'Number of reviews', 'value': 'reviews'}],
# 							value = 'genre',
# 							inputStyle={"margin-left": "30px"},
# 							style = TEXT_STYLE, className = 'dcc_compon'),
# 					], className = "create_container3 six columns"),
# 				], className = "row flex-display", style={'height':'100%'})

# content_first_column =  dbc.Card([
#                  		dbc.CardBody([
# 							 radio_buttons_1,
# 							 Piechart_1,						 
# 							])
# 						], #style = card_style 
# 						)

# content_second_column = html.Div([
# 							html.Div([
# 								dbc.Card([
#                  					dbc.CardBody([
# 								 		General_stat_after,
# 								 	])
# 							],
# 							)
# 							], style={"height":"100%"})
# ])

content_page_1 = \
	html.Div([
		html.Div([
			dbc.Row([							
				dbc.Col([ # select app column
				html.Div([
					html.P(
						'Select App Feature', 
						className = 'fix_label', 
						style = TEXT_STYLE
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
								id='the_graph', 
								style={
									'width': '50%', 
									'height': '80%', 
									'display': 'inline-block',
									'textAlign': 'center'
									}
								),
							dcc.Graph(
								id='the_graph_2', 
								style={
									'width': '50%', 
									'height': '80%', 
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
							children="Number of applications:", 
							style = {
								'font_family': 'times',
								'font_size': '22px',
								'textAlign': 'center',
								'color': '#d7d8da',
								'margin-bottom': '60px',
								"display": "block"
							}),
						html.Label(
							id='label_tot_num_after_val', 
							style = {
								'font_family': 'times',
								'font_size': '22px',
								'textAlign': 'center',
								'color': '#d7d8da',
								'margin-bottom': '60px',
								"display": "block"
							}),
						html.Label(
							id='label_categ_num_after',
							children="Number of learning categories:", 
							style = {
								'font_family': 'times',
								'font_size': '22px',
								'textAlign': 'center',
								'color': '#d7d8da',
								'margin-bottom': '90px',
								"display": "block"
							}),
						html.Label(
							id='label_categ_num_after_val', 
							style = {
								'font_family': 'times',
								'font_size': '22px',
								'textAlign': 'center',
								'color': '#d7d8da',
								'margin-bottom': '60px',
								"display": "block"
							}),
						html.H2('BEFORE FILTERING', className = 'fix_label', style = HIGHLIGHT_STYLE),	
						html.Label(
							id='label_tot_num_before',
							children="Number of applications:", 
							style = {
								'font_family': 'times',
								'font_size': '22px',
								'textAlign': 'center',
								'color': '#d7d8da',
								'margin-bottom': '60px',
								"display": "block"
							}),		
						html.Label(
							id='label_categ_num_before',
							children="Number of learning categories:", 
							style = {
								'font_family': 'times',
								'font_size': '22px',
								'textAlign': 'center',
								'color': '#d7d8da',
								'margin-bottom': '60px',
								"display": "block"
							}),
						],
						style={'top': '0'},
						)
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




#---------------------------------------------------------------
@app.callback(
    Output(component_id='the_graph', component_property='figure'),
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
		title = "Results before filtering",
		)
	
	piechart.update_traces(textposition ='inside')
	piechart.update_layout(
		autosize = True, #width = 250, height = 300,
		margin=dict(t=40, b=10, l=60, r=60),
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
    
	# else:
	# 	barchart = px.histogram(df, x='installs', 
	# 						title='After Filtering', height=450,
	# 						color_discrete_sequence=['#03DAC5'],
	# 						nbins=20,
	# 						)
	# 	barchart.update_yaxes(showgrid=False),
	# 	#barchart.update_xaxes(categoryorder='total descending')
	# 	barchart.update_traces(hovertemplate=None)
	# 	barchart.update_layout(margin=dict(t=40, b=10, l=60, r=60),
	# 							hovermode="x unified",
	# 							xaxis_tickangle=360,
	# 							xaxis_title=' Number of installations', yaxis_title=" Count ",
	# 							plot_bgcolor='#2d3035', paper_bgcolor='#2d3035',
	# 							title_font=dict(size=20, color='#d7d8da', family="times"),
	# 							font=dict(color='#8a8d93', size = 12, family='times'),
	# 							legend=dict(orientation="h", yanchor="bottom", y=0, xanchor="right", x=0),
	# 							bargap=0.2,
	# 							title_x=0.5,
	# 							)
	# 	barchart.update_layout(showlegend=False)
	# 	barchart.update_xaxes(showticklabels=False)  
	# 	barchart.update_yaxes(showticklabels=False)
	# 	return barchart


@app.callback(
	Output(component_id='the_graph_2', component_property='figure'),
    [Input(component_id='radio_items', component_property='value')]
)

def update_graph(radio_items):
    
	dff = df
	if radio_items=='genre':
		colors = color_discrete_sequence=px.colors.qualitative.Pastel1
	if radio_items=='score':
		colors = color_discrete_sequence=px.colors.qualitative.Pastel
	if radio_items=='installs':
		colors = color_discrete_sequence=px.colors.qualitative.Pastel2


	piechart = px.pie(
		data_frame=dff,
		names=radio_items,
		hole=.4,
		color_discrete_sequence=colors,
		title = "Results before filtering",
		)
	
	piechart.update_traces(textposition ='inside')
	piechart.update_layout(
		autosize = True, #width = 250, height = 300,
		margin=dict(t=40, b=10, l=60, r=60),
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

		# barchart = px.histogram(df, x='installs',
		# 					title='Before Filtering', height=450,
		# 					color_discrete_sequence=px.colors.cyclical.Phase,
		# 					nbins=20,
		# 					)
		# barchart.update_yaxes(showgrid=False),
		# #barchart.update_xaxes(categoryorder='total descending')
		# barchart.update_traces(hovertemplate=None)
		# barchart.update_layout(margin=dict(t=40, b=10, l=60, r=60),
		# 						autosize = True,
		# 						xaxis_tickangle=360,
		# 						hovermode="x unified",
		# 						xaxis_title=' Number of installations', yaxis_title=" Count ",
		# 						plot_bgcolor='#2d3035', paper_bgcolor='#2d3035',
		# 						title_font=dict(size=20, color='#d7d8da', family="times"),
		# 						font=dict(color='#8a8d93', size = 12, family='times'),
		# 						legend=dict(orientation="h", yanchor="bottom", y=0, xanchor="right", x=0),
		# 						bargap=0.2,
		# 						title_x=0.5,
		# 						)
		# barchart.update_layout(showlegend=False)
		# barchart.update_xaxes(showticklabels=False)  
		# barchart.update_yaxes(showticklabels=False)

		# return barchart




############################### App ########################################
 
app.layout = html.Div([HEADER, TABS, 
					content_page_1, 
	
					], 
					style={'margin-left': "30px", 'margin-right': "30px"})

if __name__ == '__main__':
    app.run_server()