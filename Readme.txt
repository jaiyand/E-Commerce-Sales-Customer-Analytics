E-Commerce Sales \& Customer Analytics



1\. Project Overview



This project analyzes Brazilian e-commerce data to understand sales performance, customer behaviour, product performance, and delivery efficiency.



I used \*\*Python\*\* for data cleaning and exploratory data analysis, \*\*MySQL\*\* for storing and querying the data, and \*\*Power BI\*\* to create an interactive dashboard.



2\. Tools and Technologies



\- Python: Data cleaning, validation, and exploratory data analysis

\- Pandas: Data manipulation and preparation

\- MySQL: Database management and SQL analysis

\- Power BI: Interactive dashboard and visualizations

\- DAX: KPI calculations and measures



3\. Dataset Summary



The project uses the Brazilian Olist e-commerce dataset.



| Metric |          |Records |



| Orders            | 99,441 |

| Unique Customers  | 96,096 |

| Order Items       | 112,650|

| Products          | 32,951 |

| Sellers           | 3,095  |



4\. Key Business Insights



1\. Sales Performance



\- Total gross item value was approximately \*\*15.84 million Brazilian reais (BRL)\*\* in the dataset's currency.

\- Average order value was approximately \*\*160.58 BRL\*\*.

\- These metrics help measure overall sales performance and the average value generated per order.



2\. Customer Behaviour



\- The dataset contains \*\*96,096 unique customers\*\*.

\- Approximately \*\*93,099 customers\*\* placed only one order.

\- Only \*\*2,997 customers\*\* placed repeat orders.

\- The repeat customer rate was approximately \*\*3.12%\*\*.



\*\*Insight:\*\* Repeat purchasing was relatively low, suggesting an opportunity to improve customer retention through loyalty programs, targeted offers, and better customer engagement.



3\. Order Fulfilment



\- \*\*96,478 orders\*\* were marked as delivered.

\- Other orders included shipped, canceled, unavailable, invoiced, and processing statuses.



\*\*Insight:\*\* Monitoring order statuses helps identify fulfilment issues and understand how many orders successfully reach customers.



4\. Product and Category Performance



\- The dataset contains \*\*32,951 products\*\*.

\- The dashboard compares product categories by gross item value.

\- The Top 10 category chart helps identify categories contributing the most sales value.



\*\*Insight:\*\* High-performing categories can be prioritized for inventory planning and marketing. The actual leading categories should be identified from the final chart results.



5\. Customer Geographic Analysis



\- The dashboard compares customer counts across Brazilian states.

\- The Top 10 states chart highlights the locations with the largest customer bases.



\*\*Insight:\*\* Businesses can use geographic patterns to focus marketing campaigns and plan regional expansion.



6\. Monthly Sales Trends



\- Monthly revenue and order counts help track changes in business activity over time.

\- The Year slicer allows users to compare performance across different years.



\*\*Insight:\*\* Monthly trends help identify stronger and weaker periods and support sales planning.



7\. Delivery Performance



\- The dashboard includes average delivery time and average delivery delay.

\- Delivery delay is calculated by comparing the actual delivery date with the estimated delivery date.



\*\*Insight:\*\* Delivery metrics help evaluate fulfilment efficiency and identify opportunities to improve customer experience.



\*\*Note:\*\* The average delivery delay calculation should be validated before reporting a final numerical conclusion.



5\. Data Cleaning and Validation



\- Cleaned the main datasets using Python and Pandas.

\- Handled missing values and prepared date columns.

\- Validated row counts and relationships between datasets.

\- Checked referential integrity between customers, orders, products, and order items.

\- Imported the cleaned data into MySQL for analysis.



6\. Power BI Dashboard



The report contains two pages:



Page 1: Sales Overview

\- Total Revenue

\- Total Orders

\- Total Customers

\- Total Products

\- Total Items Sold

\- Monthly Revenue Trend

\- Top 10 Product Categories by Revenue

\- Order Year slicer



Page 2: Customer \& Operations Analysis

\- Customers by State

\- Order Status Distribution

\- Monthly Orders Trend

\- Average Delivery Delay



7\. Conclusion



This project demonstrates how data cleaning, SQL analysis, and business intelligence tools can be combined to turn raw e-commerce data into useful business insights.



It highlights sales performance, customer retention, product categories, geographic distribution, and order fulfilment. These findings can help businesses make more informed decisions.


8\. Future Improvements



\- Analyze repeat customer behaviour in greater detail.

\- Add seller-level performance comparisons.

\- Investigate late deliveries and their possible causes.

\- Improve the dashboard with additional filters and drill-through pages.

\- Automate the data refresh process.

