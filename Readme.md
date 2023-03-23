# Wine Recommendation System

The ideia behind this project it's to build a content based recommender system to compare your taste and wines that you liked in the past 
and propose new wines.

data_collecting -> raw_data -> etl -> super_wine_set.csv -> pipeline(feature_engineering) -> vectorized_matrix

perfil -> pefil_NAME.csv -> my_favorite_vector

vectorize_matrix vs. my_favorite_vector -> recommendations

## Project Structure

- data_collecting

Web scraping related, collecting raw data from different sources.

- etl

From data_collecting treating and merging all raw data and prepare it for model 

- model

- perfil

- toolbox
Here all tools specific for this project are stored and managed, used in pipelines, clean specific data and etc...
