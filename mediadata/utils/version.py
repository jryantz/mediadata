"""
A set of utilities for getting the current version of the application 
in various formats.
"""


def get_version(version=None) -> str:
    """
    Return the complete semantic versioning compliant version.
    """

    version = get_complete_version(version)

    # Build the user presented version as two parts.
    main = get_main_version(version)
    sub = get_sub_version(version)

    return "-".join([main, sub])


def get_complete_version(version=None) -> tuple:
    """
    Return a tuple of the mediadata version.
    Check for the correctness of the tuple provided.
    """

    if version is None:
        from mediadata import VERSION as version
    else:
        assert len(version) == 5
        assert version[3] in ("alpha", "beta", "rc", "final")

    return version


def get_main_version(version=None):
    """
    Return the main version (X.Y.Z) from VERSION.
    """

    version = get_complete_version(version)
    return ".".join(str(x) for x in version[:3])


def get_sub_version(version=None):
    """
    Return the sub version ([-release{.N}])
    """

    sub = ""
    if version[3] != "final":
        sub = version[3]

        if version[4] > 0:
            sub = ".".join(str(x) for x in version[3:])

    return sub
