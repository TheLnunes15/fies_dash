# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd

tab1 = pd.read_csv("dados/letra_a.csv", encoding='unicode_escape')
tab2 = pd.read_csv("dados/letra_b.csv", encoding='unicode_escape')
tab3 = pd.read_csv("dados/letra_c.csv", encoding='unicode_escape')

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title = 'FIES'

app.layout = html.Div([
    html.Div([
        html.Br(), html.Br(),
        html.H1('FIES Nordeste Dashboard')],
        style={'textAlign': 'center', 'color': '#808000', 'border': '2em'

               }),

    html.Div([
        html.Label('Selecione o estado:'),
        dcc.Dropdown(id='w_estado',
                     multi=False,
                     clearable=True,
                     value=' ',
                     placeholder='Estados do Nordeste',
                     options=[{'label': c, 'value': c}
                              for c in (tab1['est'].unique())])

    ], style={'width': '10%', 'margin-left': '45%'}),

    # Create combination of bar chart
    html.Div([
        html.Br(),
        dcc.Graph(id='bar_line_1',
                  config={'displayModeBar': False}),

    ], style={'margin-left': '1.4%', 'width': '50%', 'display': 'inline-block'}),

    # Create combination of bar chart and line chart
    html.Div([
        html.Br(),
        dcc.Graph(id='bar_line_4',
                  config={'displayModeBar': False}),

    ],style={'width': '48.6%', 'display': 'inline-block', 'float': 'right'}),

    # Create horizontal bar chart 1
    html.Div([
        html.Br(),
        dcc.Graph(id='top_10_1',
                  config={'displayModeBar': 'hover'}),

    ], style={'margin-left': '1.4%', 'width': '50%', 'display': 'inline-block'}),

    # Create horizontal bar chart 2
    html.Div([
        html.Br(),
        dcc.Graph(id='top_10_2',
                  config={'displayModeBar': 'hover'}),

    ], style={'width': '48.6%', 'display': 'inline-block', 'float': 'right'}),

], style={'background-color': '#ffffff'})


# Create combination of bar chart
#4) Identificar os valores de mensalidades dos financiamentos concedidos em ordem decrescente para a região Nordeste no mês de setembro de 2019. Além da mensalidade, devem ser apresentados os respectivos cursos, instituição de ensino superior, Estado, município.
@app.callback(Output('bar_line_1', 'figure'),
              [Input('w_estado', 'value')])
def update_graph(w_estado):
    # Data for bar
    fig1 = tab1.groupby(['curso', 'est'])['val'].sum().reset_index()

    return {
        'data': [go.Bar(x=fig1[fig1['est'] == w_estado]['curso'],
                        y=fig1[fig1['est'] == w_estado]['val'],
                        text=fig1[fig1['est'] == w_estado]['val'],
                        name='Quantidade',
                        texttemplate='%{text:.2s}',
                        textposition='auto',
                        marker=dict(
                            color=fig1[fig1['est'] == w_estado]['val'],
                            colorscale='phase',
                            showscale=False),
                        yaxis='y1',

                        hoverinfo='text',
                        hovertext=
                        '<b>Estado</b>: ' + fig1[fig1['est'] == w_estado]['est'].astype(
                            str) + '<br>' +
                        '<b>Valor</b>: R$ ' + [f'{x:,.0f}' for x in
                                                fig1[fig1['est'] == w_estado][
                                                    'val']] + '<br>' +
                        '<b>Curso</b>: ' + fig1[fig1['est'] == w_estado][
                            'curso'].astype(str) + '<br>'

                        )],

        'layout': go.Layout(
            width=780,
            height=520,
            title={
                'text': 'Mensalidades dos financiamentos: Estado (' + (w_estado) + ')',
                'y': 0.93,
                'x': 0.43,
                'xanchor': 'center',
                'yanchor': 'top'},
            titlefont={'family': 'Oswald',
                       'color': 'rgb(230, 34, 144)',
                       'size': 20},

            hovermode='x',

            xaxis=dict(title='<b>Cursos</b>',
                       color='rgb(230, 34, 144)',
                       showline=True,
                       showgrid=True,
                       showticklabels=True,
                       linecolor='rgb(104, 204, 104)',
                       linewidth=2,
                       ticks='outside',
                       tickfont=dict(
                           family='Arial',
                           size=12,
                           color='rgb(17, 37, 239)'
                       )

                       ),

            yaxis=dict(title='<b>Valores</b>',
                       color='rgb(230, 34, 144)',
                       showline=True,
                       showgrid=True,
                       showticklabels=True,
                       linecolor='rgb(104, 204, 104)',
                       linewidth=2,
                       ticks='outside',
                       tickfont=dict(
                           family='Arial',
                           size=12,
                           color='rgb(17, 37, 239)'
                       )
                       ),

            legend=dict(title='',
                        x=0.25,
                        y=1.08,
                        orientation='h',
                        bgcolor='rgba(255, 255, 255, 0)',
                        traceorder="normal",
                        font=dict(
                            family="sans-serif",
                            size=12,
                            color='#000000')),

            legend_title_font_color="green",
            uniformtext_minsize=12,
            uniformtext_mode='hide',

        )

    }


# Create combination of bar chart and line chart
#5) Identificar as instituições de ensino superior da região nordeste no mês de setembro de 2019 com maior número de alunos contemplados com o financiamento. Além das instituições de ensino superior e a quantidade de alunos contemplados, devem ser apresentados os respectivos estados e municípios das instituições de ensino superior.
@app.callback(Output('bar_line_4', 'figure'),
              [Input('w_estado', 'value')])
def update_graph(w_estado):
# Data for bar
    fig2_1 = tab2.groupby(['est', 'no_ies'])['mun'].sum().reset_index()
# Data for line
    fig2_2 = tab2.groupby(['est', 'no_ies'])['qtd'].sum().reset_index()

    return {
        'data': [go.Bar(x=fig2_1[fig2_1['est'] == w_estado]['no_ies'],
                        y=fig2_1[fig2_1['est'] == w_estado]['mun'],
                        text=fig2_1[fig2_1['est'] == w_estado]['mun'],
                        name='Municipios',
                        texttemplate='%{text:.2s}',
                        textposition='auto',
                        marker = dict(color='rgb(11, 220, 239)'),
                        yaxis='y1',
                        hoverinfo='text',
                        hovertext=
                        '<b>Estado</b>: ' + fig2_1[fig2_1['est'] == w_estado]['est'].astype(str) + '<br>'+
                        '<b>Municipio</b>: ' + fig2_1[fig2_1['est'] == w_estado]['mun'] + '<br>'+
                        '<b>Instituição</b>: ' + fig2_1[fig2_1['est'] == w_estado]['no_ies'].astype(str) + '<br>'
                        ),

                go.Scatter(
                            x=fig2_2[fig2_2['est'] == w_estado]['no_ies'],
                            y=fig2_2[fig2_2['est'] == w_estado]['qtd'],
                            name='Alunos',
                            text=fig2_2[fig2_2['est'] == w_estado]['qtd'],
                            mode='markers + lines',
                            marker=dict(color='#bd3786'),
                            yaxis='y2',
                            hoverinfo='text',
                            hovertext=
                            '<b>Estado</b>: ' + fig2_2[fig2_2['est'] == w_estado]['est'].astype(str) + '<br>'+
                            '<b>Alunos</b>: ' + [f'{x:,.0f}' for x in fig2_2[fig2_2['est'] == w_estado]['qtd']] + '<br>'+
                            '<b>Instituição</b>: ' + fig2_2[fig2_2['est'] == w_estado]['no_ies'].astype(str) + '<br>'
                            )],


        'layout': go.Layout(
             width=780,
             height=520,
             title={
                'text': 'Instituições com o número de alunos contemplados: Estado (' + (w_estado) + ')',
                'y': 0.93,
                'x': 0.43,
                'xanchor': 'center',
                'yanchor': 'top'},
             titlefont={'family': 'Oswald',
                        'color': 'rgb(230, 34, 144)',
                        'size': 20},

             hovermode='x',

             xaxis=dict(title='<b>Estado</b>',
                        tick0=0,
                        dtick=1,
                        color='rgb(230, 34, 144)',
                        showline=True,
                        showgrid=True,
                        showticklabels=True,
                        linecolor='rgb(104, 204, 104)',
                        linewidth=2,
                        ticks='outside',
                        tickfont=dict(
                            family='Arial',
                            size=12,
                            color='rgb(17, 37, 239)'
                        )

                ),

             yaxis=dict(title='<b>Municipios</b>',
                        color='rgb(230, 34, 144)',
                        showline=True,
                        showgrid=True,
                        showticklabels=True,
                        linecolor='rgb(104, 204, 104)',
                        linewidth=2,
                        ticks='outside',
                        tickfont=dict(
                           family='Arial',
                           size=12,
                           color='rgb(17, 37, 239)'
                        )

                ),
             yaxis2=dict(title='<b>Quantidade</b>', overlaying='y', side='right',
                         color='rgb(230, 34, 144)',
                         showline=True,
                         showgrid=False,
                         showticklabels=True,
                         linecolor='rgb(104, 204, 104)',
                         linewidth=2,
                         ticks='outside',
                         tickfont=dict(
                           family='Arial',
                           size=12,
                           color='rgb(17, 37, 239)'
                         )

                 ),

             legend=dict(title='',
                         x=0.25,
                         y=1.08,
                         orientation='h',
                         bgcolor='rgba(255, 255, 255, 0)',
                         traceorder="normal",
                         font=dict(
                              family="sans-serif",
                              size=12,
                              color='#000000')),

                         legend_title_font_color="green",
                         uniformtext_minsize=12,
                         uniformtext_mode='hide',

                 )

    }


# Create horizontal bar chart 1
#6) Identificar os estados da região Nordeste com maior número de alunos contemplados com o financiamento no mês de setembro de 2019. Além dos cursos e da quantidade de alunos contemplados, devem ser apresentados os respectivos estados e municípios.
@app.callback(Output('top_10_1', 'figure'),
              [Input('w_estado', 'value')])
def update_graph(w_estado):
    fig3 = tab3.groupby(['est'])[['curso', 'qtd', 'mun']].sum().sort_values(by=['qtd'],
                                                                              ascending=False).nlargest(9, columns=['qtd']).reset_index()

    return {
        'data': [go.Bar(x=fig3['qtd'],
                        y=fig3['est'],
                        text=fig3['qtd'],
                        texttemplate='%{text:.2s}',
                        textposition='inside',
                        marker=dict(
                            color=fig3['qtd'],
                            colorscale='portland',
                            showscale=False),
                        orientation='h',
                        yaxis='y1',
                        hoverinfo='text',
                        hovertext=
                        '<b>Estado</b>: ' + fig3['est'].astype(str) + '<br>' +
                        '<b>Quantidade</b>: ' + [f'{x:,.0f}' for x in fig3['qtd']] + '<br>'
                        )],

        'layout': go.Layout(
            width=780,
            height=520,
            # plot_bgcolor='rgb(250, 242, 242)',
            # paper_bgcolor='rgb(250, 242, 242)',
            title={
                'text': 'Os estados com o maior número de alunos contemplados',
                'y': 0.93,
                'x': 0.43,
                'xanchor': 'center',
                'yanchor': 'top'},
            titlefont={'family': 'Oswald',
                       'color': 'rgb(230, 34, 144)',
                       'size': 20},

            hovermode='closest',

            xaxis=dict(title='<b>Quantidade</b>',
                       color='rgb(230, 34, 144)',
                       showline=True,
                       showgrid=True,
                       showticklabels=True,
                       linecolor='rgb(104, 204, 104)',
                       linewidth=2,
                       ticks='outside',
                       tickfont=dict(
                           family='Arial',
                           size=12,
                           color='rgb(17, 37, 239)'
                       )

                       ),

            yaxis=dict(title='<b>Estado</b>',
                       autorange='reversed',
                       color='rgb(230, 34, 144)',
                       showline=True,
                       showgrid=False,
                       showticklabels=True,
                       linecolor='rgb(104, 204, 104)',
                       linewidth=2,
                       ticks='outside',
                       tickfont=dict(
                           family='Arial',
                           size=12,
                           color='rgb(17, 37, 239)'
                       )

                       )

        )
    }


# Create horizontal bar chart 2
#6) Identificar os 10 cursos da região Nordeste com maior número de alunos contemplados com o financiamento no mês de setembro de 2019. Além dos cursos e da quantidade de alunos contemplados, devem ser apresentados os respectivos estados e municípios.
@app.callback(Output('top_10_2', 'figure'),
              [Input('w_estado', 'value')])
def update_graph(w_estado):
    fig4 = tab3.groupby(['curso'])[['est', 'qtd', 'mun']].sum().sort_values(by=['qtd'],
                                                                              ascending=False).nlargest(10, columns=['qtd']).reset_index()

    return {
        'data': [go.Bar(x=fig4['qtd'],
                        y=fig4['curso'],
                        text=fig4['qtd'],
                        texttemplate='%{text:.2s}',
                        textposition='outside',
                        marker=dict(
                            color=fig4['qtd'],
                            colorscale='portland',
                            showscale=False),
                        orientation='h',
                        yaxis='y1',
                        hoverinfo='text',
                        hovertext=
                        '<b>Curso</b>: ' + fig4['curso'].astype(str) + '<br>' +
                        '<b>Quantidade</b>: ' + [f'{x:,.0f}' for x in fig4['qtd']] + '<br>'
                        )],

        'layout': go.Layout(
            width=780,
            height=520,
            # plot_bgcolor='rgb(250, 242, 242)',
            # paper_bgcolor='rgb(250, 242, 242)',
            title={
                'text': 'Os 10 cursos com o maior número de alunos contemplados',
                'y': 0.93,
                'x': 0.43,
                'xanchor': 'center',
                'yanchor': 'top'},
            titlefont={'family': 'Oswald',
                       'color': 'rgb(230, 34, 144)',
                       'size': 20},

            hovermode='closest',

            xaxis=dict(title='<b>Quantidade</b>',
                       color='rgb(230, 34, 144)',
                       showline=True,
                       showgrid=True,
                       showticklabels=True,
                       linecolor='rgb(104, 204, 104)',
                       linewidth=2,
                       ticks='outside',
                       tickfont=dict(
                           family='Arial',
                           size=12,
                           color='rgb(17, 37, 239)'
                       )

                       ),

            yaxis=dict(title='<b>Curso</b>',
                       autorange='reversed',
                       color='rgb(230, 34, 144)',
                       showline=True,
                       showgrid=False,
                       showticklabels=True,
                       linecolor='rgb(104, 204, 104)',
                       linewidth=2,
                       ticks='outside',
                       tickfont=dict(
                           family='Arial',
                           size=12,
                           color='rgb(17, 37, 239)'
                       )

                       )

        )
    }


if __name__ == '__main__':
    app.run_server(debug=True)
