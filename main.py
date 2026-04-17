import customtkinter as ctk
from tkinter import ttk, messagebox, simpledialog
import database  
from Club_unsada import Arquero, JugadorCampo

class AppFutbolPro(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configuración General
        self.title("UNSAdA Stats - Gestión Deportiva")
        self.geometry("1200x750")
        ctk.set_appearance_mode("Light")
        ctk.set_default_color_theme("green")

        # Colores institucionales
        self.color_primario = "#2DAB66"  # Verde UNSAdA
        self.color_secundario = "#005596" # Azul UNSAdA
        self.bg_color = "#F0F2F5"

        self.configure(fg_color=self.bg_color)

        # Grilla: Sidebar (Izquierda) y Cuerpo Principal (Derecha)
        self.grid_columnconfigure(0, weight=0) # Sidebar fija
        self.grid_columnconfigure(1, weight=1) # Contenido expandible
        self.grid_rowconfigure(1, weight=1)

        self.crear_sidebar_completa()
        self.crear_barra_superior_acciones()
        self.crear_tabla_central()
        
        self.actualizar_vista()

    def crear_sidebar_completa(self):
        """Sidebar Izquierda: Logo + Buscador + Resumen + Eliminar"""
        self.sidebar = ctk.CTkFrame(self, width=260, corner_radius=0, fg_color="white", border_width=1)
        self.sidebar.grid(row=0, column=0, rowspan=2, sticky="nsew")
        
        # 1. Logo
        lbl_logo = ctk.CTkLabel(self.sidebar, text="⚽ UNSAdA", font=("Inter", 26, "bold"), text_color=self.color_primario)
        lbl_logo.pack(pady=(40, 20))

        # 2. Buscador (Debajo de UNSAdA)
        ctk.CTkLabel(self.sidebar, text="BUSCAR JUGADOR", font=("Segoe UI", 10, "bold"), text_color="gray").pack(pady=(10, 0))
        self.entry_busqueda = ctk.CTkEntry(self.sidebar, placeholder_text="N° o Apellido...", width=200, height=35, corner_radius=15)
        self.entry_busqueda.pack(pady=(5, 30))
        self.entry_busqueda.bind("<KeyRelease>", lambda e: self.actualizar_vista())

        # Separador visual
        ctk.CTkFrame(self.sidebar, height=2, width=180, fg_color="#F0F0F0").pack()

        # 3. Resumen Estético (Cards una debajo de la otra)
        ctk.CTkLabel(self.sidebar, text="ESTADÍSTICAS GLOBALES", font=("Segoe UI", 10, "bold"), text_color="gray").pack(pady=(30, 10))
        
        self.card_total = self.crear_card_sidebar("TOTAL JUGADORES", self.color_secundario)
        self.card_goles = self.crear_card_sidebar("GOLES EQUIPO", self.color_primario)

        # 4. Botón Eliminar (Al fondo)
        self.btn_del = ctk.CTkButton(self.sidebar, text="🗑 Eliminar Selección", fg_color="transparent", 
                                     text_color="#E74C3C", border_width=2, border_color="#E74C3C",
                                     hover_color="#FDEDEC", command=self.eliminar_jugador,
                                     width=180, height=40, corner_radius=15)
        self.btn_del.pack(side="bottom", pady=40)

    def crear_card_sidebar(self, titulo, color):
        """Pequeñas tarjetas para la sidebar"""
        f = ctk.CTkFrame(self.sidebar, corner_radius=15, fg_color="#F8F9FA", border_width=1, border_color="#E0E0E0")
        f.pack(pady=10, padx=25, fill="x")
        ctk.CTkLabel(f, text=titulo, font=("Segoe UI", 9, "bold"), text_color="#555").pack(pady=(10,0))
        lbl_val = ctk.CTkLabel(f, text="0", font=("Segoe UI", 28, "bold"), text_color=color)
        lbl_val.pack(pady=(0,10))
        return lbl_val

    def crear_barra_superior_acciones(self):
        """Barra de herramientas en la parte superior"""
        self.header = ctk.CTkFrame(self, height=70, fg_color="transparent")
        self.header.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        
        btn_cfg = {"height": 45, "corner_radius": 12, "font": ("Segoe UI", 12, "bold")}

        # Botones alineados a la izquierda
        ctk.CTkButton(self.header, text="+ Nuevo Jugador", command=self.ventana_registrar, 
                      fg_color=self.color_secundario, **btn_cfg).pack(side="left", padx=10)
        
        ctk.CTkButton(self.header, text="⚽ Sumar Goles", command=lambda: self.modificar_stats_rapido("goles"), 
                      fg_color=self.color_primario, **btn_cfg).pack(side="left", padx=10)
        
        ctk.CTkButton(self.header, text="⏱ Sumar Minutos", command=lambda: self.modificar_stats_rapido("minutos"), 
                      fg_color="#F39C12", **btn_cfg).pack(side="left", padx=10)
        
        ctk.CTkButton(self.header, text="✏️ Editar Datos", command=self.ventana_editar, 
                      fg_color="#34495E", **btn_cfg).pack(side="left", padx=10)

    def crear_tabla_central(self):
        self.frame_tabla = ctk.CTkFrame(self, corner_radius=20, fg_color="white")
        self.frame_tabla.grid(row=1, column=1, padx=20, pady=(0,20), sticky="nsew")

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background="white", rowheight=40, font=("Segoe UI", 11), borderwidth=0)
        style.configure("Treeview.Heading", background="#F8F9FA", foreground=self.color_secundario, font=("Segoe UI", 12, "bold"))
        style.map("Treeview", background=[('selected', self.color_primario)], foreground=[('selected', 'white')])

        self.tabla = ttk.Treeview(self.frame_tabla, columns=("Ape", "Cam", "Pos", "Gol", "Min"), show="headings")
        headings = {"Ape": "APELLIDO", "Cam": "N°", "Pos": "POSICIÓN", "Gol": "GOLES", "Min": "MINUTOS"}
        for key, val in headings.items():
            self.tabla.heading(key, text=val)
            self.tabla.column(key, anchor="center", width=120)
        self.tabla.pack(expand=True, fill="both", padx=15, pady=15)

    def actualizar_vista(self):
        for i in self.tabla.get_children(): self.tabla.delete(i)
        busqueda = self.entry_busqueda.get().lower()
        jugadores = database.obtener_todos()
        total_goles = 0
        for j in jugadores:
            # Filtrar por apellido o por dorsal
            if busqueda in str(j[0]).lower() or busqueda in str(j[1]):
                self.tabla.insert("", "end", values=j)
                total_goles += j[3]
        
        self.card_total.configure(text=str(len(self.tabla.get_children())))
        self.card_goles.configure(text=str(total_goles))

    def abrir_formulario(self, titulo, datos=None):
        v = ctk.CTkToplevel(self)
        v.title(titulo)
        v.geometry("400x650")
        v.configure(fg_color="white")
        v.after(100, v.lift)
        
        ctk.CTkLabel(v, text=titulo, font=("Segoe UI", 20, "bold"), text_color=self.color_secundario).pack(pady=20)
        
        def campo(texto, color="black"):
            ctk.CTkLabel(v, text=texto, font=("Segoe UI", 11, "bold"), text_color=color).pack(pady=(10,0))
            e = ctk.CTkEntry(v, width=280, height=35, corner_radius=8)
            e.pack(pady=5)
            return e

        ent_ape = campo("Apellido:")
        ent_cam = campo("Número de Camiseta (Dorsal):")
        
        def verificar_posicion(seleccion):
            if seleccion == "Arquero":
                ent_gol.delete(0, 'end')
                ent_gol.insert(0, "0")
                ent_gol.configure(state="disabled", fg_color="#E0E0E0") # Gris y bloqueado
            else:
                ent_gol.configure(state="normal", fg_color="white") # Blanco y activo
        
        ctk.CTkLabel(v, text="Posición del Jugador:", font=("Segoe UI", 11, "bold")).pack(pady=(10,0))
        combo_pos = ctk.CTkComboBox(v, values=["Arquero", "Defensor", "Central", "Delantero"], 
                                    width=280, command=verificar_posicion)
        combo_pos.pack(pady=5)

        ent_gol = campo("Goles Totales:", self.color_primario)
        ent_min = campo("Minutos Totales:", "#F39C12")

        if datos:
            ent_ape.insert(0, datos[0])
            ent_cam.insert(0, datos[1])
            ent_cam.configure(state="readonly")
            combo_pos.set(datos[2])
            ent_gol.insert(0, datos[3])
            ent_min.insert(0, datos[4])
            verificar_posicion(datos[2])
        else:
            ent_gol.insert(0, "0")
            ent_min.insert(0, "0")

        def guardar():
            try:
                # MODIFICADO: Lógica de filtro para Arquero
                posicion_actual = combo_pos.get()
                
                if posicion_actual == "Arquero":
                    g = 0  # Forzamos 0 goles si es Arquero
                else:
                    g = int(ent_gol.get())
                
                m = int(ent_min.get())                
                
                # MODIFICADO: Uso de las clases correspondientes según posición
                if posicion_actual == "Arquero":
                    nuevo = Arquero(ent_cam.get(), ent_ape.get(), m)               
                else:
                    nuevo = JugadorCampo(ent_cam.get(), ent_ape.get(), posicion_actual, g, m)
                    
                if database.guardar_jugador(nuevo):
                    self.actualizar_vista()
                    v.destroy()
                    messagebox.showinfo("Éxito", "Jugador guardado/actualizado.")
            except ValueError: # MODIFICADO: Especificamos ValueError para mayor claridad
                messagebox.showerror("Error", "Revisa que Goles y Minutos sean números.")

        ctk.CTkButton(v, text="Confirmar Datos", command=guardar, fg_color=self.color_primario, 
                      height=45, width=220, corner_radius=20).pack(pady=35)
    def ventana_registrar(self): self.abrir_formulario("Registrar Nuevo Jugador")
    
    def ventana_editar(self):
        sel = self.tabla.selection()
        if not sel: return messagebox.showwarning("Aviso", "Selecciona un jugador para editar.")
        self.abrir_formulario("Editar Jugador", self.tabla.item(sel)['values'])

    def modificar_stats_rapido(self, tipo):
        sel = self.tabla.selection()
        if not sel: 
            return messagebox.showwarning("Aviso", "Elige un jugador de la lista.")
        
        item = self.tabla.item(sel)['values']
        apellido = item[0]
        camiseta = item[1]
        posicion = item[2] # Obtenemos la posición de la tabla

        # --- NUEVO: FILTRO DE SEGURIDAD PARA ARQUEROS ---
        if tipo == "goles" and posicion == "Arquero":
            return messagebox.showwarning(
                "Acción no permitida", 
                f"No se pueden sumar goles a {apellido} porque su posición es Arquero."
            )
        valor = simpledialog.askinteger("Suma Rápida", f"¿Cuántos {tipo} sumó hoy {item[0]}?")
        if valor is not None:
            if database.actualizar_estadistica(item[1], tipo, valor):
                self.actualizar_vista()

    def eliminar_jugador(self):
        sel = self.tabla.selection()
        if not sel: return
        item = self.tabla.item(sel)['values']
        if messagebox.askyesno("Confirmar Eliminación", f"¿Estás seguro de borrar a {item[0]}?"):
            if database.eliminar_jugador_db(item[1]):
                self.actualizar_vista()

if __name__ == "__main__":
    app = AppFutbolPro()
    app.mainloop()