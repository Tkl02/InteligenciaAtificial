# Inteligência Artificial

Repositório acadêmico com implementações práticas da disciplina de **Inteligência Artificial**, cobrindo otimização com algoritmos genéticos, detecção de similaridade textual e visão computacional com detecção de objetos em tempo real.

---

## Visão geral

| Módulo | Pasta | Técnica | Descrição |
|--------|-------|---------|-----------|
| Algoritmo Genético | [`apresentação/`](apresentação/) | Otimização evolutiva | Minimização de função contínua em \(\mathbb{R}^2\) |
| Detector de Plágio | [`apresentação/`](apresentação/) | Distância de Levenshtein + Fuzzy Matching | Comparação de textos com interface gráfica |
| Detecção de Mobs | [`trabalhofinal/`](trabalhofinal/) | YOLOv8 (Ultralytics) | Classificação e tracking de entidades do Minecraft |

---

## Estrutura do repositório

```
InteligenciaArtificial/
├── apresentação/
│   ├── function_AI.py           # Algoritmo genético
│   └── plagiarism_detector.py   # Detector de plágio (GUI)
├── trabalhofinal/
│   ├── treino_modelo.py         # Treinamento do YOLOv8
│   ├── capture_windows.py       # Inferência em tempo real
│   ├── windowcapture.py         # Captura de tela (Windows API)
│   ├── mine.yaml                # Configuração do dataset YOLO
│   ├── best.pt / last.pt        # Pesos do modelo treinado
│   └── datasets2/mine/          # Dataset anotado (train / val)
├── LICENSE                      # GNU GPLv3
└── README.md
```

---

## 1. Algoritmo genético — `function_AI.py`

Implementação de um **algoritmo genético binário** para minimizar a função objetivo:

\[
f(x_1, x_2) = (x_1^2 + x_2 - 11) + (x_1 + x_2^2 - 7)^2
\]

### Características

- **Codificação:** cromossomo de 20 bits (10 bits por variável), mapeado para o intervalo \([0, 6]\)
- **Seleção:** amostragem estocástica proporcional à aptidão (*fitness proportional selection*)
- **Cruzamento:** ponto único, probabilidade de 80%
- **Mutação:** bit-flip com taxa de 5%
- **Elitismo:** preservação dos 2 melhores indivíduos a cada geração
- **Aptidão:** \( \text{fitness} = 1 / (1 + f(x_1, x_2)) \)

### Execução

```bash
python apresentação/function_AI.py
```

Parâmetros padrão: população de 20 indivíduos e 1000 gerações. Ao final de cada execução, o programa solicita se deseja reiniciar a busca.

---

## 2. Detector de plágio — `plagiarism_detector.py`

Aplicação desktop que compara dois textos e indica possível plágio com base em métricas de similaridade.

### Técnicas utilizadas

| Métrica | Biblioteca / implementação | Papel |
|---------|----------------------------|-------|
| Distância de Levenshtein | Implementação iterativa própria | Número de edições (inserção, remoção, substituição) |
| Partial Token Sort Ratio | [TheFuzz](https://github.com/seatgeek/thefuzz) | Similaridade com tokens ordenados |
| Partial Token Set Ratio | TheFuzz | Similaridade com conjuntos de tokens |

Um texto é classificado como **plágio** quando o *sort ratio* ou o *set ratio* é **≥ 60%**.

### Interface

- GUI moderna com **CustomTkinter** (tema escuro)
- Dois campos de texto e botão de análise
- Pop-up com o resultado das três métricas

### Execução

```bash
pip install thefuzz customtkinter
python apresentação/plagiarism_detector.py
```

> Créditos da implementação base: [@Fael123Programming](https://github.com/Fael123Programming)

---

## 3. Trabalho final — Detecção de mobs (Minecraft)

Sistema de **detecção e rastreamento de objetos** baseado em **YOLOv8**, treinado para reconhecer 15 classes de entidades do Minecraft a partir de capturas de tela.

### Classes detectadas

| ID | Classe | ID | Classe | ID | Classe |
|----|--------|----|--------|----|--------|
| 0 | chicken | 5 | pig | 10 | villager |
| 1 | cow | 6 | sheep | 11 | witch |
| 2 | creeper | 7 | skeleton | 12 | wolf |
| 3 | enderman | 8 | slime | 13 | zombie |
| 4 | horse | 9 | squid | 14 | spider |

### Dataset

- Formato **YOLO** (imagem + arquivo `.txt` com bounding boxes normalizados)
- **~239** imagens de treino e **~61** de validação em `trabalhofinal/datasets2/mine/`
- Configuração em [`trabalhofinal/mine.yaml`](trabalhofinal/mine.yaml)

### Pipeline

```
[Captura de tela] → [YOLOv8 best.pt] → [Bounding boxes + tracking] → [Visualização OpenCV]
```

| Arquivo | Função |
|---------|--------|
| `treino_modelo.py` | Treina o modelo a partir de `mine.yaml` (padrão: YOLOv8x, 50 epochs, GPU) |
| `capture_windows.py` | Inferência em tempo real com tracking e rastro de trajetória |
| `windowcapture.py` | Captura de região/janela via Win32 API (`win32gui` / `win32ui`) |
| `best.pt` | Melhores pesos obtidos no treinamento |
| `last.pt` | Pesos da última época |

### Dependências

```bash
pip install ultralytics opencv-python torch numpy pywin32
```

> **Nota de plataforma:** `windowcapture.py` e `capture_windows.py` dependem da API do Windows (`pywin32`). O treinamento com Ultralytics é multiplataforma.

### Treinamento

1. Ajuste os caminhos em `mine.yaml` e em `treino_modelo.py` para o ambiente local.
2. Execute:

```bash
python trabalhofinal/treino_modelo.py
```

### Inferência em tempo real

1. Ajuste o caminho do modelo (`best.pt`) e o offset de captura em `capture_windows.py`.
2. Execute:

```bash
python trabalhofinal/capture_windows.py
```

- Pressione **`q`** para encerrar.
- O tracking e o rastro de trajetória podem ser controlados pelas flags `seguir` e `deixar_rastro`.

---

## Stack tecnológica

| Tecnologia | Uso |
|------------|-----|
| **Python 3** | Linguagem principal |
| **Ultralytics YOLOv8** | Detecção de objetos e tracking |
| **PyTorch** | Backend de deep learning |
| **OpenCV** | Visualização e processamento de frames |
| **CustomTkinter / Tkinter** | Interface do detector de plágio |
| **TheFuzz** | Similaridade textual (fuzzy matching) |
| **NumPy** | Manipulação de arrays e imagens |
| **pywin32** | Captura de janela no Windows |

---

## Requisitos gerais

- Python 3.8+
- (Opcional) GPU NVIDIA com CUDA para acelerar o treinamento e a inferência do YOLO
- Windows para a captura de tela em tempo real do trabalho final

---

## Licença

Este projeto é distribuído sob a [GNU General Public License v3.0](LICENSE).

---

## Observações

- Os caminhos absolutos presentes em `treino_modelo.py`, `capture_windows.py` e `mine.yaml` apontam para o ambiente original de desenvolvimento e **precisam ser atualizados** antes de executar em outra máquina.
- Os pesos `best.pt` e `last.pt` (~84 MB cada) já estão incluídos no repositório para permitir inferência sem retreinar.
- Este material tem finalidade **educacional** e demonstra conceitos de IA clássica e de deep learning aplicados a problemas concretos.
