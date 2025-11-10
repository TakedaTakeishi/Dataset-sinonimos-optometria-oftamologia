#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Refina el filtrado de siglas_optometría.csv y actualiza a_modificar.txt.
"""
import csv
from pathlib import Path

BASE = Path(__file__).parent
CSV_FILE = BASE / 'siglas_optometría.csv'
OUT_FILE = BASE / 'a_modificar.txt'

def main():
    # Leer el CSV
    with CSV_FILE.open('r', encoding='utf-8', newline='') as f:
        reader = csv.reader(f)
        all_rows = list(reader)

    header = all_rows[0]
    data_rows = all_rows[1:]
    
    filtered_rows = []
    rows_to_keep = []

    for row in data_rows:
        if not row or len(row) < 2:
            rows_to_keep.append(row)
            continue

        sigla, expansion = row[0].strip(), row[1].strip()

        # Criterios de filtrado
        is_multiple_def = '1)' in expansion or '2)' in expansion
        is_multiple_sigla = ' / ' in sigla or '/' in expansion
        is_translation = 'inglés' in expansion
        has_parenthesis = '(' in expansion or ')' in expansion

        if is_multiple_def or is_multiple_sigla or is_translation or has_parenthesis:
            filtered_rows.append((sigla, expansion))
        else:
            rows_to_keep.append(row)

    # Ordenar alfabéticamente
    filtered_rows.sort(key=lambda x: x[0].lower())

    # Escribir a_modificar.txt
    with OUT_FILE.open('w', encoding='utf-8', newline='\n') as f:
        current_letter = None
        for sigla, expansion in filtered_rows:
            first_letter = sigla[0].upper() if sigla else ''
            if current_letter and first_letter != current_letter:
                f.write('\n')
            f.write(f"{sigla}\t{expansion}\n")
            current_letter = first_letter

    # Sobrescribir el CSV original
    with CSV_FILE.open('w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(rows_to_keep)

if __name__ == '__main__':
    main()
