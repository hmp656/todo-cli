import random
import datetime
from datetime import date
from .sqlite_com import columns

def createID():
    length = 10
    ID_Code = []
    chars = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0',
             'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J',
             'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
             'U', 'V', 'W', 'X', 'Y', 'Z',
             'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j',
             'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
             'u', 'v', 'w', 'x', 'y', 'z'
            ]

    while True:
        ID_Code.append(random.choice(chars))
        if len(ID_Code) > length:
            break
    return ''.join(ID_Code)


def checkDateFormat(givendate):
    if '/' in givendate and len(givendate) <= 10:
        givendate = givendate.split('/')
        try:
            int(givendate[0])
            int(givendate[1])
            int(givendate[2])

            if int(givendate[0]) > 31 or int(givendate[1]) > 12:
                return False

            elif int(givendate[0]) > 29 and int(givendate[1]) != 2:
                return False

            else:
                return True

        except:
            return False


def usageHelp():
    message = """
    Usage:
    -a --add                       -- prompts title and date
    -a --add <title>               -- adds title from argument
    -e --edit <index>              -- prompts new title
    -r -rm --remove <index>        -- removes item
    -t --tag <index>               -- prompts for a new tag
    -s --search                    -- prompts search tag
    -s --search <tag>              -- search tag from argument
    """

    return message


def dateDif(dateSet):
    if checkDateFormat(dateSet):
        today = datetime.date.today()

        dateSet = dateSet.split('/')
        dateObj = datetime.date(int(dateSet[2]), int(dateSet[1]), int(dateSet[0]))
        dateObj = (dateObj - today).days

    else:
        dateObj = None

    return dateObj


def daysConvert(days):
    try:
        days = int(days)

        if days == 0:
            return 'Today'

        elif days > 0:
            if days == 1:
                return 'Tomorrow'

            elif days < 7:
                return str(days) + ' days from now'

            elif days > 7:
                if days % 7 == 0:
                    return str(days / 7) + ' weeks'
                else:
                    weeks = days - days % 7
                    weeks = int(weeks / 7)
                    return str(weeks) + ' weeks and ' + str(days % 7) + ' days from now'

        elif days < 0:
            if days == -1:
                return 'Yesterday'

            elif days > -7:
                days =  days * -1
                return str(days) + ' days ago'

            elif days < -7:
                days = days * -1
                if days % 7 == 0:
                    return str(days / 7) + ' weeks'
                else:
                    weeks = days - days % 7
                    weeks = int(weeks / 7)
                    return str(weeks) + ' weeks and ' + str(days % 7) + ' days ago'


    except Exception as e:
        print(e)
        return False
