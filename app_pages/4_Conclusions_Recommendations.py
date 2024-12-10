import pandas as pd
import streamlit as st

# Conclusion and Recommendations Page
st.markdown("## Conclusion and Recommendations")

# Check if results are available in session state
if "frequent_itemsets" in st.session_state and "rules" in st.session_state:
    frequent_itemsets = st.session_state["frequent_itemsets"]
    rules = st.session_state["rules"]

    # Key Findings
    st.markdown("### Key Findings")
    st.write("""
    The analysis with a **minimum support of 0.008** and **confidence of 0.10** revealed **82 frequent itemsets** and **6 association rules**. 
    Here are the key takeaways:
    - **Frequent Itemsets**: High-support items such as `whole milk`, `other vegetables`, and `rolls/buns` dominate transactions, indicating their central role in customer purchases.
    - **Association Rules**: The strongest rules indicate that `whole milk` is frequently purchased alongside other products such as `sausage`, `yogurt`, and `rolls/buns`.
    """)

    # Display the table of Top Frequent Itemsets
    st.markdown("#### Top 10 Frequent Itemsets")
    st.dataframe(frequent_itemsets.nlargest(10, 'support')[['itemsets', 'support']], height=300)

else:
    st.error("Analysis results are not available. Please run the Analysis and Insights page first.")

# Display the table of Top Association Rules
st.markdown("#### Top 6 Association Rules")
st.dataframe(
    rules[['antecedents', 'consequents', 'support', 'confidence', 'lift']].nlargest(6, 'lift'),
    height=300
)

# Recommendations Section
st.markdown("### Recommendations")

st.markdown("#### 1. Marketing and Promotions")
st.write("""
- **Cross-Selling Opportunities**:
  - Promote `whole milk` with items such as `rolls/buns` or `sausage` to increase basket size.
  - Use association rules to create "Frequently Bought Together" recommendations online.
- **Bundling**:
  - Create promotional bundles like "Whole Milk + Rolls/Buns" or "Whole Milk + Sausage."
- **Loyalty Programs**:
  - Reward customers who frequently purchase high-support items like `whole milk` or `other vegetables`.
""")

st.markdown("#### 2. Inventory Management")
st.write("""
- **Stock Prioritization**:
  - Ensure sufficient inventory of frequently purchased items (`whole milk`, `rolls/buns`, `other vegetables`) to meet demand.
- **Peak Demand Planning**:
  - Adjust inventory levels for high-demand items during holidays or weekends.
""")

st.markdown("#### 3. Store Layout Optimization")
st.write("""
- **Product Placement**:
  - Place frequently associated items (`whole milk` and `rolls/buns`) near each other in physical stores to boost impulse purchases.
  - For e-commerce, feature these items prominently in search results or product pages.
""")

st.markdown("#### 4. Customer Personalization")
st.write("""
- **Targeted Campaigns**:
  - Use purchase history to target customers who buy `sausage`, `yogurt`, or `tropical fruit`, recommending `whole milk` to them.
- **New Product Pairings**:
  - Explore promotional opportunities for pairs like `yogurt and root vegetables` based on their frequent association.
""")

# Summary Section
st.markdown("### Summary")
st.write("""
This analysis highlights meaningful purchasing patterns and actionable insights for marketing, inventory management, and product placement. 
By leveraging these findings, businesses can optimize their operations and enhance customer satisfaction.
""")
