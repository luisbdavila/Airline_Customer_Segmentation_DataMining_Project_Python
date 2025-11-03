# Airline_Customer_Segmentation_DataMining_Project_Python

Contains the complete implementation of the Cars4You machine learning pipeline project. An end-to-end workflow — from data preprocessing to model evaluation.

The needed libraries are the ones used on DM classes.

For the Optional part (Geografical EDA, and Streamlit Dashboard) is importandt to install the libraries: streamlit, plotly, and Geopandas (we recomend doing that by: **conda install -c conda-forge geopandas -y**)

To see the Dashborda you can acess: https://aiai-dashboard-dm.streamlit.app/
Or run on the command promt were the Dashboard.py is located **python -m streamlit run 
Dashboard.py**

This contains all the code and structure for the Airline Customer Analysis project part1.

---

To run the code it expect to have a folder structure like this (if not, change the imports and folder paths on the jupyter and py files).

```plaintext
Group 12/
├── .streamlit/     # Streamlit configuration for the deployed app.
├── data/           # Dataset files used by the code (given and created).
├── Dashboard.py    # Main Streamlit application/dashboard script.
├── EDA.ipynb       # Exploratory Data Analysis Jupyter Notebook.
├── Geo_EDA.ipynb   # Geographical Exploratory Data Analysis Jupyter Notebook.
└── Value_....Demographic.ipynb # EDA Notebook for ValueBased, Demographic and Behavioral features.
```