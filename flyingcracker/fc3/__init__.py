import os
__import__('pkg_resources').declare_namespace(__name__)


VERSION = (0, 3, 0)


def get_version(join=' ', short=False):
    """
    Return the version of this package as a string.

    The version number is built from a ``VERSION`` tuple, which should consist
    of integers, or trailing version information (such as 'alpha', 'beta' or
    'final'). For example:

    >>> VERSION = (2, 0, 6)
    >>> get_version()
    '2.0.6'

    >>> VERSION = (1, 0, 'beta', 2)
    >>> get_version()
    '1.0 beta 2'

    Use the ``join`` argument to join the version elements by an alternate
    character to the default ``' '``. This is useful when building a distutils
    setup module::

        from this_package import get_version

        setup(
            version=get_version(join='-'),
            # ...
        )

    Use the ``short`` argument to get the version number without trailing
    version information.

    """
    version = []
    number = []
    remainder = []
    for i, bit in enumerate(VERSION):
        if isinstance(bit, int):
            number.append(str(bit))
        else:
            remainder = [str(bit) for bit in VERSION[i:]]
            break
    if number:
        version.append('.'.join(number))
    if not short:
        if remainder == ['alpha', 0]:
            version.append('pre-alpha')
        elif 'final' not in remainder:
            version.extend(remainder)
    return join.join(version)


def get_git_tag(join=' ', *args, **kwargs):
    ''' Gets the most recent git tag name and returns it
        with the version number '''
    from subprocess import Popen, PIPE

    loc = os.path.dirname(
        os.path.dirname(
            os.path.realpath(__file__)))

    p = Popen(
        'cd "%s" && git name-rev --name-only HEAD' % loc,
        shell=True,
        stdout=PIPE,
        stderr=PIPE
    )
    branch_name = p.communicate()[0].rstrip()

    if branch_name == '':
        branch_name = None

    p = Popen(
        'cd "%s" && git rev-parse --verify HEAD' % loc,
        shell=True,
        stdout=PIPE,
        stderr=PIPE
    )
    hash = p.communicate()[0].rstrip()
    if len(hash) == 40:
        hash = hash[:10]
    else:
        hash = None

    git_version = '(Git-Version-Not-Found)'

    if branch_name is not None and hash is not None:
        git_version = f'({branch_name.decode("UTF-8")} @{hash.decode("UTF-8")})'

    return join.join([get_version(join=join, *args, **kwargs), git_version])
