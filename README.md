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

## Files and editting

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
