SREE PRO - Sistema de Registro de Entradas y Salidas
Este proyecto es una solución integral desarrollada por High Softwares From Gravis Systems para gestionar el control de asistencia de aprendices en ambientes de formación. Permite el registro rápido de entradas/salidas, la gestión administrativa de usuarios y la visualización de reportes personales mediante un calendario interactivo.



🚀 Instalación Rápida
Para instalar todas las librerías necesarias, abre tu terminal en la carpeta del proyecto y ejecuta:

python -m pip install -r requirements.txt




🛠️ Descripción de los Archivos
1. main.py (Interfaz de Usuario)
Es el núcleo del programa. Utiliza la librería Tkinter para crear una experiencia visual moderna y organizada. Se divide en cuatro módulos principales:

Gateway (Inicio): Pantalla central para elegir entre el modo Terminal, el Panel Administrativo o el Perfil de Aprendiz.

Terminal de Aprendices: Un módulo optimizado para el registro rápido de asistencia usando el número de documento. Valida en tiempo real que no existan entradas duplicadas sin su correspondiente salida.

Panel de Aprendiz (Calendario): Incluye un Calendario Físico (tkcalendar) donde el usuario puede hacer clic en cualquier día para ver sus tarjetas de entrada y salida, además del cálculo automático de horas trabajadas en esa fecha.

Panel Administrativo: Suite completa para la gestión de la base de datos que incluye:

Historial: Visualización de todos los registros del sistema.

Gestión: Filtros por nombre o ficha y envío de usuarios a la papelera.

Registro: Formulario manual con Combobox dinámico para seleccionar fichas existentes y carga masiva desde Excel/CSV.

Papelera: Sistema de seguridad para restaurar aprendices eliminados o borrarlos definitivamente de la base de datos.

2. conexion.py (Lógica de Datos)
Contiene la clase InventarioDB, encargada de toda la comunicación con el servidor MySQL.

Gestiona el cursor bufferizado para evitar errores de sincronía.

Ejecuta las consultas SQL para insertar asistencias, consultar historiales y realizar limpiezas en las tablas.

3. techsenahsgs.sql (Base de Datos)
Es el esquema de la base de datos TechSenaHSGS. Contiene las tablas necesarias para el funcionamiento:

estudiantes: Almacena datos personales y contraseñas.

asistencias: Registra los tiempos de entrada y salida.

fichas: Almacena la información de los programas de formación.

estudiantes_eliminados: Funciona como la papelera de reciclaje del sistema.

🔒 Seguridad
Cambio de Contraseña Obligatorio: El sistema detecta si un usuario ingresa con la clave por defecto (sena123) y le obliga a actualizarla antes de entrar a su perfil.

Validación de Integridad: Gracias al uso de selectores (Combobox), el registro manual evita errores de llaves foráneas al asegurar que el aprendiz sea vinculado a una ficha real.

📋 Requisitos del Sistema
Python 3.x

Servidor MySQL (XAMPP, WAMP o similar)

Librerías: mysql-connector-python, pandas, tkcalendar, openpyxl.

Desarrollado por Gravis Systems.
Propiedad de High Softwares From Gravis Systems.
