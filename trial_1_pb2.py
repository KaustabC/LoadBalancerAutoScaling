# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: trial_1.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\rtrial_1.proto\x12\x07trial_1\"\x8a\x01\n\x10\x66unction_message\x12\x12\n\x05\x64\x61ta1\x18\x01 \x01(\x05H\x00\x88\x01\x01\x12\x12\n\x05\x64\x61ta2\x18\x02 \x01(\x05H\x01\x88\x01\x01\x12\x15\n\x08\x66unction\x18\x03 \x01(\x05H\x02\x88\x01\x01\x12\x0f\n\x02ip\x18\x04 \x01(\tH\x03\x88\x01\x01\x42\x08\n\x06_data1B\x08\n\x06_data2B\x0b\n\t_functionB\x05\n\x03_ip\"y\n\x0binitMessage\x12\x15\n\x08loadType\x18\x01 \x01(\x05H\x00\x88\x01\x01\x12\x15\n\x08\x61utoType\x18\x02 \x01(\x05H\x01\x88\x01\x01\x12\x15\n\x08services\x18\x03 \x01(\tH\x02\x88\x01\x01\x42\x0b\n\t_loadTypeB\x0b\n\t_autoTypeB\x0b\n\t_services\"i\n\tinitReply\x12\x11\n\x04port\x18\x01 \x01(\x05H\x00\x88\x01\x01\x12\x15\n\x08services\x18\x02 \x01(\tH\x01\x88\x01\x01\x12\x12\n\x05\x63ount\x18\x03 \x01(\x05H\x02\x88\x01\x01\x42\x07\n\x05_portB\x0b\n\t_servicesB\x08\n\x06_count\"\'\n\x0breturnValue\x12\x10\n\x03val\x18\x01 \x01(\x02H\x00\x88\x01\x01\x42\x06\n\x04_val\"\x06\n\x04void2\x88\x01\n\x05\x41lert\x12\x41\n\x0cInvokeMethod\x12\x19.trial_1.function_message\x1a\x14.trial_1.returnValue\"\x00\x12<\n\x0e\x43reateInstance\x12\x14.trial_1.initMessage\x1a\x12.trial_1.initReply\"\x00\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'trial_1_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _globals['_FUNCTION_MESSAGE']._serialized_start=27
  _globals['_FUNCTION_MESSAGE']._serialized_end=165
  _globals['_INITMESSAGE']._serialized_start=167
  _globals['_INITMESSAGE']._serialized_end=288
  _globals['_INITREPLY']._serialized_start=290
  _globals['_INITREPLY']._serialized_end=395
  _globals['_RETURNVALUE']._serialized_start=397
  _globals['_RETURNVALUE']._serialized_end=436
  _globals['_VOID']._serialized_start=438
  _globals['_VOID']._serialized_end=444
  _globals['_ALERT']._serialized_start=447
  _globals['_ALERT']._serialized_end=583
# @@protoc_insertion_point(module_scope)
