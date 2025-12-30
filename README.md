[README.md](https://github.com/user-attachments/files/24387573/README.md)
# Script Fusion 360: Abrir F3D y Modificar Parámetro L

## Índice

1. [Descripción](#descripción)
2. [Requisitos](#requisitos)
3. [Instalación](#instalación)
4. [Preparación del Modelo](#preparación-del-modelo)
5. [Uso](#uso)
6. [Arquitectura del Código](#arquitectura-del-código)
7. [Funciones Principales](#funciones-principales)
8. [Flujo de Ejecución](#flujo-de-ejecución)
9. [Sistema de Unidades](#sistema-de-unidades)
10. [Solución de Problemas](#solución-de-problemas)
11. [Personalización](#personalización)
12. [Autor](#autor)

---

## Descripción

Script de Python para Autodesk Fusion 360 que automatiza dos tareas:

1. **Abrir archivos F3D locales** mediante un diálogo de selección
2. **Modificar el parámetro de usuario "L"** solicitando un valor en milímetros al usuario

### Ventajas

- Automatiza la apertura de archivos para workflows repetitivos
- Modifica parámetros sin navegar manualmente por el panel
- Conversión automática de unidades (mm ↔ cm)
- Validación robusta de entrada de usuario
- Mensajes de error claros y descriptivos

### Casos de Uso

- Diseños paramétricos que requieren ajustes frecuentes de longitud
- Producción de variantes de un mismo modelo
- Integración en workflows automatizados
- Pruebas rápidas de diferentes dimensiones

---

## Requisitos

### Software

- **Autodesk Fusion 360** (versión 2020 o superior)
- **Python 3.x** (incluido con Fusion 360)

### Modelo F3D

El archivo debe contener:
- Un parámetro de usuario llamado exactamente **"L"** (mayúscula)
- El parámetro debe controlar alguna dimensión del modelo (típicamente longitud)

---

## Instalación

### Paso 1: Ubicar la carpeta de scripts

**Windows:**
```
C:\Users\[TuUsuario]\AppData\Roaming\Autodesk\Autodesk Fusion 360\API\Scripts\
```

**Mac:**
```
~/Library/Application Support/Autodesk/Autodesk Fusion 360/API/Scripts/
```

### Paso 2: Crear carpeta para el script

```
Scripts/
  └── AbrirYModificarF3D/
      └── AbrirYModificarF3D.py
```

### Paso 3: Copiar el código

Guarda el script completo en `AbrirYModificarF3D.py`

### Paso 4: Verificar en Fusion 360

1. Abrir Fusion 360
2. `Utilities → Add-Ins → Scripts and Add-Ins`
3. Pestaña: **My Scripts**
4. Debería aparecer: **AbrirYModificarF3D**

---

## Preparación del Modelo

### Crear el Parámetro "L"

Si tu modelo no tiene el parámetro:

1. En Fusion 360: `Modify → Change Parameters`
2. Click en el botón **"+"** (Add User Parameter)
3. Configurar:
   - **Name:** `L`
   - **Unit:** `mm`
   - **Expression:** `100` (o tu valor deseado)
   - **Comment:** (opcional) "Longitud de extrusión"
4. Click **OK**

### Vincular el Parámetro a la Geometría

Para usar el parámetro en una extrusión:

1. Editar la extrusión
2. En el campo **Distance**, escribir: `L`
3. La extrusión ahora usa el parámetro
4. Al cambiar "L", la extrusión se actualiza automáticamente

---

## Uso

### Ejecución del Script

#### Desde Fusion 360

1. **Abrir el panel de scripts**
   ```
   Utilities → Scripts and Add-Ins
   ```

2. **Seleccionar el script**
   - Pestaña: **My Scripts**
   - Seleccionar: **AbrirYModificarF3D**
   - Click: **Run**

3. **Seleccionar archivo F3D**
   - Aparece diálogo de selección de archivo
   - Navegar hasta tu archivo `.f3d`
   - Click: **Abrir**

4. **Confirmar apertura**
   - Mensaje: "Archivo abierto exitosamente"
   - Click: **Aceptar**

5. **Ingresar nuevo valor para L**
   - Aparece: "Valor actual de L: XX.XX mm"
   - Escribir el nuevo valor en milímetros
   - Ejemplo: `150`
   - Click: **OK**

6. **Verificar resultado**
   - Mensaje: "Parámetro actualizado exitosamente"
   - El modelo se regenera automáticamente con la nueva dimensión

### Ejemplo Completo

```
ESCENARIO: Abrir y modificar una barra metálica

1. Ejecutar script
2. Seleccionar: "barra_100mm.f3d"
3. Mensaje: "✓ Archivo abierto exitosamente"
4. Diálogo: "Valor actual de L: 100.00 mm"
5. Ingresar: 250
6. Resultado: La barra se extiende de 100mm a 250mm
7. Confirmación: "Valor anterior: 100.00 mm → Valor nuevo: 250.00 mm"
```

---

## Arquitectura del Código

### Estructura del Script

```python
# IMPORTACIONES
import adsk.core       # API principal de Fusion 360
import adsk.fusion     # API específica de diseño
import traceback       # Manejo detallado de errores
import os             # Operaciones de sistema de archivos

# FUNCIONES
run(context)                      # Punto de entrada
abrir_con_dialogo(app, ui)        # Abrir archivo F3D
modificar_parametro_L(app, ui)    # Modificar parámetro
```

### Diagrama de Flujo

```
START
  ↓
run(context)
  ↓
Inicializar app y ui
  ↓
abrir_con_dialogo()
  ↓
¿Archivo abierto? ─NO→ END
  ↓ SI
modificar_parametro_L()
  ↓
Buscar parámetro "L"
  ↓
¿Existe "L"? ─NO→ Error → END
  ↓ SI
Solicitar nuevo valor
  ↓
Validar entrada
  ↓
¿Válido? ─NO→ Error → END
  ↓ SI
Actualizar parámetro
  ↓
Confirmar éxito
  ↓
END
```

---

## Funciones Principales

### Función: `run(context)`

**Propósito:** Punto de entrada del script

**Parámetros:**
- `context`: Contexto de ejecución proporcionado por Fusion 360

**Retorno:** Ninguno

**Descripción:**
```python
def run(context):
    # 1. Inicializar variable de interfaz
    ui = None
    
    try:
        # 2. Obtener aplicación y UI de Fusion
        app = adsk.core.Application.get()
        ui = app.userInterface
        
        # 3. Abrir archivo con diálogo
        exito = abrir_con_dialogo(app, ui)
        
        # 4. Si se abrió exitosamente, modificar parámetro
        if exito:
            modificar_parametro_L(app, ui)
    
    except:
        # 5. Capturar y mostrar cualquier error
        if ui:
            ui.messageBox('Error: ' + traceback.format_exc())
```

**Flujo:**
1. Inicializa la interfaz de usuario
2. Llama a `abrir_con_dialogo()` para abrir el archivo
3. Si el archivo se abre correctamente (retorna `True`), llama a `modificar_parametro_L()`
4. Captura cualquier excepción y muestra el error detallado

---

### Función: `abrir_con_dialogo(app, ui)`

**Propósito:** Abre un archivo F3D mediante diálogo de selección

**Parámetros:**
- `app`: Objeto `Application` de Fusion 360
- `ui`: Objeto `UserInterface` para mostrar diálogos

**Retorno:**
- `True`: Archivo abierto exitosamente
- `False`: Error o usuario canceló

**Descripción Detallada:**

```python
def abrir_con_dialogo(app, ui):
    try:
        # PASO 1: Crear y configurar diálogo de archivo
        fileDialog = ui.createFileDialog()
        fileDialog.isMultiSelectEnabled = False  # Solo un archivo
        fileDialog.title = "Selecciona un archivo F3D para abrir"
        fileDialog.filter = "Archivos Fusion 360 (*.f3d);;Todos los archivos (*.*)"
        
        # PASO 2: Mostrar diálogo y capturar resultado
        dialogResult = fileDialog.showOpen()
        
        # PASO 3: Verificar si usuario presionó OK
        if dialogResult == adsk.core.DialogResults.DialogOK:
            filename = fileDialog.filename
            
            # PASO 4: Validar existencia del archivo
            if not os.path.exists(filename):
                ui.messageBox('El archivo no existe')
                return False
            
            # PASO 5: Abrir archivo usando ImportManager
            # IMPORTANTE: No usar Documents.open() con archivos locales
            importManager = app.importManager
            importOptions = importManager.createFusionArchiveImportOptions(filename)
            documento = importManager.importToNewDocument(importOptions)
            
            # PASO 6: Verificar éxito y confirmar
            if documento:
                ui.messageBox('✓ Archivo abierto exitosamente')
                return True
            else:
                ui.messageBox('No se pudo abrir el archivo')
                return False
        else:
            # Usuario canceló
            return False
    
    except Exception as e:
        ui.messageBox('Error al abrir archivo: ' + str(e))
        return False
```

**Nota Técnica Importante:**

El script usa `ImportManager` en lugar de `Documents.open()` porque:

- `Documents.open()` solo acepta objetos `DataFile` (archivos en la nube)
- `ImportManager` es necesario para archivos locales `.f3d`
- Esta es una peculiaridad de la API de Fusion 360

```python
# INCORRECTO - No funciona con archivos locales
app.documents.open(filename)  # Error!

# CORRECTO - Para archivos .f3d locales
importManager = app.importManager
importOptions = importManager.createFusionArchiveImportOptions(filename)
documento = importManager.importToNewDocument(importOptions)
```

---

### Función: `modificar_parametro_L(app, ui)`

**Propósito:** Modifica el parámetro de usuario "L" con un valor ingresado por el usuario

**Parámetros:**
- `app`: Objeto `Application` de Fusion 360
- `ui`: Objeto `UserInterface`

**Retorno:**
- `True`: Parámetro modificado exitosamente
- `False`: Error o usuario canceló

**Descripción Detallada:**

```python
def modificar_parametro_L(app, ui):
    try:
        # PASO 1: Obtener diseño activo
        design = app.activeProduct
        
        if not design:
            ui.messageBox('No hay ningún diseño activo')
            return False
        
        # Validar que es un Design (no Drawing o CAM)
        if design.objectType != adsk.fusion.Design.classType():
            ui.messageBox('El documento no es un diseño de Fusion')
            return False
        
        # PASO 2: Buscar parámetro "L"
        userParams = design.userParameters
        
        parametro_L = None
        try:
            parametro_L = userParams.itemByName('L')
        except:
            pass  # Si no existe, queda None
        
        if not parametro_L:
            ui.messageBox('No se encontró el parámetro "L"')
            return False
        
        # PASO 3: Obtener valor actual
        # Fusion usa centímetros internamente
        valor_actual_cm = parametro_L.value
        valor_actual_mm = valor_actual_cm * 10  # Convertir a mm
        
        # PASO 4: Solicitar nuevo valor al usuario
        resultado = ui.inputBox(
            f'Valor actual de L: {valor_actual_mm:.2f} mm\n\nIngresa el nuevo valor en milímetros:',
            'Modificar Parámetro L',
            str(valor_actual_mm)  # Valor por defecto
        )
        
        # PASO 5: Procesar entrada
        texto_ingresado = resultado[0]  # Texto del input
        ok_pressed = resultado[1]       # Boolean (OK o Cancel)
        
        # Verificar cancelación
        if texto_ingresado is None or (not texto_ingresado and not ok_pressed):
            return False
        
        # Verificar que no esté vacío
        if not texto_ingresado or texto_ingresado.strip() == '':
            ui.messageBox('No se ingresó ningún valor.')
            return False
        
        # PASO 6: Convertir y validar
        try:
            nuevo_valor_mm = float(texto_ingresado.strip())
        except ValueError:
            ui.messageBox(f'"{texto_ingresado}" no es un número válido.')
            return False
        
        if nuevo_valor_mm <= 0:
            ui.messageBox('El valor debe ser mayor que 0')
            return False
        
        # PASO 7: Convertir unidades y actualizar
        nuevo_valor_cm = nuevo_valor_mm / 10.0  # mm → cm
        parametro_L.value = nuevo_valor_cm
        
        # Fusion regenera el modelo automáticamente
        
        # PASO 8: Confirmar éxito
        mensaje = f'''✓ Parámetro actualizado exitosamente:

Parámetro: L
Valor anterior: {valor_actual_mm:.2f} mm
Valor nuevo: {nuevo_valor_mm:.2f} mm

El modelo se ha actualizado automáticamente.'''
        
        ui.messageBox(mensaje, 'Éxito')
        return True
    
    except Exception as e:
        ui.messageBox('Error: ' + str(e) + '\n\n' + traceback.format_exc())
        return False
```

**Validaciones Implementadas:**

1. Diseño activo existe
2. Es un documento de tipo Design
3. Parámetro "L" existe
4. Usuario no canceló
5. Valor no está vacío
6. Valor es numérico
7. Valor es positivo

---

## Flujo de Ejecución

### Secuencia Completa

```
1. INICIO
   └─> run(context)
   
2. INICIALIZACIÓN
   ├─> Obtener Application
   └─> Obtener UserInterface
   
3. ABRIR ARCHIVO
   ├─> Crear FileDialog
   ├─> Mostrar diálogo
   ├─> Usuario selecciona archivo
   ├─> Validar existencia
   ├─> Crear ImportManager
   ├─> Crear opciones de importación
   ├─> Importar a nuevo documento
   └─> Confirmar éxito
   
4. MODIFICAR PARÁMETRO (si archivo abierto)
   ├─> Obtener diseño activo
   ├─> Validar tipo de documento
   ├─> Buscar parámetro "L"
   ├─> Obtener valor actual (cm)
   ├─> Convertir a mm
   ├─> Mostrar inputBox
   ├─> Capturar entrada usuario
   ├─> Validar entrada
   │   ├─> No cancelado
   │   ├─> No vacío
   │   ├─> Es número
   │   └─> Es positivo
   ├─> Convertir mm a cm
   ├─> Actualizar parámetro
   ├─> Fusion regenera modelo
   └─> Mostrar confirmación
   
5. FIN
```

### Tiempos Estimados

| Paso | Tiempo |
|------|--------|
| Seleccionar archivo | 5-10 segundos |
| Abrir archivo | 2-15 segundos (según tamaño) |
| Ingresar valor | 2-5 segundos |
| Regenerar modelo | 1-5 segundos (según complejidad) |
| **TOTAL** | **10-35 segundos** |

---

## Sistema de Unidades

### Conversión Automática

El script maneja la conversión entre milímetros (usuario) y centímetros (Fusion):

```python
# De CM (Fusion) a MM (Usuario)
valor_mm = valor_cm * 10

# De MM (Usuario) a CM (Fusion)
valor_cm = valor_mm / 10.0
```

### Unidades Internas de Fusion 360

Fusion 360 usa **centímetros** como unidad base interna:

| Unidad | Factor de Conversión |
|--------|---------------------|
| Milímetros (mm) | `× 10` |
| Centímetros (cm) | `× 1` (base) |
| Metros (m) | `÷ 100` |
| Pulgadas (in) | `× 2.54` |
| Pies (ft) | `× 30.48` |

### Ejemplo de Conversión

```python
# Usuario ingresa: 150 mm
nuevo_valor_mm = 150

# Script convierte a cm para Fusion
nuevo_valor_cm = 150 / 10.0  # = 15.0 cm

# Actualiza parámetro
parametro_L.value = 15.0  # Fusion recibe 15.0 cm
```

---

## Solución de Problemas

### Error: "No se encontró el parámetro L"

**Causa:** El parámetro no existe o tiene un nombre diferente

**Solución:**
1. Verificar en `Modify → Change Parameters`
2. El nombre debe ser exactamente **"L"** (mayúscula)
3. Debe ser un parámetro de **usuario**, no de modelo

**Alternativa:** Modificar el código para buscar otro nombre:
```python
# Línea donde se busca el parámetro
parametro_L = userParams.itemByName('TuNombreParametro')
```

---

### Error: "No hay ningún diseño activo"

**Causa:** No hay documento abierto o el documento no es de tipo Design

**Solución:**
1. Asegurarse de que el archivo F3D se abrió correctamente
2. No debe ser un Drawing o documento CAM
3. Verificar que la pestaña de Design está activa

---

### Error: "El archivo no existe"

**Causa:** La ruta del archivo es incorrecta o el archivo fue movido

**Solución:**
1. Verificar que el archivo existe en la ubicación seleccionada
2. Verificar permisos de lectura
3. No usar caracteres especiales en la ruta

---

### Problema: Valor no es un número válido

**Causa:** Usuario ingresó texto no numérico

**Solución:** Ingresar solo números válidos:

**Válidos:**
- `150`
- `75.5`
- `200`
- `0.5`

**Inválidos:**
- `150mm` (no incluir unidades)
- `cien` (no texto)
- `150,5` (usar punto decimal, no coma)
- `-50` (no negativos)

---

### Problema: El modelo no se actualiza visualmente

**Causa:** Fusion no refrescó el viewport

**Solución:** Agregar después de actualizar el parámetro:
```python
parametro_L.value = nuevo_valor_cm
app.activeViewport.refresh()  # Forzar refresco
```

---

### Error: "Wrong number or type of arguments"

**Causa:** Uso incorrecto de `Documents.open()` con archivos locales

**Solución:** Ya está resuelto en el código usando `ImportManager`

Este error ocurría en versiones anteriores porque `Documents.open()` solo acepta objetos `DataFile`, no rutas de string.

---

## Personalización

### Modificar Otro Parámetro

Para usar un parámetro diferente a "L":

```python
# En la función modificar_parametro_L, cambiar:

# Línea donde se busca el parámetro
parametro_ANCHO = userParams.itemByName('ANCHO')

# Actualizar también los mensajes
resultado = ui.inputBox(
    f'Valor actual de ANCHO: {valor_actual_mm:.2f} mm...',
    'Modificar Parámetro ANCHO',
    str(valor_actual_mm)
)
```

---

### Modificar Múltiples Parámetros

Para modificar varios parámetros en secuencia:

```python
def modificar_multiples_parametros(app, ui):
    design = app.activeProduct
    userParams = design.userParameters
    
    # Parámetro 1: Longitud
    param_L = userParams.itemByName('L')
    resultado_L = ui.inputBox(
        f'Longitud actual: {param_L.value * 10:.2f} mm',
        'Longitud',
        str(param_L.value * 10)
    )
    if resultado_L[0]:
        param_L.value = float(resultado_L[0]) / 10
    
    # Parámetro 2: Ancho
    param_A = userParams.itemByName('ANCHO')
    resultado_A = ui.inputBox(
        f'Ancho actual: {param_A.value * 10:.2f} mm',
        'Ancho',
        str(param_A.value * 10)
    )
    if resultado_A[0]:
        param_A.value = float(resultado_A[0]) / 10
    
    ui.messageBox('Parámetros actualizados')
```

Luego en `run()`:
```python
if exito:
    modificar_multiples_parametros(app, ui)
```

---

### Abrir Archivo con Ruta Fija

Para abrir siempre el mismo archivo sin diálogo:

```python
def run(context):
    app = adsk.core.Application.get()
    ui = app.userInterface
    
    # Ruta fija al archivo
    ruta_fija = "C:/Proyectos/mi_modelo.f3d"
    
    # Abrir sin diálogo
    try:
        importManager = app.importManager
        importOptions = importManager.createFusionArchiveImportOptions(ruta_fija)
        documento = importManager.importToNewDocument(importOptions)
        
        if documento:
            ui.messageBox('Archivo abierto')
            modificar_parametro_L(app, ui)
        else:
            ui.messageBox('Error al abrir archivo')
    except Exception as e:
        ui.messageBox(f'Error: {str(e)}')
```

---

### Agregar Validación de Rango

Para limitar los valores dentro de un rango:

```python
# Después de convertir a número y antes de actualizar
VALOR_MIN = 10   # mm
VALOR_MAX = 1000 # mm

if nuevo_valor_mm < VALOR_MIN:
    ui.messageBox(f'El valor debe ser mayor o igual a {VALOR_MIN} mm')
    return False

if nuevo_valor_mm > VALOR_MAX:
    ui.messageBox(f'El valor debe ser menor o igual a {VALOR_MAX} mm')
    return False
```

---

### Agregar Logging

Para registrar las modificaciones:

```python
import datetime

def modificar_parametro_L(app, ui):
    # ... código existente ...
    
    # Después de actualizar el parámetro
    parametro_L.value = nuevo_valor_cm
    
    # Registrar cambio
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_file = "C:/Fusion_Logs/modificaciones.txt"
    
    with open(log_file, 'a') as f:
        f.write(f"{timestamp} - L modificado: {valor_actual_mm:.2f} → {nuevo_valor_mm:.2f} mm\n")
    
    # ... resto del código ...
```

---

## Autor

**Autor:** JEB  
**Fecha:** Diciembre 2024  
**Versión:** 1.0  
