from io import StringIO

import eel

from stratification import (
    init_categories_people,
    read_in_cats,
    run_stratification,
    write_selected_people_to_file
)


class FileContents():

    def __init__(self):
        self.category_raw_content = ''
        self.selection_raw_content = ''
        self.categories = None
        self.columns_data = None
        self.people = None

    def add_category_content(self, file_contents):
        csv_files.category_raw_content = file_contents
        category_file = StringIO(file_contents)
        try:
            self.categories = read_in_cats(category_file)
        except Exception as error:
            # TODO: put error in the GUI box
            print("Error reading in categories: {}".format(error))
        eel.update_categories_output_area(len(self.categories.keys()))
        self.update_run_button()

    def add_selection_content(self, file_contents):
        csv_files.selection_raw_content = file_contents
        people_file = StringIO(file_contents)
        try:
            self.people, self.columns_data = init_categories_people(people_file, self.categories)
        except Exception as error:
            # TODO: put error in the GUI box
            print("Error reading in people: {}".format(error))
        eel.update_selection_output_area(len(self.people.keys()))
        self.update_run_button()

    def update_run_button(self):
        if self.category_raw_content and self.selection_raw_content:
            eel.enable_run_button()

    def run_selection(self):
        success, tries, people_selected = run_stratification(self.categories, self.people, self.columns_data)
        outfile = StringIO()
        write_selected_people_to_file(people_selected, self.categories, self.columns_data, outfile)
        eel.enable_download(outfile.getvalue(), 'file.txt')


# global to hold contents uploaded from JS
csv_files = FileContents()


@eel.expose
def handle_category_contents(file_contents):
    csv_files.add_category_content(file_contents)


@eel.expose
def handle_selection_contents(file_contents):
    csv_files.add_selection_content(file_contents)


@eel.expose
def run_selection():
    csv_files.run_selection()


def main():
    eel.init('web')  # Give folder containing web files
    eel.start('main.html', size=(500, 500))    # Start


if __name__ == '__main__':
    main()
