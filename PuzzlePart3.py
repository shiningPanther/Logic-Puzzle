'''

Three players A, B, C play the following game. First, A picks a real number between 0 and 1 (both inclusive), 
then B picks a number in the same range (different from A’s choice) 
and finally C picks a number, also in the same range, (different from the two chosen numbers). 
We then pick a number in the range uniformly randomly. Whoever’s number is closest to this random number wins the game. 
Assume that A, B and C all play optimally and their sole goal is to maximise their chances of winning. 
Also assume that if one of them has several optimal choices, then that player will randomly pick one of the optimal choices.

1. If A chooses 0, then what is the best choice for B?
2. What is the best choice for A?
3. Can you write a program to figure out the best choice for the first player when the game is played among four players?

'''


'''
#########################################################################

We approach the problem the following way:
- We iterate through all the possible plays for players A, B, and C
- For each of these plays, we calculate the optimal play for player D and calculate the corresponding probabilities for players A, B, and C to win 
- We can then calculate the optimal play for player C for a given play of players A and B, and optimal play of player D
- We continue this process to calculate the optimal play for player B for a given play by player A and optimal plays of players C and D
- Finally, we can calculate the optimal play for player A for optimal plays of players B, C, D

Notes:
- For reasonable computation times, we have to divide the range between 0 and 1 into 100 parts (set N = 100)
- Once a rough solution has been found (0.17 for player A in this problem) we can increase the resolution around the optimal plays of all players in order find more precise value.
- It is important to always keep the numbers of player D over the complete range 0 to 1 since it's optimal position varies strongly depending on the other players and ultimately this effects the optimal play of all players.

########################################################################
'''




# This function calculates the optimal play for player D (for a given player of players A, B, C) and returns this optimal number, as well as the probabilities to win for all players
def bestPlayD (numberA, numberB, numberC, N):
	probDMax = 0.0
	bestNumberD = 0.0
	numberOfPossibilities = 1 # numberOfPossibilities counts the possibilities for player D to choose a number, which has the same probability of winning
	# go through all numbers and determine, which one is the best.
	for d in range(N+1):
		numberD = d/N
	#for d in range(1000):
		#numberD = d/1000
		# same number as A, B or C cannot be chosen
		if numberD == numberA or numberD == numberB or numberD == numberC:
			continue

		probD = getProb(numberD, numberA, numberB, numberC)

		# If it is the 'best play' calculate also the probabilities for the other players
		if probD > probDMax:
			probDMax = probD
			bestNumberD = numberD
			probC = getProb(numberC, numberA, numberB, numberD)
			probB = getProb(numberB, numberA, numberC, numberD)
			probA = getProb(numberA, numberB, numberC, numberD)
			numberOfPossibilities = 1

		# If there are several possibilities for the 'best play' take the average of all values
		elif probD == probDMax:
			numberOfPossibilities += 1
			probCNew = getProb(numberC, numberA, numberB, numberD)
			probC = (probC * (numberOfPossibilities - 1) + probCNew) / numberOfPossibilities
			probBNew = getProb(numberB, numberA, numberC, numberD)
			probB = (probB * (numberOfPossibilities - 1) + probBNew) / numberOfPossibilities
			probANew = getProb(numberA, numberB, numberC, numberD)
			probA = (probA * (numberOfPossibilities - 1) + probANew) / numberOfPossibilities
			# We take the average of the numbers since typically D has a range of choices that yield the same winning probabilities - we want to know the average position
			bestNumberD = (bestNumberD * (numberOfPossibilities - 1) + numberD) / numberOfPossibilities

			probC = round(probC, decimals)
			probB = round(probB, decimals)
			probA = round(probA, decimals)
			bestNumberD=round(bestNumberD,decimals)

		if (probA + probB + probC + probD)-1.0 > 0.001:
			print('Somehting is wrong in calculating probabilities')

	return (bestNumberD, probDMax, probC, probB, probA)


# Get the probability of a certain number
# The first argument is the number to get the probability for
# The other three arguments are the other numbers (don't need to be in order)
def getProb (numberToGet, number1, number2, number3):
	prob = 0.0
	# if numberToGet is the smallest number
	if min(numberToGet, number1, number2, number3) == numberToGet:
		prob += (min(number1, number2, number3) - numberToGet) / 2
		prob += numberToGet
	# if numberToGet is the largest number
	elif max(numberToGet, number1, number2, number3) == numberToGet:
		prob += (numberToGet - max(number1, number2, number3)) / 2
		prob += 1-numberToGet
	
	# if numberToGet is between the other numbers - this could be optimized...
	# First, number1 is the smallest number
	elif min(number1, number2, number3) == number1:
		# Number1 smallest, number3 largest
		if max(number2, number3) == number3:
			# Number1 < number2 < numberToGet < number3
			if numberToGet > number2:
				prob += (number3 - number2) / 2
			# Number1 < numberToGet < number2 < number3
			else:
				prob += (number2-number1) / 2
		# Number1 smallest, number2 largest
		else:
			if numberToGet > number3:
				prob += (number2 - number3) / 2
			else:
				prob += (number3-number1) / 2
	# Now, number2 is the smallest number
	elif min(number1, number2, number3) == number2:
		# Number2 smallest, number3 largest
		if max(number1, number3) == number3:
			if numberToGet > number1:
				prob += (number3 - number1) / 2
			else:
				prob += (number1-number2) / 2
		# Number2 smallest, number1 largest
		else:
			if numberToGet > number3:
				prob += (number1 - number3) / 2
			else:
				prob += (number3-number2) / 2
	# Finally, number3 is the smallest number
	elif min(number1, number2, number3) == number3:
		# Number3 smallest, number2 largest
		if max(number1, number2) == number2:
			if numberToGet > number1:
				prob += (number2 - number1) / 2
			else:
				prob += (number1-number3) / 2
		# Number3 smallest, number1 largest
		else:
			if numberToGet > number2:
				prob += (number1 - number2) / 2
			else:
				prob += (number2-number3) / 2
	else:
		print('Something did not work out...')
	return round(prob,decimals)



#############################################################################
#
#
# START OF MAIN FUNCTION
#
#
#############################################################################


# We divide the range 0 to 1 in N + 1 points
N = 100
decimals = 4

# First, player A chooses a number
probAMax = 0.0
# It is enough to go until N/2 since the problem is symmetric	
for a in range(int(N/2)+1): 
	numberA = a/N
#for a in range(21):
	#numberA = 0.16 + a/1000

	# Now, player B chooses a number
	probBMax = 0.0
	numberOfPossibilitesB = 1
	for b in range(N+1):
		numberB = b/N
	#for b in range(21):
		#numberB = 0.82 + b/1000
		# Two players cannot choose the same number
		if numberB == numberA:
			continue

		# Now, player C chooses a number
		probCMax = 0.0
		numberOfPossibilitesC = 1
		for c in range(N+1):
			numberC = c/N
		#for c in range(21):
			#numberC = 0.49 + c/1000
			# Two players cannot choose the same number
			if numberC == numberA or numberC == numberB:
				continue

			bestNumberD, bestProbD, probC, probB, probA = bestPlayD(numberA, numberB, numberC, N)

			# A new best play for C has been found for a given play of A and B (D is always playing best)
			if probC > probCMax:
				probCMax = probC
				bestNumberDBestPlayC = bestNumberD
				bestNumberCBestPlayC = numberC
				probDBestPlayC = bestProbD
				probCBestPlayC = probC
				probBBestPlayC = probB
				probABestPlayC = probA
				numberOfPossibilitesC = 1

			# There are several best plays for C for given numbers A and B (and best play of player D)
			elif probC == probCMax:
				numberOfPossibilitesC += 1
				probDBestPlayC = (probDBestPlayC * (numberOfPossibilitesC - 1) + bestProbD) / numberOfPossibilitesC
				probBBestPlayC = (probBBestPlayC * (numberOfPossibilitesC - 1) + probB) / numberOfPossibilitesC
				probABestPlayC = (probABestPlayC * (numberOfPossibilitesC - 1) + probA) / numberOfPossibilitesC
				# We take the average of the numbers since typically C has a range of choices that yield the same winning probabilities - we want to know the average position
				bestNumberCBestPlayC = (bestNumberCBestPlayC * (numberOfPossibilitesC - 1) + numberC) / numberOfPossibilitesC

				probDBestPlayC = round(probDBestPlayC,decimals)
				probBBestPlayC = round(probBBestPlayC,decimals)
				probABestPlayC = round(probABestPlayC,decimals)
				bestNumberCBestPlayC = round(bestNumberCBestPlayC,decimals)


		# A new best play for B has been found for given play of A and optimal play of C and D
		if probBBestPlayC > probBMax:
			probBMax = probBBestPlayC
			probDBestPlayAll = probDBestPlayC
			probCBestPlayAll = probCBestPlayC
			probBBestPlayAll = probBBestPlayC
			probABestPlayAll = probABestPlayC
			bestNumberBBestPlayAll = numberB
			bestNumberCBestPlayAll = bestNumberCBestPlayC
			bestNumberDBestPlayAll = bestNumberDBestPlayC
			numberOfPossibilitesB = 1

		# If there are several best plays for B, we need to take the average
		elif probBBestPlayC == probBMax:
			numberOfPossibilitesB += 1
			probDBestPlayAll = (probDBestPlayAll * (numberOfPossibilitesB - 1) + probDBestPlayC) / numberOfPossibilitesB
			probCBestPlayAll = (probCBestPlayAll * (numberOfPossibilitesB - 1) + probCBestPlayC) / numberOfPossibilitesB
			probBBestPlayAll = (probBBestPlayAll * (numberOfPossibilitesB - 1) + probBBestPlayC) / numberOfPossibilitesB
			probABestPlayAll = (probABestPlayAll * (numberOfPossibilitesB - 1) + probABestPlayC) / numberOfPossibilitesB
			# Note: Here we don't take the average of the numbers, since typically B has some discrecte choices (for example if player A chooses to start with 0.5)
			# The average value of these two choices does not make sense then

			round(probDBestPlayAll,decimals)
			round(probCBestPlayAll,decimals)
			round(probBBestPlayAll,decimals)
			round(probABestPlayAll,decimals)


	# A new best play for A has been found for optimal play of B, C and D
	if probABestPlayAll > probAMax:
		probAMax = probABestPlayAll
		bestNumberA = numberA
	elif probABestPlayAll == probAMax:
		print('There are several best plays for A:')
		print(bestNumberA, numberA)

	print('A:',numberA, 'B:', bestNumberBBestPlayAll, 'C:', bestNumberCBestPlayAll, 'D:', bestNumberDBestPlayAll)
	print('probs - A:',probABestPlayAll, 'B:', probBBestPlayAll, 'C:', probCBestPlayAll, 'D:', probDBestPlayAll)
	print('max prob A:',probAMax)


print('Best number for player A:', bestNumberA)
print('Probability to win:', probAMax)







