from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from concurrent.futures import ThreadPoolExecutor
from selenium.webdriver.common.by import By
from colorama import init, Fore, Style
import undetected_chromedriver as uc
from os import getcwd, system, mkdir
from threading import Lock
from time import sleep
import random
import string

init(autoreset=True)
lock = Lock()

# human like mouse movements are only important for solving the captcha

def extract(target):
    driver = uc.Chrome(use_subprocess=True, headless=True)
    driver.maximize_window()

    actions = ActionChains(driver)
    driver.get(target)
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "/html/body/header/h2")))  # wait for load

    iframe = driver.find_element(By.XPATH, "/html/body/main/form/fieldset/div/div/div/iframe")
    driver.switch_to.frame(iframe)
    location = driver.find_element(By.XPATH, "/html/body/div[2]/div[3]/div[1]/div/div/span/div[1]")

    actions.move_to_element(location).click().perform()  # open recaptcha window

    driver.switch_to.default_content()  # switch back to main frame
    iframe = driver.find_element(By.XPATH, "/html/body/div/div[4]/iframe")
    driver.switch_to.frame(iframe)  # switch to recaptcha iframe

    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//*[@id=\"rc-imageselect\"]/div[2]/div[1]/div[1]/div")))  # wait for recaptcha to load
    sleep(0.4)
    image_elements = driver.find_elements(By.CLASS_NAME, "rc-image-tile-wrapper")  # get all image elements

    prompt = driver.find_element(By.XPATH, "//*[@id=\"rc-imageselect\"]/div[2]/div[1]/div[1]/div/strong").text

    with lock:
        print(prompt)
        types.add(prompt)
        if item in prompt:

            try:
                mkdir(f"{getcwd()}\\temp\{prompt}")

            except FileExistsError:
                pass

            for element in image_elements:
                element.screenshot(f"{getcwd()}\\temp\{prompt}\{''.join(random.choices(string.hexdigits, k=50))}.png")

            print(f"{Style.BRIGHT}{Fore.GREEN}Extracted {len(image_elements)} images")

        elif item == "":
            try:
                mkdir(f"{getcwd()}\\temp\images")

            except FileExistsError:
                pass

            for element in image_elements:
                element.screenshot(f"{getcwd()}\\temp\images\{''.join(random.choices(string.hexdigits, k=50))}.png")

            print(f"{Style.BRIGHT}{Fore.GREEN}Extracted {len(image_elements)} images")

    driver.quit()


def main(target):
    while True:
        extract(target)
        sleep(random.randint(0, 3))

def count_types():
    while True:
        with lock:
            print(f"{Style.BRIGHT}{Fore.MAGENTA}{types}")
        sleep(30)


system("cls")

try: # probably not needed, i just dont know if mkdir cries if the directory already exists
    mkdir(f"{getcwd()}\\temp\\")
except:
    pass

print(f"{Style.BRIGHT}{Fore.RED}WARNING! Make sure to be on your VPN")
print(f"{Style.BRIGHT}{Fore.CYAN}How many threads? ===>> ", end="")
threadamount = int(input()) + 1
print(f"{Style.BRIGHT}{Fore.CYAN}Item to extract? (Notice: It doesnt sort them, it just groups images that popped up in that captcha with eachother) ===>> ", end="")
item = input()

types = set()
with ThreadPoolExecutor(max_workers=threadamount) as executor:
    for i in range(threadamount):
        executor.submit(count_types)
        executor.submit(main, "https://recaptcha-demo.appspot.com/recaptcha-v2-checkbox.php")


