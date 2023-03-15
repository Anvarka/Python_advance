# написать все без for в общем
from typing import List
import figureast
from pdflatex import PDFLaTeX


def rowwer(column_amount):
    def table_row(row: List):
        r = len(row)
        row = map(str, row)
        return " & ".join(row) + " & " * (column_amount - r) + " \\\\ \n\\hline"
    return table_row


def wrapper_document(rows, image):
    return "\n".join(['\\documentclass{article}',
                      '\\usepackage{graphicx}',
                      "\\begin{document}",
                      f"{wrapper_table(rows)}",
                      f"{wrapper_image(image)}",
                      "\\end{document}"
                      ])


def wrapper_table(rows):
    column_amount = max(map(len, rows))
    func = rowwer(column_amount)
    columns = "{" + "|c" * column_amount + "}"
    return "\n".join(["\\begin{table}[]",
                      "\\centering",
                      "\\begin{tabular}" + columns,
                      "\\hline",
                      "\n".join(map(func, rows)),
                      "\\end{tabular}",
                      "\\end{table}",
                      ])


def wrapper_image(image):
    return f"\\includegraphics[width=\\textwidth]{{{image}}}\n"

# def build():
#     os.system(
#         f"cd artifacts_host && xelatex -interaction=nonstopmode -halt-on-error -output-directory . {name}.tex && "
#         f"rm {name}.aux {name}.log")


if __name__ == '__main__':
    # rows = [[1, "cat", 3, 4, 5], [2, 3, 6], ["\$\%", "`g"]]
    # image = 'artifacts/ast_tree.png'
    # figureast.get_plot(image)
    # with open('artifacts/latex.tex', 'w') as tex:
    #     tex.write(wrapper_document(rows, image))

    pdfl = PDFLaTeX.from_texfile("artifacts/latex.tex")
    pdfl.create_pdf()
