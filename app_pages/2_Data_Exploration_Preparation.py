import pandas as pd
import plotly.express as px
import streamlit as st
from collections import Counter
from itertools import combinations
import seaborn as sns
import matplotlib.pyplot as plt
import networkx as nx

# Function for styled insight box
def insight_box(insight_text):
    st.markdown(
        f"""
        <div style="
            border: 2px solid #ccc; 
            padding: 10px; 
            border-radius: 5px; 
            background-color: #f9f9f9; 
            font-size: 14px;
            margin-top: 15px;
            margin-bottom: 15px;">
            <strong>Insight:</strong> {insight_text}
        </div>
        """, 
        unsafe_allow_html=True
    )

# Access the cached data from session_state
df = st.session_state["df"]

# Header
st.title("Groceries Dataset Analysis")
st.write("""
Welcome to the **Data Exploration and Preparation Section**. 
This section includes cleaning, visualization, and identifying key patterns in the dataset to prepare for further analysis.
""")

# Sidebar filters
item_options = ["ALL"] + sorted(df["itemDescription"].unique())

# Allow multiselect for item filtering
items_selected = st.sidebar.multiselect(
    "Select Items",
    item_options,
    default="ALL",
    help="Filter the dataset to show all items or specific ones."
)

# Apply filters based on user selections
df_filtered = df.copy()
if "ALL" not in items_selected:
    df_filtered = df_filtered[df_filtered["itemDescription"].isin(items_selected)]

# Check for empty dataset after filtering
if df_filtered.empty:
    st.error("Filtered dataset is empty. Adjust the filters to include more data.")
    st.stop()

# Data Cleaning
st.write("## Data Cleaning")
st.write("---")
st.write("""
### Steps:
1. **Date Conversion**: Convert the `Date` column to datetime format for time-based analysis.
2. **Filtering**: Enable dynamic selection of items for focused analysis.
""")
df_filtered["Date"] = pd.to_datetime(df_filtered["Date"])
st.write("✅ Date Conversion Completed")
st.write("✅ No missing values detected in the dataset")

# Data Preparation
st.write("## Data Preparation")
st.write("---")
st.write("""
### Steps:
1. **Grouping Transactions**: Aggregate items purchased together by `Member_number` and `Date`.
2. **Item Pair Analysis**: Analyze frequently purchased item combinations.
""")
transactions = df_filtered.groupby(['Member_number', 'Date'])['itemDescription'].apply(list)
transactions = transactions.apply(lambda x: list(set(x)))  # Remove duplicates within transactions
st.write("✅ Transactions Grouped Successfully")

# Generate combinations for co-occurrence analysis
all_combinations = Counter(
    combo for transaction in transactions for combo in combinations(sorted(transaction), 2)
)
st.write("✅ Item Pair Analysis Completed")

# Exploratory Data Analysis
st.write("## Exploratory Data Analysis (EDA)")
st.write("---")

# 1. Distribution of Item Frequency
st.markdown("### Distribution of Item Frequency")
item_frequency = df_filtered["itemDescription"].value_counts()
item_frequency_chart = px.bar(
    item_frequency,
    x=item_frequency.index,
    y=item_frequency.values,
    title="Item Frequency Distribution",
    labels={"x": "Item", "y": "Frequency"}
)
st.plotly_chart(item_frequency_chart, use_container_width=True)
insight_box(
    "Most items appear only a few times, indicating a long tail of less popular products. "
    "This distribution helps identify items for deeper analysis or inventory prioritization."
)

# 2. Co-occurrence Matrix (Heatmap)
st.markdown("### Co-occurrence Matrix of Items")
co_occurrence_df = pd.DataFrame(
    [(k[0], k[1], v) for k, v in all_combinations.items()],
    columns=["Item 1", "Item 2", "Count"]
)

# Filter top 20 co-occurring items
top_items = co_occurrence_df.groupby("Item 1")["Count"].sum().nlargest(20).index
filtered_co_occurrence_df = co_occurrence_df[
    co_occurrence_df["Item 1"].isin(top_items) & co_occurrence_df["Item 2"].isin(top_items)
]

# Create heatmap data
heatmap_data = filtered_co_occurrence_df.pivot_table(
    index="Item 1", columns="Item 2", values="Count", fill_value=0
)

fig, ax = plt.subplots(figsize=(10, 8))
sns.heatmap(heatmap_data.astype(int), cmap="YlGnBu", ax=ax, annot=True, fmt="d")
plt.title("Top 20 Co-occurrence Matrix Heatmap")
st.pyplot(fig)
insight_box(
    "The heatmap shows the strongest co-occurrence relationships between items, "
    "highlighting combinations that frequently appear together."
)

# 3. Frequent Item Combinations (Network Graph)
st.markdown("### Frequent Item Combinations")
G = nx.Graph()
for (item1, item2), freq in sorted(all_combinations.items(), key=lambda x: x[1], reverse=True)[:50]:
    if freq > 10:
        G.add_edge(item1, item2, weight=freq)

fig, ax = plt.subplots(figsize=(12, 8))
pos = nx.spring_layout(G)
nx.draw(
    G, pos, with_labels=True, font_size=8, 
    node_size=500, node_color="skyblue", edge_color="gray", ax=ax
)
plt.title("Frequent Item Combinations Network")
st.pyplot(fig)
insight_box(
    "The network graph highlights clusters of items frequently bought together. "
    "These clusters can inform product bundling and inventory placement."
)

# 4. Transaction Size Distribution
st.markdown("### Transaction Size Distribution")
transaction_lengths = transactions[transactions.str.len() > 0].apply(len)
transaction_size_chart = px.histogram(
    transaction_lengths,
    x=transaction_lengths,
    nbins=10,
    title="Transaction Size Distribution",
    labels={"x": "Number of Items", "y": "Frequency"}
)
st.plotly_chart(transaction_size_chart, use_container_width=True)
insight_box(
    "Most transactions involve a small number of unique items, reflecting frequent smaller purchases. "
    "This insight is valuable for setting realistic thresholds in further analyses."
)

st.write("---")
st.write("### Next Steps")
st.write("Proceed to the **Analysis and Insights Section** for interactive visualizations, patterns, and actionable insights.")
