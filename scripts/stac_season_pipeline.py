import pandas as pd
import ast
import os

# 🌍 Step 1: Load merged imagery dataset
merged_csv = 'merged_all_with_label_stac.csv'

if not os.path.exists(merged_csv):
    raise FileNotFoundError(f"❌ File not found: '{merged_csv}'")

merged_df = pd.read_csv(merged_csv)
print(f"✅ Loaded {len(merged_df):,} records from '{merged_csv}'")

# 🔍 Step 2: Specify correct STAC metadata column
props_col = 'properties_y'
if props_col not in merged_df.columns:
    raise KeyError(f"❌ Column '{props_col}' not found in CSV.")

# 🧠 Step 3: Define safe parser
def safe_eval(x):
    try:
        return ast.literal_eval(x)
    except Exception:
        return None

# 📦 Step 4: Apply parser and flatten JSON metadata
parsed_props = merged_df[props_col].dropna().astype(str).apply(safe_eval)
valid_props = parsed_props.dropna()
flat_props = pd.json_normalize(valid_props)

if flat_props.empty:
    print("🚫 No valid STAC metadata to unpack from 'properties_y'")
else:
    merged_df.loc[flat_props.index, flat_props.columns] = flat_props
    print(f"📦 Extracted STAC fields: {', '.join(flat_props.columns)}")

# 🌦️ Step 5: Define seasonal labeling function
def tag_season(dt_str):
    try:
        month = pd.to_datetime(dt_str, errors='coerce').month
        if month in [3, 4, 5]:
            return 'Long Rains'
        elif month in [9, 10, 11]:
            return 'Short Rains'
        elif month in [6, 7, 8]:
            return 'Cold/Dry Spell'
        elif month in [12, 1, 2]:
            return 'Hot/Dry Spell'
        else:
            return 'Unknown'
    except:
        return 'Invalid Date'

# ✅ Step 6: Apply seasonal tags
if 'datetime' in merged_df.columns:
    merged_df['season'] = merged_df['datetime'].apply(tag_season)
    print("🌦️ Season tags applied.")
else:
    print("🚫 'datetime' column missing — tagging skipped.")
    merged_df['season'] = 'Unlabeled'
