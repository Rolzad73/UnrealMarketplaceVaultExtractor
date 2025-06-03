import json
import os
# from urllib.request import urlopen
import urllib.request
from selenium import webdriver
from selenium.webdriver.common.by import By

MP_URL = "https://www.unrealengine.com/marketplace"
JSON_DIR = "./data"
OUT_FILE = "mp_vault_list.md"
# options = webdriver.ChromeOptions()
# options.add_argument("--headless=new")
# driver = webdriver.Chrome(options=options) # headless changes the return html, default mode works fine
driver = webdriver.Chrome()


def main():
    mp_jsons = []
    cost = 0.
    disc = 0.
    currency = ""
    count = 0
    for f in os.listdir(JSON_DIR):
        if not f.endswith(".json"):
            continue
        with open(os.path.join(JSON_DIR, f), encoding="utf8") as fd:
            j = json.load(fd)
            count += len(j['data']['elements'])
            mp_jsons.append(j)
    with open(OUT_FILE, "w+") as fd:
        fd.write(f"# Vault content\n\n")
        i = 0
        actualCount = 0
        for j in mp_jsons:
            for el in j['data']['elements']:
                i += 1
                print(f"\rProcessing Vault {i}/{count}\n", end="")
                # The ID found in the json dump is completely valid, and we have to resolve it to the urlSlug if we
                # want a nice and valid URL
                if 'id' in el:
                    actualCount += 1
                    # with urlopen(f"{MP_URL}/api/assets/asset/{el['id']}") as f:
                        # jj = json.load(f)
                    full_url = f"{MP_URL}/api/assets/asset/{el['id']}"
                    # print(full_url)

                    try:
                        driver.get(full_url)
                        # print(driver.page_source)
                        findingjson = driver.find_element(By.TAG_NAME, "pre").text
                        # print(findingjson)
                        jj = json.loads(findingjson)
                        jjd = jj['data']['data']
                        fd.write(f"* [{jjd['title']}]({MP_URL}/en-US/product/{jjd['urlSlug']})\n")
                        cost += jjd['priceValue']
                        currency = jjd['currencyCode']
                        disc += jjd['discountPriceValue']
                    except Exception as e:
                        print (e)
                        pass
                    # except KeyError:
                    #     print (KeyError)
                    #     pass

        driver.quit()
        fd.write(f"\n# Vault stats\n\n")
        fd.write(f"* Value: {cost / 100}{currency}\n")
        fd.write(f"* Current cost: {disc / 100}{currency}\n")
        fd.write(f"* Size: {actualCount}\n")


if __name__ == '__main__':
    main()
