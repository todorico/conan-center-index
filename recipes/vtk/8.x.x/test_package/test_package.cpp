#include <vtkSortDataArray.h>
#include <vtkDoubleArray.h>
#include <vtkIntArray.h>
#include <vtkSmartPointer.h>

int main(int, char *[])
{
    auto valueArray = vtkSmartPointer<vtkDoubleArray>::New();
    {
        valueArray->InsertNextValue(20.0);
        valueArray->InsertNextValue(10.0);
        valueArray->InsertNextValue(30.0);
    }
    auto keyArray = vtkSmartPointer<vtkIntArray>::New();
    {
        keyArray->InsertNextValue(1);
        keyArray->InsertNextValue(0);
        keyArray->InsertNextValue(2);
    }

    std::cout << "Unsorted: " << valueArray->GetValue(0) << " " << valueArray->GetValue(1) << " " << valueArray->GetValue(2) << std::endl;

    auto sortDataArray = vtkSmartPointer<vtkSortDataArray>::New();
    {
        sortDataArray->Sort(keyArray, valueArray);
    }

    std::cout << "Sorted: " << valueArray->GetValue(0) << " " << valueArray->GetValue(1) << " " << valueArray->GetValue(2) << std::endl;

    return EXIT_SUCCESS;
}
