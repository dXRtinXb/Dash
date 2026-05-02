import pandas as pd
from dash import Dash, html, dcc, Input, Output
import plotly.express as px

df = pd.read_csv("nobel_prizes_1901-2025_cleaned.csv")
df['award_year'] = pd.to_numeric(df['award_year'], errors='coerce')
df['prize_amount_adjusted'] = pd.to_numeric(df.get('prize_amount_adjusted', 0), errors='coerce').fillna(0)
df['sex'] = df['sex'].fillna('unknown')
df['category'] = df['category'].fillna('unknown')
df = df.dropna(subset=['award_year'])

min_year = int(df['award_year'].min())
max_year = int(df['award_year'].max())
available_categories = sorted(df['category'].unique().tolist())

app = Dash(__name__, title="Nobel Studio", update_title=None)

BG = "#07070a"
PANEL = "rgba(20,20,26,0.75)"
ACCENT = "#00e6a6"
TEXT = "#e6e6e6"
SUB = "#9aa0a6"

def empty_figure(title="No data"):
    fig = px.scatter(title=title)
    fig.update_traces(marker=dict(opacity=0))
    fig.update_layout(
        paper_bgcolor=BG,
        plot_bgcolor="#0d0e12",
        font_color=TEXT,
        title_font_size=14,
        margin=dict(l=30, r=20, t=50, b=40)
    )
    return fig

app.layout = html.Div(
    style={
        'background': f"linear-gradient(180deg, {BG}, #0d0e12)",
        'minHeight': '100vh',
        'color': TEXT,
        'fontFamily': 'Poppins, sans-serif',
        'padding': '20px',
        'display': 'flex',
        'gap': '20px'
    },
    children=[
        html.Div(style={
            'width': '300px',
            'background': PANEL,
            'borderRadius': '14px',
            'padding': '18px',
            'boxShadow': '0 12px 30px rgba(0,0,0,0.6)',
            'display': 'flex',
            'flexDirection': 'column',
            'gap': '14px'
        }, children=[
            html.H2("Nobel — Status", style={'margin': '0', 'color': TEXT}),
            html.Div(style={'display': 'flex', 'flexDirection': 'column', 'gap': '8px'}, children=[
                html.Div(children=[
                    html.Div("Total Laureates", style={'fontSize': '12px', 'color': SUB}),
                    html.Div(f"{len(df):,}", style={'fontSize': '20px', 'fontWeight': '700', 'color': ACCENT})
                ]),
                html.Div(children=[
                    html.Div("Categories", style={'fontSize': '12px', 'color': SUB}),
                    html.Div(f"{df['category'].nunique()}", style={'fontSize': '16px', 'fontWeight': '600', 'color': TEXT})
                ]),
                html.Div(children=[
                    html.Div("Years covered", style={'fontSize': '12px', 'color': SUB}),
                    html.Div(f"{min_year} — {max_year}", style={'fontSize': '16px', 'fontWeight': '600', 'color': TEXT})
                ])
            ]),
            html.Hr(style={'borderColor': '#151519'}),
            html.Div(style={'display': 'flex', 'flexDirection': 'column', 'gap': '10px'}, children=[
                html.Div("Filter categories", style={'fontSize': '13px', 'color': SUB}),
                dcc.Dropdown(
                    id='category-picker',
                    options=[{'label': c, 'value': c} for c in available_categories],
                    value=[available_categories[0]],
                    multi=True,
                    style={'color': '#111'}
                ),
                html.Div("Year range", style={'fontSize': '13px', 'color': SUB, 'marginTop': '6px'}),
                dcc.RangeSlider(
                    id='year-range',
                    min=min_year, max=max_year, step=1,
                    value=[min_year, max_year],
                    allowCross=False
                ),
                html.Div("Main plot", style={'fontSize': '13px', 'color': SUB, 'marginTop': '6px'}),
                dcc.Dropdown(
                    id='main-plot-type',
                    options=[
                        {'label': 'Avg Prize Over Time (line)', 'value': 'line_avg_prize'},
                        {'label': 'Prizes per Category (bar)', 'value': 'bar_category_counts'},
                        {'label': 'Prize distribution by Category (box)', 'value': 'box_prize_by_category'}
                    ],
                    value='line_avg_prize',
                    clearable=False,
                    style={'color': '#111'}
                ),
                html.Div("Side plot", style={'fontSize': '13px', 'color': SUB, 'marginTop': '6px'}),
                dcc.RadioItems(
                    id='side-plot-kind',
                    options=[
                        {'label': 'Gender % (pie)', 'value': 'gender_pie'},
                    ],
                    value='gender_pie',
                    labelStyle={'display': 'block', 'color': SUB}
                )
            ]),
            html.Div(style={'flex': 1}),
            html.Div("Tip: hover controls & the plots update smoothly.", style={'fontSize': '12px', 'color': SUB})
        ]),
        html.Div(style={'flex': 1, 'display': 'flex', 'flexDirection': 'column', 'gap': '18px'}, children=[
            html.Div(style={
                'background': PANEL, 'padding': '18px', 'borderRadius': '14px',
                'boxShadow': '0 12px 30px rgba(0,0,0,0.6)'
            }, children=[
                html.Div(style={'display': 'flex', 'justifyContent': 'space-between', 'alignItems': 'center'}, children=[
                    html.Div(children=[
                        html.H1("✨ The Nobel Studio", style={'margin': '0 0 6px 0', 'fontSize': '22px', 'color': TEXT}),
                        html.Div("Dark, bold, interactive — Plotly + Dash", style={'color': SUB, 'fontSize': '13px'})
                    ]),
                    html.Div(style={'display': 'flex', 'gap': '10px', 'alignItems': 'center'}, children=[
                        html.Div(style={
                            'background': '#0f0f11', 'padding': '8px 12px', 'borderRadius': '8px',
                            'boxShadow': 'inset 0 -2px 6px rgba(0,0,0,0.6)'
                        }, children=[
                            html.Div("Theme", style={'fontSize': '11px', 'color': SUB}),
                            html.Div("DARK", style={'fontWeight': '700', 'color': ACCENT})
                        ])
                    ])
                ])
            ]),
            html.Div(style={'display': 'flex', 'gap': '18px', 'alignItems': 'stretch'}, children=[
                html.Div(style={'flex': 2, 'background': PANEL, 'borderRadius': '12px', 'padding': '14px', 'boxShadow': '0 18px 40px rgba(0,0,0,0.6)'}, children=[
                    html.Div("Main visualization", style={'fontSize': '13px', 'color': SUB, 'marginBottom': '8px'}),
                    dcc.Graph(id='main-plot', config={'displayModeBar': False}, style={'height': '480px'})
                ]),
                html.Div(style={'flex': 1, 'background': PANEL, 'borderRadius': '12px', 'padding': '14px', 'boxShadow': '0 18px 40px rgba(0,0,0,0.6)'}, children=[
                    html.Div("Quick stats & mini plot", style={'fontSize': '13px', 'color': SUB, 'marginBottom': '8px'}),
                    html.Div(children=[
                        html.Div("Laureates (filtered)", style={'fontSize': '12px', 'color': SUB}),
                        html.Div(id='filtered-count', style={'fontSize': '18px', 'fontWeight': '700', 'color': ACCENT})
                    ], style={'marginBottom': '10px'}),
                    dcc.Graph(id='side-plot', config={'displayModeBar': False}, style={'height': '300px'})
                ])
            ])
        ])
    ]
)

@app.callback(
    Output('main-plot', 'figure'),
    Output('side-plot', 'figure'),
    Output('filtered-count', 'children'),
    Input('category-picker', 'value'),
    Input('year-range', 'value'),
    Input('main-plot-type', 'value'),
    Input('side-plot-kind', 'value')
)
def update_plots(selected_categories, year_range, main_type, side_kind):
    if not selected_categories:
        selected_categories = available_categories
    if not year_range or len(year_range) != 2:
        year_range = [min_year, max_year]
    dff = df[(df['award_year'] >= year_range[0]) & (df['award_year'] <= year_range[1])]
    dff = dff[dff['category'].isin(selected_categories)]
    if dff.empty:
        return empty_figure("No data"), empty_figure(""), "0 laureates found"
    if main_type == "line_avg_prize":
        avg_data = dff.groupby('award_year', as_index=False)['prize_amount_adjusted'].mean()
        if avg_data.empty:
            fig_main = empty_figure("No data")
        else:
            fig_main = px.line(avg_data, x='award_year', y='prize_amount_adjusted', markers=True, title="Avg Prize Amount Over Time", color_discrete_sequence=[ACCENT])
    elif main_type == "bar_category_counts":
        counts = dff['category'].value_counts().reset_index()
        counts.columns = ['category', 'count']
        fig_main = px.bar(counts, x='count', y='category', orientation='h', title="Prizes per Category", color='count', color_continuous_scale='Tealgrn')
    else:
        fig_main = px.box(dff, x='category', y='prize_amount_adjusted', color='category', title="Prize Distribution by Category", color_discrete_sequence=px.colors.sequential.Tealgrn)
    fig_main.update_layout(
        paper_bgcolor=BG, plot_bgcolor="#0d0e12", font_color=TEXT, title_font_size=16,
        margin=dict(l=40, r=20, t=60, b=40), transition_duration=500
    )
    if side_kind == "gender_pie":
        gender_counts = dff['sex'].value_counts().reset_index()
        gender_counts.columns = ['sex', 'count']
        fig_side = px.pie(gender_counts, names='sex', values='count', color_discrete_sequence=px.colors.sequential.Tealgrn, title="Gender Distribution")
    else:
        fig_side = px.scatter(dff, x='award_year', y='prize_amount_adjusted', color='category', color_discrete_sequence=px.colors.sequential.Tealgrn, title="Prize vs Year")
    fig_side.update_layout(
        paper_bgcolor=BG, plot_bgcolor="#0d0e12", font_color=TEXT, title_font_size=14,
        margin=dict(l=30, r=20, t=50, b=40), transition_duration=500
    )
    return fig_main, fig_side, f"{len(dff):,} laureates found"

if __name__ == "__main__":
    app.run(debug=True, port=8050)
