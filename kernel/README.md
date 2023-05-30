# Kernel

## Run

- **下载依赖**

```
pip install -r requirements.txt
```

- **windows下打包**

```
cd .kernel
pyinstaller -F -c app.py --distpath ../app
```

打包前记得先删除之前的exe

打包后即可直接在app中运行，会自动拉起内核进程。

