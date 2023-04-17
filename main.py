import os
import logging

from AutoAnki import AutoAnki, cli
# from AutoAnki.BookCleaner import BookCleaner
# from AutoAnki.DatabaseManager import DatabaseManager
# from AutoAnki.Dictionary.YellowBridgeDictionary import YellowBridgeDictionary


def main():

    # logger = logging.getLogger('AutoAnki')
    # logger.setLevel(logging.INFO)
    #
    # # Test BookCleaner
    # bc = BookCleaner()
    # book_path = os.path.join('media', 'test_files', 'test1.txt')
    # # book_path = os.path.join('media')
    # cleaned_path = bc.clean(book_path)
    #
    # # Test DatabaseManager
    # db_path = os.path.join('media', 'databases', 'AutoAnki1.db')
    # if not DatabaseManager.is_database(db_path):
    #     logger.info("Creating database...")
    #     DatabaseManager.create_autoanki_db(db_path)
    #     logger.info("Done creating database.")
    # db = DatabaseManager(db_path)
    # db.add_book(cleaned_path, "Test 1")
    #
    # dict = YellowBridgeDictionary()


    db_path = os.path.join('media', 'databases', 'AutoAnki1.db')
    aa = AutoAnki(db_path)

    bookpath = os.path.join('media', 'test_files', 'test1.txt')
    aa.add_book(bookpath, 'My first book😆')

    aa.complete_unfinished_definitions()

    aa.create_deck("Auto-Generated-Deck")

    # # terminal.terminal_interface("Test")
    #
    # print(aa.book_list)

    # aa.update_definitions()

    # aa.create_deck()

    # aa.add_book_to_database(os.path.join('media', 'sample_text.txt'), '皮肤颜色。：你好')
    #
    # print("\n")


if __name__ == "__main__":
    main()
