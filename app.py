import streamlit as st
import pandas as pd
from PIL import Image
from toolbox import front_utils as fu, recommender as rc
import os

st.set_page_config(
    page_title="Alfred Wine Advisor",
    page_icon=":wine_glass:",
    layout="centered",
    initial_sidebar_state="expanded",
)

st.title('Alfred wine advisor :wine_glass:')

# Load the image
image = Image.open('arts/alfred_art.png')
#image = image.resize((420,420))

col1, col2, = st.columns(2)

with col1:
    st.image(image)

with col2:
    st.markdown('''Meu nome é **Alfred**, sou um **gato** apreciador de vinhos. Durante a minha vida coletei 
    dados de diferentes vinhos, de diversos tipos e países e aprendi a indicar vinhos para as pessoas e gatos. 
    Para conseguir te ajudar vou precisar entender com você quais vinhos você mais gosta de tomar e, caso 
    tenha algum vinho que não te traz boas lembranças, também entender qual foi.''')
                
    st.markdown('''
    Ainda tenho muita coisa para aprender então pode ser que alguns vinhos que você já tomou eu nunca tenha visto, mas calma
    um dia eu chego lá, ainda vou tomar muito vinho e aprender muito.
    ''')

# Matriz com carcaterísticas do vinho.



#vinhos = fu.import_encrypted_csv('model/encr_super_wine_set_clean.csv', st.secrets["key"])

vinhos = pd.read_csv('model/super_wine_set_clean.csv')

vinhos.set_index('vinho', inplace=True)

# Matriz com vectorização dos atributos

model = pd.read_csv('model/vectorized_wine_matrix.csv') 

model.set_index('vinho', inplace=True)

#st.dataframe(data=vinhos)

# Perfil section, from here are constructed the customer perfil, used in recommendation.

st.title('Perfil')
st.markdown('''Aqui vamos criar o seu perfil de gosto, baseado em suas experiências anteriores. 
Tente se lembrar de vinhos que tenha gostado e também dos que não gostou. Isso vai ajudar a entender 
quais os vinhos mais recomendados para você.''')

option = st.checkbox("*Já criou seu perfil no passado ? Selecione aqui e faça o upload.*")

if option == True:


    try:
        uploaded_file = st.file_uploader("Jogue aqui seu .xlsx contendo seu perfil")
        upl_perfil = pd.read_excel(uploaded_file)
        st.write(upl_perfil)
        st.info('''Caso queira adicionar novos items ao seu perfil, você poderá seleciona-los normalmente depois de ter feito o upload, e assim que fizer
    o download já terá seu perfil atualizado !''')

    except:
        pass

 
perfil = {'name':[],'evaluation':[]}

good = st.multiselect(f':smiley: - Selecione alguns vinhos que você **GOSTOU** ', vinhos.index)

for wine in good:

    perfil['name'].append(wine)
    perfil['evaluation'].append(1)

bad = st.multiselect(':cold_sweat: - Selecione alguns vinhos que você **NÃO GOSTOU** (OPCIONAL)', vinhos.index)

for wine in bad:

    perfil['name'].append(wine)
    perfil['evaluation'].append(-1)

perfil_df = pd.DataFrame(perfil)

if option ==  True:

    try:

        perfil_df = pd.concat([upl_perfil,perfil_df])
        perfil_df = perfil_df.drop_duplicates()

    except:

        pass

else:

    perfil_df = perfil_df


#st.dataframe(perfil_df)

st.download_button(label="Faça Download do seu Perfil",data=fu.df_to_excel_bytes(perfil_df),file_name='perfil.xlsx')

    
st.title('Recomendação')

st.info('Esta não é uma recomendação com objetivo comercial, tem um caráter experimental/educacional ! Experimente por sua conta e risco.')

try:
    top = st.slider('Quantos Vinhos você quer que sejam recomendados ?', min_value=1, max_value=12,value=4,step=1)

    recommendations, recommendations_wscores = rc.make_recommendation(dataset=vinhos.dropna(), 
                                            matrix_wines=model.dropna(),
                                            perfil=perfil_df.dropna(), top=top)


    st.markdown('**Estes são alguns dos vinhos que você pode gostar** :wine_glass: !')

    option2 = st.checkbox("Se quiser ver os scores para cada vinho selecione aqui!")

    if option2:
        st.dataframe(recommendations_wscores)

    else:
        st.dataframe(recommendations)

except:

    st.info('Você precisa escolher pelo menos 1 vinho que já tenha gostado !')
