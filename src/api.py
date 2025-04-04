import pickle
import polars as pl
from pathlib import Path
from typing import List
from fastapi import FastAPI
from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel

MODEL_PATH = "../data/penguin_k_means.pkl"

MIN_MAX = {
    "bill_length_mm": [32.1, 59.6],
    "bill_depth_mm": [13.1, 21.5],
    "flipper_length_mm": [172.0, 231.0],
}


class BaseSchema(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True,
    )


class Penguin(BaseSchema):
    bill_length: float
    bill_depth: float
    flipper_length: float


with open(Path(MODEL_PATH), "rb") as f:
    penguin_k_means = pickle.load(f)

app = FastAPI()


@app.post("/")
async def root(penguins: List[Penguin]):
    penguin_df = (
        pl.DataFrame(penguins)
        .rename(
            {
                "bill_length": "bill_length_mm",
                "bill_depth": "bill_depth_mm",
                "flipper_length": "flipper_length_mm",
            }
        )
        .select(
            (pl.col("bill_length_mm") - MIN_MAX["bill_length_mm"][0])
            / (MIN_MAX["bill_length_mm"][1] - MIN_MAX["bill_length_mm"][0]),
            (pl.col("bill_depth_mm") - MIN_MAX["bill_depth_mm"][0])
            / (MIN_MAX["bill_depth_mm"][1] - MIN_MAX["bill_depth_mm"][0]),
            (pl.col("flipper_length_mm") - MIN_MAX["flipper_length_mm"][0])
            / (MIN_MAX["flipper_length_mm"][1] - MIN_MAX["flipper_length_mm"][0]),
        )
    )

    return penguin_k_means.predict(penguin_df).tolist()
