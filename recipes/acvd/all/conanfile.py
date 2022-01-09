import os

from conans import ConanFile, tools
from conan.tools.cmake import CMake, CMakeToolchain
from conan.tools.layout import cmake_layout
from conan.tools.files import AutoPackager, apply_conandata_patches, get

required_conan_version = ">=1.44.0"


def prefixed_cmake_layout(conanfile, prefix):
    cmake_layout(conanfile)
    for name in ["build", "generators", "imports", "package", "source"]:
        f = getattr(conanfile.folders, name)
        if not f or f == ".":
            setattr(conanfile.folders, name, name)
        f = getattr(conanfile.folders, name)
        setattr(conanfile.folders, name, os.path.join(prefix, f))


class ACVDConan(ConanFile):
    name = "acvd"
    version = "1.0.0"

    # Optional metadata
    url = "https://github.com/conan-io/conan-center-index"
    homepage = "https://www.creatis.insa-lyon.fr/~valette/public/project/acvd"
    license = "CeCILL-B"
    description = "Library to perform fast simplification of 3D surface meshes."
    topics = "3D", "surface", "mesh", "remeshing"

    # Binary configuration
    settings = "os", "arch", "compiler", "build_type"
    options = {
        "shared": [True, False],
        "fPIC": [True, False],
    }
    default_options = {
        "shared": False,
        "fPIC": True,
    }
    requires = "vtk/8.1.2@sim-and-cure/stable"
    exports_sources = "patches/**"

    _source_subfolder = "source_subfolder"

    def source(self):
        get(
            self,
            **self.conan_data["sources"][self.version],
            destination=self._source_subfolder,
            strip_root=True,
        )
        apply_conandata_patches(self)

    def generate(self):
        tc = CMakeToolchain(self)
        install_prefix = os.path.join(self.install_folder, "package")
        tc.variables["CMAKE_INSTALL_PREFIX"] = install_prefix.replace(os.sep, "/")
        tc.variables["BUILD_DOCUMENTATION"] = "OFF"
        tc.variables["BUILD_EXAMPLES"] = "OFF"
        tc.variables["BUILD_TESTING"] = "OFF"
        tc.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure(self._source_subfolder)
        cmake.build()
        cmake.install()

    def package(self):
        self.copy("*", dst="", src="package")
        self.copy(pattern="LICENSE*", dst="licenses", src=self._source_subfolder)

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
        self.cpp_info.set_property("cmake_file_name", "ACVD")
        self.cpp_info.set_property("cmake_target_name", "ACVD::ACVD")
        # Prevent CMakeDeps from generating another package config file.
        self.cpp_info.set_property("cmake_find_mode", "none")
