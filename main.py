import streamlit as st
import pandas as pd


def load_data():
    """# read csv
    df_insa = pd.read_excel("data/insa_tca.xlsx")

    # remove 2nd row a header
    df_insa.columns = df_insa.iloc[0]

    # remove 1st row
    df_insa = df_insa.iloc[1:]

    # get the column nname with the HC (it has some special characters)
    coluna_hc = df_insa.columns[13]

    # create a new column with the name of the food and the HC per 100g
    df_insa["alimento_hc"] = df_insa.apply(lambda row: f"{row['Nome do alimento']} ({row[coluna_hc]}g HC/100g)", axis=1)

    return df_insa
    """
    return pd.read_csv("data/insa_tca_processed.csv")

def formula_insulina(equivalencia_hc_insulina, fator_sensibilidade, alimento):

    df_insa = load_data()

    hc_por_100 = df_insa[df_insa["alimento_hc"] == alimento["Alimento"]][df_insa.columns[13]].values[0]

    hc = alimento["Quantidade"]*hc_por_100/100

    return hc


def correcao_glicemia(fator_sensibilidade, glicemia, glicemia_alvo):
    return (glicemia - glicemia_alvo) / fator_sensibilidade


def calculo_insulina(equivalencia_hc_insulina, fator_sensibilidade, glicemia, glicemia_alvo, tendencia_glicemia, lista_alimentos):

    # insulin dose reset
    dose_insulina = 0

    if glicemia < 60:
        return 0

    dose_insulina += correcao_glicemia(fator_sensibilidade, glicemia, glicemia_alvo)

    # check if there are foods in the list
    if len(lista_alimentos) != 0:
        # loop through the list of foods
        for alimento in lista_alimentos:
            # get the amount of insulin for each food
            dose_insulina += formula_insulina(equivalencia_hc_insulina, fator_sensibilidade, alimento)

    # add the correction dose according to the glycemia and the trend

    if tendencia_glicemia == "ascendete inclinado":
        dose_insulina *= 1.2
    elif tendencia_glicemia == "ascendente":
        dose_insulina *= 1.1
    elif tendencia_glicemia == "descendente inclinado":
        dose_insulina *= 0.8
    elif tendencia_glicemia == "descendente":
        dose_insulina *= 0.9

    return dose_insulina


def main():
    st.title("Calculadora Insulina")

    if "lista_alimentos" not in st.session_state:
        st.session_state["lista_alimentos"] = []

    if "dose_insulina" not in st.session_state:
        st.session_state["dose_insulina"] = 0

    df_insa = load_data()


    # lista de alimentos
    lista_alimentos = df_insa["alimento_hc"]

    #st.table(df_insa[["Nome do alimento","Hidratos de carbono [g]"]].head(10))

    col_1, col_2, col_3, col_4, col_5 = st.columns(5)

    with col_1:
        st.session_state["equivalencia_hc_insulina"] = st.number_input("Equivalencia HC", value=12, step=1, min_value=10, max_value=15)
    with col_2:
        st.session_state["fator_sensibilidade"] = st.number_input("Fator Sensibilidade", value=30, step=5)
    with col_3:
        st.session_state['glicemia'] = st.number_input("Glicémia (mg/dl)", value=100, step=5)
    with col_4:
        st.session_state["glicemia_alvo"] = st.number_input("Glicémia Alvo (mg/dl)", value=100, step=5)
    with col_5:
        st.session_state["tendencia_glicemia"] = st.radio("Tendencia Glicemia", ["estável", "ascendente", "ascendete inclinado", "descendente", "descendente inclinado"], horizontal=True)

    st.divider()

    tab_1, tab_2 = st.tabs(["Lista de alimentos", "outros"])
    with tab_1:
        col_5, col_6= st.columns(2)

        with col_5:
            st.session_state["alimento"] = st.selectbox("Alimento", lista_alimentos, index=0)
        with col_6:
            st.session_state["quantidade"] = st.number_input("Quantidade (g)", value=50, step=5)

        if st.button("adicionar alimento", type="secondary"):
            st.session_state["lista_alimentos"].append(
                {
                    "Alimento": st.session_state["alimento"],
                    "Quantidade":st.session_state["quantidade"]
                }
            )

        if st.button("limpar lista", type="primary"):
            st.session_state["lista_alimentos"] = []

        st.write("Lista de alimentos")
        #st.write(st.session_state["lista_alimentos"])
        st.session_state["lista_alimentos"] = st.data_editor(st.session_state["lista_alimentos"])

    with tab_2:
        st.write("Outro Alimentio")

    st.divider()

    insulina = calculo_insulina(
        st.session_state["equivalencia_hc_insulina"],
        st.session_state["fator_sensibilidade"],
        st.session_state["glicemia"],
        st.session_state["glicemia_alvo"],
        st.session_state["tendencia_glicemia"],
        st.session_state["lista_alimentos"],
    )



    st.metric("Dose Insulina", insulina)
    with st.expander("Detalhes calculo"):
        st.write("""
            The dose of insulin is calculated by summing the amount of insulin for each food and adding the correction dose according to the glycemia and the trend.
            """)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()


