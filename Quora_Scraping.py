import requests
import time
from bs4 import BeautifulSoup
from selenium import webdriver


def quora_crawler():
    url = "https://www.quora.com"
    browser = webdriver.Chrome('/home/codexnow/Downloads/chromedriver')
    browser.get(url)

    form = browser.find_element_by_class_name('regular_login')
    username = form.find_element_by_name('email')
    username.send_keys('----')              # <-- Enter Email Address

    password = form.find_element_by_name('password')
    password.send_keys('----')               # <-- Enter password
    form.find_element_by_css_selector('.submit_button').click()

    browser.switch_to.window(browser.current_window_handle)

    url = 'https://www.quora.com/topic/Crime/all_questions'

    browser.get(url)

    # to scroll page automatically

    SCROLL_PAUSE_TIME = 0.5

    # Get scroll height
    last_height = browser.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to bottom
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)
        time.sleep(5)

        # Calculate new scroll height and compare with last scroll height
        new_height = browser.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    html_source = browser.page_source
    soup = BeautifulSoup(html_source)

    topic_name = soup.find('h1')
    print("Topic Name: " + topic_name.text)

    # total questions on the topic
    questions = soup.find_all('a', {'class': 'question_link'})

    questions_urls_to_visit = []

    for i in questions:
        href_link = i.get('href')
        question_link = "https://www.quora.com" + str(href_link)
        questions_urls_to_visit.append(question_link)

    # print(questions_to_visit)
    # time.sleep(10)

    for q_url in questions_urls_to_visit:
        
        browser.get(q_url)
        
        # to scroll page automatically

        SCROLL_PAUSE_TIME = 0.5

        # Get scroll height
        last_height = browser.execute_script("return document.body.scrollHeight")

        while True:
            # Scroll down to bottom
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Wait to load page
            time.sleep(SCROLL_PAUSE_TIME)
            time.sleep(5)

            # Calculate new scroll height and compare with last scroll height
            new_height = browser.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        html_source = browser.page_source
        soup = BeautifulSoup(html_source)
        question = soup.find('h1')
        print('Question : \n' + question.text)

        total_answers = soup.find('div', {'class': 'answer_count'})
        if total_answers is not None:
            print('Total : ' + total_answers.text)

            SCROLL_PAUSE_TIME = 0.5

            # Get scroll height
            last_height = browser.execute_script("return document.body.scrollHeight")

            while True:
                # Scroll down to bottom
                browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

                # Wait to load page
                time.sleep(SCROLL_PAUSE_TIME)
                time.sleep(5)

                # Calculate new scroll height and compare with last scroll height
                new_height = browser.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    break
                last_height = new_height

            all_answers = soup.find_all('div', {'class': 'Answer AnswerBase'})

            for answer in all_answers:
                user = answer.find('a', {'class': 'user'})
                if user is not None:
                    print(user.text)

                user_details = answer.find('span', {'class': 'NameCredential IdentityNameCredential'})
                if user_details is not None:
                    print(user_details.text)

                answer_block = answer.find('div', {'class': 'ui_qtext_expanded'})
                paragraphs = answer_block.find_all('p', {'class': 'ui_qtext_para'})

                if paragraphs is not None:
                    for i in paragraphs:
                        print(i.text)
                else:
                    print("No Answers..")

                views = answer.find('span', {'class': 'meta_num'})
                print(views.text + " Views")

                upvotes = answer.find('div', {'class': 'icon_action_bar-label'})
                print(upvotes.text)

        else:
            print("No Answers..")


quora_crawler()
