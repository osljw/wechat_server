
# dev



# deploy

安装Vercel CLI：
```
npm i -g vercel
```

然后，创建一个vercel.json文件：
```
{
 "version": 2,
 "builds": [
    {
      "src": "app.py",
      "use": "@vercel/python"
    }
 ],
 "routes": [
    {
      "src": "/wechat",
      "dest": "app.py"
    }
 ]
}

```
最后，使用Vercel CLI部署你的应用：
```
vercel
```
