import pandas as pd

# Cargar los archivos
homicidios = pd.read_csv("data/processed/homicidios_canton.csv")
femicidios = pd.read_csv("data/processed/femicidios_canton.csv")
denuncias = pd.read_csv("data/processed/denuncias_prov.csv")

# Identificar columnas de fecha (todas excepto las 2 primeras)
fecha_cols = homicidios.columns[2:]

# Melt (pivotar) los datos
homicidios_long = pd.melt(homicidios, id_vars=['provincia', 'cantón'], value_vars=fecha_cols,
                          var_name='fecha', value_name='homicidios')
femicidios_long = pd.melt(femicidios, id_vars=['provincia', 'cantón'], value_vars=fecha_cols,
                          var_name='fecha', value_name='femicidios')
denuncias_long = pd.melt(denuncias, id_vars=['provincia', 'delitos_de_mayor_incidencia'], value_vars=fecha_cols,
                         var_name='fecha', value_name='denuncias')

# Convertir fechas a tipo datetime
homicidios_long['fecha'] = pd.to_datetime(homicidios_long['fecha'], format='%b-%y')
femicidios_long['fecha'] = pd.to_datetime(femicidios_long['fecha'], format='%b-%y')
denuncias_long['fecha'] = pd.to_datetime(denuncias_long['fecha'], format='%b-%y')

# Guardar los archivos reformateados para usarlos en análisis EDA
homicidios_long.to_csv("data/processed/homicidios_canton_long.csv", index=False)
femicidios_long.to_csv("data/processed/femicidios_canton_long.csv", index=False)
denuncias_long.to_csv("data/processed/denuncias_prov_long.csv", index=False)
