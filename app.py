!pip install pyngrok streamlit
# Importem les llibreries
from pyngrok import ngrok
import os

# Configura el teu token d'Ngrok
ngrok.set_auth_token("2wOrSIJYthjHQquJHdnfFDoqlTk_4qkcnEUggjPPspywe7B3b")

# Iniciar ngrok per exposar l'aplicació Streamlit a través d'un enllaç públic (utilitzant la nova API)
public_url = ngrok.connect(8501, "http")

# Executar Streamlit en segon pla
!streamlit run app.py &

# Mostrar la URL pública per accedir a l'aplicació Streamlit
print(f"Accedeix a l'aplicació Streamlit a través d'aquest enllaç: {public_url}")

import streamlit as st
from tensorflow.keras.models import model_from_json
from PIL import Image, UnidentifiedImageError
import numpy as np
import os

# Configuració de la pàgina
st.set_page_config(page_title="Classificador Gats vs Gossos", layout="centered")
st.title("🐶 Classificador de Gossos i Gats 🐱")
st.markdown("Puja una imatge i la IA et dirà si veu un gos o un gat! 🧠")

# Puja una imatge
uploaded_file = st.file_uploader("📤 Pujar imatge (jpg, png)", type=["jpg", "jpeg", "png"])

# Comprovem si els arxius del model estan presents
if not os.path.exists("model_gats_gossos.json") or not os.path.exists("model_gats_gossos.weights.h5"):
    st.error("❌ El model no s'ha trobat. Assegura't que els fitxers JSON i WEIGHTS estiguin pujats correctament al teu repositori.")
else:
    # Carregar el model
    with open("model_gats_gossos.json", "r") as json_file:
        model_json = json_file.read()

    model = model_from_json(model_json)
    model.load_weights("model_gats_gossos.weights.h5")

    # Si s'ha pujat una imatge
    if uploaded_file:
        try:
            # Obtenir la imatge i processar-la
            image = Image.open(uploaded_file).convert("RGB").resize((100, 100))
            st.image(image, caption='📷 Imatge pujada', use_container_width=True)

            # Preparar la imatge per la predicció
            img_array = np.array(image) / 255.0
            img_array = np.expand_dims(img_array, axis=0)

            # Predir la classe
            prediction = model.predict(img_array)
            prob = float(prediction[0])

            if prob > 0.5:
                st.success(f"És un **gos** 🐶 amb {prob*100:.2f}% de confiança!")
            else:
                st.success(f"És un **gat** 🐱 amb {(1 - prob)*100:.2f}% de confiança!")

        except UnidentifiedImageError:
            st.error("❌ No s'ha pogut llegir la imatge. Si us plau, puja un arxiu .jpg o .png vàlid.")
