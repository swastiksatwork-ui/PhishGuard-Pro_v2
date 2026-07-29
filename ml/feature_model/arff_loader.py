from scipy.io import arff
import pandas as pd


def load_arff(file_path):

    data, meta = arff.loadarff(
        file_path
    )

    df = pd.DataFrame(
        data
    )

    for column in df.columns:

        if df[column].dtype == object:

            try:

                df[column] = df[column].str.decode(
                    "utf-8"
                )

            except:

                pass

    return df