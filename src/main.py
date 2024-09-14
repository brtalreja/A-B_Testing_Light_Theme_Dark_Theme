#Import Required Libraries
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from statsmodels.stats.proportion import proportions_ztest
from scipy import stats
from scipy.stats import chi2_contingency

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
# The relationship between Scroll_Depth and Session_Duration suggests that engaging content is able to keep users on the site longer.
# As there is a moderate correlation between Click Through Rate and Conversion Rate variables, there is potential to increase conversions by improving the post-click experience for a user.
# We can look into analyzing the pages a user lands on after clicking through and optimize them to better align with the user’s intent and streamline the conversion process.

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
# The linear trendline is almost flat, suggesting a weak or no strong correlation between CTR and Conversion Rate. This indicates that higher click-through rates do not necessarily lead to higher conversion rates.
# The linear regression line is relatively flat, which means that overall, there is no clear upward or downward trend linking CTR to Conversion Rate. 
# This analysis emphasizes that while CTR is an important metric, it may not be the sole determinant of conversion success, and other factors should be examined for a more holistic view of user behavior.

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
# Both themes have similar distributions across most CTR ranges, with no extreme deviation for either theme, indicating that users interact similarly with both themes in terms of click behavior.
# The histogram shows that no theme significantly outperforms the other across all CTR ranges, suggesting that the choice of theme (Light vs. Dark) does not have a considerable impact on overall CTR behavior.
# Since both themes perform similarly, it's crucial to look beyond just the theme to identify other variables contributing to better CTR performance.

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
# Both themes seem to perform fairly similarly in most conversion rate ranges, with slight variations between them.
# While the Dark Theme has a slight advantage in lower conversion rates, the Light Theme appears to be performing better overall at the higher conversion rates.
# Since the Light Theme performs slightly better at higher conversion rates, a focused approach on enhancing user experience for Dark Theme users at these higher levels should be considered.

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

bins = [18, 25, 35, 45, 55, 65, 100]
labels = ['19-25', '26-35', '36-45', '46-55', '56-65', '66-100']
data_num['Age_Group'] = pd.cut(data_num['Age'], bins = bins, labels = labels, right = False)

age_data = data_num.groupby('Age_Group').mean()

figure = px.bar(age_data, x = age_data.index, y = 'Conversion Rate', title = 'Conversion Rate by Age Group')
figure.show()
figure.write_image('../output/Conversion_rate_by_Age_Group.png')

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

#Chi-Square test
contingency_table = pd.crosstab(data['Purchases'], data['Theme'])
chi2, p, dof, expected = chi2_contingency(contingency_table)
print('Chi-square test for Purchases vs Theme - chi2:', chi2, 'p-value:', p)

#COMMENT: