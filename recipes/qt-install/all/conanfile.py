import os, re, shutil

from io import StringIO
from conans import ConanFile, tools
from conans.errors import ConanInvalidConfiguration


class QtConan(ConanFile):
    name = "qt"
    description = "Qt is a cross-platform framework for graphical user interfaces."
    topics = ("qt", "ui")
    url = "https://github.com/conan-io/conan-center-index"
    homepage = "https://www.qt.io"
    license = "LGPL-3.0"

    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True]}  # Shared build only
    default_options = {"shared": True}
    no_copy_source = True  # skip copy to build_folder

    # associate configuration with compatible qt toolchain pattern
    _supported_qt_configurations = {
        "Linux gcc": "gcc_64",
        "Macos apple-clang": "clang_64",
        "Windows Visual Studio": "win64_msvc.*",
        "Windows gcc": "win64_mingw.*",
        "Windows msvc": "win64_msvc.*",
    }
    _source_subdir = "src_subdir"

    @property
    def _configuration(self):
        return f"{self.settings.os} {self.settings.compiler}"

    @property
    def _qt_toolchain_pattern(self):
        return self._supported_qt_configurations[self._configuration]

    @property
    def _qt_downloader_cmd(self):
        return "python3 " + os.path.join(
            self.folders.source_folder, self._source_subdir, "qt-downloader"
        )

    def validate(self):
        if self.settings.arch != "x86_64":
            raise ConanInvalidConfiguration("Only available for x86_64 architecture")

        if self._configuration not in self._supported_qt_configurations:
            supported_configs = list(self._supported_qt_configurations.keys())
            raise ConanInvalidConfiguration(
                f"Configuration '{self._configuration}' is not in the list of supported configurations: {supported_configs}"
            )

    def requirements(self):
        self.requires("openssl/1.1.1m")
        self.options["openssl"].shared = True

    def source(self):
        git = tools.Git(self._source_subdir)
        git.clone(
            "https://github.com/todorico/qt-downloader.git",
            branch="master",
            shallow=True,
        )

    def package(self):
        self._download_qt(self.folders.package_folder)

    def package_id(self):
        self.info.settings.compiler = str(self.settings.compiler)
        del self.info.settings.build_type

    def package_info(self):
        qt_name = "Qt" + str(self.version).split(".")[0]

        self.cpp_info.name = qt_name
        self.cpp_info.names["cmake_find_package"] = qt_name
        self.cpp_info.names["cmake_find_package_multi"] = qt_name

        module_dir = os.path.join("lib", "cmake", qt_name)
        self.cpp_info.builddirs.append(module_dir)

        bin_dir = os.path.join(self.package_folder, "bin")
        plugins_dir = os.path.join(self.package_folder, "plugins")

        for dir in [bin_dir, plugins_dir]:
            self.env_info.PATH.append(dir)

    #####################################################################################

    def _download_qt(self, destination):
        versions = self._discover_available_qt_versions()
        compatible_version = self._find_match(versions, self.version)

        if not compatible_version:
            raise ConanInvalidConfiguration(
                f"Could not find version '{self.version}' in available {self.settings.os} versions"
            )

        toolchains = self._discover_available_qt_toolchains()
        compatible_toolchain = self._find_match(toolchains, self._qt_toolchain_pattern)

        if not compatible_toolchain:
            raise ConanInvalidConfiguration(
                f"Could not find a compatible toolchain '{self._qt_toolchain_pattern}' in available {self.settings.os} toolchains"
            )

        self.output.info(
            f"Downloading Qt {compatible_version} {compatible_toolchain}..."
        )
        # Commented lines for quick testing package creation without downloading everything
        self.run(
            # f"{self._qt_downloader_cmd} {str(self.settings.os).lower()} desktop {self.version} {compatible_toolchain} --output {destination} --modules qtsvg",
            # f"{self._qt_downloader_cmd} {str(self.settings.os).lower()} desktop {self.version} {compatible_toolchain} --output {destination} --opensource --modules qtbase",
            f"{self._qt_downloader_cmd} {str(self.settings.os).lower()} desktop {self.version} {compatible_toolchain} --output {destination} --opensource --addons *",
        )
        self._relocate_qt_install_dir(
            os.path.join(destination, self.version), destination
        )

    def _discover_available_qt_versions(self):
        self.output.info(f"Discovering {self.settings.os} available Qt versions...")
        cmd_output = StringIO()
        self.run(
            f"{self._qt_downloader_cmd} {str(self.settings.os).lower()} desktop",
            output=cmd_output,
        )
        versions = self._parse_discover_available_qt_output(cmd_output.getvalue())
        self.output.info(f"Available versions: {versions}")
        return versions

    def _discover_available_qt_toolchains(self):
        self.output.info(
            f"Discovering {self.settings.os} available Qt {self.version} toolchains..."
        )
        cmd_output = StringIO()
        self.run(
            f"{self._qt_downloader_cmd} {str(self.settings.os).lower()} desktop {self.version}",
            output=cmd_output,
        )
        toolchains = self._parse_discover_available_qt_output(cmd_output.getvalue())
        self.output.info(f"Available toolchains: {toolchains}")
        return toolchains

    def _parse_discover_available_qt_output(self, discover_output: str):
        pattern = "  Choose from: "
        for line in discover_output.splitlines():
            if line.startswith(pattern):
                toolchains = line[len(pattern) :].split(", ")
                return toolchains
        return list[str]()

    def _find_match(self, list, match_pattern):
        r = re.compile(match_pattern)
        for element in list:
            if r.match(element):
                return element
        return None

    # This methods relocate qt install using it's version directory: <version_dir>/<toolchain_dir>/* -> <destination_dir>/*
    def _relocate_qt_install_dir(self, qt_version_dir, destination_dir):
        qt_toolchain_dir = os.path.join(qt_version_dir, os.listdir(qt_version_dir)[0])
        for file in os.listdir(qt_toolchain_dir):
            src = os.path.join(qt_toolchain_dir, file)
            dst = os.path.join(destination_dir, file)
            shutil.move(src, dst)
        shutil.rmtree(qt_version_dir)
