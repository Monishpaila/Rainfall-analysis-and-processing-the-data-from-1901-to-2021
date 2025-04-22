import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Load the data
data = pd.read_csv(r"C:/Users/monis/OneDrive\Desktop/PY PROJECT/excel sheet 1.csv")

# Info of the data set
print("Info of the data set: ",data.info())

# Find missing values

missing_values = data.isnull().sum()
print("Missing values: \n",missing_values)


data.columns = data.columns.str.strip().str.lower()
data = data[data['jun-sep'] != -99.9]

#Obj1

monthly_data = data.melt(id_vars='subdivision', value_vars=['jun', 'jul', 'aug', 'sep'], var_name='Month',  value_name='Rainfall')

monthly_means = monthly_data.groupby(['subdivision', 'Month'])['Rainfall'].mean().reset_index()

g = sns.catplot(data=monthly_means, x='Month', y='Rainfall', hue='Month', col='subdivision', kind='bar', palette='Blues', col_wrap=4, height=4, aspect=0.8, legend=False)
g.set_titles('{col_name}')
g.set_axis_labels('Month', 'Rainfall (mm)')
g.fig.suptitle('Average Monthly Rainfall by Subdivision', y=1.02)
plt.tight_layout()
plt.show()

# Obj 2: Bar graph for the subdivision with the highest average jun-sep rainfall

total_rainfall = data.groupby('subdivision')['jun-sep'].mean()
highest_subdivision = total_rainfall.idxmax()

highest_data = data[data['subdivision'] == highest_subdivision]

highest_monthly = highest_data.melt(id_vars='subdivision', value_vars=['jun', 'jul', 'aug', 'sep'],var_name='Month',value_name='Rainfall')
highest_means = highest_monthly.groupby('Month')['Rainfall'].mean().reset_index()

plt.figure(figsize=(6, 4))
sns.barplot(data=highest_means, x='Month', y='Rainfall', hue='Month', palette='Greens', legend=False)
plt.title(f'Average Monthly Rainfall in {highest_subdivision} (Highest Rainfall)')
plt.xlabel('Month')
plt.ylabel('Rainfall (mm)')
plt.xticks(rotation=0)
plt.tight_layout()
plt.show()

# Obj 3: Bar graph of total rainfall by subdivision
plt.figure(figsize=(12, 6))
sns.barplot(x=total_rainfall.index, y=total_rainfall.values, hue=total_rainfall.index, 
            palette='Oranges', legend=False)
plt.title('Average Total Rainfall by Subdivision (June-September)')
plt.xlabel('Subdivision')
plt.ylabel('Rainfall (mm)')
plt.xticks(rotation=90, ha='right')
plt.tight_layout()
plt.show()

# Obj4:  Heatmap for top two highest rainfall subdivisions

top_two_subdivisions = total_rainfall.nlargest(2).index
top_two_data = data[data['subdivision'].isin(top_two_subdivisions)]
top_two_monthly = top_two_data.melt(id_vars='subdivision', value_vars=['jun', 'jul', 'aug', 'sep'],  var_name='Month', value_name='Rainfall')
top_two_means = top_two_monthly.groupby(['subdivision', 'Month'])['Rainfall'].mean().unstack()
plt.figure(figsize=(8, 4))
sns.heatmap(top_two_means, annot=True, fmt='.1f', cmap='YlGnBu', cbar_kws={'label': 'Rainfall (mm)'})
plt.title('Average Monthly Rainfall for Top Two Subdivisions')
plt.xlabel('Month')
plt.ylabel('Subdivision')
plt.tight_layout()
plt.show()

# Obj  5: Donut chart for the subdivision with the least rainfall

least_subdivision = total_rainfall.idxmin()
least_data = data[data['subdivision'] == least_subdivision]
least_monthly = least_data.melt(id_vars='subdivision', value_vars=['jun', 'jul', 'aug', 'sep'],var_name='Month',value_name='Rainfall')
least_means = least_monthly.groupby('Month')['Rainfall'].mean()
plt.figure(figsize=(6, 6))
plt.pie(least_means, labels=least_means.index, colors=sns.color_palette('Pastel1'),startangle=90, wedgeprops={'width': 0.4})
plt.title(f'Monthly Rainfall Distribution in {least_subdivision} (Least Rainfall)')
plt.gca().add_artist(plt.Circle((0, 0), 0.3, color='white'))
plt.tight_layout()
plt.show()

#Obj 6: Scatter plot for every subdivison fo every 5 years


data.columns = data.columns.str.strip().str.upper().str.replace('_', '-')
clean_data = data[data['JUN-SEP'] != -99.9]
sns.set(style="whitegrid")
g = sns.FacetGrid(clean_data, col="SUBDIVISION", col_wrap=4, height=3, sharex=False, sharey=False)
g.map(plt.scatter, "YEAR", "JUN-SEP", color="blue", alpha=0.6)
g.set_titles("{col_name}")
g.set_axis_labels("Year", "Rainfall (mm)")
g.fig.suptitle("Rainfall (June-September) by Subdivision", y=1.02)
plt.tight_layout()
plt.show()

# Obj 7: The subdivision that is less or greater then ithe mean of the Jun to Sep colum
jun_sep_mean = clean_data["JUN-SEP"].mean()
avg_rainfall = clean_data.groupby('SUBDIVISION')['JUN-SEP'].mean()
heatmap_data = avg_rainfall.reset_index().set_index('SUBDIVISION')
annotations = avg_rainfall. apply(lambda x: 'High' if x > jun_sep_mean else "Low").values.reshape(-1, 1)
plt.figure(figsize=(6, 12))
sns.heatmap(heatmap_data, annot=annotations, fmt='s', # String format for annotations
        cmap= "RdYlGn",
        cbar_kws=('label': 'Rainfall (mm)'),
        linewidths=0.5)
plt.title("Average June-September Rainfall by Subdivision\n(High: Above Mean, Low: Below Mean)")
plt.xlabel('June-September Rainfall')
plt.ylabel('Subdivision')
plt.tight_layout()
Plt.show()

# Print total rainfall for reference
print("Average Total Rainfall by Subdivision (mm):")
print(total_rainfall)
print(f"Subdivision with maximum rainfall: {highest_subdivision}")
