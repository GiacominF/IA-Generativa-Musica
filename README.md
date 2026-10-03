# DCC831 – IA Generativa para Música (UFMG)
## Trabalho Prático 1 – Composição Musical Algorítmica

**Aluno:** Guilherme Farany  
**Método Escolhido:** Gramáticas Generativas (Gramática Livre de Contexto Probabilística - PCFG)  
**Restrição Estilística/Temática:** Blues Tradicional de 12 Compassos (12-bar blues em Dó)

---

## 1. Visão Geral do Projeto

Este projeto implementa um sistema de composição musical algorítmica de ponta a ponta fundamentado em **Gramáticas Generativas Estocásticas (PCFG)**. O objetivo é sintetizar peças musicais simbólicas no formato MIDI (`.mid`) e convertê-las em áudio (`.wav`), respeitando estritamente a forma tradicional de um **Blues de 12 compassos**.

## 2. Requisitos e Instalação

### Pré-requisitos
* Python 3.10 ou superior.
* Gerenciador de pacotes `pip`.

### Instalação das Dependências

Clone o repositório e instale os pacotes necessários:

```bash
git clone https://github.com/GuilhermeFarany/IA-Generativa-Musica.git
cd IA-Generativa-Musica
pip install -r requirements.txt
```

As dependências principais são:
* `mido`: Manipulação e exportação de sequências MIDI padrão.
* `numpy`: Processamento de vetores de áudio.
* `scipy`: Exportação de formas de onda em formato WAV PCM.

---

## 3. Instruções de Execução e Reprodução

Para reproduzir a geração completa das músicas simbólicas e dos respectivos arquivos de áudio sintetizado, execute:

```bash
python TP1.py
```
*(ou `python3 TP1.py`, dependendo do seu ambiente).*

O script executará a derivação a partir da gramática, exportará os arquivos `.mid` correspondentes e sintetizará diretamente os arquivos de áudio `.wav`.

---

## 4. Arquivos Gerados e Hiperparâmetros

A execução do código gera pelo menos **3 peças musicais distintas**, demonstrando a capacidade do método de variar a partir de diferentes configurações de sementes e hiperparâmetros:

* `musica_1_melodica.mid` / `musica_1_melodica.wav`: Geração com viés de condução melódica suave e andamento clássico.
* `musica_2_equilibrada.mid` / `musica_2_equilibrada.wav`: Geração balanceada com licks blues e saltos moderados.
* `musica_3_expressiva.mid` / `musica_3_expressiva.wav`: Geração com fraseado mais angular e andamento acelerado.

---

## 5. Declaração de Uso de Ferramentas de IA

> *Conforme estabelecido nas instruções do TP, o uso de ferramentas de IA deve ser declarado com a descrição do apoio e os links correspondentes.*

Link para a conversa:
https://share.gemini.google/NpU5b01fOaFr

IA Utilizada para entender melhor conceitos e jargões musicais específicos; Para definir os trade-offs entre os três possíveis
métodos apresentados na especificação do trabalho, culminando na escolha das gramáticas generativas; e para detalhes de implementação de sintaxe e também das bibliotecas de processamento áudio.

---
