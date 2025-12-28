# Airline_Customer_Segmentation_DataMining_Project_Python

This deliver contains all the code, reports, and optional part for the Airline Customer Analysis project.

The needed libraries are the ones used on DM classes (sklearn, matplotlib and seaborn).

For the Optional part1 (Geografical EDA, and Streamlit Dashboard) is importandt to install the libraries: streamlit, plotly, and Geopandas (we recomend doing that by: **conda install -c conda-forge geopandas -y** ).

To see the Dashborda you can acess: https://aiai-dashboard-dm.streamlit.app/
Or run on the command promt were the Dashboard.py is located **python -m streamlit run Dashboard.py**

For the Optional part2 (Autoencoder, and Fuzzy C-means) is importandt to install the libraries: tensorflow, scikit-fuzzy.
---
## Project Overview

This project focuses on the Loyalty Program of a major airline. The goal was to transform raw transactional and demographic data into actionable customer segments. By understanding distinct behavioral patterns, the airline can move away from generic mass marketing and adopt targeted retention and upsell strategies.

The solution utilizes a Multi-View Clustering approach, analyzing customers through separate lenses (Demographic, Value, Behavioral) before integrating them into a final solution.

---
## Repository Structure
To run the code it expect to have a folder structure like this (if not, change the imports and folder paths on the jupyter and py files).

```plaintext
├── .streamlit/     # Streamlit configuration for the deployed app.
├── 1_Delivery/
│   ├── Code/
│   │   ├── .streamlit/     # Streamlit configuration for the deployed app.
│   │   ├── data/           # Dataset files used by the code (given and created).
│   │   ├── Dashboard.py    # Main Streamlit application/dashboard script.
│   │   ├── EDA.ipynb       # Exploratory Data Analysis Jupyter Notebook.
│   │   ├── Geo_EDA.ipynb   # Geographical Exploratory Data Analysis Jupyter Notebook.
│   │   ├── requirements.txt # For streamlit app.
│   │   └── Value_....Demographic.ipynb # EDA Notebook for ValueBased, Demographic and Behavioral features.
│   ├── Group12_EDA_Poster.pdf # Poster of main findings on EDA.
│   ├── Group12_EDA_Report.pdf # Report of EDA.
│   └── README.md           # Part 1Project overview and structure guide.
│
├── data/
│   ├── DM_AIAI_CustomerDB.csv             # Raw customer database.
│   ├── DM_AIAI_FlightsDB.csv              # Raw flight transactions database.
│   ├── DM_AIAI_MasterCustomerDB.csv       # Integrated master dataset.
│   └── DM_AIAI_Metadata.csv               # Metadata and data dictionary.
│
├── Final_delivery/
│   ├── Code/
│   │   ├── behavioral_clusters_month.csv      # Month-based behavioral cluster results.
│   │   ├── behavioral_clusters_year.csv       # Year-based behavioral cluster results.
│   │   ├── behavioral_month.ipynb             # Analysis/clustering for monthly behavior.
│   │   ├── best_encoder_weights.weights.h5    # Trained weights for the autoencoder model.
│   │   ├── demographic_clusters.csv           # Demographic cluster labels/results.
│   │   ├── demographic.ipynb                  # Clustering for demographic features.
│   │   ├── hc_final_label.csv                 # Final cluster labels from hierarchical clustering.
│   │   ├── Merge_Clusters_Advance.ipynb       # Advanced consensus/merging of cluster solutions.
│   │   ├── Merge_Clusters.ipynb               # Primary logic for merging perspective clusters.
│   │   ├── value_based_clusters.csv           # Value-based cluster labels/results.
│   │   ├── Value_Based_Segmentation.ipynb     # EDA and segmentation for value-based features.
│   │   └── yearly_behavior.ipynb              # Analysis/clustering for yearly behavior.
│   ├── data/
│   │   ├── DM_AIAI_MasterCustomerDB.csv       # Integrated master dataset.
│   └── README.md                              # Part2 Project overview and structure guide.
```

---
## Conclusion: Final Cluster Profiles

**Profiling Hierarquical with 18 Clusters using an Autoencoder:**

First, we observe that longitude and latitude lose their significance as they remain almost constant across all clusters, while the other variables used to build the clusters vary significantly depending on the group.

Regarding categorical variables, most clusters do not change much; only one or two clusters show behavioral shifts in variables such as Province or State, City, Education, and Marital Status.

Here is the profiling for each cluster:

+ **The October Loyals (956):** Medium income, low revenue, long tenure. They have not purchased recently but remain a consistent, engaged group over the years. These are "October people" who accumulate points year-round to use in October when they fly less but with companions.

+ **The Pandemic Drop-offs (209):** Medium income, low revenue, moderate tenure. These are lost customers who were active in 2019 and 2020 but stopped almost completely in 2021. They previously traveled with consistent frequency and distance each month.

+ **The September Loyals (2706):** Medium income, low revenue, long tenure. Loyal, very engaged customers who purchased recently. "September people" who save points all year to use in September for flights with companions.

+ **The January Average (1045):** Medium income, low revenue, long tenure. Recently active and traveling more now than before (highly engaged). "January people" who use accumulated points for companion travel in January.

+ **The Summer-Fall Hybrids (613):** Medium income, medium revenue, moderate tenure. Recently active and showing increased engagement. "July people" who travel with companions in July and tend to travel alone in autumn.

+ **The May Planners (1078):** Medium income, medium revenue, moderate tenure. Recently active and now very engaged. "May people" who accumulate points to use during May for companion travel.

+ **The Lost Holiday Drifters (565):** Low income, low revenue, short tenure. Lost customers who were never highly engaged; they use points and tend to travel more with companions in December.

+ **The Autumn Budget (178):** Low income, low revenue, short tenure. Recently active and becoming more engaged, specifically during the autumn months.

+ **The June Loyals (897):** Medium income, medium revenue, long tenure. Very engaged, loyal customers. "June people" who save points all year for companion travel in June.

+ **Holiday Travelers (66):** Medium income, low revenue, short tenure. Recently active and increasing engagement. They travel with companions in February and June, using points in most months except November and December (when they travel the most).

+ **The November Loyals (1029):** Medium income, medium revenue, long tenure. Consistent, engaged group. "November people" who redeem points for companion travel in November.

+ **The Dormant Browsers (517):** Low income, low revenue, moderate tenure. Have not purchased recently but show some new engagement; they travel consistently but infrequently across all months and use points.

+ **The March Loyals (1126):** Medium income, medium revenue, long tenure. Consistent, engaged group. "March people" who accumulate points for companion travel in March.

+ **VIPs (64):** High income, high revenue, short tenure. Recently active and engaged. They travel in June with companions and are frequent autumn travelers, using points throughout the year except in Q4. Almost 100% Bachelors, that are Divorced or Married, with the more proportion of mens (~65%).

+ **The Q4 Boomerang (691):** Medium income, low revenue, short tenure. Re-engaged customers who are now moderately active, particularly in autumn and December with companions.

+ **The December Loyals (949):** Medium income, medium revenue, long tenure. Very engaged, loyal customers. "December people" who redeem points for companion travel in December.

+ **The February Loyals (992):** Medium income, low revenue, long tenure. Very engaged, loyal customers. "February people" who save points for companion travel in February.

+ **New travelers (2891):** Medium income, medium revenue, very short tenure (newest). Re-engaged, moderately active customers who use points and travel primarily in autumn.

We also concluded that the top 15 features that contributed the most to improve the gini on our model were:
+ Total Distance on 2020 (contribution of 13%).
+ % Flights with companions month 12 (contribution of ~11%).
+ % Flights with companions month 11 (contribution of ~6%).
+ % Flights with companions month 3 (contribution of ~5.5%).
+ % Flights with companions month 5 (contribution of ~5%).
+ Total distance (contribution of ~5%).
+ % Flights with companions month 1 (contribution of ~5%).
+ % Flights with companions month 2 (contribution of ~5%).
+ % Flights with companions month 6 (contribution of ~5%).
+ % Flights with companions month 10 (contribution of ~5%).
+ % Flights with companions month 7 (contribution of ~4.5%).
+ Recency (contribution of ~3.5%).
+ % Flights with companions month 9 (contribution of ~3%).
+ Total NumFlights (contribution of ~2.5%).
+ Total Distance month 3 (contribution of ~1.5%).

In conclusion, we can determine that our clusters are defined by three key dimensions: monthly patterns (seasonal travel), yearly perspectives (long-term loyalty and tenure), and the general behavioral characteristics of the customer, such as recency and engagement levels.