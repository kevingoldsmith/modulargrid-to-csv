#!/usr/bin/env python
"""Allows you to take a rack defined in ModularGrid and convert the list of
modules into a .csv file
"""
import argparse
import csv
from bs4 import BeautifulSoup

__author__ = "Kevin Goldsmith"
__copyright__ = "Copyright 2021, Nimble Autonomy LLC"
__credits__ = ["Kevin Goldsmith"]
__license__ = "GPLv3"
__version__ = "0.0.1"
__maintainer__ = "Kevin Goldsmith"
__date__ = "2021/10/03"
__deprecated__ = False


# string constant
__modulargrid_domain_prefix__ = 'https://www.modulargrid.net{}'

def load_file(rack_file:argparse.FileType):
    return rack_file.read()

def parse_file(html_text:str):
    soup = BeautifulSoup(html_text, 'html.parser')

    rack_name = soup.find('h1').find('a').text

    tbody = soup.find('tbody')
    rows = tbody.find_all('tr')
    modules = [['manufacturer', 'module', 'description', 'width (HP)', 'depth (mm)',
                '+12V (mA)', '-12V (mA)', '+5V (mA)', 'url', 'thumbnail', 'row']]
    for row in rows:
        module = {
            'manufacturer': '',
            'name': '',
            'description': '',
            'width': '',
            'depth': '',
            '+12V': '',
            '-12V': '',
            '+5V': '',
            'url': '',
            'thumbnail': '',
            'row': ''
        }
        cols = row.find_all('td')
        
        thumb = cols[0]
        link = thumb.find('a')
        module['url'] = __modulargrid_domain_prefix__.format(link['href'])
        img = link.find('img')
        module['thumbnail'] = __modulargrid_domain_prefix__.format(img['src'])

        name = cols[1]
        module['manufacturer'] = name.contents[0].strip()
        module['name'] = name.contents[1].text
        module['description'] = name.find('small').text

        module['row'] = cols[2].text.strip()
        module['width'] = cols[3].text.replace('\xa0','').replace('HP', '').strip()
        module['depth'] = cols[4].text.replace('\xa0','').replace('mm', '').strip()

        if not cols[5].has_attr('colspan'):
            module['+12V'] = cols[5].text.replace('\xa0','').replace('mA', '').strip()
            module['-12V'] = cols[6].text.replace('\xa0',' ').replace('mA', '').strip()
            module['+5V'] = cols[7].text.replace('\xa0',' ').replace('mA', '').strip()
        else:
            module['+12V'] = '0'
            module['-12V'] = '0'
            module['+5V'] = '0'
        
        modules.append([module['manufacturer'], module['name'],
            module['description'], module['width'], module['depth'],
            module['+12V'], module['-12V'], module['+5V'], module['url'],
            module['thumbnail'], module['row']])
    
    return rack_name, modules

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Convert a ModularGrid Rack to a CSV file')
    parser.add_argument('rack_file', type=argparse.FileType('r'), 
                        help='the html file saved from modulargrid.net')
    args = parser.parse_args()
    html = load_file(args.rack_file)
    rack_name, modules = parse_file(html)
    
    print(f'parsed rack {rack_name}, saving file')

    with open(f'{rack_name}.csv', 'w') as csvfile:
        csvwriter = csv.writer(csvfile, dialect='excel')
        csvwriter.writerows(modules)
