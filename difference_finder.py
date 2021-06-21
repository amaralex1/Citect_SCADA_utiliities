import difflib

file1 = open(r'C:\Users\1\Desktop\PLC code\2020_08_19 12_11(2)\КИС320.1\AI КИС320.1\AI КИС320.1.txt', 'r')
file2 = open(r'C:\Users\1\Desktop\PLC code\2020_08_19 11_41\КИС320.1\!КИС320.1Массив пересылок.txt', 'r')
diff = difflib.ndiff(file1.readlines()[2:], file2.readlines()[2:])
delta = ''.join(x for x in diff)
# print(delta)
print(difflib.SequenceMatcher(None, file1.readlines()[2:], file2.readlines()[2:]).ratio())
file2.close()
file1.close()
