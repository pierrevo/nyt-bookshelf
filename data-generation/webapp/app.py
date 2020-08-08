import json
from multiprocessing import process

import six.moves.urllib.request as urlreq
from six import PY3

import dash
import os
import dash_bio as dashbio
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
import dash_table as dt
import dash_bootstrap_components as dbc
import csv
import ast
import flask


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']  #[dbc.themes.LUX]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
server.secret_key = os.environ.get('secret_key', 'secret')

    #circosgraph

data = urlreq.urlopen(
    'https://raw.githubusercontent.com/plotly/dash-bio-docs-files/master/' +
    'circos_graph_data.json'
).read()

#server = flask.Flask(__name__)
server = app.server
server.secret_key = os.environ.get('SECRET_KEY', 'secret')


if PY3:
    data = data.decode('utf-8')

circos_graph_data = json.loads(data)

    #blocks
with open(os.path.join(os.path.dirname(__file__), 'blocks.txt'),'r') as fi:
    stringtheory = fi.read()

heatj = json.dumps(stringtheory)
jdata1 = json.loads(heatj)
j2 = ast.literal_eval(jdata1)
blocks = 115169878

    #bands/books
with open(os.path.join(os.path.dirname(__file__), 'cytobands.txt'),'r') as f1:
    bluestr = f1.read()

bluej = json.dumps(bluestr)
onej = json.loads(bluej)
j3 = ast.literal_eval(onej)


jdata={}
json_object = ast.literal_eval(json.loads(bluej))
current_shelf = "chr1"
with open(os.path.join(os.path.dirname(__file__), 'goodreads-ids.csv'),'r') as j:
    csvReader = csv.DictReader(j)
    book_thickness = 26604#26604
    shelf_spot = 0
    shelf_size= 0
    extra_data = False
    for access in json_object['cytobands']:
        for row in csvReader:
            if ":" in str(row['book_title']):
                str1 = row["book_title"].split(':')
                access["name"] = str1[0]
                access["subtitle"] = str1[1]
            else:
                access["name"] = row["book_title"]
            access["Genre"] = row["genre"]
            access["Author"] = row["author_name"]
            access["year"] = row["year"]
            access["block_id"] = row["block"]
            access["pages"] = int(row["num_pages"])
            access["rating"] = row["ratings"]
            access["image_url"] = row["image_url"]
            access['ratings_count'] = row['ratings_count']

            if row["block"] == current_shelf:
                try:
                    access["start"] = end
                except:
                    access["start"] = shelf_spot * book_thickness * access["pages"]
                shelf_size += book_thickness*access['pages']
                access["end"] = access["start"] + (book_thickness * access["pages"])
                end = access["end"]
                shelf_spot += 1
                # if shelf_size >= blocks:
                #     for i in j2['GRCh37']:
                #         i['len'] = shelf_size

            else:
                access["start"] = 0
                access["end"] = access["start"] + book_thickness * access["pages"]
                end = access["end"]
                shelf_spot =1
                current_shelf = row["block"]
            break


with open('tempout.json', 'w') as jsonFile:
    jsonFile.write(json.dumps(json_object,indent=4))
with open('tempout.json', 'r') as jin:
    j4 = json.loads(jin.read())

#order books by rating
with open('tempout.json','r') as js:
    incoming = json.loads(js.read())
    j5 = sorted(incoming['cytobands'],key=lambda i: float(i.get('rating', 0)),reverse=True)


with open(os.path.join(os.path.dirname(__file__), 'blocks2.txt'),'r') as f2:
    str2 = f2.read()

d_2 = json.dumps(str2)
j_2 = json.loads(d_2)
j1 = ast.literal_eval(j_2)



# test data - to be inputed on line 58, 46


# with open("test1.json","w") as out_file:
#     with open("/Users/philippevo/Desktop/circos-0.69-9/example/data/heatmap.hs.mm.5e6.txt", "r") as fin:
#         for line in fin:
#             description = list(line.strip().split(None, 4))
#             jdata = json.loads(line)
#             #json.dump(description, out_file, indent=1)


app.layout = html.Div(
        html.Div([
        html.Div([
        html.H6(
            html.Div([
                '   ','236 best books selected by the New York Times from ', html.Span('1996',style={'background-color':'#5e5e5e'}),

                    ' to ', html.Span('2019',style={'background-color':'#996600'})])



        )],
            className="twelve columns",
            style={'padding': '15px',
                   'font-family': 'Times New Roman',
                    'background-color':'#2d3245',
                   'height':'14%',
                   'color':'#e1e4ed'}),
            html.Div([
            html.Div([

    dashbio.Circos(
        id='my-dashbio-circos',
        layout=j2['GRCh37'],
        style={'fontWeight':100},
        selectEvent={"0": "hover", "1": "click", "2": "both"},
        config={
            'innerRadius': 650 / 2 - 80,
            'outerRadius': 650 / 2 - 40,
            'ticks': {'display': False, 'labelDenominator': 1000000},
            'labels': {
                'position': 'center',
                'display': True,
                'size': 11,
                'color': '#fff',
                'radialOffset': 75,
                },
        },
        tracks=[
            {
                'type': 'HIGHLIGHT',
                'data': j4['cytobands'],
                'config': {
                    'innerRadius': 650 / 2 - 80,
                    'outerRadius': 650 / 2 - 40,
                    'opacity': 0.3,
                    'tooltipContent': {
                        "name": "name"
                    },
                    'color': {'name': 'color'},
                },

            }
        ],
            ),
                ],className='ten columns'),


html.Div(id='circos-body', className='app-body', children=[
    html.Div(id='circos-control-tabs', className='control-tabs', children=[
                dbc.Card(children=[

                    html.Div(
                            id='title-output',
                            className='control-tab',
                            style={'color':'white',
                                   'lightLogo': True,
                                    'marginTop': '5px',
                                    'textAlign':'center',
                                    'marginleft': '5px'
                                   }),


                    html.Div(
                            id='author-output',
                            className='control-tab',
                            style={'color':'white',
                                   'lightLogo': True,
                                    'textAlign':'center',
                                   'fontSize':'11pt',
                                    'marginTop': '5px',
                                    'marginleft': '5px'
                                   }),

                    html.Br(),

                    html.Div(
                        id='circos-img',
                        className='two columns',
                        style={
                            'width':'60%',
                            'height':'auto',
                            'objectFit':'cover',
                            'textAlign':'center',
                               }),
                    html.Br(),



                        html.Div(
                            id='genre-output',
                            className='control-tab',
                            style={'color':'white',
                                   'lightLogo': True,
                                   'marginTop':'180px',
                                    'textAlign':'center',
                                   'fontSize':'11pt'
                                   }),

                ],

                        style={'position':'absolute',
                            'backgroundColor':'#262B3D',
                            "max-Width": "100px",
                            'width': '25%',
                            'max-Height':'30px',
                            'height':'55%',
                            'marginTop': '20px',
                            'marginLeft': '800px',
                            'padding':'5px',
                            'font_color': 'white',
                             'float':'none'
             })

    ])

])


        ],className='twelve columns',
            style={'position':'relative'}),

html.Div([
    dbc.Modal(
        [
            dbc.ModalHeader("Book Info"),
            dbc.ModalBody("This is the content of the modal"),
            dbc.ModalFooter(
                dbc.Button("Close", id="close", className="ml-auto")
            ),
        ],
        id="modal",
        className='modal',
        is_open=False,
        zIndex =1002,
        style={'display':'block',
               'position':'fixed',
               'height':'100%',
               'width':'100%',
               'textAlign':'center'}
    ),
]),

dcc.Dropdown(
    id='year/genre',
    style={'display':'none'},
    options=[
        {'label': x, 'value': x}
        for x in ['Organized by year','Organized by genre']],
    value='Organized by year',
    className='five columns'),

html.Br(),

html.Div([
    'Source: ', html.Span('New York Times API, Goodreads API', style={'color': '#a6a8ad'}),
    html.P(),
    'Created by',
    html.Span(' Pierre Vo ', style={'color': '#a6a8ad'}),
    html.P(),
    'Powered by ', html.Span('Python, Dash',style={'color': '#a6a8ad'})

],className='twelve columns',style={'position':'absolute',
         'background-color':'#2d3245',
        'color':'#e1e4ed',
         'padding':'30px',
        'height':'150px',
         'bottom':0})


]

        ),style={'background-color': '#1F2132',
                 'height':1500,
                 'position':'relative',
                 'margin':0,
                 'marginLeft':0,
                 'marginTop':0}

)

@app.callback(
    dash.dependencies.Output('title-output', 'children'),
    [dash.dependencies.Input('my-dashbio-circos', 'eventDatum')]
)
def update_output(value):
    if value is not None:
        for v in value.keys() & {'name'}:
            for i in value.keys() & {'Author'}:
                name = html.Div('{}'.format(value[v]), style={'fontFamily': 'titleFont','fontSize':'18px'})
                auth = html.Div('by {}'.format(value[i]), style={'color': '#ababab', 'font': 8})
                try:
                    for s in value.keys() and {'subtitle'}:
                        sub = html.Div('{}'.format(value[s]),style={'fontSize':'12px'})
                    if sub is not None:
                        return name,sub, auth
                except:
                        return name, auth

@app.callback(
    dash.dependencies.Output('genre-output', 'children'),
    [dash.dependencies.Input('my-dashbio-circos', 'eventDatum')]
)
def update_output(value):
    if value is not None:
        for n in value.keys() and {'Genre'}:
            for r in value.keys() and {'rating'}:
                for a in value.keys() and {'ratings_count'}:
                    gen = html.Div('{}'.format(value[n]),
                                   style={'color': '#919191', 'font': 8})

                    rate = html.Div([html.Div('Rated ',style={'color': '#ababab', 'font': 7}),html.Div('{}'.format(value[r]),style={'color':'#e8e8e8','font':7}), html.Div('by {} Goodreads users'.format(value[a]),
                                   style={'color': '#ababab', 'font': 7})])

                    return gen, rate

@app.callback(
    dash.dependencies.Output('circos-img', 'children'),
    [dash.dependencies.Input('my-dashbio-circos', 'eventDatum')]
)
def update_img(value):
    if value is not None:
        return [html.Img(src=value[v],style={
            'height':'auto',
            'max-width':'100px',
            'marginTop':'28px',
            'position':'absolute'})
            for v in value.keys() & {'image_url'}]



@app.callback(
    dash.dependencies.Output('my-dashbio-circos', 'tracks'),
    [dash.dependencies.Input('year/genre', 'value')],
    state=[dash.dependencies.State('my-dashbio-circos', 'tracks')]
)

def change_graph_type(value, current):

    if value == 'HIGHLIGHT:':
        current[0].update(
            data=j4['cytobands'],
            type='HIGHLIGHT'
        )
    if value == 'Rating':

        current[0].update(
            data=j5,
            type='Rating',
        )

    elif value == 'chords':
        current[0].update(
            data=circos_graph_data['chords'],
            type='CHORDS',
            config={
                'tooltipContent': {
                    'source': 'source',
                    'sourceID': 'id',
                    'target': 'target',
                    'targetID': 'id',
                    'targetEnd': 'end'
                }
            }
        )
    return current


if __name__ == '__main__':
    app.run_server(port=int(os.environ.get("PORT", 14094)),debug=True)

# host='127.0.0.1'??
app.css.config.serve_locally = True
app.scripts.config.serve_locally = True

