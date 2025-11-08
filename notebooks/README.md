<!-- ** 
Import main libraries:
pandas for data handling, numpy for calculations, matplotlib/seaborn for visualizations, and scipy.stats for statistical tests and outlier detection.
** -->

<!-- ** 
RAW_PATH defines where the raw data is stored.
parse_dates converts 'Timestamp' into datetime for time analysis.
set_index('Timestamp') makes time-based operations easier.
df.head() previews the first few rows to check structure and data quality.
** -->

<!-- ** 
describe() gives quick numeric summaries.
Check missing values and flag columns with over 5% nulls for cleaning attention.
** -->

<!-- ** 
Compute z-scores to detect outliers (|z| > 3) in numeric columns.
These highlight unusual or extreme sensor readings.
** -->

<!-- ** 
Fill missing or outlier values with the median to keep dataset consistent.
Save the cleaned data in data/ folder (excluded in .gitignore).
** -->

<!-- ** 
Plot GHI, DNI, DHI, and Tamb over time to observe daily or seasonal trends and detect anomalies.
 ** -->

<!-- ** 
Compare ModA and ModB before vs. after cleaning to evaluate cleaning effect on performance.
** -->

<!-- ** 
Use histograms to see variable distribution and wind rose plots to analyze wind direction and speed.
** -->

<!-- ** 
Study how humidity (RH) affects temperature (Tamb) and irradiance (GHI) using scatter plots.
** -->

<!-- ** 
Create a bubble chart (GHI vs Tamb with bubble size = RH or BP) to show interaction between variables.
** -->
