'''
    File name: copyright_insert.py
    Author: Vinny Babu Manjaly
'''
import os
import sys

if sys.version_info[0] < 3:
    raise Exception('Python 3 or a more recent version is required.')


class InsertCopyRight:

    def __init__(self):
        '''
        Reading input from yaml file in .github/workflows of the working repository
        '''
        try:
            self.data = {}
            self.data['copyright_string'] = os.environ['INPUT_COPYRIGHTSTRING'].replace(
                '\\n', '\n',
            )
            self.data['file_type'] = os.environ['INPUT_FILETYPE'].replace(
                ' ', '',
            ).split(',')
            if not os.environ['INPUT_PATH']:
                self.data['path'] = ['.']
            else:
                self.data['path'] = os.environ['INPUT_PATH'].replace(
                    ' ', '',
                ).split(',')
            if not os.environ['INPUT_IGNOREPATH']:
                self.data['ignore_path'] = None
            else:
                self.data['ignore_path'] = os.environ['INPUT_IGNOREPATH'].replace(
                    ' ', '',
                ).split(',')

        except Exception as e:
            raise e

    def listing_files(self):
        '''
        Getting all the required files from the directory
        Checking in filename, for file extensions already specified
        Appending to the list "files", all the files to which copyright have to be merged
        '''
        try:
            files = []
            _value = False
            for _path in self.data['path']:
                for _root, _dir, _files in os.walk(_path):
                    if self.data['ignore_path'] is not None:
                        for _ignore_path in self.data['ignore_path']:
                            if (_ignore_path in _root) or (_ignore_path in _root + '/') or \
                                    (_path == '.' and _ignore_path[-1] == '/' and './' + _ignore_path == _root + '/'):
                                _value = True
                                break
                            else:
                                _value = False
                    if _value is False:
                        for _filename in _files:
                            for file_type in self.data['file_type']:
                                if file_type in _filename:
                                    files.append(
                                        os.path.join(_root, _filename),
                                    )
            return files
        except Exception as e:
            raise e

    def content_check(self, files):
        '''
        Opening files in Read-Write mode and reading all contents of file to a variable
        Checking if the file is empty and if not empty, whether copyright exists
        When the file is empty, not writing the copyright string to the file
        When the file is not empty, handling multi line copyright and checking whether its present in the file
        '''
        try:
            for _file in files:
                file = open(_file, 'r+', errors='ignore')
                content = file.readlines()
                if not content:
                    print(
                        _file, 'found to be empty and copyright not added to the file',
                    )
                else:
                    if self.copyright_check(content):
                        print('Copyright already exists in', _file)
                    else:
                        print('Adding copyright notice to', _file)
                        self.insert_copyright(content, file)
        except Exception as e:
            raise e
        finally:
            file.close()

    def copyright_check(self, content):
        '''
        To handle multi line copyright extracting copyright string to a list
        Comparing copyright with contents line by line, considering number of lines the copyright is spread
        On line where comparison fails, returns False value to content_check function to add copyright
        As all lines of copyright are matching, returns true value, indicating copyright exists
        '''
        try:
            copyright_list = set(v.strip() for v in self.data['copyright_string'].split('\n'))
            contents = set(v.strip() for v in content)
            return not contents.isdisjoint(copyright_list)
        except Exception as e:
            raise e

    def insert_copyright(self, content, file):
        '''
        Inserting copyright string to the beginning of content variable
        Rewriting contents with copyright to file
        '''
        try:
            content.insert(0, self.data['copyright_string'])
            file.seek(0)
            file.writelines(content)
        except Exception as e:
            raise e


def main():
    '''
    Instantiating object 'obj' for class InsertCopyRight
    Function to get the files into which copyright has to be added
    Checking if copyright already exists and if not add respectively
    '''
    try:
        obj = InsertCopyRight()
        files = obj.listing_files()
        if files:
            obj.content_check(files)
        else:
            print('WARNING: Wrong directory or no files matching the provided criteria')
    except Exception as e:
        raise e


if __name__ == '__main__':
    main()
