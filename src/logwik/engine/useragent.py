from logging import getLogger
from ua_parser import user_agent_parser as ua_parser


logger = getLogger(__name__)


def _get_ua_version(major, minor):
    if major is None:
        return None
    if not isinstance(major, str):
        logger.error(
            'The major component of the User-Agent version in not a string: '
            '"{}"'.format(major)
        )
        return None
    if not major.isnumeric():
        logger.error(
            'The major component of the User-Agent version contains other character'
            ' than numbers: "{}"'.format(major)
        )
        return None
    if minor is None:
        return major
    if not isinstance(minor, str):
        logger.error(
            'The minor component of the User-Agent version in not a string: '
            '"{}"'.format(minor)
        )
        return major
    if not minor.isnumeric():
        logger.error(
            'The minor component of the User-Agent version contains other character'
            ' than numbers: "{}"'.format(major)
        )
        return major
    return '{}.{}'.format(major, minor)


def _get_os_version(major, minor):
    if major is None:
        return None
    if major in ('NT', 'Vista', 'XP'):
        return major
    if minor is None:
        return major
    if not isinstance(minor, str):
        logger.error(
            'The minor component of the OS version in not a string: '
            '"{}"'.format(minor)
        )
        return major
    if not minor.isnumeric():
        logger.error(
            'The minor component of the OS version contains other character'
            ' than numbers: "{}"'.format(major)
        )
        return major
    return '{}.{}'.format(major, minor)


def get_infos(text):
    info = ua_parser.Parse(text)
    ua_version = _get_ua_version(
        info['user_agent']['major'], info['user_agent']['minor']
    )
    os_version = _get_os_version(
        info['os']['major'], info['os']['minor']
    )
    return {
        'user_agent': {
            'name': info['user_agent']['family'],
            'version': ua_version,
        },
        'os': {
            'name': info['os']['family'],
            'version': os_version,
        },
        'device': info['device']['family']
    }
