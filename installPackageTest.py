from selenium import webdriver
import requests
import aiohttp
import re
from bs4 import BeautifulSoup
import tesserocr
from PIL import Image

#browser = webdriver.Chrome()
image = Image.open('/Users/shiqinghua/Downloads/image.png')
print(tesserocr.image_to_text(image))