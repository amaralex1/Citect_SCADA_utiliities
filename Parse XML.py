import xml.etree.ElementTree as ET

filename = r'C:\Users\1\Desktop\test_export_mast.xpg'
tree = ET.parse(filename)
root = tree.getroot()

for program in root.findall('program'):
    identProgram = program.find('identProgram')
    name = identProgram.get('name')
    if name == "DI_Filtration_A026_A029":
        stsource = program.find('STSource').text
        program.find('STSource').text = "Hello WORLD \n" + stsource
tree.write('output.xpg', encoding='UTF-8')
