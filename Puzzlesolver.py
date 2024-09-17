import pandas as pd
import requests
from bs4 import BeautifulSoup as bs

puzzle = [ #string for each line of the puzzle
"D C W I K O J M H S E F R N U",
"T R A I G S E N O B Y A J C M",
"R I P X L D B W B V O M L U H",
"S M S I G L O T K A T Z F X N",
"G S H Y U A O S O Y R O J I E",
"K O P N D F E W H R S T I Q G",
"A N V C S N I G Y X V N E N N",
"L D M G B J E D F S A I Z R E",
"E A V A R C W I G M P A K E L",
"E N A R H R B C Y E V R N W A",
"A V Y A E I T G B N T W X U D",
"F U B M Q I U K I C A P H J Y",
"Q Y R O J O V N A H P H I E L",
"V G Q N R J Z P S Y V I E I I",
"J S V D I A L O L L O T C F A"
]

def ConvertToChar(puzzle):
    convert = []
    for line in puzzle:
        line = line.split(" ")
        convert.append(line)
    return(convert)

def ToStringy(listChars : list):
    stringy = ''.join(listChars)
    return(stringy)

def ReverseToString(listChars : list):
    listChars.reverse()
    stringy = ToStringy(listChars)
    return(stringy)

def FindDiagnals(df,tdf):
    tempList = []
    x = 0
    lenConvert = len(df)
    x = 0
    x2 = 0
    l = 1
    HiC = 0
    for i in range(lenConvert): #loops for each row in the range
        control = []
        for c in range(l): #create list of range needed [0,1,2] - use this for to create [0,2] - [1,1] - [2,0]
            control.append(c)
            tempHold = []
            tempHold2 = []
            tempHold3 = []
            tempHold4 = []
            HiC = len(control)
            for g in control:
                if len(control) > 2: #loops through each range to find diagnal lines
                    tempHold.append(df[g][HiC-1])
                    tempHold2.append(tdf[(len(puzzle)-1)-g][HiC-1])
                    tempHold3.append(df[(lenConvert-1)-g][(lenConvert-1)-(HiC-1)])
                    tempHold4.append(df[(lenConvert-1)-g][HiC-1])
                    HiC = HiC - 1
        if len(tempHold) != 0: #how to handle tis better
            tempList.append(tempHold)
            tempList.append(tempHold2)
            tempList.append(tempHold3)
            tempList.append(tempHold4)
        l = l + 1
    return(tempList)

def GetNameList():
    names = []
    headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36'}
    page = "http://users.nexustk.com/webreport/Alizarin.html"
    user_scrape = requests.get(page, headers = headers)
    user_soup = bs(user_scrape.content, 'html.parser')
    soup_select = user_soup.get_text()
    split_soup = soup_select.splitlines()

    pos = 0
    try:
        while pos < len(split_soup):
            split_soup.remove('')
            pos = pos + 1
    except:
        pos = pos + 10000
    
    for line in split_soup: #this is sloppy but whatever
        l = line.split(" ")
        try:
            names.append(l[2].upper())
        except:
            pass #not a name
    #too lazy to fix the council names
    names.append("BARTER")
    names.append("CRYSTALICE")
    names.append("HUNTYR")
    names.append("PHILLIES")
    names.append("SHAWNEE")
    names.append("WILLOWYSPR")
    names.append("CRIMSONDAN")
    return(names)

def main():
    ToString = ConvertToChar(puzzle=puzzle)
    df = pd.DataFrame(ToString)
    tdf = df.transpose()
    diags = FindDiagnals(df=df,tdf=tdf) #list of diagnals
    df = df.values.tolist() #list of rows
    tdf = tdf.values.tolist() #list of columns

    searchStrings = df + tdf
    searchStrings = searchStrings + diags
    names = GetNameList()
    #names = []
    namesFound = {}

    for name in names:
        for line in searchStrings:
            strLine = ToStringy(line)
            rstrLine = ReverseToString(line)
            find1 = strLine.find(name)
            find2 = rstrLine.find(name)
            if find1 != -1 and name != "DAN": #why does dan appear??? find is a list not the substring
                print(line)
                namesFound.update({name : line})
            if find2 != -1 and name != "DAN":
                print(line)
                namesFound.update({name : line})
    sortNames = sorted(namesFound)
    sortDic = {}
    for name in sortNames:
        print("{} Found at location {}".format(name, namesFound[name]))
        sortDic.update({name: namesFound[name]})

main()
