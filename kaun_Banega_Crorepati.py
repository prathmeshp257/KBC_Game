import requests
from bs4 import BeautifulSoup
import random

url_economics = "https://www.gktoday.in/quizbase/indian-economy-mcqs"
url_geography = "https://www.gktoday.in/quizbase/indian-geography-mcqs"
url_culture = "https://www.gktoday.in/quizbase/indian-culture-general-studies-mcqs"
url_sports = "https://www.gktoday.in/quizbase/sports-gk"
ques_list = []
ques_option = {}
ques_answer = {}

# Extracting All URL's for Questions

main_url = 'https://www.gktoday.in/gk-questions/'
s = requests.get(main_url)
htmlContent = s.content

# Creating s soup using BS4
soup = BeautifulSoup(htmlContent, 'html.parser')
# print(soup.prettify())

all_Urls = []
for link in soup.find_all('a'):
    all_Urls.append(link.get('href'))

for url in all_Urls:
    try:
        # Get the HTML Contents from Webpage
        r = requests.get(url)
        htmlContent = r.content

        # Creating s soup using BS4
        soup = BeautifulSoup(htmlContent, 'html.parser')
        # print(soup.prettify())

        # HTML Tree Transversal
        # For Extracting Questions
        lists = soup.find_all("div", class_='wp_quiz_question testclass')
        # print(lists)
        # Converting lists to str for further filtering
        lists = str(lists)
        # print(lists)
        # Spliting the contents for further sorting
        lists = lists.split("</span>")
        lists.pop(0)  # Removing first index for even sorting

        # print(lists)
        # Removing Tag at end of the Question
        for i in range(len(lists) - 1):
            lists[i] = lists[i][:(len(lists[i]) - 72)]                  # This All Steps Performed for Filtering.
        for i in range(len(lists)):
            try:
                lists[i] = lists[i][:lists[i].index("?")+1]             # This All Steps Performed for Filtering.
            except:
                continue
        for i in range(len(lists)):
            lists[i] = lists[i].replace("<ol><li>", '\n')               # This All Steps Performed for Filtering.
            lists[i] = lists[i].replace('</li><li>', '\n')              # This All Steps Performed for Filtering.
            lists[i] = lists[i].replace('</li></ol><p>', '\n')          # This All Steps Performed for Filtering.
            lists[i] = lists[i].replace('</p>', ' ')
            lists[i] = lists[i].replace('<br/>', ' ')
            lists[i] = lists[i].replace('\xa0', ' ')
            lists[i] = lists[i].replace('</strong>', ' ')
            lists[i] = lists[i].replace("\xa0of a\xa0real\xa0", ' ')
        # print(len(lists))
        # Append this list in Global list
        ques_list.extend(lists)
        # for Extracting options for every Question

        ans_list = soup.find_all('div', type="A")
        # print(ans_list)
        ans_list = str(ans_list)
        # print(ans_list)
        ans_list = ans_list.split("<p> ")
        ans_list.pop(0)
        # print(ans_list)
        for i in range(len(ans_list)):
            # This All Steps Performed for Filtering.
            ans_list[i] = ans_list[i].replace('''</p></div>, <div class="wp_quiz_question_options" type="A">''', '')
            ans_list[i] = ans_list[i].replace('<sup>3</sup></p></div>', ' ')    # This All Steps Performed for Filtering.
            ans_list[i] = ans_list[i].replace('</sup>', ' ')                       # This All Steps Performed for Filtering.
            ans_list[i] = ans_list[i].replace('<sup>', ' ')
            ans_list[i] = ans_list[i].replace("&amp;", '&')
            ans_list[i] = ans_list[i].replace('''</p></div>]''', ' ')
            ans_list[i] = ans_list[i].replace("\n", ' ')
            ans_list[i] = ans_list[i].replace("\\", ' ')
            ans_list[i] = ans_list[i].replace("<br/>", ' ')
        '''for i in range(len(ans_list)):
            ans_list[i] = ans_list[i].split("<br/>")'''
        # print(ans_list)

        # Now Extracting All the Correct answers for the Questions

        corr_ans = soup.find_all('div', class_='ques_answer')
        corr_ans = str(corr_ans)
        corr_ans = corr_ans.split('</b>')
        corr_ans.pop(0)
        for i in range(len(corr_ans) - 1):
            corr_ans[i] = corr_ans[i][:len(corr_ans[i]) - 51]

        # Appending All the Questions & Options in a dictionary
        for i in range(len(lists)):
            ques_option[lists[i]] = ans_list[i]
            ques_answer[lists[i]] = corr_ans[i]

    except:
        # print("Error Occured")
        continue

# print(ques_answer)
# print(len(ques_answer))


# Now Create a game: Kaun Banega Crorepati

list_WinPrice = ['Rs.5000', 'Rs.10,000', 'Rs.20,000', 'Rs.50,000', 'Rs.1,00,000', 'Rs.5,00,000', 'Rs.20,00,000',
                 'Rs.50,00,000', 'RS. 75,00,000', 'Rs.1,00,00,000']
# print(len(list_WinPrice))
Correct_ans = int(0)

# Show Game Overview & Rules

print("Kaun Banega Crorepati".center(175))
print("Winning Amounts".center(175, '*'))
a = input("Press Enter key to Start the Game".center(175))

while True:
    for j in range(1, 11):
        random_ques = (random.choice(ques_list))
        print("-".center(175, "-"))
        print(random_ques)
        print(ques_option.get(random_ques))
        print('\n')
        choice_list = ['A', 'B', 'C', 'D']
        while True:
            try:
                ans = input("Enter Correct Options : (Press Either A, B, C or D & Hit Enter) ")
                if ans == "A" or ans == "B" or ans == "C" or ans == "D":
                    break
                else:
                    continue
            except:
                continue
        for i in choice_list:
            if ans == i:
                if ques_answer.get(random_ques).startswith(f' {i}'):
                    print(ques_answer.get(random_ques))
                    print("*".center(175, "*"))
                    print(" ...Hurrrey...Your Answer is Correct... ".center(175, " "))
                    print("*".center(175, "*"))
                    Correct_ans = Correct_ans + 1
                    break
        if Correct_ans == j:
            if Correct_ans == 10:
                print("-".center(175, "-"))
                print("*".center(175, "*"))
                print(f"You've Correctly answered All the Questions & Won Rs.1,00,00,000".center(175))
                print('\n')
                print("***   Hurrey...You've Won the Game.    ***".center(175))
                print("...Thanks for Playing...".center(175))
                print('\n')
                print("*".center(175, "*"))
                break
        elif Correct_ans != j:
            print("*".center(175, "*"))
            print("Ugh... You've Given a Wrong Answer")
            print("-".center(175, "-"))
            print("Game Over...Please Try Again".center(175))
            print("-".center(175, "-"))
            print("*".center(175, "*"))
            print('\n')
            print(f"You've Correctly answered {Correct_ans} Questions & Won {list_WinPrice[Correct_ans]}".center(175))
            print("Thanks for Playing...".center(175))
            print('\n')
            print("*".center(175, "*"))
            break

    user_choice = input("Would You like to play Again? (Hit Yes & Enter to Play Again) ".center(175))
    if user_choice == 'Yes':
        continue
    else:
        print('\n')

        break
