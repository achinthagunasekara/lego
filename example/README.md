# Example

You can try out `Lego Configuraiton Management Tool` using this example.

Run the following command within `example` directory to build a Docker image with Python insatlled.

```
docker build . -t ubuntu-py
```

Once you build your new Docker image, start the image and mount this repo by running the following command.

```
docker run -t -i -v /PATH_TO_LEGO_REPO/lego:/mnt -p 8080:80 ubuntu-py /bin/bash
```

Once the container is tarted run the following commands to install Lego tool.

```
cd /mnt
python setup.py install
```

Once the Lego tool is installed run the following commands to configure the system using this example Builder files.

```
cd /mnt/example
lego build server.yaml
```
