from preswald import (
    text,
    plotly,
    connect,
    get_df,
    table,
    query,
    slider,
    selectbox,
    checkbox,
    text_input,
    sidebar
)
import plotly.express as px

sidebar(defaultopen=True)

# -------------------------
# 1) Welcome text and app title
# -------------------------
text("# My Data Analysis App")
text("Here you can visualize and interactively explore Video Game Sales data from Kaggle.")

# -------------------------
# 2) Initialize connection and load data
# -------------------------
connect()
df = get_df("vgsales_csv")

# -------------------------
# 3) SQL query example (based on Global_Sales)
#    Filter example for Global_Sales > 10
# -------------------------
sql = "SELECT * FROM vgsales_csv WHERE Global_Sales > 10"
filtered_df = query(sql, "vgsales_csv")

text("## Data filtered by SQL query (Global_Sales > 10)")
table(filtered_df, title="Filtered Data")

# -------------------------
# 4) Dynamic threshold filtering (Slider control, based on Global_Sales)
# -------------------------
text("## Dynamic Threshold Filtering View")
threshold = slider("Threshold (Global_Sales)", min_val=0, max_val=100, default=10)
table(df[df["Global_Sales"] > threshold], title="Dynamic Data View")

# -------------------------
# 5) Selection controls and text input example
#    - Assuming data has "Platform" column
#    - Assuming data has "Name" column for keyword search
# -------------------------
text("## Selection Controls and Text Input Example")

if "Platform" in df.columns:
    unique_platforms = df["Platform"].unique().tolist()
else:
    unique_platforms = []

selected_platform = selectbox(
    "Select Platform (if 'Platform' column exists in data)",
    options=unique_platforms,
    default=unique_platforms[0] if unique_platforms else None
)

keyword = text_input("Game name keyword (if 'Name' column exists in data)")

sub_df = df.copy()
if "Platform" in sub_df.columns and selected_platform:
    sub_df = sub_df[sub_df["Platform"] == selected_platform]

if "Name" in sub_df.columns and keyword:
    sub_df = sub_df[sub_df["Name"].str.contains(keyword, case=False, na=False)]

text("### Filtered Data")
table(sub_df, title="Selected Data")

# -------------------------
# 6) Additional example: Checkbox toggle (show only games with Global_Sales>10)
# -------------------------
text("## Show only data with Global_Sales>10?")
use_filtered = checkbox("Enable filtering (Global_Sales>10)?", default=False)

if use_filtered:
    display_df = sub_df[sub_df["Global_Sales"] > 10]
else:
    display_df = sub_df

table(display_df, title="Data based on checkbox selection")

# -------------------------
# 7) Data visualization (Scatter Plot)
#    - Example showing Global_Sales vs NA_Sales as scatter plot coordinates
#    - Color differentiated by Platform
# -------------------------
text("## Data Visualization (Scatter Plot)")

required_cols = {"Global_Sales", "NA_Sales", "Platform"}
if required_cols.issubset(display_df.columns):
    fig = px.scatter(
        display_df,
        x="Global_Sales",
        y="NA_Sales",
        color="Platform",
        title="Global Sales vs NA Sales by Platform",
        labels={"Global_Sales": "Global Sales (Millions)", "NA_Sales": "NA Sales (Millions)"}
    )
    plotly(fig)
else:
    text("Cannot create scatter plot. Please verify column names match the dataset: 'Global_Sales', 'NA_Sales', and 'Platform' columns are required.")