import openvino as ov
 
core = ov.Core()
 
print(core.available_devices)
 
print([core.get_property(device, "FULL_DEVICE_NAME") for device in core.available_devices])
