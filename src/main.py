#Import Required Libraries
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from statsmodels.stats.proportion import proportions_ztest
from scipy import stats

#Data Load
data = pd.read_csv("../data/website_ab_test.csv")
print(data.head())

#Data Preprocessing
print(data.isnull().sum())

print(data.info())

print(data.describe())

#Exploratory Data Analysis

figure = px.scatter(data,
                    x = 'Click Through Rate',
                    y = 'Conversion Rate',
                    color = 'Theme',
                    title = 'Click Through Rate vs. Conversion Rate',
                    trendline = 'ols')

figure.show()

figure.write_image('../output/Click_through_rate_vs_Conversion_rate.png')

#Histogram
light_theme_data = data[data['Theme'] == 'Light Theme']
dark_theme_data = data[data['Theme'] == 'Dark Theme']

figure = go.Figure()

figure.add_trace(go.Histogram(x = light_theme_data['Click Through Rate'], name = 'Light Theme', opacity = 0.6))
figure.add_trace(go.Histogram(x = dark_theme_data['Click Through Rate'], name = 'Dark Theme', opacity = 0.6))

figure.update_layout(
    title_text = 'Click Through Rate by Theme',
    xaxis_title_text = 'Click Through Rate',
    yaxis_title_text = 'Frequency',
    barmode = 'group',
    bargap = 0.1
)

figure.show()

figure.write_html('../output/Click_Through_Rate_by_Theme')