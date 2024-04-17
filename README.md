# Data Stories Dashboard - Version 2

The purpose of this dashboard is to visualize livestock population/mortality/vaccination data from:

- ETH CSA Livestock Reports
  - Cattle
  - Poultry
  - Sheep
  - Goats
  - Camels
  - Horses
  - Donkeys
  - Mules

## Running the app

- Ensure you have requirements.txt installed: pip3 install -r requirements.txt
- Run python index.py

## Files and editing

### File structure

```
├─requirements.txt
├─index.py
├─utils/
│ ├─newS3TicketLib.py
│ ├─rds_functions.py
│ └─secure_rds.py
├─README.md
├─layouts/
│ ├─metadata_tab.py
│ ├─layout.py
│ ├─styling.py
│ ├─data_tab.py
│ ├─comments_section.py
│ └─graph_tab.py
├─app.py
└─data/
  ├─eth_csa_camels_category.csv
  ├─eth_csa_camels_health.csv
  ├─eth_csa_cattle_category.csv
  ├─eth_csa_cattle_health.csv
  ├─eth_csa_donkeys_category.csv
  ├─eth_csa_donkeys_health.csv
  ├─eth_csa_goats_category.csv
  ├─eth_csa_goats_health.csv
  ├─eth_csa_horses_category.csv
  ├─eth_csa_horses_health.csv
  ├─eth_csa_mules_category.csv
  ├─eth_csa_mules_health.csv
  ├─eth_csa_poultry_category.csv
  ├─eth_csa_poultry_health.csv
  ├─eth_csa_poultry_eggs.csv
  ├─eth_csa_sheep_category.csv
  ├─eth_csa_sheep_health.csv
  ├─eth_regions_csa_cattle_category.csv
  ├─eth_regions_csa_cattle_health.csv
  ├─m_eurostat.csv
  ├─m_faostat.csv
  ├─m_faotier1.csv
  ├─m_oie.csv
  └─m_unfccc.csv
```

### Tabs

The contents of each tab is in the layouts/ dir.

## Comments Section Guide

### Files
Files required for functionality:
```
├─requirements.txt       - Required dependencies
├─index.py               - Contains the callbacks for the comments section
├─utils/
│ ├─newS3TicketLib.py    - To connect to the Amazon services, access comments data
│ ├─rds_functions.py
│ └─secure_rds.py
└─layouts/
  └─comments_section.py  - Contains the dash/HTML/style components of the comments section
```

### How to add comments section to other dashboards
1. Copy the `comments_section.py`, `newS3TicketLib.py`, `rds_functions.py`, `secure_rds.py` files or ensure that the functions are the same.
2. Copy contents of the *"COMMENT CALLBACK"* section [lines 263-366], AWS session establishment [lines 20-23], and appropriate imports from the `index.py` file into the appropriate location in the new dashboard file structure (usually still index.py)
3. Change all the callback input values to match the sidebar *id* values of the new dashboard.

    e.g. *`update_comment_table`*'s callback input value of *"demographic"* should match the appropriate sidebar id for the new dashboard (e.g. *demographic* changed to *choice* in the PopulationDasboardV2 because that's the first sidebar value id). Vice-versa for *animal, table, year*, etc.


5. Change the *"dashboard"* entry in the *querystring* to the new dashboard name (no spaces). The *tablename LIKE* part of the SQL query matches how the tablename is stored in the comment file in the database. Ensure this format matches the string in *update_comment_table* callback function.
6. Ensure dependencies from `requirements.txt` are added to the new dashboard
