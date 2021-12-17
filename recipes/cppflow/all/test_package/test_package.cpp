#include <iostream>
#include <cppflow/cppflow.h>

bool is_calculation_correct(float v1, float v2, float v3)
{
    cppflow::tensor t1(v1), t2(v2), t3(v3);

    float target = (v1 + v2) * v3;
    auto result = (t1 + t2) * t3;
    auto result_value = result.get_data<float>()[0];

    return std::abs(target / result_value - 1.0f) < 1e-6;
}

int main(int argc, char *argv[])
{
    if(!is_calculation_correct(3, 10, 100))
    {
        std::cout << "[FAILURE]: CppFlow performed an INCORRECT calculation\n";
        return EXIT_FAILURE;
    }

    std::cout << "[SUCCESS]: CppFlow performed a correct calculation\n";
    return EXIT_SUCCESS;
}
