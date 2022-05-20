import socket

hote = ""
port = 15555

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((hote, port))
print("Connection on {}".format(port))

client.send("Hey my name is Olivier!")

print("Close")
client.close()