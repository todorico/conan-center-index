#include <stdio.h>
#include <tensorflow/c/c_api.h>

int main()
{
    const char* tensorflow_package_version = _package_version;
    const char* tensorflow_runtim_version = TF_Version();

    printf("TensorFlow Package Version: %s\n", tensorflow_package_version);
    printf("TensorFlow Runtime Version: %s\n", tensorflow_runtim_version);

    if (strcmp(tensorflow_package_version, tensorflow_runtim_version) != 0)
    {
        printf("[FAILURE]: TensorFlow Versions are NOT matching");
        return EXIT_FAILURE;
    }

    printf("[SUCCESS]: TensorFlow Versions are matching");
    return EXIT_SUCCESS;
}
