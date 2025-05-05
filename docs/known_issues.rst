=================
Known Issues
=================

This section lists known issues and limitations of OpsParser, along with possible solutions.

Compatibility Issues
-------------------

* **OpenSees Version Compatibility**: OpsParser is developed with reference to version 3.7.1.2. Older versions may have different command formats. Please submit an issue if you encounter compatibility problems.
* **Python Version**: Python 3.12 or higher is recommended, as lower versions may experience compatibility issues with OpenSeesPy.

Functional Limitations
---------------------

1. **Command Capture Limitations**: Some specific OpenSees commands may not be correctly captured and recorded (or may be recorded repeatedly).
2. **Complex Models**: Performance may be affected when working with very complex models.

Common Errors and Solutions
--------------------------

1. **ImportError**

   .. code-block:: python
   
       ImportError: No module named 'opsparser'
   
   Solution: Ensure OpsParser is properly installed and its installation path is added to the Python path.

2. **Version Mismatch Warning**

   When OpsParser is incompatible with your OpenSeesPy version, a warning may not appear.
   
   Solution: Update to compatible versions or check the documentation for guidance on specific version combinations.

Reporting Issues
---------------

If you encounter issues not listed here, please report them through:

1. Submitting an issue on GitHub: [GitHub Issues Link]
2. Providing detailed error information and reproduction steps
3. If possible, including a minimal example code that demonstrates the issue

Contributing Fixes
----------------

We welcome community contributions to fix known issues. If you're interested in contributing code:

1. Fork the repository
2. Create a fix branch (we recommend using uv as the package manager)
3. Submit a Pull Request with a description of your fix
