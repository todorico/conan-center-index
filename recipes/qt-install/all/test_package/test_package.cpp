#include <iostream>
#include <QCoreApplication>
#include <QDebug>

int main(int argc, char *argv[])
{
    QCoreApplication app(argc, argv);

    auto qt_package_version = std::string(_package_version);
    auto qt_compile_version = std::string(QT_VERSION_STR);
    auto qt_runtime_version = std::string(qVersion());

    std::cout << "Qt Package Version: " << qt_package_version << '\n';
    std::cout << "Qt Compile Version: " << qt_compile_version << '\n';
    std::cout << "Qt Runtime Version: " << qt_runtime_version << '\n';

    if (qt_package_version != qt_compile_version || qt_package_version != qt_runtime_version)
    {
        qDebug() << "[FAILURE]: Qt Versions are NOT matching";
        return EXIT_FAILURE;
    }

    qDebug() << "[SUCCESS]: Qt Versions are matching";
    return EXIT_SUCCESS;
}
