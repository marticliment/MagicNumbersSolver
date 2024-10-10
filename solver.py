import random, time
from itertools import permutations

RANGE_OF_VALUES_PER_DIGIT = 10
LENGTH_OF_NUMBERS = 4
REPS = 10000             # Around 500 with pypy, around 200 with regular python
PRINT_EACH_RESULT = False

RANGE_OF_INDEXES = list(range(LENGTH_OF_NUMBERS))

class Guess:
    Numbers: list[int] = []
    
    def __init__(self):
        self.Numbers = [0] * LENGTH_OF_NUMBERS
    
    def FromIterable(string: str | list[int] | tuple[int]):
        self = Guess()
        for i in RANGE_OF_INDEXES: self.Numbers[i] = int(string[i])
        return self
            
    def FromRandomGen():
        self = Guess()
        if LENGTH_OF_NUMBERS > RANGE_OF_VALUES_PER_DIGIT: 
            raise Exception("LENGTH_OF_NUMBERS must be smaller or equal than RANGE_OF_VALUES_PER_DIGIT")
        
        usedNumbers: set[int] = {-1}
        for i in RANGE_OF_INDEXES:
            num = -1
            while num in usedNumbers:
                num = random.randint(0, RANGE_OF_VALUES_PER_DIGIT-1)
            self.Numbers[i] = num
            usedNumbers.add(num)

        return self
         
    def __str__(self) -> str:
        s = "("
        for i in RANGE_OF_INDEXES:
            s += f"{self.Numbers[i]},"
        s += ")"
        return s
    
    def Contains(self, n: int) -> bool:
        for i in RANGE_OF_INDEXES:
            if self.Numbers[i] == n: return True
        return False
        
    def __eq__(self, other: "Guess") -> bool:
        for i in RANGE_OF_INDEXES:
            if self.Numbers[i] != other.Numbers[i]: return False
        return True
        

class Result:
    Guess: Guess
    CorrectNums: int
    TotalCoincidences: int
    
    def IsCompatible(self, other: 'Guess') -> bool:
        if self.GetTotalCoincidences(other) != self.TotalCoincidences: return False
        if self.GetCorrectNums(other) != self.CorrectNums: return False
        return True
    
    def GetTotalCoincidences(self, other: 'Guess') -> int:
        res = 0
        for i in RANGE_OF_INDEXES:
            res += 1 if self.Guess.Contains(other.Numbers[i]) else 0
        return res
    
    def GetCorrectNums(self, other: 'Guess') -> int:
        res = 0
        for i in RANGE_OF_INDEXES:
            res += 1 if self.Guess.Numbers[i] == other.Numbers[i] else 0
        return res


def GetPossibleCombinations() -> list[Guess]:    
    nums: list[Guess] = []
    for perm in permutations(range(RANGE_OF_VALUES_PER_DIGIT), LENGTH_OF_NUMBERS):
        nums.append(Guess.FromIterable(perm))
    
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

POSSIBLE_VALUES: list[Guess] = []

def solve():    
    NUM_TO_GUESS = Guess.FromRandomGen()
    GameHistory: list[Result] = []
    PossibleGuesses: list[Guess] = POSSIBLE_VALUES.copy()
    CurrentGuess = GetNextGuess(PossibleGuesses, GameHistory) # Initial Guess

    while(True):
        result = PlayRound(CurrentGuess, NUM_TO_GUESS)
        GameHistory.append(result)
        
        if result.CorrectNums == LENGTH_OF_NUMBERS:
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



STARTTIME = time.time()
POSSIBLE_VALUES = GetPossibleCombinations()
PGSBAR_DIVIDER_FACTOR = max(int(REPS / 1000), 1)
total = 0
done = 0

print(f"Planned rounds: {REPS} (Hit CTRL+C to abort at any point)")

try:
    for i in progressbar(range(REPS // PGSBAR_DIVIDER_FACTOR)):
        for j in range(PGSBAR_DIVIDER_FACTOR):
            total += solve()
            done += 1
except KeyboardInterrupt:
    print("Aborted")
    

ENDTIME = time.time()

print(f"AVG of {done} rounds: {total/done} attempts per game (took {int((ENDTIME - STARTTIME)*100)/100} seconds)")
