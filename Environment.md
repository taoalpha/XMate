# Instructions for setting up Vsync within Docker container

### Get access to your Docker container image

```sh
docker run -ti IMAGE_NAME 
# The -i flag starts an interactive container. 
# The -t flag creates a pseudo-TTY that attaches stdin and stdout.
```
Your probably want to start with Ubuntu's image. Search ubuntu on [docker hub](http://www.mono-project.com/docs/getting-started/install/linux/#usage)

To install some basic packages, execute the following commands

``` sh
apt-get update
apt-get install python curl vim 
curl https://bootstrap.pypa.io/get-pip.py | python
pip install flask geopy moment
```

### Set up Mono on Linux/Ubuntu within Docker

See [mono-project.com](http://www.mono-project.com/docs/getting-started/install/linux/#usage)

### Set up IronPython on Linux/Ubuntu within Docker
#### Get source file

```
git clone https://github.com/IronLanguages/main.git YOUR_DIR
cd YOUR_DIR
```

#### Build

```
xbuild /p:Configuration=Release Solutions/IronPython.sln
```

If you see the following error:

> socket.cs(1900,63): error CS0117: `System.Net.Sockets.SocketOptionName' does not contain a definition for `IPv6Only'

See the accepted answer in [this post](http://stackoverflow.com/questions/28364592/compile-ironpython-with-mono).


Commands are deployed to the `YOUR_DIR/bin/Release` directory. You can run it with Mono

```
mono ipy.exe
``` 

#### Set Path

Create a new file named `ipy`

```
touch ipy
```

Put the following content in the `ipy` file you just created. `YOUR_PATH` should be the absolute path of `bin/Release`. (`YOUR_DIR/bin/Release`).

```
#!/bin/sh
EXE_PATH=YOUR_PATH

mono $EXE_PATH/ipy.exe "$@"
```

Move `ipy` to a directory that is listed in your PATH environment variable, e.g.

```
chmod +x ipy
mv ipy /usr/local/bin/ipy
```

Add `YOUR_DIR/IronLanguages/External.LCA_RESTRICTED/Languages/IronPython/27/Lib` to an IRONPYTHONPATH environment variable so that it can find some basic python modules supported by IronPython.

Now, type `ipy` in the command and you should see IronPython prompt.

```
IronPython 2.7.6a0 (2.7.6.0) on Mono 4.0.30319.17020 (64-bit)
Type "help", "copyright", "credits" or "license" for more information.
```

### Set up Vsync on Linux/Ubuntu within Docker

First, download Vsync.cs from [Vsync's website](https://vsync.codeplex.com) to your local machine.

Copy the Vsync.cs file from your local machine to your Docker container

```
cp YOUR_LOCAL_DIR/Vsync.cs CONTAINER_ID:YOUR_DIR/Vsync.cs
```

Compile Vsync in your container
```
mcs -target:library Vsync.cs
```

Then copy the generated Vsync.dll file to `YOUR_DIR/bin/Release`.

### Update the container image
Type `exit` in your container command line to exit the image. The following commands should be executed on your local machine:

```sh
docker ps -n 1 # get the info of the most recent executed image
docker commit -a "AUTHOR_NAME" -m "COMMENT" CONTAINER_ID IMAGE_NAME # commit, the same idea as using git commit
docker push YOUR_ACCOUNT_NAME/IMAGE_NAME # push to docker hub
```

**Reference**

[https://github.com/IronLanguages/main/wiki/Building#wiki_building-mono](https://github.com/IronLanguages/main/wiki/Building#wiki_building-mono)
[http://stackoverflow.com/questions/28364592/compile-ironpython-with-mono](http://stackoverflow.com/questions/28364592/compile-ironpython-with-mono)
[http://stackoverflow.com/questions/25600874/how-to-install-ironpython-on-ubuntu-14-01/25673910#25673910](http://stackoverflow.com/questions/25600874/how-to-install-ironpython-on-ubuntu-14-01/25673910#25673910)