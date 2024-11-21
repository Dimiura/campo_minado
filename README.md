# Campo Minado

Um jogo de Campo Minado clássico implementado em Python com interface gráfica usando Tkinter.

## Características

- Interface gráfica amigável com tema azul e branco
- Três níveis de dificuldade:
  - Fácil (8x8, 10 minas)
  - Médio (12x12, 30 minas)
  - Difícil (16x16, 60 minas)
- Sistema de recordes pessoais
- Cronômetro para cada partida
- Marcação de bandeiras com clique direito
- Interface estilizada com ícones de bomba e bandeira

## Como Jogar

1. Execute o arquivo `minesweeper.py`
2. Escolha um nível de dificuldade na tela inicial
3. Clique esquerdo para revelar células
4. Clique direito para marcar/desmarcar bandeiras
5. Evite as bombas e revele todas as células seguras para vencer

## Controles

- Clique esquerdo: Revelar célula
- Clique direito: Marcar/desmarcar bandeira

## Recordes

Os recordes são salvos automaticamente para cada nível de dificuldade e podem ser visualizados na tela inicial.

## Requisitos

- Python 3.x
- Tkinter (geralmente incluído com Python)
- PIL (Python Imaging Library)

## Instalação

```bash
pip install pillow
python minesweeper.py
```