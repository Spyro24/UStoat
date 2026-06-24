#mosfu, the UStoat default text formating system

class mosfu:
    def __init__(self):
        pass
    
    def text_format(self, text):
        cursiv = False
        bold = False
        code = False
        textWords = test.split()
        output = [] #this contains the formated output
        for word in textWords: 
            if len(word) <= 1:
                output.append(("w", word)) # w is for word and than tne word
            if code and word.endwith("`"):
                output.apappend(("w", word[:-1]))
                output.append(("c", "nocode"))
            if not code and word.startswith("`"):
                output.append(("c", "nocode"))
            output.append(("w", word))