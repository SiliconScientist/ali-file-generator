# Title: Ali File Generator
# Description: Take a txt file containing sequences and turn them into ali files
# Author: Avery Hill
# Last modified: 08/09/2021

import os

# Obtain the information needed to name the ali files with the format: 'to_align_AsubGyrABCC.ali'

# Function should take sequence header ('>_Aequorivita_sublithincola_gyra_2509583882')
def get_sequence_id(sequence_header):
    sequence_id = [None] * len(sequence_header)
    for i, header in enumerate(sequence_header):
        
        # Split function using '_' ('>', 'Aequorivita', 'sublithincola', 'gyra', '2509583882')
        # Save elements 1-3 ('Aequorivita', 'sublithincola', 'gyra')
        first = header.split('_')[1]
        second = header.split('_')[2]
        third = header.split('_')[3]
        
#         fourth is some number id plus an endline (i.e. "XXXXXXXXXX\n")
        fourth = header.split('_')[4].rstrip('\n')
        
        # Save identifing letters ('A', 'sub', 'gyra')
        first = first[0]
        second = second[0:3]
        
        # Turn 'gyra' into 'GyrA'
        third, result = third.title(), ""
        for word in third.split():
            result += word[:-1] + word[-1].upper() + " "
        third = result[:-1]
        
        letter_ids = [first, second, third, domain_id, '_', fourth]
        sequence_id[i] = ''.join(letter_ids)
    return sequence_id

def make_dir(dir_name):
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)

def create_ali_file(sequnce_id):

    # Straightforward way (courtesy of Avery)
#   file_output = ''.join(['>P1;', template_info[0], '\n', template_info[1], 
#                          '\n', template_info[2], '*\n\n>P1;', sequence_id[i], 
#                          '\nsequence:', sequence_id[i], '::::::::\n', sequences[i], '*'])

    # Complicated way (courtesy of Elliot)
    file_format = ['>P1;', '\n', '\n', '*\n\n>P1;', '\nsequence:', '::::::::\n', '*']
    info = [template_info + (2 * [seq_id]) + [seq] + [''] for seq_id, seq in zip(sequence_id, sequences)]
    

    for i, seq_id in zip(info, sequence_id):
        file_output = ''.join(''.join(x) for x in zip(file_format, i))
        file_name = 'to_align_' + seq_id + '.ali'
        with open(f'/Users/averyhill/MyDocuments/schoeffler_research_summer_2021/pdbs/pdb_generation_code/{directory_name}/{file_name}', 'a') as f:
            f.write(file_output)

# Manually enter the E. Coli. template information 
template_info = [None] * 3

# template_info[0] (e.g. >P1;1ab4)
print('What is the protein id (e.g. 1ab4, 4pu9): ')
# template_info[0] = input()
template_info[0] = '1ab4'


# template_info[1] (e.g. structureX:1ab4:30:A:522:A:GyrA BCC:Escherichia coli:2.8:)
print('What is the structureX line: ')
# template_info[1] = input()
template_info[1] = 'structureX:1ab4:30:A:522:A:GyrA BCC:Escherichia coli:2.8:'

# template_info[2] (Copy/paste sequence, replace characters with dashes where the sequence is unresolved in PyMol)
print('Paste the sequence (include dashes where unresolved): ')
template_info[2] = 'VGRALPDVRDGLKPVHRRVLYAMNVLGNDWNKAYKKSARVVGDVIGKYHPHGDSAVYDTIVRMAQPFSLRYMLVDGQGNFGSIDGDSAAAMRYTEIRLAKIAHELMADLEKETVDFVDNYDGTEKIPDVMPTKIPNLLVNGSSGIAVGMATNIPPHNLTEVINGCLAYIDDEDISIEGLMEHIPGPDFPTAAIINGRRGIEEAYRTGRGKVYIRARAEVEV------ETIIVHEIPYQVNKARLIEKIAELVKEKRVEGISALRDESDKDGMRIVIE------GEVVLNNLYSQTQLQVSFGINMVALHHGQPKIMNLKDIIAAFVRHRREVVTRRTIFELRKARDRAHILEALAVALANIDPIIELIRHAPTPAEAKTALVANPWQLGNVAAMLE----DAARPEWLEPEFGVRDGLYYLTEQQAQAILDLRLQKLTGLEHEKLLDEYKELLDQIAELLRILGSADRLMEVIREELELVREQFGDKRRTEIT'

# Perhaps we manually enter BCC or ATP?

# Domain_identifier = 'BCC'

print('Enter the domain ID (e.g. BCC, ATP, etc.): ')
# domain_id = input()
domain_id = 'BCC'

directory_name = 'test_ali_files'

# Open text file with sequences and sequence headers

infile = open('test_text_file.txt', 'r')
# for i in range():
#     print(infile.readline())
lines = infile.readlines()

organism_count = 0
for line in lines:
    if (line[0] == '>'):
        organism_count += 1
        
sequence_header = [None] * organism_count
sequences = [None] * organism_count

count = 0
for i, line in enumerate(lines):
    if (line[0] == '>'):
        sequence_header[count] = lines[i]
        sequences[count] = lines[i + 1].rstrip('\n')
        count += 1

sequence_id = get_sequence_id(sequence_header)
make_dir(f'/Users/averyhill/MyDocuments/schoeffler_research_summer_2021/pdbs/pdb_generation_code/{directory_name}')
create_ali_file(sequence_id)