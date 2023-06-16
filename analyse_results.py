# %%

import pandas as pd
import os
import matplotlib.pyplot as plt

# %%

# lhcb
df_lz4 = pd.read_csv("results/lhcb/23-06-15_12:35:39.csv")
df_zstd = pd.read_csv("results/lhcb/23-06-15_17:04:17.csv")

# # atlas
# df_lz4 = pd.read_csv("results/atlas/23-06-15_19:35:12.csv")
# df_zstd = pd.read_csv("results/atlas/23-06-16_00:56:49.csv")


parameters = ["Compression Type", "Cluster Size", "Page Size", "Cluster Bunch"]

metrics = ["performance(%)", "size_decrease(%)",
           "throughput_increase(%)", "memory_usage_decrease(%)"]

# %%


def make_unique(df: pd.DataFrame, parameters: list[str], target="performance(%)"):

    unique_df = []

    for group, row in df.groupby(parameters):
        unique_df.append(row[row["performance(%)"] ==
                         row["performance(%)"].max()].iloc[0].to_numpy())

    return pd.DataFrame(unique_df, columns=df.columns)


df_lz4_unique = make_unique(df_lz4, parameters)
df_zstd_unique = make_unique(df_zstd, parameters)

# %%

df_lz4_unique.sort_values("performance(%)", ascending=False)[
    :10][parameters + metrics]
# %%

df_zstd_unique.sort_values("performance(%)", ascending=False)[
    :10][parameters + metrics]
# %%

df_zstd_unique.sort_values("performance(%)", ascending=False)[:10][parameters]

# %%


def get_rows(df, compression_type, cluster_size, page_size, cluster_bunch):
    return df[(df["Compression Type"] == compression_type) &
              (df["Page Size"] == page_size) &
              (df["Cluster Size"] == cluster_size) &
              (df["Cluster Bunch"] == cluster_bunch)]


compression_type, cluster_size, page_size, cluster_bunch = \
    list(df_zstd_unique.sort_values(
        "performance(%)", ascending=False).iloc[1][parameters])
rows = get_rows(df_lz4_unique, "lz4", cluster_size, page_size, cluster_bunch)

rows
# %%

# print(compression_type, cluster_size, page_size, cluster_bunch)


df_lz4_unique[(df_lz4_unique["Page Size"] == page_size) &
              (df_lz4_unique["Cluster Size"] == cluster_size)]
df_lz4_unique[(df_lz4_unique["Cluster Size"] == cluster_size)]

# %%

print(cluster_size)
