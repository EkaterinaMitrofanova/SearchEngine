import os
import pymorphy2

morph = pymorphy2.MorphAnalyzer()


def main():
    directory = 'docs/'
    files = os.listdir(directory)
    for file in files:
        f = open('%s/%s' %(directory, file), 'r')
        doc_file = open('lemma/%s' % os.path.split(f.name)[1], 'w')
        for line in f:
            for word in line.split():
                if word.isdigit() or word.isalpha():
                    doc_file.write(morph.parse(word)[0].normal_form + " ")
        doc_file.close()
        print(doc_file.name)
        f.close()


def get_lem(word: str) -> str:
    return morph.parse(word)[0].normal_form


if __name__ == "__main__":
    main()
