# Made by Hemaksh Chaturvedi

import dash
from dash import dcc, html, Input, Output
import pandas as pd
import random
import networkx as nx
import plotly.graph_objects as go
import plotly.express as px
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import base64
import io
from plotly.subplots import make_subplots

# Create Dash app
app = dash.Dash(
    __name__,
    suppress_callback_exceptions=True,
    external_stylesheets=[
        "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css"
    ]
)

app.title = "Spotify Multi-Page Dashboard"

# Add custom CSS directly into the layout
# Corrected custom_styles definition
custom_styles = html.Div([
    html.Div(
        '''
        <style>
        body {
            margin: 0;
            font-family: Arial, sans-serif;
            background-color: #191414; /* Spotify black */
        }
        .bubbles {
            position: relative;
            width: 100%;
            height: 100vh;
            overflow: hidden;
            background-color: #191414;
        }
        .bubble {
            position: absolute;
            bottom: -100px;
            background: rgba(29, 185, 84, 0.8); /* Spotify green */
            border-radius: 50%;
            animation: float 10s infinite ease-in-out;
            opacity: 0.7;
        }
        @keyframes float {
            0% { transform: translateY(0); opacity: 0.8; }
            50% { opacity: 0.4; }
            100% { transform: translateY(-120vh); opacity: 0; }
        }
        .bubble:nth-child(1) { left: 20%; width: 80px; height: 80px; animation-delay: 0s; }
        .bubble:nth-child(2) { left: 40%; width: 50px; height: 50px; animation-delay: 2s; }
        .bubble:nth-child(3) { left: 60%; width: 100px; height: 100px; animation-delay: 4s; }
        .bubble:nth-child(4) { left: 70%; width: 70px; height: 70px; animation-delay: 6s; }
        .spotify-logo {
            position: absolute;
            top: 40%;
            left: 50%;
            transform: translate(-50%, -50%);
            text-align: center;
            color: #1db954;
            font-size: 60px;
            font-family: Arial, sans-serif;
        }
        .spotify-logo i {
            font-size: 100px;
            margin-bottom: 20px;
        }
        </style>
        ''',
        style={"display": "none"}  # Ensures this Div does not render visibly on the page
    )
])


# Load simulated collaboration data
simulated_edges_df = pd.read_csv('simulated_collaborations.csv')

# Create a NetworkX graph
G = nx.Graph()
G.add_edges_from(simulated_edges_df.values)

# Add node attributes (e.g., random popularity scores and collaboration reach)
for node in G.nodes:
    G.nodes[node]['popularity'] = random.randint(10, 100)  # Popularity scores (10-100)
    G.nodes[node]['reach'] = random.randint(1, 50)         # Collaboration reach (1-50)

# Load Spotify tracks dataset
spotify_tracks_path = "Data/spotify_tracks_dataset.csv"  # Replace with your file path
spotify_tracks = pd.read_csv(spotify_tracks_path)

# Attributes for Radar Chart
attributes = ['danceability', 'energy', 'acousticness', 'speechiness', 'liveness']

# Load artificial dataset for Word Cloud
artificial_data_path = "Data/spotify_dataset.csv"  # Replace with your file path
artificial_data = pd.read_csv(artificial_data_path)
artificial_data = artificial_data[['name', 'popularity']].dropna()
title_popularity_dict = dict(zip(artificial_data['name'], artificial_data['popularity']))

# Generate Word Cloud
def generate_wordcloud():
    wordcloud = WordCloud(
        width=800,
        height=800,
        background_color="#191414",  # Spotify Black
        colormap="Greens",  # Spotify Green theme
        contour_color="#1db954",  # Spotify Green contour
        contour_width=2,
        max_words=200,
        prefer_horizontal=0.8
    ).generate_from_frequencies(title_popularity_dict)

    # Save the word cloud to a buffer
    buffer = io.BytesIO()
    plt.figure(figsize=(10, 10), facecolor="#191414")
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.tight_layout(pad=0)
    plt.savefig(buffer, format="png", facecolor="#191414")
    buffer.seek(0)
    image_data = base64.b64encode(buffer.read()).decode("utf-8")
    buffer.close()
    return image_data

wordcloud_image = generate_wordcloud()

# Create Tree Map
def create_treemap():
    spotify_dataset = pd.read_csv('Data/spotify_dataset.csv')  # Replace with your file path
    genre_popularity = spotify_dataset.groupby('genre')['popularity'].mean().reset_index()

    # Spotify Palette
    spotify_palette = [
        '#1a5e35', '#2e7d48', '#4b9f5a', '#74b75e',
        '#8ccf70', '#a1e184', '#c3e6a1'
    ]

    fig = px.treemap(
        genre_popularity,
        path=['genre'],  # Hierarchical data: Just genres in this case
        values='popularity',  # Size of each rectangle corresponds to average popularity
        color='popularity',  # Color based on popularity
        color_continuous_scale=spotify_palette,  # Apply Spotify palette
        title='Tree Map: Average Popularity by Genre'
    )

    # Update layout for a polished appearance
    fig.update_layout(
        margin=dict(t=40, l=20, r=20, b=20),
        paper_bgcolor='#191414',  # Spotify black background
        font=dict(family='Arial', size=12, color='#c3e6a1'),  # Pale green text
        title_font=dict(size=20, color='#a1e184', family='Arial'),  # Mint green for title
    )

    # Update the color bar for smoothness
    fig.update_coloraxes(
        colorbar=dict(
            title='Popularity',
            thickness=15,
            outlinewidth=0,  # Remove color bar border for a flush look
            tickfont=dict(color='#c3e6a1', size=10),  # Pale green ticks
            titlefont=dict(color='#a1e184', size=12)  # Mint green title
        )
    )

    # Update traces for polished visuals
    fig.update_traces(
        marker=dict(
            line=dict(width=1, color='#191414'),  # Thin border for spacing
            pad=dict(t=10, l=10, r=10, b=10)  # Add padding for better spacing
        )
    )
    return fig

treemap_figure = create_treemap()

# Create Sunburst Chart for User Behavior Page
def create_sunburst():
    user_behavior_dataset = pd.read_excel('Data/Spotify_User_Behavior_Dataset.xlsx')

    # Prepare data for the Sunburst chart
    sunburst_data = (
        user_behavior_dataset.groupby(['spotify_subscription_plan', 'premium_sub_willingness'])
        .size()
        .reset_index(name='count')
    )

    fig = px.sunburst(
        sunburst_data,
        path=['spotify_subscription_plan', 'premium_sub_willingness'],
        values='count',
        color='count',
        color_continuous_scale=[
            'rgba(29,185,84,0.9)',
            'rgba(25,94,53,0.7)',
            'rgba(46,125,72,0.8)',
            'rgba(75,159,90,0.9)',
        ],
        title='Multi-Layered Pie Chart: Subscription Plans and Willingness to Upgrade'
    )

    fig.update_layout(
        margin=dict(t=50, l=20, r=20, b=20),
        paper_bgcolor='#191414',
        font=dict(family='Arial', size=14, color='#c3e6a1'),
        title_font=dict(size=20, color='#a1e184'),
    )
    return fig

sunburst_figure = create_sunburst()

def create_polar_chart():
    user_behavior_dataset = pd.read_excel('Data/Spotify_User_Behavior_Dataset.xlsx')

    # Filter and prepare data for polar chart
    polar_data = user_behavior_dataset.groupby(['Age', 'music_time_slot']).size().reset_index(name='count')

    # Create a polar chart with enhanced visuals
    fig = px.line_polar(
        polar_data,
        r='count',  # Radial axis: Listening frequency count
        theta='music_time_slot',  # Angular axis: Time of day
        color='Age',  # Different lines for each age group
        line_close=True,  # Connect the line to form a closed shape
        title='Polar Chart: Listening Time by Age Group',
        color_discrete_sequence=[
            '#1db954',  # Spotify Green
            '#1a5e35',  # Deep Green
            '#2e7d48',  # Forest Green
            '#4b9f5a',  # Moss Green
            '#8ccf70'   # Pistachio Green
        ]
    )

    # Update layout for improved aesthetics
    fig.update_layout(
        polar=dict(
            bgcolor='#232723',  # Dark background for the polar area
            angularaxis=dict(
                showline=False,
                linewidth=2,
                linecolor='#e1ece3',
                showgrid=True,
                gridcolor='#4d4d4d',  # Subtle grid lines
                tickfont=dict(size=12, color='#c3e6a1')  # Tick font styling
            ),
            radialaxis=dict(
                showline=True,
                linewidth=1.5,
                gridcolor='#666666',
                tickfont=dict(size=12, color='#c3e6a1'),  # Subtle font styling
                linecolor='#4d4d4d'  # Border color for radial lines
            )
        ),
        paper_bgcolor='#232723',  # Dark Spotify background
        font=dict(size=14, color='#e1ece3'),  # Light font for readability
        title_font=dict(size=20, color='#a1e184'),  # Mint Green title font
        legend=dict(
            bgcolor='#191414',  # Dark Spotify black for legend background
            bordercolor='#666666',  # Subtle border for legend
            borderwidth=1,
            font=dict(size=12, color='#e1ece3')  # Styling for legend text
        ),
        margin=dict(l=50, r=50, t=80, b=50)  # Adjusted margins for spacing
    )
    return fig

def create_gauge_plot():
    # Load the Spotify User Behavior dataset
    user_behavior_dataset = pd.read_excel('Data/Spotify_User_Behavior_Dataset.xlsx')

    # Map textual ratings to numeric values
    satisfaction_mapping = {
        "Very Dissatisfied": 1,
        "Dissatisfied": 2,
        "Ok": 3,
        "Satisfied": 4,
        "Very Satisfied": 5
    }

    # Map columns
    user_behavior_dataset['pod_variety_satisfaction_numeric'] = user_behavior_dataset['pod_variety_satisfaction'].map(satisfaction_mapping)

    # Calculate averages
    average_music_satisfaction = user_behavior_dataset['music_recc_rating'].mean()
    average_podcast_satisfaction = user_behavior_dataset['pod_variety_satisfaction_numeric'].mean()

    # Create the subplot layout for two gauges side by side
    fig = make_subplots(rows=1, cols=2, specs=[[{"type": "indicator"}, {"type": "indicator"}]])


    # Add the first gauge (Music Recommendations)
    fig.add_trace(go.Indicator(
        mode="gauge+number",
        value=average_music_satisfaction,
        title={'text': "Music Recommendations", 'font': {'size': 18, 'color': '#a1e184'}},
        number={'font': {'size': 24, 'color': '#e1ece3'}},  # Ensure the number is displayed
        gauge={
            'axis': {'range': [0, 5], 'tickwidth': 1.5, 'tickcolor': '#e1ece3'},
            'bar': {'color': '#1db954', 'thickness': 0.3},
            'bgcolor': '#232723',
            'steps': [
                {'range': [0, 2], 'color': '#a8b2a8'},
                {'range': [2, 4], 'color': '#a8b2a8'},
                {'range': [4, 5], 'color': '#a8b2a8'}
            ],
            'threshold': {
                'line': {'color': '#457e59', 'width': 6},
                'thickness': 0.8,
                'value': average_music_satisfaction
            }
        }
    ), row=1, col=1)

    # Add the second gauge (Podcast Variety)
    fig.add_trace(go.Indicator(
        mode="gauge+number",
        value=average_podcast_satisfaction,
        title={'text': "Podcast Variety", 'font': {'size': 18, 'color': '#a1e184'}},
        number={'font': {'size': 24, 'color': '#e1ece3'}},  # Ensure the number is displayed
        gauge={
            'axis': {'range': [0, 5], 'tickwidth': 1.5, 'tickcolor': '#e1ece3'},
            'bar': {'color': '#1db954', 'thickness': 0.3},
            'bgcolor': '#232723',
            'steps': [
                {'range': [0, 2], 'color': '#a8b2a8'},
                {'range': [2, 4], 'color': '#a8b2a8'},
                {'range': [4, 5], 'color': '#a8b2a8'}
            ],
            'threshold': {
                'line': {'color': '#457e59', 'width': 6},
                'thickness': 0.8,
                'value': average_podcast_satisfaction
            }
        }
    ), row=1, col=2)

    # Update layout
    fig.update_layout(
        paper_bgcolor='#232723',
        font={'color': '#e1ece3', 'family': "Arial"},
        margin=dict(l=150, r=50, t=80, b=50),
        title_text="User Satisfaction: Music Recommendations and Podcast Variety",
        title_font=dict(size=20, color='#a1e184')
    )

    return fig
def create_circle_pack_diagram():
    # Load data
    xl = pd.ExcelFile(r"Data/Spotify_User_Behavior_Dataset.xlsx")
    spotify_user_behavior_data = xl.parse('Sheet1')
    
    # Preparing data for a circle pack diagram
    circle_pack_data = spotify_user_behavior_data.groupby(
        ['spotify_subscription_plan', 'music_time_slot', 'fav_music_genre']
    ).size().reset_index(name='count')

    # Creating the circle pack diagram
    fig = px.treemap(
        circle_pack_data,
        path=['spotify_subscription_plan', 'music_time_slot', 'fav_music_genre'],  # Hierarchical levels
        values='count',  # Size of circles
        title='User Behavior Clustering (Circle Pack Diagram)',
        color='spotify_subscription_plan',  # Coloring by subscription plan
        color_discrete_map={
            'Free (ad-supported)': '#8ccf70',  # Light Green
            'Premium': '#333333',             # Spotify Green
        }
    )

    # Update layout for better visualization
    fig.update_layout(
        paper_bgcolor='#191414',  # Spotify Black
        font=dict(color='#e1ece3', size=14),  # Pale Green for text with adjusted size
        title=dict(
            #text="User Behavior Clustering (Circle Pack Diagram)",
            font=dict(size=24, color="#1db954"),  # Spotify Green for title
            x=0.5, y=0.95, xanchor="center", yanchor="top"
        ),
        treemapcolorway=['#1db954', '#74b75e'],  # Custom Spotify color palette
        margin=dict(l=20, r=20, t=80, b=20),  # Reduced margins
    )

    # Update traces for smoother visuals
    fig.update_traces(
        hovertemplate="<b>%{label}</b><br>Count: %{value}<extra></extra>",  # Custom hover info
        marker=dict(line=dict(width=1.5, color='#232323'))  # Smooth borders for sections
    )

    return fig


# Spotify color palette
spotify_colors = [
    "#1db954", "#1a5e35", "#2e7d48", "#4b9f5a", "#74b75e"
]

# Navigation bar
nav_bar = html.Div(
    style={'backgroundColor': '#191414', 'padding': '10px', 'textAlign': 'center'},
    children=[
        dcc.Link('For Artists | ', href='/artists', style={'color': '#1db954', 'marginRight': '15px', 'fontSize': '18px'}),
        dcc.Link('User Behavior | ', href='/user-behavior', style={'color': '#1db954', 'marginRight': '15px', 'fontSize': '18px'}),
        dcc.Link('Genre Popularity', href='/genre-popularity', style={'color': '#1db954', 'fontSize': '18px'})  # New link
    ]
)


# App layout
app.layout = html.Div(
    style={'backgroundColor': '#191414', 'color': '#e1ece3'},
    children=[
        custom_styles,  # Add the custom styles here
        dcc.Location(id='url', refresh=False),
        nav_bar,
        html.Div(id='page-content', style={'padding': '20px'})
    ]
)



# Define the landing page
def render_landing_page():
    return html.Div(
        className="bubbles",
        children=[
            html.Div(className="bubble"),
            html.Div(className="bubble"),
            html.Div(className="bubble"),
            html.Div(className="bubble"),
            html.Div(
                className="spotify-logo",
                children=[
                    html.I(className="fab fa-spotify"),  # Spotify Font Awesome Icon
                    html.Div(
                        "Spotify Dashboard",
                        style={'fontSize': '24px', 'marginTop': '10px'}
                    ),
                ],
            ),
            html.Div(
                style={'textAlign': 'center', 'marginTop': '70vh', 'color': '#e1ece3'},
                children=[
                    dcc.Link("Enter Dashboard", href="/artists", style={
                        'fontSize': '20px', 'color': '#1db954'
                    })
                ]
            )
        ]
    )


# Page: For Artists
def render_artists_page():
    # Compute spotify_tracks_summary locally to avoid scope issues
    spotify_tracks_summary = spotify_tracks.groupby('track_genre')[attributes].mean().reset_index()
    
    # Radar Chart
    fig_radar = go.Figure()
    for i, row in spotify_tracks_summary.iterrows():
        fig_radar.add_trace(go.Scatterpolar(
            r=row[attributes].tolist(),
            theta=attributes,
            fill='toself',
            name=row['track_genre'],
            opacity=0.8,
            line=dict(color=spotify_colors[i % len(spotify_colors)], width=2),
            fillcolor=spotify_colors[i % len(spotify_colors)],
        ))

    fig_radar.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 1], gridcolor="#4d4d4d"),
            angularaxis=dict(gridcolor="#4d4d4d"),
        ),
        title="Comparison of Track Features Across Genres",
        paper_bgcolor="#191414",
        font=dict(color="white"),
        height=1000,
        width= 2300
    )

    return html.Div([
        html.H1('For Artists: Insights', style={'textAlign': 'center', 'color': '#1db954'}),

        # Word Cloud Section
        html.Div([
            html.H3('Popular Song Titles', style={'textAlign': 'center', 'color': '#1db954'}),
            html.Img(src=f"data:image/png;base64,{wordcloud_image}", style={'display': 'block', 'margin': '0 auto', 'borderRadius': '10px'})
        ], style={'padding': '20px', 'backgroundColor': '#232723', 'borderRadius': '10px', 'marginBottom': '20px'}),

        # Tree Map Section
        html.Div([
            dcc.Graph(figure=treemap_figure)
        ], style={'padding': '20px', 'backgroundColor': '#232723', 'borderRadius': '10px', 'marginBottom': '20px'}),

        # Filters and Collaboration Graph
        html.Div([
            html.Label("Filter by Popularity Influence (X-axis)", style={'color': '#e1ece3', 'fontSize': '14px'}),
            dcc.RangeSlider(
                id='popularity-filter',
                min=10,
                max=100,
                step=5,
                marks={10: '10', 50: '50', 100: '100'},
                value=[10, 100]
            ),
            html.Br(),
            html.Label("Filter by Collaboration Reach (Y-axis)", style={'color': '#e1ece3', 'fontSize': '14px'}),
            dcc.RangeSlider(
                id='reach-filter',
                min=1,
                max=50,
                step=1,
                marks={1: '1', 25: '25', 50: '50'},
                value=[1, 50]
            ),
            dcc.Graph(id='collaboration-graph'),
        ], style={'padding': '20px', 'backgroundColor': '#232723', 'borderRadius': '10px', 'marginBottom': '20px'}),

        # Radar Chart
        html.Div([
            dcc.Graph(figure=fig_radar)
        ], style={'padding': '20px', 'backgroundColor': '#232723', 'borderRadius': '10px'})
    ])

# Page: User Behavior
def render_user_behavior_page():
    # Create the gauge plot
    gauge_figure = create_gauge_plot()
    
    return html.Div([
        html.H1('User Behavior Insights', style={'textAlign': 'center', 'color': '#1db954'}),
        
        # Sunburst Chart Section
        html.Div([
            dcc.Graph(figure=sunburst_figure)
        ], style={'padding': '20px', 'backgroundColor': '#232723', 'borderRadius': '10px', 'marginBottom': '20px'}),

        # Polar Chart Section
        html.Div([
            dcc.Graph(figure=create_polar_chart())
        ], style={'padding': '20px', 'backgroundColor': '#232723', 'borderRadius': '10px'}),

        # Gauge Plot Section
        html.Div([
            dcc.Graph(figure=gauge_figure)
        ], style={'padding': '20px', 'backgroundColor': '#232723', 'borderRadius': '10px', 'marginBottom': '20px'}),

        # Circle Pack Diagram Section
        html.Div([
            html.H3("User Behavior Clustering", style={'textAlign': 'center', 'color': '#1db954'}),
            dcc.Graph(figure=create_circle_pack_diagram())
        ], style={'padding': '20px', 'backgroundColor': '#232723', 'borderRadius': '10px', 'marginBottom': '20px'}),
    ])



# Page: Genre Popularity with Filters
def render_genre_popularity_page():
    # Load dataset
    data_path = "Data/spotify_dataset.csv"  # Replace with your file path
    spotify_data = pd.read_csv(data_path)

    # Dropdown options for genres
    dropdown_options = [{"label": "All Genres", "value": "All"}]
    dropdown_options += [{"label": genre, "value": genre} for genre in spotify_data['genre'].unique()]

    # Layout for the page
    layout = html.Div([
        html.H1('Genre Popularity Insights', style={'textAlign': 'center', 'color': '#1db954'}),
        
        # Filters: Dropdown and Slider
        html.Div([
            html.Label("Filter by Genre:", style={'color': '#e1ece3', 'fontSize': '16px'}),
            dcc.Dropdown(
                id='genre-dropdown',
                options=dropdown_options,
                value="All",
                placeholder="Select a genre",
                style={'color': '#000000', 'backgroundColor': '#e1ece3'}
            ),
            html.Br(),
            html.Label("Number of Genres to Display:", style={'color': '#e1ece3', 'fontSize': '16px'}),
            dcc.Slider(
                id='genre-limit-slider',
                min=1,
                max=100,
                step=1,
                value=5,  # Default value
                marks={i: str(i) for i in range(1, 101)},  # Limit to 10 genres
                tooltip={"placement": "bottom", "always_visible": True},
            )
        ], style={'padding': '20px', 'backgroundColor': '#232723', 'borderRadius': '10px', 'marginBottom': '20px'}),
        
        # Sunburst Chart
        html.Div([
            dcc.Graph(id='sunburst-chart')
        ], style={'padding': '20px', 'backgroundColor': '#232723', 'borderRadius': '10px'})
    ], style={'backgroundColor': '#191414', 'padding': '20px', 'borderRadius': '10px'})

    return layout

@app.callback(
    Output('sunburst-chart', 'figure'),
    [Input('genre-dropdown', 'value'),
     Input('genre-limit-slider', 'value')]
)
def update_sunburst_chart(selected_genre, genre_limit):
    # Load dataset
    data_path = "Data/spotify_dataset.csv"  # Replace with your file path
    spotify_data = pd.read_csv(data_path)

    # Select and clean relevant columns
    spotify_data = spotify_data[['genre', 'artists', 'popularity']].dropna()

    # Aggregate data for visualization
    genre_data = spotify_data.groupby('genre').agg({'popularity': 'sum'}).reset_index()
    artist_data = spotify_data.groupby(['genre', 'artists']).agg({'popularity': 'sum'}).reset_index()

    # Sort genres by popularity and apply genre limit
    genre_data = genre_data.sort_values('popularity', ascending=False).head(genre_limit)
    artist_data = artist_data[artist_data['genre'].isin(genre_data['genre'])]

    # Create Sunburst chart data based on the selected genre
    def create_sunburst_data(selected_genre=None):
        if selected_genre and selected_genre != "All":
            filtered_artist_data = artist_data[artist_data['genre'] == selected_genre]
            filtered_genre_data = genre_data[genre_data['genre'] == selected_genre]
        else:
            filtered_artist_data = artist_data
            filtered_genre_data = genre_data

        labels = list(filtered_genre_data['genre'])
        parents = [''] * len(filtered_genre_data)
        values = list(filtered_genre_data['popularity'])

        for _, row in filtered_artist_data.iterrows():
            labels.append(row['artists'])
            parents.append(row['genre'])
            values.append(row['popularity'])

        return labels, parents, values

    labels, parents, values = create_sunburst_data(selected_genre)

    # Create Sunburst chart
    fig = go.Figure(go.Sunburst(
        labels=labels,
        parents=parents,
        values=values,
        branchvalues="total",
        hoverinfo="label+value+percent entry",
        marker=dict(colorscale="Greens")
    ))

    # Update layout
    fig.update_layout(
        title=dict(
            text="Genre, Artist, and Popularity Distribution",
            font=dict(size=22, color="#1db954"),
            x=0.5,
            y=0.95,
            xanchor="center",
            yanchor="top"
        ),
        font=dict(size=14, color="white"),
        paper_bgcolor="#191414",  # Spotify black background
        height=800,
        margin=dict(l=50, r=50, t=80, b=50)
    )

    return fig


# Callback for Collaboration Graph
@app.callback(
    Output('collaboration-graph', 'figure'),
    [Input('popularity-filter', 'value'),
     Input('reach-filter', 'value')]
)
def update_collaboration_graph(popularity_range, reach_range):
    # Filter nodes based on the sliders
    filtered_nodes = [node for node, attr in G.nodes(data=True)
                      if popularity_range[0] <= attr['popularity'] <= popularity_range[1]
                      and reach_range[0] <= attr['reach'] <= reach_range[1]]

    # Subgraph with filtered nodes
    filtered_G = G.subgraph(filtered_nodes)

    # Extract node attributes
    node_x = [G.nodes[node]['popularity'] for node in filtered_G.nodes]
    node_y = [G.nodes[node]['reach'] for node in filtered_G.nodes]
    node_size = [G.nodes[node]['popularity'] for node in filtered_G.nodes]
    node_color = [
        '#62d089' if G.nodes[node]['popularity'] > 75 else
        '#457e59' if G.nodes[node]['popularity'] > 50 else
        '#a8b2a8'
        for node in filtered_G.nodes
    ]

    # Extract edge coordinates
    edge_x, edge_y = [], []
    for edge in filtered_G.edges():
        x0, y0 = G.nodes[edge[0]]['popularity'], G.nodes[edge[0]]['reach']
        x1, y1 = G.nodes[edge[1]]['popularity'], G.nodes[edge[1]]['reach']
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])

    # Create the updated Plotly figure
    fig = go.Figure()

    # Add edges
    fig.add_trace(go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=0.5, color='#232723'),
        hoverinfo='none',
        mode='lines'
    ))

    # Add nodes
    fig.add_trace(go.Scatter(
        x=node_x, y=node_y,
        mode='markers',
        marker=dict(
            size=node_size,
            color=node_color,
            line=dict(color='#e1ece3', width=1)
        ),
        text=[f"Artist: {node}, Popularity: {G.nodes[node]['popularity']}, Reach: {G.nodes[node]['reach']}" for node in filtered_G.nodes],
        hoverinfo='text'
    ))

    # Update layout with proper axes
    fig.update_layout(
        title='Artist Collaboration Network',
        titlefont=dict(color='#e1ece3', size=20),
        plot_bgcolor='#232723',
        paper_bgcolor='#232723',
        font=dict(color='#e1ece3'),
        showlegend=False,
        hovermode='closest',
        margin=dict(b=0, l=0, r=0, t=40),
        xaxis=dict(
            title='Popularity Influence (Score 10-100)',
            range=[10, 100],
            titlefont=dict(color='#e1ece3', size=14),
            showgrid=False,
            zeroline=False
        ),
        yaxis=dict(
            title='Collaboration Reach (Connections 1-50)',
            range=[1, 50],
            titlefont=dict(color='#e1ece3', size=14),
            showgrid=False,
            zeroline=False
        )
    )

    return fig

# Callback for Page Navigation
@app.callback(
    Output('page-content', 'children'),
    Input('url', 'pathname')
)
def display_page(pathname):
    if pathname == '/artists':
        return render_artists_page()
    elif pathname == '/user-behavior':
        return render_user_behavior_page()
    elif pathname == '/genre-popularity':  # Add this new route
        return render_genre_popularity_page()
    else:  # Default to landing page
        return render_landing_page()

# Run app
if __name__ == '__main__':
    app.run_server(debug=True)
