# Proyecto Integrador - Nuevas Tecnologías

Este repositorio contiene el pipeline de datos (Simulación, Exportación, Limpieza, Consultas y Visualización) para el proyecto Kaizen.

## 📁 Estructura del Proyecto

```text
Integrador_NT_martes_4/
│
├── data/                    # Carpetas de datos (generadas al ejecutar)
│   ├── crudo/
│   ├── limpio/
│   └── reportes/
│
├── notebook/                # Módulos de desarrollo
│   ├── simulaciones/        # Scripts de generación con Faker (F01)
│   ├── exportaciones/       # Scripts de exportación CSV/XLSX/JSON (X01)
│   ├── limpieza/            # Scripts de limpieza de datos (L01)
│   ├── consultas/           # Consultas con Pandas y groupby (Q01)
│   └── reportes/            # Reportes gráficos con Matplotlib (G01)
│
├── src/
│   └── main.py              # Controlador principal del pipeline
│
├── .gitignore
├── requirements.txt
└── README.md