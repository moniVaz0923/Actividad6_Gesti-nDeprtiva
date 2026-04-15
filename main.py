import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import database 
from Club_unsada import Arquero, JugadorCampo
import urllib.request
import io
from PIL import Image, ImageTk

class AppFutbol:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestión Deportiva UNSADA 2026")
        self.root.geometry("1100x650")
        self.root.configure(bg="#f4f4f4")
        
        self.configurar_estilos()
        self.crear_widgets_principales()
        self.actualizar_tabla_desde_db()

    def configurar_estilos(self):
        style = ttk.Style()
        style.theme_use('clam')
        azul_unsada = "#1a2a6c"
        dorado_unsada = "#f1c40f"
        
        style.configure("Treeview.Heading", font=("Segoe UI", 11, "bold"), background=azul_unsada, foreground="white")
        style.configure("Menu.TButton", font=("Segoe UI", 10, "bold"), padding=10)
        
        style.map("Menu.TButton",
                  background=[('active', dorado_unsada), ('!active', azul_unsada)],
                  foreground=[('active', 'black'), ('!active', 'white')])
        
        style.configure("Danger.TButton", font=("Segoe UI", 10, "bold"), foreground="white", background="#c0392b")
        style.map("Danger.TButton", background=[('active', '#e74c3c')])
        
    def crear_widgets_principales(self):
        # --- HEADER ---
        header = tk.Frame(self.root, bg="#1a2a6c")
        header.pack(fill="x")
        tk.Label(header, text="SISTEMA DE ESTADÍSTICAS UNSADA", font=("Segoe UI", 18, "bold"), fg="white", bg="#1a2a6c").pack(pady=15)

        # --- CONTENEDOR CENTRAL ---
        mid_container = tk.Frame(self.root, bg="#f4f4f4")
        mid_container.pack(fill="both", expand=True, padx=20, pady=10)

        # Panel Izquierdo: Menú
        panel_menu = tk.Frame(mid_container, bg="#f4f4f4")
        panel_menu.pack(side="left", fill="y", padx=10)

        ttk.Button(panel_menu, text="➕ REGISTRAR JUGADOR", style="Menu.TButton", width=25, command=self.ventana_registrar).pack(pady=5)
        ttk.Button(panel_menu, text="⚽ CARGAR GOLES", style="Menu.TButton", width=25, command=lambda: self.ventana_stats("goles")).pack(pady=5)
        ttk.Button(panel_menu, text="⏱ CARGAR MINUTOS", style="Menu.TButton", width=25, command=lambda: self.ventana_stats("minutos")).pack(pady=5)
        ttk.Button(panel_menu, text="📝 MODIFICAR DATOS", style="Menu.TButton", width=25, command=self.ventana_modificar).pack(pady=5)
        ttk.Button(panel_menu, text="🗑 ELIMINAR JUGADOR", style="Danger.TButton", width=25, command=self.eliminar_jugador).pack(pady=20)

        try:
            url_imagen = "https://cdn-icons-png.flaticon.com/512/53/53283.png" 
            hdr = {'User-Agent': 'Mozilla/5.0'}
            req = urllib.request.Request(url_imagen, headers=hdr)
            with urllib.request.urlopen(req) as response:
                data = response.read()
            
            imagen_raw = Image.open(io.BytesIO(data))
            imagen_raw = imagen_raw.resize((150, 150))
            self.foto_web = ImageTk.PhotoImage(imagen_raw)
            
            lbl_img = tk.Label(panel_menu, image=self.foto_web, bg="#f4f4f4")
            lbl_img.pack(pady=20)
        except Exception:
            tk.Label(panel_menu, text="⚽", font=("Arial", 50), bg="#f4f4f4", fg="#1a2a6c").pack(pady=20)

        # Panel Derecho: Tabla
        frame_tabla = tk.Frame(mid_container, bg="#f4f4f4")
        frame_tabla.pack(side="right", fill="both", expand=True)

        self.tabla = ttk.Treeview(frame_tabla, columns=("apellido", "camiseta", "posicion", "goles", "minutos"), show="headings")
        
        # --- MODIFICACIÓN NUEVA: AJUSTE DE ANCHO DE COLUMNAS ---
        columnas_config = {
            "apellido": 150,
            "camiseta": 80,
            "posicion": 120,
            "goles": 80,
            "minutos": 100
        }
        
        for col, ancho in columnas_config.items():
            self.tabla.heading(col, text=col.upper())
            self.tabla.column(col, anchor="center", width=ancho, minwidth=ancho, stretch=True)
        # ------------------------------------------------------

        self.tabla.pack(fill="both", expand=True)

    def eliminar_jugador(self):
        seleccion = self.tabla.selection()
        if not seleccion:
            messagebox.showwarning("Atención", "Seleccioná un jugador de la tabla")
            return
        
        camiseta = self.tabla.item(seleccion)['values'][1]
        if messagebox.askyesno("Confirmar", "¿Eliminar jugador?"):
            if database.eliminar_jugador_db(camiseta):
                self.actualizar_tabla_desde_db()
                
    def actualizar_tabla_desde_db(self):
        for i in self.tabla.get_children(): self.tabla.delete(i)
        try:
            for j in database.obtener_todos(): self.tabla.insert("", tk.END, values=j)
        except: pass 
                
    def ventana_registrar(self):
        v = tk.Toplevel(self.root)
        v.title("Nuevo Registro")
        v.geometry("300x350")
        v.grab_set()

        ttk.Label(v, text="Apellido:").pack(pady=5)
        ent_ape = ttk.Entry(v)
        ent_ape.pack()

        ttk.Label(v, text="Camiseta:").pack(pady=5)
        ent_cam = ttk.Entry(v)
        ent_cam.pack()

        ttk.Label(v, text="Posición:").pack(pady=5)
        combo = ttk.Combobox(v, values=["Arquero", "Defensor", "Central", "Delantero"], state="readonly")
        combo.current(0)
        combo.pack()

        def guardar():
            ape, cam, pos = ent_ape.get(), ent_cam.get(), combo.get()
            if not ape or not cam: 
                return messagebox.showwarning("Error", "Faltan datos", parent=v)
            
            if pos == "Arquero": nuevo = Arquero(cam, ape, 0)
            else: nuevo = JugadorCampo(cam, ape, pos, 0, 0)
            
            if database.guardar_jugador(nuevo):
                messagebox.showinfo("Éxito", "Jugador guardado", parent=v)
                self.actualizar_tabla_desde_db()
                v.destroy()

        ttk.Button(v, text="Confirmar Registro", command=guardar).pack(pady=20)

    def ventana_modificar(self):
        v = tk.Toplevel(self.root)
        v.title("Modificar Jugador")
        v.geometry("350x400")
        v.grab_set()

        ttk.Label(v, text="Buscar por Camiseta para editar:").pack(pady=5)
        ent_bus = ttk.Entry(v)
        ent_bus.pack()

        ttk.Label(v, text="Apellido:").pack(pady=5)
        ent_ape = ttk.Entry(v)
        ent_ape.pack()
        
        ttk.Label(v, text="Nueva Posición:").pack(pady=5)
        combo = ttk.Combobox(v, values=["Arquero", "Defensor", "Central", "Delantero"], state="readonly")
        combo.pack()

        def buscar_para_editar():
            res = database.buscar_por_camiseta(ent_bus.get())
            if res:
                ent_ape.delete(0, tk.END)
                ent_ape.insert(0, res[0][0])
                combo.set(res[0][2])
            else:
                messagebox.showerror("Error", "No encontrado", parent=v)

        def actualizar():
            if database.actualizar_jugador_completo(ent_bus.get(), ent_ape.get(), combo.get()):
                messagebox.showinfo("Éxito", "Datos actualizados", parent=v)
                self.actualizar_tabla_desde_db()
                v.destroy()

        ttk.Button(v, text="🔍 Cargar Datos", command=buscar_para_editar).pack(pady=5)
        ttk.Button(v, text="💾 Guardar Cambios", command=actualizar).pack(pady=20)

    def ventana_stats(self, tipo):
        seleccion = self.tabla.selection()
        if not seleccion: return messagebox.showwarning("Atención", "Seleccioná un jugador en la tabla")
        
        camiseta = self.tabla.item(seleccion)['values'][1]
        valor = simpledialog.askinteger("Cargar " + tipo, f"¿Cuántos {tipo} desea sumar?")
        
        if valor is not None:
            database.actualizar_estadistica(camiseta, tipo, valor)
            self.actualizar_tabla_desde_db()

if __name__ == "__main__":
    root = tk.Tk()
    app = AppFutbol(root)
    root.mainloop()