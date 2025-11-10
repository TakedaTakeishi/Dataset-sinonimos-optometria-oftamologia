# Guía de Publicación en GitHub

## Archivos a incluir en el repositorio:

✅ **Archivos de Datos:**
1. `lista_sinónimos_id.json` (57 KB) - Tesauro maestro
2. `indice_invertido.json` (172 KB) - Índice de búsqueda
3. `siglas_múltiples.json` (17 KB) - Siglas procesadas
4. `siglas_optometría.csv` (14 KB) - Base de datos CSV
5. `sinónimos.yml` (8 KB) - Grupos de sinónimos

✅ **Código de Ejemplo:**
6. `ejemplo_busqueda.py` (7 KB) - Script de demostración

✅ **Documentación:**
7. `README.md` (11 KB) - Documentación principal
8. `LICENSE` (1 KB) - Licencia GPL-3.0
9. `.gitignore` - Archivos a ignorar

## Comandos Git para publicar:

### 1. Inicializar repositorio (si no está inicializado)
```bash
cd "c:\Users\Joni\Documents\Universidad\6to_Semestre\2. ISSI (Ingeniería de Software para Sistemas Inteligentes)\Buscador\Extractor de sinónimos"
git init
```

### 2. Añadir archivos al staging
```bash
git add lista_sinónimos_id.json
git add indice_invertido.json
git add siglas_múltiples.json
git add siglas_optometría.csv
git add sinónimos.yml
git add ejemplo_busqueda.py
git add README.md
git add LICENSE
git add .gitignore
```

### 3. Hacer commit
```bash
git commit -m "Initial release v1.0.0 - Dataset de Terminología Oftalmológica"
```

### 4. Crear repositorio en GitHub
1. Ve a https://github.com/new
2. Nombre del repositorio: `dataset-terminologia-oftalmologia`
3. Descripción: "Dataset completo de terminología médica en oftalmología y optometría con 753 conceptos y 1,655 términos indexados"
4. Público/Privado: Tu elección
5. NO inicialices con README, .gitignore o licencia (ya los tenemos)
6. Crea el repositorio

### 5. Conectar con el repositorio remoto
```bash
git remote add origin https://github.com/TU-USUARIO/dataset-terminologia-oftalmologia.git
git branch -M main
```

### 6. Subir a GitHub
```bash
git push -u origin main
```

### 7. Crear tag de versión v1.0.0
```bash
git tag -a v1.0.0 -m "Release v1.0.0 - Dataset inicial con 753 conceptos"
git push origin v1.0.0
```

## Después de publicar:

### Crear un Release en GitHub
1. Ve a tu repositorio en GitHub
2. Click en "Releases" → "Create a new release"
3. Tag: `v1.0.0`
4. Título: "v1.0.0 - Dataset Inicial"
5. Descripción:
```markdown
## Dataset de Terminología Oftalmológica y Optométrica v1.0.0

Primer release oficial del dataset.

### Contenido
- 753 conceptos únicos
- 1,655 términos indexados
- 51 términos ambiguos detectados
- 197 siglas médicas procesadas
- 208 grupos de sinónimos validados

### Archivos incluidos
- `lista_sinónimos_id.json` - Tesauro maestro
- `indice_invertido.json` - Índice de búsqueda
- `siglas_múltiples.json` - Siglas procesadas
- `siglas_optometría.csv` - Base CSV
- `sinónimos.yml` - Grupos de sinónimos
- `ejemplo_busqueda.py` - Código de ejemplo

### Fuentes
- Oftalmoseo: https://www.oftalmoseo.com/siglas-y-acronimos/
- UNLP: https://libros.unlp.edu.ar/index.php/unlp/catalog/download/1313/1297/4251-1
```

### Añadir temas (topics) al repositorio
En GitHub, ve a tu repositorio y añade estos topics:
- `dataset`
- `medical-terminology`
- `ophthalmology`
- `optometry`
- `spanish`
- `nlp`
- `information-retrieval`
- `medical-informatics`
- `python`

### Opcional: Añadir README al perfil
Si quieres destacar este proyecto en tu perfil de GitHub, menciona:
```markdown
📊 **Dataset de Terminología Oftalmológica** - 753 conceptos médicos con detección de ambigüedad
```

## Verificación final

Antes de hacer push, verifica:
- [ ] README.md está completo y formateado correctamente
- [ ] LICENSE existe con GPL-3.0
- [ ] .gitignore excluye archivos innecesarios
- [ ] Todos los archivos JSON están en UTF-8
- [ ] ejemplo_busqueda.py funciona correctamente
- [ ] No hay datos sensibles o personales en los archivos

## Comandos útiles

### Ver estado
```bash
git status
```

### Ver archivos que serán commiteados
```bash
git diff --staged --name-only
```

### Ver tamaño del repositorio
```bash
git count-objects -vH
```

### Deshacer último commit (si cometiste un error)
```bash
git reset --soft HEAD~1
```

---

¡Listo para publicar! 🚀
