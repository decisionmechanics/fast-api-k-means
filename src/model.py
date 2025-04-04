import pickle
import polars as pl
from pathlib import Path
from sklearn.cluster import KMeans


def build_model():
    penguin_df = (
        pl.read_csv("../data/penguins.csv", null_values=["NA"])
        .select(
            [
                "bill_length_mm",
                "bill_depth_mm",
                "flipper_length_mm",
            ]
        )
        .drop_nulls()
        .select((pl.all() - pl.all().min()) / (pl.all().max() - pl.all().min()))
    )

    k_means = KMeans(n_clusters=3, random_state=0, n_init="auto")
    k_means.fit(penguin_df)

    with open("../data/penguin_k_means.pkl", "wb") as f:
        pickle.dump(k_means, f)


def main():
    if not Path("../data/penguin_k_means.pkl").exists():
        build_model()

    print("Maximum and minimum values of the features used for clustering:")

    print(
        pl.read_csv("../data/penguins.csv", null_values=["NA"])
        .select(
            [
                "bill_length_mm",
                "bill_depth_mm",
                "flipper_length_mm",
            ]
        )
        .drop_nulls()
        .min()
    )

    print(
        pl.read_csv("../data/penguins.csv", null_values=["NA"])
        .select(
            [
                "bill_length_mm",
                "bill_depth_mm",
                "flipper_length_mm",
            ]
        )
        .drop_nulls()
        .max()
    )


if __name__ == "__main__":
    main()
