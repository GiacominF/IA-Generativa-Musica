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
    
    "COMPASSO_I" : [
        (["MOTIVO_I_BASE"], 0,4),
        (["MOTIVO_I_ARPEJO"], 0,3),
        (["MOTIVO_I_RESPOSTA", "PAUSA_CURTA"], 0,3)
    ],
    
    "COMPASSO_IV" : [
        (["LICK_BLUES_IV"], 0,7),
        (["MOTIVO_TENSAO_IV"], 0,3)
    ],
    
    "COMPASSO_V" : [
        (["MOTIVO_CLIMAX_V"], 1)
    ],

    "TURN_AROUND" : [
        (["LICK_TURN_AROUND_1"], 0,5),
        (["LICK_TURN_AROUND_2"], 0,5)
    ],

}