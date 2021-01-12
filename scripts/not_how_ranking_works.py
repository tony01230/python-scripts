import random
# data = [[name, description],[name, description]]

def rank(options, question):
    def initialRanking(data, question):
        rankedChoices = []
        rankedChoices += [random.choice(data)]
        data.pop(data.index(rankedChoices[0]))

        def removeData():
            data.pop(data.index(randomChoice))

        while True:
            randomChoice = random.choice(data)
            print(question + "\n {} - {} ".format(rankedChoices[0], randomChoice))
            while True:
                chosenOption = input("Choices (Y/N, D1, D2): ")
                if chosenOption.lower() == "y":
                    rankedChoices.insert(0, randomChoice)
                    removeData()
                    break
                elif chosenOption.lower() == "n":
                    rankedChoices.insert(1, randomChoice)
                    removeData()
                    break
                elif chosenOption.lower() == "d1":
                    print(rankedChoices[0][1])
                elif chosenOption.lower() == "d2":
                    print(randomChoice[1])
            if len(data) == 0:
                break
        return rankedChoices

    ranking = options[:]
    for _ in options:
        ranking = initialRanking(ranking, question)
    print(ranking)


rank([[x, str(x)] for x in range(8)], "Is the first option more favourable than the second?")
