import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Title
st.title("Netflix Data Visualization Dashboard")

# Load data
data = pd.read_csv('src/netflix_titles.csv')

# Preprocessing
fill_missing_val = ['director', 'cast', 'country', 'duration']
for col in fill_missing_val:
    data[col] = data[col].fillna('Unknown')
    
data['date_added'] = pd.to_datetime(data['date_added'], errors='coerce')
data['year_added'] = data['date_added'].dt.year

data = data.dropna(subset=['year_added'])
data = data.dropna(subset=['date_added'])
data['rating'] = data['rating'].fillna(data['rating'].mode()[0])

# First Graph: Distribution of Type
type_counts = data['type'].value_counts()

fig1 = go.Figure()
fig1.add_trace(go.Bar(
    x=type_counts.index,
    y=type_counts.values,
    width=[0.3, 0.3]
))
fig1.update_layout(
    title="Distribution of Type (Movie vs TV Show)",
    xaxis_title="Type",
    yaxis_title="Count",
)

# Display first graph
st.subheader("Distribution of Type (Movie vs TV Show)")
st.plotly_chart(fig1)

# Second Graph: Top 10 Countries
movies = data[data['type'] == 'Movie']
tv_shows = data[data['type'] == 'TV Show']

movies_country_counts = movies['country'].value_counts().head(10).drop('Unknown', errors='ignore')
tv_shows_country_counts = tv_shows['country'].value_counts().head(10).drop('Unknown', errors='ignore')
all_country_counts = data['country'].value_counts().head(10).drop('Unknown', errors='ignore')

fig2 = go.Figure()

# All
fig2.add_trace(go.Bar(
    x=all_country_counts.values,
    y=all_country_counts.index,
    orientation='h',
    name='All',
    visible=True
))

# Movies
fig2.add_trace(go.Bar(
    x=movies_country_counts.values,
    y=movies_country_counts.index,
    orientation='h',
    name='Movies',
    visible=False
))

# TV Shows
fig2.add_trace(go.Bar(
    x=tv_shows_country_counts.values,
    y=tv_shows_country_counts.index,
    orientation='h',
    name='TV Shows',
    visible=False
))

# Dropdown
fig2.update_layout(
    updatemenus=[
        dict(
            active=0,
            buttons=list([
                dict(label="All", method="update", args=[{"visible": [True, False, False]}, {"title": "Top 10 Countries - All Titles"}]),
                dict(label="Movies", method="update", args=[{"visible": [False, True, False]}, {"title": "Top 10 Countries - Movies Only"}]),
                dict(label="TV Shows", method="update", args=[{"visible": [False, False, True]}, {"title": "Top 10 Countries - TV Shows Only"}])
            ]),
            direction="down",
            showactive=True,
            x = 0.8,
            xanchor = 'left',
            y = 1,
            yanchor = 'top',
            font = dict(size = 14)
        )
    ],
    title="Top 10 Countries Producing Netflix Content",
    xaxis_title="Number of Titles",
    yaxis_title="Country",
    height=600
)

# Display second graph
st.subheader("Top 10 Countries Producing Netflix Content")
st.plotly_chart(fig2)



# third graph
movies_per_year = movies['year_added'].value_counts().sort_index()
tv_shows_per_year = tv_shows['year_added'].value_counts().sort_index()

fig3 = go.Figure()

# Movies
fig3.add_trace(go.Scatter(x=movies_per_year.index, y=movies_per_year.values, mode='lines + markers', name='Movies'))
# TV shows
fig3.add_trace(go.Scatter(x=tv_shows_per_year.index, y=tv_shows_per_year.values, mode='lines + markers', name='TV shows'))

fig3.update_layout(
    title='Number of Titles Added to Netflix Over Years',
    xaxis_title='Year',
    yaxis_title='Number of Titles',
    updatemenus=[
        dict(
            active = 0,
            buttons=list([
                dict(label="All", method="update", args=[{"visible": [True, True]}, {"title": "Number of Titles Added to Netflix Over Years"}]),
                dict(label="Movies", method="update", args=[{"visible": [True, False]}, {"title": "Number of Movies Added to Netflix Over Years"}]),
                dict(label="TV Shows", method="update", args=[{"visible": [False, True]}, {"title": "Number of TV Shows Added to Netflix Over Years"}]),
            ]),
            direction='down',
            showactive=True,
            x=0.9,
            y=1.2,
            font = dict(size = 14)
        )
    ]
)

st.subheader("Number of Titles Added to Netflix Over Years")
st.plotly_chart(fig3)
