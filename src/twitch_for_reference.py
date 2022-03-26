import time
import urllib.request
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import os


def download_clips(streamer_url, driver, num_of_clips):
    driver = driver
    
    driver.get(streamer_url)

    driver.implicitly_wait(5)

    for i in range(1, num_of_clips+1):
        streamer = streamer_url.split('/')[3]
        file_name = f'{streamer}_{i}.mp4'
        
        clip_xpath = driver.find_element_by_xpath(f'//*[@id="root"]/div/div[2]/div[1]/main/div[2]/div[3]/div/div/div[1]/div[1]/div[2]/div/div[3]/div/div/div/div/div[2]/div/div/div[1]/div/div/div/div[{i}]/article/div[1]/div/div[1]/div[1]/div/a/h3').click()
            
        time.sleep(1.5)

        # ###  Finds src/url of the clip
        vid = driver.find_element_by_xpath('//*[@id="root"]/div/div[2]/div[1]/main/div[2]/div[3]/div/div/div[2]/div/div[2]/div/div/video')
        video_url = vid.get_attribute("src")
        print('download_src is ' + video_url)

        # ### Downloads clip
        urllib.request.urlretrieve(video_url, 'clips/'+file_name)

        driver.get(streamer_url)
        driver.implicitly_wait(2)


def start(streamer_list = ('asunaweeb', 'hiko'), num_clips = 3, clip_range = '30d'):
    # delete all the clips currently in the clips folder
    dir = 'clips'
    for f in os.listdir(dir):
        os.remove(os.path.join(dir, f))
    
    chromeOptions = webdriver.ChromeOptions()
    chromeOptions.set_headless(headless=True)
    chromeOptions.add_argument("--mute-audio")

    driver = webdriver.Chrome(ChromeDriverManager().install(), options=chromeOptions)
    
    # for each streamer in the streamer list, download a specified number of clips from their channel
    for i in range(len(streamer_list)):
        url = f'https://twitch.tv/{streamer_list[i]}/clips?filter=clips&range={clip_range}'
        
        download_clips(url, driver, num_clips)


if __name__  == '__main__':
    start()
