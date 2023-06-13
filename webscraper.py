from bs4 import BeautifulSoup
import os
import re
import urllib.request
import json

connectionType = 0
thisPath = os.getcwd()
filePath = f'{thisPath}\\input\\testpage.html'

if connectionType == 1:
    index = urllib.request.urlopen(filePath)
else:
    HTMLFile = open(filePath, "r", encoding="utf-8")
    index = HTMLFile.read()

websiteData = BeautifulSoup(index, 'lxml')


def writeToFile(input, fileType):
    if fileType == "JSON":
        if os.path.exists(thisPath+"\\output\\"):
            if os.path.exists(thisPath+'\\output\\test.json'):
                with open(thisPath+'\\output\\test.json', 'a') as json_file:
                    json.dump(input, json_file)
            else:
                with open(thisPath+'\\output\\test.json', 'w') as json_file:
                    json.dump(input, json_file)
        else:
            os.mkdir(thisPath+"\\output\\")
            with open(thisPath+'\\output\\test.json', 'w') as json_file:
                json.dump(input, json_file)
            print("Created scraped data file.")
        

def cleanData(string):
    if len(string) > 0:
        encoded = string.encode("ascii", "ignore")
        decoded = encoded.decode()
        export_data = re.sub(r'\s+', ' ', decoded).strip()

    return export_data


def downloadImage(imageURL: str, questionID: int):
    imagePath = thisPath + "\\images\\"

    imageURLReq = urllib.request.Request(
        url=imageURL,
        headers = { "User-Agent": "Mozilla/5.0" }
        )
    
    if os.path.exists(imagePath):
        if os.path.exists(imagePath + f"question-{questionID}.png"):
            os.remove(imagePath + f"question-{questionID}.png")
            img = urllib.request.urlopen(imageURLReq).read()

            with open(f'{imagePath}question-{questionID}.png', 'wb') as handler:
                handler.write(img)
        else:
            img = urllib.request.urlopen(imageURLReq).read()

            with open(f'{imagePath}question-{questionID}.png', 'wb') as handler:
                handler.write(img)
    else:
        os.mkdir(imagePath)
        downloadImage(imageURL, questionID)


def getQuestionText(question_body, questionID):
    scoped_container = BeautifulSoup(str(question_body), 'lxml')

    revealSolution = scoped_container.select_one("a.reveal-solution").extract()
    hideSolution = scoped_container.select_one("a.hide-solution").extract()
    removeButton = scoped_container.select_one(".question-discussion-button").extract()
    if scoped_container.select_one(".question-choices-container"):
        removeVariants = scoped_container.select_one(".question-choices-container").extract()
    removeAnswer = scoped_container.select_one(".question-answer").extract()

    q_paragraphs = scoped_container.css.select("p")
    paragraphLines = q_paragraphs[0].contents
    
    
    if len(q_paragraphs) != 0:
        questionStrings = {}
        increment = 0

        for i in range(len(paragraphLines)):
            selector = paragraphLines[i]
            website_prefix = 'https://www.examplewebsite.com'

            if selector.name == 'br':
                pass
            elif selector.name == 'img':
                selectorImage = selector['src']
                if selectorImage.find(website_prefix) != -1:
                    image = downloadImage(selectorImage, questionID)
                    questionStrings[f"Image_{increment}"] = f"URL: {selectorImage}"
                    increment += 1
                else:
                    image = downloadImage(website_prefix+selectorImage, questionID)
                    questionStrings[f"Image_{increment}"] = f"URL: {website_prefix+selectorImage}"
                    increment += 1
            else:
                insertString = cleanData(selector.text)
                if len(insertString) > 0:
                    questionStrings[f"TxtLine_{increment}"] = str(insertString)
                    increment += 1     

    return questionStrings


def getAnswerVariants(parsedContainer):
    scoped_container = BeautifulSoup(str(parsedContainer), 'lxml')
    choices = scoped_container.css.select("ul > li.multi-choice-item")
    answersData = {}

    possibleVariants = ["A", "B", "C", "D", "E"]
    
    if len(choices) > 0:
        for i in range(len(choices)):
            variabila = choices[i].text
            data = cleanData(variabila)
            answersData[f"Variant_{possibleVariants[i]}"] = data[3:]

    return answersData


def getCorrectAnswer(parsedContainer):
    scoped_container = BeautifulSoup(str(parsedContainer), 'lxml')
    selectAnswer = scoped_container.css.select("p.question-answer > .correct-answer-box > .correct-answer")
    correctAnswer = selectAnswer[0].text

    return correctAnswer


def getAnswerDescription(parsedContainer):
    scoped_container = BeautifulSoup(str(parsedContainer), 'lxml')
    selectDescr = scoped_container.css.select("p.question-answer > .answer-description")
    description = cleanData(selectDescr[0].text)

    return description


def extractData(websiteData):
    main_container = websiteData.css.select("div.questions-container")
    div_container = BeautifulSoup(str(main_container),'lxml')
    question_body = div_container.css.select("div.question-body")
    output = {}

    for i in range(len(question_body)):
        questionData = getQuestionText(question_body[i], i)
        answerData = getAnswerVariants(question_body[i])
        correctAnswer = getCorrectAnswer(question_body[i])
        answerDescription = getAnswerDescription(question_body[i])
        
        output["QuestionID"] = i
        output.update(questionData)
        output.update(answerData)
        if len(correctAnswer) > 0:
            output["Correct Answer:"] = correctAnswer
        output["Explanation:"] = answerDescription

        saveToFile = writeToFile(output, "JSON")
        

run = extractData(websiteData)