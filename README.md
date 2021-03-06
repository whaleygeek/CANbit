# CANbit
A CAN interface to a vehicle diagnostics port, using a micro:bit

This is very much a work in progress, but feel free to follow along as the story unfolds!

## output from micro:bit

The .hex file, when loaded into a CANBit board, will output a number of different records.
Here is a sample of the logged data that comes (very fast!) over the USBSER serial port
when the vehicle is turned on.

     INIT,START
    INIT,OK
    RX,07E8,04,41,0C,0D,B0,00,00,00
    RPM,876
    RX,0210,FF,FF,30,A0,90,00,8E,00
    RX,07E8,03,41,0D,00,00,00,00,00
    SPEED,0
    RX,0210,FF,FF,30,A0,90,00,8F,00
    RX,07E8,03,41,0D,00,00,00,00,00
    SPEED,0
    RX,07E8,04,41,0C,0D,B0,00,00,00
    RPM,876
    RX,07E8,03,41,05,65,00,00,00,00
    TEMP,61
    RX,07E8,03,41,0D,00,00,00,00,00
    SPEED,0
    
    RX,07E8,03,41,0D,1D,00,00,00,00
    SPEED,29
    RX,07E8,04,41,0C,0D,D8,00,00,00
    RPM,886
    RX,07E8,03,41,0D,1D,00,00,00,00
    SPEED,29
    RX,0210,FF,FF,30,A0,90,00,69,00
    RX,07E8,03,41,05,7B,00,00,00,00
    TEMP,83
    RX,0210,FF,FF,30,A0,90,00,6A,00
    RX,07E8,04,41,0C,0D,DC,00,00,00
    RPM,887
    RX,0210,FF,FF,30,A0,90,00,6B,00
    RX,07E8,04,41,0C,0D,DC,00,00,00
    RPM,887

All records are CSV (comma separated values).

INIT - part of the initialise procedure, followed by START, OK or FAIL.

RX - a raw CAN message from the OBD-II diagnostics. The first hex number is the CAN identifier of
the responding unit, usually 0x7E8 for an ECU. The next 8 hex bytes are the raw CAN message.
0x0210 is a regular timestamp message that the vehicle emits when powered up.

An OBD-II response (inside the 0x07E8 message) consists of a length byte, then 0x40 + the mode number,
then 1 or more bytes (as indicated by the length byte) of data. Each message type has different
encodings. You can get the encodings from this [wiki page](https://en.wikipedia.org/wiki/OBD-II_PIDs)

The CANBit software decodes these for you, so you don't have to look in the raw messages.

SPEED is vehicle speed in MPH - this appears to be just an estimated speed on some vehicles,
as it doesn't completely match what the speedometer states, and the lag is different on the
real speedo.

RPM is the engine speed in RPM. Idle is usually about 850-900RPM.

TEMP is the coolant temperature, in degrees Celcius.

## logging

The test1.py program just logs all data that comes over USBSER from the CANBit. It logs
all messages to a file called log.txt, but strips out the RX messages for the display.

## decoding

A crude decoder is written in process.py - it takes SPEED, RPM and TEMP records,
and creates one CSV line on stdout for each record processed. That's not very efficient
as you get 3 CSV records for each cycle of data, but it was quick and simple at the
time, and means that you don't loose data if the vehicle decides not to output
one of the records for some reason (responding to a poll message is actually
optional in the spec!)

## CAN messages

There are many messages that can be requested from the vehicle, but only the speed, temp and
rpm records are actually polled at the moment.

# Future Work

1. Poll on a timer rather than 'as fast as you can go'

2. Poll more record types (e.g. fuel rate, fuel level, throttle pos)

3. Package up data into a single 'radio' payload message

4. Define the payload format

5. Write an example app in MicroPython at the receiving end, to do something
useful with the data (e.g. work out and display the gear from the RPM and SPEED)