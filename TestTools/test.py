# -*- coding:utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import demjson

data1 = {
	"VisitId": "927f2bb2-5b3d-e811-8d9e-000c2918a2b6",
	"ClinicalDiagnosis": "33333"
}

data = {
	"VisitId": "927f2bb2-5b3d-e811-8d9e-000c2918a2b6",
	"ClinicalDiagnosis": "33333",
	"InspectionFromItems": [{
		"InspectionGroupId": "c504b05c-902e-e811-8d9e-000c2918a2b6",
		"ItemName": "骨科组套1",
		"GroupName": "骨科组套1",
		"Quantity": 1
	}, {
		"InspectionGroupId": "039c86f6-f332-e811-8d9e-000c2918a2b6",
		"ItemName": "检验租套测试test1",
		"GroupName": "检验租套测试test1",
		"Quantity": 1
	}]
}

print "bianma:%s" % sys.getdefaultencoding()
print "type:%s" % type(data)
print data
print "******************************111111"
print data1
print demjson.decode(data)
print demjson.decode(data1)