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

    dose_insulina *= correcao_tendencia_glicemia(tendencia_glicemia)

    # round to 1 decimal (maybe 0 is better)
    dose_insulina = round(dose_insulina, 1)

    # return only positive values
    if dose_insulina < 0:
        return 0
    else:
        return dose_insulina


def calculo_hc(lista_alimentos):
    hc = 0
    for alimento in lista_alimentos:
        df_insa = load_data()

        hc_por_100 = df_insa[df_insa["Nome do alimento"] == alimento["Alimento"]][
            df_insa.columns[1]
        ].values[0]

        hc += alimento["Quantidade"] * hc_por_100 / 100

    return hc


def correcao_tendencia_glicemia(tendencia_glicemia):
    # add the correction dose according to the glycemia and the trend
    if tendencia_glicemia == "↑ subir rapidamente":
        return 1.2
    elif tendencia_glicemia == "↗ subir":
        return 1.1
    elif tendencia_glicemia == "↓ descer rapidamente":
        return 0.8
    elif tendencia_glicemia == "↘ descer":
        return 0.9
    else:
        return 1

def detalhes_calculo(
    equivalencia_hc_insulina,
    fator_sensibilidade,
    glicemia,
    glicemia_alvo,
    tendencia_glicemia,
    hidratos_carbono,
):
    insulina_correção_glicémia = correcao_glicemia(fator_sensibilidade, glicemia, glicemia_alvo)

    calculos_correcao_glicemia = f"""
#### A. Correção de Glicémia

Fórmula:

```
dose_insulina = (glicémia - glicémia_alvo) / fator_sensibilidade
```

*Neste caso:*

```
gliemia = {glicemia}
glicemia_alvo = {glicemia_alvo}
fator_sensibilidade = {fator_sensibilidade}

dose_insulina = ({glicemia} - {glicemia_alvo}) / {fator_sensibilidade}
dose_insulina = {insulina_correção_glicémia}
```
    
"""
    calculos_corrrecao_alimentos = """
#### B. Correção de Alimentos
"""
    if hidratos_carbono != 0:
        dose_adicional_alimentos = round(formula_insulina_hc(equivalencia_hc_insulina, hidratos_carbono), 2)
        calculos_corrrecao_alimentos += f"""
Fórmula:
```
dose_insulina_alimentos = hidratos_carbono / equivalencia_hidratos_carbono
```
*Neste caso:*
```
hidratos_carbono = {hidratos_carbono}
equivalencia_hidratos carbono = {equivalencia_hc_insulina}

dose_insulina_alimentos = {hidratos_carbono} / {equivalencia_hc_insulina}

dose_insulina_alimentos = {dose_adicional_alimentos}

dose_insulina = {insulina_correção_glicémia} + {dose_adicional_alimentos}
```
"""
    else:
        dose_adicional_alimentos = 0
        calculos_corrrecao_alimentos += f"""Sem alimentos selecionados"""

    correcao_tendencia = correcao_tendencia_glicemia(tendencia_glicemia)

    dose_final_insulina = (insulina_correção_glicémia + dose_adicional_alimentos) * correcao_tendencia

    dose_final_insulina_round = round(dose_final_insulina, 1)

    calculos_correrecao_tendencia = f"""
#### C. Correção de Tendência
Fator de correção consoante a têndiencia da glicémia:
- ↔ estável: não alterar
- ↗ subir: aumentar 10%
- ↘ descer: diminuir 10%
- ↑ subir rapidamente: aumentar 20%
- ↓ descer rapidamente: diminuir 20%

Pelo que:
```
dose_insulina = dose_insulina x fator_correcao_tendencia
```

*Neste caso:*
```
tendencia_glicemia = {tendencia_glicemia}
fator_correcao_tendencia = {correcao_tendencia}

dose_insulina = {insulina_correção_glicémia + dose_adicional_alimentos} * {correcao_tendencia}
dose_insulina = {dose_final_insulina}
```
"""

    dose_final = f"""
#### Dose final de insulina = {dose_final_insulina_round} Unidades
    """

    return calculos_correcao_glicemia + calculos_corrrecao_alimentos + calculos_correrecao_tendencia + dose_final
