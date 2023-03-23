import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

def make_recommendation(dataset, matrix_wines,perfil, top=4):
    
    """
    Receives dataframes and return top n-wines most similar with good wines.
    Evaluate and return just wines well defined, with good_score>bad_score.
    
    
    good_score ->cosin_similarity of most liked wines against dataset of all wines.
    bad_score ->cosin_similarity of not liked wines against dataset of all wines.
    
    - dataset: contains all wines attributes and come from scraping wine marketplaces.
    
    - matrix_wines: it's a dataset treated and transformed with column_transformer.
    
    - perfil: It's contains name of wines and Most liked (1) / least liked (-1)
    this is used in similarity score.
    
    """
    
    preferidos = perfil.loc[perfil['evaluation']==1,'name'].to_list()
    vector_preferido = matrix_wines.loc[matrix_wines.index.isin(preferidos)]
    good = pd.DataFrame(vector_preferido.mean(axis=0)).T
    
    ruim = perfil.loc[perfil['evaluation']==-1,'name'].to_list()

    if len(ruim)>0:
   
        vector_ruim = matrix_wines.loc[matrix_wines.index.isin(ruim)]
        bad = pd.DataFrame(vector_ruim.mean(axis=0)).T
        
        #Matrix of wines without choosed elements from users.

        #matrix_wines_wv = matrix_wines
        matrix_wines_wv = matrix_wines.loc[~(matrix_wines.index.isin(preferidos))]
        matrix_wines_wv = matrix_wines_wv.loc[~(matrix_wines_wv.index.isin(ruim))] 

        similarity_good = cosine_similarity(matrix_wines_wv,good)

        recommended = pd.DataFrame(similarity_good, index=matrix_wines_wv.index, columns=['matching_vinhos_bons'])

        similarity_bad = cosine_similarity(matrix_wines_wv,bad)

        recommended['matching_vinhos_ruins'] = similarity_bad 

        recommended.sort_values(by='matching_vinhos_bons',ascending=False,inplace=True)

        # Just a "sanity check", if cos_score_bad > matching_vinhos_bons exclude 

        recommended = recommended.loc[recommended['matching_vinhos_bons']>recommended['matching_vinhos_ruins']]

        top_recommended = recommended.head(top)

        return dataset.loc[dataset.index.isin(top_recommended.index.to_list())], pd.concat([top_recommended,dataset.loc[dataset.index.isin(top_recommended.index.to_list())]],axis=1)

    else:

        matrix_wines_wv = matrix_wines.loc[~(matrix_wines.index.isin(preferidos))]

        similarity_good = cosine_similarity(matrix_wines_wv,good)

        recommended = pd.DataFrame(similarity_good, index=matrix_wines_wv.index, columns=['matching_vinhos_bons'])

        recommended.sort_values(by='matching_vinhos_bons',ascending=False,inplace=True)

        top_recommended = recommended.head(top)

        return dataset.loc[dataset.index.isin(top_recommended.index.to_list())], pd.concat([top_recommended,dataset.loc[dataset.index.isin(top_recommended.index.to_list())]],axis=1)


    
