import random, time

NUM_OF_DIGITS = 10 # Minimum 4, maximum depends on your CPU
REPS = 100000 # Around 500 with pypy, around 200 with regular python
PRINT_EACH_RESULT = False

class PLAY:
    N1: int = 0
    N2: int = 0
    N3: int = 0
    N4: int = 0
    
    def __init__(self):
        pass
    
    def FromString(string: str):
        self = PLAY()
        self.N1 = int(string[0])
        self.N2 = int(string[1])
        self.N3 = int(string[2])
        self.N4 = int(string[3])
        return self
        
    def FromInt(x: int, y: int, z: int, w: int):
        self = PLAY()
        self.N1 = x
        self.N2 = y
        self.N3 = z
        self.N4 = w
        return self
    
    def FromRandomGen():
        self = PLAY()
        self.N1 = random.randint(0, NUM_OF_DIGITS-1)
        self.N2 = random.randint(0, NUM_OF_DIGITS-1)
        self.N3 = random.randint(0, NUM_OF_DIGITS-1)
        self.N4 = random.randint(0, NUM_OF_DIGITS-1)
        return self
         
    def __str__(self) -> str:
        return f"({self.N1},{self.N2},{self.N3},{self.N4})"
    
    def contains(self, n: int) -> bool:
        return n == self.N1 or n == self.N2 or n == self.N3 or n == self.N4
    
    def compactString(self) -> str:
        return f"{self.N1}{self.N2}{self.N3}{self.N4}"
    
bannedNumbers: list[list[int]] = [[], [], [], []]
playedCombis: list[PLAY] = []
playedResults: list[tuple[int, int]] = []


def getRandomNumber() -> str:
    num: PLAY = PLAY.FromRandomGen()
    while(num.N1 == num.N2 or num.N1 == num.N3 or num.N1 == num.N4 or num.N2 == num.N3 or num.N2 == num.N4 or num.N3 == num.N4\
        or num.N1 in bannedNumbers[0] or num.N2 in bannedNumbers[1] or num.N3 in bannedNumbers[2] or num.N4 in bannedNumbers[3]):
        num = PLAY.FromRandomGen()
                
    return num

PLAYS: list[PLAY] = []
RESULTS: list[tuple[int, int]] = []


def getPossibleCombinations() -> list[PLAY]:    
    nums: list[PLAY] = []
    for x in range(0, NUM_OF_DIGITS):
        for y in range(0, NUM_OF_DIGITS):
            for z in range(0, NUM_OF_DIGITS):
                for w in range(0, NUM_OF_DIGITS):
                    if (x == y or x == z or x == w or y == z or y == w or z == w): continue
                    if (x in bannedNumbers[0]): continue
                    if (y in bannedNumbers[1]): continue
                    if (z in bannedNumbers[2]): continue
                    if (w in bannedNumbers[3]): continue
                    
                    num = PLAY.FromInt(x, y, z, w)                                        
                    nums.append(num)
            
    return nums

def GetWrongPosCount(a: PLAY, b: PLAY) -> int:
    return (1 if a.contains(b.N1) else 0) + (1 if a.contains(b.N2) else 0) + (1 if a.contains(b.N3) else 0) + (1 if a.contains(b.N4) else 0)
    
def GetCorrectNumCount(a: PLAY, b: PLAY) -> int:
    return (1 if a.N1 == b.N1 else 0) + (1 if a.N2 == b.N2 else 0) + (1 if a.N3 == b.N3 else 0) + (1 if a.N4 == b.N4 else 0)
    
def getEqualOrBetterCombinations(combis: list[PLAY], current: PLAY, jaques, mates) -> list[PLAY]:
    if(jaques + mates == 0):
        bannedNumbers[0].append(current.N1)
        bannedNumbers[1].append(current.N2)
        bannedNumbers[2].append(current.N3)
        bannedNumbers[3].append(current.N4)
    
    new_combis_1 = []
    for entry in combis:
        if entry.N1 in bannedNumbers[0] or entry.N2 in bannedNumbers[1] or entry.N3 in bannedNumbers[2] or entry.N4 in bannedNumbers[3]: continue
        if entry in playedCombis: continue
        
        if GetWrongPosCount(entry, current) != (jaques + mates) or GetCorrectNumCount(entry, current) != mates: 
            continue
        
        new_combis_1.append(entry)
            
        
    return new_combis_1    
    
    

def compareNumbers(MY_GUESS: PLAY, NUM_TO_GUESS: PLAY) -> tuple[int, int]:
    jaque = NUM_TO_GUESS.contains(MY_GUESS.N1)
    jaque += NUM_TO_GUESS.contains(MY_GUESS.N2)
    jaque += NUM_TO_GUESS.contains(MY_GUESS.N3)
    jaque += NUM_TO_GUESS.contains(MY_GUESS.N4)

    mate = int(MY_GUESS.N1 == NUM_TO_GUESS.N1)
    mate += int(MY_GUESS.N2 == NUM_TO_GUESS.N2)
    mate += int(MY_GUESS.N3 == NUM_TO_GUESS.N3)
    mate += int(MY_GUESS.N4 == NUM_TO_GUESS.N4)

    return (jaque - mate, mate)


def getBestGuess(combis: list[PLAY]) -> PLAY:
    return combis[random.randint(0, len(combis)-1)]


def solve():
    global playedCombis, bannedNumbers, playedResults
    bannedNumbers = [[], [], [], []]
    playedCombis = []
    playedResults = []
    NUM_TO_GUESS = getRandomNumber()

    rounds: int = 0
    combis: list[PLAY] = getPossibleCombinations()

    while(True):
        rounds += 1
        current_guess = getBestGuess(combis)
        (jaque, mate) = compareNumbers(current_guess, NUM_TO_GUESS)
        
        if mate == 4:
            if PRINT_EACH_RESULT: 
                print("Solution:", combis[0], f"(original was {NUM_TO_GUESS})", f"(done in {rounds} steps)")
            return rounds
                
        playedCombis.append(current_guess)
        playedResults.append((jaque, mate))
        combis = getEqualOrBetterCombinations(combis, current_guess, jaque, mate)

import time

def to_time_str(seconds):
    mins, sec = divmod(seconds, 60)
    return f"{int(mins):02}:{sec:05.2f}"

def progressbar(it, prefix="", size=60):
    count = len(it)
    start = time.time()
    def show(j):
        x = int(size*j/count)
        elapsed = time.time() - start
        remaining = (elapsed / j) * (count - j) if j > 0 else 0
        time_str = to_time_str(remaining)
        
        bar = f"\r{prefix}[{'#'*x}{('_'*(size-x))}] {j}/{count} Est wait {time_str}"
        print(bar, end="", flush=True)
        
    for i, item in enumerate(it):
        yield item
        show(i+1)
    
    print()
    
    total_time = time.time() - start    


      
      
total = 0

STARTTIME = time.time()

divider = max(int(REPS / 100), 1)

for i in progressbar(range(REPS // divider)):
    for j in range(divider):
        total += solve()

ENDTIME = time.time()

print(f"AVG of {REPS} rounds: {total/REPS} attempts per game (took {int((ENDTIME - STARTTIME)*100)/100} seconds)")
