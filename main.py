import streamlit as st
import pandas as pd
from utils.utils import *


def load_data():
    return pd.read_csv("data/insa_tca_processed.csv")


def main():
    st.title("Calculadora de Dose de Insulina")

    with st.sidebar:
        st.write(
            """
            # Ferramenta de apoio ao :blue[cálculo da dose de insulina] a administrar para pessoas com diabetes
            Permite:
            - Correção de glicémia atual
            - Correção de glicémia atual + Calculo para ingestão de alimentos utizando: 
                - hidratos de carbono ingerido OU
                - cálculo de hidratos de carbono a partir de uma lista de alimentos
            """
        )

        st.divider()

        st.info(
            """
            ### Definições
            - **Glicémia Actual**: Glicémia medida no momento, por tira ou sensor
            - **Glicémia Alvo**: Glicémia que se pretende atingir
            - **Fator Sensibilidade**: Quantidade de mg/dL que a glicémia desce com 1 unidade de insulina. É variável de pessoa para pessoa, e traduz a resistência à insulina. Deve ser calculado pelo médico
            - **Tendencia da Glicemia**: Tendencia da glicémia (medida pelo sensor), pode estar estável(↔), a subir(↗), a descer (↘), a subir rapidamente (↑) ou a descer rapidamente (↓)
            - **Equivalencia HC**: Quantidade (gramas) de hidratos de carbono que 1 unidade de insulina consegue metabolizar
            """
        )

    if "lista_alimentos" not in st.session_state:
        st.session_state["lista_alimentos"] = []
    if "dose_insulina" not in st.session_state:
        st.session_state["dose_insulina"] = 0
    if "equivalencia_hc_insulina" not in st.session_state:
        st.session_state["equivalencia_hc_insulina"] = 12
    if "fator_sensibilidade" not in st.session_state:
        st.session_state["fator_sensibilidade"] = 50
    if "glicemia" not in st.session_state:
        st.session_state["glicemia"] = 200
    if "glicemia_alvo" not in st.session_state:
        st.session_state["glicemia_alvo"] = 100
    if "tendencia_glicemia" not in st.session_state:
        st.session_state["tendencia_glicemia"] = "↔ estável"
    if "alimento" not in st.session_state:
        st.session_state["alimento"] = ""
    if "quantidade" not in st.session_state:
        st.session_state["quantidade"] = 0
    if "hc" not in st.session_state:
        st.session_state["hc"] = 0
    if "alimentos_radio" not in st.session_state:
        st.session_state["alimentos_radio"] = "Não"

    df_insa = load_data()
    # lista de alimentos
    lista_alimentos = df_insa["alimento_hc"]
    # st.table(df_insa[["Nome do alimento","Hidratos de carbono [g]"]].head(10))

    st.subheader(":blue[1. Correção de glicémia]")

    col_1, col_2, col_3 = st.columns(3)
    with col_1:
        st.session_state["glicemia"] = st.number_input(
            "Glicémia Actual (mg/dL)", value=200, step=5
        )
    with col_2:
        st.session_state["glicemia_alvo"] = st.number_input(
            "Glicémia Alvo (mg/dL)", value=100, step=5
        )

    with col_3:
        st.session_state["fator_sensibilidade"] = st.number_input(
            "Fator Sensibilidade", value=50, step=5
        )
    st.session_state["tendencia_glicemia"] = st.radio(
        "Tendencia da Glicemia",
        [
            "↑ subir rapidamente",
            "↗ subir",
            "↔ estável",
            "↘ descer",
            "↓ descer rapidamente",
        ],
        horizontal=True,
        index=2,
    )

    st.divider()
    st.subheader(":blue[2. Alimentos]")

    st.session_state["alimentos_radio"] = st.radio(
        "Incluir Alimentos no Cálculo",
        ["Não", "Hidratos de carbono", "Lista de alimentos"],
        horizontal=True,
        index=0,
        label_visibility="collapsed",
    )

    if st.session_state["alimentos_radio"] != "Não":
        st.session_state["equivalencia_hc_insulina"] = st.number_input(
            "Equivalencia HC", value=12, step=1
        )

    if st.session_state["alimentos_radio"] == "Hidratos de carbono":
        st.session_state["hc"] = 0
        st.session_state["hc"] = st.number_input(
            "Hidratos de Carbono (g)", value=0, step=1
        )

    if st.session_state["alimentos_radio"] == "Lista de alimentos":
        st.session_state["hc"] = 0
        col_5, col_6 = st.columns(2)
        with col_5:
            st.session_state["alimento"] = st.selectbox(
                "Alimento", lista_alimentos, index=0
            )
        with col_6:
            st.session_state["quantidade"] = st.number_input(
                "Quantidade (g)", value=50, step=5
            )

        col_but_1, col_but_2 = st.columns(2)
        with col_but_1:
            if st.button("adicionar alimento", type="secondary"):
                st.session_state["lista_alimentos"].append(
                    {
                        "Alimento": st.session_state["alimento"],
                        "Quantidade": st.session_state["quantidade"],
                    }
                )
        with col_but_2:
            if st.button("limpar lista", type="primary"):
                st.session_state["lista_alimentos"] = []

        st.write("Lista de alimentos")
        if len(st.session_state["lista_alimentos"]) != 0:
            st.session_state["lista_alimentos"] = st.data_editor(
                st.session_state["lista_alimentos"]
            )
            st.session_state["hc"] = calculo_hc(st.session_state["lista_alimentos"])

    if st.session_state["alimentos_radio"] == "Não":
        # reset hc se não existir alimentos (checkbox desmarcado)
        st.session_state["hc"] = 0
    st.divider()

    st.subheader(":red[Dose de Insulina a administrar]")

    insulina = calculo_insulina(
        st.session_state["equivalencia_hc_insulina"],
        st.session_state["fator_sensibilidade"],
        st.session_state["glicemia"],
        st.session_state["glicemia_alvo"],
        st.session_state["tendencia_glicemia"],
        st.session_state["hc"],
    )

    st.metric("Dose Insulina", insulina)

    with st.expander("Detalhes de cálculo"):
        st.write(
            detalhes_calculo(
                st.session_state["equivalencia_hc_insulina"],
                st.session_state["fator_sensibilidade"],
                st.session_state["glicemia"],
                st.session_state["glicemia_alvo"],
                st.session_state["tendencia_glicemia"],
                st.session_state["hc"],
            )
        )


# Press the green button in the gutter to run the script.
if __name__ == "__main__":
    main()
