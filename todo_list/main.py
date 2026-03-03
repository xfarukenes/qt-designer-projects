import sys
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6 import uic

class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()

        # Load the UI from the .ui file
        uic.loadUi("todo_list.ui", self)

        # click events for buttons
        self.add_button.clicked.connect(self.add_task)
        self.delete_button.clicked.connect(self.delete_task)


    # Add a new task to the list
    def add_task(self):
        task = self.task_input.text()

        if task == "":
            self.task_input.setPlaceholderText("Please enter a task.")

        else:
            self.task_list.addItem(task)
            self.task_input.clear()


    # Delete the selected task(s) from the list
    def delete_task(self):
        selected_items = self.task_list.selectedItems()

        if not selected_items:
            self.task_input.setPlaceholderText("Please select a task to delete.")

        else:
            for item in selected_items:
                self.task_list.takeItem(self.task_list.row(item))
            




        







if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainApp()
    main_window.show()
    sys.exit(app.exec())