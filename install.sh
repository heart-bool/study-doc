# jdk安装包路径
JDK_PACKAGE_DIR=$1
INSTALL_DIR=$2
BASH_PROFILE=$3

if [[ ! -d $INSTALL_DIR  ]]; then
    echo "first startup, mkdir ./jdk_1.8 ..."
    mkdir $INSTALL_DIR
    echo "mkdir ./jdk_1.8 success"
fi

tar -zxvf $JDK_PACKAGE_DIR -C $INSTALL_DIR

echo "export JAVA_HOME=$INSTALL_DIR" >> ${BASH_PROFILE}
echo 'export PATH=$PATH:$JAVA_HOME/bin:$JAVA_HOME/jre/bin:$PATH' >> ${BASH_PROFILE}
echo 'export CLASSPATH=.:$JAVA_HOME/lib:$JAVA_HOME/jre/lib' >> ${BASH_PROFILE}
source ${BASH_PROFILE}

echo ''
echo "install $JDK_PACKAGE_DIR to $INSTALL_DIR succeed"
