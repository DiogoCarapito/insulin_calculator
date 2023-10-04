import pandas as pd


df_insa = pd.read_excel("insa_tca.xlsx")

# remove 2nd row a header
df_insa.columns = df_insa.iloc[0]

# remove 1st row
df_insa = df_insa.iloc[1:]

# get the column nname with the HC (it has some special characters)
coluna_hc = df_insa.columns[13]

# create a new column with the name of the food and the HC per 100g
df_insa["alimento_hc"] = df_insa.apply(
    lambda row: f"{row['Nome do alimento']} ({row[coluna_hc]}g HC/100g)", axis=1
)

# save the dataframe to a csv file
df_insa.to_csv("insa_tca_processed.csv", index=False)

# create a new dataframe with the food name and the HC per 100g
df_insa_hc = df_insa[["Nome do alimento", 'Hidratos de carbono \n[g]']]

#print(df_insa.columns)

# Save the dataframe to a csv file
df_insa_hc.to_csv("insa_lista_alimentos_hidratos.csv", index=False)
