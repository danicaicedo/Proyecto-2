import tkinter as tk
from tkinter import simpledialog, messagebox


class Socio:
    def __init__(self, cedula, nombre, tipo_suscripcion):
        self.cedula = cedula
        self.nombre = nombre
        self.fondos_disponibles = 0
        self.tipo_suscripcion = tipo_suscripcion
        self.facturas_sin_pagar = []
        self.personas_autorizadas = []

    def agregar_fondos(self, monto):
        if self.tipo_suscripcion == 'VIP':
            max_fondos = 5000000
        else:
            max_fondos = 1000000
        self.fondos_disponibles = min(self.fondos_disponibles + monto, max_fondos)

    def generar_factura(self, concepto, valor, nombre_generador):
        if valor <= self.fondos_disponibles:
            self.facturas_sin_pagar.append({'concepto': concepto, 'valor': valor, 'generador': nombre_generador})
            self.fondos_disponibles -= valor
            return True
        else:
            return False

    def pagar_factura(self, indice_factura):
        if 0 <= indice_factura < len(self.facturas_sin_pagar):
            factura = self.facturas_sin_pagar.pop(indice_factura)
            self.fondos_disponibles += factura['valor']
            return True
        else:
            return False

    def agregar_persona_autorizada(self, persona_autorizada):
        if persona_autorizada not in self.personas_autorizadas:
            self.personas_autorizadas.append(persona_autorizada)
            print(f"Persona autorizada '{persona_autorizada}' registrada correctamente para el socio '{self.nombre}'")
        else:
            print(f"La persona autorizada '{persona_autorizada}' ya está registrada para el socio '{self.nombre}'")

    def eliminar_persona_autorizada(self, persona_autorizada):
        if persona_autorizada not in self.personas_autorizadas:
            print(f"La persona autorizada '{persona_autorizada}' no está registrada para el socio '{self.nombre}'")
            return False
        for factura in self.facturas_sin_pagar:
            if factura['generador'] == persona_autorizada:
                print(f"No se puede eliminar la persona autorizada '{persona_autorizada}', tiene facturas pendientes.")
                return False
        self.personas_autorizadas.remove(persona_autorizada)
        print(f"Persona autorizada '{persona_autorizada}' eliminada correctamente para el socio '{self.nombre}'")
        return True


class ClubSocial:
    def __init__(self):
        self.socios = []
        self.socios_vip = 0

    def afiliar_socio(self, cedula, nombre, tipo_suscripcion):
        for socio in self.socios:
            if socio.cedula == cedula:
                messagebox.showerror("Error", "Ya existe un socio con esta cédula.")
                return False
        
        if tipo_suscripcion == 'VIP' and self.socios_vip >= 3:
            messagebox.showerror("Error", "No se pueden afiliar más socios VIP.")
            return False
        
        nuevo_socio = Socio(cedula, nombre, tipo_suscripcion)
        if tipo_suscripcion == 'VIP':
            self.socios_vip += 1
        
        nuevo_socio.agregar_fondos(100000 if tipo_suscripcion == 'VIP' else 50000)
        self.socios.append(nuevo_socio)
        messagebox.showinfo("Afiliar socio", f"Socio '{nombre}' afiliado correctamente.")
        return True

    def registrar_persona_autorizada(self, cedula_socio, persona_autorizada):
        for socio in self.socios:
            if socio.cedula == cedula_socio:
                socio.agregar_persona_autorizada(persona_autorizada)
                return True
        messagebox.showerror("Error", "No se encontró ningún socio con esa cédula.")
        return False

    def pagar_factura(self, cedula_socio, indice_factura):
        for socio in self.socios:
            if socio.cedula == cedula_socio:
                if socio.pagar_factura(indice_factura):
                    messagebox.showinfo("Pagar factura", "Factura pagada correctamente.")
                    return True
                else:
                    messagebox.showerror("Error", "Índice de factura inválido o fondos insuficientes.")
                    return False
        messagebox.showerror("Error", "No se encontró ningún socio con esa cédula.")
        return False

    def registrar_consumo(self, cedula_socio, concepto, valor, nombre_generador):
        for socio in self.socios:
            if socio.cedula == cedula_socio:
                if socio.generar_factura(concepto, valor, nombre_generador):
                    messagebox.showinfo("Registrar consumo", "Consumo registrado correctamente.")
                    return True
                else:
                    messagebox.showerror("Error", "Fondos insuficientes para registrar el consumo.")
                    return False
        messagebox.showerror("Error", "No se encontró ningún socio con esa cédula.")
        return False

    def aumentar_fondos_socio(self, cedula_socio, monto):
        for socio in self.socios:
            if socio.cedula == cedula_socio:
                socio.agregar_fondos(monto)
                messagebox.showinfo("Aumentar fondos de un socio", "Fondos agregados correctamente.")
                return True
        messagebox.showerror("Error", "No se encontró ningún socio con esa cédula.")
        return False


class ClubSocialApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Club Social App")

        # Frame principal
        self.main_frame = tk.Frame(root, bg="white")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Cuadro azul para el título
        title_frame = tk.Frame(self.main_frame, bg="blue")
        title_frame.pack(pady=10)
        
        # Etiqueta de bienvenida dentro del cuadro azul
        self.label = tk.Label(title_frame, text="Bienvenido al Club Social", font=("Helvetica", 18), bg="blue", fg="white")
        self.label.pack(pady=10)

        # Botones para cada opción
        options_frame = tk.Frame(self.main_frame, bg="white")
        options_frame.pack()

        self.button_afiliar = tk.Button(options_frame, text="Afiliar un socio", font=("Helvetica", 12), command=self.afiliar_socio)
        self.button_afiliar.grid(row=0, column=0, padx=10, pady=5)

        self.button_registrar = tk.Button(options_frame, text="Registrar una persona autorizada", font=("Helvetica", 12), command=self.registrar_persona_autorizada)
        self.button_registrar.grid(row=0, column=1, padx=10, pady=5)

        self.button_pagar = tk.Button(options_frame, text="Pagar una factura", font=("Helvetica", 12), command=self.pagar_factura)
        self.button_pagar.grid(row=1, column=0, padx=10, pady=5)

        self.button_consumo = tk.Button(options_frame, text="Registrar un consumo", font=("Helvetica", 12), command=self.registrar_consumo)
        self.button_consumo.grid(row=1, column=1, padx=10, pady=5)

        self.button_fondos = tk.Button(options_frame, text="Aumentar fondos de un socio", font=("Helvetica", 12), command=self.aumentar_fondos_socio)
        self.button_fondos.grid(row=2, column=0, columnspan=2, padx=10, pady=5)

        # Instanciar el club social
        self.club_social = ClubSocial()


    def afiliar_socio(self):
        cedula = simpledialog.askstring("Afiliar socio", "Ingrese la cédula del socio:")
        if cedula:
            nombre = simpledialog.askstring("Afiliar socio", "Ingrese el nombre del socio:")
            tipo_suscripcion = simpledialog.askstring("Afiliar socio", "Ingrese el tipo de suscripción (VIP o Regular):").upper()
            if tipo_suscripcion in ['VIP', 'REGULAR']:
                self.club_social.afiliar_socio(cedula, nombre, tipo_suscripcion)
            else:
                messagebox.showerror("Error", "Tipo de suscripción inválido. Debe ser VIP o Regular.")

    def registrar_persona_autorizada(self):
        cedula_socio = simpledialog.askstring("Registrar persona autorizada", "Ingrese la cédula del socio:")
        if cedula_socio:
            persona_autorizada = simpledialog.askstring("Registrar persona autorizada", "Ingrese el nombre de la persona autorizada:")
            if persona_autorizada:
                self.club_social.registrar_persona_autorizada(cedula_socio, persona_autorizada)

    def pagar_factura(self):
        cedula_socio = simpledialog.askstring("Pagar factura", "Ingrese la cédula del socio que va a pagar la factura:")
        if cedula_socio:
            indice_factura = simpledialog.askinteger("Pagar factura", "Ingrese el índice de la factura a pagar:")
            if indice_factura is not None:
                self.club_social.pagar_factura(cedula_socio, indice_factura)

    def registrar_consumo(self):
        cedula_socio = simpledialog.askstring("Registrar consumo", "Ingrese la cédula del socio que realiza el consumo:")
        if cedula_socio:
            concepto = simpledialog.askstring("Registrar consumo", "Ingrese el concepto del consumo:")
            if concepto:
                valor = simpledialog.askfloat("Registrar consumo", "Ingrese el valor del consumo:")
                if valor is not None:
                    nombre_generador = simpledialog.askstring("Registrar consumo", "Ingrese el nombre del generador del consumo:")
                    if nombre_generador:
                        self.club_social.registrar_consumo(cedula_socio, concepto, valor, nombre_generador)

    def aumentar_fondos_socio(self):
        cedula_socio = simpledialog.askstring("Aumentar fondos de un socio", "Ingrese la cédula del socio al que desea aumentar los fondos:")
        if cedula_socio:
            monto = simpledialog.askfloat("Aumentar fondos de un socio", "Ingrese el monto a agregar:")
            if monto is not None:
                self.club_social.aumentar_fondos_socio(cedula_socio, monto)


root = tk.Tk()
app = ClubSocialApp(root)
root.mainloop()
