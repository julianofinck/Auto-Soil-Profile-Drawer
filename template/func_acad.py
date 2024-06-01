def hatch(file, x, y, L, P="S"):
    """Adicionar hachura sob camada L e padrão P a geometria, clicando sob um ponto (x,y) de sua fronteira
    Para mudar o ângulo, chamar P = 'NOME_DO_LAYER SCALE ANGLE'"""
    x = round(float(x), 6)
    y = round(float(y), 6)
    file.write("-HATCH LA " + L + " P " + P + " S " + str(x) + "," + str(y) + "  \n")


def line(file, x1, y1, x2, y2, L="0_LINHA"):
    """Desenhar linha sob camada L de (x1,y1) até (x2,y2)"""
    set_layer(file, L)
    x1 = round(float(x1), 6)
    y1 = round(float(y1), 6)
    x2 = round(float(x2), 6)
    y2 = round(float(y2), 6)
    file.write(
        "LINE " + str(x1) + "," + str(y1) + " " + str(x2) + "," + str(y2) + " \n"
    )


def polyline(file, pontos, C="C", L="0_LINHA"):
    """Desenhar polilinha sob camada L via lista de pontos [x1,y1,x2,y2,x3,y3,...]
    Se a polilinha deve ser fechada, C = 'C'; se não, C = ''."""
    set_layer(file, L)
    file.write("PLINE ")
    for i in range(int(len(pontos) / 2)):
        file.write(
            str(round(pontos[int(0 + 2 * i)], 4))
            + ","
            + str(round(pontos[int(1 + 2 * i)], 4))
            + " "
        )
    file.write(C + "\n")


def rectangle(file, W, x1, y1, x2, y2, L="0_LINHA"):
    """Desenhar retângulo de espessura W sob camada L entre pontos (x1,y1) e (x2,y2)"""
    set_layer(file, L)
    x1 = round(float(x1), 6)
    y1 = round(float(y1), 6)
    x2 = round(float(x2), 6)
    y2 = round(float(y2), 6)
    file.write(
        "RECTANG W "
        + str(W)
        + " "
        + str(x1)
        + ","
        + str(y1)
        + " "
        + str(x2)
        + ","
        + str(y2)
        + "\n"
    )


def circle(file, x, y, R, L="0_LINHA"):
    """Desenhar círculo sob camada L de centro (x,y) e raio R"""
    set_layer(file, L)
    file.write("CIRCLE " + str(x) + "," + str(y) + " " + str(R) + "\n")


def mtext(file, x1, y1, x2, y2, texto, subtexto="", J="center", H=0.0621, R=0):
    """Adiciona caixa de texto com dimensões entre (x1,y1) e (x2,y2), podendo ter segundo texto em tamanho H = 0.05
    texto e subtexto são strings. H é o tamanho do primeiro texto. J é se é justificado. R é a rotação.
    """
    set_layer(file, "0_TEXTO")
    x1, y1 = [round(x1, 4), round(y1, 4)]
    x2, y2 = [round(x2, 4), round(y2, 4)]
    if J == "left":
        J = " \pxql;{"
    elif J == "right":
        J = " \pxqr;{"
    elif J == "center":
        J = " \pxqc;{"
    if subtexto == "":
        file.write(
            "MTEXT "
            + str(x1)
            + ","
            + str(y1)
            + " H "
            + str(H)
            + " R "
            + str(R)
            + " L A  J MC "
            + str(x2)
            + ","
            + str(y2)
            + J
            + "\H"
            + str(H)
            + ";"
            + texto
            + "}"
            + "\n\n"
        )
    else:
        file.write(
            "MTEXT "
            + str(x1)
            + ","
            + str(y1)
            + " H "
            + str(H)
            + " R "
            + str(R)
            + " L A  J MC "
            + str(x2)
            + ","
            + str(y2)
            + J
            + "\H"
            + str(H)
            + ";"
            + texto
            + "}"
            + "\P{\H0.05;"
            + subtexto
            + "}\n\n"
        )


def set_layer(file, nome):
    """Seleciona camada"""
    file.write("-LAYER S " + nome + "\n\n")


def new_layer(file, nome, color, RGB, L, LW, D):
    """Cria nova camada de tipo de linha L, espessura LW e descrição D
    color -> 'C' (preset color) ou 'C T' (true color)
    RGB   -> 1  or                 R,G,B
    """
    file.write(
        "-LAYER M "
        + nome
        + " "
        + color
        + " "
        + RGB
        + " "
        + nome
        + " L "
        + L
        + " "
        + nome
        + " LW "
        + LW
        + " "
        + nome
        + " D "
        + D
        + "\n"
        + nome
        + " plot plot "
        + nome
        + "\n\n"
    )


def new_style(file, font, H, scale):
    """Cria novo estilo"""
    file.write("-STYLE TEXTSTYLE\n" + font + "\n" + H + " 1 0 N N\n")


def new_block(file, name, bp_x, bp_y, x1, y1, x2, y2):
    """Cria novo bloco, marcando um ponto base (importante para quando for chamado).
    As geometrias que compõem o block deve estar entre (x1,y1) e (x2,y2)"""
    file.write(
        "-BLOCK "
        + name
        + " "
        + str(bp_x)
        + ","
        + str(bp_y)
        + " "
        + str(x1)
        + ","
        + str(y1)
        + " "
        + str(x2)
        + ","
        + str(y2)
        + " \n"
    )


def insert_block(file, name, bp_x, bp_y, scale_x="1", scale_y="1", rotation="0"):
    """Inserir bloco amarrando seu ponto base em (bp_x, bp_y), podendo escolher a escala x, escala y e rotação."""
    file.write(
        "-INSERT "
        + name
        + " "
        + str(bp_x)
        + ","
        + str(bp_y)
        + " "
        + str(scale_x)
        + " "
        + str(scale_y)
        + " "
        + str(rotation)
        + "\n"
    )


def zoom(file, x1, y1, x2, y2):
    """Ajustar zoom (Importante para conseguir selecionar pontos e limites)."""
    file.write("ZOOM " + str(x1) + "," + str(y1) + " " + str(x2) + "," + str(y2) + "\n")


def mspace_zoom(file, x1, y1, x2, y2):
    x1 = str(round(x1, 6))
    y1 = str(round(y1, 6))
    x2 = str(round(x2, 6))
    y2 = str(round(y2, 6))
    file.write("_.MSPACE ZOOM " + x1 + "," + y1 + " " + x2 + "," + y2 + "\n")


def psetup(file, layout, ctb="."):
    """Cria novo layout. Layout é string para o nome"""
    file.write(
        "_PLOT Yes " + layout + "\n"  # Nome do layout
        "AutoCAD PDF (General Documentation).pc3\n"  # Output device name
        + "ISO full bleed A4 (210.00 x 297.00 MM)\n"  # Paper size
        + "M\n"  # Paper units
        + "Landscape\n"  # Drawing orientation
        + "No\n"  # Plot upside down?
        + "Layout\n"  # Plot area: Display, Extents, Layout, View, Window
        + "1:1\n"  # Plot scale
        + "0,0\n"  # Plot offset
        + "Yes\n"  # Plot styles?
        + ctb
        + "\n"  # Plot style table name
        + "Yes\n"  # Plot with lineweights?
        + "No\n"  # Scale line weights with plot scale?
        + "No\n"  # Plot paperspace first?
        + "No\n"  # Hide paperspace first?
        + "No\n"  # Select file to plot
        + "Yes\n"  # Save changs to page setup?
        + "No\n"
    )  # Proceed with plot?
