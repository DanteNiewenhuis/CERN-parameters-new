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

# h1
df_lz4 = pd.read_csv(
    "/home/dante-niewenhuis/Documents/CERN-parameters-new/results/h1/Annealer/23-06-19_17:24:06.csv"
)
df_zstd = pd.read_csv(
    "/home/dante-niewenhuis/Documents/CERN-parameters-new/results/h1/Annealer/23-06-20_00:25:20.csv"
)

# cms
df_lz4 = pd.read_csv(
    "/home/dante-niewenhuis/Documents/CERN-parameters-new/results/cms/Annealer/23-06-17_08:24:25.csv"
)
df_zstd = pd.read_csv(
    "/home/dante-niewenhuis/Documents/CERN-parameters-new/results/cms/Annealer/23-06-18_01:23:14.csv"
)

df_lz4 = df_lz4.iloc[1:]
df_zstd = df_zstd.iloc[1:]


parameters = ["Compression Type", "Cluster Size", "Page Size", "Cluster Bunch"]

metrics = [
    "performance(%)",
    "size_decrease(%)",
    "throughput_increase(%)",
    "memory_usage_decrease(%)",
]

# %%


def make_unique(
    df: pd.DataFrame, parameters: list[str], target="performance(%)"
):
    unique_df = []

    for group, row in df.groupby(parameters):
        unique_df.append(
            row[row[target] == row[target].max()].iloc[0].to_numpy()
        )

    return pd.DataFrame(unique_df, columns=df.columns)


df_lz4_unique = make_unique(df_lz4, parameters)
df_zstd_unique = make_unique(df_zstd, parameters)

# %%

df_lz4_unique.sort_values("performance(%)", ascending=False)[:10][
    parameters + metrics
]
# %%

df_zstd_unique.sort_values("performance(%)", ascending=False)[:10][
    parameters + metrics
]
# %%


def get_rows(df, compression_type, cluster_size, page_size, cluster_bunch):
    return df[
        (df["Compression Type"] == compression_type)
        & (df["Page Size"] == page_size)
        & (df["Cluster Size"] == cluster_size)
        & (df["Cluster Bunch"] == cluster_bunch)
    ]


# %%

performance_list = list(
    df_lz4_unique.sort_values("performance(%)", ascending=False)[
        "performance(%)"
    ]
)

for i, (idx, row) in enumerate(
    df_zstd_unique.sort_values("performance(%)", ascending=False).iterrows()
):
    compression_type, cluster_size, page_size, cluster_bunch = row[parameters]

    rows = get_rows(
        df_lz4_unique, "lz4", cluster_size, page_size, cluster_bunch
    )

    if len(rows) > 0:
        perfomance = rows["performance(%)"].iloc[0]
        print(
            f"{i} => {performance_list.index(perfomance)}, {row['performance(%)']} => {perfomance}"
        )

# %%
