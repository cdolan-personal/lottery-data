import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset
df = pd.read_csv('data/streamlit_dataset.csv')

# Streamlit app title
st.title("Interactive Data Visualization with Streamlit")

# Filtering Controls
st.sidebar.header("Filter the dataset")
name_filter = st.sidebar.multiselect("Select Name(s):", options=df["name_label"].unique(), default=df["name_label"].unique())
generation_filter = st.sidebar.multiselect("Select Generation(s):", options=df["generation"].unique(), default=df["generation"].unique())
time_filter = st.sidebar.multiselect("Select Time(s):", options=df["time"].unique(), default=df["time"].unique())
selection_rank_filter = st.sidebar.slider("Select Selection Rank Range:", min_value=int(df["selection_rank"].min()), max_value=int(df["selection_rank"].max()), value=(int(df["selection_rank"].min()), int(df["selection_rank"].max())))
batch_id_filter = st.sidebar.multiselect("Select Batch ID(s):", options=df["batch_id"].unique(), default=df["batch_id"].unique())
user_id_filter = st.sidebar.multiselect("Select User ID(s):", options=df["user_id"].unique(), default=df["user_id"].unique())

# Apply Filters
filtered_df = df[
    (df["name_label"].isin(name_filter)) &
    (df["generation"].isin(generation_filter)) &
    (df["time"].isin(time_filter)) &
    (df["selection_rank"].between(*selection_rank_filter)) &
    (df["batch_id"].isin(batch_id_filter)) &
    (df["user_id"].isin(user_id_filter))
]

# Graph: Frequency Distribution of "Selection Rank" (bucketed by 10)
st.subheader("Frequency Distribution of Selection Rank (Bucketed by 10)")
fig1, ax1 = plt.subplots()
filtered_df["selection_rank"].hist(bins=range(int(df["selection_rank"].min()), int(df["selection_rank"].max()) + 10, 10), ax=ax1, color='skyblue')
ax1.set_xlabel("Selection Rank")
ax1.set_ylabel("Frequency")
ax1.set_title("Selection Rank Distribution (Bucketed by 10)")
st.pyplot(fig1)

# Graph: Distribution of Average Selection Rank per User ID (bucketed by 5, hiding zero-value bars)
st.subheader("Distribution of Average Selection Rank per User ID (Bucketed by 5)")
avg_selection_rank = filtered_df.groupby("user_id")["selection_rank"].mean()
avg_selection_rank = avg_selection_rank[avg_selection_rank > 0]  # Hide zero value bars
fig2, ax2 = plt.subplots()
avg_selection_rank.hist(bins=range(int(avg_selection_rank.min()), int(avg_selection_rank.max()) + 5, 5), ax=ax2, color='salmon')
ax2.set_xlabel("Average Selection Rank")
ax2.set_ylabel("Frequency")
ax2.set_title("Average Selection Rank per User ID (Bucketed by 5)")
st.pyplot(fig2)

# Table: Pivoted by Batch ID, showing average across batches
st.subheader("Pivot Table of Selection Rank by Batch ID")
pivot_table = filtered_df.pivot_table(index="user_id", columns="batch_id", values="selection_rank", aggfunc="mean")
pivot_table["Average"] = pivot_table.mean(axis=1)
st.dataframe(pivot_table)