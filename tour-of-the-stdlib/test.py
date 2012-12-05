import doctest

options = doctest.NORMALIZE_WHITESPACE|doctest.REPORT_NDIFF|doctest.ELLIPSIS
doctest.testfile('presentation.txt', optionflags=options)
