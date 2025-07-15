import pandas as pd

# Load the CSVs
labels_df = pd.read_csv('merged_labels.csv')
stac_df = pd.read_csv('merged_stac.csv')
metadata_df = pd.read_csv('merged_metadata.csv')
catalog_df = pd.read_csv('image_catalog.csv')

# Preview basic info
for name, df in zip(['Labels', 'STAC', 'Metadata', 'Catalog'], [labels_df, stac_df, metadata_df, catalog_df]):
    print(f"\n--- {name} ---")
    print("Shape:", df.shape)
    print("Columns:", df.columns.tolist())
    print(df.head(2))
