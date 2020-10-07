from selenium import webdriver
from time import sleep
import pyperclip
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
options = webdriver.ChromeOptions()
options.add_argument("--user-data-dir=C:/Users/sectr/AppData/Local/Google/Chrome/User Data/Default")
options.add_argument("--profile-directory=Default")
options.add_argument("--disable-notifications")
post_name = []
username = ""          # Enter your username
password = ""                   # Enter your password
driver = webdriver.Chrome(executable_path="C:/Users/sectr/OneDrive/Desktop/PythonProjects/chromedriver_win32/chromedriver.exe",options=options)


def logIn():            # Log In Function.
    driver.get(r"https://www.reddit.com/login/?dest=https%3A%2F%2Fwww.reddit.com%2F")
    sleep(5)
    sleep(10)
    username_in = driver.find_element_by_class_name("AnimatedForm__textInput").send_keys(username,Keys.ENTER)
    pass_in = driver.find_element_by_xpath("//*[@id='loginPassword']").send_keys(password,Keys.ENTER)
    sleep(5)
    profile(str(input('Enter the name of the person you would like to send posts to : \n --> ')))
    
def check(current):                         # A check function to make sure that the same post doesn't get sent twice.
    if current in post_name:
        return True
    
def profile(receiver_username):
    sleep(10)
    driver.get(f'https://www.reddit.com/user/{username}/upvoted/')       # To open the user's profile to get the upvotes data.
    sleep(8)
    while True:
        
        posts = driver.find_elements_by_class_name('_eYtD2XCVieq6emjKBH3m')
        for post in posts[2:]:
            post_name.append(post.text)
        current = posts[1].text 
        if not check(current):
            post_name.append(current)
            print(f"...Sending {current}...")
            share = driver.find_element_by_class_name('kU8ebCMnbXfjCWfqn0WPb').click()
            sleep(3)
            copy_link = driver.find_element_by_class_name('_10K5i7NW6qcm-UoCtpB3aK._3LwUIE7yX7CZQKmD2L87vf._2snJGyyGyyH38duHobOUKE._1oYEKCssGFjqxQ9jJMNj5G').click()
            post_link = pyperclip.paste()
            dm(post_link,receiver_username)
            driver.refresh()
        else:
            print("---No New Posts To Send---")
            driver.refresh()

def dm(post_link,receiver_username):
    chat = driver.find_element_by_xpath('//*[@id="change-username-tooltip-id"]/span[1]/a').click()
    sleep(5)
    direct = driver.find_element_by_xpath('//*[@id="tooltip-container"]/div[1]/div/div[1]/button[2]').click()
    sleep(3)
    parent_tagname = driver.find_elements_by_class_name("_3GDyz0bgwoWgoxYSYSxXyA._809obLHiY5wS3ZHNVH0QY")
    sleep(3)
    for chats in parent_tagname:
        try :
            anchor_tag = chats.find_elements_by_xpath('//*[@id="tooltip-container"]/div[1]/div/div[2]/div/a')
            sleep(2)
            for chat_name in anchor_tag :
                chat_text = chat_name.find_element_by_class_name('_2O9bxNWfKdVw3DGR5RL3qM').text
                if chat_text == receiver_username:
                    chat_name.click()
                    
        except NoSuchElementException :
            print('The chat you are looking for is not there.')
            
    sleep(2)
    message = driver.find_element_by_css_selector('#MessageInputTooltip--Container > textarea').send_keys(post_link,Keys.ENTER)
    sleep(1)
    close = driver.find_element_by_class_name("_3QHhpmOrsIj9Hy8FecxWKa._1PhPhuhKHqFwivRAkg2DkH._2SeZKjVwSpNwqshVnDJkYF.bwxXoigjZ4E9ofWIggxmp").click()
    

try:
    logIn()
except NoSuchElementException:
    profile(str(input('Enter the name of the person you would like to send posts to : \n --> ')))

