import os

from conans import ConanFile, tools
from conans.errors import ConanInvalidConfiguration

from conan.tools.gnu import Autotools, AutotoolsToolchain
from conan.tools.files import apply_conandata_patches

required_conan_version = ">=1.33.0"


class GPGErrorConan(ConanFile):
    version = "1.36"
    name = "libgpg-error"
    url = "https://github.com/conan-io/conan-center-index"
    homepage = "https://gnupg.org/software/libgpg-error/index.html"
    topics = ("gpg", "gnupg", "encrypt", "pgp", "openpgp")
    description = (
        "Libgpg-error is a small library that originally defined common error values for all GnuPG "
        "components."
    )
    license = "GPL-2.0-or-later"
    settings = "os", "arch", "compiler", "build_type"
    options = {
        "shared": [True, False],
        "fPIC": [True, False],
    }
    default_options = {
        "shared": False,
        "fPIC": True,
    }

    win_bash = True
    exports_sources = "patches/**"
    _autotools = None

    @property
    def _source_subfolder(self):
        return "source_subfolder"

    def config_options(self):
        del self.settings.compiler.libcxx
        del self.settings.compiler.cppstd
        if self.options.shared:
            del self.options.fPIC

    def validate(self):
        if self.settings.os != "Linux" and self.settings.os != "Windows":
            raise ConanInvalidConfiguration(
                "This recipe only support Linux. You can contribute Windows and/or Macos support."
            )

    def source(self):
        tools.get(
            **self.conan_data["sources"][self.version],
            destination=self._source_subfolder,
            strip_root=True,
        )

    def generate(self):
        tc = AutotoolsToolchain(self)
        # tc.default_configure_install_args = True # not working in dev workflow maybe BUG ?
        prefix_path = (
            tools.unix_path(self.install_folder, tools.MSYS2)
            if self.settings.os == "Windows"
            else self.install_folder
        )
        tc.configure_args.extend(
            [
                f"--prefix={prefix_path}/package",
                "--disable-dependency-tracking",
                "--disable-nls",
                "--disable-languages",
                "--disable-doc",
                "--disable-tests",
            ]
        )
        tc.generate()

    def build(self):
        apply_conandata_patches(self)
        autotools = Autotools(self)
        autotools.configure(self._source_subfolder)
        autotools.make()
        autotools.install()

    def package(self):
        self.copy("*", dst="", src="package")

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
        self.cpp_info.names["pkg_config"] = "gpg-error"
        # if self.settings.os in ["Linux", "FreeBSD"]:
        #     self.cpp_info.system_libs = ["pthread"]
