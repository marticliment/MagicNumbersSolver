import random, time

NUM_OF_DIGITS = 10   
REPS = 500             # Around 500 with pypy, around 200 with regular python
PRINT_EACH_RESULT = False

class Guess:
    N1: int = 0
    N2: int = 0
    N3: int = 0
    N4: int = 0
    
    def __init__(self):
        pass
    
    def FromString(string: str):
        self = Guess()
        self.N1 = int(string[0])
        self.N2 = int(string[1])
        self.N3 = int(string[2])
        self.N4 = int(string[3])
        return self
        
    def FromInt(x: int, y: int, z: int, w: int):
        self = Guess()
        self.N1 = x
        self.N2 = y
        self.N3 = z
        self.N4 = w
        return self
    
    def FromRandomGen():
        self = Guess()
        self.N1 = self.N2 = self.N3 = self.N4 = random.randint(0, NUM_OF_DIGITS-1)
        
        while self.N1 == self.N2:
            self.N2 = random.randint(0, NUM_OF_DIGITS-1)
        while self.N1 == self.N3 or self.N2 == self.N3: 
            self.N3 = random.randint(0, NUM_OF_DIGITS-1)
        while self.N1 == self.N4 or self.N2 == self.N4 or self.N3 == self.N4: 
            self.N4 = random.randint(0, NUM_OF_DIGITS-1)
        
        return self
         
    def __str__(self) -> str:
        return f"({self.N1},{self.N2},{self.N3},{self.N4})"
    
    def contains(self, n: int) -> bool:
        return n == self.N1 or n == self.N2 or n == self.N3 or n == self.N4
    
    def compactString(self) -> str:
        return f"{self.N1}{self.N2}{self.N3}{self.N4}"
    
    def __eq__(self, other: "Guess") -> bool:
        return other.N1 == self.N1 and other.N2 == self.N2 and other.N3 == self.N3 and other.N4 == self.N4

class Result:
    Guess: Guess
    CorrectNums: int
    TotalCoincidences: int
    
    def IsCompatible(self, other: 'Guess') -> bool:
        if self.GetTotalCoincidences(other) != self.TotalCoincidences: return False
        if self.GetCorrectNums(other) != self.CorrectNums: return False
        return True
    
    def GetTotalCoincidences(self, other: 'Guess') -> int:
        return int(self.Guess.contains(other.N1)) + \
               int(self.Guess.contains(other.N2)) + \
               int(self.Guess.contains(other.N3)) + \
               int(self.Guess.contains(other.N4))
    
    def GetCorrectNums(self, other: 'Guess') -> int:
        return int(self.Guess.N1 == other.N1) + \
               int(self.Guess.N2 == other.N2) + \
               int(self.Guess.N3 == other.N3) + \
               int(self.Guess.N4 == other.N4)

def GetPossibleCombinations() -> list[Guess]:    
    nums: list[Guess] = []
    for x in range(0, NUM_OF_DIGITS):
        for y in range(0, NUM_OF_DIGITS):
            for z in range(0, NUM_OF_DIGITS):
                for w in range(0, NUM_OF_DIGITS):
                    if (x == y or x == z or x == w or y == z or y == w or z == w): continue
                    num = Guess.FromInt(x, y, z, w)                                        
                    nums.append(num)
    return nums

def RemoveFromCombinations(OldCombis: list[Guess], LastResult: Result) -> list[Guess]:
    NewCombis: list[Guess] = []
    for num in OldCombis:
        if LastResult.IsCompatible(num):
            NewCombis.append(num)
            
    return NewCombis
        
def GetNextGuess(PossibleGuesses: list[Guess], GameHistory: list[Result]) -> Guess:
    # if len(GameHistory) == 0: return Guess.FromInt(1, 2, 3, 4)
    # else if len(GameHistory) == 1: return Guess.FromInt(8, 5, 6, 7)
    # return PossibleGuesses[0] 
    # Gettint the first element instead of a random one
    # increases average from 5.4707 to 5.5623 (tested on 1 million samples)
    return PossibleGuesses[random.randint(0, len(PossibleGuesses)-1)]

def PlayRound(MY_GUESS: Guess, NUM_TO_GUESS: Guess) -> Result:
    res = Result()
    res.Guess = MY_GUESS
    res.CorrectNums = res.GetCorrectNums(NUM_TO_GUESS)
    res.TotalCoincidences = res.GetTotalCoincidences(NUM_TO_GUESS)
    return res

def solve():    
    NUM_TO_GUESS = Guess.FromRandomGen()
    GameHistory: list[Result] = []
    PossibleGuesses: list[Guess] = GetPossibleCombinations()
    CurrentGuess = GetNextGuess(PossibleGuesses, GameHistory) # Initial Guess

    while(True):
        result = PlayRound(CurrentGuess, NUM_TO_GUESS)
        GameHistory.append(result)
        
        if result.CorrectNums == 4:
            if not(CurrentGuess.__eq__(NUM_TO_GUESS)): 
                raise Exception("FUUUUUUUUUUUUUUUUUUUUUUUUUUUCK")
            
            if PRINT_EACH_RESULT: 
                print(" Solution:", CurrentGuess, f"(original was {NUM_TO_GUESS})", f"(done in {len(GameHistory)} steps)")
            return len(GameHistory)
              
        PossibleGuesses = RemoveFromCombinations(PossibleGuesses, result)
        CurrentGuess = GetNextGuess(PossibleGuesses, GameHistory)


def to_time_str(seconds):
    mins, sec = divmod(seconds, 60)
    return f"{int(mins):02}:{sec:02.0f}"

def progressbar(it, prefix="", size=60):
    count = len(it)
    start = time.time()
    def show(j):
        x = int(size*j/count)
        elapsed = time.time() - start
        remaining = (elapsed / j) * (count - j) if j > 0 else 0
        time_str = to_time_str(remaining)
        
        if j > 0: bar = f"\r{prefix}[{'#'*x}{('_'*(size-x))}] {j/count*100:5.1f}% ETA: {time_str}"
        else: bar = f"\r{prefix}[{'#'*x}{('_'*(size-x))}] {j/count*100}% ETA: N/A"
        print(bar, end="", flush=True)
        
    show(0)
    for i, item in enumerate(it):
        yield item
        show(i+1)
    print()
    
    total_time = time.time() - start    

total = 0

STARTTIME = time.time()

print(f"Rounds: {REPS}")

divider = max(int(REPS / 1000), 1)

for i in progressbar(range(REPS // divider)):
    for j in range(divider):
        total += solve()

ENDTIME = time.time()

print(f"AVG of {REPS} rounds: {total/REPS} attempts per game (took {int((ENDTIME - STARTTIME)*100)/100} seconds)")
