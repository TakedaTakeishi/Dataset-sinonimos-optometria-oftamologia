#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para generar un tesauro maestro consolidado a partir de tres fuentes:
- sinónimos.yml: Listas de sinónimos
- siglas_médicas.json: Diccionario de siglas y sus expansiones
- siglas_optometría.csv: CSV con siglas y expansiones

Genera lista_sinónimos.json con conceptos únicos identificados por ID.
"""

import json
import csv
import re
import sys
from pathlib import Path

# Configurar codificación UTF-8 para la salida de consola
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')
from collections import defaultdict
from typing import List, Dict, Set, Tuple


def normalize_term(term: str) -> str:
    """Normaliza un término eliminando espacios extras."""
    return term.strip()


def create_concept_signature(terms: List[str]) -> Tuple[str, ...]:
    """
    Crea una firma única para un concepto basada en sus términos.
    Los términos se normalizan, eliminan duplicados y ordenan alfabéticamente.
    """
    # Normalizar y eliminar duplicados
    normalized = list(set(normalize_term(t) for t in terms if normalize_term(t)))
    # Ordenar alfabéticamente (case-insensitive)
    normalized.sort(key=lambda x: x.lower())
    return tuple(normalized)


def load_sinonimos_yml(filepath: Path) -> List[List[str]]:
    """Carga el archivo YAML de sinónimos."""
    sinonimos = []
    with filepath.open('r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            # Buscar patrón [término1, término2, ...]
            if line.startswith('[') and line.endswith(']'):
                # Remover corchetes
                content = line[1:-1]
                # Dividir por comas, pero respetando comas dentro de términos
                items = []
                current_item = ''
                in_quotes = False
                for char in content:
                    if char == ',' and not in_quotes:
                        if current_item.strip():
                            items.append(current_item.strip())
                        current_item = ''
                    else:
                        current_item += char
                # Añadir el último item
                if current_item.strip():
                    items.append(current_item.strip())
                
                if items:
                    sinonimos.append(items)
    return sinonimos


def load_siglas_json(filepath: Path) -> Dict[str, List[str]]:
    """Carga el archivo JSON de siglas médicas."""
    with filepath.open('r', encoding='utf-8') as f:
        data = json.load(f)
    return data


def load_siglas_csv(filepath: Path) -> List[Tuple[str, str]]:
    """Carga el archivo CSV de siglas de optometría."""
    rows = []
    with filepath.open('r', encoding='utf-8', newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if 'Sigla' in row and 'Expansión' in row:
                # Verificar que los valores no sean None
                sigla = row['Sigla']
                expansion = row['Expansión']
                if sigla is not None and expansion is not None:
                    sigla = sigla.strip()
                    expansion = expansion.strip()
                    if sigla and expansion:
                        rows.append((sigla, expansion))
    return rows


def build_concept_map(
    sinonimos: List[List[str]],
    siglas_json: Dict[str, List[str]],
    siglas_csv: List[Tuple[str, str]]
) -> Dict[str, List[str]]:
    """
    Construye el mapa de conceptos con IDs únicos.
    
    JERARQUÍA DE PROCESAMIENTO:
    1. siglas_médicas.json establece conceptos canónicos (NO se fusionan entre sí)
    2. sinónimos.yml y siglas_optometría.csv se unen a conceptos existentes o crean nuevos
    
    Returns:
        Diccionario donde la clave es el Concept ID y el valor es la lista de términos.
    """
    # Lista de conceptos (cada uno es un conjunto de términos)
    concepts: List[Set[str]] = []
    
    # PASO 1: Procesar siglas_médicas.json (conceptos canónicos, NO se fusionan)
    for sigla, expansiones in siglas_json.items():
        terms = [sigla] + expansiones
        normalized = set(normalize_term(t) for t in terms if normalize_term(t))
        if normalized:
            concepts.append(normalized)
    
    # PASO 2: Procesar sinónimos.yml (se pueden fusionar con existentes)
    for synonym_list in sinonimos:
        normalized = set(normalize_term(t) for t in synonym_list if normalize_term(t))
        if normalized:
            # Buscar si comparte términos con algún concepto existente
            merged = False
            for i, existing_concept in enumerate(concepts):
                if normalized & existing_concept:
                    concepts[i] = existing_concept | normalized
                    merged = True
                    break
            
            if not merged:
                concepts.append(normalized)
    
    # PASO 3: Procesar siglas_optometría.csv (se pueden fusionar con existentes)
    for sigla, expansion in siglas_csv:
        terms = [sigla, expansion]
        normalized = set(normalize_term(t) for t in terms if normalize_term(t))
        if normalized:
            # Buscar si comparte términos con algún concepto existente
            merged = False
            for i, existing_concept in enumerate(concepts):
                if normalized & existing_concept:
                    concepts[i] = existing_concept | normalized
                    merged = True
                    break
            
            if not merged:
                concepts.append(normalized)
    
    # Crear el mapa de conceptos con IDs
    concept_map: Dict[str, List[str]] = {}
    for idx, term_set in enumerate(concepts, start=1):
        concept_id = f"C{idx:04d}"
        # Eliminar sufijos -1, -2, etc. de términos internos
        cleaned_terms = set()
        for term in term_set:
            # Si el término termina con -N (donde N es un número), eliminar el sufijo
            import re
            cleaned_term = re.sub(r'-\d+$', '', term)
            cleaned_terms.add(cleaned_term)
        
        # Ordenar alfabéticamente (case-insensitive)
        terms_list = sorted(cleaned_terms, key=lambda x: x.lower())
        concept_map[concept_id] = terms_list
    
    return concept_map


def generate_statistics(concept_map: Dict[str, List[str]]) -> None:
    """Genera y muestra estadísticas del tesauro."""
    # Construir term_map para detectar ambigüedades
    term_map: Dict[str, List[str]] = defaultdict(list)
    for concept_id, terms in concept_map.items():
        for term in terms:
            term_map[term].append(concept_id)
    
    # Calcular estadísticas
    total_concepts = len(concept_map)
    term_counts = [len(terms) for terms in concept_map.values()]
    avg_terms = sum(term_counts) / total_concepts if total_concepts > 0 else 0
    max_terms = max(term_counts) if term_counts else 0
    min_terms = min(term_counts) if term_counts else 0
    
    # Detectar términos ambiguos
    ambiguous_terms = {
        term: concept_ids
        for term, concept_ids in term_map.items()
        if len(concept_ids) > 1
    }
    
    # Imprimir reporte
    print("\n--- REPORTE DEL TESAURO ---")
    print(f"Conceptos únicos totales: {total_concepts}")
    print(f"\nEstadísticas de Términos por Concepto:")
    print(f"- Promedio: {avg_terms:.1f}")
    print(f"- Máximo: {max_terms}")
    print(f"- Mínimo: {min_terms}")
    
    if ambiguous_terms:
        print(f"\nTérminos Ambiguos (aparecen en >1 concepto): {len(ambiguous_terms)}")
        # Ordenar alfabéticamente
        for term in sorted(ambiguous_terms.keys(), key=lambda x: x.lower()):
            concept_ids = ambiguous_terms[term]
            concept_ids_str = ", ".join(sorted(concept_ids))
            print(f"- {term} (en {len(concept_ids)} conceptos: {concept_ids_str})")
    else:
        print("\nTérminos Ambiguos: Ninguno")
    
    print("---------------------------\n")


def main():
    """Función principal del script."""
    # Definir rutas
    base_dir = Path(__file__).parent
    sinonimos_path = base_dir / 'sinónimos.yml'
    siglas_json_path = base_dir / 'siglas_medicas.json'
    siglas_csv_path = base_dir / 'siglas_optometría.csv'
    output_path = base_dir / 'lista_sinónimos.json'
    
    # Verificar que los archivos existen
    for filepath in [sinonimos_path, siglas_json_path, siglas_csv_path]:
        if not filepath.exists():
            print(f"ERROR: No se encuentra el archivo {filepath}")
            return
    
    print("Cargando archivos de entrada...")
    
    # Cargar datos
    sinonimos = load_sinonimos_yml(sinonimos_path)
    siglas_json = load_siglas_json(siglas_json_path)
    siglas_csv = load_siglas_csv(siglas_csv_path)
    
    print(f"- sinónimos.yml: {len(sinonimos)} grupos de sinónimos")
    print(f"- siglas_medicas.json: {len(siglas_json)} siglas")
    print(f"- siglas_optometría.csv: {len(siglas_csv)} entradas")
    
    # Construir el mapa de conceptos
    print("\nGenerando tesauro maestro...")
    concept_map = build_concept_map(sinonimos, siglas_json, siglas_csv)
    
    # Guardar el JSON
    print(f"Guardando en {output_path}...")
    with output_path.open('w', encoding='utf-8') as f:
        json.dump(concept_map, f, ensure_ascii=False, indent=2)
    
    print(f"✓ Archivo {output_path.name} generado exitosamente")
    
    # Generar estadísticas
    generate_statistics(concept_map)


if __name__ == '__main__':
    main()
