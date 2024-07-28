'''
Created on Feb 14, 2017
Update on Dec 11, 2020
Update on Feb 28, 2022

@author: felix.yao
@update: luke.pan
@update: Mark.Kan -- update to fit the requirement of  MRA4 samples
'''

bank0 =     {   0x0 :   "Enumerate",
                0x1 :   "Initialise",
                0x2 :   "SetMTPLockKey",
                0x3 :   "SetThVolt",
                0x4 :   "SetThTemp",
                0x5 :   "SetGPIO_ConfDly",
                0x6 :   "SetZMCurr",
                0x7 :   "SetZMFreq",
                0x8 :   "SetBalCurr",
                0x9 :   "SetBalVolt",
                0xA :   "SetSRMask",
                0xB :   "SetMode",
                0xC :   "SetForceErr",
                0xD :   "GetStatus",
                0xE :   "GetData",
                0xF :   "SetRegBank"               
                }

register = {    "Enumerate"     :   0x00,
                "Initialise"    :   0x01,
                "SetMTPLockKey" :   0x02,
                "SetThVolt"     :   0x03,
                "SetThTemp"     :   0x04,
                "SetGPIO_ConfDly":  0x05,
                "SetZMCurr"     :   0x06,
                "SetZMFreq"     :   0x07,
                "SetBalCurr"    :   0x08,
                "SetBalVolt"    :   0x09,
                "SetSRMask"     :   0x0A,
                "SetMode"       :   0x0B,
                "SetForceErr"   :   0x0C,
                "GetStatus"     :   0x0D,
                "GetData"       :   0x0E,
                "SetRegBank"    :   0x0F
                }

default ={      "Enumerate"     :   0x0400,
                "Initialise"    :   0x1300,
                "SetMTPLockKey" :   0x0000,
                "SetThVolt"     :   0xFF00,
                "SetThTemp"     :   0x7F80,
                "SetGPIO_ConfDly":  0x0000,
                "SetZMCurr"     :   0x0000,
                "SetZMFreq"     :   0x0F20,
                "SetBalCurr"    :   0x0000,
                "SetBalVolt"    :   0x3FFF,
                "SetSRMask"     :   0x0000,
                "SetMode"       :   0x0000,
                "SetForceErr"   :   0x0000,
                "GetStatus"     :   0x0000,
                "GetData"       :   0x0000,
                "SetRegBank"    :   0x0000
                }

Enumerate = {   "WriteMTP"      : { "NoWrite"   : 0b0 << 15,        # POR
                                    "Write"     : 0b1 << 15},
                "ContClk"      :  { "Enable"   : 0b1 << 10,        # POR
                                    "Disable"   : 0b0 << 10},
                "SplitBus"      : { "Enable"    : 0b1 << 9,
                                    "Disable"   : 0b0 << 9},        # POR
                "IgnoreBcast"   : { "Listen"    : 0b0 << 8,         # POR
                                    "Ignore"    : 0b1 << 8},   
                "SetID"         : (lambda x : x << 0)               # POR: 0; range: 1 ~ 250
                }
                              
Initialise = {  "WriteMTP"      : { "NoWrite"   : 0b0 << 15,        # POR
                                    "Write"     : 0b1 << 15},
                "Time2Mute"      : { "Disable"   : 0b0 << 14,        # POR
                                    "Enable"     : 0b1 << 14},
                "ReloadMTP"     : { "NoReload"  : 0b0 << 13,        # POR
                                    "Reload"    : 0b1 << 13},
                "EnSrvReq"      : { "Disable"   : 0b0 << 12,  
                                    "Enable"    : 0b1 << 12},       # POR
                "ResetID"       : { "NoReset"   : 0b0 << 10,        # POR
                                    "Reset"     : 0b1 << 10},
                "AutoStb"       : { "NoAutoStb"     : 0b00 << 8,    #POR
                                    "AutoStb_10"    : 0b10 << 8,    # Only if balancing is not active
                                    "AutoStb_11"    : 0b11 << 8},   # POR value only if balancing is active
               "NrOfLinxes"     : (lambda x : x << 0)               # POR: 0; range: 1 ~ 250
                }


SetMTPLockKey = {"MTPLockKey"   : (lambda x : x << 0)}              # the password : 0035h

SetThVolt = {   "ThOver"        : (lambda x : x << 8),              # POR: 255; range: 0 ~ 255 (1.8 ~ 5.8V, step 18.8mV)
                "ThUnder"       : (lambda x : x << 0)               # POR: 0; range: 0 ~ 255 (1.8 ~ 5.8V, step 18.8mV)
                }       

SetThTemp = {   "ThOver"        : (lambda x : x << 8),              # POR: 255; range: 0 ~ 255 (-128 ~ 127C, step 1C)
                "ThUnder"       : (lambda x : x << 0)               # POR: 0; range: 0 ~ 255 (-128 ~ 127C, step 1C)
                }
SetGPIO_ConfDly = {   "GPIO2_modeSPI" : {"Input"      : 0b00 << 14, # POR
                                         "OutputHigh" : 0b11 << 14,
                                         "OutputLow"  : 0b10 << 14,},
                      "GPIO1_modeSPI" : {"Input"      : 0b00 << 12, # POR
                                         "OutputHigh" : 0b11 << 12,
                                         "OutputLow"  : 0b10 << 12,},
                      "GPIO2_mode"    : {"Input"      : 0b00 << 10, # POR
                                         "OutputHigh" : 0b11 << 10,
                                         "OutputLow"  : 0b10 << 10,},
                      "GPIO1_mode"    : {"Input"      : 0b00 << 8, # POR
                                         "OutputHigh" : 0b11 << 8,
                                         "OutputLow"  : 0b10 << 8,},
                      "NrOfLinxesInBottomChain"    : (lambda x : x << 0) ,
                }
SetZMCurr = {   "EnZM"          : { "Stop"      : 0b00 << 11,       # POR
                                    "Start"     : 0b01 << 11},
                "EnXCS"         : { "Internal"  : 0b0  << 10,       # POR
                                    "External"  : 0b1  << 10},
                "HiPass"        : { "1x"        : 0b00 << 8,        # POR
                                    "4x"        : 0b01 << 8,
                                    "16x"       : 0b10 << 8,
                                    "16xx"      : 0b11 << 8},       # Undefined in MRA4
                "TimeOut"       : (lambda x : x << 0)               # POR: 0; range: 0 ~ 255 (0 ~ 9.5h, step 134s)
                }

SetZMFreq = {   "Freq_spread"   : { "Disable"  : 0b00 << 13,        #POR
                                    "Enable"   : 0b01 << 13},
                "WinEn"         : { "Disable"  : 0b00 << 12,        #POR
                                    "Enable"   : 0b01 << 12},
                "Fexponent"     : (lambda x : x << 8),              # POR: 0; range: 0 ~ 15
                "Fmantissa"     : (lambda x : x << 0)               # POR: 0; range 0 ~ 255
                }

SetBalCurr = {  "EnBal"         : { "Stop"      : 0b0 << 12,        # POR
                                    "Start"     : 0b1 << 12},       # Cannot be combined with EnZM. 
                "Current"       : (lambda x : x << 8),              # POR: 0; range: 0 ~ 15 (0 ~ 200mA, step 13.333mA)
                "TimeOut"       : (lambda x : x << 0)               # POR: 0; range: 0 ~ 255 (0 ~ 9.5h, step 134s)
                }

SetBalVolt = {  "BalMode"       : { "Disable"        : 0b0 << 14,   # POR
                                    "Enable"         : 0b1 << 14},  # Cannot be combined with EnZM. 
                "BalVolt"       : (lambda x : x << 0)               # POR: 16383; range: 0 ~ 16383 (1.2 ~ 6V) , If target voltage is reached 3 times, Linx stops balancing
                }

SetSRMask = {   "CmdErr"            : { "NoMask"    : 0b0 << 14,   # POR
                                        "Mask"      : 0b1 << 14},  # Cmd Err none-maskable
                "ClockErr"          : { "NoMask"    : 0b0 << 13,   # POR
                                        "Mask"      : 0b1 << 13},
                "IntErr"            : { "NoMask"    : 0b0 << 12,   # POR
                                        "Mask"      : 0b1 << 12},  # Integrity Errors
                "GPIOErr"           : { "NoMask"    : 0b0 << 11,   # POR
                                        "Mask"      : 0b1 << 11},  # Voltage drop at output > 100 mV
                "InvalidLockKey"    : { "NoMask"    : 0b0 << 10,   # POR
                                        "Mask"      : 0b1 << 10},  #nvalidLockKey none-maskable
                "OpenWire"          : { "NoMask"    : 0b0 << 9,    # POR
                                        "Mask"      : 0b1 << 9},
                "ZMADCErr"          : { "NoMask"    : 0b0 << 8,    # POR
                                        "Mask"      : 0b1 << 8},
                "BalZMDone"         : { "NoMask"    : 0b0 << 7,    # POR
                                        "Mask"      : 0b1 << 7},
                "CurrErr"           : { "NoMask"    : 0b0 << 6,    # POR
                                        "Mask"      : 0b1 << 6},   # Could be combined with BalCurrOor, if it is still there. Includes VDRErr.
                "LDOOoR"            : { "NoMask"    : 0b0 << 5,    # POR
                                        "Mask"      : 0b1 << 5},
                "TempADCErr"        : { "NoMask"    : 0b0 << 4,    # POR
                                        "Mask"      : 0b1 << 4},   # means DTS difference, DTS-squared difference, max.Die Temp
                "CellTempErr"       : { "NoMask"    : 0b0 << 3,    # POR
                                        "Mask"      : 0b1 << 3},   # Cell OverTemp and UnderTemp for both DTS
                "VMADCErr"          : { "NoMask"    : 0b0 << 2,    # POR
                                        "Mask"      : 0b1 << 2},   # includes ADC clipping, adcMGdiff
                "CellVoltErr"       : { "NoMask"    : 0b0 << 1,    # POR
                                        "Mask"      : 0b1 << 1},   # OverVoltage, UnderVoltage, for Main and Guard ADC
                "BrownOut"          : { "NoMask"    : 0b0 << 0,    # POR
                                        "Mask"      : 0b1 << 0}
                }

SetMode = {     "OperatingMode"     : { "Sleep"     : 0b0001 << 0,  # move to standby when signals on comm lines
                                        "Standby"   : 0b0011 << 0,  # react to commands, but don't measure
                                        "Normal"    : 0b0100 << 0,  # all functions available
# monitor for over/under voltage/temp. Blocked in SPI Linx, SPI-normal: cannot set through this command. Only via SPI_en pin.
                                        "SelfTest" : 0b0110 << 0, }
                }

SetForceErr = {  "GPIO"             : { "Disable"        : 0b0 << 13,   # POR
                                        "Enable"         : 0b1 << 13},
                "VDRcomp"           : { "Disable"        : 0b0 << 12,   # POR
                                        "Enable"         : 0b1 << 12},
                "OpenWire"          : { "Disable"        : 0b0 << 11,   # POR
                                        "Enable"         : 0b1 << 11},  # Vss/Vbat detectors, Resistor detector, DIO open wires
                "UTOT"              : { "Disable"        : 0b0 << 10,
                                        "Enable"         : 0b1 << 10},
                "DTScomp"           : { "Disable"        : 0b0 << 9,    # POR
                                        "Enable"         : 0b1 << 9},
                "UVOV"              : { "Disable"        : 0b0 << 8,    # POR
                                        "Enable"         : 0b1 << 8},
                "VMcomp"            : { "Disable"        : 0b0 << 7,    # POR
                                        "Enable"         : 0b1 << 7},
                "LDOfsm"           : { "Disable"        : 0b0 << 6,    # POR Not implemented. To be done for MRA4
                                        "Enable"         : 0b1 << 6},
                "GLDOAna"           : { "Disable"        : 0b0 << 4,    # POR
                                        "Enable"         : 0b1 << 4},
                "GLDODig"           : { "Disable"        : 0b0 << 3,    # POR
                                        "Enable"         : 0b1 << 3},
                "GLDOPll"           : { "Disable"        : 0b0 << 2,    # POR
                                        "Enable"         : 0b1 << 2},
                "MLDOAna"           : { "Disable"        : 0b0 << 1,    # POR
                                        "Enable"         : 0b1 << 1},
                "MLDOBal"           : { "Disable"        : 0b0 << 0,    # POR
                                        "Enable"         : 0b1 << 0},
                }

GetStatus = {   "StatusType"        : { "ComStatus"         : 0b00000 << 0,
                                        "Invalidedges"      : 0b00001 << 0,
                                        "GeneralStatus"     : 0b00010 << 0,
                                        "CoreStatus"        : 0b01000 << 0,
                                        "PLLStatus"         : 0b01001 << 0,
                                        "BALStatus"         : 0b10000 << 0,
                                        "SrvReqData"        : 0b10010 << 0,
                                        "VoltDiagnostics"   : 0b10011 << 0,
                                        "TempDiagnostics"   : 0b10100 << 0,
                                        "CurrDiagnostics"   : 0b10101 << 0,
                                        "ZMDiagnostics"     : 0b10110 << 0,
                                        "BoardDiagnostics"  : 0b10111 << 0,
                                        "ICDiagnostics"     : 0b11000 << 0}
                    }

GetData = {     "RstZMPh"           : { "NoReset"           : 0b0 << 15,        # POR
                                        "Reset"             : 0b1 << 15},       # Reset ZM phase. Resets ""Send Command Twice" counter
                "ClrExeCnt"         : { "NoReset"           : 0b0 << 14,        # POR
                                        "Reset"             : 0b1 << 14},       # Clear execution Counter. Resets ""Send Command Twice" counter
                "Equidist"          : { "Reset"             : 0b0 << 13,        # reset VM filter and start new measurement
                                        "NoReset"           : 0b1 << 13},       # POR
                "ResetRSC"          : { "NoAction"          : 0b0 << 12,        # POR
                                        "ResetRSC"          : 0b1 << 12},
                "SampleRate"        : (lambda x : x << 8),                      # POR: 0; range: 0 ~ 8 (4ms ~ 1s)
                "DataType"          : { "MainVolt"          : 0b000000 << 0,    # POR
                                        "GuardVolt"         : 0b000001 << 0,
                                        "MainCellTemp"      : 0b000010 << 0,
                                        "GuardCellTemp"     : 0b000011 << 0,    # accurate DTS
                                        "MainDieTemp"       : 0b000100 << 0,
                                        "GuardDieTemp"      : 0b000101 << 0,
                                        "VZM"               : 0b000110 << 0,
                                        "Zreal"             : 0b000111 << 0,
                                        "Zimag"             : 0b001000 << 0,
                                        "UniqueID1"         : 0b001001 << 0,    # Batch ID
                                        "UniqueID2"         : 0b001010 << 0,    #Batch ID[7:0] Wafer[23:16]
                                        "UniqueID3"         : 0b001011 << 0,    #p_id_wafer[15:0]
                                        "UniqueID4"         : 0b001100 << 0,    # p_id_x[7:0, p_id_y[7:0]
                                        "HwChksumMTP"       : 0b001101 << 0,
                                        "HwChksumSet"       : 0b001110 << 0,
                                        "ProductVersion"    : 0b001111 << 0},
                    }

SetRegBank = {  "RW"                : { "Write"     : 0b0 << 8,     # POR
                                        "Read"      : 0b1 << 8},
                "BankAddr"          : (lambda x : x << 0),          # POR: 0; range: 0 ~ 127
                }

