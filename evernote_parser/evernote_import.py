#!/usr/bin/env python

from base64 import b64decode
import hashlib
import logging
from lxml import etree
import os
from pypandoc import convert_text
from time import strptime

import settings

# logging
logger = logging.getLogger("parser")
logger.setLevel(logging.DEBUG)

fh = logging.FileHandler('evernote_import.log')
fh.setLevel(logging.DEBUG)

# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s -'
                              ' %(levelname)s - %(message)s')
fh.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(fh)

# http://www.hanxiaogang.com/writing/parsing-evernote-export-file-enex-using-python/
p = etree.XMLParser(remove_blank_text=True, resolve_entities=False)


def parse_content(content):
    """
    
    :param content: 
    :return: converted text
    """
    try:
        text = convert_text(content, settings.TO_FORMAT_EXT, format='html',
                            extra_args=["+RTS", settings.HEAP, "-RTS"])
    except:
        text = 'too big'
    return text


def parse_resource(resource):
    """
    
    :param resource: 
    :return: 
    """
    rsc_dict = {}
    for elem in resource:
        if elem.tag == 'data':
            # Some times elem.text is None
            rsc_dict['data'] = b64decode(elem.text) if elem.text else b''
            rsc_dict['hash'] = hashlib.md5(rsc_dict[elem.tag]).hexdigest()
        else:
            rsc_dict[elem.tag] = elem.text

    return rsc_dict


def parse_note(note):
    """    
    :param note: 
    :return: 
    """
    note_dict = {}
    resources = []
    for elem in note:
        if elem.tag == 'content':
            if 'en-crypt' not in elem.text:
                note_dict['content'] = parse_content(elem.text)
            else:
                note_dict['content'] = parse_content('content is encrypted. '
                                                     'Note can not be displayed.'
                                                     ' Give up')
            # A copy of original content
            note_dict['content-raw'] = elem.text
        elif elem.tag == 'resource':
            resources.append(parse_resource(elem))
        elif elem.tag == 'created' or elem.tag == 'updated':
            note_dict[elem.tag] = strptime(elem.text, '%Y%m%dT%H%M%SZ')
        elif elem.tag == 'en-note':
            pass
        else:
            note_dict[elem.tag] = elem.text

    note_dict['resource'] = resources

    return note_dict


def parse_note_xml(xml_file):
    """
    Without huge_tree set to True, parser may complain about huge text node
    Try to recover, because there may be "&nbsp;", which will cause
    "XMLSyntaxError: Entity 'nbsp' not defined"
    
    :param xml_file: 
    :return: 
    """
    context = etree.iterparse(xml_file,
                              encoding='utf-8',
                              strip_cdata=False,
                              huge_tree=True,
                              recover=True)
    for action, elem in context:
        if elem.tag == "note":
            yield parse_note(elem)


def write_resource(note_dir, resources):
    """
    write the resource data
    :param note_dir: 
    :param resources: 
    """
    for resource in resources:
        rsc_file = os.path.join(note_dir, resource['hash']+'.data')
        data = resource['data']
        with open(rsc_file, 'wb') as fd:
            fd.write(data)


def write_bak(bak_file, content_raw):
    """
    write the 'raw' version of the note    
    :param bak_file: 
    :param content_raw: 
    """
    with open(bak_file, 'w') as fd:
        fd.write(content_raw)


def write_too_big(title, bak_file, text_file):
    """
    
    :param title: 
    :param bak_file: 
    :param text_file: 
    :return: 
    """
    logger.warning('%s too big - try to execute pandoc "%s"'
                   ' -t %s -f html -o "%s"' % (title, bak_file,
                                               settings.TO_FORMAT,
                                               text_file))
    # create a shell script that can be executed manually
    dir_path = os.path.dirname(os.path.realpath(__file__))
    shell = os.path.join(dir_path, 'evernote_import_manual.sh')
    with open(shell, 'a+') as fd:
        line = 'pandoc "{bak_file}" -t {to_format} -f html -o "{text_file}"'\
            .format(bak_file=bak_file,
                    to_format=settings.TO_FORMAT,
                    text_file=text_file)
        fd.write(line + '\n')


def write_note(text_file, note):
    """
    write the content of the note
    :param text_file: 
    :param note: 
    """
    with open(text_file, 'w') as fd:
        # Write the original title
        fd.write(settings.HEADING1 + note['title'] + '\n')
        fd.write(note['content'])


def get_export_dir(date):
    """
    get the directory where the file are exported
    :param date: 
    :return: path to the directory 
    """
    year = str(date.tm_year)
    mon = '%02d' % date.tm_mon
    mday = '%02d' % date.tm_mday
    return os.path.join('en-export', year, mon, mday)


def export_note(note):
    """
    Save notes and attachments in directories named according to date of creation  
    :param note: 
    """
    note_dir = get_export_dir(note['created'])
    os.makedirs(note_dir, exist_ok=True)

    # Remove "/" from filenames
    title = note['title'].replace('/', ' ')[:settings.TITLE_SIZE_LIMIT]
    text_file = os.path.join(note_dir, title + '.' + settings.TO_FORMAT_EXT)

    if 'too big' not in note['content']:
        write_note(text_file, note)

    bak_file = os.path.join(note_dir, title + '.bak')
    write_bak(bak_file, note['content-raw'])

    if note['content'] == 'too big':
        write_too_big(title, bak_file, text_file)

    write_resource(note_dir, note['resource'])

if __name__ == '__main__':

    notes = parse_note_xml('mynote.enex')
    for note in notes:
        export_note(note)
