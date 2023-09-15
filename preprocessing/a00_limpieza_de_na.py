# %% [markdown]
# # Plan de Trabajo
# 

# %% [markdown]
# Deberás realizar un análisis exploratorio de datos. Al final de Jupyter Notebook, escribe: Una lista de preguntas aclaratorias.
# 
# Un plan aproximado para resolver la tarea, que especifica de 3 a 5 pasos básicos y los explica en uno o dos enunciados El líder del equipo revisará tus preguntas y plan de trabajo.
# 
# Las preguntas serán respondidas durante una videollamada. El código será revisado por el líder del equipo solo si hay algunas dudas.
# 
# Haz el proyecto en tu ordenador y súbelo cuando hayas terminado. Si tienes algún problema, intenta usar nuestra interfaz.

# %% [markdown]
# # Proyecto Final

# %% [markdown]
# Al operador de telecomunicaciones Interconnect le gustaría poder pronosticar su tasa de cancelación de clientes. Si se descubre que un usuario o usuaria planea irse, se le ofrecerán códigos promocionales y opciones de planes especiales. El equipo de marketing de Interconnect ha recopilado algunos de los datos personales de sus clientes, incluyendo información sobre sus planes y contratos.
# 
# ### Servicios de Interconnect
# 
# Interconnect proporciona principalmente dos tipos de servicios:
# 
# 1. Comunicación por teléfono fijo. El teléfono se puede conectar a varias líneas de manera simultánea.
# 2. Internet. La red se puede configurar a través de una línea telefónica (DSL, *línea de abonado digital*) o a través de un cable de fibra óptica.
# 
# Algunos otros servicios que ofrece la empresa incluyen:
# 
# - Seguridad en Internet: software antivirus (*ProtecciónDeDispositivo*) y un bloqueador de sitios web maliciosos (*SeguridadEnLínea*).
# - Una línea de soporte técnico (*SoporteTécnico*).
# - Almacenamiento de archivos en la nube y backup de datos (*BackupOnline*).
# - Streaming de TV (*StreamingTV*) y directorio de películas (*StreamingPelículas*)
# 
# La clientela puede elegir entre un pago mensual o firmar un contrato de 1 o 2 años. Puede utilizar varios métodos de pago y recibir una factura electrónica después de una transacción.
# 
# ### Descripción de los datos
# 
# Los datos consisten en archivos obtenidos de diferentes fuentes:
# 
# - `contract.csv` — información del contrato;
# - `personal.csv` — datos personales del cliente;
# - `internet.csv` — información sobre los servicios de Internet;
# - `phone.csv` — información sobre los servicios telefónicos.
# 
# En cada archivo, la columna `customerID` (ID de cliente) contiene un código único asignado a cada cliente. La información del contrato es válida a partir del 1 de febrero de 2020.

# %% [markdown]
# ## 1. Preparación de los Datos

# %%
# INSTALAMOS LAS LIBRERIAS

!pip install sidetable

# %%
# CARGAMOS LAS LIBRERIAS

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import sidetable as stb
from functools import reduce

# %%
# CARGAMOS LA DATA

try:
    contract = pd.read_csv('e:\\Users\\Admin\\Desktop\\Python Projects\\contract.csv')
    internet = pd.read_csv('e:\\Users\\Admin\\Desktop\\Python Projects\\internet.csv')
    personal = pd.read_csv('e:\\Users\\Admin\\Desktop\\Python Projects\\personal.csv')
    phone = pd.read_csv('e:\\Users\\Admin\\Desktop\\Python Projects\\phone.csv')

except: 
    contract = pd.read_csv('/datasets/final_provider/contract.csv')
    internet = pd.read_csv('/datasets/final_provider/internet.csv')
    personal = pd.read_csv('/datasets/final_provider/personal.csv')
    phone = pd.read_csv('/datasets/final_provider/phone.csv')



internet_clean = internet

internet_clean.to_csv("files/datasets/intermedia/a00_internet_clean.csv")
personal_clean.to_csv("files/datasets/intermedia/a00_personal_clean.csv")

# %% [markdown]
# ### 1.1 Información General de 'contract'

# %%
# MOSTRAMOS UNA VISTA PREVIA

contract.sample(5)

# %%
# MODIFICAMOS LOS NOMBRES DE LAS COLUMNAS

contract_nombres = {
    'customerID': 'customer_id',
    'BeginDate': 'begin_date',
    'EndDate': 'end_date',
    'Type': 'type',
    'PaperlessBilling': 'paperless_billing',
    'PaymentMethod': 'payment_method',
    'MonthlyCharges': 'monthly_charges',
    'TotalCharges': 'total_charges'
}

contract.rename(columns = contract_nombres, inplace = True)

contract.head()

# %% [markdown]
# Tenemos la siguiente información:
#     
# * **customer_id**: código único para cada cliente.
# 
# * **begin_date**: fecha en donde se suscribe el cliente.
#     
# * **end_date**: fecha en donde finaliza la suscripción el cliente.
#     
# * **type**: tipo de contrato, mensual o anual.
#     
# * **paperless_billing**: tipo de envío de factura, electrónica o por correo.
#     
# * **monthly_charges**: precio de la cuota mensual en dólares.
#     
# * **total_charges**: monto total que el cliente ha pagado en la suscripción.

# %%
# MOSTRAMOS INFORMACION GENERAL 

contract.info()

# %% [markdown]
# **Nota**: 
# 
# * La columna total_charges específica información en dólares, debido que es la facturación cobrada a cada usuario, se procederá a cambiar su tipo de 'object' a 'float'.
# 
# * Las columnas begin_date y end_date son de tipo object, mostrando información en fechas, se procederá a cambiarlas a tipo datetime.

# %%
# MODIFICAMOS EL TIPO DE LA COLUMNA 'total_charges'

contract['total_charges'] = pd.to_numeric(contract['total_charges'], errors = 'coerce')

# %% [markdown]
# **Nota**: en un principio, cuando total_charges era object, la columna no presentaba valores ausentes. Pues, cuando se cambio a tipo float, presenta valores ausentes, estos se trataran mas adelante.

# %%
# MOSTRAMOS LOS VALORES AUSENTES

contract.isna().sum()

# %%
# MOSTRAMOS INFORMACIÓN ESTADÍSTICA

contract.describe()

# %% [markdown]
# #### Conclusiones Intermedias de 'contract'

# %% [markdown]
# * El promedio de la mensualidad de los clientes es de 64.76 dólares.
# * El promedio que la facturación pagada de los clientes es de 2283.30 dólares.
# * La factura más baja es de 18.25 dólares mensual y pagada es de 18.80 dólares, lo cual puede traducirse a que existen clientes que solo abonaron un mes.
# * La columna 'total_charges' era de tipo 'objet' y se cambio a tipo 'float'.
# * En la columna 'total_charges' tenemos valores ausentes, con un total de 11 después del cambio de tipo.

# %% [markdown]
# ### 1.2 Información General de 'internet'

# %%
# MOSTRAMOS UNA VISTA PREVIA

internet.sample(5)

# %%
# MODIFICAMOS LOS NOMBRES DE LAS COLUMNAS

internet_nombres = {
    'customerID': 'customer_id',
    'InternetService': 'internet_service',
    'OnlineSecurity': 'online_security',
    'OnlineBackup': 'online_backup',
    'DeviceProtection': 'device_protection',
    'TechSupport': 'tech_support',
    'StreamingTV': 'streaming_tv',
    'StreamingMovies': 'streaming_movies'
}

internet.rename(columns = internet_nombres, inplace = True)

internet.head()

# %% [markdown]
# Tenemos la siguiente información:
# 
# **customer_id**: código único para cada cliente que se suscribio al paquete de Internet.
# 
# **internet_service**: tipo de Internet, DSL o fibra óptica.
# 
# **online_security**: si utiliza bloqueador de sitios web.
# 
# **online_backup**: si utiliza almacenamiento en la nube.
# 
# **device_protection**: si utiliza antivirus.
# 
# **tech_support**: si utiliza asistencia técnica dedicada.
# 
# **streaming_tv**: si contrato el servicio de streaming para TV.
# 
# **streaming_movies**: si contrato el servicio de ver películas.

# %%
# MOSTRAMOS INFORMACION GENERAL 

internet.info()

# %%
# MOSTRAMOS INFORMACIÓN ESTADÍSTICA

internet.describe()

# %% [markdown]
# #### Conclusiones Intermedias de 'internet'

# %% [markdown]
# * Podemos observar que todos los tipos de las columnas son object.
# 
# * 6 de 8 columnas son de tendencia booleana, es decir, si o no. Podemos decir también que internet service presenta solo dos tipos: DSL y fibra óptica.
# 
# * No presenta valores ausentes.

# %% [markdown]
# ### 1.3 Información General de 'personal'

# %%
# MOSTRAMOS UNA VISTA PREVIA

personal.sample(5)

# %%
# MODIFICAMOS LOS NOMBRES DE LAS COLUMNAS

personal_nombres = {
    'customerID': 'customer_id',
    'SeniorCitizen': 'senior_citizen',
    'Partner': 'partner',
    'Dependents': 'dependents',
}

personal.rename(columns = personal_nombres, inplace = True)

personal.head()

# %% [markdown]
# Tenemos la siguiente información:
#     
# * **customer_id**: código único para cada cliente.
# 
# * **gender**: sexo de cada cliente.
#     
# * **senior_citizen**: si el cliente está jubilado o no.
#     
# * **partner**: si el cliente tiene pareja.
#     
# * **dependents**: si el cliente tiene personas a su cargo.

# %%
# MOSTRAMOS INFORMACION GENERAL 

personal.info()

# %%
# MOSTRAMOS INFORMACIÓN ESTADÍSTICA

personal.describe()

# %% [markdown]
# #### Conclusiones Intermedias de 'personal'

# %% [markdown]
# * Todas las columnas son de tipo object menos senior_citizen, que es int64.
# 
# * Es un dataset que muestra información categórica, como el sexo del cliente, si es jubilado o si dependen personas de él.

# %% [markdown]
# ### 1.4 Información General de 'phone'

# %%
# MOSTRAMOS UNA VISTA PREVIA

phone.sample(5)

# %%
# MODIFICAMOS LOS NOMBRES DE LAS COLUMNAS

phone_nombres = {
    'customerID': 'customer_id',
    'MultipleLines': 'multiple_lines',
}

phone.rename(columns = phone_nombres, inplace = True)

phone.head()

# %% [markdown]
# Tenemos la siguiente información:
#     
# * **customer_id**: código único para cada cliente que se suscribió al paquete de telefonía.
# 
# * **multiple_lines**: si el cliente tiene una o más líneas telefónicas.

# %%
# MOSTRAMOS INFORMACION GENERAL 

phone.info()

# %%
# MOSTRAMOS INFORMACIÓN ESTADÍSTICA

phone.describe()

# %% [markdown]
# #### Conclusiones Intermedias de 'phone'

# %% [markdown]
# * De igual manera con las columnas internet y personal, es una dataframe que muestra información categórica dándonos dos columnas de tipo objeto.

# %% [markdown]
# ## 2. Preparación de los Datos

# %%
# MOSTRAMOS UNA MUESTRA DEL 'contract'

contract.sample(5)

# %% [markdown]
# NOTA:
# 
# * Cabe destacar que en la columna 'end_date' la tenemos todavía como tipo object. ¿Por qué? Si la cambiamos a tipo datetime, no podríamos hacer lo siguiente:
# 
#     * Crearemos una nueva columna en 'contract' donde muestre la información si el cliente finalizó si o no la contratación de servicios con la empresa. La nueva columna, llamada 'fin_contrato' mostrará un 0 si el cliente no ha finalizado el contrato y 1 si ya lo finalizo.
#     * Mas adelante, cambiaremos los tipos de las columnas 'begin_date' y 'end_date' a datetime, recordando que eran de tipo object.
#     * Crearemos una nueva columna, llamada 'mes_suscript' que será el resultado de la resta entre la fecha entrante y de finalización de contrato, los cual nos data el total de meses de uso del servicio por cada cliente. Asimismo, tomando en cuenta la información del enunciado que es: " La información del contrato es válida a partir del 1 de febrero de 2020", utilizaremos ese dato para rellenar los valores ausentes, el dato es la resta entre esa fecha y la fecha inicial.

# %%
# DETERMINAMOS LA INFORMACIÓN DE LA COLUMNA 'fin_contrato'

contract['fin_contrato'] = (contract['end_date'] != 'No').astype('int')

contract.head(10)


# %%
# PROCEDEMOS A REALIZAR LOS CAMBIOS DE TIPO EN LAS COLUMNAS 'begin_date' y 'end_date'

contract['begin_date'] = pd.to_datetime(contract['begin_date'], errors = 'coerce')

contract['end_date'] = pd.to_datetime(contract['end_date'], errors = 'coerce')

# %%
# PROCEDEMOS A CREAR LA COLUMNA 'mes_suscript'

contract['mes_suscript'] = np.floor((contract.end_date - contract.begin_date)/np.timedelta64(1, 'M'))
contract['mes_suscript'] = contract['mes_suscript'].fillna(np.floor((pd.to_datetime('2020-02-01') - contract.begin_date)/np.timedelta64(1, 'M')))
contract.head()

# %%
# VEMOS A CLIENTES QUE YA HAN FINALIZADO SU CONTRADO

contract[contract['fin_contrato'] == 1]

# %% [markdown]
# ### 2.1 Fusionamos el Dataframe

# %%
# APLICAMOS 'merge' PARA CREAR UN NUEVO DATAFRAME COMPLETO

proyecto = [contract, internet, personal, phone]

df = reduce(lambda  left,right: pd.merge(left,right,on=['customer_id'],
                                            how='outer'), proyecto)

df.head()

# %%
# MOSTRAMOS INFORMACIÓN GENERAL DEL DATAFRAME

df.info()

# %% [markdown]
# **Nota**:
#     
# * Creamos un nuevo dataframe con todos la información para efectos de trabajar con mayor comodidad, donde especifica toda la información de cada cliente, pero nos enfrentamos a valores aunsentes, los cuales se resolverán a continuación.

# %% [markdown]
# ### 2.2 Tratamiento de Valores Ausentes

# %%
# MOSTRAMOS TODOS LOS VALORES AUSENTES

df.stb.missing()

# %%
# MOSTRAMOS SI EXISTEN VALORES DUPLICADOS

df.duplicated().sum()

# %%
# RELLENAMOS LOS VALORES AUSENTES

columnas_faltantes = ['online_security', 
             'internet_service', 
             'streaming_movies', 
             'streaming_tv', 
             'tech_support', 
             'device_protection',
             'online_backup',
             'multiple_lines']

for col in columnas_faltantes:
    df[col] = df[col].fillna('sin_registrar')

df.stb.missing()

# %% [markdown]
# **NOTA**: 
#     
# * Decidimos que, para efectos de esa información que es categórica, se especifique si no la hay, como 'sin_registrar'.

# %%
# OBSERVAMOS LAS FILAS DONDE EXISTEN VALORES AUSENTES EN LA COLUMNA 'total_charges', SIENDO 11 FILAS.

df.loc[df['total_charges'].isna()]

# %%
# FILTRAMOS A LOS CLIENTES QUE SOLO SE SUSCRIBIERON 1 MES.

df.loc[df['mes_suscript'] == 1]

# %%
# RELLENAMOS LA COLUMNA 'total_charges' CON LOS VALORES DE 'monthly_charges'

df['total_charges'].fillna(df[df['total_charges'].isna()]['monthly_charges'], inplace=True)  

df['total_charges'].isna().sum()

# %%
# REEMPLAZAMOS EL 0 EN 'mes_suscript' POR 1 Y CAMBIAMOS EL TIPO DE COLUMNA

df['mes_suscript'] = df['mes_suscript'].replace([0], 1).astype(int)

df.info()

# %% [markdown]
# **Conclusiones Intermedias**:
# 
# * Se procedió a rellenar los valores ausentes de la columna 'total_charges' con los valores de la facturación del primer mes, porque se supone o se piensa, que esta en el mes en curso y por eso aun en sistema no se ha cargado la factura. 
#     
# * Si se puede ver que hay valores ausentes en la columna 'end_date', significan que esos clientes aun no han finalizado contrato, es decir, no tienen fecha de culminación.
# 
# * Se cambió el tipo de la columna mes_suscript a int64.
# 
# * Se determinó un dataframe completo y no varios para efectos de trabajar con la aplicación de modelos y gráficas.

# %% [markdown]
# ## 3. Lista de Preguntas

# %% [markdown]
# 1. ¿Qué tan propensos son los jubilados a finalizar contrato?
# 
# 2. ¿Qué clientes son más propensos a finalizar contrato? ¿Los que tienen contrato mensual o anual?
# 
# 3. ¿Cuál método de pago es el que presenta mayor índice de finalización de contrato?
# 
# 4. ¿Cuál es el servicio de Internet que presenta más finalización de contratos?
# 
# 5. Los servicios que ofrece la empresa como soporte técnico y protección de equipos, ¿cuáles clientes tienen más finalización de contrato, los que los usan o no?
# 
# 6. Los clientes que poseen personas a cargo, ¿qué tendencia hay entre los que sí los tiene y los que no al finalizar contrato?

# %% [markdown]
# ## 4. Plan Aproximado para la Resolución de la Tarea

# %% [markdown]
# 1. Examinar con detenimiento que información del conjunto de datos se trabajará, específicar que columnas usaremos y cuales se desecharán. Asimismo, se decidirá cual sera la columna base para la división del conjunto de datos.
# 
# 2. Aplicar modelos de Machine Learning, donde se dividan el conjunto de datos en un 80:20 para el conjunto de entrenamiento y prueba. Posteriormente se aplicaran procesos de preparación de modelos, como serán las técnicas One Hot EnCoding y el Scaling y Upsampling, si amerita el caso.
# 
# 3. ¿Cuáles modelos se aplicarán? Pues, en este apartado, decidimos aplicar Regresión Logística, Arbol de Decisión, Bosque Aleatorio, CatBoost, XGBoost y las Redes Neuronales. Pensamos que con seis modelos podemos descrifrar buenos margenes en la puntuación ROC-AUC, que tiene que ser mayor al 85%.
# 
# 4. De último, se concluirá mostrando y comparando los resultados arrojados por los distintos modelos aplicados, se determinará cual es el mejor modelo y se redactará una informe expresando los resultados y las recomendaciones a la empresa, para efectos de que la gerencia tome decisiones en pro de evitar más fuga de clientes.

# %%



