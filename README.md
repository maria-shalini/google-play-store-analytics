# GOOGLE PLAY STORE ANALYTICS
Google Play Store Analytics Dashboard

This project is an interactive analytics dashboard built using Python and Streamlit to analyze Google Play Store applications. The dashboard implements six analytical tasks, each designed with specific business rules, filters, KPIs, and time-based visibility constraints, as part of an internship assessment.

**Tools & Technologies Used**

* Python 3.12
* 
* Streamlit – Dashboard framework
* 
* Pandas – Data cleaning & transformation
* 
* Plotly (Express & Graph Objects) – Interactive visualizations
* 
* Matplotlib – Static visualizations (Task 1)
* 
* Pytz & Datetime – IST time-window control

**Datasets Used**
1. Play Store Data.csv
Raw application metadata (apps, categories, installs, ratings, size, etc.)
2. User Reviews.csv
User sentiment data:
Sentiment
Sentiment polarity
Sentiment subjectivity
3. cleaned_apps.csv (Preprocessed Dataset)
Derived from the above two datasets with:
Cleaned numeric fields (Installs, Reviews, Size_MB)
Parsed dates
Aggregated sentiment metrics:
Avg_Sentiment_Polarity
Avg_Sentiment_Subjectivity
All tasks use cleaned_apps.csv unless explicitly stated.

 **Task 1: Average Rating vs Total Reviews**
(Grouped Bar Chart)

**Objective**

Compare average rating and total reviews for the top 10 app categories by installs.

**Filters Applied**

* Average rating ≥ 4.0
* App size ≥ 10 MB
* Last updated month = January
* Top 10 categories based on total installs

**KPIs Measured**
* Average Rating (per category)
* Total Reviews (per category)

**Visualization**
* Grouped bar chart (dual bars per category)
* Left Y-axis → Average Rating
* Right Y-axis → Total Reviews

**Time Constraint**

Visible only between 3 PM and 5 PM IST

**Task 2: Free vs Paid Apps – Installs & Revenue**
(Dual-Axis Chart)

**Objective**

Compare average installs and average revenue between Free and Paid apps within the top 3 categories.

**Filters Applied**

* Installs ≥ 10,000
* Revenue ≥ $10,000
* Android version > 4.0
* App size ≥ 15 MB
* Content rating = Everyone
* App name length ≤ 30 characters

**KPIs Measured**

* Average Installs
* Average Revenue

**Visualization**

* Dual-axis bar chart
* X-axis → App Type (Free / Paid)

**Interactive filters:**

* App Type
* Category selection
* Revenue axis toggle

**Time Constraint**

* Visible only between 1 PM and 2 PM IST


**Task 3: Global Installs by Category**
(Interactive Choropleth Map)

**Objective**

Visualize global installs across countries by app category.

**Filters Applied**

* Top 5 categories by installs
* Installs > 1 million
* Category must NOT start with: A, C, G, S

**KPIs Measured**
* Total installs per country per category

**Visualization**

* Plotly choropleth map

* Interactive hover and category highlighting

**Time Constraint**

* Visible only between 6 PM and 8 PM IST

**Task 4: Cumulative Installs Over Time
(Stacked Area Chart)**

**Objective**

* Track cumulative installs over time, segmented by category.

**Filters Applied**

* Average rating ≥ 4.2

* Reviews > 1,000

* App size between 20 MB – 80 MB

* App name must NOT contain digits

* Category must start with T or P

* Category Translation: Travel & Local → Voyage et Local (French), Productivity → Productividad (Spanish), Photography → 写真 (Japanese)

**KPIs Measured**

* Monthly installs

* Cumulative installs

* Month-over-month growth %

**Visualization**

* Stacked area chart

* Highlight months where MoM growth > 25%

**Time Constraint**

* Visible only between 4 PM and 6 PM IST

**Task 5: App Size vs Rating
(Bubble Chart)**

**Objective**

* Analyze the relationship between app size, rating, and installs.

**Filters Applied**

* Rating > 3.5

* Installs > 50,000

* Reviews > 500

* App name must NOT contain letter “S”

* Avg sentiment subjectivity > 0.5

**Selected categories:**

* Game, Beauty, Business, Comics, Communication,
* Dating, Entertainment, Social, Events

**Category Translation**

* Beauty → सौंदर्य (Hindi)

* Business → வணிகம் (Tamil)

* Dating → Partnersuche (German)

**Highlighting**

* Game category highlighted in pink

**KPIs Measured**

* App Size (MB)

* Average Rating

* Installs (bubble size)

**Time Constraint**

* Visible only between 5 PM and 7 PM IST

**Task 6: Total Installs Trend Over Time
(Time Series Line Chart)**

**Objective**

* Track total installs over time, segmented by category, highlighting growth surges.

**Filters Applied**

* Reviews > 500

* App name must NOT:
Start with X, Y, Z

* Contain letter “S”

* Category must start with: E, C, or B

* Category Translation: Beauty → सौंदर्य (Hindi), Business → வணிகம் (Tamil), Dating → Partnersuche (German)

**KPIs Measured**

* Monthly total installs

* Month-over-month growth %

**Visualization**

* Multi-line time series chart

* Shaded regions where growth > 20% MoM

* Categories ordered by total installs to reduce legend clutter

**Time Constraint**

* Visible only between 6 PM and 9 PM IST

**Deployment**

* Deployed using Streamlit Community Cloud

* Time-based logic enforced using IST timezone

* All charts hidden outside allowed time windows

**Final Notes**

* All tasks are modularized under dashboard/

* Dataset preprocessing handled separately

* Dashboard is fully interactive and evaluator-ready
