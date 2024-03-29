import logging
import os
# import shutil
# import glob
# from pathlib import Path
#
# from selenium.webdriver import ActionChains
# from selenium.webdriver.common.by import By
#
# from selenium import webdriver
# from os.path import isfile, join
# import time
# MAX_TXT_TO_PINYIN_SIZE = 270000

CLEANED_FILES_DIRECTORY = 'cleaned_files'
CLEANED_FILES_SUFFIX = '_cleaned'
# Sentences That should not be added to the completed file.
GARBAGE_SENTENCES = ['',
                     "",
                     "。",
                     "\n"]

logger = logging.getLogger('autoanki')
logger.setLevel(logging.INFO)


class BookCleaner:

    def __init__(self):
        self.file_list = []
        self.bookpath = ""

    def clean(self, bookpath: str):
        """
        Cleans the files contained in the bookpath. If bookpath is a single file, clean it.
        :return: The path to the cleaned file(s)
        """
        if not os.path.exists(bookpath):
            # PRACTICE Should I raise an error here, or let the caller raise one?
            logger.warning("BookCleaner: Cannot find path [" + str(bookpath) + "]")
            return None

        # If the bookpath is a single file, clean and return it
        if os.path.isfile(bookpath):
            cleaned_path = self._clean_file(bookpath, cleaned_files_root=None)
            return cleaned_path
        # Otherwise, get a list of files to clean, and return the cleaned files directory
        else:
            dirty_files = []
            for root, dirs, files in os.walk(bookpath):
                for file in files:
                    # Only clean files that are not in cleaned_files directory
                    in_cleaned = str(root).find(CLEANED_FILES_DIRECTORY) != -1
                    if not in_cleaned:
                        if '.txt' in file:
                            dirty_files.append(os.path.join(root, file))

            # Check this cleaning won't be mean to the CPU
            if len(dirty_files) > 50:
                yn = input("The number of files is very large. Are you sure you want to convert this many files? (Y/N)")
                if yn.lower() != 'y':
                    return None

        # Now we have a list of files to convert in a list
        cleaned_files = []

        # Create directory for files
        cleaned_files_root = os.path.join(bookpath, CLEANED_FILES_DIRECTORY)
        if not os.path.exists(cleaned_files_root):
            os.mkdir(cleaned_files_root)

        for file in dirty_files:
            cleaned_filepath = self._clean_file(file, cleaned_files_root=cleaned_files_root)
            cleaned_files.append(cleaned_filepath)

        # print(dirty_files)
        # print(cleaned_files)

        return cleaned_files

    @staticmethod
    def _clean_file(filepath, cleaned_files_root):
        """
        Takes a txt file and cleans it up, putting every sentence on a new line
        :param filepath: The txt file to clean
        :param cleaned_files_root: The root
        :return:
        """

        # Set the directory where the cleaned file will go
        if not cleaned_files_root:
            # root/test1.txt -> root/hello_cleaned.txt
            new_filepath = os.path.splitext(filepath)[0] + CLEANED_FILES_SUFFIX + os.path.splitext(filepath)[1]
        else:
            new_filepath = os.path.join(cleaned_files_root, '/'.join(filepath.split('/')[1:]))

        # Clean page file of characters that may cause issues.
        page_file = open(filepath, encoding='utf-8')
        page_sentences = page_file.read().split("。")
        cleaned_file = open(new_filepath, "w", encoding='utf-8')

        for page_sentence in page_sentences:
            # Clean string
            page_sentence = page_sentence\
                .lstrip()\
                .rstrip()\
                .replace("  ", " ")\
                .lstrip("\"")\
                .rstrip("\"")\
                .replace("”","'")\
                .replace("　", "")\
                .replace("“","")\
                .rstrip("。")\
                .strip("'")\
                .strip("'")
            if page_sentence not in GARBAGE_SENTENCES:
                cleaned_file.write(page_sentence + "。" + "\n")

        return new_filepath

    # @staticmethod
    # def _compact_file(page_path):
    #
    #     print("Compacting...")
    #     """
    #     # Compacts all of the different pages in this directory into a specified size.
    #     # Compacted in this context means that the files are re-organized by size, not chapter/webpage
    #     # Some websites used have a free limit of 300kb, for example. Rather then pass all of these pages through one by
    #     # one, it is more efficient to compact these into 299kb files and send those.
    #     Currently not in use
    #     # :return: True if success
    #     """
    #     all_pages_text = ""
    #
    #     for page_path in self.pages:
    #         page = open(self.bookpath + "\\" + page_path, "r", encoding="utf-8")
    #         for i in range(file_len(self.bookpath + "\\" + page_path)):
    #             all_pages_text += page.readline()
    #
    #     print("Found " + str(len(self.pages)) + " pages totalling " + str(len(all_pages_text)) + " characters.")
    #
    #     # Splits the all_pages_text into smaller parts and saves it to the compacted_pages directory.
    #     i, current_compacted_filename_number = 0, 0
    #     all_pages_sentences = all_pages_text.split("\n")
    #     current_compacted_file_size = 0
    #     current_compacted_file_text = ""
    #     while i < len(all_pages_sentences):
    #
    #         current_sentence = all_pages_sentences[i]
    #
    #         # If the current file has hit its limit, start a new compacted file and reset all variables
    #         if (len(current_sentence) + current_compacted_file_size) > self.MAX_TXT_TO_PINYIN_SIZE:
    #             current_compacted_filename_number += 1
    #             current_file = open(self.compacted_pages_directory + "\\" + "compacted-" + str(
    #                 current_compacted_filename_number) + ".txt", "w",
    #                                 encoding="utf-8")
    #             for line in current_compacted_file_text.split("\n"):
    #                 current_file.write(line + "\n")
    #             current_file.close()
    #             current_compacted_file_size = 0
    #             current_compacted_file_text = ""
    #
    #         # Chinese characters are utf-8, meaning they are 8 bytes
    #         current_compacted_file_size += len(current_sentence) * 3
    #         current_compacted_file_text += current_sentence
    #         # A newline character is one byte
    #         current_compacted_file_size += 1
    #         current_compacted_file_text += "\n"
    #
    #         i += 1
    #
    #     current_compacted_filename_number += 1
    #     current_file = open(
    #         self.compacted_pages_directory + "\\" + "compacted-" + str(current_compacted_filename_number) + ".txt",
    #         "w",
    #         encoding="utf-8")
    #     for line in current_compacted_file_text.split("\n"):
    #         current_file.write(line + "\n")
    #     current_file.close()
    #
    #     print("Done compacting")
    #     return True