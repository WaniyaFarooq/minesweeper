import itertools
import random

class Minesweeper():
    def __init__(self, height=8, width=8, mines=8):
        self.height = height
        self.width = width
        self.mines = set()
        self.board = []
        
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)
        
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True
        
        self.mines_found = set()

    def print(self):
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        count = 0
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):
                if (i, j) == cell:
                    continue
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1
        return count

    def won(self):
        return self.mines_found == self.mines


class Sentence():
    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        if len(self.cells) == self.count and len(self.cells) > 0:
            return set(self.cells)
        return set()

    def known_safes(self):
        if self.count == 0:
            return set(self.cells)
        return set()

    def mark_mine(self, cell):
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1

    def mark_safe(self, cell):
        if cell in self.cells:
            self.cells.remove(cell)


class MinesweeperAI():
    def __init__(self, height=8, width=8):
        self.height = height
        self.width = width
        self.moves_made = set()
        self.mines = set()
        self.safes = set()
        self.knowledge = []

    def mark_mine(self, cell):
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        # Step 1: Move record karo
        self.moves_made.add(cell)
        
        # Step 2: Cell ko safe mark karo
        self.mark_safe(cell)
        
        # Step 3: New sentence create karo (neighbors ke liye)
        i, j = cell
        neighbors = set()
        
        for row in range(i-1, i+2):
            for col in range(j-1, j+2):
                if (row, col) == cell:
                    continue
                if 0 <= row < self.height and 0 <= col < self.width:
                    neighbors.add((row, col))
        
        # Step 4: Adjust count - jo mines already pata hain unhe subtract karo
        mine_count = 0
        for neighbor in list(neighbors):
            if neighbor in self.mines:
                mine_count += 1
                neighbors.remove(neighbor)
            elif neighbor in self.safes:
                neighbors.remove(neighbor)
        
        # New sentence add karo
        if len(neighbors) > 0:
            new_sentence = Sentence(neighbors, count - mine_count)
            self.knowledge.append(new_sentence)
        
        # Step 5: Inference karo (new mines/safes find karo)
        self.update_knowledge()
        
        # Step 6: Subset inference karo
        self.infer_from_subsets()

    def update_knowledge(self):
        """Knowledge base se new safes aur mines find karta hai"""
        
            
            # Knowledge base ko clean karo (empty sentences remove karo)
        self.knowledge = [s for s in self.knowledge if len(s.cells) > 0]
            
            # Har sentence se safes aur mines nikalo
        for sentence in self.knowledge:
                known_mines = sentence.known_mines()
                known_safes = sentence.known_safes()
                
                # Mark karo jo cells mines hain
                for mine in list(known_mines):
                    if mine not in self.mines:
                        self.mark_mine(mine)
                        
                
                # Mark karo jo cells safe hain
                for safe in list(known_safes):
                    if safe not in self.safes:
                        self.mark_safe(safe)
                        

    def infer_from_subsets(self):
        """Subset inference rule use karta hai"""
        new_sentences = []
        
        for i in range(len(self.knowledge)):
            for j in range(len(self.knowledge)):
                if i == j:
                    continue
                
                sentence1 = self.knowledge[i]
                sentence2 = self.knowledge[j]
                
                # Check karo ke sentence1, sentence2 ka subset hai
                if sentence1.cells.issubset(sentence2.cells):
                    new_cells = sentence2.cells - sentence1.cells
                    new_count = sentence2.count - sentence1.count
                    
                    if len(new_cells) > 0:
                        new_sentence = Sentence(new_cells, new_count)
                        if new_sentence not in self.knowledge:
                            new_sentences.append(new_sentence)
        
        # Add new sentences to knowledge base
        for sentence in new_sentences:
            self.knowledge.append(sentence)
        
        # Fir se update karo agar new sentences add hue hain
        if new_sentences:
            self.update_knowledge()

    def make_safe_move(self):
        """
        Koi aisa move return kare
        jo:
        - safe ho
        - pehle choose na kiya ho
        """
        for cell in self.safes:
            if cell not in self.moves_made and cell not in self.mines:
                return cell
        return None

    def make_random_move(self):
        """
        Random move kare:
        - jo pehle choose na ho
        - jo mine known na ho
        """
        possible_moves = []
        
        for i in range(self.height):
            for j in range(self.width):
                cell = (i, j)
                if (cell not in self.moves_made and 
                    cell not in self.mines):
                    possible_moves.append(cell)
        
        if not possible_moves:
            return None
        
        return random.choice(possible_moves)