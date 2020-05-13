#!/usr/local/bin/python3

import csv
import requests
import os

from indig_parl_logger_2 import get_logger
# from indig_parl_logger import get_logger

utils_logger = get_logger("Indig_Parl_Utils",
                          a_log_file='NWT/logs/indig_parl_utils_debug.log')


def get_file_list(directory, ext='all-files'):
    files = os.listdir(directory)
    for file in files:
        if not os.path.isfile(file):
            files.pop(files.index(file))
    if not ext == 'all-files':
        for file in files:
            if not file.endswith(ext):
                files.pop(files.index(file))
    return files


def download_docx(web_loc, date, directory="docs/"):
    """Downloads a docx file from webaddress 'web_loc' and saves it to location
    'directory'

    Arguments:
        web_loc {[type]} -- [description]
        date {[type]} -- [description]

    Keyword Arguments:
        directory {str} -- [description] (default: {"docs/"})

    Returns:
        string -- with path to downloaded file
    """
    [name] = web_loc.split('/')[-1:]
    r = requests.get(web_loc)
    file_loc = directory+"["+date+"]"+name
    with open(file_loc, 'wb') as f:
        f.write(r.content)
    utils_logger.debug('File written to: %s' % file_loc)
    return file_loc


def download_pdf(web_loc, date, directory="pdfs/"):
    """Downloads a pdf file form webaddress 'web_loc' and saves it to location
    'directory'

    Arguments:
        web_loc {[type]} -- [description]
        date {[type]} -- [description]

    Keyword Arguments:
        directory {str} -- [description] (default: {"pdfs/"})

    Returns:
        string -- path to downloaded file
    """
    '''
    date should be in following format: 180601
    '''
    [name] = web_loc.split('/')[-1:]
    r = requests.get(web_loc)
    file_loc = directory+"["+date+"]"+name
    with open(file_loc, 'wb') as f:
        f.write(r.content)
    utils_logger.debug('File written to: %s' % file_loc)
    return file_loc


def csv_from_list(csv_name, csv_list, header_row=[]):
    """Creates a CS file from a list of lists ('csv_list') and stores it to
    location 'csv_name'.

    Arguments:
        csv_name {[type]} -- [description]
        csv_list {[type]} -- [description]
    """
    with open(csv_name, mode='w') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"',
                                quoting=csv.QUOTE_ALL)
        if header_row:
            csv_writer.writerow(header_row)
        for line in csv_list:
            row = []
            for idx in range(len(line)):
                row.append(line[idx])
            csv_writer.writerow(row)
        utils_logger.debug('Created csv file :%s' % csv_name)


def send_text_to_file(file_path, data, header='', data_type='text'):
    """Store string data from different python objects to file. 

    Arguments:
        file_path {[type]} -- [description]
        data {[type]} -- [description]

    Keyword Arguments:
        header {str} -- [description] (default: {''})
        data_type {str} -- [description] (default: {'text'})
    """
    with open(file_path, 'w') as f:
        if header:
            utils_logger.debug('Adding header %s' % header)
            f.write(header.title() + '\n\n')
        if data_type == 'list':
            utils_logger.debug('Creating text file form Python list.')
            for line in data:
                f.write(line + '\n')
        elif data_type == 'dict':
            utils_logger.debug('Creating text file form Python dictionary.')
            for item in data.keys():
                f.write(item + ': ' + data[item] + '\n')
        elif data_type == 'tup_list':
            utils_logger.debug(
                'Creating text file form Python list of tuples.')
            for (a, b) in data:
                f.write(a+' - '+b+'\n')
        else:
            utils_logger.debug('Creating text file form Python string.')
            f.write(data)


def get_source_links(source_file):
    location_dict = {}
    lines = 0
    count = 0
    with open(source_file, newline='') as csv_f:
        csv_reader = csv.reader(csv_f, delimiter=',', quotechar='"')
        for row in csv_reader:
            if lines == 0:
                lines += 1
            else:
                word = row[3]
                pdf = row[4]
                session = row[0] + '-' + row[1]
                location_dict['['+str(count)+']'+row[2]] = session, word, pdf
                count += 1

    return location_dict


def download_hansards(links_csv_file, doc_dir="docs/", pdf_dir="pdfs/"):
    # preferred in ['docs','pdfs','both']
    links_filename = links_csv_file.split('.')[0]
    utils_logger.debug('[links_csv_file]: %s, [links_filename] %s' %
                       (links_csv_file, links_filename))
    hansards_path_dict = get_source_links(links_csv_file)
    doc_paths = {}
    pdf_paths = {}
    txt_out = []
    print('Downloading Hansards ')
    for key in hansards_path_dict.keys():
        [dte] = key.split(']')[-1:]
        dte_lst = dte.split('-')
        dte_ok = True
        for idx in range(3):
            if len(dte_lst[idx]) < 2:
                dte_lst[idx] = '0' + dte_lst[idx]
                dte_ok = False
        if not dte_ok:
            dte = '-'.join(dte_lst)

        doc_location = ''
        pdf_location = ''
        valid = hansards_path_dict[key][1].endswith('.docx')
        if valid:
            doc_location = download_docx(hansards_path_dict[key][1], dte,
                                         directory=doc_dir)
            doc_paths[key] = (hansards_path_dict[key][0],
                              hansards_path_dict[key][1],
                              doc_location)
        elif hansards_path_dict[key][2].endswith('.pdf'):
            pdf_location = download_pdf(hansards_path_dict[key][2], dte,
                                        directory=pdf_dir)
            pdf_paths[key] = (hansards_path_dict[key][0],
                              hansards_path_dict[key][2],
                              pdf_location)
        txt_line = ','.join([hansards_path_dict[key][0],
                             hansards_path_dict[key][1], doc_location,
                             hansards_path_dict[key][2], pdf_location])
        txt_out.append(txt_line)
        print('^')
        utils_logger.debug('\t%s\n\t\t%s:%s\n\t\t%s:%s' %
                           (key, hansards_path_dict[key][1], doc_location,
                            hansards_path_dict[key][2], pdf_location))
    send_text_to_file(links_filename + '_docs.csv', txt_out, data_type='list')
    print('List of downloaded handards created:', links_filename + '_docs.csv')

    return doc_paths, pdf_paths


if __name__ == '__main__':
    my_files = get_file_list('/Users/curtishendricks/Downloads/')
    for file in my_files:
        print(file)