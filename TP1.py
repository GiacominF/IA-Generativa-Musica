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
        (["COMPASSO_V", "COMPASSO_IV", "COMPASSO_I", "COMPASSO_I"], 1)
    ],

}