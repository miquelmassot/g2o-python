import io
import os
import os.path
import skbuild
from skbuild import cmaker

# Compiled library is at g2o/lib/g2opy.cpython-310-x86_64-linux-gnu.so


def main():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    cmake_source_dir = "g2o"

    install_requires = [
        'numpy>=1.13.3; python_version<"3.7"',
        'numpy>=1.17.0; python_version>="3.7"',  # https://github.com/numpy/numpy/pull/13725
        'numpy>=1.17.3; python_version>="3.8"',
        'numpy>=1.19.3; python_version>="3.9"',
        'numpy>=1.21.2; python_version>="3.10"',
        'numpy>=1.19.3; python_version>="3.6" and platform_system=="Linux" and platform_machine=="aarch64"',
        'numpy>=1.21.0; python_version<="3.9" and platform_system=="Darwin" and platform_machine=="arm64"',
        'numpy>=1.21.4; python_version>="3.10" and platform_system=="Darwin"',
    ]

    if os.path.exists(".git"):
        import pip._internal.vcs.git as git

        g = git.Git()  # NOTE: pip API's are internal, this has to be refactored
        g.run_command(["submodule", "sync"])
        g.run_command(
            ["submodule", "update", "--init", "--recursive", cmake_source_dir]
        )

    cmake_args = [
        # See g2o/CMakeLists.txt for options and defaults
        "-DBUILD_SHARED_LIBS=OFF",
        "-DG2O_USE_OPENGL=OFF",
        "-DG2O_BUILD_EXAMPLES=OFF",
        "-DG2O_BUILD_APPS=OFF",
        "-DG2O_BUILD_PYTHON=ON",
        "-DCMAKE_POSITION_INDEPENDENT_CODE=ON",
        "-Dg2o_LIBRARY_OUTPUT_DIRECTORY=../setuptools/lib.linux-x86_64-3.10/.",
        "-Dg2o_RUNTIME_OUTPUT_DIRECTORY=./lib",
    ]

    # https://github.com/scikit-build/scikit-build/issues/479
    if "CMAKE_ARGS" in os.environ:
        import shlex

        cmake_args.extend(shlex.split(os.environ["CMAKE_ARGS"]))
        del shlex

    skbuild.setup(
        name="g2o-python",
        version="0.0.1",
        url="https://github.com/miquelmassot/g2o-python",
        license="MIT",
        description="Wrapper package for G2O python bindings.",
        long_description=io.open("README.md", encoding="utf-8").read(),
        long_description_content_type="text/markdown",
        maintainer="Miquel Massot",
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
