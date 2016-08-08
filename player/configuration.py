import toml
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QCheckBox, QDialog, QGroupBox, QHBoxLayout,
                             QLabel, QLineEdit, QListWidget, QListWidgetItem,
                             QPushButton, QStackedWidget, QVBoxLayout, QWidget)


class FileOptions(QWidget):
    """Contains all of the user configurable options related to the
    file menu."""

    def __init__(self, parent=None):
        """Initializes a page of options to be shown in the
        preferences dialog."""
        super(FileOptions, self).__init__(parent)

        file_config = QGroupBox("File Menu Configuration")

        self.recursive_directory = QCheckBox(
            'Recursively Open Directories (open files in all subdirectories)', self)

        self.settings_file()

        file_config_layout = QHBoxLayout()
        file_config_layout.addWidget(self.recursive_directory)

        file_config.setLayout(file_config_layout)

        main_layout = QVBoxLayout()
        main_layout.addWidget(file_config)
        main_layout.addStretch(1)
        self.setLayout(main_layout)

        self.recursive_directory.stateChanged.connect(self.recursive_directory_option)

    def recursive_directory_option(self):
        """This setting changes the behavior of the Open Directory item in
        the file menu. The default setting only opens songs in the
        selected directory. With this option checked, Open Directory will
        open all songs in the directory and its subdirectories."""
        with open('settings.toml', 'r') as conffile:
            config = toml.load(conffile)

        if self.recursive_directory.isChecked():
            config['recursive_directory'] = True

        elif not self.recursive_directory.isChecked():
            config['recursive_directory'] = False

        with open('settings.toml', 'r+') as conffile:            
            toml.dump(config, conffile)

    def settings_file(self):
        """Sets the options in the preferences dialog to the
        settings defined in settings.toml."""
        with open('settings.toml', 'r') as conffile:
            conffile = conffile.read()
            config = toml.loads(conffile)

        if config['recursive_directory'] is True:
            self.recursive_directory.setChecked(True)
        elif config['recursive_directory'] is False:
            self.recursive_directory.setChecked(False)


class MediaLibrary(QWidget):
    """Contains all of the user configurable options related to the
    media library."""

    def __init__(self, parent=None):
        """Initializes a page of options to be shown in the
        preferences dialog."""
        super(MediaLibrary, self).__init__(parent)

        media_library_config = QGroupBox("Media Library Configuration")

        self.media_library_label = QLabel('Media Library', self)
        self.media_library_line = QLineEdit()
        self.media_library_button = QPushButton('Select Path')

        media_library_config_layout = QHBoxLayout()
        media_library_config_layout.addWidget(self.media_library_label)
        media_library_config_layout.addWidget(self.media_library_line)
        media_library_config_layout.addWidget(self.media_library_button)

        media_library_config.setLayout(media_library_config_layout)

        main_layout = QVBoxLayout()
        main_layout.addWidget(media_library_config)
        main_layout.addStretch(1)
        self.setLayout(main_layout)


class PreferencesDialog(QDialog):
    """Creates a dialog that shows the user all of the user configurable
    options. A list on the left shows all of the available pages, with
    the page's contents shown on the right."""

    def __init__(self, parent=None):
        """Initializes the preferences dialog with a list box on the left
        and a content layout on the right."""

        super(PreferencesDialog, self).__init__(parent)
        self.setWindowTitle('Preferences')
        self.setWindowIcon(QIcon('images/md_settings.png'))
        self.setFixedSize(800, 700)

        self.contents = QListWidget()
        self.pages = QStackedWidget()

        self.pages.addWidget(FileOptions())
        self.pages.addWidget(MediaLibrary())
        self.list_items()

        layout = QHBoxLayout()
        layout.addWidget(self.contents)
        layout.addWidget(self.pages, 1)

        self.setLayout(layout)

        self.contents.currentItemChanged.connect(self.change_page)

    def list_items(self):
        """Lists all of the pages available to the user. Each page houses
        its own user configurable options."""
        file_options = QListWidgetItem(self.contents)
        file_options.setText('File Options')
        file_options.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.contents.setCurrentRow(0)

        media_library_options = QListWidgetItem(self.contents)
        media_library_options.setText('Media Library')

    def change_page(self, current, previous):
        """Changes the page according to the clicked list item."""
        if not current:
            current = previous

        self.pages.setCurrentIndex(self.contents.row(current))
