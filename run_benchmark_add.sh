#!/bin/bash
#pytest -v smc_benchmark.py::test_party_3_add_50 -v --benchmark-min-rounds=10 --benchmark-save="test_3_50"
#pytest -v smc_benchmark.py::test_party_10_add_50 -v --benchmark-min-rounds=10 --benchmark-save="test_10_50"
#pytest -v smc_benchmark.py::test_party_10_add_100 -v --benchmark-min-rounds=10 --benchmark-save="test_10_100"
#pytest -v smc_benchmark.py::test_party_10_add_500 -v --benchmark-min-rounds=10 --benchmark-save="test_10_500"



# actual test
# increase the number of parties, keep the number of add operations same
#pytest -v smc_benchmark.py::test_actual_party_5_add_50 -v --benchmark-min-rounds=1
#pytest -v smc_benchmark.py::test_actual_party_10_add_50 -v --benchmark-min-rounds=1
#pytest -v smc_benchmark.py::test_actual_party_15_add_50 -v --benchmark-min-rounds=1
#pytest -v smc_benchmark.py::test_actual_party_20_add_50 -v --benchmark-min-rounds=1
#pytest -v smc_benchmark.py::test_actual_party_25_add_50 -v --benchmark-min-rounds=1
#pytest -v smc_benchmark.py::test_actual_party_30_add_50 -v --benchmark-min-rounds=1

# increase the number of parties, keep the number of mul operations same
#pytest -v  smc_benchmark.py::test_actual_party_5_mul_10 -v --benchmark-min-rounds=1
#pytest -v  smc_benchmark.py::test_actual_party_10_mul_10 -v --benchmark-min-rounds=1
#pytest -v  smc_benchmark.py::test_actual_party_15_mul_10 -v --benchmark-min-rounds=1
#pytest -v  smc_benchmark.py::test_actual_party_20_mul_10 -v --benchmark-min-rounds=1
#pytest -v  smc_benchmark.py::test_actual_party_25_mul_10 -v --benchmark-min-rounds=1
#pytest -v  smc_benchmark.py::test_actual_party_30_mul_10 -v --benchmark-min-rounds=1

# increase the number of add operations, keep the number of parties same
#pytest -v  smc_benchmark.py::test_actual_party_5_add_10 -v --benchmark-min-rounds=1
#pytest -v  smc_benchmark.py::test_actual_party_5_add_50 -v --benchmark-min-rounds=1
#pytest -v  smc_benchmark.py::test_actual_party_5_add_100 -v --benchmark-min-rounds=1
#pytest -v  smc_benchmark.py::test_actual_party_5_add_200 -v --benchmark-min-rounds=1
#pytest -v  smc_benchmark.py::test_actual_party_5_add_300 -v --benchmark-min-rounds=1

# increase the number of scalar, keep the number of parties and add operations same (addition of scalars)
#pytest -v  smc_benchmark.py::test_actual_party_5_add_50_scalar_5 -v --benchmark-min-rounds=1
#pytest -v  smc_benchmark.py::test_actual_party_5_add_50_scalar_10 -v --benchmark-min-rounds=1
#pytest -v  smc_benchmark.py::test_actual_party_5_add_50_scalar_50 -v --benchmark-min-rounds=1
#pytest -v  smc_benchmark.py::test_actual_party_5_add_50_scalar_100 -v --benchmark-min-rounds=1
#pytest -v  smc_benchmark.py::test_actual_party_5_add_50_scalar_200 -v --benchmark-min-rounds=1

# increase the number of mul operations, keep the number of parties same
#pytest -v  smc_benchmark.py::test_actual_party_3_mul_2 -v --benchmark-min-rounds=1
#pytest -v  smc_benchmark.py::test_actual_party_3_mul_4 -v --benchmark-min-rounds=1
#pytest -v  smc_benchmark.py::test_actual_party_3_mul_8 -v --benchmark-min-rounds=1
#pytest -v  smc_benchmark.py::test_actual_party_3_mul_16 -v --benchmark-min-rounds=1

# increase the number of scalar, keep the number of parties and mul operations same (addition of scalars)
#pytest -v  smc_benchmark.py::test_actual_party_3_mul_5_scalar_1 -v --benchmark-min-rounds=1
#pytest -v  smc_benchmark.py::test_actual_party_3_mul_5_scalar_3 -v --benchmark-min-rounds=1
#pytest -v  smc_benchmark.py::test_actual_party_3_mul_5_scalar_5 -v --benchmark-min-rounds=1
#pytest -v  smc_benchmark.py::test_actual_party_3_mul_5_scalar_7 -v --benchmark-min-rounds=1

#pytest -v smc_benchmark.py::test_actual_party_5_add_100 -v --benchmark-min-rounds=10
#pytest -v  smc_benchmark.py::test_actual_party_5_mul_10 -v --benchmark-min-rounds=10
pytest -v smc_benchmark.py::test_actual_party_5_add_50_scalar_100 -v --benchmark-min-rounds=10
pytest -v  smc_benchmark.py::test_actual_party_3_mul_5_scalar_3 -v --benchmark-min-rounds=10
