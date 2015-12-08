#
# Autogenerated by Thrift Compiler (0.9.0)
#
# DO NOT EDIT UNLESS YOU ARE SURE THAT YOU KNOW WHAT YOU ARE DOING
#
#  options string: py
#

from thrift.Thrift import TType, TMessageType, TException, TApplicationException
from ttypes import *
from thrift.Thrift import TProcessor
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol, TProtocol
try:
  from thrift.protocol import fastbinary
except:
  fastbinary = None


class Iface:
  def onUpdatePushRoute(self, rd, prefix, prefixlen, nexthop, label):
    """
    Parameters:
     - rd
     - prefix
     - prefixlen
     - nexthop
     - label
    """
    pass

  def onUpdateWithdrawRoute(self, rd, prefix, prefixlen):
    """
    Parameters:
     - rd
     - prefix
     - prefixlen
    """
    pass

  def onStartConfigResyncNotification(self, ):
    pass


class Client(Iface):
  def __init__(self, iprot, oprot=None):
    self._iprot = self._oprot = iprot
    if oprot is not None:
      self._oprot = oprot
    self._seqid = 0

  def onUpdatePushRoute(self, rd, prefix, prefixlen, nexthop, label):
    """
    Parameters:
     - rd
     - prefix
     - prefixlen
     - nexthop
     - label
    """
    self.send_onUpdatePushRoute(rd, prefix, prefixlen, nexthop, label)

  def send_onUpdatePushRoute(self, rd, prefix, prefixlen, nexthop, label):
    self._oprot.writeMessageBegin('onUpdatePushRoute', TMessageType.CALL, self._seqid)
    args = onUpdatePushRoute_args()
    args.rd = rd
    args.prefix = prefix
    args.prefixlen = prefixlen
    args.nexthop = nexthop
    args.label = label
    args.write(self._oprot)
    self._oprot.writeMessageEnd()
    self._oprot.trans.flush()
  def onUpdateWithdrawRoute(self, rd, prefix, prefixlen):
    """
    Parameters:
     - rd
     - prefix
     - prefixlen
    """
    self.send_onUpdateWithdrawRoute(rd, prefix, prefixlen)

  def send_onUpdateWithdrawRoute(self, rd, prefix, prefixlen):
    self._oprot.writeMessageBegin('onUpdateWithdrawRoute', TMessageType.CALL, self._seqid)
    args = onUpdateWithdrawRoute_args()
    args.rd = rd
    args.prefix = prefix
    args.prefixlen = prefixlen
    args.write(self._oprot)
    self._oprot.writeMessageEnd()
    self._oprot.trans.flush()
  def onStartConfigResyncNotification(self, ):
    self.send_onStartConfigResyncNotification()

  def send_onStartConfigResyncNotification(self, ):
    self._oprot.writeMessageBegin('onStartConfigResyncNotification', TMessageType.CALL, self._seqid)
    args = onStartConfigResyncNotification_args()
    args.write(self._oprot)
    self._oprot.writeMessageEnd()
    self._oprot.trans.flush()

class Processor(Iface, TProcessor):
  def __init__(self, handler):
    self._handler = handler
    self._processMap = {}
    self._processMap["onUpdatePushRoute"] = Processor.process_onUpdatePushRoute
    self._processMap["onUpdateWithdrawRoute"] = Processor.process_onUpdateWithdrawRoute
    self._processMap["onStartConfigResyncNotification"] = Processor.process_onStartConfigResyncNotification

  def process(self, iprot, oprot):
    (name, type, seqid) = iprot.readMessageBegin()
    if name not in self._processMap:
      iprot.skip(TType.STRUCT)
      iprot.readMessageEnd()
      x = TApplicationException(TApplicationException.UNKNOWN_METHOD, 'Unknown function %s' % (name))
      oprot.writeMessageBegin(name, TMessageType.EXCEPTION, seqid)
      x.write(oprot)
      oprot.writeMessageEnd()
      oprot.trans.flush()
      return
    else:
      self._processMap[name](self, seqid, iprot, oprot)
    return True

  def process_onUpdatePushRoute(self, seqid, iprot, oprot):
    args = onUpdatePushRoute_args()
    args.read(iprot)
    iprot.readMessageEnd()
    self._handler.onUpdatePushRoute(args.rd, args.prefix, args.prefixlen, args.nexthop, args.label)
    return

  def process_onUpdateWithdrawRoute(self, seqid, iprot, oprot):
    args = onUpdateWithdrawRoute_args()
    args.read(iprot)
    iprot.readMessageEnd()
    self._handler.onUpdateWithdrawRoute(args.rd, args.prefix, args.prefixlen)
    return

  def process_onStartConfigResyncNotification(self, seqid, iprot, oprot):
    args = onStartConfigResyncNotification_args()
    args.read(iprot)
    iprot.readMessageEnd()
    self._handler.onStartConfigResyncNotification()
    return


# HELPER FUNCTIONS AND STRUCTURES

class onUpdatePushRoute_args:
  """
  Attributes:
   - rd
   - prefix
   - prefixlen
   - nexthop
   - label
  """

  thrift_spec = (
    None, # 0
    (1, TType.STRING, 'rd', None, None, ), # 1
    (2, TType.STRING, 'prefix', None, None, ), # 2
    (3, TType.I32, 'prefixlen', None, None, ), # 3
    (4, TType.STRING, 'nexthop', None, None, ), # 4
    (5, TType.I32, 'label', None, None, ), # 5
  )

  def __init__(self, rd=None, prefix=None, prefixlen=None, nexthop=None, label=None,):
    self.rd = rd
    self.prefix = prefix
    self.prefixlen = prefixlen
    self.nexthop = nexthop
    self.label = label

  def read(self, iprot):
    if iprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None and fastbinary is not None:
      fastbinary.decode_binary(self, iprot.trans, (self.__class__, self.thrift_spec))
      return
    iprot.readStructBegin()
    while True:
      (fname, ftype, fid) = iprot.readFieldBegin()
      if ftype == TType.STOP:
        break
      if fid == 1:
        if ftype == TType.STRING:
          self.rd = iprot.readString();
        else:
          iprot.skip(ftype)
      elif fid == 2:
        if ftype == TType.STRING:
          self.prefix = iprot.readString();
        else:
          iprot.skip(ftype)
      elif fid == 3:
        if ftype == TType.I32:
          self.prefixlen = iprot.readI32();
        else:
          iprot.skip(ftype)
      elif fid == 4:
        if ftype == TType.STRING:
          self.nexthop = iprot.readString();
        else:
          iprot.skip(ftype)
      elif fid == 5:
        if ftype == TType.I32:
          self.label = iprot.readI32();
        else:
          iprot.skip(ftype)
      else:
        iprot.skip(ftype)
      iprot.readFieldEnd()
    iprot.readStructEnd()

  def write(self, oprot):
    if oprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and self.thrift_spec is not None and fastbinary is not None:
      oprot.trans.write(fastbinary.encode_binary(self, (self.__class__, self.thrift_spec)))
      return
    oprot.writeStructBegin('onUpdatePushRoute_args')
    if self.rd is not None:
      oprot.writeFieldBegin('rd', TType.STRING, 1)
      oprot.writeString(self.rd)
      oprot.writeFieldEnd()
    if self.prefix is not None:
      oprot.writeFieldBegin('prefix', TType.STRING, 2)
      oprot.writeString(self.prefix)
      oprot.writeFieldEnd()
    if self.prefixlen is not None:
      oprot.writeFieldBegin('prefixlen', TType.I32, 3)
      oprot.writeI32(self.prefixlen)
      oprot.writeFieldEnd()
    if self.nexthop is not None:
      oprot.writeFieldBegin('nexthop', TType.STRING, 4)
      oprot.writeString(self.nexthop)
      oprot.writeFieldEnd()
    if self.label is not None:
      oprot.writeFieldBegin('label', TType.I32, 5)
      oprot.writeI32(self.label)
      oprot.writeFieldEnd()
    oprot.writeFieldStop()
    oprot.writeStructEnd()

  def validate(self):
    return


  def __repr__(self):
    L = ['%s=%r' % (key, value)
      for key, value in self.__dict__.iteritems()]
    return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

  def __eq__(self, other):
    return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

  def __ne__(self, other):
    return not (self == other)

class onUpdateWithdrawRoute_args:
  """
  Attributes:
   - rd
   - prefix
   - prefixlen
  """

  thrift_spec = (
    None, # 0
    (1, TType.STRING, 'rd', None, None, ), # 1
    (2, TType.STRING, 'prefix', None, None, ), # 2
    (3, TType.I32, 'prefixlen', None, None, ), # 3
  )

  def __init__(self, rd=None, prefix=None, prefixlen=None,):
    self.rd = rd
    self.prefix = prefix
    self.prefixlen = prefixlen

  def read(self, iprot):
    if iprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None and fastbinary is not None:
      fastbinary.decode_binary(self, iprot.trans, (self.__class__, self.thrift_spec))
      return
    iprot.readStructBegin()
    while True:
      (fname, ftype, fid) = iprot.readFieldBegin()
      if ftype == TType.STOP:
        break
      if fid == 1:
        if ftype == TType.STRING:
          self.rd = iprot.readString();
        else:
          iprot.skip(ftype)
      elif fid == 2:
        if ftype == TType.STRING:
          self.prefix = iprot.readString();
        else:
          iprot.skip(ftype)
      elif fid == 3:
        if ftype == TType.I32:
          self.prefixlen = iprot.readI32();
        else:
          iprot.skip(ftype)
      else:
        iprot.skip(ftype)
      iprot.readFieldEnd()
    iprot.readStructEnd()

  def write(self, oprot):
    if oprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and self.thrift_spec is not None and fastbinary is not None:
      oprot.trans.write(fastbinary.encode_binary(self, (self.__class__, self.thrift_spec)))
      return
    oprot.writeStructBegin('onUpdateWithdrawRoute_args')
    if self.rd is not None:
      oprot.writeFieldBegin('rd', TType.STRING, 1)
      oprot.writeString(self.rd)
      oprot.writeFieldEnd()
    if self.prefix is not None:
      oprot.writeFieldBegin('prefix', TType.STRING, 2)
      oprot.writeString(self.prefix)
      oprot.writeFieldEnd()
    if self.prefixlen is not None:
      oprot.writeFieldBegin('prefixlen', TType.I32, 3)
      oprot.writeI32(self.prefixlen)
      oprot.writeFieldEnd()
    oprot.writeFieldStop()
    oprot.writeStructEnd()

  def validate(self):
    return


  def __repr__(self):
    L = ['%s=%r' % (key, value)
      for key, value in self.__dict__.iteritems()]
    return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

  def __eq__(self, other):
    return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

  def __ne__(self, other):
    return not (self == other)

class onStartConfigResyncNotification_args:

  thrift_spec = (
  )

  def read(self, iprot):
    if iprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None and fastbinary is not None:
      fastbinary.decode_binary(self, iprot.trans, (self.__class__, self.thrift_spec))
      return
    iprot.readStructBegin()
    while True:
      (fname, ftype, fid) = iprot.readFieldBegin()
      if ftype == TType.STOP:
        break
      else:
        iprot.skip(ftype)
      iprot.readFieldEnd()
    iprot.readStructEnd()

  def write(self, oprot):
    if oprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and self.thrift_spec is not None and fastbinary is not None:
      oprot.trans.write(fastbinary.encode_binary(self, (self.__class__, self.thrift_spec)))
      return
    oprot.writeStructBegin('onStartConfigResyncNotification_args')
    oprot.writeFieldStop()
    oprot.writeStructEnd()

  def validate(self):
    return


  def __repr__(self):
    L = ['%s=%r' % (key, value)
      for key, value in self.__dict__.iteritems()]
    return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

  def __eq__(self, other):
    return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

  def __ne__(self, other):
    return not (self == other)
