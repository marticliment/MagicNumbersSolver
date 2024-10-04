import random, time

NUM_OF_DIGITS = 4 
# Minimum 4, maximum depends on your CPU

class PLAY:
    N1: int = 0
    N2: int = 0
    N3: int = 0
    N4: int = 0
    
    def randomGen(self):
        self.N1 = random.randint(0, NUM_OF_DIGITS-1)
        self.N2 = random.randint(0, NUM_OF_DIGITS-1)
        self.N3 = random.randint(0, NUM_OF_DIGITS-1)
        self.N4 = random.randint(0, NUM_OF_DIGITS-1)
         
    def __str__(self) -> str:
        return f"{self.N1},{self.N2},{self.N3},{self.N4}"
    
    def contains(self, n: int) -> bool:
        return self.count(n) > 0
    
    def count(self, n: int) -> int:
        return int(n == self.N1) + int(n == self.N2) + int(n == self.N3) + int(n == self.N4)
    


bannedNumbers: list[list[int]] = [[], [], [], []]
bannedCombis: list[PLAY] = []



def getRandomNumber() -> str:
    num: PLAY = PLAY()
    num.randomGen()
    while(num.N1 == num.N2 or num.N1 == num.N3 or num.N1 == num.N4 or num.N2 == num.N3 or num.N2 == num.N4 or num.N3 == num.N4\
        or num.N1 in bannedNumbers[0] or num.N2 in bannedNumbers[1] or num.N3 in bannedNumbers[2] or num.N4 in bannedNumbers[3]):
        num.randomGen()
                
    return num

def getPossibleCombinations() -> list[PLAY]:    
    nums: list[PLAY] = []
    for x in range(0, NUM_OF_DIGITS):
        for y in range(0, NUM_OF_DIGITS):
            for z in range(0, NUM_OF_DIGITS):
                for w in range(0, NUM_OF_DIGITS):
                    num = PLAY()
                    num.N1 = x
                    num.N2 = y
                    num.N3 = z
                    num.N4 = w
                    
                    if (num.N1 == num.N2 or num.N1 == num.N3 or num.N1 == num.N4 or num.N2 == num.N3 or num.N2 == num.N4 or num.N3 == num.N4): continue
                    if (num.N1 in bannedNumbers[0]): continue
                    if (num.N2 in bannedNumbers[1]): continue
                    if (num.N3 in bannedNumbers[2]): continue
                    if (num.N4 in bannedNumbers[3]): continue
                    
                    nums.append(num)
        
    return nums

def getCoincidingNumbers(a: PLAY, b: PLAY):
    return (1 if a.contains(b.N1) else 0) + (1 if a.contains(b.N2) else 0) + (1 if a.contains(b.N3) else 0) + (1 if a.contains(b.N4) else 0)
    
def getCoincidingNumbersWithPositions(a: PLAY, b: PLAY):
    return (1 if a.N1 == b.N1 else 0) + (1 if a.N2 == b.N2 else 0) + (1 if a.N3 == b.N3 else 0) + (1 if a.N4 == b.N4 else 0)
    
    
def getEqualOrBetterCombinations(combis: list[PLAY], current: PLAY, jaques, mates) -> list[PLAY]:
    if(jaques + mates == 0):
        bannedNumbers[0].append(current.N1)
        bannedNumbers[1].append(current.N2)
        bannedNumbers[2].append(current.N3)
        bannedNumbers[3].append(current.N4)
    
    new_combis_4 = []
    new_combis_3 = []
    new_combis_2 = []
    new_combis_1 = []
    for entry in combis:
        if entry.N1 in bannedNumbers[0] or entry.N2 in bannedNumbers[1] or entry.N3 in bannedNumbers[2] or entry.N4 in bannedNumbers[3]: continue
        if entry in bannedCombis: continue
        
        if getCoincidingNumbers(entry, current) == (jaques + mates) and getCoincidingNumbersWithPositions(entry, current) == mates: 
            new_combis_1.append(entry)
        if getCoincidingNumbers(entry, current) >= (jaques + mates) and getCoincidingNumbersWithPositions(entry, current) == mates: 
            new_combis_2.append(entry)
        if getCoincidingNumbers(entry, current) == (jaques + mates) and getCoincidingNumbersWithPositions(entry, current) >= mates: 
            new_combis_3.append(entry)
        if getCoincidingNumbers(entry, current) >= (jaques + mates) and getCoincidingNumbersWithPositions(entry, current) >= mates: 
            new_combis_4.append(entry)
        
    if(len(new_combis_1) > 0): return new_combis_1    
    if(len(new_combis_2) > 0): return new_combis_2    
    if(len(new_combis_3) > 0): return new_combis_3
    return new_combis_4   
    
    

def compareNumbers(MY_GUESS: PLAY, NUM_TO_GUESS: PLAY) -> tuple[int, int]:
    jaque = NUM_TO_GUESS.count(MY_GUESS.N1)
    jaque += NUM_TO_GUESS.count(MY_GUESS.N2)
    jaque += NUM_TO_GUESS.count(MY_GUESS.N3)
    jaque += NUM_TO_GUESS.count(MY_GUESS.N4)

    mate = int(MY_GUESS.N1 == NUM_TO_GUESS.N1)
    mate += int(MY_GUESS.N2 == NUM_TO_GUESS.N2)
    mate += int(MY_GUESS.N3 == NUM_TO_GUESS.N3)
    mate += int(MY_GUESS.N4 == NUM_TO_GUESS.N4)

    return (jaque - mate, mate)


def getBestGuess(combis) -> str:
    return combis[random.randint(0, len(combis)-1)]


def solve():
    global bannedCombis, bannedNumbers
    # ["6","7","8","9"], ["6","7","8","9"], ["6","7","8","9"], ["6","7","8","9"]
    bannedNumbers = [[], [], [], []]
    bannedCombis = []
    NUM_TO_GUESS = getRandomNumber()

    rounds: int = 0
    combis: list[PLAY] = getPossibleCombinations()
    current_guess = getBestGuess(combis)

    while(True):
        rounds += 1
        (jaque, mate) = compareNumbers(current_guess, NUM_TO_GUESS)
        
        if mate == 4:
            print("Solution:", combis[0], f"(original was {NUM_TO_GUESS})", f"(done in {rounds} steps)")
            return rounds
                
        bannedCombis.append(current_guess)
        combis = getEqualOrBetterCombinations(combis, current_guess, jaque, mate)
        current_guess = getBestGuess(combis)

      
print("BEGIN")
total = 0

REPS = 1000
STARTTIME = time.time()

for i in range(REPS):
    total += solve()

ENDTIME = time.time()

print(f"AVG of {REPS} rounds: {total/REPS} ({(ENDTIME - STARTTIME)*100/100} seconds)")
