import requests
import telegram

def generate_text(out_list):
    for line in out_list:
        title = line["title"]
        price = line["price"]
        url = line["link"]
        img = requests.get(line["img"])
        text = f"{img}\n{title}\n\n{price}\n{url}"
        send_telegram(text)


def send_telegram(text: str):
    token = "5372206660:AAHDj9nhx9wodD9qcBDwVMndCAHzLjSNrho"
    url = "https://api.telegram.org/bot"
    channel_id = "@my_test_chanal_1"
    url += token
    method = url + "/sendMessage"

    r = requests.post(method, data={
        "chat_id": channel_id,
        "text": text
    })

    if r.status_code != 200:
        print(r.status_code)
        raise Exception("post_text error")


if __name__ == '__main__':
    send_telegram("hello world!")