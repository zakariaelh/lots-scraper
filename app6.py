import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import scraper as sc
from termcolor import colored
import itertools
import numpy as np
# import dash_table_experiments as dt
import os
from urllib.parse import quote as urlquote
from flask import Flask, send_from_directory


a = pd.read_csv('lots.csv', index_col = 0)
b = pd.read_csv('houses.csv', index_col = 0)
d_zip = pd.read_csv('zipcodes', index_col = 0)

#columns lots
cols_l = ['address', 'area', 'lat', 'lng', 'neigh', 'price', 'url']
#columns houses
cols_h = ['address', 'area', 'baths', 'beds', 'lat', 'lng', 
			'neigh', 'price', 'price_sqft','url']
#column fitlered lots
cols_f = ['address', 'area', 'lat', 'lng', 'neigh', 'price', 
		'avg_price', 'margin', 'url', 'houses_links']

#directory from which we will look up the files to download and also to which we save 
DOWNLOAD_DIRECTORY = os.getcwd() + "/downloaded_data/"


#create a server 
server = Flask(__name__)


def connect(headless):
	print(colored('connect .. ', 'yellow'))
	driver = sc.connect(headless)
	print(colored('connected', 'green'))
	return driver

def close(driver):
	print(colored('closing connection', 'red'))
	driver.quit()
	print(colored('connection closed', 'red'))

def create_html(name, link):
	return html.A(name, href = link, target = '_blank')

def generate_table(df_j, type_):
    df_ = pd.read_json(df_j)
    #print(df_)
    if type_ == 'house':
    	return(
        # Header
        [ #[html.Thead(html.Tr([html.Th(html.Button(col, id = col)) for col in df_.columns])), 
        #rows
        html.Tbody([html.Tr(
            [html.Td(df_.iloc[i][col]) 
            for col in cols_h if col != 'url'] + 
            [html.Td(create_html('check listing', df_.iloc[i]['url']))]
                            ) 
        for i in range(len(df_))])]
        )
    elif type_ == 'lot':
    	return(
        # Header
        [ #[html.Thead(html.Tr([html.Th(html.Button(col, id = col)) for col in df_.columns])), 
        #rows
        html.Tbody([html.Tr(
            [html.Td(df_.iloc[i][col]) 
            for col in cols_l if col != 'url'] + 
            [html.Td(create_html('check listing', df_.iloc[i]['url']))]
                            ) 
        for i in range(len(df_))])]
        )
    elif type_ == 'filtered_lot':
    	return(
        # Header
        [ #[html.Thead(html.Tr([html.Th(html.Button(col, id = col)) for col in df_.columns])), 
        #rows
        html.Tbody([html.Tr(
            [html.Td(df_.iloc[i][col]) 
            for col in cols_f if col not in ['url', 'houses_links']] + 
            [html.Td(create_html('check listing', df_.iloc[i]['url']))] +
            [html.Td([create_html(j, df_.iloc[i]['houses_links'][j]) for j in range(len(df_.iloc[i]['houses_links']))])]
                            ) 
        for i in range(len(df_))])]
        )


def save(k, data):
    if k is not None:
        if data is not None:
            data = pd.read_csv('lots.csv')
            data.to_csv('downloaded_data/lots' + str(k) + '.csv')


def uploaded_files():
    """List the files in the upload directory."""
    files = []
    for filename in os.listdir(DOWNLOAD_DIRECTORY):
        path = os.path.join(DOWNLOAD_DIRECTORY, filename)
        if os.path.isfile(path):
            files.append(filename)
    return files


def file_download_link(filename):
    """Create a Plotly Dash 'A' element that downloads a file from the app."""
    location = "/download/{}".format(urlquote(filename))
    return html.A(filename, href=location)

@server.route("/download/<path:path>")
def download(path):
    """Serve a file from the upload directory."""
    return send_from_directory(DOWNLOAD_DIRECTORY, path, as_attachment=True)


#add style
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css', 
			'https://www.w3schools.com/w3css/4/w3.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets, server = server)

# Loading screen CSS
app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/brPBPO.css"})

#allow two componetns with same id 
app.config.supress_callback_exceptions = True


#layout of the app (Divs, buttons .. etc)
app.layout = html.Div([
	#debug mode 
	dcc.Checklist(
	id = 'debug',
    options=[
        {'label': 'debug', 'value': True}],values=[]),
	#H2
	html.H2('Please select a list of zipcodes'),
	#establish connection
	#input zipcodes (all us zipcodes, can select multi )
	dcc.Dropdown(id = 'zip-input',
				 options = [{'label': str(i).zfill(5), 'value': str(i).zfill(5)} for i in set(d_zip.zip)],
				 multi= True,
				 value = '24555'),
	#button to trigger connection and scraping 
	#html.Button('Scrape-houses', id='scrape-button-h', className = 'button-primary'),
	#div where we output data-houses scraped
	html.Div(id = 'data-houses', style={'display': 'none'}),
	#html.Button('Scrape-lots', id='scrape-button-l', className = 'button-primary'),
	html.Button('Scrape', id='scrape-button', className = 'button-primary'),
	#div wher ewe output data-lots scraped
	html.Div(id = 'data-lots', style={'display': 'none'}),
	html.H3('Lots'),
	#html.Table(id = 'table_lots'),
	html.Div(
		[html.Thead(html.Tr([html.Th(html.Button(col, id = col + '_')) for col in cols_l]), 
			className = 'scrolltable_l',
			id = 'thead_cols_l',
			),
        html.Table(id = 'table_lots', className = 'scrolltable_l')],
        style = {'overflow-x' : 'auto'}
        ),
	html.H3('Houses'),
	#html.Table(id = 'table_houses'),
	html.Div(
        [html.Thead(html.Tr([html.Th(html.Button(col, id = col)) for col in cols_h]), 
        	className = 'scrolltable_h',
		id = 'thead_cols_h',
        	),
        html.Table(id = 'table_houses', className = 'scrolltable_h')],
        style = {'overflow-x' : 'auto'}
        ),
	html.H3('Filtered Lots'),
	html.Div([
			html.Div([html.Div([html.Form([
				html.H3('Minimum Margin (%)'),
				dcc.Input(id = 'min_margin', placeholder = 'Minimum Margin', value = 10, 
					style = {'width': '100%', 'height': '50px'})],
					style = {'padding': '40px'},
					className = 'w3-container w3-card-4 w3-light-grey')
					],
					style = {'width' : '400px', 'padding' : '20px', 'float': 'left'}),
			html.Div([html.Form([
				html.H3('Cost of Construction (per sqft)'),
				dcc.Input(id = 'cost', placeholder = 'Construction Cost', value = 10, 
					style = {'width': '100%', 'height': '50px'})],
					style = {'padding': '40px'},
					className = 'w3-container w3-card-4 w3-light-grey')
					],
				style = {'width' : '400px', 'padding' : '20px', 'float': 'left'}),
			html.Div([html.Form([
				html.H3('Radius (miles)'),
				dcc.Input(id = 'radius', placeholder = 'Radius', value = 10, 
					style = {'width': '100%', 'height': '50px'})],
					style = {'padding': '40px'},
					className = 'w3-container w3-card-4 w3-light-grey')
					],
				style = {'width' : '400px', 'padding' : '20px', 'float': 'left'}),
			html.Div([html.Form([
				html.H3('Maximum Lot Size (sqft)'),
				dcc.Input(id = 'max_size', placeholder = 'Max Lot Size', value = None, 
					style = {'width': '100%', 'height': '50px'})],
					style = {'padding': '40px'},
					className = 'w3-container w3-card-4 w3-light-grey')
					],
				style = {'width' : '400px', 'padding' : '20px', 'float': 'left'}),
			html.Div([html.Form([
				html.H3('Ratio of Livable Area (%)'),
				dcc.Input(id = 'ratio', placeholder = 'Ratio of Livable area (%)', value = 70, 
					style = {'width': '100%', 'height': '50px'})],
					style = {'padding': '40px'},
					className = 'w3-container w3-card-4 w3-light-grey')
					],
				style = {'width' : '400px', 'padding' : '20px', 'float': 'left'}),
			html.Div([html.Button('Filter', id = 'filter-button', className = 'button-primary')],
				style = {'width' : '100px', 'padding' : '30px', 'height' : '50px', 'clear': 'both'})
			],
			style = {'width' : '100%', 'padding' : '20px'}),
			]),
	html.Div(
    [html.Thead(html.Tr([html.Th(html.Button(col, id = col + '__')) for col in cols_f]), 
    	className = 'scrolltable_f',
		id = 'thead_cols_f',
    	),
    html.Table(id = 'table_filtered', className = 'scrolltable_f')],
    style = {'overflow-x' : 'auto'}
    ),
    html.Div(
    [
        html.H2("Download Links "),
        html.Button('show', id = 'show'),
        html.Ul(id="file-list"),
    ])
	], style = {'padding' : '30px'})

@app.callback(
    dash.dependencies.Output('thead_cols_h', 'style'),
    [dash.dependencies.Input('scrape-button', 'n_clicks')])

def show_head_h(k):
	'''
	if there was no click, don't show the columns headers in the app
	'''
	if k is None:
		return {'display' : 'none'}


@app.callback(
    dash.dependencies.Output('thead_cols_l', 'style'),
    [dash.dependencies.Input('scrape-button', 'n_clicks')])

def show_head_l(k):
	'''
	if there was no click, don't show the columns headers in the app
	'''
	if k is None:
		return {'display' : 'none'}


@app.callback(
    dash.dependencies.Output('thead_cols_f', 'style'),
    [dash.dependencies.Input('filter-button', 'n_clicks')])

def show_head_f(k):
    if k is None:
        return {'display' : 'none'}


@app.callback(
	dash.dependencies.Output('data-lots', 'children'),
	[dash.dependencies.Input('scrape-button', 'n_clicks')],
	[dash.dependencies.State('debug', 'values'),
	dash.dependencies.State('zip-input', 'value')])

def get_data_lots(b, debug, zips):
	'''
	click on scrape lots button, 
	and this will connect a selenium driver that will scrape the zipcodes input
	'''
	if zips is None:
		pass
	else:
		if b is not None:
			print('zipcodes: ', zips)
			# d_lots = pd.read_csv('lots.csv', index_col = 0)
			if len(debug) > 0: #debug mode
				driver = connect(headless = False)
			else:
				driver = connect(headless = True)
			d_lots, l_e = sc.get_lots(driver, zips)
			print('cleaning lots')
			d_lots = sc.clean_lots(d_lots)
			# # close connection
			close(driver)
			d_lots.to_csv(DOWNLOAD_DIRECTORY + 'd_lots.csv', index = False)
			return d_lots.to_json()
			

@app.callback(
    dash.dependencies.Output('table_lots', 'children'),
    [dash.dependencies.Input('data-lots', 'children')] + 
    list(itertools.chain.from_iterable([
        [dash.dependencies.Input(col + '_', 'n_clicks_timestamp'),
    	dash.dependencies.Input(col + '_', 'n_clicks')] for col in cols_l])))

def show_data_lots(data_lots, 
        k_a_t, k_a,
        k_ar_t, k_ar,
        k_l_t, k_l, 
        k_ln_t, k_ln,
        k_n_t, k_n,
        k_p_t, k_p,
        k_u_t, k_u
        ):
	'''
	This takes the output of the scraper and format the data into a nice looking table 
	'''
	if data_lots is not None:
		try:
		    l_k = [k_a, k_ar, k_l, k_ln, k_n, k_p, k_u] #n_clicks
		    l_k_t = [k_a_t, k_ar_t, k_l_t, k_ln_t, k_n_t, k_p_t, k_u_t] #timestamps
		    print('l_k ', l_k)
		    print('l_k_t', l_k_t)
		    df = pd.read_json(data_lots)
		    if all(v is None for v in l_k_t):
		        return generate_table(df.to_json(), type_ = 'lot')
		    else:
		        #determine which was last clicked
		        i = np.nanargmax(np.array(l_k_t, dtype=np.float))
		        print('last click: ', cols_l[i])
		        #get value of n_clicks of columns with the latest timestamp
		        if l_k[i] % 2 == 1: #even means clicked once hence decreasing
		            return generate_table(df.sort_values(cols_l[i], ascending = False).reset_index().to_json(),
		            						type_ = 'lot')
		        elif l_k[i] % 2 == 0:
		            return generate_table(df.sort_values(cols_l[i], ascending = True).reset_index().to_json(),
		            						type_ = 'lot')
		except Exception as e:
			print(colored('Error in outputting lots', 'red'), e)

@app.callback(
	dash.dependencies.Output('data-houses', 'children'),
	[dash.dependencies.Input('scrape-button', 'n_clicks')],
	[dash.dependencies.State('debug', 'values'),
	dash.dependencies.State('zip-input', 'value')])

def get_data_houses(b, debug, zips):
	'''
	Analogously for houses (see get_data_lots)
	'''
	if zips is None:
		pass
	else:
		if b is not None:
			print('zipcodes: ', zips)
			# d_houses = pd.read_csv('houses.csv', index_col = 0)
			#estibalish connection
			if len(debug) > 0: #debug mode
				driver = connect(headless = False)
			else:
				driver = connect(headless = True)
			d_houses, l_e = sc.get_houses(driver, zips)
			d_houses = sc.clean_houses(d_houses)
			# # #close connection
			close(driver)
			d_houses.to_csv(DOWNLOAD_DIRECTORY + 'd_houses.csv', index = False)
			return d_houses.to_json()



@app.callback(
    dash.dependencies.Output('table_houses', 'children'),
    [dash.dependencies.Input('data-houses', 'children')] + 
    list(itertools.chain.from_iterable([
        [dash.dependencies.Input(col, 'n_clicks_timestamp'),
    	dash.dependencies.Input(col, 'n_clicks')] for col in cols_h])),

    )

def show_data_houses(data_houses, 
        k_a_t, k_a,
        k_ar_t, k_ar,
        k_b_t, k_b,
        k_bd_t, k_bd,
        k_l_t, k_l, 
        k_ln_t, k_ln,
        k_n_t, k_n,
        k_p_t, k_p,
        k_u_t, k_u,
        k_pr_t, k_pr
        ):
	'''
	similarly for houses (see show_data_lots)
	'''
	if data_houses is not None:
		try:
		    l_k = [k_a, k_ar, k_b, k_bd, k_l, k_ln, k_n, k_p, k_u, k_pr] #n_clicks
		    l_k_t = [k_a_t, k_ar_t, k_b_t, k_bd_t, k_l_t, k_ln_t, k_n_t, k_p_t, k_u_t, k_pr_t] #timestamps
		    print('l_k ', l_k)
		    print('l_k_t', l_k_t)
		    df = pd.read_json(data_houses)
		    if all(v is None for v in l_k_t):
		        return generate_table(df.to_json(),type_ = 'house')
		    else:
		        #determine which was last clicked
		        i = np.nanargmax(np.array(l_k_t, dtype=np.float))
		        print('last click: ', cols_h[i])
		        #get value of n_clicks of columns with the latest timestamp
		        if l_k[i] % 2 == 1: #even means clicked once hence decreasing
		            return generate_table(df.sort_values(cols_h[i], ascending = False).reset_index().to_json(),
		            						type_ = 'house')
		        elif l_k[i] % 2 == 0:
		            return generate_table(df.sort_values(cols_h[i], ascending = True).reset_index().to_json(), 
		            						type_ = 'house')
		except Exception as e:
			print(colored('Error in outputting houses', 'red'), e)



@app.callback(
	dash.dependencies.Output('table_filtered', 'children'),
	[dash.dependencies.Input('data-houses', 'children'),
	dash.dependencies.Input('data-lots', 'children'),
	dash.dependencies.Input('filter-button', 'n_clicks')] + 
    list(itertools.chain.from_iterable([
        [dash.dependencies.Input(col + '__', 'n_clicks_timestamp'),
    	dash.dependencies.Input(col + '__', 'n_clicks')] for col in cols_f])),
	[dash.dependencies.State('radius', 'value'),
	dash.dependencies.State('min_margin', 'value'),
	dash.dependencies.State('cost', 'value'),
	dash.dependencies.State('max_size', 'value'),
	dash.dependencies.State('ratio', 'value')])

def filter_data(d_houses, d_lots, b, 
	        k_a_t, k_a,
	        k_ar_t, k_ar,
	        k_l_t, k_l, 
	        k_ln_t, k_ln,
	        k_n_t, k_n,
	        k_p_t, k_p,
	        k_av_t, k_av,
	        k_m_t, k_m,
	        k_u_t, k_u,
	        k_c_t, k_c,
	        radius, min_margin, cost, max_size, ratio):
	'''
	This function takes as input the filter requirements and apply them to the lots table 
	'''

	if b is not None:
		print('radius', radius)
		print('min_margin', min_margin)
		print('cost: ', cost)
		print('max_size', max_size)
		
		#inputs
		d_houses = pd.read_json(d_houses)
		d_lots = pd.read_json(d_lots)
		
		#first filtering 
		if (max_size is not None) & (max_size != ''):
			max_size = float(max_size)
			d_lots = d_lots[d_lots.area <= max_size]
		
		if (radius is not None) & (radius != ''):
			#get average price and distances 
			l_h = sc.get_distance(d_lots, d_houses)
			radius = float(radius)
			l_avg = list(map(lambda x: sc.get_avg(x, l_h, radius, d_houses), range(d_lots.shape[0])))
			l_links = list(map(lambda x: sc.get_comp_links(x, l_h, radius, d_houses), range(d_lots.shape[0])))
			# l_n = [[create_html(j, u[j]) for j in range(len(u))] for u in l_links]
			print('links of comparable houses: ')
			print(l_links)
			print('length of comp houses')
			# print(l_n)
			d_lots['avg_price'] = l_avg
			d_lots['houses_links'] = l_links

		
		if (cost is not None) & (cost != ''):
			cost = float(cost)
			ratio = float(ratio)
			d_lots['margin'] = (d_lots.avg_price / (
				(d_lots.price + cost * d_lots.area * (ratio/100)) / 
				(d_lots.area * (ratio/100))) - 1)*100
	
		#filter 
		if (min_margin is not None) & (min_margin != ''):
			min_margin = float(min_margin)
			d_lots = d_lots[d_lots.margin >= min_margin]

		#save the filtered data
		d_lots.to_csv(DOWNLOAD_DIRECTORY + 'd_lots_filtered.csv', index = False)
		
		try:
		    l_k = [k_a, k_ar, k_l, k_ln, k_n, k_p, k_av, k_m, k_u, k_c] #n_clicks
		    l_k_t = [k_a_t, k_ar_t, k_l_t, k_ln_t, k_n_t, k_p_t, k_av_t, k_m_t, k_u_t, k_c_t] #timestamps
		    print('l_k ', l_k)
		    print('l_k_t', l_k_t)
		    if all(v is None for v in l_k_t):
		    	# print(d_lots)
		    	return generate_table(d_lots.to_json(), type_ = 'filtered_lot')
		    else:
		        #determine which was last clicked
		        i = np.nanargmax(np.array(l_k_t, dtype=np.float))
		        # print('last click: ', cols_f[i])
		        #get value of n_clicks of columns with the latest timestamp
		        if l_k[i] % 2 == 1: #even means clicked once hence decreasing
		            return generate_table(d_lots.sort_values(cols_f[i], ascending = False).reset_index().to_json(),
		            						type_ = 'filtered_lot')
		        elif l_k[i] % 2 == 0:
		            return generate_table(d_lots.sort_values(cols_f[i], ascending = True).reset_index().to_json(),
		            						type_ = 'filtered_lot')
		except Exception as e:
			print(colored('Error in outputting filtered lots', 'red'), e)
			#now return filtern lots
			return generate_table(d_lots.to_json(), type_ = 'filtered_lot')


@app.callback(
    dash.dependencies.Output("file-list", "children"),
    [dash.dependencies.Input("show", "n_clicks")]
)

def update_output(k):
    """Save uploaded files and regenerate the file list."""
    if k is not None:
        files = uploaded_files()
        if len(files) == 0:
            return [html.Li("No files yet!")]
        else:
            return [html.Li(file_download_link(filename)) for filename in files]




if __name__ == '__main__':
    app.run_server(debug = True)
