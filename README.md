# Hito2_SGE_CMG
Hito2_SGE_CMG

# Manipulación de Datos de Consumo de Alcohol

Este proyecto es una aplicación gráfica en Python que permite manipular y analizar datos relacionados con el consumo de alcohol. La interfaz incluye opciones para consultar, agregar, modificar, eliminar, exportar y visualizar los datos almacenados en una base de datos MySQL.

## Requisitos Previos

Asegúrate de tener instalados los siguientes programas y bibliotecas:

1. **Python 3.8+**
2. **Bibliotecas de Python**:
   - `tkinter` (incluido por defecto en Python)
   - `mysql-connector-python`
   - `matplotlib`
   - `csv` (incluido por defecto en Python)

3. **Base de datos MySQL**
   - Crear una base de datos llamada `Encuestas` con la tabla `Encuesta`. La estructura básica debería incluir columnas como:
     - `idEncuesta` (Primary Key)
     - `Edad`
     - `Sexo`
     - `BebidasSemana`
     - `CervezasSemana`
     - `BebidasFinSemana`
     - `BebidasDestiladasSemana`
     - `VinosSemana`
     - `PerdidasControl`
     - `ProblemasDigestivos`

## Instalación

1. **Clonar el repositorio**:
   ```bash
   git clone https://github.com/usuario/repo.git
   cd repo
