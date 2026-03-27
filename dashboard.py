import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

st.set_page_config(layout="wide")

st.markdown("""
    <style>
    /* Fondo general */
    .stApp {
        background-color: #0e1117;
        color: #ffffff;
    }

    /* Títulos */
    h1, h2, h3 {
        color: #00c8ff;
    }

    /* KPIs */
    .stMetric {
        background-color: #1c1f26;
        padding: 15px;
        border-radius: 12px;
        border-left: 5px solid #00c8ff;
    }

    /* Tablas */
    .stDataFrame {
        background-color: #1c1f26;
        color: white;
    }

    /* Botones */
    .stDownloadButton button {
        background-color: #00c8ff;
        color: black;
        border-radius: 8px;
    }
    </style>
""", unsafe_allow_html=True)

st.title("📊 Dashboard_HUAWEI - Exclusiones Marzo_2026")

# Cargar Excel
df = pd.read_excel("DATA_MARZO_2026_IA.xlsx")

# =========================
# 🎛️ FILTROS
# =========================
col1, col2 = st.columns(2)

with col1:
    filtro_clasificacion = st.selectbox(
        "Filtrar por Clasificación",
        ["Todos"] + list(df["Clasificación"].dropna().unique())
    )

with col2:
    filtro_categoria = st.selectbox(
        "Filtrar por Categoría MINTIC",
        ["Todos"] + list(df["Categoría MINTIC"].dropna().unique())
    )

# Aplicar filtros
if filtro_clasificacion != "Todos":
    df = df[df["Clasificación"] == filtro_clasificacion]

if filtro_categoria != "Todos":
    df = df[df["Categoría MINTIC"] == filtro_categoria]

# Limpiar datos
df["EXCLUIDO"] = df["EXCLUIDO"].astype(str).str.upper()

total = len(df)
excluidos = df[df["EXCLUIDO"] == "SI"].shape[0]

porcentaje = (excluidos / total * 100) if total > 0 else 0

# =========================
# 📊 KPIs
# =========================
st.subheader("📊 Indicadores Clave")

col1, col2, col3 = st.columns(3)

color = "#00c8ff"
if porcentaje > 70:
    color = "#ff4b4b"
elif porcentaje > 40:
    color = "#ffc107"

col1.markdown(f"""
<div style="background-color:#1c1f26;padding:20px;border-radius:12px;text-align:center">
    <h3 style="color:white;">Total Registros</h3>
    <h1 style="color:{color};">{total}</h1>
</div>
""", unsafe_allow_html=True)

col2.markdown(f"""
<div style="background-color:#1c1f26;padding:20px;border-radius:12px;text-align:center">
    <h3 style="color:white;">Excluidos</h3>
    <h1 style="color:#ff4b4b;">{excluidos}</h1>
</div>
""", unsafe_allow_html=True)

col3.markdown(f"""
<div style="background-color:#1c1f26;padding:20px;border-radius:12px;text-align:center">
    <h3 style="color:white;">% Exclusión</h3>
    <h1 style="color:{color};">{porcentaje:.2f}%</h1>
</div>
""", unsafe_allow_html=True)

st.subheader("🧠 Análisis Inteligente")

top_categoria = df[df["EXCLUIDO"] == "SI"]["Nombre Categoría"].value_counts().idxmax()
top_region = df[df["EXCLUIDO"] == "SI"]["Regional"].value_counts().idxmax()

if porcentaje > 70:
    estado = "CRÍTICO"
elif porcentaje > 40:
    estado = "EN RIESGO"
else:
    estado = "CONTROLADO"

st.markdown(f"""
<div style="background-color:#1c1f26;padding:20px;border-radius:12px">

- 📊 Nivel actual: <b>{estado}</b>  
- 🚨 Principal causa: <b>{top_categoria}</b>  
- 🌍 Región más afectada: <b>{top_region}</b>  
- 📌 Recomendación: Priorizar acciones sobre estas variables  

</div>
""", unsafe_allow_html=True)

# =========================
# 🥧 GRÁFICO DE TORTA
# =========================
st.subheader("Proporción de Exclusiones")

fig1, ax1 = plt.subplots()
df["EXCLUIDO"].value_counts().plot.pie(autopct='%1.1f%%', ax=ax1)

st.pyplot(fig1)

# =========================
# 🚨 TOP CATEGORÍAS
# =========================
st.subheader("Top 10 Categorías con más Exclusiones")

top = df[df["EXCLUIDO"] == "SI"]["Nombre Categoría"].value_counts().head(10)

st.bar_chart(top)

# =========================
# 🚨 ALERTA GERENCIAL
# =========================
if porcentaje > 70:
    st.error("🔴 CRÍTICO: Nivel muy alto de exclusiones")
elif porcentaje > 40:
    st.warning("🟡 ALERTA: Nivel medio de exclusiones")
else:
    st.success("🟢 Nivel controlado")

# =========================
# 📊 TABLA
# =========================
st.subheader("Detalle de datos")
st.dataframe(df)

# =========================
# 📤 EXPORTAR A EXCEL
# =========================
st.subheader("Descargar reporte")

# Convertir a Excel en memoria
from io import BytesIO

output = BytesIO()
with pd.ExcelWriter(output, engine='openpyxl') as writer:
    df.to_excel(writer, index=False, sheet_name='Reporte')

excel_data = output.getvalue()

st.download_button(
    label="📥 Descargar reporte en Excel",
    data=excel_data,
    file_name="reporte_exclusiones_marzo.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)
# =========================
# 📊 EXCLUSIONES POR CLASIFICACIÓN
# =========================
st.subheader("Exclusiones por Clasificación")

clasif = df[df["EXCLUIDO"] == "SI"]["Clasificación"].value_counts()

st.bar_chart(clasif)

# =========================
# 📊 COMPARATIVO
# =========================
st.subheader("Comparativo Exclusiones por Clasificación")

comparativo = df.groupby(["Clasificación", "EXCLUIDO"]).size().unstack().fillna(0)

st.bar_chart(comparativo)

# =========================
# 🚨 TOP CATEGORÍAS
# =========================
st.subheader("Top Categorías Críticas")

top_cat = df[df["EXCLUIDO"] == "SI"]["Nombre Categoría"].value_counts().head(10)

st.bar_chart(top_cat)

st.subheader("Exclusiones por Región")

region = df[df["EXCLUIDO"] == "SI"]["Regional"].value_counts()

st.bar_chart(region)

st.subheader("Tiempo promedio de falla")

df["TIEMPO_FALLA"] = pd.to_numeric(df["TIEMPO_FALLA"], errors="coerce")

promedio = df["TIEMPO_FALLA"].mean()

st.metric("⏱️ Tiempo promedio (min)", round(promedio, 2))

st.subheader("Gestión de casos")

gestion = df["GESTION"].value_counts()

st.bar_chart(gestion)

st.subheader("Exclusiones por Municipio")

municipio = df[df["EXCLUIDO"] == "SI"]["MUNICIPIO"].value_counts().head(10)

st.bar_chart(municipio)

st.subheader("Conclusiones automáticas")

top_categoria = df[df["EXCLUIDO"] == "SI"]["Nombre Categoría"].value_counts().idxmax()
top_region = df[df["EXCLUIDO"] == "SI"]["Regional"].value_counts().idxmax()

st.write(f"""
- La categoría más crítica es: **{top_categoria}**
- La región más afectada es: **{top_region}**
- Se recomienda priorizar estas áreas para reducir exclusiones.
""")
fig, ax = plt.subplots()

# Crear conteo
conteo = df["EXCLUIDO"].value_counts()

# Graficar
fig, ax = plt.subplots()
conteo.plot(kind="bar", ax=ax, color="#00c8ff")

st.pyplot(fig)

ax.set_title("Exclusiones", color="white")
ax.set_xlabel("")
ax.set_ylabel("Cantidad", color="white")

ax.set_facecolor("#0e1117")
fig.patch.set_facecolor("#0e1117")

ax.tick_params(colors='white')

st.pyplot(fig)

st.subheader("Estado General")

if porcentaje > 70:
    st.markdown("## 🔴 CRÍTICO")
elif porcentaje > 40:
    st.markdown("## 🟡 EN RIESGO")
else:
    st.markdown("## 🟢 CONTROLADO")

# =========================
# 🤖 IA - PREDICCIÓN
# =========================
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder

st.subheader("🤖 Predicción de Exclusiones")

# Copia del dataframe
df_ml = df.copy()

# Eliminar columnas que no sirven
df_ml = df_ml.drop(columns=["Código"], errors="ignore")

# Convertir texto a números
le = LabelEncoder()

for col in ["Clasificación", "Categoría MINTIC", "Nombre Categoría"]:
    df_ml[col] = df_ml[col].astype(str)
    df_ml[col] = le.fit_transform(df_ml[col])

# Variable objetivo
df_ml["EXCLUIDO"] = df_ml["EXCLUIDO"].map({"SI":1, "NO":0})

# 🔥 VARIABLES IMPORTANTES (AQUÍ estaba tu error)
X = df_ml[[
    "Clasificación",
    "Categoría MINTIC",
    "Nombre Categoría"
]]

y = df_ml["EXCLUIDO"]

# Dividir datos
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Modelo
modelo = RandomForestClassifier()
modelo.fit(X_train, y_train)

# Precisión
accuracy = modelo.score(X_test, y_test)

st.write(f"Precisión del modelo: {accuracy:.2f}")

# =========================
# 🔥 PREDICCIONES
# =========================
st.subheader("🚨 Casos con Alto Riesgo de Exclusión")

# Predecir probabilidades
probabilidades = modelo.predict_proba(X)

# Probabilidad de ser excluido (columna 1)
df["Probabilidad_Exclusion"] = probabilidades[:, 1]

# Filtrar casos críticos
riesgo_alto = df[df["Probabilidad_Exclusion"] > 0.7]

st.write(f"Casos críticos detectados: {len(riesgo_alto)}")

st.dataframe(riesgo_alto[[
    "Clasificación",
    "Categoría MINTIC",
    "Nombre Categoría",
    "Probabilidad_Exclusion"
]])
# Clasificar riesgo
def clasificar_riesgo(prob):
    if prob > 0.7:
        return "🔴 Alto"
    elif prob > 0.4:
        return "🟡 Medio"
    else:
        return "🟢 Bajo"

df["Nivel_Riesgo"] = df["Probabilidad_Exclusion"].apply(clasificar_riesgo)

st.subheader("📊 Clasificación de Riesgo")

st.dataframe(df[[
    "Clasificación",
    "Categoría MINTIC",
    "Nombre Categoría",
    "Probabilidad_Exclusion",
    "Nivel_Riesgo"
]])
st.subheader("🚦 Distribución de Riesgo")

riesgo_counts = df["Nivel_Riesgo"].value_counts()

st.bar_chart(riesgo_counts)

st.subheader("🧠 Conclusión de Riesgo")

alto = (df["Nivel_Riesgo"] == "🔴 Alto").sum()

if alto > 0:
    st.error(f"🚨 Se detectaron {alto} casos de alto riesgo que requieren atención inmediata")
else:
    st.success("✅ No hay casos críticos actualmente")