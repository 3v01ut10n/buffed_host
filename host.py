import subprocess
import sys
import re

red = "\x1b[1;31m"
green = "\x1b[1;32m"
yellow = "\x1b[1;33m"
blue = "\x1b[1;34m"
pink = "\x1b[1;35m"
light_blue = "\x1b[1;36m"
white = "\x1b[1;37m"

color_domain = green
color_ip = white
color_ptr = blue
сolor_mail = pink
color_error = red

regexp = r"(xn--)?(www.)?([а-яА-ЯёЁa-zA-Z0-9\-\.]+\.([а-яА-ЯёЁa-zA-Z0-9+\-\-a-zA-Z0-9\-\.]+))|\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b|[a-zA-Z0-9\-]+\Z"

try:
    if len(sys.argv) == 2:  # Checking by the number of specified arguments.
        my_arg = re.search(regexp, sys.argv[1]).group(0)  # Get rid of slashes, protocol and relative URIs.
        my_arg = my_arg.encode('idna')
        my_arg = str(my_arg, 'utf-8')
        out = subprocess.check_output(['host', my_arg], universal_newlines=True)
        text = out.split('\n')
        for row in text:
            row = row.split(' ')
            if 'address' in row:
                print(color_domain + row[0] + '\x1b[0m' + ':', color_ip + row[-1] + '\x1b[0m')
                IP = (row[-1])
                try:
                    ptr = subprocess.check_output(['host', IP], universal_newlines=True)  # Запрос PTR
                    ptr_row = ptr.split(' ')
                    print('PTR:', color_ptr + ptr_row[-1] + '\x1b[0m')
                except Exception as e:
                    print(color_error + 'PTR for ' + IP + ' not found' + '\x1b[0m')
            elif 'mail' in row:
                mail = row[-1]
                priort = row[5]
                server = row[0]
                print(color_domain + row[0] + '\x1b[0m', 'MX', '\x1b[1;38m' + priort + '\x1b[0m',
                      сolor_mail + mail + ' \x1b[0m')
            elif 'pointer' in row:
                IP = my_arg
                ptr_row = row
                print('PTR record for IP:', color_ptr + ptr_row[-1] + '\x1b[0m')
    elif len(sys.argv) >= 3:
        my_arg = re.search(regexp, sys.argv[3]).group(0)
        subprocess.call(['host', sys.argv[1], sys.argv[2], my_arg], universal_newlines=True)
    elif len(sys.argv) == 1:
        print(
            '\nUsage:\n\thost [\x1b[1;34mdomain.name, http://domain.name\x1b[0m]\n\thost -t [\x1b[1;32mmx, a, txt ,ptr, aaaa, etc...\x1b[0m] [\x1b[1;34mdomain.name, http://domain.name\x1b[0m]\n')
    else:
        subprocess.call(['host'])
except subprocess.CalledProcessError as exc:
    print(color_error + exc.output + '\x1b[0m')
except IndexError as exc:
    print('Invalid сommand', color_error + sys.argv[1] + '\x1b[0m')
