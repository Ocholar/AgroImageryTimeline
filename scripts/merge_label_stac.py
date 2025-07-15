import pandas as pd

# Load base imagery catalog
base_df = pd.read_csv('merged_all.csv')

# Load label-side STAC metadata
label_stac_df = pd.read_csv('merged_stac_label.csv')

# Create ImgID from STAC 'id' suffix
label_stac_df['ImgID'] = label_stac_df['id'].apply(lambda x: f"id_{x[-8:]}" if pd.notnull(x) else None)

# Cast 'properties' to string for safe CSV storage
label_stac_df['properties'] = label_stac_df['properties'].apply(lambda x: str(x) if pd.notnull(x) else '')

# Merge into base imagery
merged_df = base_df.merge(label_stac_df[['ImgID', 'properties']], on='ImgID', how='left')

# Save enriched dataset
merged_df.to_csv('merged_all_with_label_stac.csv', index=False)

print("✅ Label-side STAC metadata merged into imagery catalog.")
print("📦 Saved as: 'merged_all_with_label_stac.csv'")
