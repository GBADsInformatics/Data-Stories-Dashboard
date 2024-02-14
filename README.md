# Population Dashboard - Version 2

The purpose of this dashboard is to visualize livestock population data from:

- FAOSTAT
  - QCL/Stocks dataset
  - GE - FAOTIER 1 dataset
  - GE - UNFCCC dataset
- WOAH
- EuroStat

## Running the app

- Ensure you have requirements.txt installed: pip3 install -r requirements.txt
- Run python index.py

## Files and editting

### File structure

```
├─requirements.txt
├─index.py
├─utils/
│ ├─get_data.py (to be deleted)
│ ├─newS3TicketLib.py
│ ├─rds_functions.py
│ ├─secure_rds.py
│ └─api_helpers.py (to be deleted)
├─README.md
├─layouts/
│ ├─metadata_tab.py
│ ├─layout.py
│ ├─styling.py
│ ├─data_tab.py
│ └─graph_tab.py
├─app.py
└─data/
  ├─m_faostat.csv
  ├─m_faotier1.csv
  ├─m_eurostat.csv
  ├─m_unfccc.csv
  └─M_oie.csv
```

### Tabs

The contents of each tab is in the layouts/ dir.
