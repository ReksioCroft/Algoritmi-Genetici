from math import log2
import random


class Cromozom:
    def __init__(self, fin, fout):
        self.debug = True
        self.fout = fout
        s = fin.readline().split()
        self.nrPopulatie = int(s[-1])
        s = fin.readline().split()
        self.domain = (int(s[-2]), int(s[-1]))
        s = fin.readline().split()
        self.function = (int(s[-3]), int(s[-2]), int(s[-1]))
        s = fin.readline().split()
        self.precisiton = int(s[-1])
        s = fin.readline().split()
        self.pRecombinare = float(s[-1])
        s = fin.readline().split()
        self.pMutatie = float(s[-1])
        self.lCromozom = int(log2((self.domain[1] - self.domain[0]) * (10 ** self.precisiton)))
        self.populatie = []
        self.generarePopulatie()
        self.co = 1

    def generarePopulatie(self):
        self.populatie = []
        for i in range(self.nrPopulatie):
            l = []
            for j in range(self.lCromozom):
                l.append(random.choice([0, 1]))
            self.populatie.append(l)

    def decodificarePopulatie(self):
        decod = []
        for i in self.populatie:
            b10 = 0
            p2 = 1
            for j in i:
                b10 = b10 * p2 + j
                p2 *= 2
            decod.append(((self.domain[1] - self.domain[0]) / ((1 << self.lCromozom) - 1)) * b10 + self.domain[0])
        return decod

    def fitnessPopulatie(self):
        fit = []
        decod = self.decodificarePopulatie()
        if self.debug:
            self.fout.write("Generation " + str(self.co) + ":\n")
        co = 0
        for x in decod:
            fit.append(self.function[0] * x * x + self.function[1] * x + self.function[2])
            if self.debug:
                self.fout.write(str(co) + ". " + str(self.populatie[co]) + " x=" + str(x) + " f=" + str(fit[-1]) + '\n')
            co += 1
        return (decod, fit)

    def probabilitateSelectie(self):
        decod, fit = self.fitnessPopulatie()
        fitnessTotal = sum(fit)
        prob = []

        if self.debug:
            self.fout.write("\nProbabilitate selectie:\n")
        co = 0
        for i in fit:
            prob.append(i / fitnessTotal)
            if self.debug:
                self.fout.write(str(co) + ". " + str(i))
            co += 1

        return (decod, fit, prob)

    def nextGeneration(self):
        def selectPopulation():
            decod, fit, prob = self.probabilitateSelectie()
            newPopulation = [self.populatie[fit.index(max(fit))]]  # criteriu elitist - adaugam cel mai fit membru

            # generam intervalul de probabilitati
            for i in range(1, len(prob)):
                prob[i] += prob[i - 1]

            if self.debug:
                self.fout.write("Interval: " + str(prob) + '\n')

            for i in range(self.nrPopulatie - 1):  # mai luam n-1 cromozomi
                nr = random.random()  # generam random un nr intre 0 si 1

                # cautam binar carui cromozom apartine nr generat folosind int
                p = 1 << (int(log2(len(prob))))
                idx = 0
                while p > 0:
                    if idx + p < len(prob) and prob[idx + p] < nr:
                        idx += p
                    p >>= 1
                if idx + 1 < len(prob):
                    idx += 1

                newPopulation.append(self.populatie[idx])
                if self.debug:
                    self.fout.write("u=" + str(nr) + " cromozom:" + str(idx) + '\n')
            return newPopulation

        def crossingOver(population):
            def crossOver(crom):
                r = random.random()
                if r < self.pRecombinare:
                    brPoint = random.choice(range(self.lCromozom))
                    if self.debug:
                        self.fout.write("BrPoint: " + str(brPoint) + " :->: " + str(crom))
                    aux = [0] * self.lCromozom
                    aux.extend(crom[0][brPoint:])
                    for i in range(1, len(crom)):
                        for j in range(brPoint, self.lCromozom):
                            aux2 = aux[j]
                            aux[j] = crom[i][j]
                            crom[i][j] = aux2
                    for j in range(brPoint, self.lCromozom):
                        aux2 = aux[j]
                        aux[j] = crom[i][j]
                        crom[i][j] = aux2
                    if self.debug:
                        self.fout.write(' :->: ' + str(crom) + '\n')
                return crom

            if self.debug:
                self.fout.write("Cromozomes with recombination:\n")
            newPopulation = [population[0]]  # pe prima poz avem elem maxim care va trece nemodificat in noua generatie
            population[0] = population[-1]
            population.pop()  # deci il scoartem

            random.shuffle(population)

            if len(population) % 2 == 1 and len(population) >= 3:
                newPopulation.extend(crossOver([population.pop(), population.pop(), population.pop()]))
            while len(population) > 0:
                newPopulation.extend(crossOver([population.pop(), population.pop()]))

            return newPopulation

        def mutation(population):
            for i in range(1, self.nrPopulatie):
                for j in range(self.lCromozom):
                    r = random.random()
                    if r < self.pMutatie:
                        population[i][j] = 1 - population[i][j]
            return population

        intermediatePopulation = selectPopulation()
        if self.debug:
            self.fout.write("selected population: " + str(intermediatePopulation) + '\n')
        intermediatePopulation = crossingOver(intermediatePopulation)
        if self.debug:
            self.fout.write("after crossover population: " + str(intermediatePopulation) + '\n')
        intermediatePopulation = mutation(intermediatePopulation)
        if self.debug:
            self.fout.write("new population: " + str(intermediatePopulation) + '\n')
        self.populatie = intermediatePopulation
        self.co += 1


fin = open("date.in")
fout = open("sol.out", "w")
cromozom = Cromozom(fin, fout)
s = fin.readline().split()
nrEtape = int(s[-1])

# print(cromozom.populatie)
for i in range(nrEtape):
    cromozom.nextGeneration()
    # print(".....................")
    cromozom.debug = False
    fout.write("Max number:" + str(max(cromozom.fitnessPopulatie()[1])) + '\n')
# print(cromozom.fitnessPopulatie())

fin.close()
fout.close()
