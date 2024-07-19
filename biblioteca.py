import streamlit as st

class Libro:
    def __init__(self, titulo, autor, isbn):
        self.titulo = titulo
        self.autor = autor
        self.isbn = isbn
        self.disponible = True
    
    def prestar(self):
        if self.disponible:
            self.disponible = False
            return f'El libro {self.titulo} ha sido prestado.'
        else:
            return f'El libro {self.titulo} no está disponible ya que ha sido prestado.'
            
    def devolver(self):
        if not self.disponible:
            self.disponible = True
            return f'El libro {self.titulo} ha sido devuelto.'
        else:
            return f'El libro {self.titulo} ya está disponible.'

    def informacion(self):
        return (f'Libro: {self.titulo}\n'
                f'Autor: {self.autor}\n'
                f'ISBN: {self.isbn}\n'
                f'Estado: {"disponible" if self.disponible else "no disponible"}')

class Miembro:
    def __init__(self, nombre, id_miembro):
        self.nombre = nombre
        self.id_miembro = id_miembro
        self.libros_prestados = []
        
    def prestar_libro(self, libro):
        self.libros_prestados.append(libro)
        return f'El libro {libro.titulo} ha sido prestado a {self.nombre}.'
    
    def devolver_libro(self, libro):
        if libro in self.libros_prestados:
            self.libros_prestados.remove(libro)
            return f'El libro {libro.titulo} ha sido devuelto por {self.nombre}.'
        else:
            return f'El libro {libro.titulo} no estaba prestado a {self.nombre}.'
    
    def informacion(self):
        return (f'Nombre: {self.nombre}\n'
                f'ID: {self.id_miembro}\n'
                f'Los libros prestados son {[libro.titulo for libro in self.libros_prestados]}')

class Biblioteca:
    def __init__(self, nombre):
        self.nombre = nombre
        self.libros = []    # Lista para almacenar libros
        self.miembros = []  # Lista para almacenar miembros
        
    def agregar_libro(self, libro):
        self.libros.append(libro)
        return f'El libro {libro.titulo} ha sido agregado a la biblioteca.'
    
    def agregar_miembro(self, miembro):
        self.miembros.append(miembro)
        return f'El miembro {miembro.nombre} ha sido agregado a la biblioteca.'
    
    def informacion_libros(self):
        if not self.libros:
            return 'No hay libros registrados en la biblioteca.'
        info = f'Los libros en la biblioteca "{self.nombre}" son:\n\n'
        for libro in self.libros:
            info += libro.informacion() + '\n\n'
        return info
    
    def informacion_miembros(self):
        if not self.miembros:
            return 'No hay miembros registrados en la biblioteca.'
        info = f'Los miembros de la biblioteca "{self.nombre}" son:\n\n'
        for miembro in self.miembros:
            info += miembro.informacion() + '\n\n'
        return info

def inicializar_biblioteca():
    if 'biblioteca' not in st.session_state:
        st.session_state.biblioteca = Biblioteca("Biblioteca Central")

def main():
    inicializar_biblioteca()
    biblioteca = st.session_state.biblioteca

    # Configurar la página de Streamlit
    st.title("Sistema de Gestión de Biblioteca")

    # Opciones en la barra lateral
    option = st.sidebar.selectbox(
        'Selecciona una opción:',
        ('Agregar Libro', 'Agregar Miembro', 'Información de Libros', 'Información de Miembros')
    )

    # Manejo de opciones
    if option == 'Agregar Libro':
        st.header("Agregar Libro")
        with st.form("form_agregar_libro"):
            titulo = st.text_input("Título")
            autor = st.text_input("Autor")
            isbn = st.text_input("ISBN")
            submit_libro = st.form_submit_button("Agregar Libro")

            if submit_libro:
                if titulo and autor and isbn:
                    try:
                        isbn = int(isbn)
                        libro = Libro(titulo, autor, isbn)
                        mensaje = biblioteca.agregar_libro(libro)
                        st.success(mensaje)
                    except ValueError:
                        st.error("El ISBN debe ser un número.")
                else:
                    st.error("Por favor, completa todos los campos.")

    elif option == 'Agregar Miembro':
        st.header("Agregar Miembro")
        with st.form("form_agregar_miembro"):
            nombre_miembro = st.text_input("Nombre")
            id_miembro = st.text_input("ID")
            submit_miembro = st.form_submit_button("Agregar Miembro")

            if submit_miembro:
                if nombre_miembro and id_miembro:
                    miembro = Miembro(nombre_miembro, id_miembro)
                    mensaje = biblioteca.agregar_miembro(miembro)
                    st.success(mensaje)
                else:
                    st.error("Por favor, completa todos los campos.")

    elif option == 'Información de Libros':
        st.header("Información de los Libros")
        if st.button("Mostrar Información de Libros"):
            st.text(biblioteca.informacion_libros())

    elif option == 'Información de Miembros':
        st.header("Información de los Miembros")
        if st.button("Mostrar Información de Miembros"):
            st.text(biblioteca.informacion_miembros())

if __name__ == "__main__":
    main()
