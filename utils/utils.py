import pandas as pd


def load_data():
    return pd.read_csv("data/insa_lista_alimentos_hidratos.csv")


def formula_insulina_hc(equivalencia_hc_insulina, hc):
    insulina_para_correcao = hc / equivalencia_hc_insulina

    return insulina_para_correcao


def correcao_glicemia(fator_sensibilidade, glicemia, glicemia_alvo):
    insulina_para_correcao = (glicemia - glicemia_alvo) / fator_sensibilidade

    return insulina_para_correcao


def calculo_insulina(
    equivalencia_hc_insulina,
    fator_sensibilidade,
    glicemia,
    glicemia_alvo,
    tendencia_glicemia,
    hidratos_carbono,
):
    # insulin dose reset
    dose_insulina = 0

    if glicemia < 60:
        return 0

    dose_insulina += correcao_glicemia(fator_sensibilidade, glicemia, glicemia_alvo)

    dose_insulina += formula_insulina_hc(equivalencia_hc_insulina, hidratos_carbono)

    # add the correction dose according to the glycemia and the trend
    if tendencia_glicemia == "↑ subir rapidamente":
        dose_insulina *= 1.2
    elif tendencia_glicemia == "↗ subir":
        dose_insulina *= 1.1
    elif tendencia_glicemia == "↓ descer rapidamente":
        dose_insulina *= 0.8
    elif tendencia_glicemia == "↘ descer":
        dose_insulina *= 0.9

    # round to 1 decimal (maybe 0 is better)
    dose_insulina = round(dose_insulina, 1)

    return dose_insulina


def calculo_hc(lista_alimentos):
    hc = 0
    for alimento in lista_alimentos:
        df_insa = load_data()

        hc_por_100 = df_insa[df_insa["alimento_hc"] == alimento["Alimento"]][
            df_insa.columns[13]
        ].values[0]

        hc += alimento["Quantidade"] * hc_por_100 / 100

    return hc


def detalhes_calculo(
    equivalencia_hc_insulina,
    fator_sensibilidade,
    glicemia,
    glicemia_alvo,
    tendencia_glicemia,
    hidratos_carbono,
):
    return None
