# Dataset de Terminología Oftalmológica y Optométrica

[![Versión](https://img.shields.io/badge/versión-1.0.0-blue.svg)](https://github.com/tu-usuario/dataset-terminologia-oftalmologia)
[![Licencia](https://img.shields.io/badge/licencia-GPL--3.0-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8%2B-yellow.svg)](https://www.python.org/)

## 📋 Descripción

Dataset completo de terminología médica especializada en oftalmología y optometría, creado como parte del proyecto de **Buscador Avanzado de Términos Optométricos** para la asignatura de Ingeniería de Software para Sistemas Inteligentes (ISSI) en la **ESCOM - Instituto Politécnico Nacional**.

Este dataset proporciona una estructura completa de sinónimos, siglas, acrónimos y sus expansiones en el dominio oftalmológico, diseñado para sistemas de búsqueda, expansión de consultas, y aplicaciones de procesamiento de lenguaje natural (PLN) en el ámbito médico.

## 🎯 Características Principales

- **753 conceptos únicos** organizados jerárquicamente
- **1,655 términos** indexados con detección de ambigüedad
- **197 siglas médicas** con múltiples expansiones
- **208 grupos de sinónimos** validados
- **417 entradas** de terminología optométrica especializada
- Soporte para **expansión automática de consultas**
- **Detección de ambigüedad** para términos polisémicos

## 📁 Estructura del Dataset

```
dataset-terminologia-oftalmologia/
├── README.md                          # Este archivo
├── LICENSE                            # Licencia GPL-3.0
├── lista_sinonimos_id.json           # Tesauro maestro con IDs de concepto
├── indice_invertido.json             # Índice invertido término→conceptos
├── siglas_múltiples.json             # Siglas con distintos significados.
├── siglas_optometría.csv             # Base de datos de siglas no ambiguas
├── sinónimos.yml                     # Grupos de sinónimos
└── ejemplo_busqueda.py               # Script de ejemplo de uso

```

### Descripción de Archivos

#### 1. `lista_sinonimos_id.json` (Archivo Principal)
Tesauro maestro que mapea **Concept IDs** a listas de términos sinónimos. Resultado de la unión de los archivos `siglas_múltiples.json`, `siglas_optometría.csv` y `sinónimos.yml`, que tienen distintos conceptos.

**Estructura:**
```json
{
  "C0001": ["Término1", "Término2", "Sigla1"],
  "C0002": ["OtroTérmino", "Sinónimo", "Acrónimo"]
}
```

**Estadísticas:**
- 753 conceptos únicos
- Promedio de 2.3 términos por concepto
- Máximo 6 términos en un concepto

#### 2. `indice_invertido.json` (Índice de Búsqueda)
Mapeo inverso que permite buscar términos y detectar ambigüedad.

**Estructura:**
```json
{
  "NM": {
    "concept_ids": ["C0108", "C0109"],
    "is_ambiguous": true
  },
  "CIL": {
    "concept_ids": ["C0026"],
    "is_ambiguous": false
  }
}
```

**Estadísticas:**
- 1,655 términos únicos
- 51 términos ambiguos (3.1%)
- 1,604 términos no ambiguos (96.9%)

#### 3. `siglas_múltiples.json`
Diccionario de siglas médicas con sus expansiones completas.

**Características:**
- 197 entradas de siglas
- Manejo de siglas con múltiples significados (ej: "AR" → Autorrefractómetro / Artritis reumatoide)
- Términos en español e inglés

#### 4. `siglas_optometría.csv`
Base de datos tabular de siglas optométricas.

**Formato:**
```csv
Sigla,Expansión
OCT,Tomografía de coherencia óptica
NM,No mejora
```

**Contenido:**
- 417 entradas
- Columnas: `Sigla`, `Expansión`

#### 5. `sinónimos.yml`
Grupos de términos sinónimos validados manualmente.

**Formato:**
```yaml
[Ablefaria, Criptoftalmos]
[Ambliopía, Ojo vago, Ojo perezoso]
```

**Contenido:**
- 208 grupos de sinónimos
- Términos validados clínicamente

## 🚀 Uso Rápido

### Requisitos
```bash
pip install json csv pyyaml
```

### Ejemplo 1: Cargar el Tesauro
```python
import json

# Cargar tesauro de sinónimos
with open('lista_sinonimos_id.json', 'r', encoding='utf-8') as f:
    tesauro = json.load(f)

# Obtener todos los términos de un concepto
concepto = tesauro['C0026']
print(f"Sinónimos de {concepto[0]}: {concepto}")
# Output: Sinónimos de CIL: ['CIL', 'CYL', 'Cilindro or astigmatismo']
```

### Ejemplo 2: Buscar un Término
```python
import json

# Cargar índice invertido
with open('indice_invertido.json', 'r', encoding='utf-8') as f:
    indice = json.load(f)

# Buscar un término
termino = "NM"
info = indice[termino]

if info['is_ambiguous']:
    print(f"⚠️ '{termino}' es ambiguo:")
    print(f"  Aparece en {len(info['concept_ids'])} conceptos diferentes")
else:
    print(f"✓ '{termino}' no es ambiguo")
    print(f"  Concepto: {info['concept_ids'][0]}")
```

### Ejemplo 3: Expansión de Consultas
```python
from ejemplo_busqueda import SynonymExpander

# Inicializar expansor
expander = SynonymExpander(
    synonyms_file='lista_sinonimos_id.json',
    inverted_index_file='indice_invertido.json'
)

# Expandir un término de búsqueda
resultado = expander.expand_term("CIL")

print(f"Término original: {resultado['original']}")
print(f"Términos expandidos: {resultado['expanded_terms']}")
print(f"Consulta booleana: {resultado['query']}")

# Output:
# Término original: CIL
# Términos expandidos: {'CIL', 'CYL', 'Cilindro or astigmatismo'}
# Consulta booleana: (CIL OR CYL OR "Cilindro or astigmatismo")
```

## 🔍 Casos de Uso

### 1. Sistemas de Búsqueda Médica
Expandir automáticamente búsquedas de términos médicos para incluir todas sus variantes:

```python
# Usuario busca: "CIL"
# Sistema expande a: (CIL OR CYL OR Cilindro OR Astigmatismo)
# Resultado: Encuentra todos los documentos relacionados con astigmatismo
```

### 2. Detección de Ambigüedad
Alertar al usuario cuando un término tiene múltiples significados:

```python
# Usuario busca: "NM"
# Sistema detecta: 2 significados diferentes
#   1. No mejora
#   2. Nistagmus manifiesto
# Resultado: Muestra resultados de ambos conceptos o solicita aclaración
```

### 3. Normalización de Términos
Estandarizar variantes de términos médicos:

```python
# Entrada: "AV CC", "CSC", "Agudeza visual Corrección"
# Sistema normaliza a: Concepto C0010
# Resultado: Todos los términos se reconocen como equivalentes
```

### 4. Validación de Datos Clínicos
Verificar que las siglas usadas en registros médicos sean válidas:

```python
# Entrada: "XYZ123"
# Sistema: No encontrado en índice
# Resultado: Advertencia de término no estándar
```

## 📊 Estadísticas del Dataset

| Métrica | Valor |
|---------|-------|
| **Conceptos únicos** | 753 |
| **Términos totales** | 1,655 |
| **Términos ambiguos** | 51 (3.1%) |
| **Términos no ambiguos** | 1,604 (96.9%) |
| **Grupos de sinónimos** | 208 |
| **Siglas procesadas** | 197 |
| **Entradas CSV** | 417 |
| **Términos por concepto (promedio)** | 2.3 |
| **Términos por concepto (máximo)** | 6 |

### Términos Más Ambiguos

| Término | Número de Conceptos | Ejemplo |
|---------|---------------------|---------|
| DP | 3 | Dioptría prismática / Diámetro pupilar / Distancia pupilar |
| OS | 3 | Oculus sinister / Oblicuo superior / Oftalmía simpática |
| FE | 3 | Facoemulsificación / Función del elevador / Fijación excéntrica |
| NM | 2 | No mejora / Nistagmus manifiesto |
| AR | 2 | Autorrefractómetro / Artritis reumatoide |

## 🔧 Metodología de Construcción

### Fuentes de Datos

1. **Oftalmoseo** - Base de datos de siglas oftalmológicas
   - URL: https://www.oftalmoseo.com/siglas-y-acronimos/
   - Contenido: Siglas y acrónimos estándar en oftalmología

2. **UNLP - Diccionario de Términos Oftalmológicos**
   - URL: https://libros.unlp.edu.ar/index.php/unlp/catalog/download/1313/1297/4251-1
   - Contenido: Terminología técnica validada académicamente

### Proceso de Consolidación

1. **Extracción**: Recopilación de términos de fuentes primarias
2. **Normalización**: Estandarización de formato y codificación
3. **Agrupación**: Identificación de sinónimos y variantes
4. **Desambiguación**: Separación de términos polisémicos
5. **Validación**: Verificación de coherencia clínica
6. **Indexación**: Generación de índice invertido

### Reglas de Agrupación

- **Expansiones idénticas** → Mismo concepto (ej: "AD" y "ADD" ambos son "Adición")
- **Expansiones diferentes** → Conceptos separados (ej: "AM" = "Agujero macular" vs "Astigmatismo mixto")
- **Jerarquía de fuentes**: siglas_médicas.json establece separaciones canónicas, otros archivos se fusionan respetando esta jerarquía

## 📝 Formato de Datos

### Concept ID
Los IDs de concepto siguen el formato `C####` donde `####` es un número secuencial de 4 dígitos con ceros a la izquierda.

**Ejemplos:**
- `C0001`: Primer concepto
- `C0026`: Concepto 26 (CIL/CYL/Astigmatismo)
- `C0753`: Último concepto

### Codificación
- **Archivos JSON**: UTF-8 sin BOM
- **Archivo CSV**: UTF-8 con encabezados
- **Archivo YML**: UTF-8 con sintaxis de lista Python

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Para contribuir:

1. Fork el repositorio
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -m 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

### Lineamientos para Contribuciones

- **Fuentes**: Proporcionar referencias de fuentes confiables
- **Documentación**: Actualizar el README con cambios significativos

## 📜 Licencia

Este proyecto está licenciado bajo la **GNU General Public License v3.0 (GPL-3.0)**.

Esto significa que puedes:
- ✓ Usar el dataset comercialmente
- ✓ Modificar el dataset
- ✓ Distribuir el dataset
- ✓ Usar el dataset de forma privada

**Condiciones:**
- Debes incluir la licencia y el copyright
- Debes indicar los cambios realizados
- Debes liberar el código fuente de trabajos derivados
- Debes usar la misma licencia GPL-3.0

Ver [LICENSE](LICENSE) para más detalles.

## 👤 Autor

**Takeishi Takeda**
- Proyecto académico: Buscador Avanzado de Términos Optométricos
- Institución: ESCOM - Instituto Politécnico Nacional
- Asignatura: Ingeniería de Software para Sistemas Inteligentes (ISSI)
- Año: 2025

## 📚 Referencias

1. Oftalmoseo. (2024). *Siglas y Acrónimos en Oftalmología*. Recuperado de https://www.oftalmoseo.com/siglas-y-acronimos/

2. UNLP Editorial. *Diccionario de Términos Oftalmológicos*. Universidad Nacional de La Plata. Recuperado de https://libros.unlp.edu.ar/index.php/unlp/catalog/download/1313/1297/4251-1

## 📧 Contacto

Para preguntas, sugerencias o reportar errores, por favor abre un [issue](https://github.com/tu-usuario/dataset-terminologia-oftalmologia/issues) en el repositorio.

---

<div align="center">

**⭐ Si este dataset te fue útil, considera darle una estrella en GitHub ⭐**

Hecho con ❤️ para la comunidad médica y de desarrollo de software

</div>
