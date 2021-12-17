import os

from conans import ConanFile, tools
from conans.errors import ConanInvalidConfiguration

class TensorFlowConan(ConanFile):
    name = "tensorflow"
    description = "TensorFlow is a free and open-source software library for machine learning and artificial intelligence."
    topics = ("tensorflow", "ia", "tensor")
    url = "https://github.com/conan-io/conan-center-index"
    homepage = "https://www.tensorflow.org/"
    license = "Apache-2.0"

    settings = "os", "arch"
    options = {
        "shared": [True, False],
        "gpu": [True, False],
        "avx": [True, False]
    }
    default_options = {
        "shared": True,
        "gpu": False,
        "avx": True
    }

    no_copy_source = True # skip copy to build_folder
    _source_subdir = "_source_subdir"

    @property
    def _tensorflow_url(self):
        hard = "gpu" if self.options.gpu else "cpu"
        os = "darwin" if self.settings.os == "Macos" else str(self.settings.os).lower()
        arch = self.settings.arch
        version = self.version
        ext = "zip" if self.settings.os == "Windows" else "tar.gz"
        return f"https://storage.googleapis.com/tensorflow/libtensorflow/libtensorflow-{hard}-{os}-{arch}-{version}.{ext}"

    def validate(self):
        if self.options.gpu == True and self.options.avx != self.default_options.avx:
            raise ConanInvalidConfiguration("Option 'avx' is not compatible with 'gpu' configurations")
        if self.settings.arch != "x86_64":
            raise ConanInvalidConfiguration("Only available for x86_64 architecture")

    def source(self):
        tools.get(self._tensorflow_url, destination=self._source_subdir)

    def package(self):
        self.copy(pattern="LICENSE", dst="licenses", src=self._source_subdir)
        self.copy(pattern="THIRD_PARTY_TF_C_LICENSES", dst="licenses", src=self._source_subdir)
        self.copy(pattern="include/*", dst=".", src=self._source_subdir)
        self.copy(pattern="lib/*", dst=".", src=self._source_subdir)

    def package_info(self):
        self.env_info.PATH.append(os.path.join(self.package_folder, "lib"))
        self.cpp_info.libs = tools.collect_libs(self)
