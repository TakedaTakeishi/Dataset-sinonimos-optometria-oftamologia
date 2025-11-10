"""
Ejemplo de uso del sistema de expansión de consultas con índice invertido.

Este script demuestra cómo usar el índice invertido y el tesauro de sinónimos
para expandir términos de búsqueda de manera inteligente.
"""

import json
import sys
import os
from pathlib import Path
from typing import List, Dict, Set

# Configurar codificación UTF-8 para Windows
if sys.platform == 'win32':
    # Cambiar la página de códigos de la consola a UTF-8
    os.system('chcp 65001 > nul')
    # Reconfigurar stdout y stderr
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')


class SynonymExpander:
    """Clase para expandir consultas usando el índice invertido y el tesauro."""
    
    def __init__(self, synonyms_file: Path, inverted_index_file: Path):
        """
        Inicializa el expansor de sinónimos.
        
        Args:
            synonyms_file: Ruta a lista_sinónimos.json
            inverted_index_file: Ruta a indice_invertido.json
        """
        # Cargar tesauro de sinónimos
        with open(synonyms_file, 'r', encoding='utf-8') as f:
            self.synonyms: Dict[str, List[str]] = json.load(f)
        
        # Cargar índice invertido
        with open(inverted_index_file, 'r', encoding='utf-8') as f:
            self.inverted_index: Dict[str, Dict] = json.load(f)
    
    def expand_term(self, term: str) -> Dict:
        """
        Expande un término de búsqueda a todos sus sinónimos.
        
        Args:
            term: Término a expandir
        
        Returns:
            Diccionario con:
            - 'original': Término original
            - 'found': Si el término existe en el índice
            - 'is_ambiguous': Si el término es ambiguo
            - 'concept_ids': Lista de Concept IDs
            - 'expanded_terms': Set de todos los términos expandidos
            - 'query': Consulta booleana lista para usar
        """
        result = {
            'original': term,
            'found': False,
            'is_ambiguous': False,
            'concept_ids': [],
            'expanded_terms': set(),
            'query': term  # Por defecto, el término original
        }
        
        # Buscar en el índice invertido
        if term not in self.inverted_index:
            # Término no encontrado - usar literalmente
            result['expanded_terms'] = {term}
            result['query'] = f'"{term}"'
            return result
        
        # Término encontrado
        index_data = self.inverted_index[term]
        result['found'] = True
        result['is_ambiguous'] = index_data['is_ambiguous']
        result['concept_ids'] = index_data['concept_ids']
        
        # Expandir a todos los sinónimos de todos los conceptos
        all_synonyms: Set[str] = set()
        
        for concept_id in result['concept_ids']:
            if concept_id in self.synonyms:
                all_synonyms.update(self.synonyms[concept_id])
        
        result['expanded_terms'] = all_synonyms
        
        # Construir consulta booleana
        if len(all_synonyms) > 0:
            # Envolver términos con espacios en comillas
            quoted_terms = [f'"{t}"' if ' ' in t else t for t in sorted(all_synonyms)]
            result['query'] = f"({' OR '.join(quoted_terms)})"
        
        return result
    
    def expand_query(self, query: str) -> Dict:
        """
        Expande una consulta completa (puede contener múltiples términos).
        
        Args:
            query: Consulta a expandir (por ahora, un solo término)
        
        Returns:
            Resultado de la expansión
        """
        # Por ahora, asumimos que la consulta es un solo término
        # En el futuro, podrías parsear consultas más complejas
        return self.expand_term(query.strip())
    
    def print_expansion_details(self, result: Dict) -> None:
        """Imprime los detalles de una expansión de forma legible."""
        print("\n" + "="*70)
        print(f"EXPANSION DE: '{result['original']}'")
        print("="*70)
        
        if not result['found']:
            print("[ ] Termino no encontrado en el indice")
            print(f">>> Busqueda literal: {result['query']}")
            return
        
        print(f"[OK] Encontrado en el indice")
        print(f"  * Concept IDs: {', '.join(result['concept_ids'])}")
        print(f"  * Ambiguo?: {'SI' if result['is_ambiguous'] else 'NO'}")
        
        if result['is_ambiguous']:
            print(f"\n[!] TERMINO AMBIGUO")
            print(f"  Expandiendo a {len(result['concept_ids'])} conceptos diferentes:")
            for cid in result['concept_ids']:
                terms = self.synonyms.get(cid, [])
                print(f"    * {cid}: {', '.join(terms)}")
        else:
            print(f"\n[OK] TERMINO NO AMBIGUO")
            cid = result['concept_ids'][0]
            print(f"  Expandiendo concepto {cid}")
        
        print(f"\nTERMINOS EXPANDIDOS ({len(result['expanded_terms'])} terminos):")
        for i, term in enumerate(sorted(result['expanded_terms']), 1):
            print(f"  {i:2d}. {term}")
        
        print(f"\nCONSULTA BOOLEANA:")
        print(f"  {result['query']}")
        print("="*70)


def main():
    # Rutas de archivos
    base_dir = Path(__file__).parent
    synonyms_file = base_dir / "lista_sinónimos.json"
    inverted_index_file = base_dir / "indice_invertido.json"
    
    # Crear expansor
    print("Inicializando expansor de sinonimos...")
    expander = SynonymExpander(synonyms_file, inverted_index_file)
    print(f"[OK] Cargado: {len(expander.synonyms)} conceptos, {len(expander.inverted_index)} terminos")
    
    # Ejemplos de búsqueda
    test_queries = [
        "CIL",           # Caso NO ambiguo (solo astigmatismo)
        "NM",            # Caso AMBIGUO (No mejora / Nistagmus manifiesto)
        "AR",            # Caso AMBIGUO (Autorrefractometro / Artritis reumatoide)
        "Astigmatismo",  # Caso NO ambiguo
        "DP",            # Caso MUY ambiguo (3 conceptos)
        "XYZ123"         # Caso NO ENCONTRADO
    ]
    
    print("\n" + "="*70)
    print("  DEMOSTRACION DE EXPANSION DE CONSULTAS")
    print("="*70)
    
    for query in test_queries:
        result = expander.expand_query(query)
        expander.print_expansion_details(result)
    
    print("\n" + "="*70)
    print("RESUMEN DE REGLAS")
    print("="*70)
    print("""
REGLA 1: Termino NO ambiguo (ej: "CIL")
  -> Expandir a todos los sinonimos del unico concepto
  -> Busqueda: (CIL OR CYL OR Cilindro OR Astigmatismo)

REGLA 2: Termino AMBIGUO (ej: "NM")
  -> Expandir a todos los sinonimos de TODOS los conceptos
  -> Busqueda: (NM OR "No mejora" OR "Nistagmus manifiesto")
  -> El usuario vera resultados de ambos significados

REGLA 3: Termino NO encontrado (ej: "XYZ123")
  -> Buscar literalmente sin expansion
  -> Busqueda: "XYZ123"
    """)


if __name__ == "__main__":
    main()
