
# 🧾 Crime Risk Clustering and Prediction

Author: AJ Diakite  
Course: ICSI 431  
Project: Final Individual Project Report  
Goal: Use clustering and classification to analyze and predict violent crime risk levels across U.S. counties based on FBI crime breakdowns.

---

## 🔍 Overview

This project uses real FBI crime breakdown data (2020–2025) to analyze county-level patterns in violent crime. It uses:

- K-Means clustering to group similar counties by crime totals  
- Random Forest classification to predict crime risk level using engineered features  
- Custom scripts to clean, organize, and analyze public data from multiple sources  

The goal was to understand not just how much crime happens, but what kind of crime, who commits it, where it happens , and how it’s carried out.

---

## 🗂️ Project Structure

```
CrimeDataMaps/
├── data/usa/                         # Cleaned and organized FBI data per county
├── output/                           # Visual outputs (PCA, bar plots, heatmaps)
├── scripts/                          # All project Python scripts
│   ├── clean_fbi_data.py             # Cleans raw .csvs
│   ├── fix_headers.py                # Standardizes header format
│   ├── organize_fbi_files.py         # Sorts files by county/crime type
│   ├── build_county_summary.py       # Creates total violent crime summary
│   ├── build_extended_features.py    # Creates normalized categorical features
│   ├── analyze_county.py             # Generates per-county bar plots
│   ├── fbi_visuals.py                # Compares FL and CA crime breakdowns
│   ├── kmeans_clustering.py          # Runs K-Means + PCA + heatmap
│   └── visualize_model_outputs.py    # Random Forest model + evaluation visuals
```

---

## 🧪 How to Run

1. **Clean and organize data**  
```bash
python3 scripts/clean_fbi_data.py  
python3 scripts/fix_headers.py  
python3 scripts/organize_fbi_files.py  
```

2. **Build features**  
```bash
python3 scripts/build_county_summary.py  
python3 scripts/build_extended_features.py  
```

3. **Generate visuals and clustering**  
```bash
python3 scripts/analyze_county.py  
python3 scripts/fbi_visuals.py  
python3 scripts/kmeans_clustering.py  
```

4. **Run classification model**  
```bash
python3 scripts/visualize_model_outputs.py  
```

---

## 📊 Outputs

- `output/plots/`: PCA cluster plot, cluster heatmap, bar plots per county  
- `output/predictions/`: Feature importance + confusion matrix images  
- `data/usa/*.csv`: Final datasets used for training and clustering

---

## 📚 Dependencies

- Python 3.10  
- `pandas`, `numpy`  
- `matplotlib`, `seaborn`  
- `scikit-learn`  
- `adjustText` (for PCA label cleanup)



```bash


---

## 📎 References

- FBI UCR Data Explorer: https://cde.ucr.cjis.gov  
- scikit-learn Documentation: https://scikit-learn.org  
- matplotlib: https://matplotlib.org  
- seaborn: https://seaborn.pydata.org  
