"""
Script para generar el índice invertido desde lista_sinónimos.json.

El índice invertido mapea cada término a sus Concept IDs, permitiendo:
1. Detectar términos ambiguos (aparecen en múltiples conceptos)
2. Expandir búsquedas con todos los sinónimos del concepto
3. Manejar casos ambiguos expandiendo a múltiples conceptos

Formato de salida (indice_invertido.json):
{
  "término": {
    "concept_ids": ["C0001", "C0002"],  // Lista de conceptos donde aparece
    "is_ambiguous": true                 // true si aparece en >1 concepto
  }
}
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Set
from collections import defaultdict

# Configurar codificación UTF-8 para la salida de consola
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')


def load_synonyms(filepath: Path) -> Dict[str, List[str]]:
    """Carga el tesauro de sinónimos."""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


def build_inverted_index(synonyms: Dict[str, List[str]]) -> Dict[str, Dict]:
    """
    Construye el índice invertido desde el tesauro de sinónimos.
    
    Args:
        synonyms: Diccionario {concept_id: [términos]}
    
    Returns:
        Diccionario {término: {"concept_ids": [...], "is_ambiguous": bool}}
    """
    # Mapeo temporal: término -> set de concept_ids
    term_to_concepts: Dict[str, Set[str]] = defaultdict(set)
    
    # Construir el mapeo
    for concept_id, terms in synonyms.items():
        for term in terms:
            term_normalized = term.strip()
            if term_normalized:
                term_to_concepts[term_normalized].add(concept_id)
    
    # Convertir a formato final con flag de ambigüedad
    inverted_index: Dict[str, Dict] = {}
    
    for term, concept_ids in sorted(term_to_concepts.items()):
        concept_list = sorted(list(concept_ids))
        inverted_index[term] = {
            "concept_ids": concept_list,
            "is_ambiguous": len(concept_list) > 1
        }
    
    return inverted_index


def generate_statistics(inverted_index: Dict[str, Dict]) -> Dict:
    """Genera estadísticas del índice invertido."""
    total_terms = len(inverted_index)
    ambiguous_terms = sum(1 for data in inverted_index.values() if data["is_ambiguous"])
    unambiguous_terms = total_terms - ambiguous_terms
    
    # Encontrar el término con más conceptos
    max_concepts = 0
    most_ambiguous_term = None
    for term, data in inverted_index.items():
        num_concepts = len(data["concept_ids"])
        if num_concepts > max_concepts:
            max_concepts = num_concepts
            most_ambiguous_term = term
    
    return {
        "total_terms": total_terms,
        "unambiguous_terms": unambiguous_terms,
        "ambiguous_terms": ambiguous_terms,
        "most_ambiguous_term": most_ambiguous_term,
        "max_concepts_per_term": max_concepts
    }


def print_examples(inverted_index: Dict[str, Dict], synonyms: Dict[str, List[str]]) -> None:
    """Imprime ejemplos de uso del índice invertido."""
    print("\n" + "="*60)
    print("EJEMPLOS DE USO DEL ÍNDICE INVERTIDO")
    print("="*60)
    
    # Ejemplo 1: Término no ambiguo
    example_terms = ["CIL", "Astigmatismo", "NM", "NO", "AR", "AM"]
    
    for term in example_terms:
        if term not in inverted_index:
            continue
            
        data = inverted_index[term]
        concept_ids = data["concept_ids"]
        is_ambiguous = data["is_ambiguous"]
        
        print(f"\n📍 Búsqueda: '{term}'")
        print(f"   Concept IDs: {concept_ids}")
        print(f"   ¿Ambiguo?: {'✓ SÍ' if is_ambiguous else '✗ NO'}")
        
        if is_ambiguous:
            print(f"   ⚠️  CASO AMBIGUO - Expandir a múltiples conceptos:")
            for cid in concept_ids:
                terms_in_concept = synonyms.get(cid, [])
                print(f"      • {cid}: {', '.join(terms_in_concept[:3])}{'...' if len(terms_in_concept) > 3 else ''}")
        else:
            cid = concept_ids[0]
            all_synonyms = synonyms.get(cid, [])
            print(f"   ✓ Expandir a: {' OR '.join(f'"{t}"' for t in all_synonyms)}")
        
        print(f"   {'-'*56}")


def main():
    # Rutas de archivos
    base_dir = Path(__file__).parent
    input_file = base_dir / "lista_sinónimos.json"
    output_file = base_dir / "indice_invertido.json"
    
    print("Cargando tesauro de sinónimos...")
    synonyms = load_synonyms(input_file)
    
    print(f"Construyendo índice invertido...")
    inverted_index = build_inverted_index(synonyms)
    
    print(f"Guardando en {output_file.name}...")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(inverted_index, f, ensure_ascii=False, indent=2)
    
    # Generar estadísticas
    stats = generate_statistics(inverted_index)
    
    print(f"\n✓ Archivo {output_file.name} generado exitosamente")
    
    print("\n" + "="*60)
    print("ESTADÍSTICAS DEL ÍNDICE INVERTIDO")
    print("="*60)
    print(f"Total de términos únicos: {stats['total_terms']}")
    print(f"  • Términos no ambiguos: {stats['unambiguous_terms']} ({stats['unambiguous_terms']/stats['total_terms']*100:.1f}%)")
    print(f"  • Términos ambiguos: {stats['ambiguous_terms']} ({stats['ambiguous_terms']/stats['total_terms']*100:.1f}%)")
    print(f"\nTérmino más ambiguo: '{stats['most_ambiguous_term']}'")
    print(f"  → Aparece en {stats['max_concepts_per_term']} conceptos diferentes")
    
    # Mostrar ejemplos de uso
    print_examples(inverted_index, synonyms)
    
    print("\n" + "="*60)
    print("CÓMO USAR EL ÍNDICE INVERTIDO")
    print("="*60)
    print("""
1. BÚSQUEDA NO AMBIGUA (ej: "CIL"):
   - Consultar índice: indice_invertido["CIL"]
   - Si is_ambiguous = false:
     → Obtener concept_ids[0]
     → Expandir a todos los sinónimos del concepto
     → Búsqueda: ("CIL" OR "CYL" OR "Cilindro" OR "Astigmatismo")

2. BÚSQUEDA AMBIGUA (ej: "NM"):
   - Consultar índice: indice_invertido["NM"]
   - Si is_ambiguous = true:
     → Expandir CADA concept_id en concept_ids
     → Unir todos los sinónimos de todos los conceptos
     → Búsqueda: ("NM" OR "No mejora" OR "Nistagmus manifiesto")

3. TÉRMINO NO ENCONTRADO:
   - Buscar literalmente el término (sin expansión)
    """)


if __name__ == "__main__":
    main()
