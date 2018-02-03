# Nyctea

(pron. nis-tee-ah) <br>
An input generation platform for testing distributed protocols.

# Installation

```
python setup.py
```

# QA
Run the quality assurance tests to make sure nyctea works on your system.
<br>
To run tests in bulk, use the following command sequence :
```
cd qa/
python unittests_driver.py
```
To run tests individually, use commands of the format :
```
python -m unittest Test_nyctea.Test_nyctea.test_nyctea_example_1

