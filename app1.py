# -*- coding: utf-8 -*-
"""
Created on Sun May 11 09:55:46 2025

@author: jahop
"""

import streamlit as st
import pandas as pd
import geopandas as gpd
from shapely.geometry import Polygon
import folium
from streamlit_folium import st_folium
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import numpy as np

# Configuración avanzada de la página
st.set_page_config(
    layout="wide", 
    page_title="SENER - Plataforma Inteligente de Exploración",
    page_icon="⚡"
)

# CSS personalizado
st.markdown("""
    <style>
    .main {background-color: #f5f5f5;}
    .st-bw {background-color: #0c4b33;}
    .st-at {color: white;}
    .header-title {color: #0c4b33; font-size: 2.5rem; font-weight: 700;}
    .header-subtitle {color: #2c7d5f; font-size: 1.2rem;}
    .metric-card {border-radius: 10px; padding: 15px; background-color: white; box-shadow: 0 4px 6px rgba(0,0,0,0.1);}
    .footer {text-align: center; padding: 15px; background-color: #0c4b33; color: white;}
    .map-container {border-radius: 15px; overflow: hidden; box-shadow: 0 6px 16px rgba(0,0,0,0.1);}
    </style>
    """, unsafe_allow_html=True)

# Título mejorado
col1, col2 = st.columns([1, 6])
with col1:
    st.image("logo_sener.jpg", width=150) 
with col2:
    st.markdown('<h1 class="header-title">Plataforma Inteligente de Exploración y Evaluación</h1>', unsafe_allow_html=True)
    st.markdown('<p class="header-subtitle">Sistema Integral de Monitoreo Estratégico - Secretaría de Energía</p>', unsafe_allow_html=True)

# Barra lateral con filtros
with st.sidebar:
    # Agregar tu nombre y la fecha
    st.markdown("---")
    st.markdown(f"**Desarrollado por:**  \n*Javier Horacio Pérez Ricárdez*")
    st.markdown(f"**Fecha:**  \n{datetime.today().strftime('%d/%m/%Y')}")
    st.markdown("---")
    
    
    # Botón para descargar manual PDF
    with open("manual.pdf", "rb") as pdf_file:
        PDFbyte = pdf_file.read()
    
    st.download_button(
        label="📄 Descargar Manual",
        data=PDFbyte,
        file_name="manual.pdf",
        mime="application/pdf",
        help="Descargue el manual de usuario en formato PDF"
    )
    st.markdown("---")
    
    
    
    #st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/5/5c/Secretar%C3%ADa_de_Energ%C3%ADa_%28M%C3%A9xico%29.svg/1200px-Secretar%C3%ADa_de_Energ%C3%ADa_%28M%C3%A9xico%29.svg.png", width=60)
    st.markdown("**Filtros Avanzados**")
    
    tipo_contrato = st.multiselect("Tipo de Contrato", ["Asignación", "Licitación"], default=["Asignación", "Licitación"])
    estado_area = st.multiselect("Estado del Área", ["Activo", "Suspendido", "En Revisión", "Terminado"], default=["Activo"])
    tipo_recurso = st.multiselect("Tipo de Recurso", ["Convencional", "No Convencional", "Aguas Profundas", "Shale"], default=["Convencional"])
    
    st.markdown("---")
    st.markdown("**Rango de Fechas**")
    fecha_inicio = st.date_input("Fecha de inicio", value=datetime(2020, 1, 1))
    fecha_fin = st.date_input("Fecha de fin", value=datetime.today())

# Función para generar datos dinámicos basados en filtros
def generar_datos_filtrados(tipo_contrato, estado_area, tipo_recurso):
    # Crear polígonos simulados
    polygons = [
        Polygon([[-101, 24], [-100, 24], [-100, 25], [-101, 25]]),
        Polygon([[-98, 21], [-97, 21], [-97, 22], [-98, 22]]),
        Polygon([[-104, 20], [-103, 20], [-103, 21], [-104, 21]]),
    ]

    gdf = gpd.GeoDataFrame({
        "Área": ["Bloque Norte", "Bloque Este", "Bloque Pacífico"],
        "Tipo de Contrato": ["Asignación", "Licitación", "Asignación"],
        "Estado": ["Activo", "Activo", "Suspendido"],
        "Tipo de Recurso": ["Convencional", "No Convencional", "Convencional"],
        "Inversión (MUSD)": [450, 320, 280],
        "Reservas (MMBOE)": [1250, 850, 620],
        "geometry": polygons
    }, crs="EPSG:4326")

    # Aplicar filtros
    filtered_gdf = gdf[
        gdf['Tipo de Contrato'].isin(tipo_contrato) &
        gdf['Estado'].isin(estado_area) &
        gdf['Tipo de Recurso'].isin(tipo_recurso)
    ]
    
    # Calcular KPIs dinámicos basados en filtros
    num_areas = len(filtered_gdf)
    inversion_total = filtered_gdf["Inversión (MUSD)"].sum()
    reservas_total = filtered_gdf["Reservas (MMBOE)"].sum()
    
    # Calcular porcentaje de avance basado en filtros (simulado)
    porcentaje_avance = min(100, 70 + (num_areas * 10) + (inversion_total / 100))
    
    return {
        "filtered_gdf": filtered_gdf,
        "num_areas": num_areas,
        "inversion_total": inversion_total,
        "reservas_total": reservas_total,
        "porcentaje_avance": porcentaje_avance
    }

# Generar datos filtrados
datos = generar_datos_filtrados(tipo_contrato, estado_area, tipo_recurso)

# Dashboard Ejecutivo con KPIs dinámicos
st.markdown("## 📊 Dashboard Ejecutivo")
kpi1, kpi2, kpi3, kpi4 = st.columns(4)
with kpi1:
    st.markdown(f'<div class="metric-card"><h3>Áreas Activas</h3><p style="font-size:24px; color:#0c4b33;">{datos["num_areas"]}</p><p>+{max(0, datos["num_areas"]-2)} vs PY</p></div>', unsafe_allow_html=True)
with kpi2:
    st.markdown(f'<div class="metric-card"><h3>Inversión Total</h3><p style="font-size:24px; color:#0c4b33;">${datos["inversion_total"]} MUSD</p><p>+{int(datos["inversion_total"]/50)}% vs PY</p></div>', unsafe_allow_html=True)
with kpi3:
    st.markdown(f'<div class="metric-card"><h3>Reservas Totales</h3><p style="font-size:24px; color:#0c4b33;">{datos["reservas_total"]} MMBOE</p><p>+{int(datos["reservas_total"]/100)}% vs PY</p></div>', unsafe_allow_html=True)
with kpi4:
    st.markdown(f'<div class="metric-card"><h3>Avance General</h3><p style="font-size:24px; color:#0c4b33;">{int(datos["porcentaje_avance"])}%</p><p>+{int(datos["porcentaje_avance"]-65)}pp vs PY</p></div>', unsafe_allow_html=True)

# Mapa interactivo
st.markdown("## 🌍 Mapa Estratégico de Áreas")
col_map1, col_map2 = st.columns([3, 1])
with col_map1:
    m = folium.Map(location=[23.5, -102], zoom_start=5, tiles="cartodbpositron")
    
    for _, row in datos["filtered_gdf"].iterrows():
        color = "#2c7d5f" if row["Estado"] == "Activo" else "#d9534f"
        folium.GeoJson(
            row["geometry"],
            style_function=lambda x, color=color: {
                "fillColor": color,
                "color": color,
                "weight": 2,
                "fillOpacity": 0.5
            },
            tooltip=f"""
            <b>Área:</b> {row['Área']}<br>
            <b>Tipo:</b> {row['Tipo de Contrato']}<br>
            <b>Recurso:</b> {row['Tipo de Recurso']}<br>
            <b>Inversión:</b> ${row['Inversión (MUSD)']} MUSD<br>
            <b>Reservas:</b> {row['Reservas (MMBOE)']} MMBOE
            """
        ).add_to(m)
    
    with st.container():
        st.markdown('<div class="map-container">', unsafe_allow_html=True)
        st_folium(m, width=900, height=600)
        st.markdown('</div>', unsafe_allow_html=True)

with col_map2:
    st.markdown("**Resumen por Tipo**")
    summary = datos["filtered_gdf"].groupby("Tipo de Recurso").agg({
        "Inversión (MUSD)": "sum",
        "Reservas (MMBOE)": "sum"
    }).reset_index()
    st.dataframe(summary.style.highlight_max(axis=0), use_container_width=True)

# Indicadores Estratégicos dinámicos
st.markdown("## 🎯 Indicadores Estratégicos")
col_met1, col_met2 = st.columns([1, 2])
with col_met1:
    # Calcular indicadores basados en filtros
    tasa_restitución = min(100, 90 + (datos["num_areas"] * 2) + (datos["reservas_total"] / 100))
    producción_total = 1500 + (datos["num_areas"] * 50) + (datos["inversion_total"] / 10)
    avance_evaluación = datos["porcentaje_avance"] * 0.9
    contenido_nacional = 65 + (datos["num_areas"] * 2)
    
    data = {
        "Indicador": [
            "Tasa de Restitución de Reservas (%)",
            "Producción Total (Miles de barriles/día)",
            "Avance de Evaluación de Planes (%)",
            "Cumplimiento de Contenido Nacional (%)"
        ],
        "Valor": [tasa_restitución, producción_total, avance_evaluación, contenido_nacional],
        "Meta": [90, 1800, 85, 70],
        "Variación": [
            f"+{tasa_restitución-90:.1f}pp",
            f"{producción_total-1800:+.0f}",
            f"{avance_evaluación-85:+.1f}pp",
            f"+{contenido_nacional-70:.1f}pp"
        ]
    }
    df_indicadores = pd.DataFrame(data)
    st.dataframe(
        df_indicadores.style
        .apply(lambda x: ["background: #e6f7ed" if x.Valor >= x.Meta else "background: #ffebee" for i in x], axis=1)
        .format({"Valor": "{:.1f}", "Meta": "{:.0f}"}),
        use_container_width=True
    )

with col_met2:
    # Gráfico de radar dinámico
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=df_indicadores["Valor"].values,
        theta=df_indicadores["Indicador"].values,
        fill='toself',
        name='Actual',
        line_color='#0c4b33'
    ))
    
    fig.add_trace(go.Scatterpolar(
        r=df_indicadores["Meta"].values,
        theta=df_indicadores["Indicador"].values,
        fill='toself',
        name='Meta',
        line_color='#d9534f'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, max(df_indicadores["Valor"].max(), df_indicadores["Meta"].max())*1.1]
            )),
        showlegend=True,
        title="Comparativo de Indicadores vs Metas"
    )
    
    st.plotly_chart(fig, use_container_width=True)

# Seguimiento de Planes dinámico - Versión corregida
st.markdown("## 🏗️ Seguimiento Estratégico de Planes")
col_plan1, col_plan2 = st.columns([2, 1])
with col_plan1:
    # Generar datos de planes basados en filtros asegurando misma longitud
    operadores = ["Pemex", "BP", "Shell", "Total", "Chevron", "Eni"]
    areas_filtradas = datos["filtered_gdf"]["Área"].tolist()
    
    # Asegurarnos de que todos los arrays tengan la misma longitud (6 elementos)
    num_elementos = 6
    if len(areas_filtradas) < num_elementos:
        areas_filtradas = areas_filtradas + ["N/A"] * (num_elementos - len(areas_filtradas))
    
    planes_data = {
        "Operador": operadores[:num_elementos],
        "Área": areas_filtradas[:num_elementos],
        "Avance (%)": [min(100, 70 + (i*5) + (datos["inversion_total"]/100)) for i in range(num_elementos)],
        "Estado del Plan": ["En Evaluación", "Aprobado", "En Revisión", "Aprobado", "En Ejecución", "Aprobado"][:num_elementos],
        "Inversión (MUSD)": [max(100, 200 + (i*50) + (datos["reservas_total"]/10)) for i in range(num_elementos)]
    }
    
    df_planes = pd.DataFrame(planes_data)
    
    def progress_bar(row):
        if row['Área'] == "N/A":
            return """<div style="height:20px; background:#eee; border-radius:5px; text-align:center; line-height:20px; font-size:12px;">
                    Sin datos</div>"""
        color = {
            "Aprobado": "#2c7d5f",
            "En Evaluación": "#f0ad4e",
            "En Revisión": "#5bc0de",
            "En Ejecución": "#5cb85c"
        }.get(row["Estado del Plan"], "#999999")
        return f"""
        <div style="position:relative; height:20px; background:#eee; border-radius:5px;">
            <div style="position:absolute; height:100%; width:{row['Avance (%)']}%; background:{color}; border-radius:5px;"></div>
            <div style="position:absolute; width:100%; text-align:center; line-height:20px; font-size:12px;">
                {row['Avance (%)']}% - {row['Estado del Plan']}
            </div>
        </div>
        """
    
    df_planes["Progreso"] = df_planes.apply(progress_bar, axis=1)
    st.write(df_planes[["Operador", "Área", "Inversión (MUSD)", "Progreso"]].to_html(escape=False), unsafe_allow_html=True)

with col_plan2:
    # Filtrar filas con datos válidos para el gráfico
    df_grafico = df_planes[df_planes["Área"] != "N/A"]
    if not df_grafico.empty:
        st.markdown("**Distribución de Inversión**")
        fig = px.pie(
            df_grafico, 
            values="Inversión (MUSD)", 
            names="Operador",
            title="Inversión por Operador",
            hole=0.4,
            color_discrete_sequence=px.colors.sequential.Emrld
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("No hay datos de inversión para mostrar con los filtros actuales")

# Análisis Predictivo dinámico
st.markdown("## 🔮 Análisis Predictivo")
col_pred1, col_pred2 = st.columns(2)
with col_pred1:
    st.markdown("**Pronóstico de Descubrimientos**")
    years = [2024, 2025, 2026, 2027]
    
    # Base de pronóstico basada en filtros
    base = datos["num_areas"] * 2 + datos["inversion_total"] / 200
    
    low = [int(base * 0.8 + i) for i in range(len(years))]
    mid = [int(base + i*1.5) for i in range(len(years))]
    high = [int(base * 1.2 + i*2) for i in range(len(years))]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=years, y=high, name="Optimista", line=dict(color="#5ab190", width=2, dash="dot")))
    fig.add_trace(go.Scatter(x=years, y=mid, name="Base", fill="tonexty", line=dict(color="#2c7d5f", width=3)))
    fig.add_trace(go.Scatter(x=years, y=low, name="Conservador", fill="tonexty", line=dict(color="#0c4b33", width=2, dash="dash")))
    
    fig.update_layout(
        title="Pronóstico de Descubrimientos por Año",
        xaxis_title="Año",
        yaxis_title="Número de Descubrimientos",
        hovermode="x"
    )
    st.plotly_chart(fig, use_container_width=True)

with col_pred2:
    st.markdown("**Riesgo Geológico**")
    cuencas = ["Burgos", "Sabinas", "Tampico", "Veracruz", "Sureste"]
    
    # Riesgo basado en filtros
    base_riesgo = 0.3 + (0.5 / (datos["num_areas"] + 1))
    riesgo = [min(0.9, base_riesgo + (i*0.1)) for i in range(len(cuencas))]
    
    fig = go.Figure(go.Bar(
        x=cuencas,
        y=riesgo,
        marker_color=np.where(
            np.array(riesgo) > 0.6, "#d9534f", 
            np.where(np.array(riesgo) > 0.3, "#f0ad4e", "#5cb85c")
        )
    ))
    
    fig.update_layout(
        title="Índice de Riesgo Geológico",
        yaxis_title="Probabilidad de Fracaso",
        yaxis_tickformat=".0%",
        xaxis_title="Cuenca"
    )
    st.plotly_chart(fig, use_container_width=True)

# Footer
st.markdown(f"""
<div class="footer">
<p style="margin:0;">Plataforma desarrollada por la <strong>Dirección General de Planes de Exploración y Programas de Evaluación</strong></p>
<p style="margin:0; font-size:0.9em;">Secretaría de Energía - Gobierno de México | Versión 2.1 | Última actualización: {datetime.today().strftime("%d/%m/%Y")}</p>
</div>
""", unsafe_allow_html=True)