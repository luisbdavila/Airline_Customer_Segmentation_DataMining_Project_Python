# Airline_Customer_Segmentation_DataMining_Project_Python

This deliver contains all the code, reports, and optional part for the Airline Customer Analysis project 2Deliver.

The needed libraries are the ones used on DM classes (sklearn, matplotlib and seaborn).

For the Optional part (Autoencoder, and Fuzzy C-means) is importandt to install the libraries: tensorflow, scikit-fuzzy.

---

To run the code it expect to have a folder structure like this (if not, change the imports and folder paths on the jupyter).

```plaintext
Final_delivery/
├── Code/
│   ├── behavioral_clusters_month.csv      # Month-based behavioral cluster results.
│   ├── behavioral_clusters_year.csv       # Year-based behavioral cluster results.
│   ├── behavioral_month.ipynb             # Analysis/clustering for monthly behavior.
│   ├── best_encoder_weights.weights.h5    # Trained weights for the autoencoder model.
│   ├── demographic_clusters.csv           # Demographic cluster labels/results.
│   ├── demographic.ipynb                  # Clustering for demographic features.
│   ├── hc_final_label.csv                 # Final cluster labels from hierarchical clustering.
│   ├── Merge_Clusters_Advance.ipynb       # Advanced consensus/merging of cluster solutions.
│   ├── Merge_Clusters.ipynb               # Primary logic for merging perspective clusters.
│   ├── value_based_clusters.csv           # Value-based cluster labels/results.
│   ├── Value_Based_Segmentation.ipynb     # EDA and segmentation for value-based features.
│   └── yearly_behavior.ipynb              # Analysis/clustering for yearly behavior.
├── data/
│   ├── DM_AIAI_MasterCustomerDB.csv       # Integrated master dataset.
└── README.md                              # Project overview and structure guide.
```