# 爱奇艺视频下载

## 包管理工具:
pipenv

##运行
`python App.py http://cache.m.iqiyi.com/mus/224570001/73250e1b8f0f4ac63b7a9165bb7e8e7d/afbe8fd3d73448c9/1549574520/20180917/55/2e/b85880b8470b21a29e8f598846ac68ef.m3u8?vt=0&prv=0&qd_time=1555002380128&qd_originate=h5&ff=ts&bossStatus=2&src=02020031010000000000&tm=1555002380000&qd_uri=dash&sgti=15_e53550172f760cf29ad34a536009d201_1555002380000&qd_vip=1&k_uid=e53550172f760cf29ad34a536009d201&tvid=1331711800&previewTime=6&previewType=1&vf=c8d24c1c67233cf46c61dc2045253fef`

该链接地址是视频播放页面移动端 `video` 标签的 `src` 值，下载 vip 视频时候，只需要把你的 cookie 填写 `config.ini` 中即可。
