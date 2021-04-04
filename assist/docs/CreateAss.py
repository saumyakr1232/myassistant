from __future__ import print_function

import io
import os
import time

from googleapiclient import discovery
from googleapiclient.http import MediaIoBaseDownload
from httplib2 import Http
from oauth2client import file, client, tools

DOCS_FILE_ID = '1PY5ccY5HYDDmqnESq6HkZ1hzxZTfatksqOVUxgCu6Yw'
SHEETS_FILE_ID = "sheets_id"
CLIENT_ID_FILE = 'credentials.json'
TOKEN_STORE_FILE = 'token.json'
SCOPES = (  # iterable or space-delimited string
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/documents',
    'https://www.googleapis.com/auth/spreadsheets.readonly',
)
SOURCES = ('text', 'sheets')
SOURCE = 'text'
COLUMNS = ['question_1', 'answer_1', 'question_2', 'answer_2', 'question_3', 'answer_3', 'question_4', 'answer_4'
    , 'question_5', 'answer_5']

TEXT_SOURCE_DATA = (
    ('Www',
     'The first e-mail was sent by Ray Tomlinson in 1971. Tomlinson sent the e-mail to himself as a test e-mail message, containing the text "something like QWERTYUIOP." However, despite sending the e-mail to himself, the e-mail message was still transmitted through ARPANET.\n',
     'some question 2', 'some answer 2', 'some question 3', 'some answer 3', 'some question 4',
     'some answer 4' 'some question 5', 'some answer 5'),
)


def get_http_client():
    """Uses project credentials in CLIENT_ID_FILE along with requested OAuth2
        scopes for authorization, and caches API tokens in TOKEN_STORE_FILE.
    """
    store = file.Storage(TOKEN_STORE_FILE)
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_ID_FILE, SCOPES)
        creds = tools.run_flow(flow, store)
    return creds.authorize(Http())


# service endpoints to Google APIs
HTTP = get_http_client()
DRIVE = discovery.build('drive', 'v3', http=HTTP)
DOCS = discovery.build('docs', 'v1', http=HTTP)
SHEETS = discovery.build('sheets', 'v4', http=HTTP)


def get_data(source):
    """Gets mail merge data from chosen data source.
    """
    if source not in {'sheets', 'text'}:
        raise ValueError('ERROR: unsupported source %r; choose from %r' % (
            source, SOURCES))
    return SAFE_DISPATCH[source]()


def _get_text_data():
    """(private) Returns plain text data; can alter to read from CSV file.
    """
    return TEXT_SOURCE_DATA


def _get_sheets_data(service=SHEETS):
    """(private) Returns data from Google Sheets source. It gets all rows of
        'Sheet1' (the default Sheet in a new spreadsheet), but drops the first
        (header) row. Use any desired data range (in standard A1 notation).
    """
    return service.spreadsheets().values().get(spreadsheetId=SHEETS_FILE_ID,
                                               range='Sheet1').execute().get('values')[1:]  # skip header row


# data source dispatch table [better alternative vs. eval()]
SAFE_DISPATCH = {k: globals().get('_get_%s_data' % k) for k in SOURCES}


def _copy_template(tmpl_id, source, service):
    """(private) Copies letter template document using Drive API then
        returns file ID of (new) copy.
    """
    body = {'name': 'Merged form letter (%s)' % source}
    return service.files().copy(body=body, fileId=tmpl_id,
                                fields='id').execute().get('id')


def merge_template(tmpl_id, source, service):
    """Copies template document and merges data into newly-minted copy then
        returns its file ID.
    """
    # copy template and set context data struct for merging template values
    copy_id = _copy_template(tmpl_id, source, service)
    context = merge.iteritems() if hasattr({}, 'iteritems') else merge.items()

    # "search & replace" API requests for mail merge substitutions
    reqs = [{'replaceAllText': {
        'containsText': {
            'text': '{{%s}}' % key.lower(),  # {{VARS}} are uppercase
            'matchCase': True,
        },
        'replaceText': value,
    }} for key, value in context]

    # send requests to Docs API to do actual merge
    DOCS.documents().batchUpdate(body={'requests': reqs},
                                 documentId=copy_id, fields='').execute()
    return copy_id


def download_assignment(file_id):
    request = DRIVE.files().export_media(fileId=file_id, mimeType='application/pdf')
    os.chdir(os.getcwd())

    fh = io.FileIO("../../data/test.pdf", "w")
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print("Download %d%%." % int(status.progress() * 100))


if __name__ == '__main__':
    merge = {
        # sender data
        'my_name': 'Ayme A. Coder',
        'my_addmission_no': '18SCSE1010138\n',
        'assignment_title': 'assignment 1',
        # - - - - - - - - - - - - - - - - - - - - - - - - - -
        # recipient data (supplied by 'text' or 'sheets' data source)
        'question_1': None,
        'answer_1': None,
        'question_2': None,
        'answer_2': None,
        'question_3': None,
        'answer_3': None,
        'question_4': None,
        'answer_4': None,
        'question_5': None,
        'answer_5': None,

        # - - - - - - - - - - - - - - - - - - - - - - - - - -
        'date': time.strftime('%Y %B %d'),
        # - - - - - - - - - - - - - - - - - - - - - - - - - -

    }

    # get row data, then loop through & process each form letter
    data = get_data(SOURCE)  # get data from data source
    for i, row in enumerate(data):
        merge.update(dict(zip(COLUMNS, row)))
        file_id = merge_template(DOCS_FILE_ID, SOURCE, DRIVE)
        print('Merged letter %d: docs.google.com/document/d/%s/edit' % (
            i + 1, file_id))
    # download_assignment("1BR_GWifF_ps_VPeY3rEqriW6UP--IPZsdonqYuWpYJA")
