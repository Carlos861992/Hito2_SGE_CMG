import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import mysql.connector
from mysql.connector import Error
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import csv


class Hito2:
    def __init__(self, root):
        self.root = root
        self.root.title("Manipulación de datos de alcohol")
        self.conectarALaBaseDeDatos()
        self.crearInterfaz()

    def conectarALaBaseDeDatos(self):
        try:
            self.connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="campusfp",
                database="Encuestas"
            )
            if self.connection.is_connected():
                messagebox.showinfo("Conexión exitosa", "Conectado a la base de datos Encuestas")
        except Error as e:
            messagebox.showerror("Error de conexión", f"No se pudo conectar a la base de datos. Error: {e}")

    def crearInterfaz(self):
        # Marco para la consulta
        self.query_frame = tk.Frame(self.root)
        self.query_frame.pack(padx=10, pady=10)

        tk.Label(self.query_frame, text="Ordenar por: ").grid(row=10, column=0, sticky="w")
        self.ordenar_por_combobox = ttk.Combobox(self.query_frame, values=["Edad", "Sexo", "BebidasSemana", "PerdidasControl", "ProblemasDigestivos"])
        self.ordenar_por_combobox.grid(row=10, column=1, padx=5, pady=5)

        tk.Label(self.query_frame, text="Condición: ").grid(row=11, column=0, sticky="w")
        self.condicion_combobox = ttk.Combobox(self.query_frame, values=["Alta frecuencia de consumo", "Más de 3 pérdidas de control", "Dolores de cabeza", "Presión alta"])
        self.condicion_combobox.grid(row=11, column=1, padx=5, pady=5)

        tk.Label(self.query_frame, text="Edad: ").grid(row=0, column=0, sticky="w")
        tk.Label(self.query_frame, text="Sexo: ").grid(row=0, column=2, sticky="w")
        tk.Label(self.query_frame, text="Consumo Semanal: ").grid(row=1, column=0, sticky="w")
        tk.Label(self.query_frame, text="Problemas de Salud: ").grid(row=1, column=2, sticky="w")

        self.edad_entry = tk.Entry(self.query_frame)
        self.edad_entry.grid(row=0, column=1, padx=5, pady=5)
        self.sexo_entry = tk.Entry(self.query_frame)
        self.sexo_entry.grid(row=0, column=3, padx=5, pady=5)
        self.consumo_semanal_entry = tk.Entry(self.query_frame)
        self.consumo_semanal_entry.grid(row=1, column=1, padx=5, pady=5)
        self.problemas_salud_entry = tk.Entry(self.query_frame)
        self.problemas_salud_entry.grid(row=1, column=3, padx=5, pady=5)

        tk.Button(self.query_frame, text="Consultar", command=self.consultar).grid(row=2, columnspan=4, pady=10)
        tk.Button(self.query_frame, text="Agregar Nueva Encuesta", command=self.abrirVentanaNuevaEncuesta).grid(row=3, columnspan=4, pady=10)
        tk.Button(self.query_frame, text="Eliminar Encuesta", command=self.abrirVentanaEliminarEncuesta).grid(row=4, columnspan=4, pady=10)
        tk.Button(self.query_frame, text="Aplicar Filtros", command=self.consultarConFiltros).grid(row=12, columnspan=2, pady=10)
        tk.Button(self.root, text="Exportar a CSV", command=self.exportarACSV).pack(pady=5)
        tk.Button(self.query_frame, text="Visualizar Gráfico", command=self.visualizarGrafico).grid(row=13, columnspan=2, pady=10)
        tk.Button(self.query_frame, text="Modificar Encuesta", command=self.abrirVentanaModificarEncuesta).grid(row=5, columnspan=4, pady=10)

        # Configuración de la tabla
        self.tree = ttk.Treeview(self.root, columns=("id","Edad", "Sexo", "BebidasSemana", "CervezasSemana", "BebidasFinSemana", "BebidasDestiladas", "VinosSemana", "PerdidasControl", "ProblemasDigestivos"), show="headings")
        self.tree.heading("id", text="id")
        self.tree.heading("Edad", text="Edad")
        self.tree.heading("Sexo", text="Sexo")
        self.tree.heading("BebidasSemana", text="Bebidas Semana")
        self.tree.heading("CervezasSemana", text="Cervezas Semana")
        self.tree.heading("BebidasFinSemana", text="Bebidas Fin Semana")
        self.tree.heading("BebidasDestiladas", text="Bebidas Destiladas")
        self.tree.heading("VinosSemana", text="Vinos Semana")
        self.tree.heading("PerdidasControl", text="Pérdidas de Control")
        self.tree.heading("ProblemasDigestivos", text="Problemas Digestivos")
        self.tree.pack()

    def visualizarGrafico(self):
        if not hasattr(self, 'rows') or not self.rows:
            messagebox.showerror("Error", "No hay datos para visualizar. Por favor, aplica un filtro primero.")
            return

        # Crear una ventana emergente para elegir el tipo de gráfico
        grafico_ventana = tk.Toplevel(self.root)
        grafico_ventana.title("Seleccionar tipo de gráfico")

        tk.Label(grafico_ventana, text="Selecciona el tipo de gráfico:").pack(pady=5)
        tipo_grafico_combobox = ttk.Combobox(grafico_ventana, values=["Barras", "Pastel", "Líneas"])
        tipo_grafico_combobox.pack(pady=5)

        tk.Button(grafico_ventana, text="Generar", command=lambda: self.generarGrafico(tipo_grafico_combobox.get(), grafico_ventana)).pack(pady=10)
    
    def generarGrafico(self, tipo, ventana):
        if tipo == "Barras":
            edades = [row[0] for row in self.rows]
            consumos = [row[2] for row in self.rows]
            plt.bar(edades, consumos)
            plt.xlabel('Edad')
            plt.ylabel('Consumo (Bebidas por semana)')
            plt.title('Consumo por Edad')
        elif tipo == "Pastel":
            problemas = [row[7] for row in self.rows if row[7] == 'SI']
            sin_problemas = [row[7] for row in self.rows if row[7] == 'NO']
            plt.pie([len(problemas), len(sin_problemas)], labels=['Con problemas', 'Sin problemas'], autopct='%1.1f%%')
            plt.title('Proporción de Encuestados con Problemas de Salud')
        elif tipo == "Líneas":
            edades = [row[0] for row in self.rows]
            consumos = [row[2] for row in self.rows]
            plt.plot(edades, consumos, marker='o')
            plt.xlabel('Edad')
            plt.ylabel('Consumo (Bebidas por semana)')
            plt.title('Tendencia de Consumo por Edad')
        else:
            messagebox.showerror("Error", "Tipo de gráfico no válido.")
            return

        plt.show()
        ventana.destroy()

    def consultarConFiltros(self):
        query = """SELECT idEncuesta ,Edad, Sexo, BebidasSemana, CervezasSemana, BebidasFinSemana, BebidasDestiladasSemana, VinosSemana, PerdidasControl, ProblemasDigestivos 
                   FROM Encuesta WHERE 1=1"""
        
        # Aplicar filtros según la condición seleccionada
        condicion = self.condicion_combobox.get()
        if condicion == "Alta frecuencia de consumo":
            query += " AND BebidasSemana > 7"
        elif condicion == "Más de 3 pérdidas de control":
            query += " AND PerdidasControl > 3"
        elif condicion == "Dolores de cabeza":
            query += " AND ProblemasDigestivos = 'SI'"
        elif condicion == "Presión alta":
            query += " AND TensionAlta = 'SI'"

        # Aplicar orden
        ordenar_por = self.ordenar_por_combobox.get()
        if ordenar_por:
            query += f" ORDER BY {ordenar_por}"

        cursor = self.connection.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()

        # Limpiar la tabla antes de mostrar los resultados
        for row in self.tree.get_children():
            self.tree.delete(row)

        for row in rows:
            self.tree.insert("", tk.END, values=row)

    def exportarACSV(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if not file_path:
            return

        try:
            with open(file_path, mode="w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow(["Edad", "Sexo", "Bebidas Semana", "Pérdidas de Control", "Problemas Digestivos"])

                for row_id in self.tree.get_children():
                    row = self.tree.item(row_id)['values']
                    writer.writerow(row)
            messagebox.showinfo("Éxito", "Datos exportados a CSV correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo exportar a CSV. Error: {e}")

    def abrirVentanaNuevaEncuesta(self):
        self.nueva_encuesta_window = tk.Toplevel(self.root)
        self.nueva_encuesta_window.title("Nueva Encuesta")

        # Entradas para la nueva encuesta
        tk.Label(self.nueva_encuesta_window, text="Edad: ").grid(row=0, column=0, sticky="w")
        self.edad_nueva_entry = tk.Entry(self.nueva_encuesta_window)
        self.edad_nueva_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.nueva_encuesta_window, text="Sexo: ").grid(row=1, column=0, sticky="w")
        self.sexo_nueva_entry = tk.Entry(self.nueva_encuesta_window)
        self.sexo_nueva_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(self.nueva_encuesta_window, text="Bebidas por semana: ").grid(row=2, column=0, sticky="w")
        self.bebidas_semana_entry = tk.Entry(self.nueva_encuesta_window)
        self.bebidas_semana_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(self.nueva_encuesta_window, text="Cervezas por semana: ").grid(row=3, column=0, sticky="w")
        self.cervezas_semana_entry = tk.Entry(self.nueva_encuesta_window)
        self.cervezas_semana_entry.grid(row=3, column=1, padx=5, pady=5)

        tk.Label(self.nueva_encuesta_window, text="Bebidas en fin de semana: ").grid(row=4, column=0, sticky="w")
        self.bebidas_fin_semana_entry = tk.Entry(self.nueva_encuesta_window)
        self.bebidas_fin_semana_entry.grid(row=4, column=1, padx=5, pady=5)

        tk.Label(self.nueva_encuesta_window, text="Bebidas destiladas por semana: ").grid(row=5, column=0, sticky="w")
        self.bebidas_destiladas_entry = tk.Entry(self.nueva_encuesta_window)
        self.bebidas_destiladas_entry.grid(row=5, column=1, padx=5, pady=5)

        tk.Label(self.nueva_encuesta_window, text="Vinos por semana: ").grid(row=6, column=0, sticky="w")
        self.vinos_semana_entry = tk.Entry(self.nueva_encuesta_window)
        self.vinos_semana_entry.grid(row=6, column=1, padx=5, pady=5)

        tk.Label(self.nueva_encuesta_window, text="Pérdidas de control: ").grid(row=7, column=0, sticky="w")
        self.perdidas_control_entry = tk.Entry(self.nueva_encuesta_window)
        self.perdidas_control_entry.grid(row=7, column=1, padx=5, pady=5)

        tk.Label(self.nueva_encuesta_window, text="Problemas digestivos (SI/NO): ").grid(row=8, column=0, sticky="w")
        self.problemas_digestivos_entry = tk.Entry(self.nueva_encuesta_window)
        self.problemas_digestivos_entry.grid(row=8, column=1, padx=5, pady=5)

        # Botón para guardar la nueva encuesta
        tk.Button(self.nueva_encuesta_window, text="Guardar", command=self.guardarNuevaEncuesta).grid(row=9, columnspan=2, pady=10)

    def guardarNuevaEncuesta(self):
        # Recuperar los valores de las entradas
        edad = self.edad_nueva_entry.get()
        sexo = self.sexo_nueva_entry.get()
        bebidas_semana = self.bebidas_semana_entry.get()
        cervezas_semana = self.cervezas_semana_entry.get()
        bebidas_fin_semana = self.bebidas_fin_semana_entry.get()
        bebidas_destiladas = self.bebidas_destiladas_entry.get()
        vinos_semana = self.vinos_semana_entry.get()
        perdidas_control = self.perdidas_control_entry.get()
        problemas_digestivos = self.problemas_digestivos_entry.get().upper()

        # Validación de los campos
        if not (edad and sexo and bebidas_semana and cervezas_semana and bebidas_fin_semana and bebidas_destiladas and vinos_semana and perdidas_control and problemas_digestivos):
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        try:
            cursor = self.connection.cursor()
            query = """INSERT INTO Encuesta (Edad, Sexo, BebidasSemana, CervezasSemana, BebidasFinSemana, BebidasDestiladasSemana, VinosSemana, PerdidasControl, ProblemasDigestivos)
                       VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            cursor.execute(query, (edad, sexo, bebidas_semana, cervezas_semana, bebidas_fin_semana, bebidas_destiladas, vinos_semana, perdidas_control, problemas_digestivos))
            self.connection.commit()
            messagebox.showinfo("Éxito", "Encuesta guardada exitosamente.")
            self.nueva_encuesta_window.destroy()
        except Error as e:
            messagebox.showerror("Error", f"No se pudo guardar la encuesta. Error: {e}")

    def abrirVentanaEliminarEncuesta(self):
        self.eliminar_encuesta_window = tk.Toplevel(self.root)
        self.eliminar_encuesta_window.title("Eliminar Encuesta")

        tk.Label(self.eliminar_encuesta_window, text="ID de la encuesta a eliminar: ").grid(row=0, column=0, padx=5, pady=5)
        self.id_eliminar_entry = tk.Entry(self.eliminar_encuesta_window)
        self.id_eliminar_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Button(self.eliminar_encuesta_window, text="Eliminar", command=self.eliminarEncuesta).grid(row=1, columnspan=2, pady=10)

    def eliminarEncuesta(self):
        id_encuesta = self.id_eliminar_entry.get()
        if not id_encuesta:
            messagebox.showerror("Error", "El ID de la encuesta es obligatorio.")
            return

        try:
            cursor = self.connection.cursor()
            query = "DELETE FROM Encuesta WHERE idEncuesta = %s"
            cursor.execute(query, (id_encuesta,))
            self.connection.commit()
            if cursor.rowcount > 0:
                messagebox.showinfo("Éxito", "Encuesta eliminada correctamente.")
                self.eliminar_encuesta_window.destroy()
            else:
                messagebox.showerror("Error", "No se encontró ninguna encuesta con ese ID.")
        except Error as e:
            messagebox.showerror("Error", f"No se pudo eliminar la encuesta. Error: {e}")

    def consultar(self):
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM Encuesta")
            self.rows = cursor.fetchall()

            # Limpiar la tabla antes de mostrar los resultados
            for row in self.tree.get_children():
                self.tree.delete(row)

            for row in self.rows:
                self.tree.insert("", tk.END, values=row)
        except Error as e:
            messagebox.showerror("Error", f"No se pudo realizar la consulta. Error: {e}")

    def abrirVentanaModificarEncuesta(self):
        # Crear ventana para modificar encuesta
        self.modificar_encuesta_window = tk.Toplevel(self.root)
        self.modificar_encuesta_window.title("Modificar Encuesta")

        # Entradas para modificar la encuesta
        tk.Label(self.modificar_encuesta_window, text="ID de la Encuesta: ").grid(row=0, column=0, sticky="w")
        self.id_modificar_entry = tk.Entry(self.modificar_encuesta_window)
        self.id_modificar_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.modificar_encuesta_window, text="Edad: ").grid(row=1, column=0, sticky="w")
        self.edad_modificar_entry = tk.Entry(self.modificar_encuesta_window)
        self.edad_modificar_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(self.modificar_encuesta_window, text="Sexo: ").grid(row=2, column=0, sticky="w")
        self.sexo_modificar_entry = tk.Entry(self.modificar_encuesta_window)
        self.sexo_modificar_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(self.modificar_encuesta_window, text="Bebidas por semana: ").grid(row=3, column=0, sticky="w")
        self.bebidas_semana_modificar_entry = tk.Entry(self.modificar_encuesta_window)
        self.bebidas_semana_modificar_entry.grid(row=3, column=1, padx=5, pady=5)

        tk.Label(self.modificar_encuesta_window, text="Cervezas por semana: ").grid(row=4, column=0, sticky="w")
        self.cervezas_semana_modificar_entry = tk.Entry(self.modificar_encuesta_window)
        self.cervezas_semana_modificar_entry.grid(row=4, column=1, padx=5, pady=5)

        tk.Label(self.modificar_encuesta_window, text="Bebidas en fin de semana: ").grid(row=5, column=0, sticky="w")
        self.bebidas_fin_semana_modificar_entry = tk.Entry(self.modificar_encuesta_window)
        self.bebidas_fin_semana_modificar_entry.grid(row=5, column=1, padx=5, pady=5)

        tk.Label(self.modificar_encuesta_window, text="Bebidas destiladas por semana: ").grid(row=6, column=0, sticky="w")
        self.bebidas_destiladas_modificar_entry = tk.Entry(self.modificar_encuesta_window)
        self.bebidas_destiladas_modificar_entry.grid(row=6, column=1, padx=5, pady=5)

        tk.Label(self.modificar_encuesta_window, text="Vinos por semana: ").grid(row=7, column=0, sticky="w")
        self.vinos_semana_modificar_entry = tk.Entry(self.modificar_encuesta_window)
        self.vinos_semana_modificar_entry.grid(row=7, column=1, padx=5, pady=5)

        tk.Label(self.modificar_encuesta_window, text="Pérdidas de control: ").grid(row=8, column=0, sticky="w")
        self.perdidas_control_modificar_entry = tk.Entry(self.modificar_encuesta_window)
        self.perdidas_control_modificar_entry.grid(row=8, column=1, padx=5, pady=5)

        tk.Label(self.modificar_encuesta_window, text="Problemas digestivos (SI/NO): ").grid(row=9, column=0, sticky="w")
        self.problemas_digestivos_modificar_entry = tk.Entry(self.modificar_encuesta_window)
        self.problemas_digestivos_modificar_entry.grid(row=9, column=1, padx=5, pady=5)

        # Botón para guardar los cambios
        tk.Button(self.modificar_encuesta_window, text="Modificar", command=self.modificarEncuesta).grid(row=10, columnspan=2, pady=10)


    def modificarEncuesta(self):
        # Recuperar los valores
        id_encuesta = self.id_modificar_entry.get()
        edad = self.edad_modificar_entry.get()
        sexo = self.sexo_modificar_entry.get()
        bebidas_semana = self.bebidas_semana_modificar_entry.get()
        cervezas_semana = self.cervezas_semana_modificar_entry.get()
        bebidas_fin_semana = self.bebidas_fin_semana_modificar_entry.get()
        bebidas_destiladas = self.bebidas_destiladas_modificar_entry.get()
        vinos_semana = self.vinos_semana_modificar_entry.get()
        perdidas_control = self.perdidas_control_modificar_entry.get()
        problemas_digestivos = self.problemas_digestivos_modificar_entry.get().upper()

        # Validar campos obligatorios
        if not id_encuesta:
            messagebox.showerror("Error", "El ID de la encuesta es obligatorio.")
            return

        try:
            cursor = self.connection.cursor()
            query = """
                UPDATE Encuesta 
                SET Edad = %s, Sexo = %s, BebidasSemana = %s, CervezasSemana = %s, BebidasFinSemana = %s,
                    BebidasDestiladasSemana = %s, VinosSemana = %s, PerdidasControl = %s, ProblemasDigestivos = %s
                WHERE idEncuesta = %s
            """
            cursor.execute(query, (edad, sexo, bebidas_semana, cervezas_semana, bebidas_fin_semana, bebidas_destiladas, 
                                   vinos_semana, perdidas_control, problemas_digestivos, id_encuesta))
            self.connection.commit()
            if cursor.rowcount > 0:
                messagebox.showinfo("Éxito", "Encuesta modificada correctamente.")
                self.modificar_encuesta_window.destroy()
            else:
                messagebox.showerror("Error", "No se encontró ninguna encuesta con ese ID.")
        except Error as e:
            messagebox.showerror("Error", f"No se pudo modificar la encuesta. Error: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = Hito2(root)
    root.mainloop()
