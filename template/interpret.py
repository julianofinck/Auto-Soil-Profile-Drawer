"""
Purpose:  optimize the drawing of figures of boreholes
  Author: J S F
  E-Mail: @gmail.com
  Date: 11.03.2021 [Update 3rd Feb 2022]

Summary:
  1. Import libraries
  2. Functions
  3. Read files
  4. Open output .scr file
    4.1 Create layers and blocks
    4.2 Shallow and normal depth boreholes
  5. Final message


#  espaço é um enter menos poderoso; o enter sempre "finaliza" a entrada.
#  _ antes de um comando -> utilizar comando em Inglês
#  - antes de um comando -> versão em linha do comando (sem caixa de diálogo)
# Para adicionar novas cores, atualizar no "interpretar_cor" e adicionar o "new_layer"
# Para adicionar novas granulometrias, criar nova hachura em PADRAO/HATCHES e adicionar em "interpretar_granulometria"
"""

# 1. Import libraries ===================================================================
from import_libs import install_if_nonexistent
from func_print import final_message, division, section  # printing functions
from func_acad import hatch, line, polyline, rectangle, circle, \
    mtext, set_layer, new_layer, new_style, new_block, insert_block, zoom, mspace_zoom, psetup
import os
import codecs

install_if_nonexistent('pandas')
import pandas as pd
import numpy as np

install_if_nonexistent('colorama')
from colorama import Fore, Style

os.system('cls')


# 2. Functions ==========================================================================
def read_files(title_block, borehole_data, output_scr_acad, logo_png):
    abs_path = os.path.abspath(os.getcwd()) + r'\a'.replace('a', '')
    title_block = abs_path + title_block
    borehole_data = abs_path + borehole_data
    output_scr_acad = abs_path + output_scr_acad
    logo_png = abs_path + logo_png

    # Title block
    section(84, '1. Title block')
    INFO = pd.read_csv(title_block, sep=';', encoding='mbcs', header=None)
    cliente, projeto, data, escala, sist_geo = INFO.iloc[0:5, 1]
    for _ in range(len(INFO)):
        print(' ' + INFO.iloc[_, 0] + ':' + ' ' * (15 - len(INFO.iloc[_, 0])) + INFO.iloc[_, 1])

    # Borehole data
    section(84, '2. Borehole data')
    CSV = pd.read_csv(borehole_data, sep=';', encoding='mbcs', header=0, skiprows=lambda x: x in [1],
                      dtype={
                          'ID_sonda': str,
                          'ID_poco': str,
                          'Local_da_sonda': str,
                          'Lat': np.float32,
                          'Lon': np.float32,
                          'Cota': np.float32,
                          'Diam_sond': np.float32,
                          'Diam_poco': np.float32,
                          'Prof': np.float32,
                          'NA_sond': np.float32,
                          'NA_estab': np.float32,
                          'Topo_liso': np.float32,
                          'C_liso': np.float32,
                          'C_sec_filtr': np.float32,
                          'Cimento_i': np.float32,
                          'Cimento_f': np.float32,
                          'Bentonita_i': np.float32,
                          'Bentonita_f': np.float32,
                          'Prefiltro_i': np.float32,
                          'Prefiltro_f': np.float32,
                          'NA_FT01': np.float32,
                          'CH': np.float32
                      })
    CSV = CSV.dropna(axis=0, how='all')

    for _ in range(len(CSV)):
        CSV.loc[_, 'ID_sonda'] = str(CSV['ID_sonda'][_])
        CSV.loc[_, 'ID_poco'] = str(CSV['ID_poco'][_])
        CSV.loc[_, 'ID_sonda'] = '' if CSV['ID_sonda'][_] == 'nan' else CSV['ID_sonda'][_]
        CSV.loc[_, 'ID_poco'] = '' if CSV['ID_poco'][_] == 'nan' else CSV['ID_poco'][_]

    print(CSV)
    return cliente, projeto, data, escala, sist_geo, CSV, logo_png, output_scr_acad


def create_layers(file):
    # Generic colors
    new_style(file, '"Trebuchet MS"', '.0621', '1')
    new_layer(file, '0_LINHA', 'C', 'red', 'Continuous', '0.00', 'Desenhar o layout')
    new_layer(file, '0_LINHA_0.15', 'C', 'yellow', 'Continuous', '0.15', 'Limite do geomecânico')
    new_layer(file, '0_TEXTO', 'C', 'red', 'Continuous', 'default', 'Escrever texto')
    new_layer(file, '0_SOLO_GRANULOMETRIA', 'C', 'red', 'Continuous', '0.05', 'Desenhar o layout')
    new_layer(file, '0_SELO', 'C', 'cyan', 'Continuous', 'default', u'Limites no layout')
    new_layer(file, '1_ACABAMENTO', 'C T', '255,201,14', 'Continuous', 'default', 'Cor do acabamento e cap de pressão')
    new_layer(file, '1_BORRACHA', 'C T', '99,100,102', 'Continuous', 'default', 'Cor da borracha')
    new_layer(file, '1_BRANCO', 'C T', '255,255,255', 'Continuous', 'default', 'Cor branca para espaço vazio')
    new_layer(file, u'"SÍMBOLO_NÍVEL ÁGUA"', 'C', '152', 'Continuous', 'default', u'Nível da água')
    new_layer(file, u'"SÍMBOLO_COLETA AMOSTRA"', 'C T', '240,0,0', 'Continuous', 'default', 'Marcador da profundidade de coleta da amostra')
    new_layer(file, u'"H_CIMENTO"', 'C', '253', 'Continuous', 'default', 'Cor do cimento')
    new_layer(file, u'"H_BENTONITA"', 'C', '23', 'Continuous', 'default', 'Cor da bentonita')
    new_layer(file, u'"H_PRE_FILTRO"', 'C T', '255,223,127', 'Continuous', 'default', u'Cor do pré-filtro')

    # Soil colors
    new_layer(file, u'"SC_AMARELO"', 'C T', '255,223,127', 'Continuous', 'default', u'Cor do solo')
    new_layer(file, u'"SC_AMARELO_ESCURO (Ocre)"', 'C T', '219,186,57', 'Continuous', 'default', u'Cor do solo')
    new_layer(file, u'"SC_AREIA_DE_FORRAÇÃO"', 'C T', '243,229,210', 'Continuous', 'default', u'Cor do solo')
    new_layer(file, u'"SC_ASFALTO"', 'C T', '40,40,40', 'Continuous', 'default', u'Cor do asfalto')
    new_layer(file, u'"SC_BEGE"', 'C T', '244,230,189', 'Continuous', 'default', u'Cor do solo')
    new_layer(file, u'"SC_BRANCA"', 'C T', '254,255,255', 'Continuous', 'default', u'Cor do solo')
    new_layer(file, u'"SC_CINZA"', 'C T', '105,105,105', 'Continuous', 'default', u'Cor do solo')
    new_layer(file, u'"SC_CINZA_CLARO"', 'C T', '192,192,192', 'Continuous', 'default', u'Cor do solo')
    new_layer(file, u'"SC_CINZA_ESCURO"', 'C T', '55,55,55', 'Continuous', 'default', u'Cor do solo')
    new_layer(file, u'"SC_CINZA_ESVERDEADO"', 'C T', '118,137,109', 'Continuous', 'default', u'Cor do solo')
    new_layer(file, u'"SC_CONCRETO"', 'C T', '231,231,231', 'Continuous', 'default', u'Cor do concreto')
    new_layer(file, u'"SC_GRAMADO"', 'C T', '0,255,0', 'Continuous', 'default', u'Cor do gramado')
    new_layer(file, u'"SC_GRAMADO_PF"', 'C T', '19,103,52', 'Continuous', 'default', u'Cor do plano de fundo do gramado')
    new_layer(file, u'"SC_MARROM"', 'C T', '76,57,38', 'Continuous', 'default', u'Cor do solo')
    new_layer(file, u'"SC_MARROM_AVERMELHADO"', 'C T', '132,41,0', 'Continuous', 'default', u'Cor do solo')
    new_layer(file, u'"SC_MARROM_ALARANJADO"', 'C T', '175,92,10', 'Continuous', 'default', u'Cor do solo')
    new_layer(file, u'"SC_MARROM_CLARO"', 'C T', '165,124,82', 'Continuous', 'default', u'Cor do solo')
    new_layer(file, u'"SC_MARROM_ESCURO"', 'C T', '76,38,38', 'Continuous', 'default', u'Cor do solo')
    new_layer(file, u'"SC_MARROM_AMARELADO"', 'C T', '169,143,56', 'Continuous', 'default', u'Cor do solo')
    new_layer(file, u'"SC_PRETO"', 'C T', '40,15,16', 'Continuous', 'default', u'Cor do solo')
    new_layer(file, u'"SC_ROXO"', 'C T', '76,53,89', 'Continuous', 'default', u'Cor do solo')
    new_layer(file, u'"SC_VERDE"', 'C T', '69,107,59', 'Continuous', 'default', u'Cor do solo')
    new_layer(file, u'"SC_VERMELHO"', 'C T', '252,70,62', 'Continuous', 'default', u'Cor do solo')
    new_layer(file, u'"SC_VERMELHO_CLARO"', 'C T', '252,140,125', 'Continuous', 'default', u'Cor do solo')
    new_layer(file, u'"SC_VERMELHO_ESCURO"', 'C T', '252,14,3', 'Continuous', 'default', u'Cor do solo')


def create_blocks(file):
    zoom(file, -2, -2, 2, 2)
    L = u'"SÍMBOLO_NÍVEL ÁGUA"'
    line(file, 0, 0, .1375, 0, L=L)
    line(file, 0, 0, .075, 0, L=L)
    line(file, .0094, -.0188, .0656, -.0188, L=L)
    line(file, .0187, -.0375, .0562, -.0375, L=L)
    pontos = [0, 0.075, 0.075, 0.075, 0.0375, 0]
    polyline(file, pontos, 'C', L)
    hatch(file, 0.0375, 0.0, L=L, P='S CO ByLayer .')
    new_block(file, 'NA_ESTAB', 0.1375, 0, 1, 1, -1, -1)

    L = u'"SÍMBOLO_NÍVEL ÁGUA"'
    line(file, 0, 0, .1375, 0, L=L)
    line(file, 0, 0, .075, 0, L=L)
    line(file, .0094, -.0188, .0656, -.0188, L=L)
    line(file, .0187, -.0375, .0562, -.0375, L=L)
    pontos = [0, 0.075, 0.075, 0.075, 0.0375, 0]
    polyline(file, pontos, 'C', L)
    new_block(file, 'NA_SONDA', 0.1375, 0, 1, 1, -1, -1)

    L = u'"SÍMBOLO_COLETA AMOSTRA"'
    line(file, 0, 0, 0.1071, 0, L=L)
    circle(file, 0, 0, 0.0375, L=L)
    hatch(file, -0.0375, 0, L=L, P='S')
    new_block(file, 'CA', 0.1071, 0, 1, 1, -1, -1)


def validate(CSV, n_p):
    if np.isnan(CSV['Topo_liso'][n_p]) and np.isnan(CSV['C_liso'][n_p]) and np.isnan(CSV['C_sec_filtr'][n_p]):
        existe_poco = 0
    else:
        existe_poco = 1
        # CONSISTIR PROFUNDIDADE DE SONDAGEM E POÇO
        if float(CSV['Prof'][n_p]) < round(float(CSV['Topo_liso'][n_p]) + float(CSV['C_liso'][n_p]) + float(CSV['C_sec_filtr'][n_p]), 4):
            lim = 60
            MSG = ('\n\t' + Style.BRIGHT + Fore.RED + '  # Erro na sondagem ' + CSV['ID_sonda'][n_p] + '! #')
            MSG += (lim - len(MSG) + 9) * ' ' + '\n\t'
            msg = '  Inconsistencia! O poco esta passando a base da sondagem!'
            MSG += msg + (lim - len(msg)) * ' ' + '\n\t'
            msg = '  Profundidade de sondagem:     ' + str(CSV['Prof'][n_p])
            MSG += msg + (lim - len(msg)) * ' ' + '\n\t'
            msg = '  Topo liso: ' + '                   ' + str(CSV['Topo_liso'][n_p])
            MSG += msg + (lim - len(msg)) * ' ' + '\n\t'
            msg = '  Comprimento liso:             ' + str(CSV['C_liso'][n_p])
            MSG += msg + (lim - len(msg)) * ' ' + '\n\t'
            msg = '  Comprimento secao filtrante:  ' + str(CSV['C_sec_filtr'][n_p])
            MSG += msg + (lim - len(msg)) * ' ' + '\n\n\t' + Style.RESET_ALL + Fore.RESET
            raise SyntaxError(MSG)
    return existe_poco


def cabecalho(file, CSV, n_p, existe_poco, i_layout, x, y, prof, VOC_dist, sist_geo):
    VOC = CSV['VOC'][n_p]
    ID_sonda = CSV['ID_sonda'][n_p]
    ID_poco = CSV['ID_poco'][n_p]
    Local_da_sonda = CSV['Local_da_sonda'][n_p]
    Lat = CSV['Lat'][n_p]
    Lon = CSV['Lon'][n_p]
    Cota = CSV['Cota'][n_p]
    Prof_coleta = CSV['Prof_coleta'][n_p]
    NA_sond = CSV['NA_sond'][n_p]
    NA_estab = CSV['NA_estab'][n_p]
    Diam_sond = CSV['Diam_sond'][n_p]
    Diam_poco = CSV['Diam_poco'][n_p]

    zoom(file, x - 1, y - 1, x + 6, y + prof + 2)
    rectangle(file, 0, x, y, x + 5, y + prof + 0.42)  # BORDAS DO PERFIL

    # Soil profile ruler starts 0.2m above ground (Major 0.5; Minor 0.1)
    line(file, x + .3, 0, x + .3, prof)  # VOC vertical line
    voc = VOC.split(',')  # VOC as list
    z = 0.2
    while z > -prof:
        # Ruler
        if round(z % 0.5, 1) == 0:
            mtext(file, x, y + z + prof, x + 0.25, y + z + prof, "{:.1f}".format(z).replace('.', ',').replace('-', ''))
            line(file, x + 0.20, z + prof + y, x + 0.30, z + prof + y)
        else:
            line(file, x + 0.25, z + prof + y, x + 0.30, z + prof + y)
        # VOC
        if z < 0 and round((10*z) % (10*VOC_dist), 1)/10 == 0:
            try:
                string = str(voc[0])
                if string != '':
                    if string[0] == '.':
                        string = '0' + string
                    if string.count('.') == 0:
                        string += '.0'
                if string in ['-999.0', '', '-']:
                    string = ''
                mtext(file, x + .3, y + z + prof, x + .3 + .3, y + z + prof, string.replace('.', ','))
                voc.pop(0)
            except:
                pass
        z = round(z - .1, 1)

    # Identification
    if existe_poco > 0:
        if ID_sonda != '':
            texto = '  ' + str(ID_sonda) + ' / ' + str(ID_poco)
        else:
            texto = '  ' + str(ID_poco)
    else:
        texto = '  ' + str(ID_sonda)
    X = x
    if i_layout < 3:
        mtext(file, X, y + prof + .42 + 7.3, X + 5, y + prof + .42 + .3 + 3.3, texto.replace('/', '\n'), subtexto='', J='center', H=0.9, R=0)
    else:
        mtext(file, X, y + prof + .42 - 10, X + 5, y + prof + .42 + .3 - 8, texto.replace('/', '\n'), subtexto='', J='center', H=0.9, R=0)
    mtext(file, X, y + prof + .42 + .3, X + 5, y + prof + .42 + .3 + .3, texto, H=.1056, J='left')
    rectangle(file, .02, X, y + prof + .42 + .3, X + 5, y + prof + .42 + .3 + .3)
    try:
        LAT = str(Lat).replace(',', '')
        LAT = "{:.2f}".format(round(float(LAT), 2))
        LAT = LAT.replace('.', ',')
    except:
        LAT = '-'
    try:
        LON = str(Lon).replace(',', '')
        LON = "{:.2f}".format(round(float(LON), 2))
        LON = LON.replace('.', ',')
    except:
        LON = '-'
    try:
        COTA = str(Cota).replace(',', '')
        COTA = "{:.2f}".format(round(float(COTA), 2))
        COTA = COTA.replace('.', ',')
    except:
        COTA = '-'

    # LAT LON COTA
    texto = 'LATITUDE: ' + LAT + ' | LONGITUDE: ' + LON + ' | COTA: ' + COTA
    mtext(file, X + 2.1, y + prof + .42 + .3, X + 4.975, y + prof + .42 + .3 + .3, texto, H=.0621, J='right')

    # SISTEMA DE COORDENADAS
    texto = sist_geo
    mtext(file, X, y + prof + .42 + .3, X + 4.975, y + prof + .42 + .3 + .1, texto, H=.0421, J='right')

    # PROF. (METROS)
    texto, subtexto = ['PROF.', '(metro)']
    mtext(file, X, y + prof + .42, X + .3, y + prof + 0.42 + 0.3, texto, subtexto)
    rectangle(file, .02, X, y + prof + .42, X + .3, y + prof + .42 + .3)

    # VOC
    X += .3
    texto, subtexto = ['VOC', '(ppm)']
    mtext(file, X, y + prof + .42, X + .3, y + prof + 0.42 + 0.3, texto, subtexto)
    rectangle(file, .02, X, y + prof + .42, X + .3, y + prof + .42 + .3)
    line(file, X, y, X, y + prof + .42)

    # AMOSTRA
    X += .3
    texto = 'AMOS.'
    mtext(file, X, y + prof + .42, X + .3, y + prof + 0.42 + 0.3, texto)
    rectangle(file, .02, X, y + prof + .42, X + .3, y + prof + .42 + .3)
    line(file, X, y, X, y + prof + .42)

    try:
        insert_block(file, 'CA', X + .3, prof - float(Prof_coleta) + y)
    except:
        try:
            Prof_coletas = Prof_coleta[1:-1].split(',')
            for i in Prof_coletas:
                insert_block(file, 'CA', X + .3, prof - float(i) + y)
        except:
            pass

    # NÍVEL ÁGUA
    X += .3
    texto = u'NÍVEL\nAGUA'
    mtext(file, X, y + prof + .42, X + .3, y + prof + 0.42 + 0.3, texto)
    rectangle(file, .02, X, y + prof + .42, X + .3, y + prof + .42 + .3)
    line(file, X, y, X, y + prof + .42)
    line(file, X + .15, y, X + .15, y + prof + .42)

    # NA Sondagem
    texto = u'SONDAGEM'
    mtext(file, X + .15 / 3, y + prof, X + .15, y + prof + 0.4, texto, R=90, H=0.045, J="right")
    if not np.isnan(NA_sond): insert_block(file, 'NA_SONDA', X + .15, prof - float(NA_sond) + y)

    # NA Estabilizado
    texto = u'ESTABILIZADO'
    mtext(file, X + .15 * 4 / 3, y + prof, X + .3, y + prof + 0.4, texto, R=90, H=0.045, J="right")
    if not np.isnan(NA_estab): insert_block(file, 'NA_ESTAB', X + .30, prof - float(NA_estab) + y)

    # PERFIL DO POÇO
    X += .3
    texto = u'PERFIL DO POÇO'
    mtext(file, X, y + prof + .42, X + .9, y + prof + 0.42 + 0.3, texto)
    rectangle(file, .02, X, y + prof + .42, X + .9, y + prof + .42 + .3)
    line(file, X, y, X, y + prof + .42)

    # LOCAL DA SONDAGEM
    X += .9

    if isinstance(Local_da_sonda, str):
        texto = u'  LOCAL DA SONDAGEM: ' + str(Local_da_sonda)
    else:
        texto = u'  LOCAL DA SONDAGEM: -'
    if len(texto) < 65:
        mtext(file, X, y + prof + .42 + .15, X + 2.9, y + prof + 0.42 + 0.3, texto, '', 'left', H=.0621)
    elif len(texto) < 75:
        mtext(file, X, y + prof + .42 + .15, X + 2.9, y + prof + 0.42 + 0.3, texto, '', 'left', H=.0521)
    else:
        mtext(file, X, y + prof + .42 + .15, X + 2.9, y + prof + 0.42 + 0.3, texto, '', 'left', H=.0421)
    rectangle(file, .02, X, y + prof + .42 + .15, X + 2.9, y + prof + .42 + .3)
    line(file, X, y, X, y + prof + .42)

    # DIÂMETRO DA SONDAGEM
    if np.isnan(Diam_sond):
        texto = u'  DIÂMETRO DA SONDAGEM: -'
    else:
        texto = u'  DIÂMETRO DA SONDAGEM: ' + str(Diam_sond).replace('.', ',') + "''"
    mtext(file, X, y + prof + .42, X + 1.45, y + prof + 0.42 + 0.15, texto, '', 'left')
    rectangle(file, .02, X, y + prof + .42, X + 1.45, y + prof + .42 + .15)

    # DIÂMETRO DO POÇO
    if np.isnan(Diam_poco):
        texto = u'  DIÂMETRO DO POÇO: -'
    else:
        texto = u'  DIÂMETRO DO POÇO: ' + str(Diam_poco).replace('.', ',') + "''"
    X += 1.45
    mtext(file, X, y + prof + .42, X + 1.45, y + prof + 0.42 + 0.15, texto, '', 'left')
    rectangle(file, .02, X, y + prof + .42, X + 1.45, y + prof + .42 + .15)

    # SOLO NÍVEL 0
    if existe_poco == 1:
        rectangle(file, 0, x + .3, y + prof, x + 1.2 + .15 + .17, y + prof - 0.015)
        hatch(file, x + .6, y + prof, '0_LINHA', P='ANSI31 0.005 0 0')
        rectangle(file, 0, x + 2.1 - .15 - .17, y + prof, x + .3 + 4.7, y + prof - 0.015)
        hatch(file, x + 2.1, y + prof, '0_LINHA', P='ANSI31 0.005 0 0')
    else:
        rectangle(file, 0, x + .3, y + prof, x + 5, y + prof + 0.013)
        hatch(file, x + .6, y + prof, '0_LINHA', P='ANSI31 0.005 0 0')
    try:
        D = Diam_poco
        return D
    except:
        pass


def perfil_pedologico(file, n_p, x, y, D, Pedologia, prof, existe_poco):
    def solo(file, x, y, y1, y2, Diam_poco, string, existe_poco):
        """Para cada horizonte do solo, desenhar dois retângulos (esquerda e direita) ao redor do poço,
         e uma polyline na direita com a descrição do horizonte (string) num mtext"""
        if existe_poco == 1:
            rectangle(file, 0, x + 1.2, y1 + y, x + 1.65 - .05 * Diam_poco / 2 - .1, y2 + y, L='0_LINHA')
            rectangle(file, 0, x + 2.1, y1 + y, x + 1.65 + .05 * Diam_poco / 2 + .1, y2 + y, L='0_LINHA')
        else:
            rectangle(file, 0, x + 1.2, y1 + y, x + 2.1, y2 + y, L='0_LINHA')
        # DESCRICAO
        if abs(y2 - y1) < 0.06:
            pontos = [x + 2.1, y1 + y,
                      x + 5, y1 + y,
                      x + 5, y2 + y,
                      x + 4.8, y2 + y,
                      x + 4.8, y2 - .05 + y,
                      x + 2.3, y2 - .05 + y,
                      x + 2.3, y2 + y,
                      x + 2.1, y2 + y]
        else:
            pontos = [x + 2.1, y1 + y,
                      x + 5, y1 + y,
                      x + 5, y2 + y,
                      x + 2.1, y2 + y]
        polyline(file, pontos, C='C', L='0_LINHA')
        gap = (5 - 2.1)
        mtext(file, x + 2.1 + .02 * gap, y1 + y, x + 5 - .02 * gap, y2 + y, string, H=.071, R=0)

    # 90
    def interpretar_cor(file, x, y, y2, description, existe_poco):
        """Baseado na descrição do solo e em se há ou não poço, interpretar cor comparando com o banco de dados de cores.
        y2 é a base do horizonte"""

        def add_color(file, name, existe_poco, x, y, y2):
            hatch(file, x + 1.4, y2 + y, name, P='S')
            if existe_poco == 1: hatch(file, x + 2.0, y2 + y, name, P='S')
            i = len(description)
            return i

        description = description.split(' ')
        i = 0
        while i < len(description):
            if description[i] in ["AMARELO", "AMARELA"]:
                if len(description) - 1 > i:
                    if description[i + 1] in ["ESCURO", "ESCURA"]:
                        i = add_color(file, '"SC_AMARELO_ESCURO (Ocre)"', existe_poco, x, y, y2)
                    else:
                        i = add_color(file, '"SC_AMARELO"', existe_poco, x, y, y2)
                else:
                    i = add_color(file, '"SC_AMARELO"', existe_poco, x, y, y2)
            elif description[i] in ('ASFALTO', 'ASFALTICO', 'ASFÁLTICO', 'ASFALTO'):
                i = add_color(file, '"SC_ASFALTO"', existe_poco, x, y, y2)
            elif description[i] in ["BEGE"]:
                i = add_color(file, '"SC_BEGE"', existe_poco, x, y, y2)
            elif description[i] in ["BRANCA", "BRANCO"]:
                i = add_color(file, '"SC_BRANCA"', existe_poco, x, y, y2)
            elif description[i] in ["CINZA"]:
                if len(description) - 1 > i:
                    if description[i + 1] in ["CLARO", "CLARA"]:
                        i = add_color(file, '"SC_CINZA_CLARO"', existe_poco, x, y, y2)
                    elif description[i + 1] in ["ESCURO", "ESCURA"]:
                        i = add_color(file, '"SC_CINZA_ESCURO"', existe_poco, x, y, y2)
                    elif description[i + 1] in ["ESVERDEADA", "ESVERDEADO"]:
                        i = add_color(file, '"SC_CINZA_ESVERDEADO"', existe_poco, x, y, y2)
                    else:
                        i = add_color(file, '"SC_CINZA"', existe_poco, x, y, y2)
                else:
                    i = add_color(file, '"SC_CINZA"', existe_poco, x, y, y2)
            elif description[i] in ('CONCRETO', 'CONCRETICO', 'CONCRÉTICO', '(CONCRETO)'):
                i = add_color(file, '"SC_CONCRETO"', existe_poco, x, y, y2)
            elif description[i] in ('GRAMADO', 'GRAMA', 'MATO', 'RASTEIRO', 'RASTEIRA'):
                hatch(file, x + 1.4, y2 + y, 'SC_GRAMADO_PF', P='S')
                hatch(file, x + 1.4, y2 + y, 'SC_GRAMADO', P='GRAMADO 1 0')
                if existe_poco == 1:
                    hatch(file, x + 2, y2 + y, 'SC_GRAMADO_PF', P='S')
                    hatch(file, x + 2, y2 + y, 'SC_GRAMADO', P='GRAMADO 1 0')
                i = len(description)
            elif description[i] in ["OCRE"]:
                i = add_color(file, '"SC_AMARELO_ESCURO (Ocre)"', existe_poco, x, y, y2)
            elif description[i] in ["MARROM"]:
                if len(description) - 1 > i:
                    if description[i + 1] in ["CLARO", "CLARA"]:
                        i = add_color(file, '"SC_MARROM_CLARO"', existe_poco, x, y, y2)
                    elif description[i + 1] in ["ESCURO", "ESCURA"]:
                        i = add_color(file, '"SC_MARROM_ESCURO"', existe_poco, x, y, y2)
                    elif description[i + 1] in ["AVERMELHADA", "AVERMELHADO"]:
                        i = add_color(file, '"SC_MARROM_AVERMELHADO"', existe_poco, x, y, y2)
                    elif description[i + 1] in ["ALARANJADA", "ALARANJADO"]:
                        i = add_color(file, '"SC_MARROM_ALARANJADO"', existe_poco, x, y, y2)
                    elif description[i + 1] in ["AMARELADA", "AMARELADO"]:
                        i = add_color(file, '"SC_MARROM_AMARELADO"', existe_poco, x, y, y2)
                    else:
                        i = add_color(file, '"SC_MARROM"', existe_poco, x, y, y2)
                else:
                    i = add_color(file, '"SC_MARROM"', existe_poco, x, y, y2)
            elif description[i] in ["PRETO", "PRETA"]:
                i = add_color(file, '"SC_PRETO"', existe_poco, x, y, y2)
            elif description[i] in ["ROXO", "ROXA"]:
                i = add_color(file, '"SC_ROXO"', existe_poco, x, y, y2)
            elif description[i] in ["VERDE"]:
                i = add_color(file, '"SC_VERDE"', existe_poco, x, y, y2)
            elif description[i] in ["VERMELHO", "VERMELHA"]:
                if len(description) - 1 > i:
                    if description[i + 1] in ["CLARO", "CLARA"]:
                        i = add_color(file, '"SC_VERMELHO_CLARO"', existe_poco, x, y, y2)
                    elif description[i + 1] in ["ESCURO", "ESCURA"]:
                        i = add_color(file, '"SC_VERMELHO_ESCURO"', existe_poco, x, y, y2)
                    elif description[i + 1] in ["ACINZENTADO", "ACINZENTADA"]:
                        i = add_color(file, '"SC_VERMELHO_ACINZENTADO"', existe_poco, x, y, y2)
                    else:
                        i = add_color(file, '"SC_VERMELHO"', existe_poco, x, y, y2)
                else:
                    i = add_color(file, '"SC_VERMELHO"', existe_poco, x, y, y2)
            else:
                i += 1

    # 140
    def interpretar_granulometria(file, x, y, y2, descricao, existe_poco):
        """Baseado na descrição do solo e em se há ou não poço, interpretar a granulometria comparando com o banco de granu-
        metrias que temos.
        y2 é a base do horizonte"""

        def add_grain(file, existe_poco, x, y, y2, layer, pattern):
            hatch(file, x + 1.4, y2 + y, layer, P=pattern)
            if existe_poco == 1: hatch(file, x + 2.0, y2 + y, layer, P=pattern)

        # todo AREIA - (GROSSA, MÉDIA, FINA, DE FORRAÇÃO)
        descricao = descricao.split(' ')
        layer = '0_SOLO_GRANULOMETRIA'
        i = 0
        while i < len(descricao):
            if descricao[i] in ["AREIA", "ARENO", "ARENOSA", "ARENOSO"]:  # AREIA
                if len(descricao) - 1 > i:
                    while descricao[i + 1] in ['MUITO', 'POUCO', 'FINA', 'A', 'MÉDIA', 'MEDIA', 'GROSSA']:
                        i += 1
                    if descricao[i + 1] in ["SILTOSO", "SILTOSA", "SILTE", "SILTO"]:  # AREIA SILTE
                        if len(descricao) - 2 > i:
                            if descricao[i + 2] in ["ARGILOSA", "ARGILA"]:  # AREIA SILTE ARGILA
                                add_grain(file, existe_poco, x, y, y2, layer, '2areia+silte+argila 1 0')
                            else:  # AREIA SILTE
                                add_grain(file, existe_poco, x, y, y2, layer, '1areia+silte 1 0')
                        else:  # AREIA SILTE
                            add_grain(file, existe_poco, x, y, y2, layer, '1areia+silte 1 0')
                    elif descricao[i + 1] in ["ARGILOSA", "ARGILA"]:  # AREIA ARGILA
                        if len(descricao) - 2 > i:
                            if descricao[i + 2] in ["SILTOSA", "SILTE", "SILTO"]:  # AREIA ARGILA SILTE
                                add_grain(file, existe_poco, x, y, y2, layer, '2areia+silte+argila 1 0')
                            else:  # AREIA ARGILA
                                add_grain(file, existe_poco, x, y, y2, layer, '1areia+argila 1 0')
                        else:  # AREIA ARGILA
                            add_grain(file, existe_poco, x, y, y2, layer, '1areia+argila 1 0')
                    elif descricao[i + 1] in ["DE", "FORRAÇÃO"]:  # AREIA ARGILA
                        add_grain(file, existe_poco, x, y, y2, 'SC_AREIA_DE_FORRAÇÃO', 'S')
                        add_grain(file, existe_poco, x, y, y2, layer, '0areia 1 0')
                    else:  # AREIA (ou de forração)
                        add_grain(file, existe_poco, x, y, y2, layer, '0areia 1 0')
                else:  # AREIA (ou de forração)
                    add_grain(file, existe_poco, x, y, y2, layer, '0areia 1 0')
                i = len(descricao)  # Stop while constructor
            elif descricao[i] in ["SILTE", "SILTO", "SILTOSO", "SILTOSA"]:  # SILTE
                if len(descricao) - 1 > i:
                    if descricao[i + 1] in ["ARGILOSO", "ARGILA", "ARGILO"]:  # SILTE	ARGILA
                        if len(descricao) - 2 > i:
                            if descricao[i + 2] in ["ARENOSO", "AREIA"]:  # SILTE ARGILA AREIA
                                add_grain(file, existe_poco, x, y, y2, layer, '2areia+silte+argila 1 0')
                            else:  # SILTE ARGILA
                                add_grain(file, existe_poco, x, y, y2, layer, '1silte+argila 1 0')
                        else:  # SILTE ARGILA
                            add_grain(file, existe_poco, x, y, y2, layer, '1silte+argila 1 0')
                    elif descricao[i + 1] in ["ARENOSO", "AREIA"]:  # SILTE AREIA
                        while descricao[i + 1] in ['MUITO', 'POUCO', 'FINA', 'A', 'MÉDIA', 'MEDIA', 'GROSSA']:
                            i += 1
                        if len(descricao) - 2 > i:
                            if descricao[i + 2] in ["ARGILOSO", "ARGILA", "ARGILO"]:  # SILTE AREIA ARGILA
                                add_grain(file, existe_poco, x, y, y2, layer, '2areia+silte+argila 1 0')
                            else:  # SILTE AREIA
                                add_grain(file, existe_poco, x, y, y2, layer, '1areia+silte 1 0')
                        else:  # SILTE AREIA
                            add_grain(file, existe_poco, x, y, y2, layer, '1areia+silte 1 0')
                    else:  # SILTE
                        add_grain(file, existe_poco, x, y, y2, layer, '0silte 1 0')
                else:  # SILTE
                    add_grain(file, existe_poco, x, y, y2, layer, '0silte 1 0')
                i = len(descricao)  # Stop while constructor
            elif descricao[i] in ["ARGILA", "ARGILOSO", "ARGILOSA", "ARGILO"]:  # ARGILA
                if len(descricao) - 1 > i:
                    if descricao[i + 1] in ["SILTOSO", "SILTOSA", "SILTE", "SILTO"]:  # ARGILA SILTE
                        if len(descricao) - 2 > i:
                            if descricao[i + 2] in ["ARENOSA", "AREIA", "ARENO"]:  # ARGILA SILTE AREIA
                                add_grain(file, existe_poco, x, y, y2, layer, '2areia+silte+argila 1 0')
                            else:  # ARGILA SILTE
                                add_grain(file, existe_poco, x, y, y2, layer, '1silte+argila 1 0')
                        else:  # ARGILA SILTE
                            add_grain(file, existe_poco, x, y, y2, layer, '1silte+argila 1 ')
                    elif descricao[i + 1] in ["ARENOSA", "AREIA", "ARENO"]:  # ARGILA AREIA
                        while descricao[i + 1] in ['MUITO', 'POUCO', 'FINA', 'A', 'MÉDIA', 'MEDIA', 'GROSSA']:
                            i += 1
                        if len(descricao) - 2 > i:
                            if descricao[i + 2] in ["SILTOSA", "SILTE", "SILTO"]:  # ARGILA AREIA SILTE
                                add_grain(file, existe_poco, x, y, y2, layer, '2areia+silte+argila 1 0')
                            else:  # ARGILA AREIA
                                add_grain(file, existe_poco, x, y, y2, layer, '1areia+argila 1 0')
                        else:  # ARGILA AREIA
                            add_grain(file, existe_poco, x, y, y2, layer, '1silte+argila 1 0')
                    else:  # ARGILA
                        add_grain(file, existe_poco, x, y, y2, layer, '0argila 1 0')
                else:  # ARGILA
                    add_grain(file, existe_poco, x, y, y2, layer, '0argila 1 0')
                i = len(descricao)  # Stop while constructor
            elif descricao[i] in ["BLOCO"]:  # BLOCO
                if len(descricao) - 1 > i:
                    if descricao[i + 1] in ["DE"]:  # BLOCO DE
                        if len(descricao) - 2 > i:
                            if descricao[i + 2] in ["ROCHA"]:  # BLOCO DE ROCHA
                                add_grain(file, existe_poco, x, y, y2, layer, 'bloco_de_rocha 1 0')
                i = len(descricao)  # Stop while constructor
            elif descricao[i] in ["MATACÃO", "PEDRA", "PEDRAS"]:  # MATACÃO
                add_grain(file, existe_poco, x, y, y2, layer, 'matacao 1 0')
                i = len(descricao)  # Stop while constructor
            elif descricao[i] in ["PARALELEPÍPEDO"]:  # PARALELEPÍPEDO
                add_grain(file, existe_poco, x, y, y2, layer, 'paralelepipedo 1 0')
                i = len(descricao)  # Stop while constructor
            elif descricao[i] in ["RESÍDUOS"]:  # RESÍDUOS
                add_grain(file, existe_poco, x, y, y2, layer, 'residuos 1 30')
                i = len(descricao)  # Stop while constructor
            elif descricao[i] in ["SAIBRO"]:  # SAIBRO
                add_grain(file, existe_poco, x, y, y2, layer, 'saibro 1 0')
                i = len(descricao)  # Stop while constructor
            elif descricao[i] in ["SEIXO"]:  # SEIXO
                add_grain(file, existe_poco, x, y, y2, layer, 'seixo 1 0')
                i = len(descricao)  # Stop while constructor
            elif descricao[i] in ["SEXTANADO"]:  # SEXTANADO
                add_grain(file, existe_poco, x, y, y2, layer, 'sextanado 1 0')
                i = len(descricao)  # Stop while constructor
            elif descricao[i] in ["ATERRO"]:  # ATERRO
                add_grain(file, existe_poco, x, y, y2, layer, 'aterro 1 0')
                i = len(descricao)  # Stop while constructor
            elif descricao[i] in ["BRITA", "BRITAS"]:  # BRITA
                add_grain(file, existe_poco, x, y, y2, layer, 'brita 1 0')
                i = len(descricao)  # Stop while constructor
            elif descricao[i] in ["RACHÃO"]:  # RACHÃO
                add_grain(file, existe_poco, x, y, y2, layer, 'brita 2.5 0')
                i = len(descricao)  # Stop while constructor
            elif descricao[i] in ["PEDREGULHO", "CASCALHO", "PEDREGULHOS"]:  # PEDREGULHO
                add_grain(file, existe_poco, x, y, y2, layer, 'pedregulho 1 30')
                i = len(descricao)  # Stop while constructor
            elif descricao[i] in ["BLOQUETE"]:  # BLOQUETE
                add_grain(file, existe_poco, x, y, y2, layer, 'bloquete 1 0')
                i = len(descricao)  # Stop while constructor
            else:
                i += 1

    pedo = Pedologia[n_p][2:-2].split(',')
    try:
        y1 = prof
        for i in range(len(pedo[0::2])):  # while estiver subindo pega y1 = 0 (primeiro) depois y1=y2
            y2 = round(prof - float(pedo[0::2][i]), 4)
            descricao = pedo[1::2][i]
            # Linha do poço
            solo(file, x, y, y1, y2, D, descricao, existe_poco)
            interpretar_cor(file, x, y, y2, descricao, existe_poco)
            interpretar_granulometria(file, x, y, y2, descricao, existe_poco)
            y1 = y2
    except:
        lim = 85
        MSG = '\n\t\033[1;41m  # Erro no ' + str(n_p + 1) + 'o Poco! #'
        MSG += (lim - len(MSG)) * ' ' + '\033[40m'
        msg = '\n\t\033[1;41m  Deve ter faltado uma virgula entre um horizonte do solo e sua descricao.'
        MSG += msg + (lim - len(msg)) * ' ' + '\t\033[40m'
        raise SyntaxError(MSG)


def adicionar_poco(file, CSV, n_p, prof, x, y, existe_poco):
    D = CSV['Diam_poco'][n_p]
    B_i = CSV['Bentonita_i'][n_p]
    B_f = CSV['Bentonita_f'][n_p]
    C_i = CSV['Cimento_i'][n_p]
    C_f = CSV['Cimento_f'][n_p]
    T_l = CSV['Topo_liso'][n_p]
    C_l = CSV['C_liso'][n_p]
    C_sf = CSV['C_sec_filtr'][n_p]
    Pre_i = CSV['Prefiltro_i'][n_p]
    Pre_f = CSV['Prefiltro_f'][n_p]
    CxConc = CSV['Cx_conc'][n_p] / 100
    CamCalc = CSV['Cam_calc'][n_p]
    PescComp = CSV['Pesc_comp'][n_p] / 100

    if np.isnan(CxConc):
        CxConc = 0
    if np.isnan(PescComp):
        PescComp = 0

    if existe_poco == 0:
        pass
    else:
        # PREENCHIMENTO ------------------------------------------------------------------------------------------------
        ## PRE_FILTRO
        comp_poco = T_l + C_l + C_sf
        if Pre_f > comp_poco:  # Caso em que o poço vai até o fim da sondagem
            pontos = [x + 1.65 - .025 * D, prof - Pre_i + y,
                      x + 1.65 - .025 * D - .1, prof - Pre_i + y,
                      x + 1.65 - .025 * D - .1, prof - Pre_f + y,
                      x + 1.65 + .025 * D + .1, prof - Pre_f + y,
                      x + 1.65 + .025 * D + .1, prof - Pre_i + y,
                      x + 1.65 + .025 * D, prof - Pre_i + y,
                      x + 1.65 + .025 * D, prof - comp_poco + y,
                      x + 1.65 - .025 * D, prof - comp_poco + y]
            polyline(file, pontos, C='C')
            hatch(file, x + 1.65 - .025 * D - .05, prof - Pre_i + y, 'H_PRE_FILTRO', P='S')
            hatch(file, x + 1.65 - .025 * D - .05, prof - Pre_i + y, '0_SOLO_GRANULOMETRIA', P='AR-SAND 0.0008 0')
        else:  # Caso em que o poço não vai até o fim da sondagem
            pontos = [x + 1.65 - .025 * D, prof - Pre_i + y,
                      x + 1.65 - .025 * D - .1, prof - Pre_i + y,
                      x + 1.65 - .025 * D - .1, prof - Pre_f + y,
                      x + 1.65 - .025 * D, prof - Pre_f + y]
            polyline(file, pontos, C='C')
            hatch(file, x + 1.65 - .025 * D - .05, prof - Pre_i + y, 'H_PRE_FILTRO', P='S')
            hatch(file, x + 1.65 - .025 * D - .05, prof - Pre_i + y, '0_SOLO_GRANULOMETRIA', P='AR-SAND 0.0008 0')
            pontos = [x + 1.65 + .025 * D, prof - Pre_f + y,
                      x + 1.65 + .025 * D + .1, prof - Pre_f + y,
                      x + 1.65 + .025 * D + .1, prof - Pre_i + y,
                      x + 1.65 + .025 * D, prof - Pre_i + y]
            polyline(file, pontos, C='C')
            hatch(file, x + 1.65 + .025 * D + .05, prof - Pre_f + y, 'H_PRE_FILTRO', P='S')
            hatch(file, x + 1.65 + .025 * D + .05, prof - Pre_f + y, '0_SOLO_GRANULOMETRIA', P='AR-SAND 0.0008 0')

        ## BENTONITA
        pontos = [x + 1.65 - .025 * D, prof - B_i + y,
                  x + 1.65 - .025 * D - .1, prof - B_i + y,
                  x + 1.65 - .025 * D - .1, prof - B_f + y,
                  x + 1.65 - .025 * D, prof - B_f + y]
        polyline(file, pontos, C='C')
        hatch(file, x + 1.65 - .025 * D - .05, prof - B_i + y, 'H_BENTONITA', P='S')
        pontos = [x + 1.65 + .025 * D, prof - B_i + y,
                  x + 1.65 + .025 * D + .1, prof - B_i + y,
                  x + 1.65 + .025 * D + .1, prof - B_f + y,
                  x + 1.65 + .025 * D, prof - B_f + y]
        polyline(file, pontos, C='C')
        hatch(file, x + 1.65 + .025 * D + .05, prof - B_i + y, 'H_BENTONITA', P='S')

        ## CIMENTO
        pontos = [x + 1.65 - .30, prof + y,
                  x + 1.65 - .29, prof + y + CxConc / 3,
                  x + 1.65 - .27, prof + y + CxConc * 2 / 3,
                  x + 1.65 - .22, prof + y + CxConc,
                  x + 1.65 - .13, prof + y + CxConc,
                  x + 1.65 - .13, prof - C_i + y,
                  x + 1.65 - .025 * D, prof - C_i + y,
                  x + 1.65 - .025 * D, prof - C_f + y,
                  x + 1.65 - .025 * D - .15, prof - C_f + y,
                  x + 1.65 - .025 * D - .15, prof - C_f / 2 + y,
                  x + 1.65 - .30, prof - C_f / 2 + y]
        polyline(file, pontos, C='C')
        hatch(file, x + 1.65 - .22, prof + y + CxConc, 'H_CIMENTO', P='S')
        pontos = [x + 1.65 + .30, prof + y,
                  x + 1.65 + .29, prof + y + CxConc / 3,
                  x + 1.65 + .27, prof + y + CxConc * 2 / 3,
                  x + 1.65 + .22, prof + y + CxConc,
                  x + 1.65 + .13, prof + y + CxConc,
                  x + 1.65 + .13, prof - C_i + y,
                  x + 1.65 + .025 * D, prof - C_i + y,
                  x + 1.65 + .025 * D, prof - C_f + y,
                  x + 1.65 + .025 * D + .15, prof - C_f + y,
                  x + 1.65 + .025 * D + .15, prof - C_f / 2 + y,
                  x + 1.65 + .30, prof - C_f / 2 + y]
        polyline(file, pontos, C='C')
        hatch(file, x + 1.65 + .22, prof + y + CxConc, 'H_CIMENTO', P='S')

        # POÇO -----------------------------------------------------------------------------------------
        ## RANHURADO
        rectangle(file, 0, x + 1.65 - .025 * D, prof - (T_l + C_l + C_sf) + y,
                  x + 1.65 + .025 * D, prof - (T_l + C_l) + y)
        hatch(file, x + 1.65, prof - (T_l + C_l) + y, '0_LINHA', P='LINE 0.01 0')
        rectangle(file, 0, x + 1.65 - .030 * D, prof - (T_l + C_l + C_sf) + .02 * D + y,
                  x + 1.65 + .030 * D, prof - (T_l + C_l + C_sf) + y)
        hatch(file, x + 1.65 - .030 * D, prof - (T_l + C_l + C_sf) + .01 * D + y, '1_BRANCO', P='S')  # .254
        ## LISO
        rectangle(file, 0, x + 1.65 - .025 * D, prof - (T_l + C_l) + y,
                  x + 1.65 + .025 * D, prof - T_l + y)
        ## CAP DE PRESSÃO
        pontos = [x + 1.65 - .025 * D, prof - T_l + y,
                  x + 1.65 - .025 * D, prof - T_l + .0105 * D + y,
                  x + 1.65 - .010 * D, prof - T_l + .0105 * D + y,
                  x + 1.65 - .010 * D, prof - T_l + .0030 * D + y,
                  x + 1.65 - .008 * D, prof - T_l + .0030 * D + y,
                  x + 1.65 - .008 * D, prof - T_l + .0125 * D + y,
                  x + 1.65 - .025 * D, prof - T_l + .0125 * D + y,
                  x + 1.65 - .025 * D, prof - T_l + .0225 * D + y,
                  x + 1.65 - .023 * D, prof - T_l + .025 * D + y,
                  x + 1.65 - .018 * D, prof - T_l + .025 * D + y,
                  x + 1.65, prof - T_l + .0175 * D + y,  # centro
                  x + 1.65 + .018 * D, prof - T_l + .025 * D + y,
                  x + 1.65 + .023 * D, prof - T_l + .025 * D + y,
                  x + 1.65 + .025 * D, prof - T_l + .0225 * D + y,
                  x + 1.65 + .025 * D, prof - T_l + .0125 * D + y,
                  x + 1.65 + .008 * D, prof - T_l + .0125 * D + y,
                  x + 1.65 + .008 * D, prof - T_l + .0030 * D + y,
                  x + 1.65 + .010 * D, prof - T_l + .0030 * D + y,
                  x + 1.65 + .010 * D, prof - T_l + .0105 * D + y,
                  x + 1.65 + .025 * D, prof - T_l + .0105 * D + y,
                  x + 1.65 + .025 * D, prof - T_l + y]
        polyline(file, pontos, 'C', L='0_LINHA')
        hatch(file, x + 1.65, prof - T_l + y, '1_ACABAMENTO', P='S')
        pontos = [x + 1.65 - .008 * D, prof - T_l + .0125 * D + y,
                  x + 1.65 - .006 * D, prof - T_l + .0140 * D + y,
                  x + 1.65 + .006 * D, prof - T_l + .0140 * D + y,
                  x + 1.65 + .008 * D, prof - T_l + .0125 * D + y]
        polyline(file, pontos, '', L='0_LINHA')
        line(file, x + 1.65 - .025 * D, prof - T_l + .0022 * D + y, x + 1.65 + .025 * D, prof - T_l + .0022 * D + y,
             L='0_LINHA')
        circle(file, x + 1.65 - .0175 * D, prof - T_l + .006 * D + y, .003 * D, L='0_LINHA')
        hatch(file, x + 1.65 - .0175 * D, prof - T_l + .006 * D + .003 * D + y, '1_BRANCO', P='S')
        line(file, x + 1.65 - .023 * D, prof - T_l + .0105 * D + y, x + 1.65 - .023 * D, prof - T_l + .0022 * D + y,
             L='0_LINHA')
        circle(file, x + 1.65 + .0175 * D, prof - T_l + .006 * D + y, .003 * D, L='0_LINHA')
        hatch(file, x + 1.65 + .0175 * D, prof - T_l + .006 * D + .003 * D + y, '1_BRANCO', P='S')
        line(file, x + 1.65 + .023 * D, prof - T_l + .0105 * D + y, x + 1.65 + .023 * D, prof - T_l + .0022 * D + y,
             L='0_LINHA')
        rectangle(file, 0, x + 1.65 - .025 * D, prof - T_l + y, x + 1.65 + .025 * D, prof - (T_l + .025 * D) + y)
        hatch(file, x + 1.65, prof - (T_l + .025 * D) + y, '1_BORRACHA', P='S')
        rectangle(file, 0, x + 1.65 - .025 * D, prof - (T_l + .025 * D) + y, x + 1.65 + .025 * D,
                  prof - (T_l + .027 * D) + y)
        hatch(file, x + 1.65, prof - (T_l + .027 * D) + y, '1_ACABAMENTO', P='S')
        rectangle(file, 0, x + 1.65 - .008 * D, prof - (T_l + .027 * D) + y, x + 1.65 + .008 * D,
                  prof - (T_l + .029 * D) + y)
        hatch(file, x + 1.65, prof - (T_l + .029 * D) + y, '1_ACABAMENTO', P='S')
        rectangle(file, 0, x + 1.65 - .006 * D, prof - (T_l + .029 * D) + y, x + 1.65 + .006 * D,
                  prof - (T_l + .055 * D) + y)
        hatch(file, x + 1.65, prof - (T_l + .055 * D) + y, '1_ACABAMENTO', P='S')
        hatch(file, x + 1.65, prof - (T_l + .055 * D) + y, '0_LINHA', P='LINE 0.001 0')
        pontos = [x + 1.65 - .006 * D, prof - (T_l + .055 * D) + y,
                  x + 1.65 - .005 * D, prof - (T_l + .057 * D) + y,
                  x + 1.65 + .005 * D, prof - (T_l + .057 * D) + y,
                  x + 1.65 + .006 * D, prof - (T_l + .055 * D) + y]
        polyline(file, pontos, 'C', L='0_LINHA')
        hatch(file, x + 1.65, prof - (T_l + .057 * D) + y, '1_ACABAMENTO', P='S')

        ## LIMITE DO GEOMECÂNICO
        pontos = [x + 1.65 - .025 * D, prof - T_l + y,
                  x + 1.65 - .025 * D, prof - (T_l + C_l + C_sf) + .02 * D + y,
                  x + 1.65 - .030 * D, prof - (T_l + C_l + C_sf) + .02 * D + y,
                  x + 1.65 - .030 * D, prof - (T_l + C_l + C_sf) + y,
                  x + 1.65 + .030 * D, prof - (T_l + C_l + C_sf) + y,
                  x + 1.65 + .030 * D, prof - (T_l + C_l + C_sf) + .02 * D + y,
                  x + 1.65 + .025 * D, prof - (T_l + C_l + C_sf) + .02 * D + y,
                  x + 1.65 + .025 * D, prof - T_l + y]
        polyline(file, pontos, '', L='0_LINHA_0.15')

        # TAMPA E ACABAMENTOS
        if PescComp > 0:
            # Esquerda - lateral
            pontos = [x + 1.65 - .13, prof + y + PescComp,
                      x + 1.65 - .13, prof + y - 0.05,
                      x + 1.65 - .15, prof + y - 0.05,
                      x + 1.65 - .15, prof + y - 0.03,
                      x + 1.65 - .15, prof + y + 0.03,
                      x + 1.65 - .14, prof + y + 0.03,
                      x + 1.65 - .14, prof + y + PescComp - 0.01,
                      x + 1.65 - .16, prof + y + PescComp - 0.01,
                      x + 1.65 - .16, prof + y + PescComp]
            polyline(file, pontos, 'C', L='0_LINHA')
            hatch(file, x + 1.65 - .14, prof + y + 0.04, '1_ACABAMENTO', P='S')
            pontos = [x + 1.65 - .13, prof + y + PescComp,
                      x + 1.65 - .13, prof + y + PescComp + 0.01,
                      x + 1.65 - .16, prof + y + PescComp + 0.01,
                      x + 1.65 - .16, prof + y + PescComp]
            polyline(file, pontos, 'C', L='0_LINHA')
            hatch(file, x + 1.65 - .14, prof + y + PescComp + 0.01, '1_ACABAMENTO', P='S')

            pontos = [x + 1.65 - .16, prof + y + PescComp - 0.005,
                      x + 1.65 - .16 - .013, prof + y + PescComp + 0.005,
                      x + 1.65 - .16 - .013, prof + y + PescComp + 0.025,
                      x + 1.65 - .14, prof + y + PescComp + 0.032,
                      x + 1.65 - .14, prof + y + PescComp + 0.01,
                      x + 1.65 - .16, prof + y + PescComp + 0.01]
            polyline(file, pontos, 'C', L='0_LINHA')
            hatch(file, x + 1.65 - .14, prof + y + PescComp - .02, '1_ACABAMENTO', P='S')
            circle(file, x + 1.65 - .17, prof + y + PescComp + 0.02, R=0.015, L='0_LINHA')
            hatch(file, x + 1.65 - .17, prof + y + PescComp + 0.035, '1_ACABAMENTO', P='S')

            # Direita - lateral
            pontos = [x + 1.65 + .13, prof + y + PescComp,
                      x + 1.65 + .13, prof + y - 0.05,
                      x + 1.65 + .15, prof + y - 0.05,
                      x + 1.65 + .15, prof + y - 0.03,
                      x + 1.65 + .15, prof + y + 0.03,
                      x + 1.65 + .14, prof + y + 0.03,
                      x + 1.65 + .14, prof + y + PescComp - 0.01,
                      x + 1.65 + .16, prof + y + PescComp - 0.01,
                      x + 1.65 + .16, prof + y + PescComp]
            polyline(file, pontos, 'C', L='0_LINHA')
            hatch(file, x + 1.65 + .14, prof + y + 0.04, '1_ACABAMENTO', P='S')
            pontos = [x + 1.65 + .13, prof + y + PescComp,
                      x + 1.65 + .13, prof + y + PescComp + 0.01,
                      x + 1.65 + .16, prof + y + PescComp + 0.01,
                      x + 1.65 + .16, prof + y + PescComp]
            polyline(file, pontos, 'C', L='0_LINHA')
            hatch(file, x + 1.65 + .14, prof + y + PescComp + 0.01, '1_ACABAMENTO', P='S')

            # Fechador
            pontos = [x + 1.65 + .16, prof + y + PescComp - 0.01,
                      x + 1.65 + .17, prof + y + PescComp - 0.05,
                      x + 1.65 + .21, prof + y + PescComp - 0.05,
                      x + 1.65 + .21, prof + y + PescComp - 0.04,
                      x + 1.65 + .18, prof + y + PescComp - 0.04,
                      x + 1.65 + .17, prof + y + PescComp + 0.005]
            polyline(file, pontos, 'C', L='0_LINHA')
            hatch(file, x + 1.65 + .21, prof + y + PescComp - .045, '1_ACABAMENTO', P='S')
            circle(file, x + 1.65 + .21, prof + y + PescComp - .045, R=0.015, L='0_LINHA')
            hatch(file, x + 1.65 + .21, prof + y + PescComp - .045 + .015, '1_ACABAMENTO', P='S')
            circle(file, x + 1.65 + .16, prof + y + PescComp, R=0.015, L='0_LINHA')
            hatch(file, x + 1.65 + .16 + .015, prof + y + PescComp, '1_ACABAMENTO', P='S')

            # Tampa
            rectangle(file, 0, x + 1.65 - .14, prof + y + PescComp + .01,
                      x + 1.65 + .14, prof + y + PescComp + .04)
            hatch(file, x + 1.65, prof + y + PescComp + .04, '1_ACABAMENTO', P='S')

            pontos = [x + 1.65 + .09, prof + y + PescComp + .01 + 0.03,
                      x + 1.65 + .11, prof + y + PescComp + .01 + 0.05,
                      x + 1.65 + .125, prof + y + PescComp + .01 + 0.05,
                      x + 1.65 + .125, prof + y + PescComp + .01 + 0.03]
            polyline(file, pontos, 'C', L='0_LINHA')
            hatch(file, x + 1.65 + .125, prof + y + PescComp + .01 + 0.04, '1_ACABAMENTO', P='S')

            circle(file, x + 1.65 + .125, prof + y + PescComp + 0.06, 0.015, L='0_LINHA')
            hatch(file, x + 1.65 + .140, prof + y + PescComp + 0.06, '1_ACABAMENTO', P='S')

        elif T_l < 0:
            rectangle(file, 0, x + 1.65 - .13, prof + abs(T_l) + .10 + y, x + 1.65 + .13,
                      prof + abs(T_l) + .10 + .0132 + y)
            hatch(file, x + 1.65 - .12, prof + abs(T_l) + .10 + y, '1_ACABAMENTO', P='S')
            line(file, x + 1.65 - .13, prof + CxConc, x + 1.65 - .13, prof + abs(T_l) + .10 + y)
            line(file, x + 1.65 + .13, prof + CxConc, x + 1.65 + .13, prof + abs(T_l) + .10 + y)

        else:
            y = y + CxConc
            rectangle(file, 0, x + 1.65 - .13, prof + y, x + 1.65 + .13, prof - .01 + y)
            hatch(file, x + 1.65, prof + y, '1_ACABAMENTO', P='S')
            rectangle(file, 0, x + 1.65 - .13, prof - .013 + y, x + 1.65 - .125,
                      prof - .013 - T_l - round(.75 * (C_f - T_l), 4) + y)
            hatch(file, x + 1.65 - .125, prof - .014 + y, '1_BRANCO', P='S')
            rectangle(file, 0, x + 1.65 + .13, prof - .013 + y, x + 1.65 + .125,
                      prof - .013 - T_l - round(.75 * (C_f - T_l), 4) + y)
            hatch(file, x + 1.65 + .125, prof - .014 + y, '1_BRANCO', P='S')
            pontos = [x + 1.65 - .13, prof + y,
                      x + 1.65 - .19, prof + y,
                      x + 1.65 - .19, prof - .01 + y,
                      x + 1.65 - .16, prof - .01 + y,
                      x + 1.65 - .158, prof - .015 + y,
                      x + 1.65 - .150, prof - .015 + y,
                      x + 1.65 - .148, prof - .016 + y,  # inicio_curva
                      x + 1.65 - .1465, prof - .017 + y,  # inicio_curva
                      x + 1.65 - .145, prof - .0185 + y,
                      x + 1.65 - .1435, prof - .0202 + y,
                      x + 1.65 - .142, prof - .0225 + y,  # fim_curva
                      x + 1.65 - .141, prof - .025 + y,  # fim_curva
                      x + 1.65 - .14, prof - .03 + y,
                      x + 1.65 - .14, prof - .15 + y,
                      x + 1.65 - .13, prof - .15 + y]
            polyline(file, pontos, 'C', L='0_LINHA')
            hatch(file, x + 1.65 - .14, prof - .15 + y, '1_ACABAMENTO', P='S')
            pontos = [x + 1.65 + .13, prof + y,
                      x + 1.65 + .19, prof + y,
                      x + 1.65 + .19, prof - .01 + y,
                      x + 1.65 + .16, prof - .01 + y,
                      x + 1.65 + .158, prof - .015 + y,
                      x + 1.65 + .150, prof - .015 + y,
                      x + 1.65 + .148, prof - .016 + y,  # inicio_curva
                      x + 1.65 + .1465, prof - .017 + y,  # inicio_curva
                      x + 1.65 + .145, prof - .0185 + y,
                      x + 1.65 + .1435, prof - .0202 + y,
                      x + 1.65 + .142, prof - .0225 + y,  # fim_curva
                      x + 1.65 + .141, prof - .025 + y,  # fim_curva
                      x + 1.65 + .14, prof - .03 + y,
                      x + 1.65 + .14, prof - .15 + y,
                      x + 1.65 + .13, prof - .15 + y]
            polyline(file, pontos, 'C', L='0_LINHA')
            hatch(file, x + 1.65 + .14, prof - .15 + y, '1_ACABAMENTO', P='S')


def boreholes_per_layout(stacks_of, CSV, normal, i_normal):
    try:  # There might not be subsequent boreholes
        existem_pocos, layout, titulo = [0, '"', '']
        for i in range(i_normal, i_normal + stacks_of):
            layout += CSV['ID_sonda'][normal[i]] + ' '
            titulo += layout[:-1]
            existe_poco = validate(CSV, normal[i])
            if existe_poco == 1: titulo += '/' + CSV['ID_poco'][normal[i]]
            titulo += ' E '
            existem_pocos = existe_poco
    except:
        pass
    layout = layout[:-1] + '"'
    titulo = titulo[:-3].replace('"', '')
    print(' New layout:', layout)
    return existem_pocos, layout, titulo


def fazer_layout(file, layout, titulo, existem_pocos, CTB, sist_geo, logo_png):
    # 240
    def perfil_esquematico_poco(file):
        """Perfil esquemático de poço de monitoramento para o layout"""
        zoom(file, 252, 148, 294, 190)
        # SOLO LADO ESQUERDO
        pontos = [262 - 7, 150,
                  262 - 7, 173,
                  262 - 5, 173,
                  262 - 5, 169,
                  262 - 3, 169,
                  262 - 3, 150]
        polyline(file, pontos, C='C')
        hatch(file, 262 - 7, 170, 'SC_MARROM', P='S')
        # SOLO LADO DIREITO
        pontos = [262 + 7, 150,
                  262 + 7, 173,
                  262 + 5, 173,
                  262 + 5, 169,
                  262 + 3, 169,
                  262 + 3, 150]
        polyline(file, pontos, C='C')
        hatch(file, 262 + 7, 170, 'SC_MARROM', P='S')

        # CIMENTO LADO ESQUERDO
        pontos = [262 - 3, 173,
                  262 - 5, 173,
                  262 - 5, 168,
                  262 - 4, 168,
                  262 - 4, 167,
                  262 - 1, 167,
                  262 - 1, 169,
                  262 - 2.7, 169,
                  262 - 2.7, 171.5,
                  262 - 3, 171.5]
        polyline(file, pontos, C='C')
        hatch(file, 262 - 4, 173, 'H_CIMENTO', P='S')
        # CIMENTO LADO DIREITO
        pontos = [262 + 3, 173,
                  262 + 5, 173,
                  262 + 5, 168,
                  262 + 4, 168,
                  262 + 4, 167,
                  262 + 1, 167,
                  262 + 1, 169,
                  262 + 2.7, 169,
                  262 + 2.7, 171.5,
                  262 + 3, 171.5]
        polyline(file, pontos, C='C')
        hatch(file, 262 + 4, 173, 'H_CIMENTO', P='S')

        # BENTONITA LADO ESQUERDO
        rectangle(file, 0, 262 - 3, 167, 262 - 1, 159)
        hatch(file, 262 - 3, 165, 'H_BENTONITA', P='S')
        # BENTONITA LADO DIREITO
        rectangle(file, 0, 262 + 3, 167, 262 + 1, 159)
        hatch(file, 262 + 3, 165, 'H_BENTONITA', P='S')

        # PRÉ-FILTRO LADO ESQUERDO
        rectangle(file, 0, 262 - 3, 159, 262 - 1, 150)
        hatch(file, 262 - 2, 150, 'H_PRE_FILTRO', P='S')
        hatch(file, 262 - 2, 150, '0_SOLO_GRANULOMETRIA', P='AR-SAND 0.0126 0')
        # PRÉ-FILTRO LADO DIREITO
        rectangle(file, 0, 262 + 3, 159, 262 + 1, 150)
        hatch(file, 262 + 2, 150, 'H_PRE_FILTRO', P='S')
        hatch(file, 262 + 2, 150, '0_SOLO_GRANULOMETRIA', P='AR-SAND 0.0126 0')

        # CANO DO POÇO
        # LISO
        rectangle(file, 0, 262 - 1, 170, 262 + 1, 156)
        # RANHURADO
        rectangle(file, 0, 262 - 1, 156, 262 + 1, 151)
        hatch(file, 262, 151, '0_LINHA', P='LINE 0.22 0')
        # TAMPA BASE
        rectangle(file, 0, 262 - 1.5, 151, 262 + 1.5, 150)
        hatch(file, 262, 150, '1_BRANCO', P='S')

        #### CAP DE PRESSÃO
        D = 4
        pontos = [262 - .25 * D, 170,
                  262 - .25 * D, 170 + .105 * D,
                  262 - .10 * D, 170 + .105 * D,
                  262 - .10 * D, 170 + .030 * D,
                  262 - .08 * D, 170 + .030 * D,
                  262 - .08 * D, 170 + .125 * D,
                  262 - .25 * D, 170 + .125 * D,
                  262 - .25 * D, 170 + .225 * D,
                  262 - .23 * D, 170 + .25 * D,
                  262 - .18 * D, 170 + .25 * D,
                  262, 170 + .175 * D,  # centro
                  262 + .18 * D, 170 + .25 * D,
                  262 + .23 * D, 170 + .25 * D,
                  262 + .25 * D, 170 + .225 * D,
                  262 + .25 * D, 170 + .125 * D,
                  262 + .08 * D, 170 + .125 * D,
                  262 + .08 * D, 170 + .030 * D,
                  262 + .10 * D, 170 + .030 * D,
                  262 + .10 * D, 170 + .105 * D,
                  262 + .25 * D, 170 + .105 * D,
                  262 + .25 * D, 170]
        polyline(file, pontos, 'C', L='0_LINHA')
        hatch(file, 262, 170, '1_ACABAMENTO', P='S')
        pontos = [262 - .08 * D, 170 + .125 * D,
                  262 - .06 * D, 170 + .140 * D,
                  262 + .06 * D, 170 + .140 * D,
                  262 + .08 * D, 170 + .125 * D]
        polyline(file, pontos, '', L='0_LINHA')
        line(file, 262 - .25 * D, 170 + .022 * D,
             262 + .25 * D, 170 + .022 * D, L='0_LINHA')
        circle(file, 262 - .175 * D, 170 + .06 * D, .03 * D, L='0_LINHA')
        hatch(file, 262 - .175 * D, 170 + .06 * D + .03 * D, '1_BRANCO', P='S')
        line(file, 262 - .23 * D, 170 + .105 * D,
             262 - .23 * D, 170 + .022 * D, L='0_LINHA')
        circle(file, 262 + .175 * D, 170 + .06 * D, .03 * D, L='0_LINHA')
        hatch(file, 262 + .175 * D, 170 + .06 * D + .03 * D, '1_BRANCO', P='S')
        line(file, 262 + .23 * D, 170 + .105 * D,
             262 + .23 * D, 170 + .022 * D, L='0_LINHA')
        rectangle(file, 0, 262 - .25 * D, 170,
                  262 + .25 * D, 170 - (.25 * D))
        hatch(file, 262, 170 - .25 * D, '1_BORRACHA', P='S')
        rectangle(file, 0, 262 - .25 * D, 170 - (.25 * D),
                  262 + .25 * D, 170 - (.27 * D))
        hatch(file, 262, 170 - .27 * D, '1_ACABAMENTO', P='S')
        rectangle(file, 0, 262 - .08 * D, 170 - (.27 * D),
                  262 + .08 * D, 170 - (.29 * D))
        hatch(file, 262, 170 - .29 * D, '1_ACABAMENTO', P='S')
        rectangle(file, 0, 262 - .06 * D, 170 - (.29 * D),
                  262 + .06 * D, 170 - (.55 * D))
        hatch(file, 262, 170 - (.55 * D), '1_ACABAMENTO', P='S')
        hatch(file, 262, 170 - (.55 * D), '0_LINHA', P='LINE 0.04 0')
        pontos = [262 - .06 * D, 170 - (.55 * D),
                  262 - .05 * D, 170 - (.57 * D),
                  262 + .05 * D, 170 - (.57 * D),
                  262 + .06 * D, 170 - (.55 * D)]
        polyline(file, pontos, 'C', L='0_LINHA')
        hatch(file, 262, y + 170 - (.57 * D), '1_ACABAMENTO', P='S')

        # ACABAMENTO
        rectangle(file, 0, 262 - 2.7, 173 - .7,
                  262 - 2.5, 168.5)
        hatch(file, 262 - 2.5, 170, '1_BRANCO', P='S')
        rectangle(file, 0, 262 + 2.7, 173 - .7,
                  262 + 2.5, 168.5)
        hatch(file, 262 + 2.5, 170, '1_BRANCO', P='S')
        pontos = [262 - 3, 173,
                  262 - 4.5, 173,
                  262 - 4.5, 173 - .4,
                  262 - 3.8, 173 - .4,
                  262 - 3.75, 173 - .5,
                  262 - 3.545, 173 - .507,  # inicio_curva
                  262 - 3.517, 173 - .527,
                  262 - 3.488, 173 - .556,
                  262 - 3.459, 173 - .588,
                  262 - 3.431, 173 - .633,
                  262 - 3.411, 173 - .681,  # fim_curva
                  262 - 3.4, 173 - .78,
                  262 - 3.4, 173 - 3.5,
                  262 - 3, 173 - 3.5]
        polyline(file, pontos, 'C', L='0_LINHA')
        hatch(file, 262 - 3, 172.5, '1_ACABAMENTO', P='S')
        pontos = [262 + 3, 173,
                  262 + 4.5, 173,
                  262 + 4.5, 173 - .4,
                  262 + 3.8, 173 - .4,
                  262 + 3.75, 173 - .5,
                  262 + 3.545, 173 - .507,  # inicio_curva
                  262 + 3.517, 173 - .527,
                  262 + 3.488, 173 - .556,
                  262 + 3.459, 173 - .588,
                  262 + 3.431, 173 - .633,
                  262 + 3.411, 173 - .681,  # fim_curva
                  262 + 3.4, 173 - .78,
                  262 + 3.4, 173 - 3.5,
                  262 + 3, 173 - 3.5]
        polyline(file, pontos, 'C', L='0_LINHA')
        hatch(file, 262 + 3, 172.5, '1_ACABAMENTO', P='S')
        # TAMPA
        rectangle(file, 0, 262 - 3, 173, 262 + 3, 173 - 0.5)
        hatch(file, 262, 173, '1_ACABAMENTO', P='S')

        #### LIMITE DO GEOMECÂNICO
        pontos = [262 - 1, 170,
                  262 - 1, 151,
                  262 - 1.5, 151,
                  262 - 1.5, 150,
                  262 + 1.5, 150,
                  262 + 1.5, 151,
                  262 + 1, 151,
                  262 + 1, 170]
        polyline(file, pontos, '', L='0_LINHA_0.15')

        # ESCRITOS - LEGENDAS DO ESQUEMA
        def seta(file, x, y, txt):
            mtext(file, 272, y + 1, 288.5, y - 1, txt, J='left', H=1.1382, R=0)
            line(file, x, y, 271, y)
            line(file, x, y, x + 1.4, y_arrow + .5)
            line(file, x, y, x + 1.4, y_arrow - .5)

        x_arrow, y_arrow = [265.5, 172.7]
        txt = u'Câmara de calçada'
        seta(file, x_arrow, y_arrow, txt)

        x_arrow, y_arrow = [262, 169.5]
        txt = u'Cap de pressão'
        seta(file, x_arrow, y_arrow, txt)

        x_arrow, y_arrow = [265.3, 167.5]
        txt = 'Cimento'
        seta(file, x_arrow, y_arrow, txt)

        x_arrow, y_arrow = [263.5, 165.5]
        txt = 'Selo de bentonita'
        seta(file, x_arrow, y_arrow, txt)

        x_arrow, y_arrow = [262, 161.5]
        txt = u'Tubo de PVC\nGeomecânico DN50'
        seta(file, x_arrow, y_arrow, txt)

        x_arrow, y_arrow = [263.5, 157]
        txt = u'Pré-filtro (areia)'
        seta(file, x_arrow, y_arrow, txt)

        x_arrow, y_arrow = [262, 154]
        txt = u'Seção filtrante'
        seta(file, x_arrow, y_arrow, txt)

        mtext(file, 254.1909, 178.9105 - 8, 285.1810, 178.9105 + 8, u'PERFIL ESQUEMÁTICO DE UM POÇO MONITORAMENTO', J='left', H=1.6694, R=0)
        zoom(file, -2, -2, 298, 210)

    def legenda(file):
        # todo não mostrar NA se não existe
        # LEGENDA
        mtext(file, 6.1966 + 0.8309, 27.3131 - 2.2399, 53.6600, 27.3131, 'LEGENDA', J='left', H=1.2, R=0)
        gap = (25.0481 - 10.8758) / 4

        mtext(file, 12.7863, 10.8758 + 3 * gap, 53.6600, 10.8758 + 4 * gap, u'Nível da água durante a sondagem',
              J='left', H=1.44, R=0)
        insert_block(file, 'NA_SONDA', 10.8758, 10.8758 + 3.5 * gap, scale_x='20', scale_y='20')
        mtext(file, 12.7863, 10.8758 + 2 * gap, 53.6600, 10.8758 + 3 * gap, u'Nível da água estabilizado', J='left',
              H=1.44, R=0)
        insert_block(file, 'NA_ESTAB', 10.8758, 10.8758 + 2.5 * gap, scale_x='20', scale_y='20')

        mtext(file, 12.7863, 10.8758 + gap, 53.6600, 10.8758 + 2 * gap, u'Medição de VOC (ppm)', J='left', H=1.44, R=0)
        mtext(file, 7.5764, 10.8758 + gap, 53.6600, 10.8758 + 2 * gap, u'XXX', J='left', H=1.26, R=0)

        mtext(file, 12.7863, 11.3758, 53.6600 + 0.3, 10.8758 + gap, u'Profundidade do ponto amostrado', J='left',
              H=1.44, R=0)
        insert_block(file, 'CA', 10.8758, 10.8758 + .5 * gap + 0.3, scale_x='20', scale_y='20')

    file.write('-LAYOUT N ' + layout + '\n')
    file.write('-LAYOUT S ' + layout + '\n')
    psetup(file, layout, ctb=CTB)
    file.write('ERASE ALL \n')  # Limpa tudo
    if existem_pocos > 0:
        file.write(
            '_VIEWPORTS 6.1966,27.3131 251.3136,196.6754\n')  # Cria o viewport menor com espaço para perfil esquemático de um poço
        rectangle(file, 0, 6.1966, 27.3131, 251.3136, 196.6754, L='0_SELO')  # Retangulo pro Viewport menor
        texto = u'FIGURA XX – PERFIS DE SONDAGEM E POÇOS DE MONITORAMENTO ' + titulo
        mtext(file, 53.6600 + 2.7814, 19.5444, 217.7796, 27.3131, texto, J='left', H=1.92, R=0)
        perfil_esquematico_poco(file)
    else:
        file.write('_VIEWPORTS 6.1966,27.3131 289.1967,196.6754\n')  # Cria o viewport maior
        rectangle(file, 0, 6.1966, 27.3131, 289.1967, 196.6754, L='0_SELO')  # Retangulo pro Viewport maior
        texto = u'FIGURA XX – PERFIS DE SONDAGEM ' + titulo
        mtext(file, 53.6600 + 2.7814, 19.5444, 217.7796, 27.3131, texto, J='left', H=1.92, R=0)
    rectangle(file, 0, 6.1966, 196.6754, 289.1967, 11.7758, L='0_SELO')  # Retangulo pro layout
    rectangle(file, 0, 6.1966, 27.3131, 289.1967, 11.7758, L='0_SELO')  # Retangulo pro rodape

    line(file, 53.6600, 27.3131, 53.6600, 11.7758, L='0_SELO')  # Linha nome figura vertical
    line(file, 53.6600, 19.5444, 241.1388, 19.5444, L='0_SELO')  # Linha nome figura horizontal

    line(file, 218.3075, 19.5444, 218.3075, 27.3131, L='0_SELO')  # Linha escala vertical
    texto = escala
    mtext(file, 218.3075 + 2.7814, 19.5444, 241.1388, 27.3131, texto, J='left', H=1.92, R=0)
    mtext(file, 218.3075 + 0.8309, 27.3131 - 2.2399, 241.1388, 27.3131, 'ESCALA', J='left', H=1.2, R=0)

    texto = projeto  # Projeto
    mtext(file, 53.6600 + 2.7814, 11.7758 - .8, 127.7154, 19.5444 - .8, texto, J='left', H=1.92, R=0)
    mtext(file, 53.6600 + 0.8309, 19.5444 - 2.2399, 127.7154, 19.5444, 'PROJETO', J='left', H=1.2, R=0)

    line(file, 127.7329, 11.7758, 127.7329, 19.5444, L='0_SELO')  # Linha cliente vertical
    texto = cliente
    mtext(file, 127.7329 + 2.7814, 11.7758, 168.3090, 19.5444, texto, J='left', H=1.92, R=0)
    mtext(file, 127.7329 + 0.8309, 19.5444 - 2.2399, 168.3090, 19.5444, 'CLIENTE', J='left', H=1.2, R=0)

    line(file, 168.3090, 11.7758, 168.3090, 19.5444, L='0_SELO')  # Linha sist_geo vertical
    texto = sist_geo
    gap = 0
    if len(sist_geo) > 25:
        gap = 1
    mtext(file, 168.3090 + 2.7814, 11.7758 - gap, 208.2969, 19.5444 - gap, texto, J='left', H=1.92, R=0)
    mtext(file, 168.3090 + 0.8309, 19.5444 - 2.2399, 208.2969, 19.5444, u'SISTEMA DE REFERÊNCIA', J='left', H=1.2, R=0)

    line(file, 208.2969, 11.7758, 208.2969, 19.5444, L='0_SELO')  # Linha data vertical
    texto = data
    mtext(file, 208.2969 + 2.7814, 11.7758, 241.1388, 19.5444, texto, J='left', H=1.92, R=0)
    mtext(file, 208.2969 + 0.8309, 19.5444 - 2.2399, 241.1388, 19.5444, 'DATA', J='left', H=1.2, R=0)

    # LOGO
    set_layer(file, '0_SELO')
    file.write("-IMAGE A " + '"' + logo_png + '"' + "\n" + "239.5104,11.7758\n" + "0.0994\n" + "0\n")
    #           -IMAGE Attach      PATH                     POINT                  SCALE       ROT
    # file.write("-IMAGE A " + '"' + logo_png + '"' + "\n" + "239.5104,11.7758\n" + "0.3105\n" + "0\n")
    legenda(file)


def final_adjusts_and_finish(file):
    file.write('-LAYOUT D Layout1\n')  # Delete default layouts
    file.write('-LAYOUT D Layout2\n')

    file.write('LWDISPLAY ON\n')  # Last adjusts and close
    file.write('PDMODE 33\n')
    file.write("-OSNAP End,Mid,Cen,Node,Quad,Int,Ins,perp,Tan,Near,Gcen,Ext,Par\n")
    file.close()


# 3. Read files =========================================================================
title_block = '1_title_block.csv'
borehole_data = '2_borehole_data.csv'
output_scr_acad = '4_script_borehole_acad.scr'
ctb = 'company_plotstyle.ctb'  # Set on AutoCAD (option support file path new+browse)
logo_png = r'template\logo.png'
cliente, projeto, data, escala, sist_geo, CSV, logo_png, output_scr_acad = read_files(title_block, borehole_data, output_scr_acad, logo_png)

section(84, '3. VOC measurement spacing:')
VOC_dist = input(' Spacing between VOC measurements (default: 0.5m, hit enter): ')
if VOC_dist == '':
    VOC_dist = 0.5
else:
    VOC_dist = float(VOC_dist)
print('', VOC_dist)

# 4. Open output file
file = codecs.open(output_scr_acad, 'wb', encoding='mbcs')
file.write('OSMODE 0\n')
file.write('SHADEMODE 2\n')

# 4.1 Create layers and blocks
create_layers(file)
create_blocks(file)

# 4.2 Shallow and normal depth boreholes
shallow, normal = [[], []]
for n_p in range(len(CSV)):
    if CSV['Prof'][n_p] < 2:
        shallow.append(n_p)
    else:
        normal.append(n_p)

# Layouts
section(84, '4. Layouts:')

# Normal depth boreholes
x, y, i_layout = [0, 0, 0]
profs_list = CSV.iloc[normal, CSV.columns.tolist().index('Prof')].tolist()
if normal: prof_max = round(max(profs_list), 1)

for n_p in normal:
    existe_poco = validate(CSV, n_p)
    D = cabecalho(file, CSV, n_p, existe_poco, i_layout, x, y, prof_max, VOC_dist, sist_geo)
    perfil_pedologico(file, n_p, x, y, D, CSV['Pedologia'], prof_max, existe_poco)
    adicionar_poco(file, CSV, n_p, prof_max, x, y, existe_poco)

    # Layout
    if i_layout == 0:  # 1st borehole
        i_normal = normal.index(n_p)
        existem_pocos, layout, titulo = boreholes_per_layout(2, CSV, normal, i_normal)
        print(' New layout:', layout)
        fazer_layout(file, layout, titulo, existem_pocos, ctb, sist_geo, logo_png)
        mspace_zoom(file, x - .05, y - .05, x + 5.18 + .05, y + prof_max + 1.02)
        file.write('PSPACE\nMODEL\n')
        x = x + 5.18
        i_layout += 1
    else:  # 2nd borehole
        file.write('-LAYOUT S ' + layout + '\n')  # To the layout
        mspace_zoom(file, x - 5.18 - .05, y - .05, x + 5.0 + .05, y + prof_max + 1.02)
        file.write('PSPACE\nMODEL\n')
        x = x + 11.23
        i_layout = 0

# Shallow depth boreholes
x, i_layout = [x + 11.23, 0]
profs_list = CSV.iloc[shallow, CSV.columns.tolist().index('Prof')].tolist()
if shallow: prof_max = round(max(profs_list), 1)

for n_p in shallow:
    existe_poco = validate(CSV, n_p)

    D = cabecalho(file, CSV, n_p, existe_poco, i_layout, x, y, prof_max, VOC_dist, sist_geo)
    perfil_pedologico(file, n_p, x, y, D, CSV['Pedologia'], prof_max, existe_poco)
    adicionar_poco(file, CSV, n_p, prof_max, x, y, existe_poco)

    # Layout
    if i_layout == 0:  # 1st borehole
        i_shallow = shallow.index(n_p)
        existem_pocos, layout, titulo = boreholes_per_layout(2, CSV, shallow, i_shallow)
        fazer_layout(file, layout, titulo, existem_pocos, ctb, sist_geo, logo_png)
        mspace_zoom(file, x - .05, y - .05, x + 5.18 + .05, y + prof_max + 1.02)
        file.write('PSPACE\nMODEL\n')
        x = x + 5.18
        i_layout += 1
    elif i_layout == 1:  # 2nd borehole
        file.write('-LAYOUT S ' + layout + '\n')  # To the layout
        mspace_zoom(file, x - 5.18 - .05, y - .05, x + 5.00 + .05, y + prof_max + 1.02 + .05)
        file.write('PSPACE\nMODEL\n')
        x = x - 5.18
        y = y - (prof_max + .42 + .3 + .3 + .18)
        i_layout += 1
    elif i_layout == 2:  # 3rd borehole
        file.write('-LAYOUT S ' + layout + '\n')  # To the layout
        mspace_zoom(file, x - .05, y - .05, x + 10.18 + .05, y + 2 * prof_max + 2 * 1.02 + 0.2 + .05)
        file.write('PSPACE\nMODEL\n')
        x = x + 5.18
        i_layout += 1
    else:
        file.write('-LAYOUT S ' + layout + '\n')  # To the layout
        mspace_zoom(file, x - 5.18 - .05, y - .05, x + 5.00 + .05, y + 2 * prof_max + 2 * 1.02 + 0.2 + .05)
        file.write('PSPACE\nMODEL\n')
        x = x + 11.23
        y = y + (prof_max + .42 + .3 + .3 + .18)
        i_layout = 0

profs_list = CSV.iloc[:, CSV.columns.tolist().index('Prof')].tolist()
prof_max = round(max(profs_list), 1)
zoom(file, -1, -1, x + 6, y + prof_max + 2)
final_adjusts_and_finish(file)

# 4.3 Final message
a = output_scr_acad
a = a[::-1][:a[::-1].index('\\')][::-1]

division(84)
msg = 'Done! Open AutoCAD, select "No Template-Metric", click on "Start drawing!"\n' \
      'Type "scr", press enter, and select "' + a + '"!'

signature = 'Automatically Soil Profile Drawer\n' \
            'Last update 2022\n' \
            '----------------\n' \
            'J S F\n' \
            '20/02/2021\n'
final_message(msg, signature, 84)
division(84)
