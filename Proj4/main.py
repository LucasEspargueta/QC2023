import pandas as pd
import math

def get_min_distance(x, y, z, sup):
    # Calcula a menor distância entre o átomo fornecido (x,y,z) e todos os átomos que fazem parte da superficie
    # inicialização da distancia
    min_dist = 999999
    # sup.iterrows retorna um tuplo com o indice e o valor duma row da DataFrame, como o indice não nos interessa é descartado com uma throwaway variable, '_'
    for _, sup_atom in sup.iterrows():
        dist = distance(x, float(sup_atom['x']), y, float(sup_atom['y']), z, float(sup_atom['z']))
        min_dist = min(min_dist, dist)
    
    return min_dist

def distance(x1,x2,y1,y2,z1,z2):
    # Calcula a distância entre dois pontos
    d = math.sqrt((x1-x2)**2+(y1-y2)**2+(z1-z2)**2)
    
    return d

# assume que se uma posição está presente, as outras também estarão. ex: se y está presente então x e z também deverão estar, 
# funciona para a vx, vy e vz

# vai à string e vai buscar blocos de tamanho col_size, começando no caractere com indíce start_index, transforma esse bloco num float
def get_gro_positions(line, start_index, col_size):
    
    positions = []
    # vai do inicio ao fim-1 em incrementos de coluna a coluna
    # -1 por causa do \n
    # este for vai parar quando tiver 6 valores adicionados, pode para antes caso não existam vx, vy e vz
    for i in range(start_index, len(line)-1, col_size):
        positions.append(float(line[i:i+col_size]))
    
    # while loop vai preencher com None caso não existam vx, vy e vz
    while (len(positions)) < 6:
        positions.append(None)
    
    return positions

# residue number (5 positions, integer)
# residue name (5 characters)
# atom name (5 characters)
# atom number (5 positions, integer)
# position (in nm, x y z in 3 columns, each 8 positions with 3 decimal places)
# separa a linha em diferentes "pedaços" que são a informação útil
def parse_gro_line(line):
    residue_number = int(line[:5])
    residue_name = line[5:10].strip()
    atom_name = line[10:15].strip()
    atom_number = int(line[15:20])
    # começa no caractér 20 pois apenas queremos as posições
    positions = get_gro_positions(line, 20, 8)

    return [residue_number, residue_name, atom_name , atom_number] + positions

# lê o ficheiro de acordo com o input do user
def read_gro(filepath):
    with open(filepath, 'r') as grofile:
        lines = grofile.readlines()
        # guarda o título e tamanho da caixa
        title = lines[0]
        box_size = lines[-1]

        # extrair linhas com informação relevante aos átomos
        lines = lines[2:-1]
        atoms_info = []

        for line in lines:
            atoms_info.append(parse_gro_line(line))
        
        return (title, box_size, atoms_info)

# garante que caso um elemento não ocupe os 5 caractéres, i.e. o número 1, os restantes caractéres são preenchidos por espaços
def format_str(str, spaces, alignment_right=True):
    if (len(str) > spaces):
        return str[-spaces:]
    
    # preenche os caractéres vazios com espaços à direita
    if (alignment_right):
        return str.rjust(spaces, ' ')
    
    # preenche os caractéres vazios com espaços à direita
    return str.ljust(spaces, ' ')

# garante que cada elemento (residue_number, residue_name, etc) tem 5 caractéres. tipico do ficheiro .gro
def format_int(num, spaces):
    return format_str(str(num), spaces)

# garante que cada elemento (x, y, z, vx, vy, vz) tem 8 caractéres e 3 casas decimais. tipico do ficheiro .gro
def format_float(num, spaces, decimals):
    num = round(num, decimals)
    
    return format_str("{:.{}f}".format(num, decimals), spaces)

# escreve as informações para a lista parts passando pelas funções format_int, format_str e format_float, de modo a que o ficheiro .gro seja escrito corretamente
def to_gro_line(atom):
    parts = []
    parts.append(format_int(atom['residue_number'], 5))
    parts.append(format_str(atom['residue_name'], 5, alignment_right=False)) # caso com o alinhamento à esquerda
    parts.append(format_str(atom['atom_name'], 5))
    # parts.append(format_int(atom['atom_number'], 5)) esta linha não será necessária uma vez que o ficheiro original não apresenta esta coluna
    parts.append(format_int(atom['residue_number'], 5))
    parts.append(format_float(atom['x'], 8, 3))
    parts.append(format_float(atom['y'], 8, 3))
    parts.append(format_float(atom['z'], 8, 3))
    
    # caso em que vx, vy e vz não estão presentes, preenchendo os caractéres com espaços vazios
    if not pd.isnull(atom['vx']):
        parts.append(format_float(atom['vx'], 8, 4))
    else:
        parts.append(format_str(" ", 8))
    
    if not pd.isnull(atom['vy']):        
        parts.append(format_float(atom['vy'], 8, 4))
    else: 
        parts.append(format_str(" ", 8))
    
    if not pd.isnull(atom['vz']):
        parts.append(format_float(atom['vz'], 8, 4))
    else: 
        parts.append(format_str(" ", 8))

    # junta todos os elementos da lista parts numa string
    return "".join(parts)

filepath = str(input('Insira o nome do ficheiro a ser tratado: '))

# invoca a função read_gro e guarda o seu retorno nas variaveis
gro_title, gro_box_size, atoms = read_gro(filepath)

# cria uma DataFrame com as seguintes colunas
original_df = pd.DataFrame(columns=['residue_number', 'residue_name', 'atom_name', 'atom_number', 'x', 'y', 'z', 'vx', 'vy', 'vz'], data=atoms)

important_info = []

# while loop que vai perguntando ao utilizador os seus inputs ate este estar satisfeito
while True:
    mol_name = input('Diga qual molécula: ')
    # variavel que procura na DataFrame original pela molécula introduzida pelo utilizador
    # de modo a que não seja necessario identificar o numero da mesma, analizando todas as moléculas equivalentes
    mol_df = original_df.loc[original_df['residue_name'] == mol_name]
    if mol_df.empty:
        print('Essa molécula não existe')
        continue

    atm_name = input('Diga qual átomo dessa molécula deve ser utilizado para o cálculo da distância: ')
    # função if que itera no que foi previamente feito e vai verificar todos os átomos correspondentes ao
    # input do utilizador
    if mol_df.loc[atm_name == mol_df['atom_name']].empty:
        print(f'Esse átomo não existe na molécula, {mol_name}.')
        continue
    
    # criação de um tuple que irá conter as informações relevantes para os futuros cálculos
    important_info.append((mol_name, atm_name))

    resp = input('Deseja adicionar mais moléculas e átomos? (s/n) ')
    if resp == 's':
        continue
    else: break

# variavel que irá conter o nome da superficie
sup_name = ''
while True:
    sup_name = input('Nome da superfície: ')
    # verifca se a superficie existe na DataFrame original sem haver necessidade de
    # indicar o número do grupo
    if original_df.loc[original_df['residue_name'] == sup_name].empty:
        print('Essa superfície não existe')
        continue
    break

# variavel que irá conter a informação da superficie
sup_df = original_df.loc[original_df['residue_name'] == sup_name]

# (mol1, P3), (mol2, CF2), (mol3, CF3)      apenas serão utilizados os primeiros elementos dos tuplos da lista
# [mol1, mol2, ....]
options = '|'.join(map(lambda x: x[0], important_info))
mol_rel_df = original_df.loc[original_df['residue_name'].str.contains(options)]

user_dist = float(input('Distância para a condição, em nm: '))

selected_mols = pd.DataFrame(columns=original_df.columns)

for (mol_name, atom_name) in important_info:

    # moléculas que contém o nome (FPa, por exemplo)
    mol_df = mol_rel_df.loc[mol_rel_df['residue_name'] == mol_name]
    
    residue_numbers = mol_df['residue_number'].unique()

    for residue_number in residue_numbers:
        # df que contém as linhas correspondentes aos átomos da molécula com o Grupo = mol_name
        mol_rows = mol_df.loc[mol_df['residue_number'] == residue_number]

        # a linha da molécula que tem Grupo = mol_name e o Átomo = atom_name
        atoms = mol_rows.loc[mol_rows['atom_name'] == atom_name]
        min_distance = 999999
        # o '_' é uma throwaway variable pois queremos o segundo elemento do tuplo, neste caso atomo, descartando o primeiro elemento
        for _, atom in atoms.iterrows():
            # invocar a função que determina qual é a distância entre o atomo e a superficie
            atom_distance = get_min_distance(float(atom['x']), float(atom['y']), float(atom['z']), sup_df)
            if atom_distance < min_distance:
                min_distance = atom_distance
        
        if min_distance == 999999:
            print(f'found error')
            exit()
            
        # Se a distância não for menor que a distância que o utilizador especificou
        # então avançar para a proxima molécula
        if min_distance >= user_dist:
            continue
        
        # Se a distância do átomo da molécula for menor que user_dist então adicionamos
        # a informação da molécula a selected_mols
        selected_mols = pd.concat([selected_mols, mol_rows])
    
final_df = pd.concat([selected_mols, sup_df])

filename = str(input('Insira o nome do ficheiro de saída, sem extensão: '))

# ao ficheiro output vai adicionar o titulo, número de átomos, a informação dos átomos e o tamanho da caixa de simulação
with open(f'{filename}.gro', 'w') as file:
    file.write(gro_title)
    file.write(str(len(final_df))+'\n')
    for _, atom in final_df.iterrows():
        file.write(f'{to_gro_line(atom)}\n')
    file.write(gro_box_size)