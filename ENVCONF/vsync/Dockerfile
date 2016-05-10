FROM ubuntu:latest
MAINTAINER "Tao"

ENV WORKSPACE /root

RUN apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys 3FA7E0328081BFF6A14DA29AA6A19B38D3D831EF && \
    echo "deb http://download.mono-project.com/repo/debian wheezy main" | tee /etc/apt/sources.list.d/mono-xamarin.list && \
    apt-get update && apt-get --yes install zsh \
    git \
    python \
    vim \
    curl && \
    curl https://bootstrap.pypa.io/get-pip.py | python && \
    pip install flask geopy moment && \
    git clone https://github.com/IronLanguages/main.git ${WORKSPACE}/ironPython && \
    echo "deb http://download.mono-project.com/repo/debian wheezy-apache24-compat main" | tee -a /etc/apt/sources.list.d/mono-xamarin.list && \
    apt-get --yes install mono-complete && \
    git clone https://github.com/taoalpha/XMate ${WORKSPACE}/xmate && \
    cp -f ${WORKSPACE}/xmate/Common.proj ${WORKSPACE}/ironPython/Solutions/Common.proj && \
    xbuild /p:Configuration=Release ${WORKSPACE}/ironPython/Solutions/IronPython.sln && \
    touch ipy && \
    echo '#!/bin/sh \nEXE_PATH=${WORKSPACE}/ironPython/bin/Release\nmono $EXE_PATH/ipy.exe "$@"' > ipy && \
    chmod +x ipy && \
    mv ipy /usr/local/bin/ && \
    echo "export IRONPYTHONPATH=${WORKSPACE}/ironPython/External.LCA_RESTRICTED/Languages/IronPython/27/Lib" >> ${WORKSPACE}/.bashrc && \
    mcs -target:library ${WORKSPACE}/xmate/Vsync.cs && \
    cp -f ${WORKSPACE}/xmate/Vsync.dll ${WORKSPACE}/ironPython/bin/Release && \
    rm -rf ${WORKSPACE}/ironPython/.git && \
    chmod +x ${WORKSPACE}/xmate/scripts/auto_start.sh && \
    crontab ${WORKSPACE}/xmate/scripts/crontab_config

WORKDIR ${WORKSPACE}
ENTRYPOINT ["sh","/root/xmate/scripts/auto_start.sh"]
