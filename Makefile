doc:
	PYTHONPATH=`pwd` pydoc2.2 dictdlib > dictdlib.txt
	PYTHONPATH=`pwd` pydoc2.2 -w dictdlib

clean:
	-rm -f `find . -name "*~"`
	-rm -f `find . -name "*.pyc"`

changelog:
	cvs2cl
	cvs commit ChangeLog
	rm ChangeLog.bak
