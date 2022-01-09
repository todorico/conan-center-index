// STL
#include <iostream>

// VTK
#include <vtkSmartPointer.h>

// ACVD
#include <vtkSurface.h>

void test(std::string description, bool check)
{
    std::cout << "[TEST] " << description << ": ";
    if (!check)
    {
        std::cout << "FAILURE\n";
        exit(EXIT_FAILURE);
    }
    std::cout << "SUCCESS\n";
}

int main(int argc, char *argv[])
{
    double x[7][3] = {{0, 0, 1}, {0.707, 0.707, 0}, {0.707, -0.707, 0}, {-0.707, -0.707, 0}, {-0.707, 0.707, 0}, {0, 0, -1}, {0, 0, 2}};
    int pts[12][3] = {{0, 1, 2}, {0, 2, 3}, {0, 3, 4}, {0, 4, 1}, {5, 1, 2}, {5, 2, 3}, {5, 3, 4}, {5, 4, 1}, {6, 1, 2}, {6, 2, 3}, {6, 3, 4}, {6, 4, 1}};

    auto surface = vtkSmartPointer<vtkSurface>::New();

    for (int i = 0; i < 7; i++)
        surface->AddVertex(x[i]);

    test("Number of points should be 7", surface->GetNumberOfPoints() == 7);

    for (int i = 0; i < 8; i++)
        surface->AddFace(pts[i][0], pts[i][1], pts[i][2]);

    test("Number of faces  should be 8", surface->GetNumberOfCells() == 8);

    return EXIT_SUCCESS;
}
