"""
Script para convertir siglas_multiples.txt a siglas_medicas.json correctamente.
Mantiene las siglas con múltiples significados como entradas SEPARADAS.
"""

import json
import sys
from pathlib import Path
from collections import defaultdict

# Configurar codificación UTF-8 para la salida de consola
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

def parse_siglas_multiples(filepath: Path) -> dict:
    """
    Lee siglas_multiples.txt y genera un diccionario donde:
    - Si las EXPANSIONES son iguales → se agrupan como sinónimos (mismo concepto)
    - Si las EXPANSIONES son diferentes → conceptos separados (aunque la sigla sea igual)
    
    Lógica:
    - AD: Adición y ADD: Adición → JUNTOS (misma expansión)
    - AM: Agujero macular y AM: Astigmatismo mixto → SEPARADOS (expansiones diferentes)
    """
    
    # Agrupar por expansión (clave = expansiones, valor = lista de siglas)
    expansion_groups = defaultdict(set)
    
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            
            # Ignorar líneas vacías
            if not line:
                continue
            
            # Separar sigla de expansiones por ':'
            if ':' not in line:
                continue
                
            parts = line.split(':', 1)
            sigla = parts[0].strip()
            expansiones_str = parts[1].strip()
            
            # Separar las expansiones por coma
            expansiones = [exp.strip() for exp in expansiones_str.split(',')]
            
            # Crear una clave única basada en las expansiones (ordenadas)
            expansion_key = tuple(sorted(expansiones))
            
            # Agregar la sigla a este grupo de expansiones
            expansion_groups[expansion_key].add(sigla)
    
    # Convertir a formato final: cada grupo único de expansiones se convierte en un concepto
    siglas_dict = {}
    concept_counter = defaultdict(int)
    
    for expansiones_tuple, siglas_set in expansion_groups.items():
        expansiones_list = list(expansiones_tuple)
        siglas_list = sorted(siglas_set)  # Ordenar siglas alfabéticamente
        
        # Combinar siglas + expansiones
        terminos = siglas_list + expansiones_list
        
        # Generar clave única
        # Si solo hay una sigla, usar esa sigla como clave
        # Si hay múltiples siglas, usar la primera con sufijo si es necesario
        primary_sigla = siglas_list[0]
        
        # Verificar si esta sigla ya se usó
        if primary_sigla in siglas_dict:
            # Agregar sufijo
            concept_counter[primary_sigla] += 1
            key = f"{primary_sigla}-{concept_counter[primary_sigla]}"
        else:
            key = primary_sigla
            concept_counter[primary_sigla] = 1
        
        siglas_dict[key] = terminos
    
    return siglas_dict


def main():
    # Rutas de archivos
    base_dir = Path(__file__).parent
    input_file = base_dir / "siglas_multiples.txt"
    output_file = base_dir / "siglas_medicas.json"
    
    print(f"Leyendo {input_file.name}...")
    siglas_dict = parse_siglas_multiples(input_file)
    
    print(f"\nGenerando {output_file.name}...")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(siglas_dict, f, ensure_ascii=False, indent=2)
    
    # Estadísticas
    total_entries = len(siglas_dict)
    duplicated = sum(1 for key in siglas_dict.keys() if '-' in key)
    unique = total_entries - duplicated
    
    print(f"\n✓ Archivo generado exitosamente")
    print(f"\n--- ESTADÍSTICAS ---")
    print(f"Total de entradas: {total_entries}")
    print(f"Siglas únicas: {unique}")
    print(f"Siglas con múltiples significados: {duplicated}")
    
    # Mostrar algunas siglas duplicadas como ejemplo
    print(f"\nEjemplos de siglas separadas:")
    for key in list(siglas_dict.keys())[:10]:
        if '-' in key:
            print(f"  {key}: {siglas_dict[key][0]} → {', '.join(siglas_dict[key][1:])}")


if __name__ == "__main__":
    main()
