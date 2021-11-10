from pycaret.regression import load_model, predict_model 
import pandas as pd 
import numpy as np
from pathlib import Path
import streamlit as st
from PIL import Image
import os

#from google.colab import drive
#drive.mount('/content/drive')


from pycaret.regression import load_model, predict_model 
import pandas as pd 
import numpy as np
import streamlit as st
from PIL import Image
import os

class StreamlitApp:
    
    def __init__(self):
        pkl_path = Path(__file__).parents[1] / 'src/BoxOfficeModel'
        self.model = load_model(pkl_path)
        self.save_fn = 'path.csv'  

    def predict(self, input_data):
        return predict_model(self.model, data=input_data)

    def store_prediction(self, output_df): 
        if os.path.exists(self.save_fn):
            save_df = pd.read_csv(self.save_fn)
            save_df = save_df.append(output_df, ignore_index=True)
            save_df.to_csv(self.save_fn, index=False)
            
        else: 
            output_df.to_csv(self.save_fn, index=False) 
        
    def run(self):
        img_path = Path(__file__).parents[1] / 'src/Movie.jpg'
        image = Image.open(img_path)
        image.resize = (200, 200)
        st.image(image, use_column_width=True)


        st.title(" Box Office Predictions ")
        title = st.text_input("Name of movie", "Type here")
        genres = st.multiselect('Select genres:', ['Action', 'Comedy', 'Romance', 'Sci-fi', 'Drama', 'Fantasy', 'Horror', 'Mystery', 'Thriller', 'Western', 'Other', 'Adventure', 'Documentary'])

        for i in range (len(genres)):
            genres[i] =  "'name' :'" + genres[i]

        #jsonGenres = json.dumps(genres)
        budget = st.number_input('Budget', step=100000)

        collection = st.checkbox("Part of a collection: ")
        collectionBool = 0
        if collection:
            collectionBool = 1


        production_comp = st.selectbox("Production company", ['Disney', 'Warner Bros', 'Universal' , 'Sony', 'Paramount', 'Miramax', 'Columbia', 'Tristar' ,'20th Century','Other'])

        cast = st.text_input("Name of main actor")
        cast2 = st.text_input("Name of supporting actor")
        cast3 = st.text_input("Name of supporting actress")
        castlist = []
        if cast is not None:
            castlist.append(cast)
        if cast2 is not None:
            castlist.append(cast2)
        if cast3 is not None:
            castlist.append(cast3)


        crew = st.text_input("Name of director")
        crew2 = st.text_input("Name of producer")
        crewlist = []
        if crew is not None:
            crewlist.append(crew)
        if crew2 is not None:
            crewlist.append(crew2)

        #revstring = ""
        keyword = st.text_input("Plot keyword")
        language = st.selectbox("Language spoken", ['English', 'Other'])
        runtime = st.number_input('Runtime in minutes', step=1)
        date = st.date_input("Release date")
        #st.button("Calculate")
        #st.info(revstring)
        #st.info(collectionBool)
        original_language = st.selectbox("Original Language", ['en', 'other'])
        popularity = st.slider("Expected Popularity", 0,100,50)
        production_country = st.text_input("Production Country")
        status = st.selectbox("Released", ['1','0'])

        #revstring = "Calculated revenue :"

        output = None
        if st.button("Calculate", 12021241):
            input_dict = {'budget':budget, 'genres':genres, 'belongs_to_collection': collectionBool, 'status': status, 'crew': crew, 'cast': cast, 'original_language': original_language, 'Keywords': keyword, 'spoken_languages': original_language, 'production_countries': production_country, 'original_title': title, 'production_companies': production_comp, 'popularity': popularity, 'runtime': runtime, 'release_date': date }
            input_df = pd.DataFrame([input_dict], index=[0])
            output = self.model.predict(input_df)
            #revstring = predict_model(self.model, data=input_df)
            st.success('Predicted revenue: {revenue:,.2f}$ million'.format(revenue = output[0]/1000000).replace(",", " "))



sa = StreamlitApp()
sa.run()

