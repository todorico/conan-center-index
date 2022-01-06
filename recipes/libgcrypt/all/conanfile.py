import os
from conans import ConanFile, tools
from conans.errors import ConanInvalidConfiguration

from conan.tools.gnu import Autotools, AutotoolsToolchain
from conan.tools.files import apply_conandata_patches
from conan.tools.env import Environment


required_conan_version = ">=1.33.0"


class LibgcryptConan(ConanFile):
    # version = "1.8.4"
    name = "libgcrypt"
    url = "https://github.com/conan-io/conan-center-index"
    homepage = "https://www.gnupg.org/download/index.html#libgcrypt"
    description = "Libgcrypt is a general purpose cryptographic library originally based on code from GnuPG"
    topics = ("libgcrypt", "gcrypt", "gnupg", "gpg", "crypto", "cryptography")
    license = "LGPL-2.1-or-later"
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
                "This recipe only support Linux and Windows subsystems. You can contribute Macos support."
            )

    def requirements(self):
        self.requires("libgpg-error/1.36@sim-and-cure/stable")
        # self.requires("libcap/2.50")

    def source(self):
        tools.get(
            **self.conan_data["sources"][self.version],
            destination=self._source_subfolder,
            strip_root=True,
        )

    def _maybe_msys2_path(self, path):
        return (
            tools.unix_path(path, tools.MSYS2)
            if self.settings.os == "Windows"
            else path
        )

    def generate(self):
        tc = AutotoolsToolchain(self)
        # tc.default_configure_install_args = True # not working in dev workflow maybe BUG ?

        libgpg_error = self.dependencies["libgpg-error"]
        tc.configure_args.extend(
            [
                f"--with-gpg-error-prefix={self._maybe_msys2_path(libgpg_error.package_folder)}",
                f"--prefix={self._maybe_msys2_path(self.install_folder)}/package",
                "--disable-doc",
            ]
        )
        tc.generate()

    def build(self):
        autotools = Autotools(self)
        autotools.configure(self._source_subfolder)
        autotools.make()
        autotools.install()

    def package(self):
        self.copy("*", dst="", src="package")
        self.copy(pattern="COPYING*", dst="licenses", src=self._source_subfolder)
        tools.remove_files_by_mask(os.path.join(self.package_folder, "lib"), "*la")
        tools.rmdir(os.path.join(self.package_folder, "lib", "pkgconfig"))
        tools.rmdir(os.path.join(self.package_folder, "share"))

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
        self.cpp_info.names["pkg_config"] = "gcrypt"

        # self.cpp_info.libs = ["gcrypt"]
        # bin_path = os.path.join(self.package_folder, "bin")
        # self.output.info("Appending PATH env var with : {}".format(bin_path))
        # self.env_info.PATH.append(bin_path)
        # self.cpp_info.names["pkg_config"] = "gcrypt"
        # if self.settings.os in ["Linux", "FreeBSD"]:
        #     self.cpp_info.system_libs = ["pthread"]
