import json
from pathlib import Path
import streamlit as st
import pandas as pd
import base64

def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Cambia "static/tu_foto_militar.jpeg" por la ruta real donde esté tu foto ahora mismo
# Si está en la misma carpeta que el script, pon solo "tu_foto_militar.jpeg"
try:
    bin_str = get_base64("static/tu_foto_militar.jpeg")
except:
    bin_str = "" # Por si falla que no rompa la app
# 1. CONFIGURACIÓN (SIEMPRE PRIMERO)
st.set_page_config(page_title="App Ejército 2026", page_icon="🇪🇸", layout="wide")
# 2. EL AJUSTE PARA MÓVIL (Copia y pega esto aquí)
st.markdown("""
<style>
    /* Arreglo para que los títulos de los botones no se corten */
    div[data-testid="stExpander"] summary p {
        font-size: clamp(14px, 4vw, 20px) !important; /* Tamaño adaptable */
        white-space: normal !important;
        line-height: 1.2 !important;
        font-weight: bold !important;
        color: #3B441E !important;
    }
    /* Ajuste para los botones de "Gestión de..." para que quepa el texto */
    .stElementContainer button {
        height: auto !important;
        padding-top: 10px !important;
        padding-bottom: 10px !important;
    }
    
    /* Forzar que el selector sea legible */
    .stSelectbox label p {
        color: #3B441E !important;
        font-weight: bold !important;
    }
    
    /* Dar más espacio a los botones y textos */
    .stButton button {
        width: 100% !important; /* Que el botón ocupe todo el ancho para que sea fácil dar con el dedo */
    }
    /* Si la pantalla es pequeña (móvil) */
    @media (max-width: 800px) {
        .titulo-top-gun, h1 {
            font-size: 45px !important; /* Baja de 120px a 45px en móvil */
            white-space: normal !important; /* Permite que el texto baje de línea si es necesario */
            text-align: center !important;
        }
        /* Ajustamos la bandera para que no tape el texto en móvil */
        img {
            width: 80px !important; 
        }
        div[style*="display: flex"] {
            flex-direction: column !important; /* Pone la bandera arriba y el texto abajo en móvil */
            gap: 10px !important;
        }
    }
</style>
""", unsafe_allow_html=True)
# 2. EL CAMUFLAJE MILITAR (CSS DEFINITIVO)
# --- MAQUILLAJE DEFINITIVO CON TU FOTO DE FONDO ---
st.markdown(f"""
    <style>
    /* 1. QUITAR MENÚS */
    [data-testid="stSidebar"], [data-testid="stSidebarNav"], .stSidebar {{display: none !important;}}
    button[kind="header"] {{display: none !important;}}
    header {{visibility: hidden !important;}}

    /* 2. TU FOTO DE FONDO (INCRUSTADA) */
    .stApp {{
        background: 
            linear-gradient(rgba(0, 0, 0, 0.7), rgba(0, 0, 0, 0.7)), 
            url("data:image/jpeg;base64,{bin_str}");
        background-size: cover !important;
        background-position: center !important;
        background-attachment: fixed !important;
    }}

    /* ESTO ARREGLA LAS LETRAS INVISIBLES EN MÓVIL */
    div[data-testid="stExpander"] summary p {{
        color: white !important;
        font-weight: bold !important;
    }}

    div[data-testid="stExpander"] div[role="region"] p, 
    div[data-testid="stExpander"] div[role="region"] li {{
        color: #f0f0f0 !important;
    }}

    /* 3. BANDERA DE ESPAÑA SUPERIOR */
    .stApp::before {{
        content: "";
        position: fixed;
        top: 0; left: 0; width: 100%; height: 12px;
        background: linear-gradient(to bottom, #AA151B 0%, #AA151B 33%, #F1BF00 33%, #F1BF00 66%, #AA151B 66%, #AA151B 100%);
        z-index: 999999;
    }}

    /* 4. TUS TARJETAS */
    .stExpander {{
        border: 2px solid #556b2f !important;
        border-radius: 15px !important;
        background-color: rgba(255, 255, 255, 0.9) !important;
        box-shadow: 0px 4px 15px rgba(0,0,0,0.3) !important;
        margin-bottom: 20px !important;
    }}
    </style>
    """, unsafe_allow_html=True)

# 3. BANDERA DE CABECERA (Imagen real, sutil pero clara)
st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/8/89/Bandera_de_Espa%C3%B1a.svg/1200px-Bandera_de_Espa%C3%B1a.svg.png", width=120)

st.markdown("---") # Una línea divisoria elegante

# --- FUNCIONES DE CÁLCULO (EL MOTOR) ---
def obtener_puntos(tipo_prueba, genero, edad, marca_usuario, data_json):
    """
    Busca en el JSON el tramo de edad y devuelve los puntos exactos.
    """
    # 1. Identificar el grupo de edad del JSON
    grupo_edad_final = None
    for grupo in data_json["age_groups"]:
        if "-" in grupo:
            inicio, fin = map(int, grupo.split("-"))
            if inicio <= edad <= fin:
                grupo_edad_final = grupo
                break
        elif "+" in grupo:
            inicio = int(grupo.replace("+", ""))
            if edad >= inicio:
                grupo_edad_final = grupo
                break

    if not grupo_edad_final:
        return 0 # Edad no contemplada

    # 2. Ir a la tabla del JSON (flexiones -> Hombre -> "17-25")
    try:
        lista_puntos = data_json["tables"][tipo_prueba][genero][grupo_edad_final]
        
        # 3. Recorrer la lista de arriba a abajo
        for tramo in lista_puntos:
            # Si la marca del usuario es MAYOR o IGUAL a la del JSON, esos son sus puntos
            if marca_usuario >= tramo["reps"]:
                return tramo["points"]
        
        return 0 # Si no llega ni al mínimo
    except KeyError:
        return 0



def mmss_to_seconds(t: str) -> int:
    t = t.strip()
    if ":" not in t: return 0
    m, s = t.split(":")
    return int(m) * 60 + int(s)

def load_paef_baremos() -> dict:
    path = Path(__file__).parent / "data" / "paef_baremos.json"
    if not path.exists():
        return {"age_groups": [], "tables": {}}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def puntos_flexiones(baremos, sexo, age_group, valor_input):
    try:
        num_reps = int(valor_input)
        tabla = baremos.get("tables", {}).get("flexiones", {}).get(sexo, {}).get(age_group, [])
        if not tabla and num_reps >= 21: return 100 # Red de seguridad
        for row in sorted(tabla, key=lambda x: int(x["reps"]), reverse=True):
            if num_reps >= int(row["reps"]): return int(row["points"])
        return 20 if num_reps >= 9 else 0
    except: return 0

def puntos_agilidad(baremos, sexo, age_group, valor_input):
    try:
        t_usuario = float(str(valor_input).replace(',', '.'))
        tabla = baremos.get("tables", {}).get("agilidad", {}).get(sexo, {}).get(age_group, [])
        for row in sorted(tabla, key=lambda x: float(x["time_sec"])):
            if t_usuario <= float(row["time_sec"]): return int(row["points"])
        return 0
    except: return 0

def puntos_2000m(baremos, sexo, age_group, tiempo_mmss):
    try:
        t_sec = mmss_to_seconds(tiempo_mmss)
        tabla = baremos.get("tables", {}).get("carrera_2000m", {}).get(sexo, {}).get(age_group, [])
        for row in sorted(tabla, key=lambda x: mmss_to_seconds(x["time_max"])):
            if t_sec <= mmss_to_seconds(row["time_max"]): return int(row["points"])
        return 0
    except: return 0

def puntos_plancha(baremos, sexo, age_group, tiempo_mmss):
    try:
        t_sec = mmss_to_seconds(tiempo_mmss)
        # Intentamos buscar en UNISEX, si no, en el sexo elegido
        tablas_plancha = baremos.get("tables", {}).get("plancha", {})
        tabla = tablas_plancha.get("UNISEX", {}).get(age_group, []) or tablas_plancha.get(sexo, {}).get(age_group, [])
        for row in sorted(tabla, key=lambda x: mmss_to_seconds(x["time_min"]), reverse=True):
            if t_sec >= mmss_to_seconds(row["time_min"]): return int(row["points"])
        return 0
    except: return 0

def obtener_marca_inversa(baremos, prueba_key, sexo, edad, puntos_objetivo):
    try:
        tablas_prueba = baremos.get("tables", {}).get(prueba_key, {})
        if prueba_key == "plancha" and "UNISEX" in tablas_prueba:
            tabla = tablas_prueba["UNISEX"].get(edad, [])
        else:
            tabla = tablas_prueba.get(sexo, {}).get(edad, [])
        
        if not tabla: return "No hay datos"
        
        if prueba_key in ["flexiones", "plancha"]:
            for row in sorted(tabla, key=lambda x: int(x["points"])):
                if int(row["points"]) >= puntos_objetivo:
                    return row.get("reps") or row.get("time_min")
        else:
            for row in sorted(tabla, key=lambda x: int(x["points"]), reverse=True):
                if int(row["points"]) >= puntos_objetivo:
                    return row.get("time_max") or row.get("time_sec")
        return "Marca no encontrada"
    except: return "Error"

# --- CUERPO PRINCIPAL (ESTRUCTURA DE BLOQUES) ---

st.write(f'<div style="display: flex; align-items: center; justify-content: center; gap: 30px;"><h1 style="font-size: clamp(40px, 8vw, 120px); font-family: Oswald, sans-serif; font-weight: 900; margin: 0; background: linear-gradient(to bottom, #bf9b30 0%, #f2d87e 50%, #bf9b30 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; filter: drop-shadow(4px 4px 0px #FF0000); text-transform: uppercase; line-height: 1.1; text-align: center;">SOMOS TU EJÉRCITO</h1></div>', unsafe_allow_html=True)
col_izq, col_der = st.columns(2)

# BLOQUE IZQUIERDO: ACCESO
with col_izq:
    with st.expander("🪖 FORMA PARTE DE NOSOTROS", expanded=False):              
       
        with st.expander("✅ Condiciones para participar en la Convocatoria"):
            st.markdown("### 📋 Requisitos Generales (Base Tercera)")                       
            col_req1, col_req2 = st.columns(2)           
            with col_req1:
                st.markdown("**🎂 Edad:**")
                st.write("- Tener cumplidos **18 años**.")
                st.write("- No cumplir **29 años** el día de incorporación al centro de formación.")                
                st.markdown("**🇪🇸 Nacionalidad:**")
                st.write("- Nacionalidad española o la de alguno de los países autorizados.")           
            with col_req2: # <--- Aquí estaba el fallo, ahora se llama igual que arriba
                st.markdown("**⚖️ Antecedentes y Justicia:**")
                st.write("- Carecer de antecedentes penales.")
                st.write("- No estar privado de derechos civiles.")
                st.write("- No estar procesado o imputado por delito doloso.")
            st.divider()
            
            st.markdown("**🚫 Otros Requisitos Críticos:**")
            st.info("""
            * **Tatuajes:** No se permiten los que sean contrarios a los valores constitucionales, autoridades o virtudes militares. 
            * **Expulsiones:** No haber sido expulsado de las FF.AA. por expediente disciplinario.
            * **Habilitación:** No estar inhabilitado para el ejercicio de funciones públicas.
            """)
            
            st.warning("⚠️ **Nota sobre la altura:** El BOE actual no establece una altura mínima general, pero algunas unidades operativas podrían tener requisitos específicos en el cuadro médico.")
        
        with st.expander("📅 Cita Previa para participar en el proceso de selección"):
            st.markdown("### 🔗 Gestión de Cita")
            st.write("La solicitud de cita previa se realiza de forma telemática en la Sede Electrónica de Defensa:")
            st.link_button("🌐 Solicitar Cita Previa (Oficial)", "https://sede.defensa.gob.es/acceda/index")           
            st.info("☎️ **Teléfonos oficiales (BOE):** 902 432 100 / 91 308 97 98")
            st.divider()
            st.markdown("### 📍 Sedes de las Unidades de Reconocimiento")
            st.write("Direcciones extraídas fielmente del **Apéndice 5** del BOE-A-2026-436:")           
            dict_provincias = {
                "01 ARABA/ALAVA (VITORIA)": "DIRECCIÓN: C/ Postas, 52-54. CÓDIGO POSTAL: 01004. TFNO. 945.25.14.33. EMAIL: reclutamientoalava@oc.mde.es",
                "02 ALBACETE": "DIRECCIÓN: Plaza de Gabriel Lodares, 2. CÓDIGO POSTAL: 02002. TFNO. 967.55.09.34. EMAIL: reclutamientoalbacete@oc.mde.es",
                "03 ALICANTE": "DIRECCIÓN: C/ Colombia, 3. CÓDIGO POSTAL: 03010. TFNO. 965.25.25.90 / 965.24.33.68. EMAIL: reclutamientoalicante@oc.mde.es",
                "04 ALMERÍA": "DIRECCIÓN: C/ General Luque, S/N. CÓDIGO POSTAL: 04002. TFNO. 950.23.21.03. EMAIL: reclutamientoalmeria@oc.mde.es",
                "05 ÁVILA": "DIRECCIÓN: Paseo de San Roque, 9. CÓDIGO POSTAL: 05003. TFNO. 920.35.20.88 / 920.35.22.60. EMAIL: reclutamientoavila@oc.mde.es",
                "06 BADAJOZ": "DIRECCIÓN: Avda. Fernando Calzadilla, 8. CÓDIGO POSTAL: 06004. TFNO. 924.20.79.46 / 924.20.79.47. EMAIL: reclutamientobadajoz@oc.mde.es",
                "07 ILLES BALEARS (PALMA DE MALLORCA)": "DIRECCIÓN: C/ Antonio Planas Franch n.º 9. CÓDIGO POSTAL: 07001. TFNO. 971.22.77.51 / 971.22.77.52. EMAIL: reclutamientobaleares@oc.mde.es",
                "08 BARCELONA": "DIRECCIÓN: C/ Tcol. González Tablas, s/n (Cuartel del Bruch). CÓDIGO POSTAL: 08034. TFNO. 932.80.44.44. EMAIL: reclutamientobarcelona@oc.mde.es",
                "09 BURGOS": "DIRECCIÓN: C/ Vitoria, 63. CÓDIGO POSTAL: 09006. TFNO. 947.24.53.77 / 947.24.53.35. EMAIL: reclutamientoburgos@oc.mde.es",
                "10 CÁCERES": "DIRECCIÓN: Avda. de las Delicias, s/n (Cuartel Infanta Isabel). CÓDIGO POSTAL: 10004. TFNO. 927.62.53.70. EMAIL: reclutamientocaceres@oc.mde.es",
                "11 CÁDIZ": "DIRECCIÓN: Paseo de Carlos III, 7. CÓDIGO POSTAL: 11003. TFNO. 956.21.04.21. EMAIL: reclutamientocadiz@oc.mde.es",
                "12 CASTELLÓN": "DIRECCIÓN: Avda. del Mar, 19. CÓDIGO POSTAL: 12003. TFNO. 964.27.02.52 / 964.27.01.33. EMAIL: reclutamientocastellon@oc.mde.es",
                "13 CIUDAD REAL": "DIRECCIÓN: C/ Toledo, 60. CÓDIGO POSTAL: 13003. TFNO. 926.27.43.20. EMAIL: reclutamientociudadreal@oc.mde.es",
                "14 CÓRDOBA": "DIRECCIÓN: Plaza de Ramón y Cajal, s/n. CÓDIGO POSTAL: 14003. TFNO. 957.49.69.47 / 957.49.69.46. EMAIL: reclutamientocordoba@oc.mde.es",
                "15 A CORUÑA": "DIRECCIÓN: Avda. Porto da Coruña, 15. CÓDIGO POSTAL: 15006. TFNO. 981.12.68.13 / 981.12.68.14. EMAIL: reclutamientoacoruna@oc.mde.es",
                "16 CUENCA": "DIRECCIÓN: Parque San Julián, 13. CÓDIGO POSTAL: 16002. TFNO. 969.24.18.70. EMAIL: reclutamientocuenca@oc.mde.es",
                "17 GIRONA": "DIRECCIÓN: C/ Emili Grahit, 4. CÓDIGO POSTAL: 17003. TFNO. 972.20.01.28. EMAIL: reclutamientogerona@oc.mde.es",
                "18 GRANADA": "DIRECCIÓN: C/ Santa Bárbara, 13. CÓDIGO POSTAL: 18071. TFNO. 958.80.62.50 / 958.80.62.52. EMAIL: reclutamientogranada@oc.mde.es",
                "19 GUADALAJARA": "DIRECCIÓN: C/ Plaza de España, s/n. CÓDIGO POSTAL: 19001. TFNO. 949.23.43.37 / 949.21.17.08. EMAIL: reclutamientoguadalajara@oc.mde.es",
                "20 GIPUZKOA (SAN SEBASTIAN)": "DIRECCIÓN: C/ Sierra de Aralar, 51-53. (Acuartelamiento de Loyola). CÓDIGO POSTAL: 20014. TFNO. 943.47.03.75. EMAIL: reclutamentogipuzkoa@oc.mde.es",
                "21 HUELVA": "DIRECCIÓN: C/ Sanlúcar de Barrameda, 2. CÓDIGO POSTAL: 21001. TFNO. 959.22.02.42. EMAIL: reclutamientohuelva@oc.mde.es",
                "22 HUESCA": "DIRECCIÓN: C/ Rioja, 1. CÓDIGO POSTAL: 22002. TFNO. 974.21.52.38 / 974.21.52.36 / 974.21.52.17. EMAIL: reclutamientohuesca@oc.mde.es",
                "23 JAÉN": "DIRECCIÓN: C/ Pintor Zabaleta, 2. CÓDIGO POSTAL: 23008. TFNO. 953.22.18.33. EMAIL: reclutamientojaen@oc.mde.es",
                "24 LEÓN": "DIRECCIÓN: C/ de la Policía Nacional, 7. CÓDIGO POSTAL: 24003. TFNO. 987.87.69.02. EMAIL: reclutamientoleon@oc.mde.es",
                "25 LLEIDA": "DIRECCIÓN: C/ Onofre Cerveró, 1. CÓDIGO POSTAL: 25004. TFNO. 973.23.09.85. EMAIL: reclutamientolleida@oc.mde.es",
                "26 LA RIOJA (LOGROÑO)": "DIRECCIÓN: C/ Comandancia, 6. CÓDIGO POSTAL: 26001. TFNO. 941.50.32.72. EMAIL: reclutamientolarioja@oc.mde.es",
                "27 LUGO": "DIRECCIÓN: C/ Ronda de la Muralla, 142, Bajo. CÓDIGO POSTAL: 27004. TFNO. 982.26.44.45. EMAIL: reclutamientolugo@oc.mde.es",
                "28 MADRID": "DIRECCIÓN: C/ Quintana, 5. CÓDIGO POSTAL: 28008. TFNO. 91.308.98.92 / 91.308.98.94. EMAIL: reclutamientomadrid@oc.mde.es",
                "29 MÁLAGA": "DIRECCIÓN: Paseo de La Farola, 10. CÓDIGO POSTAL: 29016. TFNO. 952.06.18.25 / 952.06.17.82. EMAIL: reclutamientomalaga@oc.mde.es",
                "30 MURCIA": "DIRECCIÓN: General San Martín, s/n. CÓDIGO POSTAL: 30003. TFNO. 968.22.60.80 / 968.22.60.73. EMAIL: reclutamientomurcia@oc.mde.es",
                "31 NAVARRA (PAMPLONA)": "DIRECCIÓN: C/ General Chinchilla, 10, 2.º. CÓDIGO POSTAL: 31002. TFNO. 948.20.76.30. EMAIL: reclutamientonavarra@oc.mde.es",
                "32 OURENSE": "DIRECCIÓN: C/ Paseo, 35. CÓDIGO POSTAL: 32003. TFNO. 988.21.22.00. EMAIL: reclutamientoourense@oc.mde.es",
                "33 ASTURIAS (OVIEDO)": "DIRECCIÓN: Plaza de España, 4. CÓDIGO POSTAL: 33007. TFNO. 985.96.25.11 / 985.96.25.43. EMAIL: reclutamientoasturias@oc.mde.es",
                "34 PALENCIA": "DIRECCIÓN: C/ Casado del Alisal, 2. CÓDIGO POSTAL: 34001. TFNO. 979.70.67.14 / 979.70.67.16. EMAIL: reclutamientopalencia@oc.mde.es",
                "35 LAS PALMAS": "DIRECCIÓN: C/ Sierra Nevada, s/n. (Las Palmas de Gran Canaria). (Risco de San Francisco). CÓDIGO POSTAL: 35014. TFNO. 928.43.26.66. EMAIL: reclutamientolaspalmas@oc.mde.es",
                "36 PONTEVEDRA": "DIRECCIÓN: Paseo de Cervantes, 3. CÓDIGO POSTAL: 36001. TFNO. 986.86.87.06 / 986.85.18.73. EMAIL: reclutamientopontevedra@oc.mde.es",
                "37 SALAMANCA": "DIRECCIÓN: C/ De los Ingenieros Zapadores, 23. CÓDIGO POSTAL: 37006. TFNO. 923.22.36.97 / 923.28.38.49 / 923.28.26.15. EMAIL: reclutamientosalamanca@oc.mde.es",
                "38 SANTA CRUZ DE TENERIFE": "DIRECCIÓN: Avda. 25 de Julio, 3 Bajo. CÓDIGO POSTAL: 38004. TFNO. 922.29.39.00. EMAIL: reclutamientotenerife@oc.mde.es",
                "39 CANTABRIA (SANTANDER)": "DIRECCIÓN: Plaza Velarde, s/n. CÓDIGO POSTAL: 39001. TFNO. 942.31.17.89. EMAIL: reclutamientocantabria@oc.mde.es",
                "40 SEGOVIA": "DIRECCIÓN: C/ Puente de Sancti Spiritus, 2. CÓDIGO POSTAL: 40002. TFNO. 921.46.11.53. EMAIL: reclutamientosegovia@oc.mde.es",
                "41 SEVILLA": "DIRECCIÓN: Avda. Eduardo Dato, 21. CÓDIGO POSTAL: 41005. TFNO. 954.98.85.21 / 954.98.84.79. EMAIL: reclutamientosevilla@oc.mde.es",
                "42 SORIA": "DIRECCIÓN: Avda. Duques de Soria, 16 bajo. CÓDIGO POSTAL: 42003. TFNO. 975 23 92 52. EMAIL: reclutamientosoria@oc.mde.es",
                "43 TARRAGONA": "DIRECCIÓN: Rambla Vella, 4. CÓDIGO POSTAL: 43003. TFNO. 977.24.98.47. EMAIL: reclutamientotarragona@oc.mde.es",
                "44 TERUEL": "DIRECCIÓN: Avda. de Sagunto, 11. CÓDIGO POSTAL: 44002. TFNO. 978.61.87.30. EMAIL: reclutamientoteruel@oc.mde.es",
                "45 TOLEDO": "DIRECCIÓN: C/ Duque de Lerma, 6. CÓDIGO POSTAL: 45004. TFNO. 925.28.33.71 / 925.28.33.69 / 925.28.42.35. EMAIL: reclutamientotoledo@oc.mde.es",
                "46 VALENCIA": "DIRECCIÓN: Paseo de la Alameda, 28. CÓDIGO POSTAL: 46010. TFNO. 961.96.34.00. EMAIL: reclutamientovalencia@oc.mde.es",
                "47 VALLADOLID": "DIRECCIÓN: C/ Fray Luis de León, 7. CÓDIGO POSTAL: 47002. TFNO. 983.20.38.12. EMAIL: reclutamientovalladolid@oc.mde.es",
                "48 BIZKAIA (BILBAO)": "DIRECCIÓN: C/ Urizar, 13. CÓDIGO POSTAL: 48012. TFNO. 944.70.66.50 / 944.70.66.66. EMAIL: reclutamientovizcaya@oc.mde.es",
                "49 ZAMORA": "DIRECCIÓN: Avda. Requejo, 14, Bajo. CÓDIGO POSTAL: 49030. TFNO. 980.52.26.85. EMAIL: reclutamientozamora@oc.mde.es",
                "50 ZARAGOZA": "DIRECCIÓN: Paseo del Canal, 1. CÓDIGO POSTAL: 50007. TFNO. 976.25.53.75. EMAIL: reclutamientozaragoza@oc.mde.es",
                "51 CEUTA": "DIRECCIÓN: C/ Marina Española, 12 Bajo. CÓDIGO POSTAL: 51001. TFNO. 856.20.05.08 / 856.20.05.09. EMAIL: dd.ceuta@oc.mde.es",
                "52 MELILLA": "DIRECCIÓN: C/ Gabriel de Morales, 5. CÓDIGO POSTAL: 52002. TFNO. 952.69.03.36. EMAIL: reclutamientomelilla@oc.mde.es",
                "ALGECIRAS (CÁDIZ)": "DIRECCIÓN: Avda. Hispanidad, 8. CÓDIGO POSTAL: 11207. TFNO. 956.58.76.35.",
                "CARTAGENA (MURCIA)": "DIRECCIÓN: C/ Real, 20, Bajo. CÓDIGO POSTAL: 30201. TFNO. 968.52.35.27.",
                "FERROL (A CORUÑA)": "DIRECCIÓN: C/ Cuntis, 26-28. CÓDIGO POSTAL: 15403. TFNO. 981.33.05.87."
            }
            prov_sel = st.selectbox("Selecciona tu Provincia", sorted(list(dict_provincias.keys())))
            st.success(f"📍 **Dirección Oficial (Apéndice 5):**\n\n {dict_provincias[prov_sel]}")
        
        
        
        with st.expander("📄 Documentación Previa Necesaria"):           
            st.error("⚠️ **AVISO IMPORTANTE:** De todo lo que leas abajo, debes llevar **ORIGINAL Y FOTOCOPIA**. Sin la fotocopia no te dejarán hacer las pruebas.")
            st.markdown("### 🔹 1. Documentos Comunes")
            st.write("""
            * **DNI / Pasaporte / NIE:** En vigor (Original + Copia).
            * **Titulación Académica:** Mínimo ESO o equivalente (Original + Copia).
            * **Nº Seguridad Social (NAF):** Documento oficial con tu propio número de afiliación (Original + Copia).
            * **Méritos:** Carné de conducir, títulos de inglés, etc. (Original + Copia).
            """)

            # 2. SEGÚN TU SITUACIÓN (Nacionales, Extranjeros, Menores)
            st.markdown("### 📋 2. Según tu situación específica")
            
            tab_nac, tab_ext, tab_men = st.tabs(["🇪🇸 Nacionales", "🌎 Extranjeros", "🔞 Menores"])
            
            with tab_nac:
                st.write("**Solo necesitas:** DNI en vigor y el resto de documentos comunes.")
            
            with tab_ext:
                st.write("**Documentación extra:**")
                st.write("- **Pasaporte** en vigor.")
                st.write("- **Tarjeta de Residencia** (Temporal o Larga duración) en vigor.")
                st.write("- Documento que autorice tu incorporación a FF.AA. extranjeras (si tu país lo exige).")
            
            with tab_men:
                st.warning("Si no has cumplido los 18 el día de la cita:")
                st.write("- **Apéndice 9 del BOE** (Autorización paterna) firmado.")
                st.write("- **DNI del padre/madre/tutor** (Original + Copia).")

            st.divider()

            # CONSEJOS EXTRAÍDOS DEL BOE
            with st.container():
                st.markdown("**📌 Notas del BOE (Base Quinta):**")
                st.info("""
                * **Tatuajes:** Se revisarán en esta fase. No deben ser visibles con el uniforme o ser contrarios a los valores constitucionales.
                * **Bolígrafo:** Lleva tu propio bolígrafo (azul o negro) para los impresos.
                * **Cita:** Si llegas tarde o sin el DNI original, pierdes el derecho a examen.
                """)

        with st.expander("📑 FASES DEL PROCESO DE SELECCIÓN"):
            st.markdown("### **Fase Primera: Evaluación**")
            st.write("**1. Concurso (30%):** Valoración de méritos generales y académicos.")
            st.write("**2. Oposición (70%):** Exámenes de conocimientos e inglés.")
            st.info("💡 **Fórmula:** (Mér x 3 + Opos x 7) / 10")
            st.markdown("---")
            st.markdown("### **Fase Segunda: Pruebas de Aptitud**")
            st.markdown("* **Prueba de personalidad.**\n* **Reconocimiento médico.**\n* **Pruebas físicas.**")

    # Sub-desplegable 2: Físicas
        # 1. Este es el desplegable. Todo lo que esté "dentro" debe llevar sangría (espacios).
        with st.expander("🏆 CONSULTAR MARCAS FÍSICAS MÍNIMAS", expanded=False):
            
            # Mantenemos los datos para que no de error, pero no los pintamos
            data_fisicas = {
                "Prueba": ["Flexiones", "Abdominales", "2.000m", "Agilidad"],
                "H": ["9", "40\"", "11' 54\"", "15,4\""],
                "M": ["5", "40\"", "12' 58\"", "17,1\""]
            }
            
            st.markdown("### Marcas Mínimas por Sexo")
            
            # 2. Las pestañas (OJO: deben estar alineadas con el markdown de arriba)
            tab_h, tab_m = st.tabs(["👨 Hombres", "👩 Mujeres"])
            
            with tab_h:
                c1, c2, c3, c4 = st.columns(4)
                c1.metric("Flexiones", "9")
                c2.metric("Abdominales", "40\"")
                c3.metric("2.000m", "11'54\"")
                c4.metric("Agilidad", "15,4\"")
                
            with tab_m:
                c1, c2, c3, c4 = st.columns(4)
                c1.metric("Flexiones", "5")
                c2.metric("Abdominales", "40\"")
                c3.metric("2.000m", "12'58\"")
                c4.metric("Agilidad", "17,1\"")

    # 3. Aquí termina el desplegable. Lo siguiente que escribas ya irá fuera.

    

    # Sub-desplegable 3: Baremo
        with st.expander("📊 BAREMO DE CONCURSO (MÉRITOS)", expanded=False):
            st.markdown("## 📈 Cálculo de Méritos (Máximo 40 puntos)")

            # --- 🎓 SECCIÓN ACADÉMICA (CON MÁS COLORES) ---
            with st.container(border=True):
                st.markdown("#### 🎓 1. Méritos Académicos")
                c_ac1, c_ac2, c_ac3 = st.columns(3)
                with c_ac1:
                    st.success("**Grado Medio (Específicas): 30 pts**")
                with c_ac2:
                    st.info("**Bachillerato / Grado Medio: 16 pts**")
                with c_ac3:
                    st.warning("**Título de la ESO: 6 pts**")
                st.caption("*(Solo se puntuará el nivel más alto aportado)*")

            st.divider()

            # --- 🚗 SECCIÓN GENERAL (CARNETS REPARTIDOS) ---
            st.markdown("#### 🚗 2. Méritos Generales")
            
            # Tarjeta de Carnets
            with st.container(border=True):
                st.markdown("**🪪 Permisos de Conducción** (repartidos para mejor lectura)")
                col_c1, col_c2, col_c3 = st.columns(3)
                with col_c1:
                    st.write("🚚 **Pesados+**")
                    st.write("- D1, D, D+E: **9 pts**")
                    st.write("- C+E: **8 pts**")
                with col_c2:
                    st.write("🚛 **Pesados**")
                    st.write("- C: **7 pts**")
                    st.write("- C1+E: **6 pts**")
                    st.write("- C1: **5 pts**")
                with col_c3:
                    st.write("🚗 **Ligeros**")
                    st.write("- B+E: **4 pts**")
                    st.write("- B: **3 pts**")

            # Tarjeta de Inglés (debajo de los carnets para que respire)
            with st.container(border=True):
                st.markdown("**🇬🇧 Idioma Inglés**")
                ci1, ci2, ci3 = st.columns(3)
                ci1.metric("Nivel C1/C2", "8 pts")
                ci2.metric("Nivel B2", "5 pts")
                ci3.metric("Nivel B1", "3 pts")

            st.divider()

            # --- 🎖️ SECCIÓN MILITAR ---
            with st.container(border=True):
                st.markdown("#### 🎖️ 3. Méritos Militares")
                col_mil1, col_mil2 = st.columns(2)
                with col_mil1:
                    st.markdown("**🪖 Empleos**")
                    st.write("- Cabo o superior: **2,00 pts**")
                    st.write("- Soldado/Marinero: **1,00 pt**")
                    st.write("- Reservista Voluntario: **0,25 pts**")
                with col_mil2:
                    st.markdown("**🏅 Recompensas**")
                    st.write("- Cruz Dist. Rojo: **2,00 pts**")
                    st.write("- Cruz Dist. Blanco: **1,50 pts**")
                    st.write("- Misión Int. (>2 meses): **0,50 pts**")
                
                st.error("⚠️ **LÍMITE SECCIÓN MILITAR:** Máximo 4 puntos.")

            st.info("💡 **Recordatorio:** La suma de Académicos + Generales tiene un tope de **36 puntos**.")

# BLOQUE DERECHO: MILITAR
with col_der:
    st.markdown("""
        <style>
        /* Importamos una fuente de Google profesional y condensada */
        @import url('https://fonts.googleapis.com/css2?family=Oswald:wght@700&display=swap');

        /* Seleccionamos el título del expander "¿ERES MILITAR?" */
        div[data-testid="stExpander"] summary p {
            font-size: 42px !important; 
            font-weight: 800 !important;
            color: #3B441E !important; /* VERDE OLIVA MÁS OSCURO (MÁS LEGIBLE) */
            font-family: 'Oswald', 'Arial Narrow', sans-serif !important;
            text-transform: uppercase !important;
            letter-spacing: 1px !important;
            margin: 0 !important;
            line-height: 1.1 !important;
        }
        
        /* Limpieza absoluta para que el resto de la web no cambie */
        .stMarkdown p:not(summary p) {
            color: inherit !important;
            font-family: inherit !important;
            font-size: inherit !important;
        }
        </style>
    """, unsafe_allow_html=True)

    # EL DESPLEGABLE PRINCIPAL
    with st.expander("¿ERES MILITAR?", expanded=False):
                with st.expander("📊 PAEF (Calculadora y Objetivos)", expanded=False):
                        # 1. CREAMOS LAS PESTAÑAS
                        pestana_calculo, pestana_objetivo = st.tabs(["🧮 Calculadora Total", "🎯 Marca Inversa (Objetivo)"])
                        
                        baremos = load_paef_baremos() # Tu función de carga de JSON
                        
                        # Selectores comunes
                        col_paef1, col_paef2 = st.columns(2)
                        with col_paef1: 
                            sexo_input = st.selectbox("Sexo", ["Hombre", "Mujer"], key="s_global")
                            sexo_sel = "H" if sexo_input == "Hombre" else "M"
                        with col_paef2: 
                            # Usamos un contenedor vacío para dar espacio
                            # Si el JSON no carga bien las edades, ponemos estas por defecto para que no se quede bloqueado
                            opciones_edad = baremos.get("age_groups", ["17-25", "26-30", "31-35", "36-40", "41-45", "46-50", "51-55", "56-59", "60+"])
                            if not opciones_edad:
                                 opciones_edad = ["17-25", "26-30", "31-35", "36-40", "41-45", "46-50", "51-55", "56-59", "60+"]
                            edad_sel = st.selectbox("Selecciona tu Rango de Edad", opciones_edad, key="e_global")
                        
                        st.divider()

                        # --- PESTAÑA 1: CALCULAR TOTAL (TODO DENTRO DEL BOTÓN PARA EVITAR ERRORES) ---
                        with pestana_calculo:
                            st.subheader("Calcula tu nota final")
                            f_reps = st.text_input("Flexiones (reps)", "0")
                            c_time = st.text_input("2000m (mm:ss)", "12:00")
                            p_time = st.text_input("Plancha (mm:ss)", "01:00")
                            a_time = st.text_input("Agilidad (seg.dec)", "14.0")
                            
                            if st.button("Calcular Nota Final"):
                                # A. CÁLCULOS (Aquí es donde p1, p2, p3 y p4 reciben su valor)
                                p1 = puntos_flexiones(baremos, sexo_sel, edad_sel, f_reps)
                                p2 = puntos_2000m(baremos, sexo_sel, edad_sel, c_time)
                                p3 = puntos_plancha(baremos, sexo_sel, edad_sel, p_time)
                                p4 = puntos_agilidad(baremos, sexo_sel, edad_sel, a_time)
                                
                                total = p1 + p2 + p3 + p4
                                
                                # B. COMPROBAR MÍNIMOS (Regla de los 20 puntos)
                                fallos = []
                                if p1 < 20: fallos.append("Flexiones")
                                if p2 < 20: fallos.append("2000m")
                                if p3 < 20: fallos.append("Plancha")
                                if p4 < 20: fallos.append("Agilidad")

                                # C. MOSTRAR RESULTADO PRINCIPAL
                                st.divider()
                                col_metrica, col_info = st.columns([1, 2])
                                with col_metrica:
                                    st.metric(label="PUNTUACIÓN TOTAL", value=f"{total} pts")
                                with col_info:
                                    if not fallos:
                                        st.success("✅ RESULTADO: APTO")
                                    else:
                                        st.error(f"❌ NO APTO: Mínimo de 20 pts no alcanzado en: {', '.join(fallos)}")

                                # D. SEMÁFORO DE CADA PRUEBA
                                st.write("### Desglose de rendimiento:")
                                pruebas_nombres = ["Flexiones", "2000m", "Plancha", "Agilidad"]
                                puntos_lista = [p1, p2, p3, p4]
                                
                                for prueba, pts in zip(pruebas_nombres, puntos_lista):
                                    if pts < 20:
                                        st.error(f"❌ {prueba}: {pts} pts (Por debajo del mínimo)")
                                    elif pts < 50:
                                        st.warning(f"⚠️ {prueba}: {pts} pts (Apto, marca floja)")
                                    else:
                                        st.success(f"✅ {prueba}: {pts} pts (¡Buena marca!)")

                                # --- E y F: DIAGNÓSTICO, PLAN Y CONSEJOS (TODO JUNTO) ---
                                st.divider()
                                
                                # Creamos el diccionario notas AQUÍ DENTRO
                                notas = {"Flexiones": p1, "2000m": p2, "Plancha": p3, "Agilidad": p4}
                                
                                # Filtramos las pruebas en las que va justo (menos de 50 pts)
                                justas = [p for p, nota in notas.items() if nota < 50]
                                
                                if justas:
                                    st.subheader("👟 Plan de Mejora y Consejos Pro")
                                    st.info(f"Hemos detectado que puedes mejorar en: {', '.join(justas)}")
                                    
                                    # Usamos un expander para cada prueba que necesite mejorar
                                    for prueba_justa in justas:
                                        with st.expander(f"Análisis para {prueba_justa}"):
                                            if prueba_justa == "2000m":
                                                st.markdown("**🏃 EL PLAN:** 2 días de series de 400m al 90% y 1 día de carrera continua.")
                                                st.write("**💡 CONSEJO PRO:** No corras siempre igual. Las series mejoran tu $VO_2$ máx para que el examen te parezca un paseo.")
                                            
                                            elif prueba_justa == "Flexiones":
                                                st.markdown("**💪 EL PLAN:** Entrenamiento piramidal (50%, 75%, 100% de tu máximo).")
                                                st.write("**💡 CONSEJO PRO:** El tríceps cae primero. Entrena el empuje bajo fatiga para ganar esas últimas 5 reps.")
                                            
                                            elif prueba_justa == "Plancha":
                                                st.markdown("**🧘 EL PLAN:** Series isométricas sumando 10s cada semana.")
                                                st.write("**💡 CONSEJO PRO:** Es batalla mental. Bloquea glúteos y respira corto para mantener la tensión del core.")
                                            
                                            elif prueba_justa == "Agilidad":
                                                st.markdown("**⚡ EL PLAN:** Técnica de giro sin velocidad y saltos explosivos.")
                                                st.write("**💡 CONSEJO PRO:** El tiempo se pierde en los giros. Pivota sobre el pie interno y revisa el agarre de tus suelas.")
                                else:
                                    st.balloons()
                                    st.success("🎯 ¡Nivel excelente en todas las pruebas! No necesitas plan de mejora urgente.")



                                # Creamos el diccionario para buscar la peor nota
                                notas = {"Flexiones": p1, "2000m": p2, "Plancha": p3, "Agilidad": p4}
                                peor_prueba = min(notas, key=notas.get)
                                nota_min = notas[peor_prueba]

                                if nota_min < 50:
                                    st.warning(f"Tu prioridad de entrenamiento es: **{peor_prueba}**")
                                    if peor_prueba == "2000m":
                                        st.write("• **Plan:** 2 días de series de 400m al 90% y 1 día de carrera continua de 40 min.")
                                    elif peor_prueba == "Flexiones":
                                        st.write("• **Plan:** Entrenamiento piramidal (50%, 75%, 100% de tu máximo) y fondos de tríceps.")
                                    elif peor_prueba == "Plancha":
                                        st.write("• **Plan:** Series de plancha isométrica aumentando 10 seg cada semana y trabajo de lumbares.")
                                    elif peor_prueba == "Agilidad":
                                        st.write("• **Plan:** Practica la técnica de giro sin velocidad y añade ejercicios de saltos explosivos.")
                                else:
                                    st.success("💪 ¡Nivel excelente! Mantén tus marcas actuales para asegurar el apto.")



                        # --- PESTAÑA 2: MARCA INVERSA (CORREGIDA Y FUNCIONAL) ---
                        with pestana_objetivo:
                            st.subheader("🎯 ¿Qué marca necesito para mis puntos?")
                            
                            # Selectores
                            puntos_buscados = st.slider("Puntos objetivo", 20, 100, 50, key="slider_inv")
                            prueba_tipo = st.selectbox("Selecciona la prueba", 
                                                    ["Flexiones", "2000m", "Plancha", "Agilidad"], 
                                                    key="sel_inv")
                            
                            # Mapeo para conectar con el JSON
                            mapa_claves = {
                                "Flexiones": "flexiones",
                                "2000m": "carrera_2000m",
                                "Plancha": "plancha",
                                "Agilidad": "agilidad"
                            }
                            
                            if st.button("Calcular marca necesaria", key="btn_inv"):
                                # Llamamos a la función "segura" que pusimos arriba
                                res = obtener_marca_inversa(baremos, mapa_claves[prueba_tipo], sexo_sel, edad_sel, puntos_buscados)
                                
                                if "Error" in res or "No hay" in res:
                                    st.error(f"⚠️ {res}")
                                else:
                                    st.success(f"Para obtener **{puntos_buscados} puntos** en {prueba_tipo}:")
                                    st.metric(label="Marca mínima necesaria", value=str(res))
                            
                            st.divider()
                            st.info("💡 Datos según baremos oficiales del Ejército de Tierra.")
                with st.expander("📍 GESTIÓN DE DESTINOS", expanded=False):
                    st.markdown("### Seleccione su Escala")
            
            # --- SECCIÓN TROPA ---
                    with st.expander("🎖️ ESCALA DE TROPA", expanded=False):
                        with st.expander("📋 Vacantes por LD (Libre Designación)"):
                            st.write("Listado de vacantes de libre designación para Tropa.")
                        with st.expander("🏆 Vacantes por Concurso de Méritos"):
                            st.write("Listado de vacantes por méritos para Tropa.")
                        with st.expander("🛡️ Vacantes Ordinarias"):
                            st.write("Listado de vacantes ordinarias para Tropa.")

            # --- SECCIÓN SUBOFICIALES ---
                    with st.expander("🎖️ ESCALA DE SUBOFICIALES", expanded=False):
                        with st.expander("📋 Vacantes por LD (Libre Designación)"):
                            st.write("Listado de vacantes de libre designación para Suboficiales.")
                        with st.expander("🏆 Vacantes por Concurso de Méritos"):
                            st.write("Listado de vacantes por méritos para Suboficiales.")
                        with st.expander("🛡️ Vacantes Ordinarias"):
                            st.write("Listado de vacantes ordinarias para Suboficiales.")

            # --- SECCIÓN OFICIALES ---
                    with st.expander("🎖️ ESCALA DE OFICIALES", expanded=False):
                        with st.expander("📋 Vacantes por LD (Libre Designación)"):
                            st.write("Listado de vacantes de libre designación para Oficiales.")
                        with st.expander("🏆 Vacantes por Concurso de Méritos"):
                            st.write("Listado de vacantes por méritos para Oficiales.")
                        with st.expander("🛡️ Vacantes Ordinarias"):
                            st.write("Listado de vacantes ordinarias para Oficiales.")
                
                
                with st.expander("🚀 NO TE QUEDES PARADO ¡PROMOCIONA!", expanded=False):
                    st.markdown("### Elige tu objetivo de carrera")
                    
                    # --- SUBSECCIÓN: COMO SER SUBOFICIAL ---
                    with st.expander("🎖️ CÓMO SER SUBOFICIAL", expanded=False):
                        st.write("### Requisitos y Vías de Acceso")
                        st.write("- **Promoción Interna:** Requisitos de tiempo de servicio y titulación.")
                        st.write("- **Examen de Oposición:** Temarios, pruebas físicas y baremo.")
                        st.info("💡 Recuerda que para el acceso por promoción interna se requiere un tiempo mínimo de servicio.")

                    # --- SUBSECCIÓN: COMO SER OFICIAL ---
                    with st.expander("🎓 CÓMO SER OFICIAL", expanded=False):
                        st.write("### Escala de Oficiales")
                        st.write("- **Acceso con Titulación:** Requisitos para titulados universitarios.")
                        st.write("- **Acceso sin Titulación:** Vía de ingreso directo o promoción interna.")
                        st.write("- **Cuerpo General y Especialistas:** Diferentes perfiles operativos.")
                        st.warning("⚠️ Consulta las convocatorias anuales para las plazas específicas de tu Cuerpo.")
