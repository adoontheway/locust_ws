#!/bin/bash
protoc --proto_path=src --python_out=../ src/Common.Message.proto
protoc --proto_path=src --python_out=../ src/Game.Common.proto
protoc --proto_path=src --python_out=../ src/ProxyServer.Message.proto
protoc --proto_path=src --python_out=../ src/HallServer.Message.proto
protoc --proto_path=src --python_out=../ src/GameServer.Message.proto
