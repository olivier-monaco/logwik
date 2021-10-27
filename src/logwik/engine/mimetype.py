from logging import getLogger

logger = getLogger(__name__)

_MAPPING = {
    'application/annodex': 'video',
    'application/atom+xml': 'document',
    'application/dat': 'other',
    'application/data': 'other',
    'application/epub+zip': 'document',
    'application/excel': 'document',
    'application/font-woff': 'font',
    'application/font-woff2': 'font',
    'application/force-download': 'other',
    'application/java-archive': 'application',
    'application/javascript': 'javascript',
    'application/json': 'javascript',
    'application/mp4': 'video',
    'application/mspowerpoint': 'document',
    'application/msword': 'document',
    'application/octet-stream': 'other',
    'application/opensearchdescription+xml': 'other',
    'application/ogg': 'video',
    'application/pdf': 'document',
    'application/postscript': 'document',
    'application/powerpoint': 'document',
    'application/rar': 'archive',
    'application/rss+xml': 'document',
    'application/rtf': 'document',
    'application/vnd.amazon.ebook': 'document',
    'application/vnd.android.package-archive': 'application',
    'application/vnd.apple.installer+xml': 'application',
    'application/vnd.google-earth.kml+xml': 'other',
    'application/vnd.microsoft.portable-executable': 'application',
    'application/vnd.ms-excel.addin.macroEnabled.12': 'document',
    'application/vnd.ms-excel.sheet.binary.macroEnabled.12': 'document',
    'application/vnd.ms-excel.sheet.macroEnabled.12': 'document',
    'application/vnd.ms-excel.template.macroEnabled.12': 'document',
    'application/vnd.ms-excel': 'document',
    'application/vnd.ms-fontobject': 'font',
    'application/vnd.ms-powerpoint.presentation.macroEnabled.12': 'document',
    'application/vnd.ms-powerpoint.slideshow.macroEnabled.12': 'document',
    'application/vnd.ms-powerpoint.template.macroEnabled.12': 'document',
    'application/vnd.ms-powerpoint': 'document',
    'application/vnd.ms-word.document.macroEnabled.12': 'document',
    'application/vnd.oasis.opendocument.presentation': 'document',
    'application/vnd.oasis.opendocument.spreadsheet': 'document',
    'application/vnd.oasis.opendocument.text': 'document',
    'application/vnd.openxmlformats-officedocument.presentationml.presentation': 'document',
    'application/vnd.openxmlformats-officedocument.presentationml.slideshow': 'document',
    'application/vnd.openxmlformats-officedocument.presentationml.template': 'document',
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': 'document',
    'application/vnd.openxmlformats-officedocument.spreadsheetml.template': 'document',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document': 'document',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.template': 'document',
    'application/vnd.rn-realmedia': 'video',
    'application/vnd.visio': 'video',
    'application/x-7z-compressed': 'archive',
    'application/x-abiword': 'document',
    'application/x-bzip': 'archive',
    'application/x-bzip2': 'archive',
    'application/x-download': 'other',
    'application/x-excel': 'document',
    'application/x-font-otf': 'font',
    'application/x-font-ttf': 'font',
    'application/x-font-woff': 'font',
    'application/x-gzip': 'archive',
    'application/x-javascript': 'javascript',
    'application/x-matroska': 'video',
    'application/x-msexcel': 'document',
    'application/x-mspowerpoint': 'document',
    'application/x-pkcs7-crl': 'other',
    'application/x-rar-compressed': 'archive',
    'application/x-shockwave-flash': 'application',
    'application/x-silverlight-app': 'application',
    'application/x-tar': 'archive',
    'application/xhtml+xml': 'page',
    'application/xml': 'document',
    'application/xslt+xml': 'other',
    'application/zip': 'archive',
    'httpd/unix-directory': 'other',
    'multipart/byteranges': 'other',
    'text/calendar': 'document',
    'text/css': 'css',
    'text/csv': 'document',
    'text/html': 'page',
    'text/javascript': 'javascript',
    'text/json': 'javascript',
    'text/markdown': 'page',
    'text/plain': 'page',
    'text/rtf': 'document',
    'text/xml': 'document',
    'text/x-component': 'other',
}

def get_category(mimetype):
    if mimetype == '-':
        return None
    if mimetype.startswith('audio/'):
        return 'audio'
    if mimetype.startswith('image/'):
        return 'image'
    if mimetype.startswith('video/'):
        return 'video'
    if mimetype.startswith('font/'):
        return 'font'
    mimetype = mimetype.split(';')[0]
    if mimetype in _MAPPING:
        return _MAPPING[mimetype]
    logger.warn('Unknow MIME type "{}"'.format(mimetype))
    return 'other'
