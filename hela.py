import sys
import re


def openFile(file_path):
    try:
        with open(file_path, 'r') as file:
            iterateLines(file.readlines())
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")


def iterateLines(file):
    lineNum = -1
    output = ""
    for line in file:
        lineNum += 1
        line = line.strip()
        line = line.strip("\n")

        # check for empty line
        if (line == "" and not PositionInfo.inTable):
            # if we are right after a headder we dont want double backslashs
            if (PositionInfo.postHeadder):
                output += "\n"
            else:
                output += "\\\\\n"
            continue

        # line is not empty, so post header is irrevelant
        PositionInfo.postHeadder = False

        # Check if there is a table
        if (not PositionInfo.inTable and line[0] == "|"):
            if (re.search(r"\|[-]*\|",  file[lineNum + 1].replace(" ", ""))):
                PositionInfo.inTable = True

        # if we are in a table, find out the length of it
        if (PositionInfo.inTable):
            if (line != "" and line[0] == "|"):
                PositionInfo.MdTable.append(line)
                continue
            else:  # table ended, so add converted table to output
                output += (markdown_table_to_latex(PositionInfo.MdTable))
                PositionInfo.inTable = False
                PositionInfo.MdTable = []

        # Check if the line contains $$, then we dont
        # need linebreaks in that scope
        if ("$$" in line):
            PositionInfo.inDoubleDollar = not PositionInfo.inDoubleDollar
            # check if we have an align block, we dont need that line then
            if (PositionInfo.inDoubleDollar and "\\begin{align" in file[lineNum + 1]):
                continue  # next line align check
            if (lineNum != 0 and not PositionInfo.inDoubleDollar and "\\end{align" in file[lineNum-1]):
                continue

            output += (line + "\n")
            continue

        # handle Headings
        if len(line) >= 2 and line[:2] == "# ":
            output += ("\\section*{" + line[2:] + "}\n")
            PositionInfo.postHeadder = True
            continue
        elif len(line) >= 3 and line[:3] == "## ":
            output += ("\\subsection*{" + line[3:] + "}\n")
            PositionInfo.postHeadder = True
            continue
        elif len(line) >= 4 and line[:4] == "### ":
            output += ("\\subsubsection*{" + line[4:] + "}\n")
            PositionInfo.postHeadder = True
            continue

        if (PositionInfo.inDoubleDollar):
            output += (line + "\n")
            continue
        output += (line + " \\\\\n")

    output = output.replace("\\begin{align}", "\\begin{align*}")
    output = output.replace("\\end{align}", "\\end{align*}")
    print(output)


# info about the point in Document where we are converting
class PositionInfo:
    inDoubleDollar = False
    inTable = False
    postHeadder = True
    MdTable = []


def markdown_table_to_latex(markdownArr):
    rows = len(markdownArr)

    # get coloum num
    coloums = markdownArr[1].count("|") - 1

    out = "\\begin{tabular}{|"
    for i in range(coloums):
        out += "c|"
    out += "}"
    out += "\n\\hline\n"

    def rowToLatex(thisRow):
        return (thisRow.strip()[1:len(thisRow)-1]).replace("|", " & ")+" \\\\"

    # header
    out += rowToLatex(markdownArr[0]) + "\n\\hline\n\\hline\n"

    # rest
    for i in range(2, rows):
        out += rowToLatex(markdownArr[i]) + "\n\\hline\n"

    out += "\\end{tabular}\\\\\n"
    return out


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python hela.py <file_path>")
    else:
        file_path = sys.argv[1]
        openFile(file_path)
