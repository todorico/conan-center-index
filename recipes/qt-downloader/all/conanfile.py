import os, sys, subprocess

from conan import ConanFile

# TODO: remove legacy imports
from conans import tools


class PipPackageTool:
    """A simple Python Pip wrapper"""

    def install(self, packages):
        subprocess.check_call([sys.executable, "-m", "pip", "install"] + packages)


class QtDownloaderConan(ConanFile):
    name = "qt-downloader"
    version = "1.0.0"

    # Optional metadata
    homepage = "https://github.com/todorico/qt-downloader"
    license = "MIT"
    description = "Program to download and install qt versions."
    topics = "cli", "qt", "downloader", "installer"

    # Package options
    no_copy_source = True  # skip copy to build_folder

    def system_requirements(self):
        pip = PipPackageTool()
        packages = [
            "lxml==4.6.5",
            "py7zr==0.17.0",
            "requests==2.26.0",
            "semantic-version==2.8.5",
        ]
        pip.install(packages)

    def source(self):
        git = tools.Git(self.source_folder)
        git.clone(
            "https://github.com/todorico/qt-downloader.git",
            branch="master",
            shallow=True,
        )

    def package(self):
        self.copy("qt-downloader*", dst="bin", src=self.source_folder)

    def package_info(self):
        self.env_info.PATH.append(os.path.join(self.package_folder, "bin"))
