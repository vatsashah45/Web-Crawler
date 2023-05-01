import re

class Indexer:
    def __init__(self, n: int) -> None:
        self.currentTermIndex = 0
        self.n = n

    def removeSpecialChars(self, term: str):
        return re.sub(r'[^a-zA-Z0-9]','', term)

    def processPage(self, index: dict[str, list[int]], termIndexMap: dict[str, int], text: str, id: int):
        terms = text.split()
        for term in terms:
            editedTerm = self.removeSpecialChars(term)
            if (editedTerm == ""):
                continue
            if (editedTerm not in termIndexMap):
                termIndexMap[editedTerm] = self.currentTermIndex
                self.currentTermIndex += 1
            if (editedTerm not in index):
                index[editedTerm] = []
            if (id not in index[editedTerm]):
                index[editedTerm].append(id)

    def build(self):
        termIndexMap: dict[str, int] = {}
        index: dict[str, list[int]] = {}
        for i in range(0, self.n):
            text = open('pages/' + str(i) + '.txt', 'r').read()
            self.processPage(index, termIndexMap, text, i)
        return (index, termIndexMap)