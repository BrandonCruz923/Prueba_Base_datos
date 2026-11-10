import os
from supabase import create_client, Client
import cv2
import numpy as np


#Credenciales de base de datos
SUPABASE_URL= "https://lvxzqiepdhcgcgxyivak.supabase.co"
SUPABASE_KEY= "sb_publishable_eMyBHQaMyL37kRMnS54cVA_gAnB9Cxw"

#Conexion a base  de datos 
def coexion(URL, KEY):
    try:
        # Inicializar el cliente
        supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
        print("Existosa")
        return supabase
    except Exception as error:
        print(f"Error Al realizar La Conexion {error}")
        return None
    
def add_registro(supabase, ruta_imagen):
    # Abrir la imagen y leer en binario
    with open(ruta_imagen, "rb") as archivo:
        blod_data = archivo.read()
    insertar_imagen = {"nombre_img":ruta_imagen, "data_img":blod_data}
    insertar = supabase.table("galeria").insert(insertar_imagen).execute()
    print("Imagen Insertada")


#Obtner registros 
def obtner_registro(supabase,tabla, valor):
    #todos = supabase.table("galeria").select("*").execute()
    filtar = (
        supabase.table(tabla).
        select("data_img").
        gt("nombre_img", valor).
        execute()
    )
    image = filtar.data[0]["data_img"]
    return image

def convertir_binario_imagen(datos_bin):
    # Verificar el formato recibido
    if isinstance(datos_bin, str):
        # BYTEA hexadecimal de PostgreSQL
        if datos_bin.startswith("\\x"):
            bytes_reales = bytes.fromhex(datos_bin[2:])
        else:
            raise ValueError("Formato BYTEA no reconocido")
    elif isinstance(datos_bin, bytes):
        bytes_reales = datos_bin
    else:
        raise TypeError(f"Tipo no compatible: {type(datos_bin)}")
    # Convertir bytes a NumPy
    array_nump = np.frombuffer(bytes_reales,dtype=np.uint8)
    # Reconstruir imagen
    imagen = cv2.imdecode(array_nump,cv2.IMREAD_COLOR)
    if imagen is None:
        raise ValueError("No se pudo reconstruir la imagen")
    return imagen

# Recuperar imagen
def mostrar_img(image):
    # Mostrar imagen
    cv2.imshow("Imagen desde Supabase", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
def main():
    supabase = coexion(SUPABASE_URL, SUPABASE_KEY)
    if supabase is None:
        return

    try:
        print("CONSULTANDO REGISTRO...")
        datos = obtner_registro(
            supabase,
            "galeria",
            "imagenes.jpg"
        )
        print("CONSULTA REALIZADA")
        imagen = convertir_binario_imagen(datos)
        mostrar_img(imagen)

    except Exception as error:
        print("ERROR:", error)

if __name__ == "__main__":
    main()