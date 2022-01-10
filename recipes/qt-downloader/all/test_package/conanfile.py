from conan import ConanFile

# TODO: remove legacy imports
from conans import tools


class TestPackage(ConanFile):
    settings = "os"
    generators = "VirtualRunEnv"

    def test(self):
        if not tools.cross_building(self):
            print("[TEST] qt-downloader --help should work")
            self.run("qt-downloader --help", env="conanrun")
