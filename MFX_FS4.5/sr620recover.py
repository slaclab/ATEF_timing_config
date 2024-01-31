from epics import caget, caput, cainfo


#caput("",)
caput("LAS:FS45:CNT:TI:A:SetTrigSlope",0)
caput("LAS:FS45:CNT:TI:B:SetTrigSlope",0)
caput("LAS:FS45:CNT:TI:EXT:GetInputTerm",0)
caput("LAS:FS45:CNT:TI:GetArmMode",0)
caput("LAS:FS45:CNT:TI:GetNumScanPoints",0)
caput("LAS:FS45:CNT:TI:GetRefLvlAmp",0)
caput("LAS:FS45:CNT:TI:A:GetTrigSlope",0)
caput("LAS:FS45:CNT:TI:B:GetTrigSlope",0)
caput("LAS:FS45:CNT:TI:GetAutoMeasMode",0)
caput("LAS:FS45:CNT:TI:GetGraphEnable",0)
caput("LAS:FS45:CNT:TI:GetClockSource",0)


print(caget("LAS:FS45:CNT:TI:A:SetTrigSlope"))
print(caget("LAS:FS45:CNT:TI:B:SetTrigSlope"))
print(caget("LAS:FS45:CNT:TI:EXT:GetInputTerm"))
print(caget("LAS:FS45:CNT:TI:GetArmMode"))
print(caget("LAS:FS45:CNT:TI:GetNumScanPoints"))
print(caget("LAS:FS45:CNT:TI:GetRefLvlAmp"))
print(caget("LAS:FS45:CNT:TI:A:GetTrigSlope"))
print(caget("LAS:FS45:CNT:TI:B:GetTrigSlope"))
print(caget("LAS:FS45:CNT:TI:GetAutoMeasMode"))
print(caget("LAS:FS45:CNT:TI:GetGraphEnable"))
print(caget("LAS:FS45:CNT:TI:GetClockSource"))
#caget("LAS:FS45:CNT:TI:A:SetTrigSlope")







