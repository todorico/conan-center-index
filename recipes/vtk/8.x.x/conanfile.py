import os

from itertools import chain

from conans import ConanFile, tools
from conan.tools.cmake import CMake, CMakeToolchain
from conan.tools.files import apply_conandata_patches
from conan.tools.layout import cmake_layout
from conan_vtk_options import get_vtk_groups, get_vtk_modules

required_conan_version = ">=1.40.0"


def camel2snake(s):
    return "".join(["_" + c.lower() if c.isupper() else c for c in s]).lstrip("_")


def snake2camel(s):
    return "".join(word.title() for word in s.split("_"))


class VTKConan(ConanFile):

    # Information
    version = "8.1.2"
    name = "vtk"
    description = "The Visualization Toolkit (VTK) is open source software for manipulating and displaying scientific data."
    topics = ("visualization", "scientific", "processing")
    url = "https://github.com/conan-io/conan-center-index"
    homepage = "https://vtk.org/"
    license = "MIT"
    exports = "conan_vtk_options.py", "patches*"

    # Configuration
    settings = "os", "compiler", "build_type", "arch"

    _groups = get_vtk_groups(version).keys()
    _modules = get_vtk_modules(version).keys()

    options = {
        "shared": [True, False],
        "fPIC": [True, False],
    }
    options.update({o: [True, False, "default"] for o in chain(_groups, _modules)})
    # options.update({m: [True, False, None] for m in _modules})

    default_options = {
        "shared": True,
        "fPIC": True,
    }
    default_options.update({o: "default" for o in chain(_groups, _modules)})
    default_options.update(
        {
            "group_standalone": True,
            "group_qt": True,
            "module_infovis_boost": True,
            "module_infovis_boost_graph_algorithms": True,
        }
    )

    short_paths = True

    _data_subfolder = "subfolder"

    # def __init__(self):
    # super()
    # self.options.update({g: [True, False] for g in self._group_options})
    # super().__init__()

    def _to_vtk_group(self, option):
        return get_vtk_groups(self.version)[option]

    def _to_vtk_module(self, option):
        return get_vtk_modules(self.version)[option]

    def _to_vtk_choice(self, option):
        if option == "default":
            return "DEFAULT"
        elif option:
            return "ON"
        else:
            return "OFF"

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def requirements(self):
        if self.options.group_qt:
            self.requires("qt/5.12.12@sim-and-cure/stable")
            self.options["qt"].shared = True
        if self.options.group_rendering:
            self.requires("opengl/system")
        if (
            self.options.module_infovis_boost
            or self.options.module_infovis_boost_graph_algorithms
        ):
            self.requires("boost/1.77.0")

    def source(self):
        git = tools.Git(self._data_subfolder)
        git.clone(
            "https://github.com/Kitware/VTK", branch=f"v{self.version}", shallow=True
        )

    # def layout(self):  # not ready yet problem for dev workflow
    #     self.folders.source = self._data_subfolder
    #     self.folders.build = self._data_subfolder

    #     cmake_layout(self)
    #     # self.folders.
    #     self.folders.build = self.build_folder
    #     self.folders.generators = os.path.join(self.folders.build, "conan")

    # self.folders.build = "tmp/build"

    # self.output.info("source: " + str(self.source_folder))
    # self.output.info("build: " + str(self.build_folder))
    # self.folders.source = self.source_folder
    # self.folders.build = self.build_folder

    def generate(self):
        tc = CMakeToolchain(self)
        tc.variables["BUILD_TESTING"] = "OFF"
        tc.variables["BUILD_EXAMPLES"] = "OFF"
        # cmake_tc.variables["PYTHON_LIBRARY"] = (
        #     sys.exec_prefix.replace("\\", "/") + "/libs/python3.lib"
        # )

        for g in self._groups:
            o = self.options.get_safe(g)
            if o != "default":
                tc.variables[self._to_vtk_group(g)] = self._to_vtk_choice(o)

        for m in self._modules:
            o = self.options.get_safe(m)
            if o != "default":
                tc.variables[self._to_vtk_module(m)] = self._to_vtk_choice(o)

        tc.generate()

    def build(self):
        apply_conandata_patches(self)
        cmake = CMake(self)
        cmake.configure(self._data_subfolder)
        cmake.build()
        # cmake.definitions["BUILD_TESTING"] = "OFF"
        # cmake.definitions["BUILD_EXAMPLES"] = "OFF"
        # cmake.definitions["BUILD_SHARED_LIBS"] = self.options.shared

        # cmake.definitions["VTK_Group_IMAGING"]=self.options.group_imaging
        # cmake.definitions["VTK_Group_MPI"]=self.options.group_mpi
        # cmake.definitions["VTK_Group_Qt"]=self.options.group_qt
        # cmake.definitions["VTK_Group_Rendering"]=self.options.group_rendering
        # cmake.definitions["VTK_Group_StandAlone"]=self.options.group_standalone
        # cmake.definitions["VTK_Group_Tk"]=self.options.group_tk
        # cmake.definitions["VTK_Group_Views"]=self.options.group_views
        # cmake.definitions["VTK_Group_Web"]=self.options.group_web

        # if self.settings.os == 'Macos':
        #     cmake.definitions["CMAKE_INSTALL_NAME_DIR"] = "@rpath"

        # cmake.definitions["VTK_Group_IMAGING"]=self.options.group_imaging
        # cmake.definitions["VTK_Group_MPI"]=self.options.group_mpi
        # cmake.definitions["VTK_Group_Qt"]=self.options.group_qt
        # cmake.definitions["VTK_Group_Rendering"]=self.options.group_rendering
        # cmake.definitions["VTK_Group_StandAlone"]=self.options.group_standalone
        # cmake.definitions["VTK_Group_Tk"]=self.options.group_tk
        # cmake.definitions["VTK_Group_Views"]=self.options.group_views
        # cmake.definitions["VTK_Group_Web"]=self.options.group_web

        # if self.settings.build_type == "Debug" and self.settings.compiler == "Visual Studio":
        #     cmake.definitions["CMAKE_DEBUG_POSTFIX"] = "_d"

        # if self.settings.os == 'Macos':
        #     self.env['DYLD_LIBRARY_PATH'] = os.path.join(self.build_folder, 'lib')
        #     self.output.info("cmake build: %s" % self.build_folder)

        #     if self.settings.compiler == 'apple-clang' and tools.Version(self.settings.compiler.version).major >= '12':
        #         self.output.info("apple-clang v12 detected")
        #         cmake.definitions["CMAKE_CXX_FLAGS"] = "-Wno-implicit-function-declaration"
        #         cmake.definitions["CMAKE_C_FLAGS"] = "-Wno-implicit-function-declaration"

        # cmake.configure(source_folder=self.source_folder+'/'+self._source_subdir,build_folder='build')

        # if self.settings.os == 'Macos':
        #     # run_environment does not work here because it appends path just from
        #     # requirements, not from this package itself
        #     # https://docs.conan.io/en/latest/reference/build_helpers/run_environment.html#runenvironment
        #     lib_path = os.path.join(self.build_folder, 'lib')
        #     self.run('DYLD_LIBRARY_PATH={0} cmake --build build {1} -j'.format(lib_path, cmake.build_config))
        # else:
        #     cmake.build()
        # cmake.install()

    # # From https://git.ircad.fr/conan/conan-vtk/blob/stable/8.2.0-r1/conanfile.py
    # def cmake_fix_path(self, file_path, package_name):
    #     try:
    #         tools.replace_in_file(
    #             file_path,
    #             self.deps_cpp_info[package_name].rootpath.replace('\\', '/'),
    #             "${CONAN_" + package_name.upper() + "_ROOT}",
    #             strict=False
    #         )
    #     except:
    #         self.output.info("Ignoring {0}...".format(package_name))

    # def cmake_fix_macos_sdk_path(self, file_path):
    #     # Read in the file
    #     with open(file_path, 'r') as file:
    #         file_data = file.read()

    #     if file_data:
    #         # Replace the target string
    #         file_data = re.sub(
    #             # Match sdk path
    #             r';/Applications/Xcode\.app/Contents/Developer/Platforms/MacOSX\.platform/Developer/SDKs/MacOSX\d\d\.\d\d\.sdk/usr/include',
    #             '',
    #             file_data,
    #             re.M
    #         )

    #         # Write the file out again
    #         with open(file_path, 'w') as file:
    #             file.write(file_data)

    def package(self):
        cmake = CMake(self)
        cmake.install()
        # for path, subdirs, names in os.walk(os.path.join(self.package_folder, 'lib', 'cmake')):
        #     for name in names:
        #         if fnmatch(name, '*.cmake'):
        #             cmake_file = os.path.join(path, name)

        #             # if self.options.external_tiff:
        #                 # self.cmake_fix_path(cmake_file, "libtiff")
        #             # if self.options.external_zlib:
        #                 # self.cmake_fix_path(cmake_file, "zlib")

        #             if tools.os_info.is_macos:
        #                 self.cmake_fix_macos_sdk_path(cmake_file)

    def package_info(self):
        self.cpp_info.names["cmake_find_package"] = "VTK"
        self.cpp_info.names["cmake_find_package_multi"] = "VTK"
        self.cpp_info.libs = tools.collect_libs(self)

        # version = str(self.version).split(".")
        # module_dir = os.path.join("lib", "cmake", f"{version[0]}.{version[1]}")

        # self.cpp_info.builddirs.append(module_dir)

        # version_split = self.version.split('.')
        # short_version = "%s.%s" % (version_split[0], version_split[1])

        # self.cpp_info.includedirs = [
        #     "include/vtk-%s" % short_version,
        #     "include/vtk-%s/vtknetcdf/include" % short_version,
        #     "include/vtk-%s/vtknetcdfcpp" % short_version
        # ]

        # if self.settings.os == 'Linux':
        #     self.cpp_info.libs.append('pthread')

    #####################################################################################
