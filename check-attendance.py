from bs4 import BeautifulSoup
import re
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementNotInteractableException, NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

config_f = open("./format.txt", "r", encoding="utf-8")
pformat = config_f.read().strip()
config_f.close()

config_m = open("./members.txt", "r", encoding="utf-8")
members = list(map(str.strip, config_m.readlines()))
config_m.close()

if len(members) <= 0:
    print("members.txt를 설정해주세요.")
    exit(1)

print("출력예시:", pformat.replace("{serial}", "01").replace("{name}", members[0]))

def by_serial_number(x):
    match = re.findall(r"\d{4}", x)
    out = match[0] if len(match) else None
    return out

def by_name(x):
    match = re.match(r"^.*? ?_?([ 가-힣]+)$", x)
    out = match.groups()[0]
    return out

def to_korean_name(x):
    match = re.match(r"([가-힣]+) ([가-힣]+)", x)
    out = (match.groups()[1] + match.groups()[0]) if match else x
    return out

def chrome():
    options = webdriver.ChromeOptions()
    options.add_argument("--log-level=3")
    options.add_argument("--mute-audio")
    
    return (
        webdriver.Chrome(executable_path="./bin/chromedriver.exe", service_log_path="NUL", options=options)
    )

def firefox():
    profile = webdriver.FirefoxProfile()
    profile.set_preference("media.volume_scale", "0.0")

    return (
        webdriver.Firefox(executable_path="./bin/geckodriver.exe", service_log_path="NUL", firefox_profile=profile)
    )

def send_chat(driver, chatarea, msg):
    chatarea.clear()
    if msg == "미출석자:":
        chatarea.send_keys("미출석자 없음")
    else:
        for part in msg.split('\n'):
            chatarea.send_keys(part)
            ActionChains(driver).key_down(Keys.SHIFT).key_down(Keys.ENTER).key_up(Keys.SHIFT).key_up(Keys.ENTER).perform()
        chatarea.send_keys(Keys.BACK_SPACE)
    chatarea.send_keys(Keys.RETURN)

def find_not_attended(html):
    soup = BeautifulSoup(html, "html.parser")
    raw_participants = soup.find_all("span", {"class": "participants-item__display-name"})

    participants = list(map(lambda x: x.decode_contents(), raw_participants))
    participants = list(map(by_name, participants))
    participants = list(map(to_korean_name, participants))

    msg = "미출석자:"
    for idx, member in enumerate(members):
        if member not in participants:
            msg += ("\n" + pformat.replace("{serial}", "%02d" % (idx + 1)).replace("{name}", member))

    return msg

driver = chrome()
wait = WebDriverWait(driver, 100000)

# Join meeting
driver.get("https://zoom.us/wc/join/" + input("Meeting ID: "))

inputname = driver.find_element_by_id("inputname")
inputname.clear()
inputname.send_keys("출석체크봇")
inputname.send_keys(Keys.RETURN)

wait.until(EC.presence_of_element_located((By.ID, "inputpasscode")))

inputpasscode = driver.find_element_by_id("inputpasscode")
inputpasscode.clear()
inputpasscode.send_keys(input("Meeting Password: "))
inputpasscode.send_keys(Keys.RETURN)

input("참가자 버튼과 채팅 버튼이 보이는 상태에서 엔터를 누르세요.")
while True:
    try:
        # Click participants btn
        participantsbtn = driver.find_element_by_css_selector(".footer__btns-container > div:nth-child(1) > button:nth-child(1)")
        participantsbtn.click()
        wait.until(EC.presence_of_element_located((By.ID, "participants-ul")))

        # Click chat btn
        chatbtn = driver.find_element_by_css_selector("div.footer-button__wrapper:nth-child(3) > button:nth-child(1)")
        chatbtn.click()
        wait.until(EC.presence_of_element_located((By.ID, "chat-list-content")))
        chatarea = driver.find_element_by_css_selector(".chat-box__chat-textarea")
        break
    except ElementNotInteractableException:
        pass
    except NoSuchElementException:
        pass

    input("버튼 클릭 실패. 참가자 버튼과 채팅 버튼이 보이는 상태에서 엔터를 누르세요.")


while True:
    i = input("엔터를 누르면 출석체크를 진행합니다. 나가려면 Ctrl-C를 누르세요.")
    if i == 'q':
        break

    try:
        msg = find_not_attended(driver.page_source)
        send_chat(driver, chatarea, msg)
        print(msg)
    except:
        print("출석자를 가져오지 못했습니다.")
