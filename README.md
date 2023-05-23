# Population Dashboard - Version 2

The purpose of this dashboard is to visualize livestock population data from: 
* FAOSTAT 
    * QCL/Stocks dataset
    * GE - FAOTIER 1 dataset
    * GE - UNFCCC dataset
* WOAH
* EuroStat 

## Running the app

* Ensure you have requirements.txt installed 
* Run python index.py 

## Files and editting

### File structure 

```
├─requirements.txt
├─index.py
├─utils/
│ ├─get_data.py
│ └─api_helpers.py
├─README.md
├─layouts/
│ ├─metadata_tab.py
│ ├─map_tab.py
│ ├─layout.py
│ ├─styling.py
│ ├─data_tab.py
│ ├─graph_helpers.py
│ └─graph_tab.py
├─app.py
└─data/
  ├─m_faostat.csv
  ├─m_faotier1.csv
  ├─oie.csv
  ├─m_eurostat.csv
  ├─faostat.csv
  ├─unfccc.csv
  ├─FAOSTAT_mappings.csv
  ├─m_unfccc.csv
  ├─world_map_110m.geojson
  └─eurostat.csv
```

### Tabs 

The contents of each tab is in the layouts/ dir. 