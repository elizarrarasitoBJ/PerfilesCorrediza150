"""
Script para abrir archivos F3D en Fusion 360 y modificar parámetros
Versión corregida - Todas las variables actualizadas
"""

import adsk.core
import adsk.fusion
import traceback
import os


def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface
        
        # Abrir archivo con diálogo
        exito = abrir_con_dialogo(app, ui)
        
        # Si se abrió exitosamente, modificar el parámetro L
        if exito:
            modificar_parametro_L(app, ui)
        
    except:
        if ui:
            ui.messageBox('Error al ejecutar el script:\n{}'.format(traceback.format_exc()))


def abrir_con_dialogo(app, ui):
    """
    Abre un diálogo para que el usuario seleccione el archivo F3D
    """
    try:
        # Crear diálogo de apertura de archivo
        fileDialog = ui.createFileDialog()
        fileDialog.isMultiSelectEnabled = False
        fileDialog.title = "Selecciona un archivo F3D para abrir"
        fileDialog.filter = "Archivos Fusion 360 (*.f3d);;Todos los archivos (*.*)"
        
        # Mostrar diálogo
        dialogResult = fileDialog.showOpen()
        
        if dialogResult == adsk.core.DialogResults.DialogOK:
            filename = fileDialog.filename
            
            # Verificar que el archivo existe
            if not os.path.exists(filename):
                ui.messageBox(f'El archivo no existe:\n{filename}', 'Error')
                return False
            
            # Usar importManager para archivos locales
            importManager = app.importManager
            importOptions = importManager.createFusionArchiveImportOptions(filename)
            documento = importManager.importToNewDocument(importOptions)
            
            if documento:
                ui.messageBox(f'✓ Archivo abierto exitosamente:\n{os.path.basename(filename)}', 
                             'Éxito')
                return True
            else:
                ui.messageBox('No se pudo abrir el archivo', 'Error')
                return False
        else:
            # Usuario canceló
            return False
            
    except Exception as e:
        ui.messageBox(f'Error al abrir archivo:\n{str(e)}', 'Error')
        return False


def modificar_parametro_L(app, ui):
    """
    Solicita al usuario un valor en milímetros y modifica 
    el parámetro de usuario "L" en el diseño activo
    """
    try:
        # Obtener el diseño activo
        design = app.activeProduct
        
        if not design:
            ui.messageBox('No hay ningún diseño activo', 'Error')
            return False
        
        # Verificar que es un Design
        if design.objectType != adsk.fusion.Design.classType():
            ui.messageBox('El documento activo no es un diseño de Fusion 360', 'Error')
            return False
        
        # Obtener los parámetros de usuario
        userParams = design.userParameters
        
        # Buscar el parámetro "L"
        parametro_L = None
        try:
            parametro_L = userParams.itemByName('L')
        except:
            pass
        
        if not parametro_L:
            ui.messageBox('No se encontró el parámetro "L" en el diseño.\n\n' +
                         'Asegúrate de que:\n' +
                         '1. El parámetro existe\n' +
                         '2. Se llama exactamente "L" (mayúscula)\n' +
                         '3. Es un parámetro de usuario',
                         'Error')
            return False
        
        # Obtener el valor actual en cm y convertir a mm
        valor_actual_cm = parametro_L.value
        valor_actual_mm = valor_actual_cm * 10
        
        # Mostrar diálogo de entrada
        resultado = ui.inputBox(
            f'Valor actual de L: {valor_actual_mm:.2f} mm\n\nIngresa el nuevo valor en milímetros:',
            'Modificar Parámetro L',
            str(valor_actual_mm)
        )
        
        # Desempaquetar resultado
        texto_ingresado = resultado[0]
        ok_pressed = resultado[1]
        
        # Verificar si canceló (valor None o vacío)
        if texto_ingresado is None or (not texto_ingresado and not ok_pressed):
            return False
        
        # Verificar que no esté vacío
        if not texto_ingresado or texto_ingresado.strip() == '':
            ui.messageBox('No se ingresó ningún valor.', 'Error')
            return False
        
        # Convertir a número
        try:
            nuevo_valor_mm = float(texto_ingresado.strip())
        except ValueError:
            ui.messageBox(f'"{texto_ingresado}" no es un número válido.\n\nEjemplos: 150, 75.5, 200', 'Error')
            return False
        
        # Validar positivo
        if nuevo_valor_mm <= 0:
            ui.messageBox('El valor debe ser mayor que 0', 'Error')
            return False
        
        # Convertir de mm a cm (unidades internas)
        nuevo_valor_cm = nuevo_valor_mm / 10.0
        
        # Modificar el parámetro
        parametro_L.value = nuevo_valor_cm
        
        # Confirmación
        mensaje = f'''✓ Parámetro actualizado exitosamente:

Parámetro: L
Valor anterior: {valor_actual_mm:.2f} mm
Valor nuevo: {nuevo_valor_mm:.2f} mm

El modelo se ha actualizado automáticamente.'''
        
        ui.messageBox(mensaje, 'Éxito')
        return True
        
    except Exception as e:
        ui.messageBox(f'Error al modificar parámetro:\n{str(e)}\n\n{traceback.format_exc()}', 'Error')
        return False