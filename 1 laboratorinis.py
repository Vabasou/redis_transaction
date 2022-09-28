import redis

SEPERATOR = ":"

r = redis.Redis(host='localhost', port=49153, password="redispw")

def makeMultipleTransactions():
    print("Make transaction: ")
    makeNewTransaction = True
    while (makeNewTransaction):
        sender, receiver, amount = getSenderAndReceiver()
        makeTransaction(sender, receiver, amount)
        print("Make another transacton? Y, N: ")
        makeAnother = input()
        if (makeAnother == "N" or makeAnother == "n"):
            makeNewTransaction = False

def makeTransaction(senderKey, receiverKey, amount):
    p = r.pipeline()
    if (checkStudentBalance(senderKey, amount)):
        p.watch(senderKey)
        senderMoney = p.get(senderKey)
        receiverMoney = p.get(receiverKey)
        p.multi()
        p.set(senderKey, float(senderMoney) - float(amount))
        p.set(receiverKey, float(receiverMoney) + float(amount))
        p.execute()
        print("Sender balance: " + str(getStudentBalance(senderKey)))
        print("Receiver balance: " + str(getStudentBalance(receiverKey)))
        return True
    else:
        print("No money, no honey")
        return False

def getSenderAndReceiver():
    senderExist = False
    while (senderExist == False):
        print("Type sender's name:")
        senderName = input()
        print("Type sender's surname:")
        senderSurname = input()
        senderKey = getStudentKey(senderName, senderSurname)
        senderExist = studentExist(senderKey)
        if (senderExist == False):
            print("No user with this name")
    receiverExist = False
    while (receiverExist == False):
        print("Type receiver's name:")
        receiverName = input()
        print("Type receiver's surname:")
        receiverSurname = input()
        receiverKey = getStudentKey(receiverName, receiverSurname)
        receiverExist = studentExist(receiverKey)
        if (receiverExist == False):
            print("No user with this name")
    correctAmount = False
    while (correctAmount == False):
        print("Type amount to transfer:")
        amount = input()
        correctAmount = checkAmount(float(amount))
        if (correctAmount == False):
            print("Incorrect amount")
    return senderKey, receiverKey, amount    

def consoleUser():
    print("Type user name:")
    name = input()
    print("Type user surname:")
    surname = input()
    print("Type user balance")
    balance = input()

    return name, surname, balance

def getStudentKey(name, surname): #2 different variables if two students with same name/surname appeared
    key = str(name + SEPERATOR + surname)
    return key

def createUsers():
    print("Creating users...")
    createNewUser = True
    while (createNewUser):
        name, surname, balance = consoleUser()
        studentKey = getStudentKey(name, surname)
        if (name == "" or surname == ""):
            print("Name cannot be empty")
        else:
            print(studentKey + " Praejo")
            setStudent(studentKey, balance)
            print(getStudentBalance(studentKey))
            print(r.keys())
            print("Add another student? Y, N: ")
            addAnother = input()
            if (addAnother == "N" or addAnother == "n"):
                createNewUser = False

# Helper functions
def setStudent(key, balance):
    return r.set(key, balance)

def getStudentBalance(key):
    return r.get(key)

def checkStudentBalance(key, amount):
    return (float(getStudentBalance(key)) >= float(amount))
        
def studentExist(key):
    return r.exists(key) == 1

def checkAmount(amount):
    if (type(amount) == int or type(amount) == float):
        return (amount > 0)
    else:
        return False

# Main
def main():
    createUsers()
    makeMultipleTransactions()

if __name__ == "__main__":
    main()