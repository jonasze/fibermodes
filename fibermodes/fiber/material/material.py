"""Module for fiber materials.

A material gives a refractive index, as function of the wavelength.

"""

import warnings


class OutOfRangeWarning(UserWarning):

    """Warning raised when a material parameter is out of the allowed range.

    If this warning is raised, it means that results are possibily
    innacurate.

    """
    pass


class Material(object):

    """Material abstract class.

    This gives the interface for the different materials, as well as
    some common functions. All methods in that class are class methods.

    """

    name = "Abstract Material"  # English name for the mateial
    nparams = 0  # Number of material parameters
    info = None  # Info about the material
    url = None  # URL for the reference about the material
    WLRANGE = None  # Acceptable range for the wavelength

    @classmethod
    def _testRange(cls, wl):
        if cls.WLRANGE is None:
            return
        if cls.WLRANGE[0] <= wl <= cls.WLRANGE[1]:
            return

        msg = ("Wavelength {} out of supported range for material {}. "
               "Wavelength should be in the range {} - {}. "
               "Results could be innacurate.").format(
            str(wl),
            cls.name,
            cls.WLRANGE[0],
            cls.WLRANGE[1])
        warnings.warn(msg, OutOfRangeWarning)

    @classmethod
    def n(cls, wl, *args, **kwargs):
        raise NotImplementedError(
            "This method must be implemented in derived class.")

    @classmethod
    def str(cls, *args):
        return cls.name

    @classmethod
    def __str__(cls):
        return cls.name

    @classmethod
    def __repr__(cls):
        return "{}()".format(cls.__name__)


if __name__ == '__main__':
    m = Material()
    print(m)
    print(repr(m))
