# Example

You can try out `Lego Configuraiton Management Tool` using this example.

Check out this repo to a local directory on your machine.

Make sure you have `Docker` installed.

Run the following command.

```
docker run -t -i -v /PATH_TO_LEGO_REPO/lego:/mnt -p 8080:80 ubuntu /mnt/example/run_example.sh
```

Run the following command to test the newly installed apache/php container.

```
curl -vs http://localhost:8080
```
