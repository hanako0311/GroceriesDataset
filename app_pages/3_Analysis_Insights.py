import pandas as pd
import plotly.express as px
import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
from mlxtend.frequent_patterns import apriori, association_rules

# Cached functions for preprocessing and analysis
@st.cache_data
def preprocess_transactions(df):
    return df.groupby(['Member_number', 'Date'])['itemDescription'].apply(list).apply(set)

@st.cache_data
def encode_transactions(transactions):
    unique_items = sorted(set(item for transaction in transactions for item in transaction))
    encoded_data = pd.DataFrame(0, index=transactions.index, columns=unique_items)
    for idx, transaction in transactions.items():
        encoded_data.loc[idx, list(transaction)] = 1  # Convert the set to a list
    return encoded_data

@st.cache_data
def generate_frequent_itemsets(encoded_data, min_support):
    return apriori(encoded_data, min_support=min_support, use_colnames=True)

@st.cache_data
def generate_association_rules(frequent_itemsets, min_confidence):
    return association_rules(frequent_itemsets, metric="confidence", min_threshold=min_confidence)

# Function to plot network graph
def plot_network_graph(rules, title="Association Rules Network"):
    rules_graph = nx.DiGraph()
    for _, row in rules.iterrows():
        rules_graph.add_edge(str(row['antecedents']), str(row['consequents']), weight=row['lift'])
    fig, ax = plt.subplots(figsize=(12, 8))
    pos = nx.spring_layout(rules_graph)
    nx.draw(
        rules_graph, pos, with_labels=True, font_size=8,
        node_size=500, node_color="lightblue", edge_color="gray", ax=ax
    )
    plt.title(title)
    return fig

# Access the cleaned and prepared data from session_state
df = st.session_state["df"]

# Header
st.write("""
This section provides interactive visualizations of association rules, highlights key insights, and allows users to explore patterns and trends dynamically.
""")

# Preprocess transactions
transactions = preprocess_transactions(df)

# Encode transactions
encoded_data = encode_transactions(transactions)

# Sidebar parameters
st.sidebar.markdown("### Analysis Parameters")

# Set default values for support and confidence
min_support = st.sidebar.slider(
    "Minimum Support (Detailed)", 
    min_value=0.001, 
    max_value=0.05, 
    value=0.008,  # Default value
    step=0.001, 
    format="%.3f", 
    help="Adjust the minimum support threshold. Smaller values include more itemsets."
)

min_confidence = st.sidebar.slider(
    "Minimum Confidence (Detailed)", 
    min_value=0.1, 
    max_value=1.0, 
    value=0.10,  # Default value
    step=0.01, 
    format="%.2f", 
    help="Adjust the minimum confidence threshold. Higher values include only reliable rules."
)

# Generate frequent itemsets and rules
frequent_itemsets = generate_frequent_itemsets(encoded_data, min_support)
frequent_itemsets['length'] = frequent_itemsets['itemsets'].apply(len)

if not frequent_itemsets.empty:
    rules = generate_association_rules(frequent_itemsets, min_confidence)
    
    if not rules.empty:
        st.markdown("### Insights from Analysis")
        st.write(f"""
        - With a **minimum support** of {min_support:.3f} and **confidence** of {min_confidence:.2f}, 
          we identified {len(frequent_itemsets)} frequent itemsets and {len(rules)} association rules.
        """)

        # Frequent Itemsets Visualization
        st.markdown("### Top Frequent Itemsets")
        frequent_itemsets['itemsets'] = frequent_itemsets['itemsets'].apply(lambda x: ', '.join(list(x)))
        top_itemsets_chart = px.bar(
            frequent_itemsets.nlargest(10, 'support'),
            x='itemsets',
            y='support',
            title="Top 10 Frequent Itemsets",
            labels={"itemsets": "Itemsets", "support": "Support"}
        )
        st.plotly_chart(top_itemsets_chart, use_container_width=True)
        st.write("**Insight:** The top frequent itemsets represent commonly purchased product combinations, which can be used to suggest product bundles or promotions.")

        # Association Rules Network Graph
        st.markdown("### Simplified Association Rules Network")
        fig = plot_network_graph(rules, title="Top 6 Association Rules Network")
        st.pyplot(fig)
        st.write("**Insight:** The network graph shows key relationships between products, useful for cross-selling strategies.")

        # Confidence vs Lift Scatter Plot
        st.markdown("### Confidence vs Lift Scatter Plot")
        scatter_chart = px.scatter(
            rules,
            x='confidence',
            y='lift',
            size='support',
            color='antecedents',
            title="Confidence vs Lift of Association Rules",
            labels={"confidence": "Confidence", "lift": "Lift", "antecedents": "Antecedents"}
        )
        st.plotly_chart(scatter_chart, use_container_width=True)
        st.write("**Insight:** Rules with higher confidence and lift indicate strong and actionable product associations.")

        # Display Top Rules
        st.markdown("### Top 6 Association Rules")
        st.dataframe(
            rules[['antecedents', 'consequents', 'support', 'confidence', 'lift']].nlargest(6, 'lift'),
            height=300
        )
        st.write("**Insight:** These rules highlight the strongest correlations between products, ideal for strategic marketing.")
    else:
        st.error(f"No association rules were found for support {min_support:.3f} and confidence {min_confidence:.2f}. Try lowering the thresholds.")
else:
    st.error(f"No frequent itemsets were found for support {min_support:.3f}. Try lowering the support threshold.")
# Store results in session state
st.session_state["frequent_itemsets"] = frequent_itemsets
st.session_state["rules"] = rules

# Summary and Next Steps
st.write("---")
st.write("""
### Summary
This analysis uncovers meaningful patterns and relationships, offering actionable insights for marketing, inventory optimization, and strategic planning.

### Next Steps
- Refine thresholds to explore deeper associations.
- Use these insights for targeted promotions or product placement strategies.
""")
