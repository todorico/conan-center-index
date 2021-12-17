from conans import ConanFile, tools

class CppFlowConan(ConanFile):
    name = "cppflow"
    version = "2.0"
    description = "Run TensorFlow models in C++ without Bazel, without TensorFlow installation and without compiling Tensorflow."
    topics = ("tensorflow", "ia")
    url = "https://github.com/conan-io/conan-center-index"
    homepage = "https://github.com/serizba/cppflow"
    license = "MIT"

    # No settings/options are necessary, this is header only

    requires = "tensorflow/2.6.0@sim-and-cure/stable"

    no_copy_source = True # skip copy to build_folder
    _source_subdir = "_source_subdir"

    def source(self):
        git = tools.Git(self._source_subdir)
        git.clone("https://github.com/serizba/cppflow.git", branch="master", shallow=True)

    def package(self):
        self.copy(pattern="LICENSE", dst="licenses", src=self._source_subdir)
        self.copy(pattern="include/*", dst=".", src=self._source_subdir)

    def package_id(self):
        self.info.header_only()
