st.markdown(f"""
    <style>
    /* 1. FONDO Y CAPA GENERAL */
    .stApp {{ background: none !important; }}
    .stApp::before {{
        content: ""; position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; z-index: -1;
        background: linear-gradient(rgba(0, 0, 0, 0.7), rgba(0, 0, 0, 0.7)), 
        url("data:image/jpeg;base64,{bin_str}");
        background-size: cover !important; background-position: center !important;
    }}

    /* 2. BLINDAJE DE INPUTS Y DESPLEGABLES (Para que se lean siempre) */
    /* Esto arregla los cuadros de texto, números y selectores */
    div[data-baseweb="select"], div[data-baseweb="input"], input, select {{
        background-color: white !important;
        border: 1px solid #3B441E !important;
        border-radius: 10px !important;
    }}

    /* Color del texto dentro de los desplegables y cuadros de texto */
    div[data-baseweb="select"] *, div[data-baseweb="input"] *, input, select, option {{
        color: black !important;
        -webkit-text-fill-color: black !important; /* Forzado para iPhone */
    }}

    /* 3. TARJETAS (EXPANDERS) */
    div[data-testid="stExpander"] {{
        background-color: white !important;
        border: 2px solid #556b2f !important;
        border-radius: 15px !important;
    }}

    /* Títulos de Expanders y texto general */
    div[data-testid="stExpander"] summary p, .stApp p, .stApp span, .stApp label, .stApp li {{
        color: #1a1a1a !important;
        font-weight: bold !important;
    }}

    /* 4. BOTONES (El de Calcular Nota) */
    .stButton button {{
        background-color: #3B441E !important;
        color: white !important;
        border-radius: 10px !important;
        font-weight: bold !important;
        min-height: 50px !important;
        border: none !important;
    }}
    /* Arreglo para que el texto del botón de calcular no sea invisible */
    .stButton button p {{
        color: white !important;
    }}

    /* 5. TABS (Hombres/Mujeres) */
    button[data-baseweb="tab"] p {{ color: #1a1a1a !important; }}
    button[data-baseweb="tab"][aria-selected="true"] {{ background-color: #f0f2f6 !important; }}

    /* 6. QUITAR CORTES DE PALABRAS */
    * {{ hyphens: none !important; word-break: keep-all !important; }}

    /* 7. BANDERA SUPERIOR */
    header::after {{
        content: ""; position: fixed; top: 0; left: 0; width: 100%; height: 10px;
        background: linear-gradient(to bottom, #AA151B 0%, #AA151B 33%, #F1BF00 33%, #F1BF00 66%, #AA151B 66%, #AA151B 100%);
        z-index: 999999;
    }}
    header {{ visibility: hidden !important; }}
    </style>
    """, unsafe_allow_html=True)
