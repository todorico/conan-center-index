#include <iostream>
#include <QCoreApplication>
#include <QDebug>

int versions_should_match(std::string package_version, std::string compile_version, std::string runtime_version)
{
    std::cout << "[TEST] Qt Versions should match: ";

    if (package_version != compile_version || package_version != runtime_version)
    {
        std::cout << "FAILURE\n";
        return EXIT_FAILURE;
    }

    qDebug() << "SUCCESS";
    return EXIT_SUCCESS;
}

int main(int argc, char *argv[])
{
    QCoreApplication app(argc, argv);
    app.setApplicationName("Qt::test_package");

    auto qt_package_version = std::string(_package_version);
    auto qt_compile_version = std::string(QT_VERSION_STR);
    auto qt_runtime_version = std::string(qVersion());

    std::cout << "[INFO] Qt Package Version: " << qt_package_version << '\n';
    std::cout << "[INFO] Qt Compile Version: " << qt_compile_version << '\n';
    std::cout << "[INFO] Qt Runtime Version: " << qt_runtime_version << '\n';

    return versions_should_match(qt_package_version, qt_compile_version, qt_runtime_version);
}
