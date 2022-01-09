import os

from conan import ConanFile
from conan.tools.cmake import CMake, CMakeToolchain

# TODO: remove legacy imports
from conans import tools

required_conan_version = ">=1.44.0"


def cmake_add_pkg_vars(conanfile, toolchain, package):
    pkg = conanfile.dependencies[package]
    pkg_refs = ["version"]
    for r in pkg_refs:
        toolchain.variables["_pkg_" + r] = getattr(pkg.ref, r)
    pkg_props = ["cmake_file_name", "cmake_target_name"]
    for p in pkg_props:
        toolchain.variables["_pkg_" + p] = pkg.cpp_info.get_property(p)
    pkg_variables = ["_pkg_" + v for v in pkg_refs + pkg_props]
    toolchain.variables["_pkg_variables"] = ";".join(pkg_variables)


class TestPackage(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    generators = "VirtualRunEnv"

    def generate(self):
        tc = CMakeToolchain(self)
        cmake_add_pkg_vars(self, tc, "acvd")
        tc.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()
        cmake.install()

    def test(self):
        if not tools.cross_building(self):
            test = os.path.join(self.package_folder, "test_package")
            self.run(test, env="conanrun")
