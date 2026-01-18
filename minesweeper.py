import itertools
import random
# itertools: combinations waghera banane ke kaam aata hai (AI logic mein use hota hai)
# random: random numbers generate karne ke liye (mines random place karne ke liye)


class Minesweeper():
    """
    Minesweeper game ka representation
    Yeh class actual game board aur mines handle karti hai
    """

    def __init__(self, height=8, width=8, mines=8):

        # Board ki height (rows) set kar rahe hain
        self.height = height

        # Board ki width (columns) set kar rahe hain
        self.width = width

        # Mines ko ek set mein store karenge (unique cells)
        self.mines = set()

        # Board initialize kar rahe hain (2D list)
        # False ka matlab: is cell mein mine nahi hai
        self.board = []
        for i in range(self.height):        # har row ke liye
            row = []
            for j in range(self.width):     # har column ke liye
                row.append(False)           # initially sab cells safe
            self.board.append(row)

        # Random jagah par mines add kar rahe hain
        # Jab tak required mines add na ho jayein
        while len(self.mines) != mines:

            # Random row select
            i = random.randrange(height)

            # Random column select
            j = random.randrange(width)

            # Agar is cell mein pehle mine nahi hai
            if not self.board[i][j]:

                # Mine ka coordinate set mein add kar do
                self.mines.add((i, j))

                # Board par bhi mark kar do ke yahan mine hai
                self.board[i][j] = True

        # Player ne abhi tak koi mine find nahi ki
        self.mines_found = set()

    def print(self):
        """
        Text-based board print karta hai
        X = mine
        blank = empty cell
        (Debugging / samajhne ke liye)
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):

                # Agar cell mein mine hai
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        # Cell ke coordinates nikal lo
        i, j = cell

        # Board se check karo ke mine hai ya nahi
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Diye gaye cell ke aas paas (8 neighbors)
        kitni mines hain, woh count karta hai
        """

        # Nearby mines ka counter
        count = 0

        # Cell ke around 3x3 grid check kar rahe hain
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Apne aap ko ignore karo
                if (i, j) == cell:
                    continue

                # Check karo cell board ke andar hai
                if 0 <= i < self.height and 0 <= j < self.width:

                    # Agar us jagah mine hai
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Game jeetne ki condition:
        Jo mines actual hain, wohi mines player ne find ki hon
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical sentence jo AI ke knowledge base ka hissa hoti hai

    Example:
    {(1,2), (1,3), (2,2)} = 1
    Matlab: in 3 cells mein se 1 mine hai
    """

    def __init__(self, cells, count):

        # Cells ka set (coordinates)
        self.cells = set(cells)

        # Batata hai ke in cells mein kitni mines hain
        self.count = count

    def __eq__(self, other):
        # Do sentences tab equal hain
        # jab cells aur count dono same hon
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        # Sentence ko readable string mein convert karta hai
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Yeh function logically decide karega
        kaun se cells definitely mines hain

        (Abhi implement nahi hai)
        """
        raise NotImplementedError

    def known_safes(self):
        """
        Yeh function logically decide karega
        kaun se cells definitely safe hain

        (Abhi implement nahi hai)
        """
        raise NotImplementedError

    def mark_mine(self, cell):
        """
        Jab AI ko pata chal jaye ke koi cell mine hai,
        toh is sentence se us cell ko remove karega
        aur count kam karega

        (Abhi implement nahi hai)
        """
        raise NotImplementedError

    def mark_safe(self, cell):
        """
        Jab koi cell safe prove ho jaye,
        toh sentence se remove kar diya jata hai

        (Abhi implement nahi hai)
        """
        raise NotImplementedError


class MinesweeperAI():
    """
    Yeh class AI player ko represent karti hai
    Jo logical reasoning se game khelta hai
    """

    def __init__(self, height=8, width=8):

        # Board dimensions
        self.height = height
        self.width = width

        # Jo moves AI already kar chuka hai
        self.moves_made = set()

        # Cells jo definitely mines hain
        self.mines = set()

        # Cells jo definitely safe hain
        self.safes = set()

        # Knowledge base (Sentence objects ki list)
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Kisi cell ko mine mark karta hai
        aur har sentence ko update karta hai
        """
        self.mines.add(cell)

        # Har sentence ko bata do ke yeh mine hai
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Kisi cell ko safe mark karta hai
        aur knowledge base update karta hai
        """
        self.safes.add(cell)

        # Har sentence ko bata do ke yeh safe hai
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Jab AI koi safe cell open karta hai
        aur game batata hai ke paas kitni mines hain

        Steps (sirf description):
        1) move record karo
        2) cell ko safe mark karo
        3) new logical sentence banao
        4) new safes / mines infer karo
        5) new sentences derive karo

        (Logic abhi implement nahi)
        """
        raise NotImplementedError

    def make_safe_move(self):
        """
        Koi aisa move return kare
        jo:
        - safe ho
        - pehle choose na kiya ho

        (Abhi implement nahi)
        """
        raise NotImplementedError

    def make_random_move(self):
        """
        Random move kare:
        - jo pehle choose na ho
        - jo mine known na ho

        (Abhi implement nahi)
        """
        raise NotImplementedError
