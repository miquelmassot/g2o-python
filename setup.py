import io
import os
import os.path
import skbuild
from skbuild import cmaker


def main():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    cmake_source_dir = "g2o"

    install_requires = [
        'numpy',
        'scikit-build',
    ]

    # Fix g2o/python/CMakeLists.txt file, install pybind11 to "."
    with open(os.path.join(cmake_source_dir, "python/CMakeLists.txt"), "r") as file:
        filedata = file.read()
        filedata = filedata.replace(
            "install(TARGETS g2opy LIBRARY DESTINATION g2opy)",
            "install(TARGETS g2opy LIBRARY DESTINATION .)"
        )
    with open(os.path.join(cmake_source_dir, "python/CMakeLists.txt"), "w") as file:
        file.write(filedata)

    # Fix g2o/CMakeLists.txt file, remove the lines
    #   set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${g2o_LIBRARY_OUTPUT_DIRECTORY})
    #   set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${g2o_LIBRARY_OUTPUT_DIRECTORY})
    #   set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${g2o_RUNTIME_OUTPUT_DIRECTORY})
    with open(os.path.join(cmake_source_dir, "CMakeLists.txt"), "r") as file:
        filedata = file.read()
        filedata = filedata.replace(
            "set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${g2o_LIBRARY_OUTPUT_DIRECTORY})",
            "",
        )
        filedata = filedata.replace(
            "set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${g2o_LIBRARY_OUTPUT_DIRECTORY})",
            "",
        )
        filedata = filedata.replace(
            "set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${g2o_RUNTIME_OUTPUT_DIRECTORY})",
            "",
        )
    with open(os.path.join(cmake_source_dir, "CMakeLists.txt"), "w") as file:
        file.write(filedata)

    # Add __init__.py at g2o root folder to be able to write in python:
    #   import g2o
    with open(os.path.join(cmake_source_dir, "__init__.py"), "w") as file:
        file.write("from .g2opy import *  # noqa: F401")

    cmake_args = [
        # See g2o/CMakeLists.txt for options and defaults
        "-DBUILD_SHARED_LIBS=OFF",
        "-DG2O_USE_OPENGL=OFF",
        "-DG2O_BUILD_EXAMPLES=OFF",
        "-DG2O_BUILD_APPS=OFF",
        "-DG2O_BUILD_PYTHON=ON",
        "-DCMAKE_POSITION_INDEPENDENT_CODE=ON",
    ]

    # https://github.com/scikit-build/scikit-build/issues/479
    if "CMAKE_ARGS" in os.environ:
        import shlex

        cmake_args.extend(shlex.split(os.environ["CMAKE_ARGS"]))
        del shlex

    skbuild.setup(
        name="g2o-python",
        version="0.0.9",
        url="https://github.com/miquelmassot/g2o-python",
        license="MIT",
        description="Wrapper package for G2O python bindings.",
        long_description=io.open("README.md", encoding="utf-8").read(),
        long_description_content_type="text/markdown",
        maintainer="Miquel Massot",
        packages=["g2o"],
        ext_modules=EmptyListWithLength(),
        install_requires=install_requires,
        python_requires=">=3.6",
        classifiers=[
            "Development Status :: 5 - Production/Stable",
            "Environment :: Console",
            "Intended Audience :: Developers",
            "Intended Audience :: Education",
            "Intended Audience :: Information Technology",
            "Intended Audience :: Science/Research",
            "License :: OSI Approved :: MIT License",
            "Operating System :: MacOS",
            "Operating System :: Microsoft :: Windows",
            "Operating System :: POSIX",
            "Operating System :: Unix",
            "Programming Language :: Python",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3 :: Only",
            "Programming Language :: Python :: 3.6",
            "Programming Language :: Python :: 3.7",
            "Programming Language :: Python :: 3.8",
            "Programming Language :: Python :: 3.9",
            "Programming Language :: Python :: 3.10",
            "Programming Language :: C++",
            "Programming Language :: Python :: Implementation :: CPython",
            "Topic :: Scientific/Engineering",
            "Topic :: Software Development",
        ],
        cmake_args=cmake_args,
        cmake_source_dir=cmake_source_dir,
    )


# This creates a list which is empty but returns a length of 1.
# Should make the wheel a binary distribution and platlib compliant.
class EmptyListWithLength(list):
    def __len__(self):
        return 1


if __name__ == "__main__":
    main()
