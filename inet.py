import struct
ENC_JSON = 0X01
ENC_PB = 0X02
ENC_JSON_BYTES = 0X11
ENC_PB_BYTES = 0X12
ENC_JSON_RSA = 0X21
ENC_PB_RSA = 0X22
ENC_JSON_AES = 0X31
ENC_PB_AES = 0X32

headerLen = 18

class UHeader:
    def __init__(self):
        self.len = 0
        self.crc = 0
        self.ver = 0
        self.sign = 0
        self.mainId = 0
        self.subId = 0
        self.enctyptType = 0
        self.other = 0
        self.requestId = 0
        self.realSize = 0
        self.ba = bytearray()

    def decode(self,buf):
        if(len(buf) < 18):
            print("Buf length is less than 18, actual:{}".format(len(buf)))
        # struct.pack()

    def encode(self,write_array, protobuf_array):
        struct.pack_into("<HHccccIH",self.ba,self.ver,self.sign,self.mainId,self.subId,self.enctyptType,self.other,self.requestId,self.realSize)
        struct.pack_into("s",self.ba,protobuf_array)
        len0 = len(protobuf_array)
        crc = self.get_crc(protobuf_array,len0)
        self.ba.position = 0
        struct.pack_into("<H",self.ba,self.ver)
        pass

    def get_crc(self,buff,len):
        buf_len = len//2
        sum = 0
        for _ in range(0,buf_len):
            sum += struct.unpack("<H")
        aa = len%2
        if aa != 0:
            sum += struct.unpack("<H")
        sum = sum%65536
        return sum