import difflib

with open('symmetric n=4, x=20.csv') as text1:
    with open('test symmetric n=4, x=20.csv') as text2:
        d = difflib.Differ()
        diff = list(d.compare(text1.readlines(), text2.readlines()))
        with open('diff.txt', 'w') as diff_file:
            _diff = ''.join(diff)
            diff_file.write(_diff)