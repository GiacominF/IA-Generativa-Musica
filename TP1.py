from dataclasses import dataclass
from typing import List, Dict, Tuple

#Definição da estrutura da nota
@dataclass
class Nota:
    pitch: int
    duracao: float

#Definição da estrutura da gramática
#Id é o nó não terminal (string)
#Conteúdo desse Id é uma lista de possbilidades(sequências e suas probabilidades)
Gramatica = Dict[str, List[Tuple[List[str], int]]]

#Povoar o dicionário com as regras
minha_gramatica: Gramatica = {
    #Primeiro nível de "decisão"
    #Axioma
    "BLUES" : [
        (["CHORUS", "CHORUS", "CHORUS"], 1)
    ],
    
    "CHORUS" : [
        (["FRASE_1", "FRASE_2", "FRASE_3"], 1)
    ],
    
    #Expansão para os compassos:
    "FRASE_1" : [
        (["COMPASSO_I", "COMPASSO_I", "COMPASSO_I", "COMPASSO_I"], 1)
    ],
    
    "FRASE_2": [
        (["COMPASSO_IV", "COMPASSO_IV", "COMPASSO_I", "COMPASSO_I"], 1)
    ],
    
    "FRASE_3": [
        (["COMPASSO_V", "COMPASSO_IV", "COMPASSO_I", "TURN_AROUND"], 1)
    ],
    
    #Estrutura dos compassos
    "COMPASSO_I" : [
        (["MOTIVO_I_BASE"], 0.4),
        (["MOTIVO_I_ARPEJO"], 0.3),
        (["MOTIVO_I_RESPOSTA", "PAUSA_CURTA"], 0.3)
    ],
    
    "COMPASSO_IV" : [
        (["LICK_BLUES_IV"], 0.7),
        (["MOTIVO_TENSAO_IV"], 0.3)
    ],
    
    "COMPASSO_V" : [
        (["MOTIVO_CLIMAX_V"], 1)
    ],

    "TURN_AROUND" : [
        (["LICK_TURN_AROUND_1"], 0.5),
        (["LICK_TURN_AROUND_2"], 0.5)
    ],
    
    #Nível dos acordes
    "MOTIVO_I_BASE": [
        (["NOTA_MEDIA_I", "NOTA_MEDIA_I", "NOTA_MEDIA_I", "NOTA_MEDIA_I"], 0.6),
        (["NOTA_CURTA_I", "NOTA_CURTA_I", "NOTA_MEDIA_I", "NOTA_LONGA_I"], 0.4)
    ],

    "MOTIVO_I_ARPEJO": [
        (["NOTA_CURTA_I", "NOTA_CURTA_I", "NOTA_MEDIA_I", "NOTA_LONGA_I"], 1)
    ],

    "MOTIVO_I_RESPOSTA": [
        (["NOTA_CURTA_I", "NOTA_CURTA_I", "NOTA_LONGA_I"], 0.6),
        (["NOTA_MEDIA_I", "NOTA_MEDIA_I", "NOTA_MEDIA_I"], 0.4)
    ],
    
    "LICK_BLUES_IV": [
        (["NOTA_CURTA_IV", "NOTA_CURTA_IV", "NOTA_CURTA_IV", "NOTA_CURTA_IV", "NOTA_LONGA_IV"], 1.0)
    ],

    "MOTIVO_TENSAO_IV": [
        (["NOTA_LONGA_IV", "NOTA_LONGA_IV"], 0.7),
        (["NOTA_LONGA_IV", "NOTA_MEDIA_IV", "NOTA_MEDIA_IV"], 0.3)
    ],
    
    "MOTIVO_CLIMAX_V": [
        (["NOTA_CURTA_V", "NOTA_CURTA_V", "NOTA_CURTA_V", "NOTA_CURTA_V", "NOTA_CURTA_V", "NOTA_CURTA_V", "NOTA_MEDIA_V"], 1.0)
    ],
    
    "LICK_TURNAROUND_1": [
        (["NOTA_CURTA_I", "NOTA_CURTA_IV", "NOTA_CURTA_V", "NOTA_CURTA_I", "NOTA_LONGA_I"], 1.0)
    ],

    "LICK_TURNAROUND_2": [
        (["NOTA_MEDIA_V", "NOTA_MEDIA_V", "NOTA_LONGA_I"], 1.0)
    ]
}

# Mapeamento do tipo de nota para o tempo em batidas
TABELA_DURACOES = {
    "LONGA": 2.0,
    "MEDIA": 1.0,
    "CURTA": 0.5,
    "PAUSA_CURTA": 1.0
}

# Tabela de frequências permitidas (MIDI) por acorde
ESCALAS_BLUES = {
    "I":  [60, 63, 65, 66, 67, 70],  # Dó, Mib, Fá, Fá#, Sol, Sib
    "IV": [65, 68, 70, 71, 72, 75],  # Fá, Láb, Sib, Si, Dó, Mib
    "V":  [67, 70, 72, 73, 74, 77]   # Sol, Sib, Dó, Dó#, Ré, Fá
}