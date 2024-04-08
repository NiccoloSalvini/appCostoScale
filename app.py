import streamlit as st
import pandas as pd
import numpy as np

def calcola_spese(spese_totali, incremento_percentuale, num_piani):
    # Calcola la spesa per millesimi (equamente divisa)
    spesa_per_appartamento_millesimi = (spese_totali / 2) / num_piani
    
    # Calcola la spesa in base all'altezza
    coeff_incremento = np.array([(1 + incremento_percentuale / 100) ** i for i in range(num_piani)])
    somma_coeff = np.sum(coeff_incremento)
    spese_per_piano_altezza = (spese_totali / 2) * coeff_incremento / somma_coeff
    
    # Totale spese per appartamento
    spese_totali_per_appartamento = spesa_per_appartamento_millesimi + spese_per_piano_altezza
    
    return pd.DataFrame({
        'Piano': range(1, num_piani + 1),
        'Spesa Totale': np.round(spese_totali_per_appartamento, 2)
    })

# Titolo dell'app
st.title('Rendi la vita facile all\'Eli 🐕')

# Input dell'utente
spese_totali = st.number_input('Inserisci le spese totali di pulizia:', value=1000)
incremento_percentuale = st.number_input('Inserisci l\'incremento percentuale per piano:', value=10)
num_piani = st.number_input('Inserisci il numero di piani:', value=5, format='%d')

# Bottone per eseguire il calcolo
if st.button('Calcola Spese'):
    # Esegui il calcolo
    risultato_df = calcola_spese(spese_totali, incremento_percentuale, num_piani)
    
    # Mostra i risultati
    st.write("Spese per piano:")
    st.dataframe(risultato_df)

