# Liderlogo Kit Digital Dashboard

Aplicación Streamlit para gestión de justificaciones Kit Digital.

## Características

- Sistema de autenticación
- Vista general con métricas y gráficos
- Páginas individuales por cliente
- Información de dominios y estado de justificaciones
- Gráficos interactivos

## Instalación Local

1. Clonar el repositorio
2. Instalar dependencias:
```bash
pip install -r requirements.txt
```

3. Ejecutar la aplicación:
```bash
streamlit run app.py
```

## Despliegue en Streamlit Cloud

La aplicación está configurada para usar Streamlit Secrets para datos sensibles.

### Configuración de Secrets

En Streamlit Cloud, ve a Settings → Secrets y configura:

1. **Credenciales de login:**
```toml
[credentials]
username = "liderlogo"
password = "liderlogo20205"
```

2. **Datos CSV:**
```toml
csv_data = """
cuenta,Vencimiento FASE I,Vencimiento FASE II,Estado,Resolución,directorio,alta_gsc,sitemap_enviado,dominio,usuario_admin,contraseña_admin,justificacion FASE I,justificacion FASE II,sheets
[PEGAR AQUÍ EL CONTENIDO COMPLETO DEL CSV]
"""
```

## Seguridad

- Las credenciales y datos sensibles se manejan mediante Streamlit Secrets
- No se exponen contraseñas en el código fuente
- El repositorio puede mantenerse público sin riesgo de seguridad