import docker
client=docker.from_env()
# print(client.containers.run("alpine",["echo","hello","world"]))
containers = client.containers.list(all=True, filters={"name": "endserverContainer"})
print(containers)
if not containers:
    client.containers.run("endserver", name="endserverContainer", detach=True, network="cloudtemp")
    print("End Server container started.")
#     logger.debug("End Server container started.")
else:
    print("End Server container is already running.")
#     logger.debug("End Server container is already running.")