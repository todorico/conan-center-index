import os
import re
import glob

# from pprint import pformat
from io import StringIO
from conans import ConanFile, tools
from conans.errors import ConanInvalidConfiguration
from conans.model.version import Version

class QtConan(ConanFile):
    name = "qt"
    description ="Qt is a cross-platform framework for graphical user interfaces."
    topics = ("qt", "ui")
    url = "https://github.com/conan-io/conan-center-index"
    homepage = "https://www.qt.io"
    license = "LGPL-3.0"

    settings = "os", "compiler", "build_type", "arch"
    options = {
        "shared": [True, False]
    }
    default_options = {
        "shared": True
    }
    no_copy_source = True # skip copy to build_folder

    # associate configuration with compatible qt toolchain pattern
    _supported_configuration_qt_toolchain = {
        "Linux gcc": "gcc_64",
        "Macos apple-clang": "clang_64",
        "Windows Visual Studio": "win64_msvc.*",
        "Windows gcc": "win64_mingw.*",
        "Windows msvc": "win64_msvc.*",
    }
    _source_subdir = "_source_subdir"

    @property
    def _configuration(self):
        return f"{self.settings.os} {self.settings.compiler}"

    @property
    def _qt_toolchain_pattern(self):
        return self._supported_configuration_qt_toolchain[self._configuration]

    def validate(self):
        if self.options.shared == False:
            raise ConanInvalidConfiguration("Only available with shared=True")
        if self.settings.arch != "x86_64":
            raise ConanInvalidConfiguration("Only available for x86_64 architecture")
        if self._configuration not in self._supported_configuration_qt_toolchain:
            supported_configs = list(self._supported_configuration_qt_toolchain.keys())
            raise ConanInvalidConfiguration(f"Configuration '{self._configuration}' is not in the list of supported configurations: {supported_configs}")

    def source(self):
        git = tools.Git(self._source_subdir)
        git.clone("https://github.com/todorico/qt-downloader.git", branch="master", shallow=True)

        versions = self._discover_available_qt_versions()
        compatible_version = self._find_match(versions, self.version)
        if not compatible_version:
            raise ConanInvalidConfiguration(f"Could not find version '{self.version}' in available {self.settings.os} versions")

        toolchains = self._discover_available_qt_toolchains()
        compatible_toolchain = self._find_match(toolchains, self._qt_toolchain_pattern)
        if not compatible_toolchain:
            raise ConanInvalidConfiguration(f"Could not find a compatible toolchain '{self._qt_toolchain_pattern}' in available {self.settings.os} toolchains")

        self.output.info(f"Downloading Qt {compatible_version} {compatible_toolchain}...")
        # Commented lines for quick testing package creation without downloading everything
        # self.run(f"python3 {self._source_subdir}/qt-downloader {str(self.settings.os).lower()} desktop {self.version} {compatible_toolchain} --modules qtsvg")
        # self.run(f"python3 {self._source_subdir}/qt-downloader {str(self.settings.os).lower()} desktop {self.version} {compatible_toolchain} --opensource --modules qtbase")
        self.run(f"python3 {self._source_subdir}/qt-downloader {str(self.settings.os).lower()} desktop {self.version} {compatible_toolchain} --opensource --addons *")

    def package(self):
        qt_dir = glob.glob(f"{self.folders.source_folder}/{self.version}/*")[0]
        self.copy("*", src=f"{qt_dir}", dst=".")

    def package_id(self):
        self.info.settings.compiler = str(self.settings.compiler)
        del self.info.settings.build_type

    def package_info(self):
        qt_name = f"Qt{Version(self.version).major().removesuffix('.Y.Z')}"

        self.cpp_info.name = qt_name
        self.cpp_info.names["cmake_find_package"] = qt_name
        self.cpp_info.names["cmake_find_package_multi"] = qt_name

        module_dir = os.path.join("lib", "cmake", qt_name) # lib/cmake/Qt{4,5,6,...}
        self.cpp_info.builddirs.append(module_dir)

        bin_dir = os.path.join(self.package_folder, "bin")
        plugins_dir = os.path.join(self.package_folder, "plugins")

        for dir in [bin_dir, plugins_dir]:
            self.output.info("Appending PATH environment variable: {}".format(dir))
            self.env_info.PATH.append(dir)

    #####################################################################################

    def _discover_available_qt_versions(self):
        self.output.info(f"Discovering {self.settings.os} available Qt versions...")
        discover_output = StringIO()
        self.run(f"python3 {self._source_subdir}/qt-downloader {str(self.settings.os).lower()} desktop", output=discover_output)
        versions = self._parse_discover_available_qt_output(discover_output.getvalue())
        self.output.info(f"Available versions: {versions}")
        return versions

    def _discover_available_qt_toolchains(self):
        self.output.info(f"Discovering {self.settings.os} available Qt {self.version} toolchains...")
        discover_output = StringIO()
        self.run(f"python3 {self._source_subdir}/qt-downloader {str(self.settings.os).lower()} desktop {self.version}", output=discover_output)
        toolchains = self._parse_discover_available_qt_output(discover_output.getvalue())
        self.output.info(f"Available toolchains: {toolchains}")
        return toolchains

    def _parse_discover_available_qt_output(self, discover_output: str):
        pattern = "  Choose from: "
        for line in discover_output.splitlines():
            if line.startswith(pattern):
                toolchains = line[len(pattern):].split(', ')
                return toolchains
        return list[str]()

    def _find_match(self, list, element_pattern):
        r = re.compile(element_pattern)
        for element in list:
            if r.match(element):
                return element
        return None
