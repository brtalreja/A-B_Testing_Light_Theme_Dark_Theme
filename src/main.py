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

#Correlation matrix
data['Theme_num'] = data['Theme'].map({'Light Theme': 0, 'Dark Theme':1})
data['Location_num'] = data['Location'].map({'Bangalore': 1,'Chennai': 2, 'Kolkata': 3, 'New Delhi': 4, 'Pune':5})
data['Purchases_num'] = data['Purchases'].map({'No': 0, 'Yes':1})
data['Added_to_Cart_num'] = data['Added_to_Cart'].map({'No': 0, 'Yes':1})

data_num = data[['Theme_num','Click Through Rate','Conversion Rate','Bounce Rate','Scroll_Depth','Age','Location_num','Session_Duration','Purchases_num','Added_to_Cart_num']]

correlation_matrix = data_num.corr()
figure = px.imshow(correlation_matrix, 
                   title="Correlation Matrix", 
                   labels=dict(color="Correlation"))

figure.show()

figure.write_image('../output/Correlation_Matrix.png')

#COMMENT:

#Outlier detection using Z-Scores
z_scores = stats.zscore(data[['Bounce Rate', 'Session_Duration', 'Scroll_Depth']])
outliers = (abs(z_scores) > 3).sum(axis=0)
print("Number of Outliers per Feature:", outliers)

#Click Through Rate vs Conversion Rate
figure = px.scatter(data,
                    x = 'Click Through Rate',
                    y = 'Conversion Rate',
                    color = 'Theme',
                    title = 'Click Through Rate vs. Conversion Rate',
                    trendline = 'ols')

figure.show()

figure.write_image('../output/Click_through_rate_vs_Conversion_rate.png')

#COMMENTS:

#Click Through Rate Histogram
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

figure.write_image('../output/Click_Through_Rate_by_Theme.png')

#COMMENTS:

#Conversion Rate Histogram
figure = go.Figure()

figure.add_trace(go.Histogram(x=light_theme_data['Conversion Rate'], name='Light Theme', opacity=0.6, nbinsx=20))
figure.add_trace(go.Histogram(x=dark_theme_data['Conversion Rate'], name='Dark Theme', opacity=0.6, nbinsx=20))

figure.update_layout(
    title_text='Conversion Rate by Theme',
    xaxis_title_text='Conversion Rate',
    yaxis_title_text='Frequency',
    barmode='group',
    bargap=0.1
)

figure.show()

figure.write_image('../output/Conversion_Rate_by_Theme.png')

#COMMENT:

#Bounce Rate
figure = go.Figure()
figure.add_trace(go.Box(y=light_theme_data['Bounce Rate'], name='Light Theme'))
figure.add_trace(go.Box(y=dark_theme_data['Bounce Rate'], name='Dark Theme'))

figure.update_layout(
    title_text='Bounce Rate by Theme',
    yaxis_title_text='Bounce Rate',
)

figure.show()

figure.write_image('../output/Bounce_Rate_by_Theme.png')

#COMMENT:

#Scroll Depth Rate
figure = go.Figure()
figure.add_trace(go.Box(y=light_theme_data['Scroll_Depth'], name='Light Theme'))
figure.add_trace(go.Box(y=dark_theme_data['Scroll_Depth'], name='Dark Theme'))

figure.update_layout(
    title_text='Scroll Depth by Theme',
    yaxis_title_text='Scroll Depth',
)

figure.show()

figure.write_image('../output/Scroll_Depth_Rate_by_Theme.png')

#Segmented Analysis
age_data = data.groupby('Age').mean()
location_data = data.groupby('Location_num').mean()

figure = px.bar(age_data, x = age_data.index, y = 'Conversion Rate', title = 'Conversion Rate by Age Group')
figure.show()
figure.write_image('../output/Conversion_rate_by_Age_Group.png')

figure = px.bar(location_data, x = location_data.index, y = 'Purchases_num', title = 'Purchases by Location Group')
figure.show()
figure.write_image('../output/Purchases_by_Location_Group.png')


#COMMENT:

#A/B testing for Purchases
light_theme_conversions = light_theme_data[light_theme_data['Purchases'] == 'Yes'].shape[0]
light_theme_total = light_theme_data.shape[0]

dark_theme_conversions = dark_theme_data[dark_theme_data['Purchases'] == 'Yes'].shape[0]
dark_theme_total = dark_theme_data.shape[0]

conversion_counts = [light_theme_conversions, dark_theme_conversions]
sample_sizes = [light_theme_total, dark_theme_total]

light_theme_conversion_rate = light_theme_conversions / light_theme_total
dark_theme_conversion_rate = dark_theme_conversions / dark_theme_total

#Perform two-sample proportion test
zstat, pval = proportions_ztest(conversion_counts, sample_sizes)
print("Light Theme Conversion Rate:", light_theme_conversion_rate)
print("Dark Theme Conversion Rate:", dark_theme_conversion_rate)
print("A/B Testing - z-statistic:", zstat, " p-value:", pval)

#COMMENT:

#A/B testing for Session Duration
light_theme_session_duration = light_theme_data['Session_Duration']
dark_theme_session_duration = dark_theme_data['Session_Duration']

# Calculate the average session duration for both themes
light_theme_avg_duration = light_theme_session_duration.mean()
dark_theme_avg_duration = dark_theme_session_duration.mean()

# Print the average session duration for both themes
print("Light Theme Average Session Duration:", light_theme_avg_duration)
print("Dark Theme Average Session Duration:", dark_theme_avg_duration)

# Perform two-sample t-test for session duration
tstat, pval = stats.ttest_ind(light_theme_session_duration, dark_theme_session_duration)
print("A/B Testing for Session Duration - t-statistic:", tstat, " p-value:", pval)

#COMMENT: