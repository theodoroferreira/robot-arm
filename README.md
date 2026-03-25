# Robot Arm

Simulador de braço robótico articulado com visual industrial, construído com PyGame. O robô possui uma base móvel sobre trilhos e dois segmentos rotativos com paleta de cores metálicas (aço escuro, prata e ciano/azul).

## Como executar

```bash
source venv/bin/activate
python robot_arm.py
```

## Controles

| Tecla | Ação |
|---|---|
| ← / → | Move a base para esquerda/direita |
| Q / W | Rotaciona o braço 1 (anti-horário / horário) |
| A / S | Rotaciona o braço 2 (anti-horário / horário) |

## Principais funções

Todas as funções estão em `robot_arm.py`:

| Função | Descrição |
|---|---|
| `main()` | Ponto de entrada. Inicializa o PyGame, gerencia o loop principal a 60 FPS e processa entrada do teclado. |
| `draw_ground(screen)` | Desenha o retângulo marrom do chão na parte inferior da tela. |
| `draw_base(screen, base_x)` | Desenha a base industrial com formato escalonado (plataforma + pedestal), detalhes de trilhos, parafusos e bordas com sombra/destaque. |
| `draw_arm1(screen, base_x, arm1_angle)` | Desenha o segmento 1 (prata) com formato cônico, linha de painel central, rebites e efeitos de profundidade. Retorna o ponto final `(float, float)` para encadear o braço 2. |
| `draw_arm2(screen, arm1_end, arm1_angle, arm2_angle)` | Desenha o segmento 2 (ciano/azul) com o mesmo estilo industrial do braço 1. O ângulo é relativo à orientação do braço 1. |
| `draw_joint(screen, x, y)` | Desenha uma junta mecânica em camadas: anel externo escuro, preenchimento metálico intermediário e eixo/parafuso central. |
| `draw_axes(screen, font)` | Desenha os eixos de coordenadas X (horizontal) e Y (vertical) com rótulos. |

## Arquitetura

- **Paleta metálica**: cada componente (base, braço 1, braço 2) usa uma cor primária com variantes de destaque (highlight) e sombra (shadow) para efeito 3D.
- **Rotação**: os segmentos são polígonos de 4 vértices rotacionados ao redor do pivô usando matriz de rotação 2D (`x·cos - y·sin`, `x·sin + y·cos`).
- **Encadeamento**: `draw_arm1` retorna a posição da ponta, que é usada como pivô por `draw_arm2`, permitindo cinemática direta.
- **Formato cônico**: os segmentos são mais largos no pivô e mais estreitos na ponta, criando aparência de atuador mecânico.
