#!/usr/bin/env python3

import csv

cemitery = [{
    'zone': ('Cemitério São João Batista', 'Novo'),
    'streets': (1, 60),
    'numbers': (1, 41)
}, {
    'zone': ('Cemitério São João Batista', 'Antigo'),
    'streets': (73, 119),
    'numbers': (1, 41)
}, {
    'zone': ('Cruzeiro', ''),
    'streets': (119, 148),
    'numbers': (1, 41)
}, {
    'zone': ('Cruzeiro', ''),
    'streets': (174, 194),
    'numbers': (1, 41)
}, {
    'zone': ('Ala', '1'),
    'streets': (148, 174),
    'numbers': (1, 41)
}, {
    'zone': ('Ala', '2'),
    'streets': (148, 174),
    'numbers': (1, 41)
}, {
    'zone': ('Quadra', 'A'),
    'streets': (1, 27),
    'numbers': (1, 41)
}, {
    'zone': ('Quadra', 'B'),
    'streets': (1, 27),
    'numbers': (1, 41)
}, {
    'zone': ('Quadra', 'C'),
    'streets': (1, 27),
    'numbers': (1, 41)
}, {
    'zone': ('Quadra', 'D'),
    'streets': (1, 27),
    'numbers': (1, 41)
}, {
    'zone': ('Valas', ''),
    'streets': (1, 9),
    'numbers': (1, 45)
}, {
    'zone': ('Valinha', ''),
    'streets': (60, 73),
    'numbers': (1, 41)
}, {
    'zone': ('Cemitério Santíssimo Sacramento', '1'),
    'streets': (1, 30),
    'numbers': (1, 41)
}, {
    'zone': ('Cemitério Santíssimo Sacramento', '2'),
    'streets': (1, 30),
    'numbers': (1, 41)
}]

with open('graves.tsv', 'wt') as graves:
    writer = csv.writer(graves, delimiter='\t')
    writer.writerow(['RUA', 'NÚMERO', 'REGIÃO', 'COMPLEMENTO'])

    for graves in cemitery:
        for street in range(*graves.get('streets')):
            for number in range(*graves.get('numbers')):
                writer.writerow([street, number, *graves.get('zone')])
