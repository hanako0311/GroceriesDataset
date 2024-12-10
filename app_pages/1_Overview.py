import pandas as pd
import streamlit as st

# Access the cached data from session_state
df = st.session_state["df"]

# Introduction page content
st.title("Groceries Dataset Analysis with Apriori Algorithm")
st.write(
    """
## Overview
The **Groceries Dataset** captures transaction data from a grocery store, detailing which items were purchased together in each transaction. 
This analysis focuses on leveraging the **Apriori Algorithm** to uncover frequent itemsets and meaningful association rules, providing insights into customer purchasing behavior.

By analyzing these patterns, grocery stores can enhance operations through:
- **Product Recommendations**: Suggesting frequently bought-together items to increase sales.
- **Inventory Optimization**: Prioritizing stock for high-demand combinations.
- **Promotional Campaigns**: Designing offers around popular product groupings.

### Objectives
- Identify frequent item combinations to understand customer purchasing trends.
- Discover actionable association rules to support data-driven decision-making in operations.

This interactive dashboard provides a seamless way to explore transaction patterns, apply the Apriori Algorithm, and generate valuable business insights.
"""
)

# Separator line to distinguish the introduction from user instructions
st.write("---")

# Research Question
st.write("### Research Question")
st.write("""
How can we identify frequent item combinations and actionable association rules from grocery store transaction data to inform business strategies?
""")

# Selected Analysis Technique
st.write("### Selected Analysis Technique: Apriori Algorithm")
st.write("""
The **Apriori Algorithm** identifies frequent item combinations in large datasets and generates association rules by evaluating metrics such as **support**, **confidence**, and **lift**. 
This technique enables us to pinpoint high-impact patterns for actionable business insights.
""")

# Display Dataset Structure
st.write("### Dataset Structure")
st.write("""
The dataset contains:
- **Member_number**: A unique customer identifier.
- **Date**: The transaction date.
- **itemDescription**: The description of items purchased.

Preview of the dataset:
""")
st.dataframe(df.head())

# Additional instructions for users
st.write(
    """
### Next Steps
Proceed to the following sections to:
1. **Prepare the data** for analysis.
2. Apply the **Apriori Algorithm**.
3. Visualize and explore patterns interactively.
4. Derive **business insights** from the results.
"""
)
