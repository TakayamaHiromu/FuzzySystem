import matplotlib.pyplot as plt


#ファジィ型を作成
class Fuzzy:

    #コンストラクタ
    def __init__(self, value):
        self.value = value

    #文字列表示
    def __str__(self):
        return self.value


    #選言（または）
    def __or__(self, other):
        return self.__class__(max(self.value, other.value))

    #連言（かつ）
    def __and__(self, other):
        return self.__class__(min(self.value, other.value))

    #含意（ならば）
    def implication(self, p, q):
        if p > q:
            answer = 1 - p + q
        else:
            answer = 1

        return self.__class__()

#Fuzzy集合型を定義
class FuzzySet:


    #コンストラクタ(辞書を一旦バラして再構築している)．setはデフォルトで空集合にしておく
    def __init__(self, set={}):
        self.set = {}
        keys = list(set.keys())
        values = list(set.values())
        for i, j in zip(keys, values):
            self.set[i] = Fuzzy(j)


    #文字列表示
    def __str__(self):
        disp = []
        for k in sorted(self.set.keys()):
            disp.append((k, self.set[k].value))

        return str(disp)


    #凸ファジィ集合かどうか
    def convax(self):
        before = 0
        grad = 0
        gradbefore = 0

        #勾配が負から正に変わると、谷になるので、凸ファジィでなくなる
        for k in sorted(self.set.keys()):
            if self.set[k].value > before:
                grad = 1
            elif self.set[k].value < before:
                grad = -1

            if gradbefore == -1 and grad == 1:
                return False

            before = self.set[k].value
            gradbefore = grad

        return True


    #αカット(クリスプ集合への変換)
    def alpha(self, a):
        alphaset = {}
        keys = list(self.set.keys())
        values = list(self.set.values())
        for i, j in zip(keys, values):
            #a以上は全て１として，それ以外を0とする
            if j.value >= a:
                alphaset[i] = 1
            else:
                alphaset[i] = 0

        return alphaset



    #ファジィ集合の演算の足し算(ファジィ数)
    def __add__(self, other):
        resultset = FuzzySet()

        for i in self.set.keys():
            for j in other.set.keys():
                sum = i + j
                if sum in resultset.set:
                    resultset.set[sum] = resultset.set[sum] | self.set[i] & other.set[j]
                else:
                    resultset.set[sum] = self.set[i] & other.set[j]

        return resultset

    #ファジィ集合の演算の掛け算(ファジィ数)
    def __mul__(self, other):
        resultset = FuzzySet()

        for i in self.set.keys():
            for j in other.set.keys():
                mul = i * j
                if mul in resultset.set:
                    resultset.set[mul] = resultset.set[mul] | self.set[i] & other.set[j]
                else:
                    resultset.set[mul] = self.set[i] & other.set[j]

        return resultset






"""
p = input("p = ")
q = input("q = ")


p = Fuzzy(p)
q = Fuzzy(q)


x = p | q
"""

#ファジィ集合を作成するための辞書
r = {1:0, 2:0.2, 3:0.5, 4:0.6, 5:1, 6:1}
many = {2:0.2, 3:0.5, 4:0.9, 5:1}
afew = {1:0.6, 2:1, 3:0.8, 4:0.2}

abouttwo = {1:0.2, 2:1, 3:0.3}
aboutsix = {5:0.5, 6:1, 7:0.4}

#ファジィ集合の作成
r = FuzzySet(r)
many = FuzzySet(many)
afew = FuzzySet(afew)
abouttwo = FuzzySet(abouttwo)
aboutsix = FuzzySet(aboutsix)

print(r)

#凸かどうかの判定
print(r.convax())

#0.5でαカット
print(str(r.alpha(0.5)))

#拡張原理による演算
result = many + afew
#result = abouttwo * aboutsix
print(result)

plt.bar(many.set.keys(), [i.value for i in many.set.values()], width=0.1, align='edge', label='many')
plt.bar(afew.set.keys(), [i.value for i in afew.set.values()], width=0.1, label='a few')
plt.bar(result.set.keys(), [i.value for i in result.set.values()], width=0.1, label='result')

"""

plt.bar(result.set.keys(), [i.value for i in result.set.values()])
plt.bar(aboutsix.set.keys(), [i.value for i in aboutsix.set.values()], width=0.4)
plt.bar(abouttwo.set.keys(), [i.value for i in abouttwo.set.values()], width=0.4, align='edge')

plt.plot(aboutsix.set.keys(), [i.value for i in aboutsix.set.values()])
plt.plot(abouttwo.set.keys(), [i.value for i in abouttwo.set.values()])
plt.plot(result.set.keys(), [i.value for i in result.set.values()])

"""

plt.legend(loc = 'upper right')
plt.show()
