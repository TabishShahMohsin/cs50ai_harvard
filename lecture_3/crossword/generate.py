import sys

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        _, _, w, h = draw.textbbox((0, 0), letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        for i in self.domains:
            unvalid = set()
            for j in self.domains[i]:
                if i.length != len(j):
                    unvalid.add(j)
            self.domains[i] -= unvalid

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        change = False
        intersection = self.crossword.overlaps[(x, y)]
        if intersection == None:
            return False

        (i, j) = intersection
        unvalid = set()
        for word1 in self.domains[x]:
            validity = False
            for word2 in self.domains[y]:
                if word1[i] == word2[j]:
                    validity = True
                    break
            if validity == False:
                unvalid.add(word1)
                change = True

        self.domains[x] -= unvalid

        return change

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        if arcs == None:
            arcs = list(self.crossword.overlaps.keys())
            '''
            arcs = list()
            for i in self.domains:
                for j in self.domains:
                    if i==j:
                        continue
                    arcs.append((i, j))
            '''

        while 0 < len(arcs):
            arc = arcs.pop()
            revision = self.revise(arc[0], arc[1])
            if len(self.domains[arc[0]]) == 0:
                return False
            if revision:
                for neighbour in self.crossword.neighbors(arc[0]):
                    if neighbour == arc[1]:
                        continue
                    arcs.append((neighbour, arc[0]))
        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        for var in self.domains:
            if var not in assignment:
                return False
        return True

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        values = set()
        for var in assignment:
            value = assignment[var] 

            # Check length
            if len(value) != var.length:
                return False
            # Check if re-using values
            if value in values:
                return False
            values.add(value)
            # Check if conflict
            for neighbor in self.crossword.neighbors(var):
                if neighbor in assignment:
                    value = assignment[neighbor]
                    (i, j) = self.crossword.overlaps[var, neighbor]
                    if assignment[var][i] != assignment[neighbor][j]:
                        return False
        return True

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        # values notes the corresponding rulles out value of every word in the domain of the variable
        values = dict()
        neighbors = self.crossword.neighbors(var)
        for value in self.domains[var]:
            contradict = 0
            for i in neighbors:
                # Already assigned value should not be considered with the contradictions
                if i in assignment:
                    continue
                p, q = self.crossword.overlaps[var, i]
                for j in self.domains[i]:
                    if value[p] != j[q]:
                        contradict += 1
                values[value] = contradict

        # Sorting in the basis of no. of contradictions
        return sorted(values, key=lambda value: values[value])

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        value_count = float("inf")
        for i, j in self.domains.items():
            # Checking len and if it is unassigned
            if i not in assignment and len(j) <= value_count:
                if len(j) == value_count and self.crossword.neighbors(i) > self.crossword.neighbors(variable):
                    # If len is same, then no. of neighbor should be less for the selected variable hence continue if not so
                    continue
                variable = i
                value_count = len(j)
        return variable

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        # Defining recursion end
        if self.assignment_complete(assignment):
            return assignment
        # Gerring the unassigned_variable and checking all possible ways
        var = self.select_unassigned_variable(assignment)
        for value in self.domains[var]:
            as_copy = assignment
            as_copy[var] = value
            # Checking if this choice satisfies our previoius choices
            if self.consistent(as_copy):
                assignment[var] = value
                # Checking all possible ways after it using recursion
                result = self.backtrack(assignment)
                if result != None:
                    return result
                assignment.pop(var)
        return None


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
