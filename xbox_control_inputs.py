import asyncio
import evdev

def find_controller():
    devices = [evdev.InputDevice(path) for path in evdev.list_devices()]

    for device in devices:
        name = device.name
        output = "Himal this is you speaking. Controller not found"
        found = name.find("Xbox")
        if found != -1:
            output = device.path
            break

    return output


async def controller_inputs (controller_path):
    dev = evdev.InputDevice(controller_path)

    async for ev in dev.async_read_loop():
        if ev.code == 1:
            fraction = 1 - ev.value/65535
            print(fraction)
            return fraction
        
    asyncio.sleep(0.01)
        


#loop = asyncio.get_event_loop()
#loop.run_until_complete(helper(dev))