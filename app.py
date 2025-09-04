import streamlit as st
import pandas as pd
import plotly.express as px
import random
from datetime import datetime

st.set_page_config(
    page_title="Liderlogo - Kit Digital",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

def check_password():
    """Retorna True si el usuario ha ingresado las credenciales correctas."""
    
    def password_entered():
        """Valida las credenciales ingresadas."""
        if (st.session_state["username"] == "liderlogo" and 
            st.session_state["password"] == "liderlogo20205"):
            st.session_state["password_correct"] = True
            del st.session_state["password"]
            del st.session_state["username"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.markdown("## 🔒 Login")
        st.text_input("Usuario", key="username")
        st.text_input("Contraseña", type="password", key="password")
        st.button("Ingresar", on_click=password_entered)
        return False
    
    elif not st.session_state["password_correct"]:
        st.markdown("## 🔒 Login")
        st.text_input("Usuario", key="username")
        st.text_input("Contraseña", type="password", key="password")
        st.button("Ingresar", on_click=password_entered)
        st.error("😕 Usuario o contraseña incorrectos")
        return False
    else:
        return True

@st.cache_data
def load_data():
    """Carga y procesa el archivo CSV."""
    df = pd.read_csv("LIDERLOGO _ Justificaciones Kit Digital - nico.csv")
    df = df[df['cuenta'].notna()]
    df = df.fillna("")
    return df

def format_date(date_str):
    """Formatea las fechas del CSV."""
    if pd.isna(date_str) or date_str == "":
        return "-"
    try:
        date_obj = pd.to_datetime(date_str, format="%d/%m/%Y", errors='coerce')
        if pd.isna(date_obj):
            return date_str
        return date_obj.strftime("%d/%m/%Y")
    except:
        return date_str

def get_status_color(status):
    """Retorna el color según el estado."""
    colors = {
        "Presentado": "🟢",
        "Pendiente": "🟡",
        "Pendiente FASE II": "🟠",
        "Aprobado": "✅",
        "Subsanación": "🔴"
    }
    return colors.get(status, "⚪")

def get_resolution_color(resolution):
    """Retorna el color según la resolución."""
    colors = {
        "Aprobado": "✅",
        "Pendiente": "🟡",
        "Subsanación": "🔴"
    }
    return colors.get(resolution, "⚪")

def show_domain_info(domain_data):
    """Muestra la información de un dominio específico."""
    
    st.markdown(f"## 🏢 {domain_data['cuenta']}")
    
    if domain_data['dominio']:
        st.markdown(f"### 🌐 Dominio: [{domain_data['dominio']}]({domain_data['dominio']})")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("#### 📅 Vencimientos")
        fase1 = format_date(domain_data['Vencimiento FASE I'])
        fase2 = format_date(domain_data['Vencimiento FASE II'])
        st.write(f"**FASE I:** {fase1}")
        st.write(f"**FASE II:** {fase2}")
    
    with col2:
        st.markdown("#### 📊 Estado")
        estado = domain_data['Estado'] if domain_data['Estado'] else "-"
        st.write(f"{get_status_color(estado)} **{estado}**")
        
        resolucion = domain_data['Resolución'] if domain_data['Resolución'] else "-"
        st.write(f"**Resolución:** {get_resolution_color(resolucion)} {resolucion}")
    
    with col3:
        st.markdown("#### ✅ Justificaciones")
        just1 = domain_data['justificacion FASE I'] if domain_data['justificacion FASE I'] else "-"
        just2 = domain_data['justificacion FASE II'] if domain_data['justificacion FASE II'] else "-"
        st.write(f"**FASE I:** {just1}")
        st.write(f"**FASE II:** {just2}")
    
    st.markdown("---")
    
    col4, col5 = st.columns(2)
    
    with col4:
        st.markdown("#### 🔧 Configuración")
        gsc = "✅ Sí" if domain_data['alta_gsc'] == "si" else "❌ No" if domain_data['alta_gsc'] == "no" else "-"
        sitemap = "✅ Sí" if domain_data['sitemap_enviado'] == "si" else "❌ No" if domain_data['sitemap_enviado'] == "no" else "-"
        st.write(f"**Alta GSC:** {gsc}")
        st.write(f"**Sitemap Enviado:** {sitemap}")
        
        if domain_data['sheets']:
            st.write(f"**Sheets:** ✅ {domain_data['sheets']}")
    
    with col5:
        st.markdown("#### 👤 Acceso Admin")
        if domain_data['usuario_admin']:
            st.info(f"**Usuario:** {domain_data['usuario_admin']}")
        if domain_data['contraseña_admin']:
            with st.expander("Ver contraseña"):
                st.code(domain_data['contraseña_admin'])
    
    if domain_data['directorio']:
        st.markdown("#### 📁 Directorios")
        directorios = domain_data['directorio'].split(' | ')
        for dir in directorios:
            if dir.strip():
                st.write(f"- [{dir.strip()}]({dir.strip()})")
    
    st.markdown("---")
    
    st.markdown("### 📊 Gráfico de Notas")
    
    valores = [random.choice(range(10, 101, 10)) for _ in range(random.randint(3, 7))]
    categorias = [f"Categoría {i+1}" for i in range(len(valores))]
    
    fig = px.bar(
        x=categorias,
        y=valores,
        title="Notas",
        labels={'x': 'Categorías', 'y': 'Puntuación'},
        color=valores,
        color_continuous_scale='viridis'
    )
    
    fig.update_layout(
        yaxis_range=[0, 100],
        yaxis_dtick=10,
        showlegend=False,
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)

def main():
    if not check_password():
        return
    
    df = load_data()
    
    with st.sidebar:
        st.markdown("# 🚀 Liderlogo Kit Digital")
        st.markdown("---")
        
        st.markdown("### 🔍 Seleccionar Cliente")
        
        cuentas_con_dominio = df[df['dominio'] != '']['cuenta'].tolist()
        cuentas_sin_dominio = df[df['dominio'] == '']['cuenta'].tolist()
        
        todas_las_cuentas = ["📊 Vista General"] + cuentas_con_dominio + cuentas_sin_dominio
        
        selected = st.selectbox(
            "Selecciona un cliente:",
            todas_las_cuentas,
            format_func=lambda x: f"🌐 {x}" if x in cuentas_con_dominio else f"⚪ {x}" if x != "📊 Vista General" else x
        )
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Clientes", len(df))
        with col2:
            st.metric("Con Dominio", len(cuentas_con_dominio))
        
        st.markdown("---")
        
        if st.button("🚪 Cerrar Sesión"):
            for key in st.session_state.keys():
                del st.session_state[key]
            st.rerun()
    
    if selected == "📊 Vista General":
        st.title("📊 Vista General - Kit Digital")
        st.markdown("---")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            presentados = len(df[df['Estado'] == 'Presentado'])
            st.metric("Presentados", presentados)
        
        with col2:
            pendientes = len(df[df['Estado'] == 'Pendiente'])
            st.metric("Pendientes", pendientes)
        
        with col3:
            aprobados = len(df[df['Resolución'] == 'Aprobado'])
            st.metric("Aprobados", aprobados)
        
        with col4:
            subsanacion = len(df[df['Resolución'] == 'Subsanación'])
            st.metric("Subsanación", subsanacion)
        
        st.markdown("---")
        
        st.markdown("### 📋 Lista de Clientes")
        
        display_df = df[['cuenta', 'dominio', 'Estado', 'Resolución', 'Vencimiento FASE I', 'Vencimiento FASE II']].copy()
        display_df['dominio'] = display_df['dominio'].apply(lambda x: x if x else '-')
        
        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "cuenta": st.column_config.TextColumn("Cliente", width="medium"),
                "dominio": st.column_config.LinkColumn("Dominio", width="medium"),
                "Estado": st.column_config.TextColumn("Estado", width="small"),
                "Resolución": st.column_config.TextColumn("Resolución", width="small"),
                "Vencimiento FASE I": st.column_config.TextColumn("Venc. FASE I", width="small"),
                "Vencimiento FASE II": st.column_config.TextColumn("Venc. FASE II", width="small")
            }
        )
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        
        with col1:
            estado_counts = df['Estado'].value_counts()
            fig_estado = px.pie(
                values=estado_counts.values,
                names=estado_counts.index,
                title="Distribución por Estado"
            )
            st.plotly_chart(fig_estado, use_container_width=True)
        
        with col2:
            resolucion_counts = df['Resolución'].value_counts()
            fig_resolucion = px.pie(
                values=resolucion_counts.values,
                names=resolucion_counts.index,
                title="Distribución por Resolución"
            )
            st.plotly_chart(fig_resolucion, use_container_width=True)
    
    else:
        domain_data = df[df['cuenta'] == selected].iloc[0]
        show_domain_info(domain_data)

if __name__ == "__main__":
    main()