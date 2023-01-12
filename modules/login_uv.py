from os import getcwd, makedirs
import uuid

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import urllib.request

def get_user_uv(user="", password=""):

    if(len(user) == 0 or len(password) == 0):
        return "No se ha introducido un usuario o matricula valida"
    

    DRIVER_PATH = '/path/to/chromedriver'
    #options = Options()
    #options.add_argument("--window-size=1920,1200")
    #driver = webdriver.Chrome(executable_path=DRIVER_PATH)

      
    options = Options()
    options.add_argument("start-maximized"); 
    #options.add_argument("--headless"); # ejecutar chrome sin abrir la ventana
    options.add_argument("disable-infobars"); 
    options.add_argument("--disable-extensions"); 
    options.add_argument("--disable-gpu"); 
    options.add_argument("--disable-dev-shm-usage"); 
    options.add_argument("--no-sandbox");
    #options.binary_location = "/mnt/c/Program Files/Google/Chrome/Application/chrome.exe"
    options.binary_location = "/usr/bin/google-chrome"
    driver = webdriver.Chrome(chrome_options = options,executable_path=DRIVER_PATH)


    driver.get('https://dsia.uv.mx/miuv/escritorio/login.aspx')
    #print(driver.page_source)

    USERNAME = user
    PASSWORD = password  
    try:
        #driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)
        
        driver.find_element(By.XPATH, '//*[@id="txtPassword"]').send_keys(PASSWORD)
        driver.find_element(By.XPATH, '//*[@id="txtUser"]').send_keys(USERNAME)
        driver.find_element(By.XPATH, '//*[@id="btnValidacion"]').click()
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="Slide1P1Grid1X2"]/a')))
        driver.find_element(By.XPATH, '//*[@id="Slide1P1Grid1X2"]/a').click()

        #driver.get('https://dsiapes.uv.mx/MiUVestudiantes/portales/estudiantes/szigral.aspx')
        full_name =  driver.find_element(By.XPATH, '//*[@id="nombreUsuario_lblNombre"]').text
        inst_email = driver.find_element(By.XPATH, '//*[@id="content_wucDatosGralAlum1_lblCorrInst"]').text

        student_tel = driver.find_element(By.XPATH, '//*[@id="content_wucDatosGralAlum1_lblTel"]').text
        student_photo_profile = driver.find_element(By.XPATH, '//*[@id="content_wucDatosGralAlum1_imgFoto"]').get_attribute('src')
        
        new_name_picture = uuid.uuid4()
    
        makedirs('uploads', exist_ok=True)
        makedirs('uploads/pictures/', exist_ok=True)
        
        new_path_picture = getcwd() + "/uploads/pictures/" + str(new_name_picture)+".png"
        

        
        university_prog = driver.find_element(By.XPATH, '//*[@id="content_wucDatosGralAlum1_lblProg"]').text
        university_fac = driver.find_element(By.XPATH, '//*[@id="content_wucDatosGralAlum1_lblFac"]').text

        university_campus = driver.find_element(By.XPATH, '//*[@id="content_wucDatosGralAlum1_lblcampus"]').text
        university_level = driver.find_element(By.XPATH, '//*[@id="content_wucDatosGralAlum1_lblNivel"]').text
        university_per = driver.find_element(By.XPATH, '//*[@id="content_wucDatosGralAlum1_lblPerCur"]').text

        driver.get(student_photo_profile)
        driver.save_screenshot(new_path_picture)
        student_photo_profile =  new_path_picture
        
        
        driver.get('https://dsiapes.uv.mx/MiUVestudiantes/escritorio/smutiles.aspx#')
        
        student_data = {
            "nombre": full_name.replace('-', ' '),
            "telefono": student_tel,
            "foto_perfil": student_photo_profile,
            "correo": inst_email,
            "programa": university_prog,
            "facultad": university_fac,
            "campus": university_campus,
            "nivel": university_level,
            "periodo_actual": university_per
        }
        print(student_data)
        driver.find_element(By.XPATH, '//*[@id="li-salir"]').click()
        return student_data
    except NoSuchElementException:
        return "No fue posiible loguearse"
        #print(driver.page_source)
    finally:
        driver.quit()
