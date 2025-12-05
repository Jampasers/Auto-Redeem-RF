import requests

def generate_qr_image(qr_string: str, filename: str = "qris.png"):
    url = f"https://chart.googleapis.com/chart?cht=qr&chs=500x500&chl={qr_string}"
    img = requests.get(url).content

    with open(filename, "wb") as f:
        f.write(img)
    
    return filename
