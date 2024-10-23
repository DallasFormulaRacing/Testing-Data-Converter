import struct
import time
from typing import List, TypeVar, Generic, Union, BinaryIO

T = TypeVar('T', float, int)


class DataType:
    def __init__(self, data_type: int, data_type_length: int):
        self.DataType = data_type
        self.DataTypeLength = data_type_length


DataTypeFloat32 = DataType(0x07, 4)
DataTypeInt16 = DataType(0x03, 2)
DataTypeInt32 = DataType(0x05, 4)


class LdFileChannelMeta:
    FORMAT = '<IIIIHHHHhhhh32s8s12s40s'

    def __init__(self):
        self.PreviousMetaPointer = 0
        self.NextMetaPointer = 0
        self.DataPointer = 0
        self.DataLength = 0  # Should be uint32
        self.ChannelId = 0
        self.DataType = 0
        self.DataTypeLength = 0
        self.Frequency = 0
        self.Shift = 0
        self.Mul = 1
        self.Scale = 1
        self.DecPlaces = 0
        self.Name = b''
        self.ShortName = b''
        self.Unit = b''
        self.Padding = b'\x00' * 40  # 40 bytes padding

    def pack(self) -> bytes:
        return struct.pack(
            self.FORMAT,
            self.PreviousMetaPointer,           # I
            self.NextMetaPointer,               # I
            self.DataPointer,                   # I
            self.DataLength,                    # I (Corrected from 'H' to 'I')
            self.ChannelId,                     # H
            self.DataType,                      # H
            self.DataTypeLength,                # H
            self.Frequency,                     # H
            self.Shift,                         # h
            self.Mul,                           # h
            self.Scale,                         # h
            self.DecPlaces,                     # h
            self.Name.ljust(32, b'\x00'),       # 32s
            self.ShortName.ljust(8, b'\x00'),   # 8s
            self.Unit.ljust(12, b'\x00'),       # 12s
            self.Padding                        # 40s
        )


class LdFileEvent:
    FORMAT = '<64s64s1024sH'

    def __init__(self):
        self.Name = b''
        self.Session = b''
        self.Comment = b''
        self.VenuePointer = 0

    def pack(self) -> bytes:
        return struct.pack(
            self.FORMAT,
            self.Name.ljust(64, b'\x00'),
            self.Session.ljust(64, b'\x00'),
            self.Comment.ljust(1024, b'\x00'),
            self.VenuePointer
        )


class LdFileHead:
    FORMAT = (
        '<I4sII20sI24sHHHI8sHHI4s'   # Up to self.Padding4
        '16s16s16s16s'               # Date and Time fields
        '64s64s64s64s64s'            # Five 64-byte fields including self.Padding7
        '1024sI66s64s126s'           # Remaining fields
    )

    def __init__(self):
        self.LDMarker = 0x40
        self.Padding1 = b'\x00' * 4
        self.ChannelsMetaPointer = 0
        self.ChannelsDataPointer = 0
        self.Padding2 = b'\x00' * 20
        self.EventPointer = 0
        self.Padding3 = b'\x00' * 24
        self.Unknown1 = 1
        self.Unknown2 = 0x4240
        self.Unknown3 = 0xF
        self.DeviceSerial = 0x1F44
        self.DeviceType = b'ADL\x00\x00\x00\x00\x00'
        self.DeviceVersion = 420
        self.Unknown4 = 0xADB0
        self.ChannelsCount = 0
        self.Padding4 = b'\x00' * 4
        self.Date = b''
        self.Padding5 = b'\x00' * 16
        self.Time = b''
        self.Padding6 = b'\x00' * 16
        self.Driver = b''
        self.Vehicle = b''
        self.Padding7 = b'\x00' * 64   # Missing in format string before
        self.Venue = b''
        self.Padding8 = b'\x00' * 64
        self.Padding9 = b'\x00' * 1024
        self.EnableProLogging = 0xC81A4
        self.Padding10 = b'\x00' * 66
        self.ShortComment = b''
        self.Padding11 = b'\x00' * 126

    def pack(self) -> bytes:
        return struct.pack(
            self.FORMAT,
            self.LDMarker,                       # I
            self.Padding1,                       # 4s
            self.ChannelsMetaPointer,            # I
            self.ChannelsDataPointer,            # I
            self.Padding2,                       # 20s
            self.EventPointer,                   # I
            self.Padding3,                       # 24s
            self.Unknown1,                       # H
            self.Unknown2,                       # H
            self.Unknown3,                       # H
            self.DeviceSerial,                   # I
            self.DeviceType,                     # 8s
            self.DeviceVersion,                  # H
            self.Unknown4,                       # H
            self.ChannelsCount,                  # I
            self.Padding4,                       # 4s
            self.Date.ljust(16, b'\x00'),        # 16s
            self.Padding5,                       # 16s
            self.Time.ljust(16, b'\x00'),        # 16s
            self.Padding6,                       # 16s
            self.Driver.ljust(64, b'\x00'),      # 64s
            self.Vehicle.ljust(64, b'\x00'),     # 64s
            self.Padding7,                       # 64s (Previously missing)
            self.Venue.ljust(64, b'\x00'),       # 64s
            self.Padding8,                       # 64s
            self.Padding9,                       # 1024s
            self.EnableProLogging,               # I
            self.Padding10,                      # 66s
            self.ShortComment.ljust(64, b'\x00'),# 64s
            self.Padding11                       # 126s
        )


class LdFileVehicle:
    FORMAT = '<64s128sI32s32s'

    def __init__(self):
        self.Id = b''
        self.Padding = b'\x00' * 128
        self.Weight = 0
        self.Type = b''
        self.Comment = b''

    def pack(self) -> bytes:
        return struct.pack(
            self.FORMAT,
            self.Id.ljust(64, b'\x00'),
            self.Padding,
            self.Weight,
            self.Type.ljust(32, b'\x00'),
            self.Comment.ljust(32, b'\x00')
        )


class LdFileVenue:
    FORMAT = '<64s1034sH'

    def __init__(self):
        self.Name = b''
        self.Padding = b'\x00' * 1034
        self.VehiclePointer = 0

    def pack(self) -> bytes:
        return struct.pack(
            self.FORMAT,
            self.Name.ljust(64, b'\x00'),
            self.Padding,
            self.VehiclePointer
        )


class Channel(Generic[T]):
    def __init__(self, frequency: int, name: str, short_name: str, unit: str, data: List[T]):
        self.Frequency = frequency
        self.Name = name.encode('utf-8')
        self.ShortName = short_name.encode('utf-8')
        self.Unit = unit.encode('utf-8')
        self.Data = data

    def write(
        self,
        fd: BinaryIO,
        n: int,
        channels_count: int,
        channels_meta_pointer: int,
        current_data_pointer: int,
    ) -> int:
        # Determine data type
        if isinstance(self.Data[0], float):
            data_type = DataTypeFloat32
            data_format = '<' + 'f' * len(self.Data)
        elif isinstance(self.Data[0], int):
            if all(-32768 <= x <= 32767 for x in self.Data):
                data_type = DataTypeInt16
                data_format = '<' + 'h' * len(self.Data)
            else:
                data_type = DataTypeInt32
                data_format = '<' + 'i' * len(self.Data)
        else:
            raise TypeError("Unsupported data type")

        previous_meta_pointer = 0
        next_meta_pointer = 0

        if n > 0:
            previous_meta_pointer = channels_meta_pointer + struct.calcsize(LdFileChannelMeta.FORMAT) * (n - 1)
        if n < channels_count - 1:
            next_meta_pointer = channels_meta_pointer + struct.calcsize(LdFileChannelMeta.FORMAT) * (n + 1)

        current_meta_pointer = channels_meta_pointer + struct.calcsize(LdFileChannelMeta.FORMAT) * n

        channel_meta = LdFileChannelMeta()
        channel_meta.PreviousMetaPointer = previous_meta_pointer
        channel_meta.NextMetaPointer = next_meta_pointer
        channel_meta.DataPointer = current_data_pointer
        channel_meta.DataLength = len(self.Data)
        channel_meta.ChannelId = 0x2EE1 + n
        channel_meta.DataType = data_type.DataType
        channel_meta.DataTypeLength = data_type.DataTypeLength
        channel_meta.Frequency = self.Frequency
        channel_meta.Name = self.Name
        channel_meta.ShortName = self.ShortName
        channel_meta.Unit = self.Unit

        # Pack data
        binary_data = struct.pack(data_format, *self.Data)

        # Write to file
        fd.seek(current_meta_pointer)
        fd.write(channel_meta.pack())

        fd.seek(current_data_pointer)
        fd.write(binary_data)

        # Return next data pointer
        next_data_pointer = current_data_pointer + len(binary_data)
        return next_data_pointer


class File:
    def __init__(self):
        self.Time = time.localtime()
        self.Driver = ''
        self.Vehicle = ''
        self.Venue = ''
        self.ShortComment = ''
        self.EventName = ''
        self.EventSession = ''
        self.EventComment = ''
        self.VehicleId = ''
        self.VehicleWeight = 0
        self.VehicleType = ''
        self.VehicleComment = ''
        self.Channels: List[Channel] = []

    def add_channels(self, *channels: Channel):
        self.Channels.extend(channels)

    def write(self, fd: BinaryIO):
        # Calculate pointers
        header_size = struct.calcsize(LdFileHead.FORMAT)
        event_size = struct.calcsize(LdFileEvent.FORMAT)
        venue_size = struct.calcsize(LdFileVenue.FORMAT)
        vehicle_size = struct.calcsize(LdFileVehicle.FORMAT)
        channel_meta_size = struct.calcsize(LdFileChannelMeta.FORMAT)

        event_pointer = header_size
        venue_pointer = event_pointer + event_size
        vehicle_pointer = venue_pointer + venue_size
        channels_meta_pointer = vehicle_pointer + vehicle_size
        channels_data_pointer = channels_meta_pointer + channel_meta_size * len(self.Channels)

        # Create the file header
        head = LdFileHead()
        head.ChannelsMetaPointer = channels_meta_pointer
        head.ChannelsDataPointer = channels_data_pointer
        head.EventPointer = event_pointer
        head.ChannelsCount = len(self.Channels)

        date_str = time.strftime("%d/%m/%Y", self.Time).encode('utf-8')
        time_str = time.strftime("%H:%M:%S", self.Time).encode('utf-8')
        head.Date = date_str
        head.Time = time_str
        head.Driver = self.Driver.encode('utf-8')
        head.Vehicle = self.Vehicle.encode('utf-8')
        head.Venue = self.Venue.encode('utf-8')
        head.ShortComment = self.ShortComment.encode('utf-8')

        # Create the Event
        event = LdFileEvent()
        event.VenuePointer = venue_pointer
        event.Name = self.EventName.encode('utf-8')
        event.Session = self.EventSession.encode('utf-8')
        event.Comment = self.EventComment.encode('utf-8')

        # Create the Venue
        venue = LdFileVenue()
        venue.VehiclePointer = vehicle_pointer
        venue.Name = self.Venue.encode('utf-8')

        # Create the Vehicle
        vehicle = LdFileVehicle()
        vehicle.Weight = self.VehicleWeight
        vehicle.Id = self.VehicleId.encode('utf-8')
        vehicle.Type = self.VehicleType.encode('utf-8')
        vehicle.Comment = self.VehicleComment.encode('utf-8')

        # Write to file
        fd.seek(0)
        fd.write(head.pack())

        fd.seek(event_pointer)
        fd.write(event.pack())

        fd.seek(venue_pointer)
        fd.write(venue.pack())

        fd.seek(vehicle_pointer)
        fd.write(vehicle.pack())

        # Write channels
        current_data_pointer = channels_data_pointer
        for i, channel in enumerate(self.Channels):
            current_data_pointer = channel.write(
                fd,
                i,
                head.ChannelsCount,
                channels_meta_pointer,
                current_data_pointer
            )