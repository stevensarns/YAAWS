import time
import signal
import smbus
import config

bus = smbus.SMBus(1)
time.sleep(1)

def unsigned2signed(x):
    if x>0x7FFF:
        x = x - 0x10000
    return x

config.pin = 0.0
config.tin = 0.0
Tcal = -7.0
Pcal = 0.0
def get():
        try:
                ADDR_H = 0x38
                config = [0x08, 0x00]
                MeasureCmd = [0x33, 0x00]
                
                ADDR_B     = 0x76
                TEMP_XSB   = 0xFC
                TEMP_LSB   = 0xFB
                TEMP_MSB   = 0xFA
                PRES_XSB   = 0xF9
                PRES_LSB   = 0xF8
                PRES_MSB   = 0xF7
                CONFIG     = 0xF5
                CTRL       = 0xF4
                TCOMP      = 0x88
                PCOMP      = 0x8E
                
                DIG_T1_LSB = 0x88
                DIG_T1_MSB = 0x89 
                DIG_T2_LSB = 0x8A
                DIG_T2_MSB = 0x8B
                DIG_T3_LSB = 0x8C
                DIG_T3_MSB = 0x8D
                
                DIG_P1_LSB = 0x8E
                DIG_P1_MSB = 0x8F 
                DIG_P2_LSB = 0x90
                DIG_P2_MSB = 0x91
                DIG_P3_LSB = 0x92
                DIG_P3_MSB = 0x93
                DIG_P4_LSB = 0x94
                DIG_P4_MSB = 0x95 
                DIG_P5_LSB = 0x96
                DIG_P5_MSB = 0x97
                DIG_P6_LSB = 0x98
                DIG_P6_MSB = 0x99
                DIG_P7_LSB = 0x9A
                DIG_P7_MSB = 0x9B 
                DIG_P8_LSB = 0x9C
                DIG_P8_MSB = 0x9D
                DIG_P9_LSB = 0x9E
                DIG_P9_MSB = 0x9F
                
                
                VAL_CONFIG = 0b01001000 # t_sb=010, filter=010, spi_en=0
                VAL_CTRL   = 0b00101011 # T=001, P=010, MODE=11
                
                dig_T1 = (bus.read_byte_data(ADDR_B,DIG_T1_MSB)<<8) | bus.read_byte_data(ADDR_B,DIG_T1_LSB)
                dig_T2 = (bus.read_byte_data(ADDR_B,DIG_T2_MSB)<<8) | bus.read_byte_data(ADDR_B,DIG_T2_LSB)
                dig_T2 = unsigned2signed(dig_T2)
                dig_T3 = (bus.read_byte_data(ADDR_B,DIG_T3_MSB)<<8) | bus.read_byte_data(ADDR_B,DIG_T3_LSB)
                dig_T3 = unsigned2signed(dig_T3)
                
                dig_P1 = (bus.read_byte_data(ADDR_B,DIG_P1_MSB)<<8) | bus.read_byte_data(ADDR_B,DIG_P1_LSB)
                dig_P2 = (bus.read_byte_data(ADDR_B,DIG_P2_MSB)<<8) | bus.read_byte_data(ADDR_B,DIG_P2_LSB)
                dig_P2 = unsigned2signed(dig_P2)
                dig_P3 = (bus.read_byte_data(ADDR_B,DIG_P3_MSB)<<8) | bus.read_byte_data(ADDR_B,DIG_P3_LSB)
                dig_P3 = unsigned2signed(dig_P3)
                dig_P4 = (bus.read_byte_data(ADDR_B,DIG_P4_MSB)<<8) | bus.read_byte_data(ADDR_B,DIG_P4_LSB)
                dig_P4 = unsigned2signed(dig_P4)
                dig_P5 = (bus.read_byte_data(ADDR_B,DIG_P5_MSB)<<8) | bus.read_byte_data(ADDR_B,DIG_P5_LSB)
                dig_P5 = unsigned2signed(dig_P5)
                dig_P6 = (bus.read_byte_data(ADDR_B,DIG_P6_MSB)<<8) | bus.read_byte_data(ADDR_B,DIG_P6_LSB)
                dig_P6 = unsigned2signed(dig_P6)
                dig_P7 = (bus.read_byte_data(ADDR_B,DIG_P7_MSB)<<8) | bus.read_byte_data(ADDR_B,DIG_P7_LSB)
                dig_P7 = unsigned2signed(dig_P7)
                dig_P8 = (bus.read_byte_data(ADDR_B,DIG_P8_MSB)<<8) | bus.read_byte_data(ADDR_B,DIG_P8_LSB)
                dig_P8 = unsigned2signed(dig_P8)
                dig_P9 = (bus.read_byte_data(ADDR_B,DIG_P9_MSB)<<8) | bus.read_byte_data(ADDR_B,DIG_P9_LSB)
                dig_P9 = unsigned2signed(dig_P9)
                
                bus.write_byte_data(ADDR_B,CONFIG,VAL_CONFIG) # initialize BMP280
                bus.write_byte_data(ADDR_B,CTRL,  VAL_CTRL)
                
                tempMSB = bus.read_byte_data(ADDR_B,TEMP_MSB)
                tempLSB = bus.read_byte_data(ADDR_B,TEMP_LSB)
                tempXSB = bus.read_byte_data(ADDR_B,TEMP_XSB)
                adc_T = ((tempMSB<<16) | (tempLSB<<8) | tempXSB)>>4
                
                var1 = (((adc_T>>3) - (dig_T1<<1)) * dig_T2)>>11
                var2 = (((((adc_T>>4) - dig_T1)) * ((adc_T>>4) - ((dig_T1)))>>12) * dig_T3)>>14
                t_fine = var1 + var2
                T = (((t_fine*5)+128)>>8)/100.
                T = (9.*T/5.) + 32.
                tin = T + Tcal
                
                presMSB = bus.read_byte_data(ADDR_B,PRES_MSB)
                presLSB = bus.read_byte_data(ADDR_B,PRES_LSB)
                presXSB = bus.read_byte_data(ADDR_B,PRES_XSB) # i2c takes 4 mS
                adc_P = ((presMSB<<16) | (presLSB<<8) | presXSB)>>4
                
                var1 = t_fine/2. - 64000
                var2 = var1 * var1 * dig_P6/32768.
                var2 = var2 + var1 * dig_P5 *2
                var2 = var2/4 + dig_P4*65536.
                var1 = (dig_P3 * var1 * var1 / 524288. + var1 * dig_P2) / 524288.
                var1 = (1. + var1/32768.) * dig_P1
                p = 1048576. - adc_P
                p = (p - (var2/4096.)) * 6250. / var1
                var1 = dig_P9 * p / 2147483648. * p
                var2 = p * dig_P8 / 32768.
                p = (p + (var1 + var2 + dig_P7)/ 16.)/100.
                pin = p
                return tin, pin
        except:
                print("get() in bmp() fail")
