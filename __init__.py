import os
import requests
from bs4 import BeautifulSoup
from aqt import mw
from aqt.editor import Editor
from aqt.qt import QMessageBox
from aqt.gui_hooks import main_window_did_init
from anki.hooks import addHook


# Functions to scrape data (follow their names)
def fetch_hebrew_definition(word):
    url = f"https://milog.co.il/{word}"
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        definition_list = [
            i.text.strip()
            for i in soup.find_all(
                "div", class_="sr_e_txt"
            )  # Get definitions from Milog
        ]
        definition = ""
        # Sort definitions to display no more than 4, sometimes there is an enormous quantity of them on the page
        for i in range(len(definition_list)):
            if len(definition_list) > 3:
                if i < 3:
                    definition += f"{i + 1}. " + definition_list[i] + "<hr>"
                elif i == 3:
                    definition += f"{i + 1}. " + definition_list[i]
                    break
            else:
                if i < len(definition_list) - 1:
                    definition += f"{i + 1}. " + definition_list[i] + "<hr>"
                elif i == len(definition_list) - 1:
                    definition += f"{i + 1}. " + definition_list[i]
                    break
        return definition
    else:
        return


def fetch_english_translation(word):
    url = f"https://context.reverso.net/translation/hebrew-english/{word}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"  # Needed for access to the site
    }
    response = requests.get(url, headers=headers)
    print(response.status_code)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        translation_list = soup.findAll(
            "span", class_="display-term"
        )  # Get translations from Reverso
        translation = ""
        # Sort translations to display no more than 4
        for i in range(len(translation_list)):
            if len(translation_list) > 3:
                if i < 3:
                    translation += translation_list[i].text + " | "
                elif i == 3:
                    translation += translation_list[i].text
                    break
            else:
                if i < len(translation_list) - 1:
                    translation += translation_list[i].text + " | "
                elif i == len(translation_list) - 1:
                    translation += translation_list[i].text
                    break
        return str(translation)
    else:
        return


def fetch_russian_translation(word):
    url = f"https://context.reverso.net/translation/hebrew-russian/{word}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    print(response.status_code)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        translation_list = soup.findAll("span", class_="display-term")
        translation = ""
        for i in range(len(translation_list)):
            if len(translation_list) > 3:
                if i < 3:
                    translation += translation_list[i].text + " | "
                elif i == 3:
                    translation += translation_list[i].text
                    break
            else:
                if i < len(translation_list) - 1:
                    translation += translation_list[i].text + " | "
                elif i == len(translation_list) - 1:
                    translation += translation_list[i].text
                    break
        return str(translation)
    else:
        return


def fetch_hebrew_image(word):
    url = f"https://www.google.com/search?udm=2&q={word}"
    response = requests.get(url)
    if response.status_code == 200:
        try:
            soup = BeautifulSoup(response.content, "html.parser")
            image = soup.findAll("img", src=True)[1]
            if image is None:
                return
            return str(image)
        except Exception:
            return
    else:
        return


def fetch_hebrew_info(word):
    url = f"https://milog.co.il/{word}"
    response = requests.get(url)
    if response.status_code == 200:
        try:
            soup = BeautifulSoup(response.content, "html.parser")
            info = soup.find("div", class_="sr_e").find("div").find("a").text
            if info is None:
                return
            return info
        except Exception:
            return
    else:
        return


def fetch_hebrew_forms(word):
    url = f"https://www.pealim.com/en/search/?q={word}"
    response = requests.get(url)
    if response.status_code == 200:
        try:
            soup = BeautifulSoup(response.content, "html.parser")
            url2 = "https://www.pealim.com" + soup.find(
                "div", class_="verb-search-lemma"
            ).find("a").get("href")
            response = requests.get(url2)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, "html.parser")
                forms = soup.find(
                    "table", class_="table table-condensed conjugation-table"
                )
                if forms is None:
                    return
                return str(forms)
            else:
                return
        except Exception:
            return
    else:
        return


# Adding our custom model/template for notes
def add_english_model():
    col = mw.col  # Access the collection
    mm = col.models  # Access the models

    model_name = "Hebrew English Simple"
    # Check if the model already exists to avoid duplicates
    existing_model = mm.byName(model_name)
    if existing_model:
        return

    model = mm.new(model_name)
    model["type"] = 0  #
    model[
        "css"
    ] = """
    

    .card {
    font-family: arial;
    font-size: 20px;
    text-align: center;
    background-color: #F9F6E6;
    color: black;
		width: 100vw;
		height: 100vh;
    }

    .card > * {
        border-radius: 9px;
    }
	hr {
		border: none;
    }

    h2 {
    	padding: 10px;
    }
    .content {
    	display: flex;
    		align-items: center;
    		jujstify-content: center;
    flex-direction: column;
    		margin-top: 100px;
    }

    .content > div {
    width: 75%;
    }

    h1 {
    	font-size: 72px;
        background-color: #BAD8B6;
    }

    h2 {
    	font-size: 36px;
        font-weight: 400;
        background-color: #E1EACD;
    }

    p {
        color: #8D77AB;
    }

    img {
      width: 250px;
      height: 250px;
      object-fit: fill;
    }

    /* General table styling */
    .conjugation-table {
      width: 100%;
      border-collapse: collapse;
      font-family: Arial, sans-serif;
      font-size: 14px;
      background-color: #f9f9f9;
    }

    /* Header styles */
    .conjugation-table thead th {
      background-color: #ffc107;
      color: #4a4a4a;
      font-weight: bold;
      text-align: center;
      padding: 8px;
      border: 1px solid #ddd;
    }

    /* Body cell styles */
    .conjugation-table tbody td, 
    .conjugation-table tbody th {
      text-align: center;
      padding: 6px 8px;
      border: 1px solid #ddd;
    }

    /* Row and column grouping */
    .conjugation-table tbody th[rowspan] {
      background-color: #ffd54f;
      color: #333;
      vertical-align: middle;
    }

    .conjugation-table .column-header {
      background-color: #ffe082;
      font-weight: bold;
      font-size: 13px;
    }

    /* Compact cells */
    .conjugation-table td.conj-td {
      padding: 4px;
      font-size: 13px;
    }

    /* Menukad (Hebrew text) styling */
    .conjugation-table .menukad {
      font-size: 16px;
      color: #333;
      font-weight: bold;
    }

    .conjugation-table .transcription {
      font-size: 12px;
      color: #555;
    }

    /* Popover styles for aux forms */
    .conjugation-table .popover-host {
      position: relative;
    }

    .conjugation-table .popover-host .aux-forms {
      display: none;
      position: absolute;
      top: 100%;
      left: 50%;
      transform: translateX(-50%);
      background: #fff;
      border: 1px solid #ccc;
      padding: 6px;
      font-size: 12px;
      box-shadow: 0 2px 6px rgba(0, 0, 0, 0.15);
      z-index: 1000;
      width: 200px;
    }

    .conjugation-table .popover-host:hover .aux-forms {
      display: block;
    }

    /* Hover and zebra-striping */
    .conjugation-table tbody tr:nth-child(odd) {
      background-color: #fffde7;
    }

    .conjugation-table tbody tr:hover {
      background-color: #ffecb3;
    }

    /* Responsive table for smaller screens */
    @media (max-width: 768px) {
      .conjugation-table {
        font-size: 12px;
      }

      .conjugation-table th,
      .conjugation-table td {
        padding: 4px;
      }
    }


    """

    # Define fields
    field_1 = mm.newField("Word")
    field_2 = mm.newField("Definition")
    field_3 = mm.newField("Image")
    field_4 = mm.newField("Info")
    field_5 = mm.newField("English")
    field_6 = mm.newField("Forms")
    field_7 = mm.newField("Audio Optional")
    mm.addField(model, field_1)
    mm.addField(model, field_2)
    mm.addField(model, field_3)
    mm.addField(model, field_4)
    mm.addField(model, field_5)
    mm.addField(model, field_6)
    mm.addField(model, field_7)

    # Define card templates
    template = mm.newTemplate("Card 1")

    template[
        "qfmt"  # For front
    ] = """
    <div class="content">
        <div>
        	<h1>{{Word}}</h1>
        	<div class="image">{{Image}}</div>
        	<div class="table-div">{{Forms}}</div>
        </div>
    </div>
    """

    template[
        "afmt"  # For back
    ] = """
    <div class="content">
        <div>
            <h1>{{Word}}</h1>
            <h2>{{Definition}}</h2>
            <p>{{Info}}</p>
            <p>{{English}}</p>
            <div class="image">{{Image}}</div>
            {{Forms}}
        </div>
    </div>
    """
    mm.addTemplate(model, template)

    # Add the model to the collection with simple command
    mm.add(model)


def add_russian_model():
    col = mw.col  # Access the collection
    mm = col.models  # Access the models

    model_name = "Hebrew Russian Simple"
    # Check if the model already exists to avoid duplicates
    existing_model = mm.byName(model_name)
    if existing_model:
        return

    model = mm.new(model_name)
    model["type"] = 0  #
    model[
        "css"
    ] = """
    

    .card {
    font-family: arial;
    font-size: 20px;
    text-align: center;
    background-color: #F9F6E6;
    color: black;
		width: 100vw;
		height: 100vh;
    }

    .card > * {
        border-radius: 9px;
    }

    .content {
    	display: flex;
    		align-items: center;
    		jujstify-content: center;
    flex-direction: column;
    		margin-top: 100px;
    }
	hr {
		border: none;
    }
    
    h2 {
    	padding: 10px;
    }
    .content > div {
    width: 75%;
    }

    h1 {
    	font-size: 72px;
        background-color: #BAD8B6;
    }

    h2 {
    	font-size: 36px;
        font-weight: 400;
        background-color: #E1EACD;
    }

    p {
        color: #8D77AB;
    }

    img {
      width: 250px;
      height: 250px;
      object-fit: fill;
    }

    /* General table styling */
    .conjugation-table {
      width: 100%;
      border-collapse: collapse;
      font-family: Arial, sans-serif;
      font-size: 14px;
      background-color: #f9f9f9;
    }

    /* Header styles */
    .conjugation-table thead th {
      background-color: #ffc107;
      color: #4a4a4a;
      font-weight: bold;
      text-align: center;
      padding: 8px;
      border: 1px solid #ddd;
    }

    /* Body cell styles */
    .conjugation-table tbody td, 
    .conjugation-table tbody th {
      text-align: center;
      padding: 6px 8px;
      border: 1px solid #ddd;
    }

    /* Row and column grouping */
    .conjugation-table tbody th[rowspan] {
      background-color: #ffd54f;
      color: #333;
      vertical-align: middle;
    }

    .conjugation-table .column-header {
      background-color: #ffe082;
      font-weight: bold;
      font-size: 13px;
    }

    /* Compact cells */
    .conjugation-table td.conj-td {
      padding: 4px;
      font-size: 13px;
    }

    /* Menukad (Hebrew text) styling */
    .conjugation-table .menukad {
      font-size: 16px;
      color: #333;
      font-weight: bold;
    }

    .conjugation-table .transcription {
      font-size: 12px;
      color: #555;
    }

    /* Popover styles for aux forms */
    .conjugation-table .popover-host {
      position: relative;
    }

    .conjugation-table .popover-host .aux-forms {
      display: none;
      position: absolute;
      top: 100%;
      left: 50%;
      transform: translateX(-50%);
      background: #fff;
      border: 1px solid #ccc;
      padding: 6px;
      font-size: 12px;
      box-shadow: 0 2px 6px rgba(0, 0, 0, 0.15);
      z-index: 1000;
      width: 200px;
    }

    .conjugation-table .popover-host:hover .aux-forms {
      display: block;
    }

    /* Hover and zebra-striping */
    .conjugation-table tbody tr:nth-child(odd) {
      background-color: #fffde7;
    }

    .conjugation-table tbody tr:hover {
      background-color: #ffecb3;
    }

    /* Responsive table for smaller screens */
    @media (max-width: 768px) {
      .conjugation-table {
        font-size: 12px;
      }

      .conjugation-table th,
      .conjugation-table td {
        padding: 4px;
      }
    }


    """

    # Define fields
    field_1 = mm.newField("Word")
    field_2 = mm.newField("Definition")
    field_3 = mm.newField("Image")
    field_4 = mm.newField("Info")
    field_5 = mm.newField("Russian")
    field_6 = mm.newField("Forms")
    field_7 = mm.newField("Audio Optional")
    mm.addField(model, field_1)
    mm.addField(model, field_2)
    mm.addField(model, field_3)
    mm.addField(model, field_4)
    mm.addField(model, field_5)
    mm.addField(model, field_6)
    mm.addField(model, field_7)

    # Define card templates
    template = mm.newTemplate("Card 1")

    template[
        "qfmt"  # For front
    ] = """
    <div class="content">
        <div>
        	<h1>{{Word}}</h1>
        	<div class="image">{{Image}}</div>
        	<div class="table-div">{{Forms}}</div>
        </div>
    </div>
    """

    template[
        "afmt"  # For back
    ] = """
    <div class="content">
        <div>
            <h1>{{Word}}</h1>
            <h2>{{Definition}}</h2>
            <p>{{Info}}</p>
            <p>{{Russian}}</p>
            <div class="image">{{Image}}</div>
            {{Forms}}
        </div>
    </div>
    """
    mm.addTemplate(model, template)

    # Add the model to the collection with simple command
    mm.add(model)


# Proccess and fill up the fields
def process(editor: Editor):
    # Check if note exists
    note = editor.note
    if not note:
        QMessageBox.warning(
            editor.parentWindow, "Error", "No note is currently being edited."
        )
        return

    # Retrieve word from the first field
    word = note.fields[0].strip()
    if not word:
        QMessageBox.warning(editor.parentWindow, "Error", "Field 'Word' is empty.")
        return

    # Look up definition, image, etc (follow variable names)
    definition = fetch_hebrew_definition(word)
    if not definition:
        definition = "NOT FOUND"

    image = fetch_hebrew_image(word)
    if not image:
        image = "NOT FOUND"

    info = fetch_hebrew_info(word)
    if not info:
        info = "No additional info"

    if "English" in note:
        translation = fetch_english_translation(word)
        if not translation:
            translation = ""
    elif "Russian" in note:
        translation = fetch_russian_translation(word)
        if not translation:
            translation = ""

    forms = fetch_hebrew_forms(word)
    if not forms:
        forms = ""

    # Update note fields (done in different try/except for clarity)
    try:
        note["Definition"] = definition  # Update the "Definition" field
        editor.loadNote()  # Refresh the editor to show the updated field
    except Exception:
        QMessageBox.warning(
            editor.parentWindow,
            "Error",
            "Needed fields do not exist in this note type OR You've inserted extra space in 'Word' field OR You've inserted text with decorations",
        )

    try:
        note["Info"] = info
        editor.loadNote()
    except Exception:
        QMessageBox.warning(
            editor.parentWindow,
            "Error",
            "Needed fields do not exist in this note type.",
        )
    try:
        note["Image"] = image
        editor.loadNote()
    except Exception:
        QMessageBox.warning(
            editor.parentWindow,
            "Error",
            "Needed fields do not exist in this note type.",
        )
    if "English" in note:
        try:
            note["English"] = translation
            editor.loadNote()
        except Exception:
            QMessageBox.warning(
                editor.parentWindow,
                "Error",
                "Needed fields do not exist in this note type.",
            )
    elif "Russian" in note:
        try:
            note["Russian"] = translation
            editor.loadNote()
        except Exception:
            QMessageBox.warning(
                editor.parentWindow,
                "Error",
                "Needed fields do not exist in this note type.",
            )
    try:
        note["Forms"] = forms
        editor.loadNote()
    except Exception:
        QMessageBox.warning(
            editor.parentWindow,
            "Error",
            "Needed fields do not exist in this note type.",
        )


# Add a button to the editor
def add_editor_button(buttons, editor: Editor):
    editor._links["process"] = process
    return buttons + [
        editor._addButton(
            os.path.join(
                os.path.dirname(__file__), "media/logo/logo.png"
            ),  # "/full/path/to/icon.png",
            "process",  # link name that we defined above
            "Insert word, click!",
        )
    ]


# Hooks (Legacy (1st) and New (2nd))
addHook("setupEditorButtons", add_editor_button)


def on_main_window_initialized():
    add_english_model()
    add_russian_model()


main_window_did_init.append(on_main_window_initialized)
