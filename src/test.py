import logging, re, datetime, sys, traceback, os, shutil


from romdb import tvparser2 as tvparser
from romdb.romlog import *

_TEST_SOURCE = '/home/steini/tvtesttree'
_TEST_DEST = '/home/steini/tvtestdest'

def non_destructive_test():

    scanner = tvparser.TVParser(_TEST_SOURCE)
    try:
        scanner.scan_source()
    except:
        pass

    test_log.info(
        '\n--------------------------\n%s - Start of new test.\n------------------\n' % datetime.datetime.now()
        )
    test_log.info('\nPROPER EPS\n\n')
    [test_log.info('%s\n'%ep) for ep in scanner.parsed_eps]
    test_log.info( '\n\nUNPARSABLE EPS\n')
    [test_log.info('%s\n'%ep) for ep in scanner.unparsed_eps]
    test_log.info('\n\nSINGLE EP DIRS\n')
    [test_log.info('%s\n'%ep) for ep in scanner.single_ep_dirs]

    test_log.info('Number of parsed_eps = %d' % len(scanner.parsed_eps))
    test_log.info('Number of unparseable_eps = %d' % len(scanner.unparsed_eps))
    test_log.info('Number of single_ep_dirs = %d' % len(scanner.single_ep_dirs))
    return scanner


def destructive_test():
    '''
    Parses test tv folder and sorts episodes into the target tv directory.\n
    Does not delete anything. Files are copied.
    '''
    non_destructive_test()    
    scanner = tvparser.TVParser(_TEST_SOURCE)
    scanner.scan_source()
    for ep in scanner.parsed_eps:
        path = os.path.join(_TEST_DEST, ep['series_name'], 's'+str(ep['season_num']))
        try:
            os.makedirs(path)
        except OSError:
            test_log.warning('Folder exists, \'%s\'.' % path)
        rseries = ep['series_name'].replace(' ', '.')
        rseason = str(ep['season_num'])
        rep = str(ep['ep_num'])
        rextraep = ''
        if ep['extra_ep_num']:
            rextraep = 'e'+str(ep['extra_ep_num'])
        rrelgroup = ep['release_group']
        if rrelgroup: rrelgroup = '-'+rrelgroup
        else: rrelgroup = ''
        extension = os.path.splitext(ep.path)[1]


        if len(rep)==1:rep='0'+rep
        if len(rextraep)==1:rextraep='0'+rep
        if len(rseason)==1:rseason='0'+rseason
            
        result_file = ('%(series_name)s.s%(season_num)se%(ep_num)s%(extra_ep)s%(release_group)s%(extension)s' %
        {'series_name': rseries, 'season_num':rseason, 'ep_num':rep, 'extra_ep':rextraep, 'release_group':rrelgroup,'extension':extension})
        result_file = os.path.join(path, result_file)
        shutil.copyfile(ep.path, result_file)


def regex_test():    
    testcases = [
        'series name season 1',
        'series.name.s01e02.some.shit',
        'episode 1',
        'season 1 episode 2',
        'season 2',
        'series name season 1 episode 2'
        ]
    for case in testcases:
        match = None
        for regex in tv_regexes:
            match = re.match(regex.pattern, case)
            if match: break
        if match:
            test_log.info('SUCCESS: case [%s] matched pattern [%s]' % (case, regex.pattern))
        else:
            test_log.info('FAILURE: case [%s] did not match anything' % (case))


def my_excepthook(etype, value, tback):
    print 'this is the cool excepthook'
    #sys.__excepthook__(etype, value, tback)
    s = ''.join(traceback.format_exception(etype, value, tback))
    print 'UNEFINED EXCEPTION OCCURED:\n\n%s\n' % (s,)

if __name__ == "__main__":
    sys.excepthook = my_excepthook
    rom_log.setLevel(logging.DEBUG)
    test_log.setLevel(logging.DEBUG)
    #non_destructive_test()
    destructive_test()
