import streamlit as st
from utils.utils import load_data, calculo_insulina, calculo_hc, detalhes_calculo


def main():
    # title
    st.title("Calculadora de Dose de Insulina")

    # sidebar
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

    # session state variables
    # lista de alimentos
    if "lista_alimentos" not in st.session_state:
        st.session_state["lista_alimentos"] = []

    # dose insulina
    if "dose_insulina" not in st.session_state:
        st.session_state["dose_insulina"] = 0

    # equivalencia hidratos de carbono por unidade de insulina
    if "equivalencia_hc_insulina" not in st.session_state:
        st.session_state["equivalencia_hc_insulina"] = 12

    # fator sensibilidade
    if "fator_sensibilidade" not in st.session_state:
        st.session_state["fator_sensibilidade"] = 50

    # glucemia
    if "glicemia" not in st.session_state:
        st.session_state["glicemia"] = 200

    # glicemia alvo
    if "glicemia_alvo" not in st.session_state:
        st.session_state["glicemia_alvo"] = 100

    # tendencia da glicemia
    if "tendencia_glicemia" not in st.session_state:
        st.session_state["tendencia_glicemia"] = "↔ estável"

    # alimento
    if "alimento" not in st.session_state:
        st.session_state["alimento"] = ""

    # quantidade
    if "quantidade" not in st.session_state:
        st.session_state["quantidade"] = 0

    # hidratos carbono
    if "hc" not in st.session_state:
        st.session_state["hc"] = 0

    # radio se alimentos estão selecionados ou não
    if "alimentos_radio" not in st.session_state:
        st.session_state["alimentos_radio"] = "Não"

    # load lista alimentos
    df_insa = load_data()

    # lista de alimentos
    lista_alimentos = df_insa["alimento_hc"]

    st.subheader(":blue[1. Correção de glicémia]")

    col_1, col_2, col_3 = st.columns(3)
    with col_1:
        # input glicémia
        st.session_state["glicemia"] = st.number_input(
            "Glicémia Actual (mg/dL)", value=200, step=5
        )
    with col_2:
        # input glicemia alvo
        st.session_state["glicemia_alvo"] = st.number_input(
            "Glicémia Alvo (mg/dL)", value=100, step=5
        )

    with col_3:
        # input fator sensibilidade
        st.session_state["fator_sensibilidade"] = st.number_input(
            "Fator Sensibilidade", value=50, step=5
        )

    # input tendencia glicémia
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

    # secção de alimentos
    st.subheader(":blue[2. Alimentos (opcional)]")

    # opção se incluit alimentos ou não
    st.session_state["alimentos_radio"] = st.radio(
        "Incluir Alimentos no Cálculo",
        ["Não", "Hidratos de carbono", "Lista de alimentos"],
        horizontal=True,
        index=0,
        label_visibility="collapsed",
    )

    # se incluir calculo com alimentos, então

    if st.session_state["alimentos_radio"] != "Não":
        # input equivalencia de hidratos de carbono por unidade de insulina
        st.session_state["equivalencia_hc_insulina"] = st.number_input(
            "Equivalencia HC", value=12, step=1
        )

    # se só informação de hidratos de carbono totais
    if st.session_state["alimentos_radio"] == "Hidratos de carbono":
        # reset hidratos carbono
        st.session_state["hc"] = 0
        # input hidratos de carbono
        st.session_state["hc"] = st.number_input(
            "Hidratos de Carbono (g)", value=0, step=1
        )
    # se opºção de introdução de lista de alimentos
    if st.session_state["alimentos_radio"] == "Lista de alimentos":
        # reset hidratos carbono
        st.session_state["hc"] = 0

        col_5, col_6 = st.columns(2)
        with col_5:
            # input alimento
            st.session_state["alimento"] = st.selectbox(
                "Alimento", lista_alimentos, index=0
            )
        with col_6:
            # input quantidade
            st.session_state["quantidade"] = st.number_input(
                "Quantidade (g)", value=50, step=5
            )

        col_but_1, col_but_2 = st.columns(2)
        with col_but_1:
            # botão para adicionar alimento à lista de alimentos
            if st.button("adicionar alimento", type="secondary"):
                st.session_state["lista_alimentos"].append(
                    {
                        "Alimento": st.session_state["alimento"],
                        "Quantidade": st.session_state["quantidade"],
                    }
                )
        with col_but_2:
            # botão para limpar lista de alimentos
            if st.button("limpar lista", type="primary"):
                st.session_state["lista_alimentos"] = []

        # mostar lista de alimentos se existirem aliemntos na lista
        st.write("Lista de alimentos")
        if len(st.session_state["lista_alimentos"]) != 0:
            # utilização de tablea data_editor para possibiliadde de alterar valores de quantidae
            st.session_state["lista_alimentos"] = st.data_editor(
                st.session_state["lista_alimentos"]
            )
            st.session_state["hc"] = calculo_hc(st.session_state["lista_alimentos"])

    # caso não se queira calcular com aliemtnos
    if st.session_state["alimentos_radio"] == "Não":
        # reset hc se não existir alimentos (checkbox desmarcado)
        st.session_state["hc"] = 0
    st.divider()

    st.subheader(":green[Dose de Insulina a administrar]")

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
