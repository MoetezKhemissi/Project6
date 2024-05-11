

from config import *

import os
import time
import pandas as pd

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import logging

file_path = os.path.join(os.getcwd(), Main_file)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', filename='app.log', filemode='w')

def login(driver,username_value,password_value):
    # Locate the username and password fields and the submit button
    username = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "user_login"))
        )
    password = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "user_pass"))
        )
    submit_button = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "wp-submit"))
        )

    # Input the username and password
    username.send_keys(username_value)
    time.sleep(0.5)
    password.send_keys(password_value)
    time.sleep(0.5)
    # Click the submit button
    submit_button.click()

def init_driver():

    options = Options()
    options.add_argument("--start-maximized")  # Opens the browser in maximized mode

    # Initialize the WebDriver with options
    driver = webdriver.Chrome(options=options)
    return driver

def navigate_to_import_export(driver):
    # Click on "Magic Page"
    magic_page = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, '#menu-posts-magicpage .wp-menu-name'))
        )
    
    magic_page.click()
    time.sleep(1)  # Wait for the submenu to appear

    # Click on "Settings" under "Magic Page"
    settings = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, 'a[href*="magic-page-settings"]'))
        )
    settings.click()
    time.sleep(1)  # Wait for the settings page to load

    # Click on "Import - Export"
    import_export = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, 'a[href*="magic-page-import-export"]'))
        )
    import_export.click()
    time.sleep(1)  # Wait for the import-export page to load

def delete_database_and_navigate(driver):
    try:
        # Click on "Delete Database"
        delete_button=WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, 'span.delete-database[title="Delete Database"]'))
        )
        delete_button.click()
        time.sleep(1)  # Wait for any confirmation dialog or updates

        # Click on "Database & Locations" button
        db_locations_button=WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, 'button.btn.btn-default'))
        )
        db_locations_button.click()
        time.sleep(1)  # Wait for the subsequent page or modal to load

    except Exception as e:
        logging.error("No database to be deleted or the elements are not accessible.")


def import_db(driver, file_path=file_path,db_name="New database"):
    try:
        # Type the database name into the "Database label" input field
        db_label_input=WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "import_label"))
        )
        db_label_input.clear()
        db_label_input.send_keys(db_name)
        time.sleep(0.5)  # Give it some time after typing

        # Click on the "Continue" button
        continue_button=WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "check-database-exist"))
        )
        continue_button.click()
        time.sleep(1)  # Wait for any possible page updates

        # Handle the file upload
        file_input=WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "upload-dropzone-xls-database"))
        )
        file_input.send_keys(os.path.abspath(file_path))
        time.sleep(1)  # Allow time for the file to be uploaded

    except Exception as e:
        logging.error("Error during database import:", str(e))

def process_and_wait_for_completion(driver):
    try:
        # Click on the "Process Database" button
        process_button=WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "process-database"))
        )
        process_button.click()
        # Wait for the "All Done!" message to appear, indicating the process is complete
        WebDriverWait(driver, 120).until(
            EC.visibility_of_element_located((By.ID, "create-database-release"))
        )

        logging.info("Database is imported successfully !")

    except Exception as e:
        logging.error("Error during processing:", str(e))
def preprocessing(excel1_path, excel2_path):
    # Load data from Excel files
    df1 = pd.read_excel(excel1_path)
    df2 = pd.read_excel(excel2_path)
    
    # Extract location slugs and urls
    slugs = df1['location slug'].tolist()
    urls = df2.iloc[:, 0].tolist()
    
    # Transform slugs for URL matching and for output
    joined_slugs = [''.join(slug.split('-')) for slug in slugs]
    spaced_slugs = [' '.join(slug.split('-')) for slug in slugs]
    
    # Create a map for the output
    results = []
    
    # Process each url and corresponding joined slug
    for url, joined_slug, spaced_slug in zip(urls, joined_slugs, spaced_slugs):
        if joined_slug == "":  # Check if the slug is empty
            raise ValueError(f"Error: No slug found for the website {url}")
        if joined_slug in url:  # Check if modified slug is in the URL
            login = df2[df2.iloc[:, 0] == url].iloc[0, 1]
            password = df2[df2.iloc[:, 0] == url].iloc[0, 2]
            # Append the details to the results list
            results.append({
                'website': url, 
                'login': login, 
                'password': password, 
                'slug': spaced_slug  # Output the slug with spaces
            })
    
    return results

def set_radius(driver, radius_value):
    try:
        # Wait for the radius input field to be visible and clear it
        radius_input = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, 'input.radius_field'))
        )
        radius_input.clear()  # Clear the current value in the input field
        
        # Type the new radius value into the field
        radius_input.send_keys(str(radius_value))
        

    except Exception as e:
        logging.error(f"An error occurred while setting the radius: {str(e)}")

def navigate_and_input(driver, slug_first_word):
    try:
        # Wait and click on the 'Magic Page' link in the menu
        magic_page_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(@class, 'menu-top') and contains(@href, 'post_type=magicpage')]"))
        )
        magic_page_link.click()

        # Wait and click on the 'Location' link
        location_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(@aria-label, '“Location” (Edit)')]"))
        )
        location_link.click()

        # Wait for the input field and type the first word of the slug
        input_field = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "input.magic-page-locs.ui-autocomplete-input"))
        )
        input_field.clear()
        input_field.send_keys(slug_first_word)
        autocomplete_item = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "ul.ui-autocomplete.ui-menu .ui-menu-item div"))
        )
        autocomplete_item.click()
        try:
            set_radius(driver,radius)
        except :
            logging.error(f"An error occurred while setting up the radius: {str(e)}")
        update_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.editor-post-publish-button'))
        )
        update_button.click()  
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")


def click_confirm_email_button(driver):
    try:
        # Wait until the submit button is clickable
        submit_button = WebDriverWait(driver, 2).until(
            EC.element_to_be_clickable((By.ID, "correct-admin-email"))
        )
        # Click the submit button
        submit_button.click()

    except Exception as e:
       print()
try:
    result = preprocessing(Main_file,Logins_file)
except ValueError as e:
    logging.error("Failed to preprocess files ( a website dosen't have a corresponding slug): %s", str(e))
driver=init_driver()
for website_info in result:
    try:
        logging.info("Starting update for website %s ...", website_info["website"])
        driver.get(website_info["website"])
        login(driver,website_info["login"],website_info["password"])
        click_confirm_email_button(driver)
        navigate_to_import_export(driver)
        delete_database_and_navigate(driver)
        import_db(driver)
        process_and_wait_for_completion(driver)
        navigate_and_input(driver,website_info["slug"])
        logging.info("Finished updating sucessfully for website %s !", website_info["website"])
        time.sleep(3)
    except :
        logging.info("Failed to process %s ( Website may be down)", website_info["website"])
time.sleep(100)