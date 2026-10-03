from dataclasses import dataclass
from typing import List, Dict, Tuple
import random
import mido
from mido import Message, MidiFile, MidiTrack, MetaMessage
import numpy as np
from scipy.io import wavfile

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
    
    "LICK_TURN_AROUND_1": [
        (["NOTA_CURTA_I", "NOTA_CURTA_IV", "NOTA_CURTA_V", "NOTA_CURTA_I", "NOTA_LONGA_I"], 1.0)
    ],

    "LICK_TURN_AROUND_2": [
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

#Expansão do axioma até os nós terminais
def gerar_terminais(simbolo: str, gramatica: dict) -> List[str]:
        """
        Expande recursivamente um símbolo através da gramática probabilística.
        
        :param simbolo: Símbolo atual a ser expandido (ex.: "BLUES", "COMPASSO_I", etc.)
        :param gramatica: Dicionário contendo as regras de produção e probabilidades
        :param temperatura: Hiperparâmetro que controla a aleatoriedade das escolhas
        :return: Lista linear de símbolos puramente terminais
        """
        #Se o símbolo não está nas regras, é terminal
        if simbolo not in gramatica:
            return [simbolo]
        
        #Obter as produções possíveis para o símbolo não-terminal (Lista de tuplas)
        producoes = gramatica[simbolo]
        
        opcoes = [regra for regra, _ in producoes]
        pesos = [peso for _, peso in producoes]
        
        #Sorteio probabilístico
        sorteio = random.choices(opcoes, weights=pesos, k=1) #Retorna lista sorteada
        lista_escolhida = sorteio[0]
        
        #Expandir cada símbolo da lista escolhida
        resultado_final: List[str] = []
        for sub_simbolo in lista_escolhida:
            resultado_final.extend(gerar_terminais(sub_simbolo, gramatica))
            
        return resultado_final

#Conversão da lista de nós terminais para notas reais
def converter_terminais_para_notas(terminais: List[str], tabela_duracoes: Dict[str, float] = TABELA_DURACOES,
    escalas: Dict[str, List[int]] = ESCALAS_BLUES, step_bias: float = 2.0
    ) -> List[Nota]:
        """
        Converte uma lista de terminais gramaticais em uma sequência coerente de objetos Nota.
        
        :param terminais: Lista de strings geradas pela gramática (ex.: ["NOTA_CURTA_I", "PAUSA_CURTA", ...])
        :param tabela_duracoes: Dicionário mapeando os tipos rítmicos para durações em batidas
        :param escalas: Dicionário contendo as notas MIDI permitidas para cada grau (I, IV, V)
        :param step_bias: Hiperparâmetro que favorece notas vizinhas (quanto maior, mais fluida a melodia)
        :return: Lista de instâncias de Nota(pitch, duracao)
        """
        #Instanciação da estrutura que irá armazenas as notas
        notas_musicais: List[Nota] = []
        
        #Inicia a referência melódica na tônica de Dó para calcular as distâncias
        pitch_anterior: int = escalas["I"][0]
        
        for terminal in terminais:
            #Tratamento de Pausas
            if terminal == "PAUSA_CURTA":
                duracao = tabela_duracoes.get("PAUSA_CURTA", 1.0)
                notas_musicais.append(Nota(pitch=0, duracao=duracao))
                continue
            
            #Tratamento de Notas
            partes = terminal.split("_")
            if len(partes) != 3 or partes[0] != "NOTA":
                continue  # Ignora símbolos desconhecidos
            
            tipo_duracao = partes[1]   # "CURTA", "MEDIA", "LONGA"
            grau_acorde = partes[2]    # "I", "IV", "V"
            
            duracao = tabela_duracoes.get(tipo_duracao, 1.0)
            notas_possiveis = escalas.get(grau_acorde, escalas["I"])
            
            #Cálculo dos pesos para cada nota da escala do acorde atual
            pesos_notas = []
            for nota in notas_possiveis:
                #Distância melódica em semitons da nota anterior
                distancia = abs(nota - pitch_anterior)
                #Quanto mais perto, maior o peso base
                peso = 1.0 / ((distancia + 1) ** (1.0 / step_bias))
                
                #Heurística musical de estabilidade para notas LONGAS
                #As notas de repouso ideais no blues são a tônica (índice 0) e a 5ª (índice 4)
                if tipo_duracao == "LONGA":
                    if nota == notas_possiveis[0] or nota == notas_possiveis[4]:
                        peso *= 3.0  # Reforça resolução harmônica
                
                #Heurística para notas CURTAS: valorizar notas de passagem e blue note (índice 3)
                elif tipo_duracao == "CURTA":
                    if nota == notas_possiveis[3]:  #Blue note
                        peso *= 1.8
                        
                pesos_notas.append(peso)
            
            #Sorteia a nota respeitando os pesos de condução melódica
            pitch_escolhido = random.choices(notas_possiveis, weights=pesos_notas, k=1)[0]
            
            notas_musicais.append(Nota(pitch=pitch_escolhido, duracao=duracao))
            pitch_anterior = pitch_escolhido  #Atualiza o ponto de partida da próxima nota

        return notas_musicais
    
def salvar_midi(notas: List[Nota], caminho_arquivo: str, bpm: int = 120) -> None:
        """
        Exporta a lista de objetos Nota para um arquivo padrão MIDI (.mid).
        """
        mid = MidiFile(ticks_per_beat=480)
        track = MidiTrack()
        mid.tracks.append(track)
    
        #Metadados de andamento e compasso
        track.append(MetaMessage('set_tempo', tempo=mido.bpm2tempo(bpm), time=0))
        track.append(MetaMessage('time_signature', numerator=4, denominator=4, time=0))
    
        tempo_acumulado = 0
        ticks_por_batida = 480
    
        for nota in notas:
            duracao_ticks = int(nota.duracao * ticks_por_batida)
            
            #Se for pausa (pitch 0), acumulamos o silêncio sem emitir note_on
            if nota.pitch == 0:
                tempo_acumulado += duracao_ticks
            else:
                #Início da nota (com o atraso acumulado de eventuais pausas anteriores)
                track.append(Message('note_on', note=nota.pitch, velocity=90, time=tempo_acumulado))
                #Fim da nota após a sua duração
                track.append(Message('note_off', note=nota.pitch, velocity=64, time=duracao_ticks))
                tempo_acumulado = 0
                
        track.append(MetaMessage('end_of_track', time=tempo_acumulado))
    
        mid.save(caminho_arquivo)
        print(f"-> Arquivo MIDI salvo em: {caminho_arquivo}")


def sintetizar_wav(notas: List[Nota], caminho_arquivo: str, bpm: int = 120, samplerate: int = 44100) -> None:
    """
    Sintetiza a lista de notas em um arquivo de áudio PCM WAV (.wav) puro.
    Utiliza síntese aditiva com harmônicos e envelope de amplitude para evitar estalos (clicks).
    """
    segundos_por_batida = 60.0 / bpm
    segmentos_de_audio = []

    for nota in notas:
        duracao_segundos = nota.duracao * segundos_por_batida
        num_amostras = int(samplerate * duracao_segundos)
        
        if num_amostras <= 0:
            continue
            
        t = np.linspace(0, duracao_segundos, num_amostras, endpoint=False)

        if nota.pitch == 0:
            #Pausa: silêncio absoluto
            onda = np.zeros(num_amostras)
        else:
            #Frequência fundamental da nota em Hz: f = 440 * 2^((pitch - 69)/12)
            freq = 440.0 * (2.0 ** ((nota.pitch - 69) / 12.0))
            
            #Síntese aditiva: fundamental + harmônicos suaves para timbre expressivo
            onda = (
                0.60 * np.sin(2 * np.pi * freq * t) +
                0.25 * np.sin(2 * np.pi * 2 * freq * t) +
                0.15 * np.sin(2 * np.pi * 3 * freq * t)
            )
            
            #Envelope de amplitude para suavizar o ataque e o release
            fade_len = min(int(samplerate * 0.02), num_amostras // 4)
            if fade_len > 0:
                envelope = np.ones(num_amostras)
                envelope[:fade_len] = np.linspace(0, 1, fade_len)
                envelope[-fade_len:] = np.linspace(1, 0, fade_len)
                onda *= envelope

        segmentos_de_audio.append(onda)

    if not segmentos_de_audio:
        return

    #Concatenação e normalização do sinal para 16-bit PCM
    audio_completo = np.concatenate(segmentos_de_audio)
    pico = np.max(np.abs(audio_completo))
    if pico > 0:
        audio_normalizado = audio_completo / pico
    else:
        audio_normalizado = audio_completo

    audio_int16 = (audio_normalizado * 32767).astype(np.int16)
    wavfile.write(caminho_arquivo, samplerate, audio_int16)
    print(f"-> Arquivo Áudio WAV salvo em: {caminho_arquivo}")


if __name__ == "__main__":
    
    experimentos = [
        {"nome": "musica_1_melodica", "bias": 3.0, "bpm": 110, "seed": 42},    #Condução melódica suave e fluida
        {"nome": "musica_2_equilibrada", "bias": 1.5, "bpm": 120, "seed": 105}, #Condução com licks e saltos moderados
        {"nome": "musica_3_expressiva", "bias": 0.8, "bpm": 130, "seed": 999}  #Condução mais angular e andamento rápido
    ]
    
    for exp in experimentos:
        random.seed(exp["seed"])
        print(f"\n--- Gerando {exp['nome']} (Bias: {exp['bias']}, BPM: {exp['bpm']}, Seed: {exp['seed']}) ---")
        
        #Expansão gramatical probabilística a partir do axioma
        terminais = gerar_terminais("BLUES", minha_gramatica)
        
        #Conversão dos terminais para notas reais com condução melódica
        notas = converter_terminais_para_notas(terminais, step_bias=exp["bias"])
        
        #Exportação simbólica (.mid) e em áudio (.wav)
        arq_mid = f"{exp['nome']}.mid"
        arq_wav = f"{exp['nome']}.wav"
        
        salvar_midi(notas, arq_mid, bpm=exp["bpm"])
        sintetizar_wav(notas, arq_wav, bpm=exp["bpm"])
        
        dur_batidas = sum(n.duracao for n in notas)
        print(f"Concluído: {len(notas)} eventos gerados ({dur_batidas} batidas, 3 choruses).")

