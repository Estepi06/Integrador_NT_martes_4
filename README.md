# Proyecto Integrador - Nuevas Tecnologías

Este repositorio contiene el pipeline de datos (Simulación, Exportación, Limpieza, Consultas y Visualización) para el proyecto Kaizen.

## 📁 Estructura del Proyecto

```text
Integrador_NT_martes_4/
│
├── data/                    # Carpetas de datos (generadas al ejecutar)
│   ├── crudo/
│   ├── limpio/
│   └── graficas/
│
├── notebook/                # Módulos de desarrollo
│   ├── simulaciones/        # Scripts de generación con Faker (F01)
│   ├── exportaciones/       # Scripts de exportación CSV/XLSX/JSON (X01)
│   ├── limpieza/            # Scripts de limpieza de datos (L01)
│   ├── consultas/           # Consultas con Pandas y groupby (Q01)
│   └── graficas/            # Reportes gráficos con Matplotlib (G01)
│
├── src/
│   └── main.py              # Controlador principal del pipeline
│
├── .gitignore
├── requirements.txt
└── README.md
```

---

## Instalación y Configuración

### 1. Clonar el repositorio
```bash
git clone <URL_DE_TU_REPOSITORIO>
cd Integrador_NT_martes_4
```

### 2. Crear y activar el entorno virtual

* **Git Bash / Linux / macOS:**
  ```bash
  python -m venv .venv
  source .venv/Scripts/activate
  ```

* **Windows (CMD):**
  ```cmd
  python -m venv .venv
  .venv\Scripts\activate
  ```

* **Windows (PowerShell):**
  ```powershell
  python -m venv .venv
  .\.venv\Scripts\Activate.ps1
  ```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

---

## Ejecución del Pipeline

Para ejecutar la simulación, limpieza, consultas y generación de gráficas en un solo comando:

```bash
python src/main.py
```

---

## 👥 Trabajo Colaborativo (Integración de tablas)

Cada integrante desarrolla sus Historias de Usuario bajo las siguientes carpetas en `notebook/`:
* `empresas`
* `retos`
* `categorias`
* `registros`