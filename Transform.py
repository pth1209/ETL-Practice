import Extract
import pandas as pd

def data_quality(dataset):
    if dataset.empty:
        print("No songs have been extracted.")
        return False
    
    if dataset.isnull().values.any():
        raise Exception("Null values found")

#Find out users' favorite/most recently listened to artists
def transform(dataset):
    transformed_df = dataset.groupby(["timestamp", "artist"], as_index = False).count()
    transformed_df.rename(columns = {"played_at":"count"}, inplace = True)

    transformed_df["id"] = str(transformed_df["timestamp"]) + "-" + transformed_df["artist"]

    return transformed_df[["id", "artist", "count"]]

if __name__ == "__main__":
    load_df = Extract.get_recently_played_track()
    data_quality(load_df)
    transformed_df = transform(load_df)
    print(transformed_df)