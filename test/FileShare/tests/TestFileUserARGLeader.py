# $Id: TestFileUserARGLeader.py 1047 2009-01-15 14:48:58Z graham $
#
# Unit testing for FileUserARGLeader module
#

import os
import sys
import httplib
import urllib2
import unittest
import subprocess

sys.path.append("../..")

from TestConfig import TestConfig

# Initialize authenticated HTTP connection opener

class TestFileUserARGLeader(unittest.TestCase):

    def do_HTTP_redirect(self, opener, method, uri, data, content_type):
        req=urllib2.Request(uri, data=data)
        if content_type: req.add_header('Content-Type', content_type)
        req.get_method = lambda: method
        try:
            url=opener.open(req)
        except urllib2.HTTPError as e:
            if e.code == 301:                # Follow redirection
                req=urllib2.Request( e.headers['Location'], data=data)
                if content_type: req.add_header('Content-Type', content_type)
                req.get_method = lambda: method
                url=opener.open(req)
            else:
                raise e     # propagate exception
        return

    def setUp(self):
        mountcommand = ( 'mount.cifs //%(host)s/%(share)s/%(userA)s %(mountpt)s -o rw,user=%(user)s,password=%(pass)s,nounix,forcedirectio' %
                         { 'host': TestConfig.hostname
                         , 'share': TestConfig.cifssharename
                         , 'userA': TestConfig.userAname
                         , 'user': TestConfig.userRGleadername
                         , 'mountpt': TestConfig.cifsmountpoint
                         , 'pass': TestConfig.userRGleaderpass
                         } )
        status=os.system(mountcommand)

        self.assertEqual(status, 0, 'CIFS Mount failure')
        return

    def tearDown(self):
        os.system('umount.cifs '+TestConfig.cifsmountpoint)
        return

    # Test cases
    def testNull(self):
        assert (True), "True expected"
        return

    def testReadMeSSH(self):
        f=os.system(ssh_string)
        print f        
        return
        
    def testReadMeCIFS(self):
        # Test assumes ADMIRAL shared file system is mounted at mountpoint
        # Open README file
        f = open(TestConfig.cifsmountpoint+'/'+TestConfig.readmefile)
        assert (f), "README file open failed (CIFS)"
        # Read first line
        l = f.readline()
        # Close file
        f.close()
        # Check first line
        self.assertEqual(l, TestConfig.readmetext, 'Unexpected README content')
        return

    def testCreateFileCIFS(self):
        f=None
        try:
            f = open(TestConfig.cifsmountpoint+'/testCreateFile.tmp','w+')
        except:
            pass
        assert (f==None), "Research Group leader can create files in User A's filespace!"
        return

    def testUpdateFileCIFS(self):
        f=None
        try: 
            f = open(TestConfig.cifsmountpoint+'/'+TestConfig.readmefile,'w+')
        except:
            pass
        assert (f==None), "Research Group leader can open User A's files for writing!"
        return

    def testDeleteFileCIFS(self):
        filename1 = TestConfig.cifsmountpoint+'/testCreateFile.tmp'
        # Test and delete first file
        try:
            s = os.stat(filename1)
        except:
            assert (False), "File "+filename1+" not found or other stat error"
        os.remove(filename1)
        try:
            s = os.stat(filename1)
            assert (False), "File "+filename1+" not deleted"
        except:
            pass
        return

    def testReadMeDAVfs(self):
        # Test assumes ADMIRAL shared file system is mounted at mountpoint
        # Open README file
        status=os.system('mount '+TestConfig.webdavmountpoint)
        self.assertEqual(status, 0, 'DAVfs Mount failure')
        f = open(TestConfig.webdavmountpoint+'/'+TestConfig.readmefile)
        assert (f), "README file open failed (DAVfs)"
        # Read first line
        l = f.readline()
        # Close file
        f.close()
        # Check first line
        self.assertEqual(l, TestConfig.readmetext, 'Unexpected README content')
        os.system('umount '+TestConfig.webdavmountpoint)
        return

    def testCreateFileDAVfs(self):
        status=os.system('mount '+TestConfig.webdavmountpoint)
        self.assertEqual(status, 0, 'DAVfs Mount failure')
        f = open(TestConfig.webdavmountpoint+'/testCreateWebDAVFile.tmp','w+')
        assert (f), "File creation failed"
        f.write('Test creation of file\n')
        f.close()
        f = open(TestConfig.webdavmountpoint+'/testCreateWebDAVFile.tmp','r')
        l = f.readline()
        f.close()
        self.assertEqual(l, 'Test creation of file\n', 'Unexpected file content') 
        os.system('umount '+TestConfig.webdavmountpoint)
        return

    def testUpdateFileDAVfs(self):
        status=os.system('mount '+TestConfig.webdavmountpoint)
        self.assertEqual(status, 0, 'DAVfs Mount failure')
        filename = TestConfig.webdavmountpoint+'/testUpdateWebDAVFile.tmp'
        f = open(filename,'w+')
        assert (f), "File creation failed"
        f.write('Test creation of file\n')
        f.close()
        f = open(filename,'a+')
        f.write('Test update of file\n')
        f.close()
        f = open(filename,'r')
        l1 = f.readline()
        l2 = f.readline()
        f.close()
        self.assertEqual(l1, 'Test creation of file\n', 'Unexpected file content: l1') 
        self.assertEqual(l2, 'Test update of file\n', 'Unexpected file content: l2') 
        os.system('umount '+TestConfig.webdavmountpoint)
        return

    def testDeleteFileDAVfs(self):
        status=os.system('mount '+TestConfig.webdavmountpoint)
        self.assertEqual(status, 0, 'DAVfs Mount failure')
        filename1 = TestConfig.webdavmountpoint+'/testCreateWebDAVFile.tmp'
        filename2 = TestConfig.webdavmountpoint+'/testUpdateWebDAVFile.tmp'
        # Test and delete first file
        try:
            s = os.stat(filename1)
        except:
            assert (False), "File "+filename1+" not found or other stat error"
        os.remove(filename1)
        try:
            s = os.stat(filename1)
            assert (False), "File "+filename1+" not deleted"
        except:
            pass
        # Test and delete second file
        try:
            s = os.stat(filename2)
        except:
            assert (False), "File "+filename2+" not found or other stat error"
        os.remove(filename2)
        try:
            s = os.stat(filename2)
            assert (False), "File "+filename2+" not deleted"
        except:
            pass
        os.system('umount '+TestConfig.webdavmountpoint)
        return


    def testReadMeHTTP(self):
        passman = urllib2.HTTPPasswordMgrWithDefaultRealm()
        passman.add_password(None, TestConfig.webdavbaseurl, TestConfig.userRGleadername, TestConfig.userRGleaderpass)
        authhandler = urllib2.HTTPBasicAuthHandler(passman)
        opener = urllib2.build_opener(authhandler)
        urllib2.install_opener(opener)
        pagehandle = urllib2.urlopen(TestConfig.webdavbaseurl+'/'+TestConfig.userAname+'/'+TestConfig.readmefile)
        thepage = pagehandle.read()
        self.assertEqual(thepage, TestConfig.readmetext) 
        return

    def testCreateFileHTTP(self):
        passman = urllib2.HTTPPasswordMgrWithDefaultRealm()
        passman.add_password(None, TestConfig.webdavbaseurl, TestConfig.userRGleadername, TestConfig.userRGleaderpass)
        authhandler = urllib2.HTTPBasicAuthHandler(passman)
        opener = urllib2.build_opener(authhandler)
        urllib2.install_opener(opener)
        disallowed=False
        createstring="Testing file creation with HTTP"
        try:
            # Write data to server
            self.do_HTTP_redirect(opener, "PUT",
                TestConfig.webdavbaseurl+'/'+TestConfig.userAname+'/TestHTTPCreate.tmp', 
                createstring, 'text/plain')
        except urllib2.HTTPError as e:
            self.assertEqual(e.code, 401, "Operation should be 401 (auth failed), was: "+str(e))
            disallowed=True
        assert disallowed, "Research Group leader can create a file in User A's filespace by HTTP!"
        return

    def testUpdateFileHTTP(self):
        passman = urllib2.HTTPPasswordMgrWithDefaultRealm()
        passman.add_password(None, TestConfig.webdavbaseurl, TestConfig.userRGleadername, TestConfig.userRGleaderpass)
        authhandler = urllib2.HTTPBasicAuthHandler(passman)
        opener = urllib2.build_opener(authhandler)
        urllib2.install_opener(opener)
        disallowed=False
        modifystring="Testing file modification with HTTP"
        try:
            # Write data to server
            self.do_HTTP_redirect(opener, "PUT",
                TestConfig.webdavbaseurl+'/'+TestConfig.userAname+'/TestHTTPUpdate.tmp', 
                modifystring, 'text/plain')
        except urllib2.HTTPError as e:
            self.assertEqual(e.code, 401, "Operation should be 401 (auth failed), was: "+str(e))
            disallowed=True
        assert disallowed, "Research Group leader can update User A's file by HTTP!"
        return

    def testDeleteFileHTTP(self):
        passman = urllib2.HTTPPasswordMgrWithDefaultRealm()
        passman.add_password(None, TestConfig.webdavbaseurl, TestConfig.userRGleadername, TestConfig.userRGleaderpass)
        authhandler = urllib2.HTTPBasicAuthHandler(passman)
        opener = urllib2.build_opener(authhandler)
        urllib2.install_opener(opener)
        disallowed = False
        try:
            # Write data to server
            self.do_HTTP_redirect(opener, "DELETE",
                TestConfig.webdavbaseurl+'/'+TestConfig.userAname+'/TestHTTPDelete.tmp', 
                None, None)
        except urllib2.HTTPError as e:
            self.assertEqual(e.code, 401, "Operation should be 401 (auth failed), was: "+str(e))
            disallowed = True
        assert disallowed, "User B can delete User A's file by HTTP!"
        return

    # Sentinel/placeholder tests

    def testUnits(self):
        assert (True)

    def testComponents(self):
        assert (True)

    def testIntegration(self):
        assert (True)

    def testPending(self):
        assert (False), "No pending test"

# Assemble test suite

from MiscLib import TestUtils

def getTestSuite(select="unit"):
    """
    Get test suite

    select  is one of the following:
            "unit"      return suite of unit tests only
            "component" return suite of unit and component tests
            "all"       return suite of unit, component and integration tests
            "pending"   return suite of pending tests
            name        a single named test to be run
    """
    testdict = {
        "unit": 
            [ "testUnits"
            , "testNull"
            ],
        "component":
            [ "testComponents"
            , "testReadMeCIFS"
            , "testReadMeHTTP"
            , "testCreateFileCIFS"
            , "testCreateFileHTTP"
            , "testUpdateFileCIFS"
            , "testUpdateFileHTTP"
            , "testDeleteFileHTTP"
            ],
        "integration":
            [ "testIntegration"
            ],
        "pending":
            [ "testPending"
            , "testReadMeSSH"
            , "testReadMeDAVfs"
            , "testCreateFileDAVfs"
            , "testUpdateFileDAVfs"
            , "testDeleteFileDAVfs"
            , "testDeleteFileCIFS"
            ]
        }
    return TestUtils.getTestSuite(TestFileUserARGLeader, testdict, select=select)

# Run unit tests directly from command line
if __name__ == "__main__":
    TestUtils.runTests("TestFileUserARGLeader", getTestSuite, sys.argv)

# End.


