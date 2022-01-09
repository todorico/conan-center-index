import os

from conans import ConanFile, tools
from conan.tools.cmake import CMake, CMakeToolchain

required_conan_version = ">=1.44.0"


class TestPackage(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    generators = "VirtualRunEnv"

    @property
    def _pkg(self):
        return self.dependencies["acvd"]

    def _pkg_prop(self, prop):
        return self._pkg.cpp_info.get_property(prop)

    def generate(self):
        cmake_tc = CMakeToolchain(self)
        cmake_tc.variables["_pkg_name"] = "ACVD"
        cmake_tc.variables["_pkg_version"] = self._pkg.ref.version
        cmake_tc.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()
        cmake.install()  # not needed with layout

    def test(self):
        if not tools.cross_building(self):
            # test = os.path.join(self.cpp.build.bindirs[0], "test_package") # with layout only
            test = os.path.join(self.package_folder, "test_package")
            self.run(test, env="conanrun")
