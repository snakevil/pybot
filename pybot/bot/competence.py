# encoding: utf-8

class Competence(list):
    def __init__(self, *reflexes):
        if 1 == len(reflexes) and isinstance(reflexes[0], list):
            reflexes = reflexes[0]
        super(Competence, self).__init__(reflexes)

    def __str__(self):
        return type(self).__name__
