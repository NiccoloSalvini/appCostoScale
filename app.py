import streamlit as st
import pandas as pd
import numpy as np

def calcola_spese(spese_totali, incremento_percentuale, millesimi, appartamenti_per_piano):
    num_piani = len(appartamenti_per_piano)
    
    # Calcola la spesa per millesimi
    spesa_per_millesimi = (spese_totali / 2) * np.array(millesimi) / sum(millesimi)
    
    # Calcola la spesa in base all'altezza
    coeff_incremento = np.array([(1 + incremento_percentuale / 100) ** i for i in range(num_piani)])
    somma_coeff = np.sum(coeff_incremento)
    spese_base_altezza = (spese_totali / 2) * coeff_incremento / somma_coeff
    
    # Distribuisci le spese per altezza su tutti gli appartamenti per piano
    spese_per_altezza = []
    for piano, spesa in zip(range(num_piani), spese_base_altezza):
        spese_per_altezza.extend([spesa / appartamenti_per_piano[piano]] * appartamenti_per_piano[piano])
    
    # Totale spese per appartamento
    spese_totali_per_appartamento = spesa_per_millesimi + np.array(spese_per_altezza)
    
    return pd.DataFrame({
        'Appartamento': range(1, sum(appartamenti_per_piano) + 1),
        'Spesa per Millesimi': np.round(spesa_per_millesimi, 2),
        'Spesa per Altezza': np.round(spese_per_altezza, 2),
        'Spesa Totale': np.round(spese_totali_per_appartamento, 2)
    })

# Titolo dell'app
st.title('Bassotto Budgeter 💰 - Calcolatore Spese Condominiali per l\'Eli')

# Input dell'utente
spese_totali = st.number_input('Inserisci le spese totali di pulizia:', value=1000)
incremento_percentuale = st.number_input('Inserisci l\'incremento percentuale per piano:', value=10)

# Millesimi per appartamento
millesimi_str = st.text_input('Inserisci i millesimi per ciascun appartamento separati da virgola:', '100,100,100,100,100')
millesimi = [float(x.strip()) for x in millesimi_str.split(',')]

# Appartamenti per piano
appartamenti_per_piano_str = st.text_input('Inserisci il numero di appartamenti per piano separati da virgola:', '1,1,1,1,1')
appartamenti_per_piano = [int(x.strip()) for x in appartamenti_per_piano_str.split(',')]

# Bottone per eseguire il calcolo
if st.button('Calcola Spese'):
    # Esegui il calcolo
    if len(millesimi) != sum(appartamenti_per_piano):
        st.error("Il numero totale di appartamenti specificato nei millesimi non corrisponde al totale degli appartamenti per piano.")
    else:
        risultato_df = calcola_spese(spese_totali, incremento_percentuale, millesimi, appartamenti_per_piano)
    
        # Mostra i risultati
        st.write("Spese dettagliate per appartamento:")
        st.dataframe(risultato_df)
