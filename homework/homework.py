"""
Escriba el codigo que ejecute la accion solicitada.
"""

# pylint: disable=import-outside-toplevel

from zipfile import ZipFile
import os
import pandas as pd

def clean_campaign_data():
    """
    En esta tarea se le pide que limpie los datos de una campaña de
    marketing realizada por un banco, la cual tiene como fin la
    recolección de datos de clientes para ofrecerls un préstamo.

    La información recolectada se encuentra en la carpeta
    files/input/ en varios archivos csv.zip comprimidos para ahorrar
    espacio en disco.

    Usted debe procesar directamente los archivos comprimidos (sin
    descomprimirlos). Se desea partir la data en tres archivos csv
    (sin comprimir): client.csv, campaign.csv y economics.csv.
    Cada archivo debe tener las columnas indicadas.

    Los tres archivos generados se almacenarán en la carpeta files/output/.

    client.csv:
    - client_id
    - age
    - job: se debe cambiar el "." por "" y el "-" por "_"
    - marital
    - education: se debe cambiar "." por "_" y "unknown" por pd.NA
    - credit_default: convertir a "yes" a 1 y cualquier otro valor a 0
    - mortage: convertir a "yes" a 1 y cualquier otro valor a 0

    campaign.csv:
    - client_id
    - number_contacts
    - contact_duration
    - previous_campaing_contacts
    - previous_outcome: cmabiar "success" por 1, y cualquier otro valor a 0
    - campaign_outcome: cambiar "yes" por 1 y cualquier otro valor a 0
    - last_contact_day: crear un valor con el formato "YYYY-MM-DD",
        combinando los campos "day" y "month" con el año 2022.

    economics.csv:
    - client_id
    - const_price_idx
    - eurobor_three_months



    """

    meses = {
        "jan": "01", "feb": "02", "mar": "03", "apr": "04",
        "may": "05", "jun": "06", "jul": "07", "aug": "08",
        "sep": "09", "oct": "10", "nov": "11", "dec": "12"
    }

    carpeta_entrada = os.path.join("files", "input")
    carpeta_salida = os.path.join("files", "output")
    archivos_zip = [archivo for archivo in os.listdir(carpeta_entrada) if archivo.endswith(".zip")]
    todos_los_datos = []
    for archivo_zip in archivos_zip:
        ruta_zip = os.path.join(carpeta_entrada, archivo_zip)
        with ZipFile(ruta_zip) as zip_ref:
            with zip_ref.open(zip_ref.namelist()[0]) as archivo_csv:
                datos = pd.read_csv(archivo_csv)
                if "Unnamed: 0" in datos.columns:
                    datos = datos.drop(columns=["Unnamed: 0"])
                todos_los_datos.append(datos)
    datos_completos = pd.concat(todos_los_datos, ignore_index=True)
    clientes = datos_completos[["client_id", "age", "job", "marital", "education", "credit_default", "mortgage"]]
    clientes["job"] = clientes["job"].str.replace(".", "", regex=False).str.replace("-", "_", regex=False)
    clientes["education"] = clientes["education"].replace("unknown", pd.NA).str.replace("-", "_", regex=False).str.replace(".", "_", regex=False)
    clientes["credit_default"] = clientes["credit_default"].apply(lambda x: 1 if x == "yes" else 0)
    clientes["mortgage"] = clientes["mortgage"].apply(lambda x: 1 if x == "yes" else 0)
    campania = datos_completos[["client_id", "number_contacts", "contact_duration", "previous_campaign_contacts", "previous_outcome", "campaign_outcome", "month", "day"]]
    campania["month"] = campania["month"].apply(lambda x: meses.get(x.lower(), "00"))
    campania["previous_outcome"] = campania["previous_outcome"].apply(lambda x: 1 if x == "success" else 0)
    campania["campaign_outcome"] = campania["campaign_outcome"].apply(lambda x: 1 if x == "yes" else 0)
    campania["last_contact_date"] = "2022-" + campania["month"].str.zfill(2) + "-" + campania["day"].astype(str).str.zfill(2)
    campania = campania.drop(columns=["month", "day"])
    economia = datos_completos[["client_id", "cons_price_idx", "euribor_three_months"]]
    if not os.path.exists(carpeta_salida):
        os.makedirs(carpeta_salida)
    clientes.to_csv(os.path.join(carpeta_salida, "client.csv"), index=False)
    campania.to_csv(os.path.join(carpeta_salida, "campaign.csv"), index=False)
    economia.to_csv(os.path.join(carpeta_salida, "economics.csv"), index=False)


if __name__ == "__main__":
    clean_campaign_data()
