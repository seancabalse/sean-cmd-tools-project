'''
Author: seancabalse
CreatedAt: 28/08/2021 1:00PM
'''

__all__ = [
    'initialize_logger',
    'initialize_parser',
    'generate_path_string',
    'retrieve_files',
    'rename_files',
    'duplicate_files',
    'check_if_directory'    
]


# %% Import modules here
import argparse
import os
from os import path
import glob
import shutil
import logging
import sys



# %% Define functions here\
    
# Function to iniatialize logger here
def initialize_logger(level):
    global logger
    log_level = getattr(logging,level.upper(), None)
    if not isinstance(log_level, int):
        raise ValueError('Invalid log level: %s' % level)
    logging.basicConfig(
        filename='bulk_renamer_logs.log',
        level=log_level,
        format='[%(asctime)s %(levelname)s %(module)s %(lineno)d - %(message)s'
                        )
    logger = logging.getLogger(__name__)
   
    
# Function to initialize argparse parser
def initialize_parser():
    parser = argparse.ArgumentParser(description='Rename all files that match a filter pattern in the target directory')
    
    # Add parser arguments
    parser.add_argument('new_name', help='The file name pattern which will be used to rename the target files.')
    parser.add_argument('file_pattern', help='The regex that will be used to filter for files in the target directory')
    parser.add_argument('target_dir', help='The directory where the files to be renamed reside')
    
    # Add additional positional arguments
    parser.add_argument('--copy', '-c', type=bool, nargs='?', const=False, help='Duplicates the existing files with the new file names')
    parser.add_argument('--dir', '-d', type=str, help='Destination directory to save the duplicates')
    parser.add_argument('--log-level', '-l', type=str, default='info', help='Set the logging level')
    args = parser.parse_args()
    
    return args


# Determine the file path expression
def generate_path_string(file_pattern, source_dir):
    if (source_dir == None):
        path = os.getcwd() + '\\' + file_pattern # Current working directory
    else:
        if source_dir.strip().endswith('\\'):
            path = source_dir.strip() + file_pattern
        else:
            path = source_dir.strip() + '\\' + file_pattern
    
    return path
        

# Retrieve all file using file path expression
def retrieve_files(filepath_regex):
    file_list = [file for file in glob.glob(filepath_regex)]
    if (file_list == []):
        print('Error: No file was found with that file pattern!')
        logger.error(f'No files were found with the file pattern')
        sys.exit(1)
    return file_list
        

# Function to rename all the files
def rename_files(files_to_rename, new_name, target_dir):
    count = 0
    for file in files_to_rename:
        count+=1
        new_file_name = generate_path_string(new_name, target_dir) + str(count)
        try:
            if file.strip() == new_file_name.strip():
                print(f'Warning: Renaming the file to the same name')
                logger.warning(f'Warning: Renaming the file to the same name')
                continue
            os.rename(file, new_file_name)
            print(f'SUCCESS: {file} --> {new_file_name}')
            logger.info(f'SUCCESS: {file} --> {new_file_name}')
        except FileExistsError as err:
            print(f'Error: {err}')
            logging.error(f'Error: {err}')
            sys.exit(1)
    print('Successfully renamed all files!')
    return sys.exit(0) 
    
    
# Function to check if input directory exists
def check_if_directory(directories):
    for directory in directories:
        if (directory is None or path.exists(directory) ):
            continue
        else:
            print(f'Error: Invalid directory name. Kindly check your input or if the directory exists')
            logger.error(f'Error: Invalid directory name.')
            sys.exit(1)
    if directories[1] is None:
        return directories[0]
    else:
        return directories[1]


# Function to duplicate all the files
def duplicate_files(files_to_copy, new_name, dest_dir):
    count = 0
    for file in files_to_copy:
        count+=1
        new_file_name = generate_path_string(new_name, dest_dir) + str(count)
        try:
            if (file.strip() == new_file_name.strip() or path.exists(new_file_name)):
                print(f'Warning: Same file exist in the destination directory')
                logger.warning(f'Warning: Same file exist in the destination directory')
                continue
            shutil.copy(file, new_file_name)
            print(f'SUCCESS: {file} --> {new_file_name}')
            logger.info(f'SUCCESS: {file} --> {new_file_name}')
        except FileExistsError as err:
            print(f'Error: {err}')
            logger.error(f'Error: {err}')
            sys.exit(1)
    print('Successfully duplicated all files!')
    return sys.exit(0)
    
    

# Main driver code here
def main():
    args = initialize_parser()
    initialize_logger(args.log_level)
    
    cwd = check_if_directory([args.target_dir, args.dir])
 
    file_path = generate_path_string(args.file_pattern, args.target_dir)

    files = retrieve_files(file_path)

    if (args.copy == True):
        duplicate_files(files, args.new_name, cwd)
    else:
        rename_files(files, args.new_name, args.target_dir)

# %% Driver code here
if __name__ == '__main__':
    main()
    
    
    
    