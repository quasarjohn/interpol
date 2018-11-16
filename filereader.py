import re


class FileReader:

    FILE_EXTENSION = 'ipol'

    def read_file(self):
        file_name = input('Script to execute: ')

        if file_name.endswith(FileReader.FILE_EXTENSION):

            try:
                # read file line by line. we'll do line by line parsing later
                file = open(file_name, 'r')
                raw_string = file.read()
                lines = raw_string.split('\n')

                # remove tabs
                lines = [line.replace('\t', '') for line in lines]

                # # remove empty lines
                # lines = self.remove_values_from_list(lines, '')

                for i in range(len(lines)):

                    # space is the delimiter, but we want to not delimit strings, anything in brackets
                    # treat strings as one token
                    # search the line for anything in brackets
                    try:
                        # find string in brackets using regex
                        found = re.findall('\[(.+?)\]', lines[i])

                        # iterate if there are multiple matches
                        for f in found:
                            # findall does not include brackets in the result
                            # re-append the brackets to ensure we are replacing the correct substring
                            original = '[' + f + ']'
                            lines[i] = lines[i].replace(
                                original, original.replace(' ', '&nbsp')).strip()

                    except AttributeError:
                        # no matches found
                        pass

                # not necessary but makes the list cleaner
                # remove double spaces
                for i in range(len(lines)):
                    while('  ' in lines[i]):
                        lines[i] = lines[i].replace('  ', ' ').strip()

                return lines
            except:
                print('File not found. Operation stopped.')

        else:
            print('Incorrect file type. Operation stopped.')

        return ""
    def remove_values_from_list(self, the_list, val):
        return [value for value in the_list if value != val]
