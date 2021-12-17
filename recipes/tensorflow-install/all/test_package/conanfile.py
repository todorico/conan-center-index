import os
import shutil

from conans import ConanFile, tools
from conan.tools.cmake import CMake, CMakeToolchain
from conan.tools.layout import cmake_layout

class TestPackage(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    generators = "CMakeDeps", "CMakeToolchain", "VirtualBuildEnv", "VirtualRunEnv"

    @property
    def _package(self):
        return self.deps_cpp_info["tensorflow"]

    def layout(self):
        cmake_layout(self)

    def generate(self):
        cmake_tc = CMakeToolchain(self)
        cmake_tc.variables["_package_name"] = self._package.name
        cmake_tc.variables["_package_version"] = self._package.version
        cmake_tc.preprocessor_definitions["_package_name"] = self._package.name
        cmake_tc.preprocessor_definitions["_package_version"] = self._package.version
        cmake_tc.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def test(self):
        if not tools.cross_building(self):
            test = os.path.join(self.cpp.build.bindirs[0], "test_package")
            self.run(test, env="conanrun")
        self._remove_artifacts()

    #####################################################################################

    def _remove_artifacts(self):
        for file in ["conan.lock", "conanbuildinfo.txt", "conaninfo.txt", "graph_info.json"]:
            file_path = os.path.join(self.folders.source_folder, file)
            if os.path.isfile(file_path):
                os.remove(file_path)
        shutil.rmtree(self.folders.build_folder, ignore_errors=True)
