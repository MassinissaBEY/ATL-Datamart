import gc
import os
import sys

import pandas as pd
from sqlalchemy import create_engine


def write_data_postgres(dataframe: pd.DataFrame) -> bool:
    """
<<<<<<< HEAD
    Dumps a Dataframe to the DBMS engine with real-time logging

    Parameters:
        - dataframe (pd.DataFrame) : The dataframe to dump into the DBMS engine

    Returns:
        - bool : True if successful, False otherwise
    """
    db_config = {
        "dbms_engine": "postgresql",
        "dbms_username": "admin",
=======
    Dumps a Dataframe to the DBMS engine

    Parameters:
        - dataframe (pd.Dataframe) : The dataframe to dump into the DBMS engine

    Returns:
        - bool : True if the connection to the DBMS and the dump to the DBMS is successful, False if either
        execution is failed
    """
    db_config = {
        "dbms_engine": "postgresql",
        "dbms_username": "postgres",
>>>>>>> 2ecb5002085e6a6f73c022aeb65f46a29bbeb5d0
        "dbms_password": "admin",
        "dbms_ip": "localhost",
        "dbms_port": "15432",
        "dbms_database": "nyc_warehouse",
        "dbms_table": "nyc_raw"
    }

    db_config["database_url"] = (
        f"{db_config['dbms_engine']}://{db_config['dbms_username']}:{db_config['dbms_password']}@"
        f"{db_config['dbms_ip']}:{db_config['dbms_port']}/{db_config['dbms_database']}"
    )
<<<<<<< HEAD

    try:
        engine = create_engine(db_config["database_url"])
        with engine.begin() as conn:
            success = True
            total_rows = len(dataframe)
            chunk_size = 10000
            print(f"✅ Connexion à PostgreSQL réussie")
            print(f"📦 Début de l'insertion de {total_rows} lignes dans la table `{db_config['dbms_table']}`")

            for start in range(0, total_rows, chunk_size):
                end = min(start + chunk_size, total_rows)
                chunk = dataframe.iloc[start:end]
                chunk.to_sql(
                    db_config["dbms_table"],
                    conn,
                    index=False,
                    if_exists='append',
                )
                print(f"➡️  {end}/{total_rows} lignes insérées...")

    except Exception as e:
        success = False
        print(f"❌ Erreur de connexion ou d'insertion : {e}")
        return success

    print("✅ Insertion complète terminée !")
=======
    try:
        engine = create_engine(db_config["database_url"])
        with engine.connect():
            success: bool = True
            print("Connection successful! Processing parquet file")
            dataframe.to_sql(db_config["dbms_table"], engine, index=False, if_exists='append')

    except Exception as e:
        success: bool = False
        print(f"Error connection to the database: {e}")
        return success

>>>>>>> 2ecb5002085e6a6f73c022aeb65f46a29bbeb5d0
    return success


def clean_column_name(dataframe: pd.DataFrame) -> pd.DataFrame:
<<<<<<< HEAD
=======
    """
    Take a Dataframe and rewrite it columns into a lowercase format.
    Parameters:
        - dataframe (pd.DataFrame) : The dataframe columns to change

    Returns:
        - pd.Dataframe : The changed Dataframe into lowercase format
    """
>>>>>>> 2ecb5002085e6a6f73c022aeb65f46a29bbeb5d0
    dataframe.columns = map(str.lower, dataframe.columns)
    return dataframe


<<<<<<< HEAD

=======
>>>>>>> 2ecb5002085e6a6f73c022aeb65f46a29bbeb5d0
def main() -> None:
    # folder_path: str = r'..\..\data\raw'
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Construct the relative path to the folder
    folder_path = os.path.join(script_dir, '..', '..', 'data', 'raw')

    parquet_files = [f for f in os.listdir(folder_path) if
                     f.lower().endswith('.parquet') and os.path.isfile(os.path.join(folder_path, f))]

    for parquet_file in parquet_files:
        parquet_df: pd.DataFrame = pd.read_parquet(os.path.join(folder_path, parquet_file), engine='pyarrow')

        clean_column_name(parquet_df)
        if not write_data_postgres(parquet_df):
            del parquet_df
            gc.collect()
            return

        del parquet_df
        gc.collect()


if __name__ == '__main__':
    sys.exit(main())
