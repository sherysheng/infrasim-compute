'''
*********************************************************
Copyright @ 2018 Dell EMC Corporation All Rights Reserved
*********************************************************
'''

import mmap
import os

import posix_ipc


class CShareMemory:
    handle_memory = None
    handle_file = None

    def create(self, key_name, size):
        if self.handle_memory is not None:
            raise Exception()
        if self.handle_file is not None:
            raise Exception()
        flags = posix_ipc.O_CREAT  # posix_ipc.O_CREX
        self.handle_memory = posix_ipc.SharedMemory(key_name, flags, mode=0644, size=size)
        self.handle_file = mmap.mmap(self.handle_memory.fd, self.handle_memory.size)
        return self.handle_file

    def open(self, key_name):
        if self.handle_memory is not None:
            raise Exception()
        if self.handle_file is not None:
            raise Exception()
        flags = 0  # open it
        self.handle_memory = posix_ipc.SharedMemory(key_name, flags, mode=0644)
        self.handle_file = mmap.mmap(self.handle_memory.fd, self.handle_memory.size)
        return self.handle_file

    def close(self):
        if self.handle_memory is None:
            raise Exception()
        if self.handle_file is None:
            raise Exception()
        self.handle_file.close()
        self.handle_memory.close_fd()

    def write(self, position, src):
        self.handle_file.seek(position, os.SEEK_SET)
        self.handle_file.write(src)

    def read(self, position, length):
        self.handle_file.seek(position, os.SEEK_SET)
        return self.handle_file.read(length)
